# ai.ericeaglstun.com

A working notebook on AI & machine learning - a plain-language **glossary** of AI/ML
terms, plus blog posts, practice notes, and deep dives. The premise: almost nobody
fully understands how modern AI works, so let's make it legible one term at a time.

**Live:** https://ai.ericeaglstun.com

## Stack

- [Hugo](https://gohugo.io/) **extended** (v0.161+) - static site generator
- Custom theme in `themes/ee-ai/` (plain CSS, no build step; Fraunces + JetBrains Mono, light/dark)
- One small vanilla-JS file for the glossary filter; no runtime dependencies

## Local development

```bash
hugo server -D        # → http://localhost:1313
```

## Layout

```
content/
  _index.md            home / landing copy
  why.md               the philosophy - "why this exists"
  glossary/            generated term pages + _index.md
  practice/            how I use AI day-to-day (stub)
  blog/                posts (stub)
  deep-dives/          longer walkthroughs (stub)
themes/ee-ai/          layouts, partials, CSS, JS
static/                robots.txt, llms.txt, humans.txt, .well-known/
scripts/gen-glossary.py  glossary generator (see below)
deploy/                nginx vhost for the droplet
deploy.sh              build (minified) + rsync deploy
```

## Glossary (generated - don't hand-edit)

The pages in `content/glossary/` are **generated** by `scripts/gen-glossary.py` from a
separate set of source entries. The script:

- converts `[[wikilink]]` cross-references into real inline links,
- lifts each entry's "See also" into `related` frontmatter (rendered as chips),
- writes title / summary / category / related frontmatter per term.

To add or change a term: edit the source entry and the maps at the top of the script
(`TITLE`, `INLINE`, `SUMMARY`, `CATEGORY`, `RELATED`), then regenerate:

```bash
python3 scripts/gen-glossary.py
```

Every term carries at least one inline body link plus its See-also chips, and category
order is controlled by `themes/ee-ai/layouts/partials/glossary-categories.html`.

## Deploy

```bash
cp .env.example .env   # set DEPLOY_HOST / DEPLOY_PATH / DEPLOY_BASE_URL
./deploy.sh            # hugo --minify + rsync public/ to the server
```

Served as a static site behind nginx (vhost in `deploy/`), TLS via its own Let's
Encrypt cert.

## Standards files

Ships the usual + a few on-theme extras under `static/`:
`/.well-known/security.txt` (RFC 9116), `/.well-known/gpc.json`,
`/.well-known/tdmrep.json`, `robots.txt`, `llms.txt`, `humans.txt`.
(There may also be an easter egg or two. Go look.)

## Accessibility

Targets WCAG 2.1 AA: semantic landmarks, one `h1` per page, labelled controls,
visible focus rings, `prefers-reduced-motion` support, and AA-contrast color tokens
in both light and dark themes.
