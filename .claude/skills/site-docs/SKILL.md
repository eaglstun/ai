---
name: site-docs
version: 1.2.0
description: Non-obvious Hugo mechanics for the ai.ericeaglstun.com site (theme ee-ai, repo ~/Documents/web/ericeaglstun-ai) - Goldmark render hooks, the bespoke multi-part "series" machinery, layout lookup, page bundles, and the gotchas that aren't in the repo's CLAUDE.md. Use when editing the theme's templates/layouts/render hooks, building a new content type or a series, or debugging why a template, link, table, or section isn't rendering the way it should on this site.
---

# site-docs - non-obvious Hugo on ai.ericeaglstun.com

The stuff that isn't obvious from the file tree and isn't already in the repo's `CLAUDE.md`.

**Read `CLAUDE.md` first for the basics** - it covers the generated glossary
(`scripts/gen-glossary.py`; don't hand-edit `content/glossary/*.md`), the scalar-`category`
taxonomy (Hugo taxonomies disabled), the `render-link.html` external-link hook, and `deploy.sh`
(builds with **no** `-D`/`-F`, so `draft = true` keeps a page off production; preview drafts
with `hugo server -D`).

This skill is the layer below that - the mechanics you have to have _built_ to know. Load the
one reference for your task:

- **`references/render-hooks.md`** - Goldmark render hooks & `render-table.html`. The `_markup/`
  mechanism, the table hook's context object (`.THead`/`.TBody`/`.Text`/`.Alignment`), and the
  `--quiet`-swallows-template-errors trap. _Read when editing a render hook or table styling._
- **`references/series.md`** - the hand-rolled multi-part "series": nested branch bundle,
  `layout = "series"`, `weight` ordering, the prev/next scope gotcha, and the absolute-only
  inter-part link rule. _Read when building or editing a multi-part deep dive._
- **`references/layouts-and-bundles.md`** - Hugo layout lookup (the nested-section-type
  subtlety) and leaf-vs-branch page bundles + the `foo.md`/`foo/` collision. _Read when adding a
  content type, a section template, or a bundled post._
- **`references/glossary-generator.md`** - the `gen-glossary.py` hidden contract: out-of-repo
  source, the per-slug dicts, back-link reciprocity, wikilink rewriting, the category-order
  partial. _Read when adding or changing a glossary term._
- **`references/css-tokens.md`** - the `:root` token system, never-hardcode-a-color / dark-mode,
  `color-mix` derived shades, the token-collision trap, **and per-page styling without a build
  step** (the `.louuy-chat` chat-UI pattern: scoping class in the global stylesheet, the
  markdown-needs-a-shortcode-not-a-raw-div rule, `:has()` opt-outs, `white-space:pre-line`).
  _Read when touching `style.css` or styling a single page._
- **`references/summaries.md`** - `<!--more-->`, `.Summary` precedence, and the one-line
  frontmatter `summary` doing quadruple duty (cards, deks, SEO) as **plain text, not markdown**.
  _Read when a card/dek/meta-description renders wrong._
