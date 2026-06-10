# `<!--more-->`, `.Summary`, and the one-line `summary` that does quadruple duty

`.Summary` precedence in Hugo: frontmatter **`summary`** wins → else the **`<!--more-->`**
divider → else an auto cut (~first 70 words). This site sets a frontmatter `summary` on
basically everything (the glossary generator writes one; posts set one by hand), so in practice
**`.Summary` is the frontmatter `summary`** almost everywhere.

That one line is doing a lot of jobs at once - change it and all of these move:

- list-page cards (`_default/list.html`, `series.html`) - `.Summary | plainify | truncate`
- home-page section deks (`index.html`) and glossary card + dek (`glossary/`)
- the `<meta name="description">` / SEO + social tag - `head.html` does
  `or .Description .Summary site.Params.description`

**Because the cards `plainify` it, frontmatter `summary` is plain text - never markdown.**
Markdown in a `summary` isn't processed; it renders literally. (This is exactly the bug where a
glossary `summary` with `*not*` showed the asterisks - `plainify` strips HTML tags, but the
markdown was never turned into tags in the first place.) Contrast with the glossary `plain`
field, which `glossary/single.html` runs through **`markdownify`** - so `plain` _can_ hold
links/emphasis, but `summary` cannot. Different fields, different rules.

`<!--more-->` in the blog/deep-dive bodies is mostly belt-and-suspenders given the above: it's
**stripped from the rendered `.Content`** (invisible on the page - it does _not_ create a
visible "read more" fold by itself) and only changes `.Summary` for a page that _omits_ a
frontmatter `summary`. Keeping it means a post that forgets its frontmatter summary still gets a
clean hand-placed cut on its card instead of an auto-truncation mid-sentence.
