# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`ai.ericeaglstun.com` - a Hugo static site: a plain-language AI/ML glossary plus
blog/practice/deep-dives sections. Hugo **extended** v0.161+, custom theme in
`themes/ee-ai/` (plain CSS, no build step), one vanilla-JS file for the glossary filter.
No package manager, no runtime dependencies.

## Commands

```bash
hugo server -D                 # local dev → http://localhost:1313 (includes drafts)
python3 scripts/gen-glossary.py # regenerate content/glossary/*.md (see below)
./deploy.sh                    # build --minify + rsync public/ to the droplet
```

`deploy.sh` reads `DEPLOY_HOST` / `DEPLOY_PATH` / `DEPLOY_BASE_URL` from `.env`
(gitignored; see `.env.example`). The server vhost lives in `deploy/`.

## The glossary is generated - don't hand-edit `content/glossary/*.md`

Every `content/glossary/<slug>.md` (except `_index.md`) is **output** of
`scripts/gen-glossary.py`. Editing them directly gets overwritten on the next run.

Source entries live **outside this repo** at
`~/.claude/skills/ai-dev/references/glossary/`. The script:

- drops the leading `# Heading` (Hugo renders the title from frontmatter),
- rewrites `[[slug]]` wikilinks into real `/glossary/slug/` links,
- lifts the trailing `**See also:**` paragraph into `related` frontmatter (rendered as chips),
- writes `title` / `summary` / `category` / `related` frontmatter.

To add or change a term: edit the source entry, then update the per-slug maps at the
top of the script (`TITLE`, `SUMMARY`, `CATEGORY`, `RELATED`), then re-run it.

**`tags` and `semantic_id` are the exception** — they're minted by `semantic-ids.py`,
not by this script, and `gen-glossary.py` carries them through verbatim on regeneration
(see `carry_over()`). If you rewrite the frontmatter block in that script, preserve
those two fields or every glossary ID is destroyed.

## Semantic IDs: `scripts/semantic-ids.py`

Every content page carries a `semantic_id` — a 192-bit, 32-character **base64url**
string whose bits **are** the meaning of the page:

```
┌──────────────── 172 bits semantic ────────────────┬── 16b day ──┬─ 4b hash ─┐
│  sign(embedding[i] - frozenMean[i]),  i = 0..171  │ since 2026  │ tiebreak  │
└───────────────────────────────────────────────────┴─────────────┴───────────┘

geUp5zbmgovefpbj0zjw_PuPFM9fQApS    "A Conscience You Can Patch Out Overnight"
18co9P3055up1QLz1boi7cifFeRqYAjm    "Everyone Deserves a Mascara Treat"
```

Two pages about the same thing get IDs that are close in **Hamming distance** (count of
differing bits), so "related posts" is an XOR and a popcount — no vector database, no
server, no runtime dependency. The embedded text is `title + summary + tags`, not the
body: an embedding is a fixed-size container, so a whole article averages into a vague
blob that is near everything and about nothing.

**Why base64url and not hex.** Hex spends 4 bits per character and throws away the other
half of every character's capacity. Base64 spends 6. At the same 32-character width
that's 192 bits instead of 128 — **172 semantic bits instead of 108** — which measured
out at 54% recall vs 51% on this corpus. The sizes land exactly: 192 bits = 24 bytes,
and base64 packs 3 bytes into 4 chars, so 24 bytes is precisely 32 characters with no
padding. 64 symbols rather than 62 (plain alphanumerics) because a power of two means
encoding is bit-shifting rather than bignum division. `-` and `_` (base64**url**) keep
the IDs safe in URLs and filenames.

⚠️ **`-` is a valid character in the ID, not a separator.** The old hex format looked
like a UUID and invited dash-stripping. Do that now and you silently corrupt the
comparison. Use `decode64()`.

```bash
python3 scripts/semantic-ids.py            # fill in missing tags + IDs (needs Ollama)
python3 scripts/semantic-ids.py --dry-run  # report, write nothing
python3 scripts/semantic-ids.py --force    # re-mint everything (see the warning below)
```

**Four rules, and breaking any of them corrupts the IDs silently:**

1. **`data/semantic-model.json` is frozen.** It holds the 768-float corpus mean, and
   binarization is `sign(v - mean)`. Recompute the mean and every previously-issued ID
   silently becomes wrong — no error, no warning, just quietly incomparable numbers.
   The script only writes it if it does not already exist. Do not delete it. (The mean
   is independent of the bit count, so changing `SEMANTIC_BITS` does NOT require
   retraining it — only re-minting.)
2. **Compare through the mask.** The day/tiebreak bits are Hamming _noise_. Use the
   `hamming()` helper in the script, which masks them off, or two identical pages
   published a year apart will look unrelated.
3. **Tags come from a controlled vocabulary** (glossary slugs + `EXTRA_VOCAB`), because
   free-form tag generation produced hallucinated garbage like `aspartame-grade-ml` —
   and since tags feed the embedding, junk tags mean junk vectors. Anything the model
   invents that isn't on the list is dropped.
4. **The bit constants are duplicated in `themes/ee-ai/static/js/search.js`.** The
   browser has to decode and compare the same IDs, so `ALPHABET`, `SEMANTIC_BITS`,
   `TAIL_BITS`, and `MAX_DISTANCE` exist in **both** files. Change one without the other
   and search silently returns nonsense — it will not throw, it will just rank noise.
   There is no build step to catch this; it is on you.

## `related_by_meaning` and `/search/`

Two features ride on the IDs. Both are pure Hamming distance — XOR the two IDs, popcount
the difference. No vector database, no server, no runtime dependency.

**`related_by_meaning`** is a frontmatter list of page refs, minted by `semantic-ids.py`
at the same time as the ID and rendered by
`themes/ee-ai/layouts/partials/related-by-meaning.html`. It runs at mint time rather than
render time because Go templates have no popcount, and because doing it once beats doing
it on every build.

The partial resolves each ref through `site.GetPage`, which returns nothing for a page
the build never emitted — a draft, or a future-dated post. So an unpublished neighbour is
skipped in production and simply appears the day it ships. No dead links, nothing to
re-run.

**`/search/`** (`content/search.md` → `themes/ee-ai/layouts/_default/search.html` +
`static/js/search.js`) fetches `/index.json` once, lazily. That index carries **no body
text** — just title, url, section, summary, tags, and `x`, the semantic ID — so it stays
a few kilobytes. A query lexically seeds a page, and everything after that is pure ID
arithmetic: XOR the seed against every other page, popcount, sort ascending.

**`RELATED_MAX_DISTANCE = 72` is not a vibe.** Two pages picked at random differ by ~87 of
the 172 semantic bits — which is chance, since half of 172 is 86. Unrelated pages sit at a
coin flip, exactly as they should. The 5th percentile of all pairs is 70 bits, so a cutoff
of 72 means "closer than roughly 95% of random pairs." Above it you are ranking noise and
calling the winner a recommendation.

## Taxonomy: scalar `category`, not Hugo taxonomies

Hugo's built-in tag/category taxonomies are **disabled** in `hugo.toml` (`[taxonomies]`
is empty). The glossary groups itself by a **scalar `category` frontmatter string**,
filtered with `where ... "Params.category"` in `themes/ee-ai/layouts/glossary/list.html`.

Category **display order** is the canonical list returned by
`themes/ee-ai/layouts/partials/glossary-categories.html`. Categories present on terms
but missing from that list still render - they're appended after the ordered ones. When
introducing a new category, add it to that partial.

## Layout templates

- `themes/ee-ai/layouts/glossary/list.html` - grouped term grid + search/filter.
- `themes/ee-ai/layouts/glossary/single.html` - individual term page (breadcrumb,
  body, "See also" chips resolved from `related` via `site.GetPage`). Also renders
  **alphabetical prev/next nav within the same `category`** (`.term-nav`), built from
  `.CurrentSection.RegularPages` filtered by category and sorted `.ByTitle`.
- `themes/ee-ai/layouts/_default/` - `baseof.html`, `single.html`, `list.html` for
  the non-glossary sections (blog, practice, deep-dives).
- `themes/ee-ai/layouts/partials/related-by-meaning.html` - the "Related" nav at the
  foot of a page, resolved from the `related_by_meaning` frontmatter (see above).
  Included from `_default/single.html`.
- `themes/ee-ai/layouts/index.json` + `_default/search.html` +
  `static/js/search.js` - the client-side semantic search behind `/search/`
  (`content/search.md`, `layout = "search"`). `index.json` is the metadata-only index;
  `search.js` decodes the base64url IDs and does the XOR/popcount in the browser. **It
  duplicates the bit constants from `scripts/semantic-ids.py` — keep them in sync.**
- `themes/ee-ai/layouts/_default/_markup/render-link.html` - **link render hook** applied
  to all markdown content site-wide. Any link whose host ≠ the `baseURL` host gets
  `class="external-link"`, `target="_blank"`, `rel="noopener noreferrer"`, and an inline
  arrow-out SVG icon. Internal/relative links pass through untouched. CSS: `.external-icon`.
- `themes/ee-ai/layouts/shortcodes/` - theme shortcodes. The markdown-wrapping ones
  (`louuy-chat.html`, `claude-term.html`) re-render their `.Inner` via
  `RenderString (dict "display" "block")`, so the inner blockquotes/paragraphs/code/`---`
  still parse. `louuy-chat` styles a run of `> prompt` + verbatim-response exchanges as a
  chat thread (`practice/louuy-dispatches`); `claude-term` renders an exchange as a faked
  Claude Code terminal window (`> line` = the user's ❯ prompt, paragraphs = the ⏺ reply;
  first used by `blog/my-claude-code-started-roasting-me`). Also: `bbros.html` (Beagle
  Bros-style margin cards), `details.html`, and the interactive `pulse-playground.html` /
  `seance-playground.html` widgets. See the css-tokens site-docs ref for the styling.

**Per-page styling without a build step:** there's no per-page CSS file - page-specific
styles live in the one global `themes/ee-ai/static/css/style.css` under a scoping class that
only appears on that page (`.louuy-chat`, `.series-1930-...`). Goldmark `unsafe = true`, but
raw `<div>` in markdown won't re-parse inner markdown - use a shortcode (above) when you need
markdown inside the wrapper.

## Writing conventions (blog / practice / deep-dives)

These sections hold hand-written posts (NOT generated like the glossary). Conventions that
are deliberate - don't "normalize" them:

- **Routing:** _practice_ = reusable tools/workflows; _deep-dives_ = mechanism-heavy
  walkthroughs; _blog_ = notes/opinion/ideas. Apple-Silicon ports are case studies that
  link to the shared playbook `deep-dives/porting-ml-to-apple-silicon.md`.
- **`draft = true`** on stubs keeps them off the live build (`deploy.sh` has no `-F`/`-D`).
  Flip to publish. Use `hugo server -D` to preview drafts.
- **Cross-links must respect publish state, or they 404 in production.** Because the live
  build drops drafts and future-dated posts, a **live** post that hyperlinks one that is still
  `draft = true` or future-dated produces a dead link on the deployed site (Hugo emits no page
  for the hidden post; the link is just a string it never validates). Rule: a live post may only
  link to other already-live, already-dated posts. For a forward reference to something not yet
  shipped, **de-link it** (plain text or "coming soon") until the target publishes, then restore
  the link - the pattern behind the LOUUY dispatches deep-dive link and the deliberate
  `the-first-ai-law-was-a-weapons-law` 404. When you re-date, publish, or unpublish a post,
  re-check both the links _inside_ it and the links _pointing at_ it. A clean
  `hugo --minify` build plus an internal-link sweep over `public/` catches these.
- **Dates are staggered on purpose** (~3-day cadence). Drafts are **future-dated** into a
  forward publishing calendar, not backdated. Do not reset them to today. The full chronological
  master list lives in `meta/publish-schedule.md`, which is **generated** by
  `scripts/gen-publish-schedule.py` (reads each post's `date`/`draft`) - re-run it after adding
  or re-dating posts; don't hand-edit it. Watch for date-anchored posts (ones that reference a
  real event or relative time like "this week"): pin those to absolute dates so re-dating the
  post doesn't break the narrative.
- **Every published post ships share metadata.** Non-draft, non-future posts carry a
  `description` ≤125 chars (the og:description) and `images = ["/og/<slug>.png"]` pointing
  at a real 1200×630 card in `static/og/` - a missing PNG means a silently broken share
  card, so verify the file exists after a re-slug or re-date. Cards are built in the
  `meta/` workspace (its own private repo): art via flux into `og-assets/`, card copy in
  `_buildcards.py`, rendered with headless Chrome (`--virtual-time-budget` or the webfonts
  won't load). Posts with inline illustrations are **page bundles** (`<slug>/index.md` +
  image beside it), not bare `.md` files.
- **Titles are voice-forward hooks, not summaries**, and the body leans into Eric's
  artist/communicator voice (weird-but-illuminating analogies, DEVO/de-evolution motif).
  The detailed voice guidance + blessed title examples live in Claude's project memory.
