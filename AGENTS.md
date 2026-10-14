# AGENTS.md

This file provides guidance to LLM agent harnesses when working with code in this repository.

## What this is

`ai.ericeaglstun.com` - a Hugo static site: a plain-language AI/ML glossary plus
blog/practice/deep-dives sections. Hugo **extended** v0.161+, custom theme in
`themes/ee-ai/` (plain CSS, no build step), one vanilla-JS file for the glossary filter.
No package manager, no runtime dependencies.

## Commands

```bash
hugo server -D                 # local dev → http://localhost:1313 (includes drafts)
./deploy.sh                    # build --minify + rsync public/ to the droplet
```

`scripts/` is **gitignored**: anything in it is local-only and absent from a fresh clone.

`deploy.sh` reads `DEPLOY_HOST` / `DEPLOY_PATH` / `DEPLOY_BASE_URL` from `.env`
(gitignored; see `.env.example`). The server vhost lives in `deploy/`.

## The glossary is hand-edited markdown

Every `content/glossary/<slug>.md` (except `_index.md`) is the source of truth; edit it
directly. These pages used to be **output** of `scripts/gen-glossary.py`, built from entries
in the `ai-dev` skill's `references/glossary/`. That script was deleted on 2026-09-19
(`1eb03ea cleanup`), so nothing regenerates them any more. The skill's copies still exist
but are now an independent fork: an edit in one doesn't reach the other.

Frontmatter a term page uses:

- `title`, `summary` (the dek), `category` (see Taxonomy below).
- `related` - glossary slugs rendered as "See also" chips. Keep links reciprocal: when a
  term points at another, add the back-link on the other page too.
- `plain` - the "In plain English" aside, rendered through `markdownify`.
- `image` + `image_alt` - optional figure above the body. Art lives in
  `static/glossary-img/<slug>.webp` at 1024x768 (4:3); drafts and their prompts go in
  `concepts/glossary-<slug>/`.
- `tags` (hand-curated) and `semantic_id` (minted by the semantic-ids skill, below). Never
  hand-edit `semantic_id`.

Body links between terms are plain markdown links to `/glossary/<slug>/`.

## Semantic IDs: the `semantic-ids` skill, v2 encoder

Every content page carries a `semantic_id`: a versioned, 192-bit, 32-character
**base64url** string whose bits **are** the meaning of the page.

```
v2:<──────────────────── 192 semantic bits ─────────────────────>
    calibrated SimHash of the page's embedding, all 192 bits semantic

v2:t-kOUKApT4XQwZrvyVA9JbrLngZ5bn7O    "Switched-Off Bach"
```

Two pages about the same thing get IDs that are close in **Hamming distance** (count of
differing bits), so "related" is an XOR and a popcount: no vector database, no server, no
runtime dependency. The embedded text is `title + summary`, not the body: an embedding is a
fixed-size container, so a whole article averages into a vague blob that is near
everything and about nothing.

The engine lives in the skill (`~/.agents/skills/semantic-ids/`, read its `SKILL.md`). This
repo only supplies the context file, `.agents/semantic-ids.toml` (gitignored with the rest
of `.agents/`), which the engine auto-discovers when run from anywhere in the repo:

```bash
S=~/.agents/skills/semantic-ids/scripts/semantic_ids.py
python3 $S mint --dry-run    # always first
python3 $S mint              # stamp IDs on new pages; idempotent (needs Ollama + nomic-embed-text)
python3 $S stats             # bit health: dead bits, mean pair distance, 5th percentile
python3 $S near content/deep-dives/switched-off-bach/index.md
```

The site was migrated from the old in-repo v1 script (172 mean-centered bits + a 20-bit
date tail, `data/semantic-model.json` as its frozen mean) on 2026-10-02 with one
deliberate `mint --force`. Nothing reads `data/semantic-model.json` any more. The home
page (`content/_index.md`) is excluded and carries no ID: it's titled "Home", has no
summary, and isn't in `/index.json`.

**Rules, and breaking any of them corrupts the IDs silently:**

1. **Encoder versions never mix.** The `v2:` prefix is part of the ID. The engine and
   `search.js` both refuse to compare across versions rather than return a plausible
   wrong distance. Changing the embedding model, the embedded text, or the bit layout
   means a new version and a full re-mint.
2. **`-` is a valid character in the ID, not a separator.** It looks enough like a UUID
   to invite dash-stripping. Do that and you delete real bits. Use `decode64()`.
3. **No `[tags]` block in the context, on purpose.** With tags enabled, `mint --force`
   regenerates every page's tags with a chat model, which would overwrite the
   hand-curated ones. If tags ever feed the embedding, they must come from a controlled
   vocabulary (free-form generation produced `aspartame-grade-ml`).
4. **The bit layout is duplicated in `themes/ee-ai/static/js/search.js`.** The browser
   decodes and compares the same IDs, so `ALPHABET`, `ID_VERSION`, `SEMANTIC_BITS`, and
   `MAX_DISTANCE` exist there too. Change the encoder without updating it and search
   silently ranks noise. There is no build step to catch this.

## `related_by_meaning` and `/search/`

**`related_by_meaning`** is a frontmatter list of page refs rendered by
`themes/ee-ai/layouts/partials/related-by-meaning.html`, which resolves each ref through
`site.GetPage` so unpublished neighbours are skipped until they ship. Two caveats: the
partial is **currently commented out** in `_default/single.html`, and the lists were
minted by the retired v1 script. The skill writes its own `related_ids` (IDs, not paths)
and doesn't maintain `related_by_meaning`; `related_stamp = 0` in the context keeps it from
touching every file. Re-derive the lists from `near` before switching the partial back on.

**`/search/`** (`content/search.md` → `themes/ee-ai/layouts/_default/search.html` +
`static/js/search.js`) fetches `/index.json` once, lazily. That index carries **no body
text**, just title, url, section, summary, tags, and `x`, the semantic ID, so it stays a
few kilobytes. A query lexically seeds a page, and everything after that is pure ID
arithmetic: XOR the seed against every other page, popcount, sort ascending.

**`MAX_DISTANCE = 60` is not a vibe.** It's the 5th percentile of all pairwise distances
from `stats` at the v2 re-mint: "closer than about 95% of pairs." The mean pair sits at 75
bits rather than the 96 of pure chance because every page here is about AI, so the corpus
is tighter than random text. Re-run `stats` after big content changes and keep the context's
`related_max_distance` and `search.js`'s `MAX_DISTANCE` in step.

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
  duplicates the v2 bit layout from the semantic-ids skill - keep them in sync.**
- `themes/ee-ai/layouts/_default/_markup/render-link.html` - **link render hook** applied
  to all markdown content site-wide. Any link whose host ≠ the `baseURL` host gets
  `class="external-link"`, `target="_blank"`, `rel="noopener noreferrer"`, and an inline
  arrow-out SVG icon. Internal/relative links pass through untouched. CSS: `.external-icon`.
- `themes/ee-ai/layouts/shortcodes/` - theme shortcodes. The markdown-wrapping ones
  (`llm-chat.html`, `claude-term.html`) re-render their `.Inner` via
  `RenderString (dict "display" "block")`, so the inner blockquotes/paragraphs/code/`---`
  still parse. `llm-chat` styles a run of `> prompt` + verbatim-response exchanges as a
  chat thread (`practice/louuy-dispatches`); `claude-term` renders an exchange as a faked
  Claude Code terminal window (`> line` = the user's ❯ prompt, paragraphs = the ⏺ reply;
  first used by `blog/my-claude-code-started-roasting-me`). Also: `bbros.html` (Beagle
  Bros-style margin cards), `details.html`, `diptych.html` (two images as one framed
  before/after figure, shared crop ratio, stacks on phones; keep the call on ONE line, since
  the markdown formatter turns a leading `>}}` into a blockquote and breaks the build), and
  the interactive `pulse-playground.html` / `seance-playground.html` widgets. See the
  css-tokens site-docs ref for the styling.

## The stylesheet is split into ordered parts, concatenated by Hugo

There is still exactly **one** published stylesheet at `/css/style.css` and exactly one
`<link>`, but the source now lives in numbered pieces at
`themes/ee-ai/assets/css/parts/NN-name.css`. `partials/head.html` runs
`resources.Match "css/parts/*.css" | resources.Concat "css/style.css"`, so:

- **The numeric prefix IS the cascade order.** `resources.Match` returns files sorted by
  path, and the parts are concatenated in that order. Renaming `19-` to `05-` silently
  reorders the sheet and changes which rules win ties. Two-digit prefixes keep lexical
  order equal to numeric order.
- **Adding a part needs no template change** - drop a correctly-numbered file in and it
  gets picked up. Deleting one likewise.
- Still no build step to run, still no extra HTTP request. `assets/` (not `static/`) is
  what makes the file a Hugo resource the pipeline can read.

Roughly: `00` tokens, `01-02` base + editorial media, `03-05` header/home/glossary,
`06-16` prose, tables, chips, search, nav, lists, series, footer, responsive, and `17-23`
the page-scoped widgets (1930 series, LOUUY chat, pulse, seance, details, claude-term,
scroll treatments).

**Per-page styling without a build step:** there's no per-page CSS file - page-specific
styles live in the one global stylesheet under a scoping class that only appears on that
page (`.llm-chat`, `.series-1930-...`). Give it its own high-numbered part in
`assets/css/parts/` so it lands late in the cascade. Goldmark `unsafe = true`, but
raw `<div>` in markdown won't re-parse inner markdown - use a shortcode (above) when you need
markdown inside the wrapper.

## Writing conventions (blog / practice / deep-dives)

These sections hold hand-written posts. Conventions that
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
  or re-dating posts; don't hand-edit it, except the `Lock` column (`X` = date must not move,
carried through verbatim on regeneration). Watch for date-anchored posts (ones that reference a
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
