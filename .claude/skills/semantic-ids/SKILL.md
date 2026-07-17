---
name: semantic-ids
version: 1.0.0
description: The `semantic_id` and `tags` frontmatter on every page of ai.ericeaglstun.com - a 192-bit base64url string whose bits ARE the meaning of the page, so "related posts" is an XOR and a popcount with no vector database. Use when adding or editing content (new posts need an ID minted), when touching `scripts/semantic-ids.py` or `scripts/gen-glossary.py`, when building any related-posts / similar-content / tag feature, when a `semantic_id` looks wrong or two obviously-related pages score as unrelated, or when anything proposes recomputing the corpus mean or changing the bit layout. Read this BEFORE editing frontmatter by hand - several innocent-looking edits corrupt every ID on the site silently, with no error.
---

# Semantic IDs

Every content page carries two generated frontmatter fields:

```toml
tags = ["apple-silicon", "music-generation", "mps", "transformer"]
semantic_id = "cDVwp8E6PRQG8aNhbveXU8LHSdT7EAsO"   # ← 32 chars, base64url
```

The `semantic_id` is not a random identifier. **Its bits are the meaning of the page.**
It's a binary-quantized text embedding: two pages about the same thing get IDs that are
close in **Hamming distance** (the count of differing bits). So "find related posts"
becomes an XOR and a popcount over a frontmatter string — no vector database, no server,
no runtime dependency, nothing to deploy.

```
┌──────────────── 172 bits semantic ────────────────┬── 16b day ──┬─ 4b hash ─┐
│  sign(embedding[i] - frozenMean[i]),  i = 0..171  │ since 2026  │ tiebreak  │
└───────────────────────────────────────────────────┴─────────────┴───────────┘
 192 bits total = 24 bytes = exactly 32 base64url chars, no padding
```

It works. These neighbours were found using nothing but the ID strings:

| page                                     | nearest neighbour                | distance      |
| ---------------------------------------- | -------------------------------- | ------------- |
| Everyone Deserves a Mascara Treat        | Why the Sephora Bot Has No Floor | 56 / 172 bits |
| A Conscience You Can Patch Out Overnight | The Bill Comes Due               | 60 / 172      |
| A Crutch and a Lever                     | the **Alignment** glossary entry | 61 / 172      |

## Running it

```bash
python3 scripts/semantic-ids.py            # mint IDs + tags for pages missing them
python3 scripts/semantic-ids.py --dry-run  # report, write nothing
python3 scripts/semantic-ids.py --force    # re-mint EVERYTHING (see the rules below)
```

Needs Ollama running with `nomic-embed-text` (embeddings) and `qwen35-cl46-abl-9b`
(tag selection). Standard library only — no pip, no npm, consistent with the repo's
no-dependencies rule.

**New posts:** just run it with no flags. It only touches pages that lack a
`semantic_id`, and it is idempotent — the "random" tiebreak bits come from a content
hash, not a PRNG, so re-running never changes an existing ID.

## The four rules

Break any of these and the IDs corrupt **silently** — no error, no warning, just
quietly wrong distances that still look like plausible numbers.

**1. `data/semantic-model.json` is frozen. Never recompute it.**
It holds the 768-float corpus mean, and binarization is `sign(v - mean)`. That mean was
computed once, from the corpus as it stood, and it is the shared reference frame every
ID is measured against. Recompute it on a grown corpus and _every previously-issued ID
becomes wrong_ — they were minted against a different origin. The script only writes the
file if it doesn't already exist. Do not delete it. Do not "refresh" it.
(It is independent of the bit count, so changing `SEMANTIC_BITS` requires re-minting but
_not_ retraining.)

**2. `-` is a character in the ID, not a separator.**
The ID is base64url, whose alphabet is `A–Z a–z 0–9 - _`. It used to be hex and looked
like a UUID, which invites a reflexive `.replace("-", "")`. Do that now and you delete
real bits out of the middle of the ID. Use `decode64()` in `scripts/semantic-ids.py`.

**3. Always compare through the mask.**
The bottom 20 bits are a date and a tiebreak hash. To Hamming distance they are pure
**noise** — two identical pages published a year apart differ by ~10 tail bits for no
semantic reason. Use the `hamming()` helper, which masks them off. Comparing raw IDs is
the single most likely way to make this system look broken when it isn't.

**4. Tags come from a controlled vocabulary. Never free-form.**
`build_vocab()` = the glossary slugs + `EXTRA_VOCAB`. Anything the model invents that
isn't on the list is dropped on the floor. This is not fussiness: free-form generation
produced `aspartame-grade-ml`, `sepahora-bot`, and `three-hours-150-dollars`, and bolted
`attention-mechanism` onto essays about labour policy. **Tags feed the embedding text**,
so junk tags mean junk vectors — strictly worse than no tags at all.

Also: never add a tag that would be true of every post (`writing`, `ai`, `technology`).
A tag that describes everything discriminates nothing. It's the taxonomy version of a
dead bit — address space you paid for and can't use.

## `gen-glossary.py` will eat the IDs if you let it

`scripts/gen-glossary.py` rewrites all 36 glossary pages' frontmatter **from scratch**
on every run. It preserves `tags` and `semantic_id` via `carry_over()`. If you refactor
that script's frontmatter block, **preserve those two fields** or you destroy every
glossary ID. There is no way to regenerate them except re-minting — and re-minting is
fine, but only because the mean is frozen (rule 1).

## What gets embedded

`title + summary + tags`. **Not the body.**

An embedding is a fixed-size container — 768 floats whether you hand it a sentence or an
entire essay. Feed it a whole article and you get the _centroid_ of everything in it: a
vector that is near everything and specifically about nothing. One embedding should hold
about one idea. The hand-written `summary` on each page is already the best possible
one-sentence description of it, which is why nothing here generates summaries.

## Related posts: `related_by_meaning`

Built, and precomputed at mint time — the only sane answer for a static site. Go
templates have no popcount, so the XOR runs in Python and Hugo just renders a list.
Zero runtime cost, zero JS, nothing to deploy.

```toml
related_by_meaning = ["/blog/a-conscience-you-can-patch-out-overnight/", "/blog/the-middle-is-crowded/", ...]
```

`semantic-ids.py` writes up to `RELATED_COUNT` (6) neighbours within
`RELATED_MAX_DISTANCE` (72 bits) on every non-glossary page;
`themes/ee-ai/layouts/partials/related-by-meaning.html` renders the first 3 that
resolve. Glossary pages don't get the field — they have hand-curated "See also" chips,
and `gen-glossary.py` would eat it anyway. They remain _candidates_, though, which is
how the Temperature post ends up pointing at the **Temperature** glossary entry.

**Why 72 bits.** Two random pages differ by ~87 of the 172 semantic bits, which is
chance (half of 172 is 86) — unrelated pages sit at a coin flip, exactly as they should.
The 5th percentile of all pairs is 70. So 72 means "closer than ~95% of random pairs."
Past that you are ranking noise and calling the winner a recommendation.

**Unlike the IDs, these lists are rewritten on every run, and must be** — a new post is a
new neighbour for a page minted a year ago. Rewriting a derived list of slugs cannot
corrupt an ID, so this is safe.

**Drafts and future-dated posts stay in the frontmatter list on purpose.** The template
resolves each ref through `site.GetPage`, which returns nothing for a page the
production build never emitted. So an unpublished neighbour is skipped in prod and
appears the day it ships. The dead-link failure CLAUDE.md warns about is made
_structurally impossible_ here rather than something you have to remember. Do not
"optimize" this by filtering drafts in the script: the list would go stale the moment
the publishing calendar rolled forward.

Do not reach for a vector database. At this corpus size that is a punchline.

## Search: `/search/`

The same IDs power client-side semantic search — no server, no index of body text.

- `themes/ee-ai/layouts/index.json` emits the index: title, url, section, summary, tags,
  and `x` (the semantic ID). **No body text**, because the ID already _is_ the meaning,
  so the whole thing stays a few kilobytes.
- `themes/ee-ai/static/js/search.js` decodes the base64url into 24 bytes and does the
  XOR/popcount in the browser. A query lexically **seeds** a page; everything after that
  is pure ID arithmetic — XOR the seed against every other page, popcount, sort.
- `content/search.md` (`layout = "search"`) +
  `themes/ee-ai/layouts/_default/search.html` are the page itself.

The index is built from `site.RegularPages`, which is exactly what the production build
emits — so drafts and future-dated posts are absent for the same reason they're absent
from the site. Nothing to filter, nothing to remember.

### ⚠️ Rule 5: `search.js` duplicates the bit constants

`ALPHABET`, `SEMANTIC_BITS`, `TAIL_BITS`, and `MAX_DISTANCE` exist in **both**
`scripts/semantic-ids.py` and `themes/ee-ai/static/js/search.js`, because the browser has
to decode and compare the same IDs the Python minted. **Change one without the other and
search silently ranks noise** — it will not throw, it will not warn, it will just return
confidently wrong results. There is no build step to catch this. The JS carries a comment
saying so; believe it.

## Deeper background

`references/design.md` — why binary quantization works at all, why mean-centering is
mandatory, why the hex-prefix-as-semantic-bucket idea is a trap, the encoder comparison
(truncate vs ITQ vs SimHash vs PCA) and why this site uses the _simplest_ one, and the
measured recall numbers. Read it before changing the bit layout, the encoder, or the
embedding model.
