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
- `themes/ee-ai/layouts/_default/_markup/render-link.html` - **link render hook** applied
  to all markdown content site-wide. Any link whose host ≠ the `baseURL` host gets
  `class="external-link"`, `target="_blank"`, `rel="noopener noreferrer"`, and an inline
  arrow-out SVG icon. Internal/relative links pass through untouched. CSS: `.external-icon`.

## Writing conventions (blog / practice / deep-dives)

These sections hold hand-written posts (NOT generated like the glossary). Conventions that
are deliberate - don't "normalize" them:

- **Routing:** _practice_ = reusable tools/workflows; _deep-dives_ = mechanism-heavy
  walkthroughs; _blog_ = notes/opinion/ideas. Apple-Silicon ports are case studies that
  link to the shared playbook `deep-dives/porting-ml-to-apple-silicon.md`.
- **`draft = true`** on stubs keeps them off the live build (`deploy.sh` has no `-F`/`-D`).
  Flip to publish. Use `hugo server -D` to preview drafts.
- **Dates are staggered on purpose** (~3-day cadence). Drafts are **future-dated** into a
  forward publishing calendar, not backdated. Do not reset them to today. The full chronological
  master list lives in `meta/publish-schedule.md`, which is **generated** by
  `scripts/gen-publish-schedule.py` (reads each post's `date`/`draft`) - re-run it after adding
  or re-dating posts; don't hand-edit it. Watch for date-anchored posts (ones that reference a
  real event or relative time like "this week"): pin those to absolute dates so re-dating the
  post doesn't break the narrative.
- **Titles are voice-forward hooks, not summaries**, and the body leans into Eric's
  artist/communicator voice (weird-but-illuminating analogies, DEVO/de-evolution motif).
  The detailed voice guidance + blessed title examples live in Claude's project memory.
