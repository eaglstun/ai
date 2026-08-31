#!/usr/bin/env python3
"""
Stamp every content page with a semantic ID, plus the tags used to compute it.

A semantic ID is a 192-bit, 32-character base64url string whose bits ARE the meaning of
the page. Two pages about the same thing get IDs that are close in Hamming distance
(count of differing bits). So `related posts` becomes an XOR and a popcount, with no
vector database, no server, and no runtime dependency at all.

    ┌──────────────── 172 bits semantic ────────────────┬── 16b day ──┬─ 4b hash ─┐
    │  sign(v[i] - frozenMean[i]),  i = 0..171          │ since 2026  │ tiebreak  │
    └───────────────────────────────────────────────────┴─────────────┴───────────┘
    192 bits = 24 bytes = exactly 32 base64url chars, no padding

This also writes `related_by_meaning` (the nearest neighbours, by Hamming distance) into
frontmatter, which the theme renders directly. The same IDs drive the client-side search
at /search/ — see themes/ee-ai/static/js/search.js, which DUPLICATES the bit constants
below. Change them here and you must change them there, or search silently ranks noise.

Two properties this script guarantees, because a frontmatter field committed to git
is forever:

  IDEMPOTENT   Re-running produces byte-identical IDs. The 4 "random" tiebreak bits
               are derived from a content hash, not a PRNG. Pages that already have a
               semantic_id keep it untouched unless you pass --force.

  STABLE       The mean vector is computed ONCE, written to data/semantic-model.json,
               and never recomputed. This is the whole ballgame: binarization is
               sign(v - mean), so if the mean drifts as the blog grows, every
               previously-issued ID silently becomes wrong — no error, no warning,
               just quietly incomparable numbers. Freeze it and new posts stay
               comparable to old ones forever.

Requires Ollama running locally with `nomic-embed-text` (embeddings) and a small chat
model (tag generation). Standard library only.

    python3 scripts/semantic-ids.py              # fill in what's missing
    python3 scripts/semantic-ids.py --force      # re-mint everything
    python3 scripts/semantic-ids.py --dry-run    # show what would change
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MODEL_FILE = ROOT / "data" / "semantic-model.json"

OLLAMA = "http://127.0.0.1:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen35-cl46-abl-9b:latest"

# ── why base64url and not hex ─────────────────────────────────────────────────
#
# Hex spends 4 bits per character — one nibble — and throws the other half of every
# character's capacity away. Base64 spends 6. At a fixed 32-character width that's the
# difference between 128 bits and 192, i.e. 108 semantic bits vs 172, for free.
#
# The sizes land perfectly: 192 bits = 24 bytes, and base64 encodes 3 bytes into 4
# characters, so 24 bytes is exactly 32 characters with NO padding and no ragged edge.
#
# 64 rather than 62 (plain alphanumerics) because 64 is a power of two: encoding is
# then pure bit-shifting instead of bignum long division, and you gain 2 bits. The
# `-` and `_` of base64URL (rather than base64's `+` and `/`) keep the IDs safe in
# URLs and filenames, which matters for a static site.

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

SEMANTIC_BITS = 172
DAY_BITS = 16
HASH_BITS = 4
TOTAL_BITS = SEMANTIC_BITS + DAY_BITS + HASH_BITS  # 192 = 24 bytes = 32 base64 chars
ID_CHARS = TOTAL_BITS // 6

EPOCH = date(2026, 1, 1)

TAG_COUNT = 6

# ── related_by_meaning ────────────────────────────────────────────────────────
#
# The distance function is an XOR and a popcount, but it has to run SOMEWHERE, and Go
# templates have no popcount. So it runs here, at mint time, and Hugo just renders a
# list. Zero runtime cost, no JS, nothing to deploy.
#
# The cutoff is not a vibe. Across this corpus, two pages picked at random differ by ~87
# of the 172 semantic bits, which is chance, since half of 172 is 86. Unrelated pages
# sit at a coin flip, as they should. The 5th percentile of all pairs is 70 bits, so
# RELATED_MAX_DISTANCE = 72 means "closer than roughly 95% of random pairs". Above it,
# you are just ranking noise and calling the winner a recommendation.
RELATED_COUNT = 4
RELATED_MAX_DISTANCE = 72


# ── ollama ────────────────────────────────────────────────────────────────────


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{OLLAMA}{path}",
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())
    except urllib.error.URLError as e:
        sys.exit(f"ollama unreachable at {OLLAMA}: {e}\nIs `ollama serve` running?")


def embed(texts: list[str]) -> list[list[float]]:
    # nomic wants a task prefix; documents and queries land in slightly different
    # regions of the space on purpose.
    out = post("/api/embed", {"model": EMBED_MODEL, "input": [f"search_document: {t}" for t in texts]})
    return out["embeddings"]


# Tags come from a CONTROLLED VOCABULARY, not the model's imagination.
#
# Free-form tag generation was tried first and produced `aspartame-grade-ml`,
# `sepahora-bot`, and `three-hours-150-dollars` — the model shredding title fragments
# into tag-shaped noise, then bolting `attention-mechanism` onto essays about labour
# policy. Those tags feed the embedding text, so junk tags mean junk vectors: strictly
# worse than no tags at all.
#
# A fixed vocabulary fixes all of it. The model now CHOOSES rather than INVENTS,
# anything off-list is dropped, tags are consistent across posts (so they're a real
# taxonomy you could browse), and every tag matching a glossary slug is a free
# cross-link to /glossary/<slug>/.

# Site-level topics the glossary doesn't cover. Glossary slugs are appended at runtime.
EXTRA_VOCAB = [
    "ai-policy", "ai-safety", "apple-silicon", "consciousness", "context-window",
    "datasets", "deployment", "diffusion", "fine-tuning", "hugo", "image-generation",
    "inference", "labour", "local-inference", "music-generation", "open-weights",
    "prompt-engineering", "quantization", "rag", "search", "speech-to-text",
    "static-sites", "tooling", "training", "vector-search",
]
# Deliberately NOT in the vocabulary: "writing", "ai", "technology". Every post here is
# writing about AI — a tag that is true of everything carries zero discriminative signal.
# It is the taxonomy version of a dead bit: address space you paid for and cannot use.


def build_vocab() -> list[str]:
    glossary = sorted(
        p.stem for p in (CONTENT / "glossary").glob("*.md") if p.stem != "_index"
    )
    return sorted(set(glossary) | set(EXTRA_VOCAB))


def generate_tags(title: str, summary: str, body: str, vocab: list[str]) -> list[str]:
    prompt = (
        f"Choose the tags that describe this article.\n\n"
        f"Title: {title}\n"
        f"Summary: {summary}\n\n"
        f"Excerpt:\n{body[:1500]}\n\n"
        f"ALLOWED TAGS (you may ONLY use tags from this list):\n{', '.join(vocab)}\n\n"
        f"Pick between 2 and {TAG_COUNT} tags that genuinely describe this article. "
        f"Fewer is better than wrong. Do NOT invent tags. Do NOT pick a tag just because "
        f"it sounds technical — only pick it if the article is actually about it.\n"
        f"Respond with ONLY a comma-separated list from the allowed tags, nothing else."
    )
    out = post(
        "/api/generate",
        {"model": CHAT_MODEL, "prompt": prompt, "stream": False, "think": False, "options": {"temperature": 0.1}},
    )
    raw = out.get("response", "")
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.S)  # some models think out loud

    allowed = set(vocab)
    tags = []
    for t in re.split(r"[,\n]", raw):
        t = t.strip().strip("-*`.").lower()
        # Anything the model made up is dropped on the floor. That's the whole point.
        if t in allowed and t not in tags:
            tags.append(t)
    return tags[:TAG_COUNT]


# ── frontmatter ───────────────────────────────────────────────────────────────

FM = re.compile(r"\A\+\+\+\n(.*?)\n\+\+\+\n", re.S)


def toml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse(path: Path) -> tuple[dict, str, str]:
    """→ (fields, frontmatter_text, body). Values stay as raw TOML source."""
    text = path.read_text()
    m = FM.match(text)
    if not m:
        return {}, "", text

    fields = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([a-z_][a-z0-9_]*)\s*=\s*(.*)$", line)
        if km:
            fields[km.group(1)] = km.group(2).strip()
    return fields, m.group(1), text[m.end() :]


def unquote(v: str) -> str:
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def set_fields(fm_text: str, updates: dict[str, str]) -> str:
    """Replace or append `key = value` lines, preserving everything else verbatim."""
    lines = fm_text.splitlines()
    for key, value in updates.items():
        line = f"{key} = {value}"
        for i, existing in enumerate(lines):
            if re.match(rf"^{key}\s*=", existing):
                lines[i] = line
                break
        else:
            lines.append(line)
    return "\n".join(lines)


# ── the ID ────────────────────────────────────────────────────────────────────


def days_since_epoch(fields: dict) -> int:
    """Undated pages (the glossary) get day 0. Stable, and honest about having no date."""
    raw = fields.get("date")
    if not raw:
        return 0
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if not m:
        return 0
    d = (date(int(m.group(1)), int(m.group(2)), int(m.group(3))) - EPOCH).days
    return max(0, min(d, (1 << DAY_BITS) - 1))


def encode64(bits: int) -> str:
    """192 bits → 32 base64url characters. Six bits per character, big-endian."""
    return "".join(
        ALPHABET[(bits >> (TOTAL_BITS - 6 * (i + 1))) & 0x3F] for i in range(ID_CHARS)
    )


def decode64(text: str) -> int:
    bits = 0
    for ch in text:
        bits = (bits << 6) | ALPHABET.index(ch)
    return bits


def mint(vector: list[float], mean: list[float], days: int, text: str) -> str:
    """
    sign(v - mean) for the top 172 dims, then the tail.

    Mean-centering is NOT optional: raw embedding dims aren't zero-centered, so a naive
    sign() emits bits that are constant across the whole corpus. Dead bits — address
    space you paid for and cannot use.
    """
    bits = 0
    for i in range(SEMANTIC_BITS):
        bits = (bits << 1) | (1 if vector[i] - mean[i] > 0 else 0)

    bits = (bits << DAY_BITS) | days

    # Deterministic tiebreak, so re-running the script never changes an ID.
    tie = int(hashlib.sha256(text.encode()).hexdigest(), 16) & ((1 << HASH_BITS) - 1)
    bits = (bits << HASH_BITS) | tie

    return encode64(bits)


def hamming(a: str, b: str) -> int:
    """
    Semantic distance. Masks off the day/tiebreak tail — those bits are NOISE.

    Note there is no dash-stripping here: `-` is a legitimate base64url character, so
    treating it as a separator (as the old hex/UUID format required) would silently
    corrupt the comparison.
    """
    mask = ((1 << SEMANTIC_BITS) - 1) << (DAY_BITS + HASH_BITS)
    x = (decode64(a) ^ decode64(b)) & mask
    return bin(x).count("1")


def page_ref(path: Path) -> str:
    """content/blog/foo/index.md -> /blog/foo/, the ref Hugo's site.GetPage resolves."""
    rel = path.relative_to(CONTENT)
    parts = list(rel.parts[:-1]) if rel.stem == "index" else [*rel.parts[:-1], rel.stem]
    return "/" + "/".join(parts) + "/"


def is_listable(d: dict) -> bool:
    """Section list pages are not destinations. The glossary keeps its curated See-also."""
    return d["path"].stem != "_index" and d["path"].relative_to(CONTENT).parts[0] != "glossary"


# ── main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-mint IDs and re-tag pages that already have them")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    args = ap.parse_args()

    pages = sorted(p for p in CONTENT.rglob("*.md"))
    print(f"{len(pages)} pages under content/\n")

    docs = []
    for path in pages:
        fields, fm_text, body = parse(path)
        if not fields.get("title"):
            print(f"  skip (no frontmatter): {path.relative_to(ROOT)}")
            continue
        docs.append({"path": path, "fields": fields, "fm": fm_text, "body": body})

    # ── tags ──────────────────────────────────────────────────────────────────
    vocab = build_vocab()
    need_tags = [d for d in docs if args.force or "tags" not in d["fields"]]
    print(f"generating tags for {len(need_tags)} pages with {CHAT_MODEL}")
    print(f"  (controlled vocabulary of {len(vocab)} tags — anything off-list is dropped)\n")

    for i, d in enumerate(need_tags, 1):
        title = unquote(d["fields"]["title"])
        summary = unquote(d["fields"].get("summary", ""))
        tags = generate_tags(title, summary, d["body"], vocab)
        d["tags"] = tags
        print(f"  [{i}/{len(need_tags)}] {title[:44]:44} → {', '.join(tags)}")

    for d in docs:
        if "tags" not in d:
            raw = d["fields"].get("tags", "[]")
            d["tags"] = [unquote(t.strip()) for t in raw.strip("[]").split(",") if t.strip()]

    # ── the text we actually embed ────────────────────────────────────────────
    # Title + summary + tags. NOT the body: an embedding is a fixed-size container, so
    # a whole article averages into a vague blob that is near everything and about
    # nothing. One embedding should hold about one idea.
    for d in docs:
        title = unquote(d["fields"]["title"])
        summary = unquote(d["fields"].get("summary", ""))
        d["text"] = f"{title}. {summary} Topics: {', '.join(d['tags'])}."

    print(f"\nembedding {len(docs)} pages with {EMBED_MODEL}...")
    vectors = embed([d["text"] for d in docs])
    for d, v in zip(docs, vectors):
        d["vector"] = v

    # ── the frozen mean ───────────────────────────────────────────────────────
    if MODEL_FILE.exists():
        model = json.loads(MODEL_FILE.read_text())
        mean = model["mean"]
        print(f"using FROZEN mean from {MODEL_FILE.relative_to(ROOT)} "
              f"(trained on {model['trained_on']} pages, {model['trained_at']})")
        if model.get("embed_model") != EMBED_MODEL:
            sys.exit(f"model file was built with {model.get('embed_model')}, not {EMBED_MODEL} — IDs would be incomparable")
    else:
        dims = len(vectors[0])
        mean = [sum(v[i] for v in vectors) / len(vectors) for i in range(dims)]
        model = {
            "embed_model": EMBED_MODEL,
            "semantic_bits": SEMANTIC_BITS,
            "day_bits": DAY_BITS,
            "hash_bits": HASH_BITS,
            "epoch": EPOCH.isoformat(),
            "trained_on": len(docs),
            "trained_at": date.today().isoformat(),
            "mean": mean,
        }
        print(f"computing mean from {len(docs)} pages and FREEZING it → {MODEL_FILE.relative_to(ROOT)}")
        print("  (never recompute this: every existing ID would silently become wrong)")
        if not args.dry_run:
            MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
            MODEL_FILE.write_text(json.dumps(model))

    # ── mint ──────────────────────────────────────────────────────────────────
    minted = 0
    for d in docs:
        existing = unquote(d["fields"].get("semantic_id", ""))
        if existing and not args.force:
            d["id"] = existing  # IDs are forever. Only --force re-mints.
            d["fresh"] = False
            continue
        d["id"] = mint(d["vector"], mean, days_since_epoch(d["fields"]), d["text"])
        d["fresh"] = True
        minted += 1

    # ── related_by_meaning ────────────────────────────────────────────────────
    # Unlike the IDs, these are recomputed for EVERY page on every run, and they have
    # to be. A new post is a new neighbour for pages that were minted a year ago, and
    # nothing about rewriting a derived list of slugs can corrupt an ID.
    #
    # Drafts and future-dated posts stay in the list. They are NOT filtered here: the
    # template resolves each ref through site.GetPage, which yields nothing for a page
    # the production build never emitted. So the block self-heals as the publishing
    # calendar rolls forward, and a live post can't render a link into an unpublished
    # one. The failure CLAUDE.md warns about, made structurally impossible instead of
    # something you have to remember.
    #
    # `unlisted = true` pages are dropped from the POOL but still get a list of their
    # own: nothing links to them, they link out. Without this the next run would
    # quietly re-add an unlisted post to some neighbour's related_by_meaning and put
    # back the inbound link that unlisting exists to prevent.
    pool = [d for d in docs
            if d["path"].stem != "_index" and d["fields"].get("unlisted") != "true"]
    for d in docs:
        if not is_listable(d):
            continue
        near = sorted(
            ((hamming(d["id"], o["id"]), o) for o in pool if o is not d),
            key=lambda x: x[0],
        )
        d["related"] = [page_ref(o["path"]) for dist, o in near[:RELATED_COUNT] if dist <= RELATED_MAX_DISTANCE]

    # ── write ─────────────────────────────────────────────────────────────────
    written = 0
    for d in docs:
        updates = {}
        if d["fresh"]:
            updates["tags"] = "[" + ", ".join(toml_str(t) for t in d["tags"]) + "]"
            updates["semantic_id"] = toml_str(d["id"])
        if "related" in d:
            value = "[" + ", ".join(toml_str(r) for r in d["related"]) + "]"
            if value != d["fields"].get("related_by_meaning"):
                updates["related_by_meaning"] = value
        if not updates:
            continue
        if not args.dry_run:
            fm = set_fields(d["fm"], updates)
            d["path"].write_text(f"+++\n{fm}\n+++\n{d['body']}")
        written += 1

    verb = "would write" if args.dry_run else "wrote"
    print(f"\nminted {minted} new IDs; {verb} {written} files "
          f"(related lists ≤ {RELATED_MAX_DISTANCE} bits, top {RELATED_COUNT})")

    # ── does it actually work? ────────────────────────────────────────────────
    print("\nnearest neighbours by Hamming distance on the IDs alone:")
    for d in docs[:6]:
        others = sorted(
            ((hamming(d["id"], o["id"]), o) for o in docs if o is not d),
            key=lambda x: x[0],
        )[:3]
        print(f"\n  {unquote(d['fields']['title'])}")
        print(f"  {d['id']}")
        for dist, o in others:
            print(f"    {dist:3d} bits  {unquote(o['fields']['title'])}")


if __name__ == "__main__":
    main()
