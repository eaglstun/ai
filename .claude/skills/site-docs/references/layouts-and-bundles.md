# Layout lookup & page bundles

## Layout lookup - the part that's always fuzzy

- A section/list page with `layout = "foo"` → Hugo looks for `<section>/foo.html`, then
  `_default/foo.html`.
- **Nested sections inherit the top-level section name for lookup.** A series hub under
  `deep-dives/` is type `deep-dives`, so a `layouts/deep-dives/list.html` would hijack _both_
  the top-level deep-dives list _and_ every nested series hub. That's exactly why the series
  uses a `layout = "series"` escape hatch instead of a `deep-dives/list.html` - to style the
  hub without touching the section index. (See `series.md`.)

## Page bundles - leaf vs branch, and the collision

- **Leaf bundle:** a dir with `index.md` (no underscore) + co-located assets. Used for richer
  posts that own an image, e.g. `porting-ml-to-apple-silicon/index.md` + `six-monsters.png`.
  The URL is the directory.
- **Branch bundle:** a dir with `_index.md` (underscore) + child pages/sections. Every
  section and every series hub is a branch bundle.
- **Collision:** a `foo.md` file and a `foo/` bundle dir resolve to the _same URL_ and
  conflict. When promoting a single-file post to a bundle (as the CTranslate2 post went from
  `ctranslate2-metal-backend.md` to `ctranslate2-metal-backend/`), **delete the old `.md`** or
  the build fights itself.
