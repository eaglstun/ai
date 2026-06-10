# Multi-part "series" — the bespoke deep-dives machinery

Hugo has **no built-in series.** This is hand-rolled. Reference implementation:
`content/deep-dives/ctranslate2-metal-backend/`. (Depends on layout lookup and page bundles —
see `layouts-and-bundles.md`.)

**Shape — a nested branch bundle:**

- Hub: `content/deep-dives/<series>/_index.md` with `layout = "series"`.
- Parts: `content/deep-dives/<series>/NN-slug.md` (regular pages). The `NN-` filename prefix
  is just for editor ordering; the real order is the `weight` frontmatter. Set
  `slug = "pretty-slug"` so the URL drops the number.

**Per-part frontmatter:** `series = "<series>"`, `weight = N`, `slug = "…"`, `draft = true`.

**How the pieces find each other:**

- `layout = "series"` on the hub → Hugo's layout lookup resolves `_default/series.html`
  (the `layout` value is honored for section/list pages). That template lists
  `.Pages.ByWeight` — we need a custom template because the default `list.html` sorts
  `.ByDate`, which scrambles a numbered series.
- **Prev/next nav** lives in `_default/single.html`, inside a `{{ if .Params.series }}`
  guard so normal posts are untouched. It walks `.Parent.Pages.ByWeight` to find the current
  page and pick neighbors. **Scope gotcha:** declare `$prev`/`$next` at the _top_ of the
  template with `:=`, then assign inside the range with `=`. Declaring them inside one
  `{{ if }}` block and using them in another is a separate scope → `undefined variable`
  error (cost a debugging round).
- **Why the parent `/deep-dives/` list shows the series as ONE card, not seven:** the section
  list template iterates `.Pages`, which includes child _sections_ (the series hub) as a
  single entry. The parts are regular pages of the nested section, so they never surface at
  the top level. Free grouping.

**Inter-part links MUST be absolute root paths** — `/deep-dives/<series>/<slug>/`, not a bare
`<slug>/`. Each part renders to its **own directory** (`…/<series>/<slug>/index.html`), so a
relative `other-slug/` resolves against the current part's dir → `…/<slug>/other-slug/`, which
404s. The hub's own links _could_ be relative (it's the parent dir) but use absolute
everywhere for consistency. (Verify after building: every in-body `/deep-dives/<series>/…`
href should map to a real `public/.../index.html`.)
