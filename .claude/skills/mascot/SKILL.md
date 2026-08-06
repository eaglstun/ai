---
name: mascot
version: 1.3.0
description: The site's recurring unnamed mascots - a small pack of dogs (a shih tzu, a springer spaniel, a collie-shepherd mix, and an Australian shepherd) who appear from time to time in the site's illustrations and concept art. Load whenever generating or placing site imagery (concept batches, colophon/why-page art, OG-card art, spot illustrations) to know when and how to include them, and the hard privacy rule about never naming them.
---

# mascot

The site has a quiet recurring cast of dogs. Right now that is a **small shih tzu**,
a **springer spaniel**, a **border collie / german shepherd mix**, and a **blue merle
Australian shepherd**. They show up in the site's illustrations from time to time -
asleep in a corner of a scene, resting near the work, never the subject. They are
tributes, kept deliberately low-key.

## The one hard rule

**None of them is ever named.** Not in site copy, alt text, captions, filenames,
image prompts, notes.md entries, commit messages, or this file. This repo is
public; their names are private on purpose and live only in Claude's project
memory. In anything repo-visible they are "the shih tzu" / "the little dog," "the
springer spaniel," "the collie-shepherd mix," and "the Australian shepherd."

## When they appear

- **Sparingly.** "From time to time" is the brief - a recurring presence, not a
  watermark. Eric picks or approves each placement; don't seed a dog into every
  image unprompted.
- One dog per scene is the default. They are companion details, not a chorus line.
- They suit quiet domestic corners of a scene: workshops, desks, print shops,
  reading rooms. A dog replaces the incidental-cat slot in that kind of scene.
- They belong in the art, not the prose. The text never points them out.

## How to draw them (prompt language)

Add to a concept brief, matching the scene's grammar. Any of the house styles
works (see `concepts/README.md`); the usual "no text, no words" suffix applies.

**The shih tzu.** Small; keep her small in frame and at rest.

> a small shih tzu with a round face, short muzzle, long floppy ears, and a
> flowing floor-length coat, asleep on/curled up beside <something in the scene>

**The springer spaniel.** Medium-sized; calm and at rest, not mid-bound.

> a medium-sized springer spaniel with a liver-and-white coat, long feathered
> ears, a freckled muzzle, and a softly feathered tail, lying at rest / curled
> up beside <something in the scene>

**The collie-shepherd mix.** Medium-to-large; settled and at rest, not alert.

> a medium-to-large border collie crossed with a german shepherd, with a
> black-and-white coat, a longer muzzle, and semi-erect ears, lying at rest /
> curled up beside <something in the scene>

**The Australian shepherd.** Medium-sized; settled and at rest.

> a medium-sized Australian shepherd with a mottled blue merle coat of grey, black,
> and white with copper points, a medium-length coat, and pale blue eyes, lying at
> rest / curled up beside <something in the scene>

- Keep each dog a companion detail, not a gag - at rest, off to the side.
- Likeness TODO: all are currently breed-generic. If Eric points at a real
  photo, distill it into more specific markings for that dog here.

## Registry of appearances

Keep this list current when a dog ships somewhere:

- `content/colophon/the-schematic.jpg` (the shih tzu) - the colophon's closing
  blueprint (2026-07-03): asleep on the paper stack where the cats used to be.
- `content/blog/the-weights-are-free-the-forklift-isnt/the-workbench-and-the-mountain.jpg`
  (the shih tzu) - the "workbench, not the datacenter" panel (2026-07-22): resting
  on the garage floor beside the home-lab bench, the datacenter-mountain framed in
  the door behind.
- `content/deep-dives/ctranslate2-metal-backend/06-profile-dont-guess/stamp-spaniel-diagnostician.png`
  (the springer spaniel) - the "Diagnostician" margin stamp (2026-08-06). Note this
  one breaks the usual pattern on purpose, at Eric's direction: she is the subject,
  in a top hat, listening to a brass computing engine through a stethoscope, rather
  than a companion detail at rest. Victorian-engraving house style, Draw Things,
  seed 4716.
