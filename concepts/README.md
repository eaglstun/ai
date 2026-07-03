# Concept images: 4 per post, editorial-illustration program

The plan for giving every post a set of 4 concept images with a New Yorker
sensibility: one strong visual idea per image, wit over decoration, restraint
over spectacle. Concepts are workshop material, NOT post content. They live
here, get reviewed, and only a chosen winner (if any) graduates into a post,
via a deliberate layout treatment rather than a bare inline image.

## The two variety axes

Every post gets 4 concepts = 4 distinct (engine, style) pairings. Never four
takes from one model in one style; the point is a contact sheet that argues
with itself.

### Axis 1: engines (all wired today except one)

| Engine                  | Access                               | Strengths                                                                                                  | Cost       |
| ----------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ---------- |
| Together `FLUX.1.1-pro` | `TOGETHER_API_KEY` live              | painterly, mid-century, Kodachrome; proven on the postcard + staircase                                     | ~$0.04/img |
| Draw Things (local)     | app + API server on 127.0.0.1:7860   | free infinite retries; ink, lineart, riso experiments; model-swappable                                     | $0         |
| Pollinations            | `polli` CLI / `scripts/pollinate.py` | fast drafts, lo-fi collage energy                                                                          | ~$0        |
| Replicate               | needs ~$10 top-up (402'd 2026-07-02) | `recraft-v3` (true flat-vector spot illo), `flux-kontext-pro` (Eric-likeness cameos per the ericoo recipe) | cents/img  |

Fallback while Replicate is dry: run 3 engines and give Draw Things two slots
(different checkpoints/styles count as different voices).

### Axis 2: style palette (pick 4 per post, rotate)

1. **Single-panel gag** - ink + gray wash, lots of white space, no background
   clutter. The caption is NOT in the image (see treatments below).
2. **Continuous-line** - Steinberg-ish one-line drawings; good for abstract
   posts (alignment, minds, floors).
3. **Mid-century flat / Kodachrome** - the established CT2-series look; keep
   for technical series so they stay a family.
4. **Woodcut / engraving** - Beagle Bros adjacency; suits the glossary-brain
   and tinkering posts.
5. **Risograph 2-color** - cheap-print texture; good for practice posts.
6. **Photo-collage cutout** - Gilliam-ish; for the absurdist blog posts.
7. **Ink wash, darker register** - Addams energy; for the no-floor /
   conscience posts.
8. **Blueprint / technical diagram** - for deep-dives; diagrams that are
   almost real but quietly absurd.

House rules: no text baked into images (models garble it, and superimposed
HTML text is the whole treatment strategy). Exception: the big-letter
postcard genre, which flux has proven it can spell. Winners get the JPEG
quality-75 + strip treatment before shipping (colophon footprint rule).

## Storage and naming (never in post bundles)

```text
concepts/<post-slug>/
  a-together-kodachrome.jpg
  b-drawthings-inkwash.jpg
  c-pollinations-collage.jpg
  d-replicate-recraft-vector.jpg
  notes.md            # per image: prompt, engine, params/seed, cost, verdict
  contact-sheet.html  # self-contained review page, generated
```

Root `concepts/` is outside `content/`, so Hugo never publishes it. It is
tracked on dev (nothing sensitive; the sanitizer gate covers main). Page
bundles are NOT used for concepts: Hugo publishes every bundle resource,
referenced or not, so parking rejects next to index.md would ship them.

## Generation pipeline (functional prototype, not a product)

`scripts/gen-concepts.py --slug <post-slug> [--brief "one-line visual idea"]`

1. Reads the post's frontmatter + summary (and `--brief` when given) to build
   a subject line.
2. Holds one prompt template per style in the palette (subject slot + style
   scaffold + "no text, no words" suffix).
3. Fans out 4 calls (engine adapters: together HTTP, drawthings HTTP,
   pollinations script, replicate script; each ~15 lines).
4. Writes images + `notes.md` + `contact-sheet.html` (plain HTML file, opens
   locally, zero build step: filename, engine, style, prompt under each
   image).

Prototype discipline: stdlib Python only, no queue, no retries beyond one,
no config file. If an engine errors it writes the error into notes.md and
moves on with 3 images.

## Display treatments (where winners can go)

Prototype as theme shortcodes + scoped CSS in the one global style.css, per
house convention (markdown-wrapping shortcodes re-render `.Inner`). Build
them rough on ONE draft post first (candidates: temperature post, Jul 21, or
the karaoke post) and preview with `hugo server -D`.

1. **`nyer-panel`** - the flagship. Image in a hairline-ruled panel, italic
   serif caption BELOW the image as real HTML text, New Yorker cartoon
   layout. Optional `alt-captions` param: hover/tap cycles 2-3 rejected
   captions (a few lines of JS). Superimposed-text variant: caption set over
   the image's quiet zone with `mix-blend-mode`.
2. **`spot`** (SHIPPED 2026-07-03) - nyer-panel's modest sibling: a small
   spot illustration floated into the prose (`float="left|right|center"`,
   default right), text wraps around it, no rule, no caption. For images
   that are a grace note rather than a panel. First used on the
   cognitohazard post (the smile-and-fishhook continuous-line).
3. **`concept-strip`** - a 4-up strip of the whole contact sheet as content:
   "same idea, four hands." CSS-only expand on click (`:target` or
   details/summary). Turns the workshop into a post-able artifact for
   process posts.
4. **`poster-hero`** - full-bleed opener image with superimposed display
   type (Ultra/Rye faces from the OG cards migrate to the web), scoped class
   per post like `.series-1930-*`.
5. **One interactive widget, exactly one for now** - the style-slider: two
   engines' takes on the same concept with a draggable divider (pure CSS +
   ~20 lines JS, no deps). If it lands, the caption-contest widget (reader
   types a caption, localStorage, no backend) is the follow-up.

## Review flow

1. Generate 4 per post into `concepts/<slug>/`.
2. Eric opens contact-sheet.html, verdicts go in notes.md (keep / kill /
   redo-with-note).
3. Winner: `magick -quality 75 -strip` into the post's page bundle, placed
   via one of the treatments above; never a bare `![...]()` drop.
4. Losers stay in concepts/ as the argument record (and future
   concept-strip fodder).

## Rollout (prototype-first)

- **Phase 1:** gen-concepts.py prototype; run it on 2 posts (one live blog
  post, one upcoming draft). Deliverable: two contact sheets to react to.
- **Phase 2:** `nyer-panel` + `concept-strip` shortcodes on one draft post.
- **Phase 3:** the style-slider widget on that same post; judge whether
  interactions earn their weight.
- **Phase 4:** only after treatments prove out, walk the backlog (37 posts x
  4 = ~150 images, under $5 on Together even without the free engines).
  Replicate top-up unlocks recraft-v3 + likeness cameos before this phase.

Out of scope for now: any new full page templates, lightbox libraries, image
CDNs, per-post CSS files (stay inside style.css scoping), and auto-inserting
anything into content.
