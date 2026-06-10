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
