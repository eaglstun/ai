# Goldmark render hooks - the `_markup/` directory

Any template at `themes/ee-ai/layouts/_default/_markup/render-<kind>.html` is a **render
hook**: Hugo runs it for every instance of that element in **all** markdown content,
sitewide (glossary, blog, deep-dives - everything). We have two: `render-link.html`
(external-link decoration, documented in CLAUDE.md) and `render-table.html`.

A render hook **replaces Hugo's default rendering of that element entirely.** It does not get
raw markdown - it gets a typed context object and re-emits the HTML itself. Upside: total
control. Downside: a bug in the hook silently breaks _that element on every page_, not one
post. Build with `hugo --buildDrafts` while iterating - **`--quiet` swallows template
errors** (a real `undefined variable` error hid behind `--quiet` during dev and the build
looked like it "succeeded" with missing output).

## `render-table.html` - wrap every table for mobile scroll

**Why it exists:** a markdown `| … |` table renders as a bare `<table>` with no way to
scroll. Wide benchmark grids (the CTranslate2 series is full of them) blow past the prose
measure on narrow screens. The hook wraps each table in `<div class="table-wrap">`, and the
CSS (`.table-wrap` in `assets/css/parts/08-tables.css`) gives that wrapper `overflow-x: auto` + the
rounded border, capped at `--content`.

**The context object** the hook receives (this is the part you can't guess):

| field             | what it is                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `.THead`          | slice of header rows; each row is a slice of cells                                                                        |
| `.TBody`          | slice of body rows; same shape                                                                                            |
| cell `.Text`      | the cell's **already-rendered inline HTML** (inline code, bold, links) as `template.HTML` - emit it raw, do not re-escape |
| cell `.Alignment` | `"left"` / `"center"` / `"right"`, or empty for default (from markdown `:--` / `--:`)                                     |

So the hook loops `.THead` then `.TBody`, emits `<th>`/`<td>` with an optional
`style="text-align: …"` from `.Alignment`, and drops `{{ .Text }}` inside. Because _we_ own
the markup, this is also where you'd add a `<caption>`, column classes, etc. Current file is
deliberately minimal - wrapper + faithful rebuild.

**Styling pairs with the hook** (`assets/css/parts/08-tables.css`): `tabular-nums` so
benchmark digits line up, zebra `:nth-child(even)`, `--accent-soft` row hover, mono header
(`--font-mono`). One non-obvious CSS gotcha baked in: inline `code` inside a cell normally
uses `--surface-2` as its background - which is _also_ the zebra-row color, so it'd vanish;
table `code` is overridden to `--surface` + a border to stay visible on striped rows. (Full
token rationale: `css-tokens.md`.)
