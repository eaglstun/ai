#!/usr/bin/env python3
"""Phase-1 prototype: generate 4 concept images for a post into concepts/<slug>/.

Usage:
  python3 scripts/gen-concepts.py --slug <post-slug> \
      --brief "one-line visual subject" \
      --pairs together:kodachrome,drawthings:gag-panel,pollinations:collage,replicate:continuous-line \
      [--fallback together]

Engines: together (FLUX.1.1-pro), drawthings (local :7860), pollinations,
replicate (recraft-v3). On engine failure the style is retried once on the
--fallback engine (noted in notes.md); if that fails too, we move on.
Stdlib only. See concepts/README.md for the whole program.
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STYLES = {
    "gag-panel": "Single-panel magazine cartoon, black ink and soft gray wash, generous "
                 "white space, one clear witty visual idea, minimal background detail",
    "continuous-line": "Sophisticated editorial illustration drawn as one continuous "
                       "unbroken black line on cream paper, abstract, witty, mid-century",
    "kodachrome": "1950s mid-century American illustration, warm Kodachrome palette, "
                  "aged paper grain, cheerful retro-futurist",
    "woodcut": "Antique woodcut engraving, dense cross-hatching, Victorian scientific "
               "catalog energy, black ink on aged cream paper",
    "risograph": "Two-color risograph print, coarse halftone grain, slightly "
                 "misregistered fluorescent pink and teal inks, flat shapes, zine energy",
    "collage": "Surreal paper cutout collage of old photographs and engravings with "
               "visible torn edges, absurdist animation energy",
    "ink-wash-dark": "Moody ink wash illustration, deadpan gothic humor, soft gray "
                     "washes with deep blacks, quiet menace played straight",
    "blueprint": "Technical blueprint, crisp white linework on deep cyanotype blue, "
                 "precise draftsmanship of an absurd machine, exploded views and "
                 "annotation arrows",
}
SUFFIX = " No text, no words, no letters, no watermark."
W, H = 1024, 768


def http(url, data=None, headers=None, timeout=180):
    h = {"User-Agent": "Mozilla/5.0 (gen-concepts prototype)"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def save(raw, out):
    """
    Write bytes as a REAL jpeg, whatever the engine actually handed us.

    Replicate returns WebP. Saved under a `.jpg` name it looks fine, opens fine, and
    previews fine - and then the day that image wins and becomes a post thumbnail, Hugo's
    image pipeline dies with `image: unknown format` and the whole build fails. A lie in
    the file extension is a bug with a very long fuse.

    sips is macOS-stock, so this stays dependency-free.
    """
    out.write_bytes(raw)
    if raw[:3] == b"\xff\xd8\xff":  # already a jpeg
        return
    subprocess.run(["sips", "-s", "format", "jpeg", str(out), "--out", str(out)],
                   check=True, capture_output=True)


def gen_together(prompt, out):
    body = json.dumps({"model": "black-forest-labs/FLUX.1.1-pro", "prompt": prompt,
                       "width": W, "height": H, "steps": 25, "n": 1}).encode()
    r = json.loads(http("https://api.together.xyz/v1/images/generations", body,
                        {"Authorization": f"Bearer {os.environ['TOGETHER_API_KEY']}",
                         "Content-Type": "application/json"}))
    save(http(r["data"][0]["url"]), out)


def gen_drawthings(prompt, out):
    body = json.dumps({"prompt": prompt, "negative_prompt": "text, words, letters, "
                       "watermark, signature", "width": W, "height": H,
                       "steps": 22}).encode()
    r = json.loads(http("http://127.0.0.1:7860/sdapi/v1/txt2img", body,
                        {"Content-Type": "application/json"}, timeout=420))
    save(base64.b64decode(r["images"][0]), out)


def gen_pollinations(prompt, out):
    q = urllib.parse.quote(prompt)
    save(http(f"https://image.pollinations.ai/prompt/{q}"
              f"?width={W}&height={H}&nologo=true&model=flux", timeout=240), out)


def gen_replicate(prompt, out):
    body = json.dumps({"input": {"prompt": prompt, "size": "1365x1024"}}).encode()
    r = json.loads(http(
        "https://api.replicate.com/v1/models/recraft-ai/recraft-v3/predictions", body,
        {"Authorization": f"Bearer {os.environ['REPLICATE_API_TOKEN']}",
         "Content-Type": "application/json", "Prefer": "wait"}, timeout=300))
    url = r["output"] if isinstance(r["output"], str) else r["output"][0]
    save(http(url), out)   # recraft-v3 hands back WebP, not jpeg


ENGINES = {"together": gen_together, "drawthings": gen_drawthings,
           "pollinations": gen_pollinations, "replicate": gen_replicate}


def post_context(slug):
    for md in list(ROOT.glob(f"content/*/{slug}.md")) + \
              list(ROOT.glob(f"content/*/{slug}/index.md")) + \
              list(ROOT.glob(f"content/*/*/{slug}.md")):
        fm = md.read_text().split("+++")[1]
        title = re.search(r'(?m)^title = "(.*)"', fm)
        summary = re.search(r'(?m)^summary = "(.*)"', fm)
        return (title.group(1) if title else slug,
                summary.group(1) if summary else "")
    return slug, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--brief", default="")
    ap.add_argument("--pairs", required=True,
                    help="comma list of engine:style")
    ap.add_argument("--fallback", default="together")
    ap.add_argument("--letters", default="abcd",
                    help="slot letters matching --pairs (for partial redos)")
    args = ap.parse_args()

    title, summary = post_context(args.slug)
    subject = args.brief or summary or title
    outdir = ROOT / "concepts" / args.slug
    outdir.mkdir(parents=True, exist_ok=True)

    notes = [f"# Concepts: {title}", "", f"subject: {subject}", ""]
    results = []
    letters = args.letters
    for i, pair in enumerate(args.pairs.split(",")):
        engine, style = pair.split(":")
        prompt = f"{STYLES[style]}. Subject: {subject}.{SUFFIX}"
        name = f"{letters[i]}-{engine}-{style}.jpg"
        out = outdir / name
        used = engine
        t0 = time.time()
        try:
            ENGINES[engine](prompt, out)
        except Exception as e:
            notes.append(f"- {name}: FAILED on {engine} ({e}); retrying on "
                         f"{args.fallback}")
            used = args.fallback
            name = f"{letters[i]}-{used}-{style}.jpg"
            out = outdir / name
            try:
                ENGINES[used](prompt, out)
            except Exception as e2:
                notes.append(f"- {name}: fallback FAILED too ({e2}); skipped")
                continue
        secs = round(time.time() - t0, 1)
        kb = out.stat().st_size // 1024
        notes.append(f"- {name}: {used} / {style}, {secs}s, {kb}KB")
        notes.append(f"  prompt: {prompt}")
        notes.append("  verdict: (pending)")
        results.append((name, used, style))
        print(f"ok {name} ({secs}s)")

    mode = "a" if (outdir / "notes.md").exists() else "w"
    with open(outdir / "notes.md", mode) as f:
        f.write("\n".join(notes if mode == "w" else notes[3:]) + "\n")

    cells = "\n".join(
        f'<figure><img src="{n}"><figcaption>{n[0].upper()}: {u} / {s}'
        f"</figcaption></figure>" for n, u, s in results)
    (outdir / "contact-sheet.html").write_text(
        "<!doctype html><meta charset=utf-8><title>" + args.slug + "</title>"
        "<style>body{font:16px Georgia;margin:2rem;background:#f4efe4}"
        "main{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:1200px}"
        "img{width:100%;border:1px solid #999}figcaption{font-style:italic;"
        "margin-top:.4rem}</style><h1>" + title + "</h1><main>" + cells + "</main>")
    print(f"wrote {outdir}/notes.md and contact-sheet.html "
          f"({len(results)}/4 images)")


if __name__ == "__main__":
    main()
