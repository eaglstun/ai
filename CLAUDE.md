# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`ai.ericeaglstun.com` — a Hugo static site: a plain-language AI/ML glossary plus
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

## The glossary is generated — don't hand-edit `content/glossary/*.md`

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
but missing from that list still render — they're appended after the ordered ones. When
introducing a new category, add it to that partial.

## Layout templates

- `themes/ee-ai/layouts/glossary/list.html` — grouped term grid + search/filter.
- `themes/ee-ai/layouts/glossary/single.html` — individual term page (breadcrumb,
  body, "See also" chips resolved from `related` via `site.GetPage`).
- `themes/ee-ai/layouts/_default/` — `baseof.html`, `single.html`, `list.html` for
  the non-glossary sections (blog, practice, deep-dives — currently stubs).
