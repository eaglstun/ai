# The glossary generator's hidden contract (`scripts/gen-glossary.py`)

CLAUDE.md says "don't hand-edit `content/glossary/*.md` — they're generated." This is the part
it doesn't say: the **source of truth lives outside the repo** at
`~/.claude/skills/ai-dev/references/glossary/<slug>.md`, and the generator is driven by a stack
of **per-slug Python dicts at the top of the script** that you must keep in lockstep. Adding or
changing a term is a multi-file ritual, not a one-line edit.

**To add a term** `foo`:

1. Write the source entry `~/.claude/skills/ai-dev/references/glossary/foo.md` — a `# Heading`
   (dropped on generation; Hugo renders the title from frontmatter), the body, and a trailing
   `**See also:** …` paragraph.
2. Add `foo` to the dicts in `gen-glossary.py`: `TITLE` (and `INLINE` if the inline link text
   should differ, usually a lowercased common noun), `SUMMARY`, `PLAIN` (the "In plain English"
   callout — optional), `CATEGORY`, and `RELATED`.
3. **Reciprocate the back-links** — this is the rule that's easy to forget: every slug in
   `RELATED["foo"]` must get `foo` added to _its_ `RELATED` list too, so the "See also" chips
   point both ways. (This is its own standing rule; see the `glossary-backlink-rule` memory.)
4. Re-run `python3 scripts/gen-glossary.py`.

**What the generator does to each source file** (so the output looks the way it does):

- Drops the leading `# Heading` line.
- Rewrites every `[[slug]]` wikilink into a real `[text](/glossary/slug/)` link, using `INLINE`
  for the link text. **An unknown `[[slug]]` prints a `! unknown wikilink target` warning to
  stderr and is left as raw `[[slug]]`** — so watch the generator's output, don't just trust it.
- Lifts the trailing `**See also:**` paragraph out of the body and into the `related`
  frontmatter (rendered as chips by `glossary/single.html` via `site.GetPage`). Note: the
  rendered chips come from the `RELATED` **dict**, not from parsing the See-also line — keep
  them consistent or the page and the source disagree.
- Writes `title` / `summary` / `category` / `related` / `plain` frontmatter.

**Category display order** is _not_ alphabetical and _not_ in the script — it's the hardcoded
slice in `themes/ee-ai/layouts/partials/glossary-categories.html`. A category present on a term
but missing from that slice still renders, appended after the ordered ones. New category →
add it to that partial.
