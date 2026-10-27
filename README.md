# ai.ericeaglstun.com

A working notebook on AI and machine learning: a plain-language glossary, plus
blog posts, practice notes, and deep dives. The premise: almost nobody fully
understands how modern AI works, so let's make it legible one term at a time.

**Live:** https://ai.ericeaglstun.com

## Stack

- [Hugo](https://gohugo.io/) **extended** v0.161+; no package manager or runtime dependencies
- Custom theme in `themes/ee-ai/`, with self-hosted Newsreader and Atkinson Hyperlegible Mono
- Plain CSS in numbered files under `themes/ee-ai/assets/css/parts/`, concatenated by Hugo into one stylesheet
- Vanilla JavaScript for the glossary filter, site search, and page treatments

## Local development

```bash
hugo server -D        # http://localhost:1313, including drafts
hugo --minify         # production build in public/
```

## Repository map

```text
content/
  _index.md           home page
  why.md              why the site exists
  colophon.md         how the site is made
  glossary/           hand-edited term pages
  practice/           reusable tools and workflows
  blog/               notes, opinion, ideas
  deep-dives/         mechanism-heavy walkthroughs and series
  search.md           client-side site search
themes/ee-ai/         layouts, partials, shortcodes, CSS, and JS
static/               fonts, glossary art, share cards, and standards files
```

`scripts/`, `meta/`, and `deploy.sh` are gitignored local tools or workspaces;
they are absent from a fresh clone. The site builds without them. The old
`scripts/gen-glossary.py` was retired; it does not regenerate glossary pages.

## Editing the glossary

Each `content/glossary/<slug>.md` is its own source of truth. Edit the Markdown
directly. Frontmatter includes `title`, `summary`, and a scalar `category`, plus
optional `plain` text, `related` term slugs, `mentions`, and an image. Keep
`related` links reciprocal. Category display order is set in
`themes/ee-ai/layouts/partials/glossary-categories.html`.

Term pages show See also links and up to four published posts under “Where it
comes up.” The latter are selected from post links, text mentions, then shared
tags. Hugo's built-in tag and category taxonomies are disabled.

Content pages also carry a `semantic_id` derived from their title and summary.
Do not edit it by hand. The local semantic-ids skill and the
`.agents/semantic-ids.toml` context maintain these IDs. The `/search/` page uses
them to rank related pages in the browser; its metadata-only index contains no
article body text.

## Publishing posts

Set `draft = true` for unfinished posts; the production build excludes drafts
and future-dated pages. Published posts need a short `description` and an
`images` entry pointing to a real 1200×630 card in `static/og/`. Posts with
inline illustrations are page bundles (`<slug>/index.md` with images beside it).
Check links between posts before publishing: a live page must not link to an
unpublished one.

The publishing calendar and share-card tools live in the local `meta/`
workspace. See [AGENTS.md](AGENTS.md) for the full content and editing
conventions.

## Deploy

The production build is `hugo --minify`. Deployment is configured locally:
`deploy.sh` (gitignored) reads `.env` for `DEPLOY_HOST` and `DEPLOY_PATH`,
builds the site, then rsyncs `public/` to the server. `.env.example` documents
the settings. The live site is served by nginx with TLS.

## Standards and accessibility

`static/` includes `robots.txt`, `llms.txt`, `humans.txt`, and files under
`.well-known/` for security, privacy, and text-and-data-mining preferences.
The theme targets WCAG 2.1 AA with semantic landmarks, labelled controls,
visible focus styles, reduced-motion support, and light/dark color tokens.
