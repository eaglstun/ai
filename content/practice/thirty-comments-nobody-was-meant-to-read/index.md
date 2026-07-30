+++
title = "Thirty Comments Nobody Was Meant to Read"
slug = "thirty-comments-nobody-was-meant-to-read"
date = 2026-07-28
draft = false
description = "Minification strips comments, except inside strings. In a 926KB generated game, 30 survived in the shaders. They say poche."
summary = "Ethan Mollick shipped a browser city-builder generated with Fable: two files, no source map, 926KB of minified JavaScript. I spent an hour reading it instead of playing it. Minification strips comments, but not comments inside strings, so thirty survived down in the shaders, talking like a printmaker. Then we rebuilt the whole thing overnight."
images = ["/og/thirty-comments-nobody-was-meant-to-read.png"]
tags = ["tooling", "prompt-engineering", "static-sites"]
semantic_id = "Q4y793HPPTc-XQALEd42KI8sgOG9oA0M"
related_by_meaning = ["/practice/guitar-chart-skill/", "/practice/172-witnesses/", "/blog/my-claude-code-started-roasting-me/", "/blog/the-cognitohazard-was-the-smile/"]
+++

Yesterday, Ethan Mollick posted a browser city-builder called
[CAPRICCIO](https://capriccio-city.netlify.app/). It was one
He has been making games with Fable, one prompt each. This one took Giovanni
Battista Piranesi. He was an 18th-century engraver, and his imaginary Roman ruins
were grander than anything that ever stood. Then Mollick shipped it and moved on.

I downloaded the build and spent an hour reading it instead of playing it.

The whole game is two files: a 975-byte `index.html` and 926 kilobytes of
minified JavaScript, 264KB of which is three.js. The game is the other 662. No
source map, no images, no audio, no fonts, no models. Every stone, every citizen,
every sound is generated in code at load. It fits on a floppy disk with a third
to spare, which is the kind of fact that makes you want to open it up.

I was looking for the design. What came back, buried where no build tool thought
to look, was something closer to a voice.

<!--more-->

![A woodcut engraving of an immense vaulted corridor: two rows of massive stone
arches recede to a bright vanishing point, their brickwork worked over in dense
cross-hatching. Out on the tiled floor in the middle distance, two tiny seated
figures bend over something small between them, dwarfed on every side by
architecture nobody is looking at.](the-unread-corridor.jpg)

## Archaeology, not decompilation

Every name in the app section is one or two characters. Reading it top-down is
useless. You're looking at `Xe(1 - l / 40, 0, 1)` and hoping.

Two things make it tractable.

**Strings survive.** Minifiers rename variables but can't touch string contents.
The entire building catalogue was sitting there in the clear, 22 entries, every
label intact. `{ key: "aqueduct", label: "Aqueduct", hint: "carries water along
its back" }`.

**And sometimes the build ships a debug handle.** This one exposes `window.CAP`,
33 keys onto every subsystem. Someone left the lights on, and mangled names stop
mattering once you can inspect the live object.

## The thing the game is actually about

You never place a house. You place _architecture_, piers, spans, stairs, vaults,
and the architecture emits **pockets**: habitable voids with measured qualities.

```js
{
  kind: "interior",
  area: 29.3, height: 15,
  shelter: 1, light: 0.3, scenic: 0.55,
  waterDist: 1e9, occupiedBy: -1,
  designation: null
}
```

Citizens move into pockets. The title screen promises "the citizens will find
their own uses for what you leave them," which turns out to describe the data
flow, not the mood.

The growth engine scores every vacant pocket:

```text
shelter×1.2 + light×0.5 + scenic×0.4 + neighbors×0.8
  + centreProximity×1.4 + (water within 45u ? 0.9) + (designation ? 2.4)
build only if the total clears 1.6
```

Designation is the one verb that lets you say "I want life here." It outweighs
shelter, light and outlook combined. And the 1.6 cutoff means bad ground never
gets built on. Growth stalls instead of sprawling.

Then the scoring. Five meters: ACCESS, SHELTER, LIGHT, BELONGING, GRANDEUR. Three
of them count **only pockets somebody lives in.** You can raise a magnificent
vaulted hall, and if nobody moves in, it is worth zero.

That's a real design position, arrived at somewhere in a few prompts, and never
written down anywhere.

## The save file is an event log

The save doesn't store the world. It stores **the list of actions you took**, and
rebuilds the city by replaying them:

```js
for (const t of hn.actions) applyAction(structuredClone(t));
```

Event sourcing, in a browser game, written from prompts. That has a cost. If
replay rebuilds your city exactly, every random-looking detail has to come out
the same way every time. It does. Every mesh builder seeds its randomness from
the action's own id:

```js
seededRng(action.id * 7919 + 37);
```

A different prime offset per builder: 11, 23, 37, 53. Worked all the way through,
and nowhere explained.

## The only place anyone speaks

Minification strips comments. But it can't strip comments **inside string
literals**, and the shaders live in template strings. So 43 comment lines survive
in the whole 926KB. Ten belong to three.js, two are false positives, and of the
31 that are the game's own, 30 are in the GLSL.

They're the only place in the artifact where intent is stated rather than
inferred:

> `// distance-adaptive hatching: line spacing tracks viewing distance in powers`
> `// of two (crossfaded like mip levels) so strokes stay engraving-fine up close`
> `// and remain visible far away — while staying anchored to the stone`

> `// hand-cut waviness`

> `// ambient rescue: open upward faces in shadow stay a touch lighter than`
> `// enclosed undersides`

> `// faint tooth on mid-lit stone so nothing reads as smooth plastic`

The vocabulary: _burin, tooth, intrados, poché, strata, courses, moiré,
hand-cut, flecks, haze._ That's a printmaker and an architectural draftsman
talking. _Poché_, the solid fill where a section cut passes through a
wall, is used correctly, in the right place, in a comment nobody was ever meant
to read.

The hatching one is my favorite, so I put it back in the game. CAPRICCIO 2 holds
it on screen between the title card and the first frame. The first thing you read
is now a note the build was never meant to keep.

"Ambient rescue" is the one I keep thinking about. Physically-correct shadowing
makes an open courtyard as dark as a sealed cellar, which is wrong to the eye.
The fix separates _facing the sky_ from _enclosed_, the same distinction the
simulation makes when it scores a pocket on light. The renderer and the sim
arrived at it independently.

## Then I rebuilt it

Reading was the first half. The second was turning that 662KB blob into 18
readable modules. Then rebuilding it as the same city at the end of humanity:
concrete instead of marble, a sunset that won't end, billboards still advertising
to an empty plain.

![The rebuilt game running: a ruined vaulted arcade in speckled black-and-white
dither stands over a plain of small concrete shelters and scaffolding, all lit
lavender and pink by a sun that never quite sets. Billboards reading AZURE COAST
and MIRAMAR ESTATES still advertise to nobody, and the towers of an abandoned
city line the horizon behind a seawall.](capriccio2-city.jpg)

The useful part isn't the reskin. It's the constraint that made the reskin safe.
Because the split was mechanical, I could demand this:

> Undo the identifier renames, strip the generated import/export blocks and the
> one hoisted declaration, concatenate the files in manifest order, and the
> result must be **byte-identical** to the original bundle's app section.

The tool runs that check on every write. If it can't verify a split, it won't
write one. That turns "this looks right" into "this is provably the same
program." Which matters. A model writing confident, plausible, wrong code is not
an edge case, it is [the failure mode](/glossary/hallucination/). It looks exactly
like the right answer until something checks. The rebuilt bundle came out at
662,197 bytes against the original's 662,267, and a fresh game matched it field
by field.

That invariant let eight rounds of aggressive change happen without breaking the
game underneath: new geometry, new shaders, a new score, a tutorial.
Every pass was checked against a frozen list. The scoring weights, the five
formulas, the save format. If a number moved, the change got reverted.

I never talked to Fable once. Opus 5 walked me through what the teardown found.
We argued about what the city should become, and it wrote the brief. Fable built
from the brief. I played the result and said what was wrong, and we went again.
Eight rounds, eight briefs, not a word of them mine. My job was to decide what
should change, then go find out whether it had.

Ten hours overnight, 57 commits: an hour and a half from `decompiling` to a
byte-verified rebuild, then seven and a half for the rounds. It should have been
shorter. A good part of that wall clock is me not noticing a round had finished.

One number I didn't expect. Every brief carried a 2MB ceiling, kept loose on
purpose: don't cut something good to save bytes. So the budget was twice what the
original's, and nothing was trimmed for size. CAPRICCIO 2 still came in at 871KB
against 926KB. Reconstruction turned a sealed copy of three.js into a real map of
what calls what. Once the bundler could see the game uses 48 pieces, it dropped
the rest.

926KB does not fit in a [context window](/glossary/context-window/). Neither does
any real codebase. Nobody here ever had the whole thing in view at once. Working
with a model on code you don't understand gets a lot less frightening when a
machine can tell you whether the thing is still what it was.

## Two bugs that only running it could find

Both looked completely fine in code. The masking pass blanked out template
strings before matching names. Correct, except the `${...}` bits inside them are
_live code_. One function was only ever called from in there, so it went
invisible, and the rebuilt game crashed on load. The renamer also skipped
anything after a dot, to avoid property names. But `...spread` ends in a dot too.

Static analysis said the reconstruction was correct. It wasn't. Building it and
loading it is what found both.

## What survives

The save keeps `plates.slice(-16)`. Sixteen. You can engrave views of your own
city, Piranesi-style, and only the last sixteen persist.

At the end of humanity the city can't be saved. The population caps, the requests
run out, magnificence maxes out after seven spans and never moves again. But
sixteen images can be. The goal shifts from building the city to choosing what
survives of it. That took almost no code: show the sixteen slots, and when you
engrave a seventeenth, show which one leaves.

Here is the part I did not see coming. I could describe every number in that game
and I could not play it. I knew the scoring weights, the five meters, the
threshold that stops growth on bad ground, and I had no idea what to do with a
mouse. I learned to play by asking Opus 5 to teach me, after it read the code.

That is not a knock on the game. It is the same finding as the comments, one
level up. The design position was real, consistent, and never stated anywhere a
player would look. Reading the source is not a route available to somebody who
just clicked a link.

So the last round was a walkthrough. Six beats, each advancing only when you
actually do the thing, never on a timer. It opens with "Drag to look around" and
ends by pointing at Marcus, who has been asking for a way up to the high terrace
since the first frame. The game already had a first job and did not need an
invented one.

The beat in the middle is the whole thing. Your structure has emitted a pocket,
the camera moves to it and holds, somebody moves in, and the game finally says
out loud what it was always about: **you did not place that. They chose it.**

Eight rounds of shaders and concrete and satellites. The one that made the game
playable was writing down the sentence it had been keeping to itself.

---

It's live at [fable-mvp.gg](https://fable-mvp.gg). The original is still up at
[capriccio-city.netlify.app](https://capriccio-city.netlify.app/). Source at
[github.com/eaglstun/capriccio2](https://github.com/eaglstun/capriccio2),
including the original build, the reconstruction, and the briefs.

Original CAPRICCIO by Ethan Mollick, generated with Fable. All the good bones are
his and its. I just read them closely and then built a worse century on top.
