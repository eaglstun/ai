# The CSS token system (`static/css/style.css`)

The theme is **plain CSS, no build step**, and everything is driven by custom properties in
`:root`. The cardinal rule: **never hardcode a color - always use a token**, because dark mode
is implemented _entirely_ by overriding those same tokens in a single
`@media (prefers-color-scheme: dark)` block. Use a token and your component inverts for free;
hardcode a hex and it breaks in dark mode and nowhere else (so you won't notice).

The palette (warm paper / ink / indigo):

| token                                            | role                                                                                                      |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `--bg` / `--surface` / `--surface-2`             | page bg / card bg / raised panel (code, table headers, chips bg)                                          |
| `--ink` / `--muted`                              | body text / secondary text                                                                                |
| `--line`                                         | all hairline borders & dividers                                                                           |
| `--accent` / `--accent-ink` / `--accent-soft`    | indigo link/border / darker text-on-light / faint tint (hover, chips)                                     |
| `--font-display` / `--font-mono` / `--font-sans` | Fraunces / JetBrains Mono / system - mono = the "technical data" font (code, dates, chips, table headers) |
| `--content` / `--wide`                           | prose measure (46rem) / grid+home measure (70rem)                                                         |
| `--radius` / `--shadow`                          | 12px corner / card elevation                                                                              |

Two non-obvious habits in this file:

- **`color-mix()` for derived shades** instead of new tokens - e.g. the table zebra row is
  `color-mix(in srgb, var(--surface-2) 45%, transparent)`, so it tracks the theme (and dark
  mode) automatically rather than being a frozen color.
- **Watch for token collisions between layered components.** Inline `code` defaults to a
  `--surface-2` background; table zebra rows are _also_ `--surface-2`-derived, so code in a
  striped cell would disappear - table `code` is explicitly overridden to `--surface` + a
  border. When you put one tinted thing on top of another, check they don't share a token.

The dark-mode block also carries a contrast note worth heeding: the dark accent is light
indigo, so **white text on it fails WCAG** - dark text on the accent is used instead (see the
`.btn` override).

## Per-page styling without a build step (the `.louuy-chat` pattern)

There is no per-page stylesheet. To style a single page, add rules under a **scoping class
that only appears on that page** to the one global `style.css` (existing examples:
`.louuy-chat`, `.series-1930-on-the-machine-we-switched-off`). The class is harmless
everywhere else because the selector never matches. Append at the end of the file so your
rules win ties against the `.prose` defaults by source order (same specificity).

`.louuy-chat` (the `practice/louuy-dispatches` chat UI) is the worked example, and it leans on
a few non-obvious tricks:

- **Markdown inside a wrapper needs a shortcode, not a raw `<div>`.** Goldmark has
  `unsafe = true`, but CommonMark does **not** re-parse markdown inside a raw HTML block - the
  blockquotes/paragraphs would come out literal. The `louuy-chat` shortcode
  (`themes/ee-ai/layouts/shortcodes/`) renders `.Inner` with
  `.Page.RenderString (dict "display" "block")` - **`display:block` is required**; the default
  is `inline` and won't emit block elements.
- **Flex column + alignment, not floats.** `.louuy-chat` is `display:flex; flex-direction:column;
align-items:flex-start`; direct-child `blockquote` (the prompt) flips to `align-self:flex-end`
  (right, user) while every other direct child is a left bubble (LOUUY).
- **`:has()` opt-outs.** Images (`p:has(> img)`) and editorial `_(...)_` asides
  (`p:has(> em:only-child)`) are pulled out of the bubble treatment so they read as a full-width
  figure / centered caption. Relies on `:has()` (Baseline 2023, fine here); browsers without it
  just fall back to bubble styling.
- **`white-space: pre-line` on the bubbles** preserves the author's intentional line breaks
  (haiku, the warning label, count-to-ten) that markdown would otherwise collapse to a space.
  Safe **only because** the dispatch prose paragraphs are single-line in source - a soft-wrapped
  paragraph would get false mid-sentence breaks. Lists/code are exempted (`white-space:normal` /
  `<pre>` has its own).
- **The user bubble is `--accent` bg**, so it inherits the same WCAG trap as `.btn`: `#fff` text
  in light, overridden to `var(--bg)` (dark text) in a `@media (prefers-color-scheme: dark)`
  block. The minifier strips attribute quotes, so the rendered class reads `class=louuy-chat` -
  grep without quotes when verifying the build.

`.claude-term` (the `{{< claude-term >}}` faked Claude Code terminal, first used by
`blog/my-claude-code-started-roasting-me`) is the second worked example. Same shortcode
pattern (`RenderString` display:block; a `> ...` blockquote is the user's prompt line, any
other paragraph is the reply), with two wrinkles of its own:

- **It is the one sanctioned exception to the never-hardcode-a-color rule.** A terminal
  only reads as a terminal if it stays dark in BOTH color schemes, so the block pins a
  local warm-dark palette (hexes chosen to sit in the site's ink family) instead of the
  invertible tokens - the CSS comment says so out loud. Don't "fix" it back to tokens.
- The ❯ (user, green) and ⏺ (Claude, orange `#d97757`) prefixes are `::before` content on
  the direct children, not characters in the markdown - so drafts stay clean text and the
  markers can't be copy-pasted into a quote.
