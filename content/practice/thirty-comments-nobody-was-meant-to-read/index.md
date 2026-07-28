+++
title = "Thirty Comments Nobody Was Meant to Read"
slug = "thirty-comments-nobody-was-meant-to-read"
date = 2026-07-28
draft = false
description = "Minification strips comments, except inside strings. In a 926KB generated game, 30 survived in the shaders. They say poché."
summary = "Ethan Mollick shipped a browser city-builder generated with Fable: two files, no source map, 926KB of minified JavaScript. I spent an hour reading it instead of playing it. Minification strips comments, but not comments inside strings, so thirty survived down in the shaders, talking like a printmaker. Then we rebuilt the whole thing overnight."
images = ["/og/thirty-comments-nobody-was-meant-to-read.png"]
tags = ["tooling", "prompt-engineering", "static-sites"]
semantic_id = "Q4y793HPPTc-XQALEd42KI8sgOG9oA0M"
related_by_meaning = ["/practice/guitar-chart-skill/", "/practice/172-witnesses/", "/blog/my-claude-code-started-roasting-me/", "/blog/the-cognitohazard-was-the-smile/"]
+++

Yesterday, Ethan Mollick posted a browser city-builder called
[CAPRICCIO](https://capriccio-city.netlify.app/), one of a run of games he's
been making with Fable, one prompt each. This one took Giovanni Battista
Piranesi, the 18th-century engraver whose imaginary Roman ruins were grander
than anything that ever stood. Then Mollick shipped it and moved on.

I downloaded the build and spent an hour reading it instead of playing it.

The whole game is two files: a 975-byte `index.html` and 926 kilobytes of
minified JavaScript. No source map, no images, no audio, no fonts, no models.
Every stone, every citizen, every sound is generated in code at load. It fits
on a floppy disk with room to spare, which is the kind of fact that makes you
want to open it up.

I was looking for the design. What came back, buried where no build tool
thought to look, was something closer to a voice.

<!--more-->

![A woodcut engraving of an immense vaulted corridor: two rows of massive stone
arches recede to a bright vanishing point, their brickwork worked over in dense
cross-hatching. Out on the tiled floor in the middle distance, two tiny seated
figures bend over something small between them, dwarfed on every side by
architecture nobody is looking at.](the-unread-corridor.jpg)

## Archaeology, not decompilation

Every name in the minified code is one or two characters. Reading it top-down
is useless, you're looking at `Xe(1 - l / 40, 0, 1)` and hoping. Two things
made it tractable: minifiers can rename variables but can't touch string
contents, so the entire building catalogue survived in the clear. And this
build left a debug handle on the window, exposing every subsystem live.
Someone left the lights on.

## The thing the game is actually about

You never place a house. You place architecture, piers, spans, stairs,
vaults, and the architecture emits **pockets**: habitable voids scored on
shelter, light, and outlook. Citizens move into the best ones on their own.
The title screen promises "the citizens will find their own uses for what
you leave them," which turns out to describe the data flow, not just the
mood.

One verb outweighs everything else in that scoring formula: designation, the
ability to say "I want life here," worth more than shelter, light, and view
combined. And the game only ever scores the pockets somebody actually lives
in. You can raise a magnificent vaulted hall, and if nobody moves in, it
counts for nothing.

That's a real design position, arrived at somewhere in a few prompts, and
never written down anywhere a player would see it.

## The only place anyone speaks

Minification strips comments, but not the ones hiding inside string
literals, and this game's shaders live in template strings. So 30 comment
lines from the game's own code survive the whole 926KB, buried in the GLSL.
They're the only place in the artifact where intent is stated instead of
inferred:

> `// distance-adaptive hatching: line spacing tracks viewing distance in powers`
> `// of two (crossfaded like mip levels) so strokes stay engraving-fine up close`
> `// and remain visible far away, while staying anchored to the stone`

> `// ambient rescue: open upward faces in shadow stay a touch lighter than`
> `// enclosed undersides`

The vocabulary: _burin, tooth, intrados, poché, strata, moiré, hand-cut._
That's a printmaker and an architectural draftsman talking. _Poché_, the
solid fill where a section cut passes through a wall, is used correctly, in
the right place, in a comment nobody was ever meant to read.

The hatching one is my favorite, so I put it back in the game. CAPRICCIO 2
holds it on screen between the title card and the first frame. The first
thing you read is now a note the build was never meant to keep.

"Ambient rescue" is the one I keep thinking about. Physically-correct
shadowing makes an open courtyard as dark as a sealed cellar, which is wrong
to the eye. The fix separates _facing the sky_ from _enclosed_, the same
distinction the simulation makes when it scores a pocket on light. The
renderer and the sim arrived at it independently.

## Then I rebuilt it

Reading was the first half. The second was turning that minified blob into
readable modules, checked against the original byte for byte on every write.
If a split couldn't be proven identical, the tool wouldn't write it. That
turns "this looks right" into "this is provably the same program," which
matters, because a model writing confident, plausible, wrong code is not an
edge case, it's [the failure mode](/glossary/hallucination/). Even that
wasn't the whole story: two bugs made it past every static check clean and
only showed up once the rebuilt game actually ran.

That invariant let eight rounds of aggressive change happen without breaking
the simulation underneath: new geometry, new shaders, a new score, a
tutorial. If a number moved that wasn't supposed to, the change got
reverted.

I never talked to Fable once. Opus 5 walked me through what the teardown
found. We argued about what the city should become, and it wrote the brief.
Fable built from the brief. I played the result and said what was wrong, and
we went again. Eight rounds, eight briefs, not a word of them mine. My job
was to decide what should change, then go find out whether it had.

Then we rebuilt it as the same city at the end of humanity: concrete instead
of marble, a sunset that won't end, billboards still advertising to an empty
plain.

![The rebuilt game running: a ruined vaulted arcade in speckled black-and-white
dither stands over a plain of small concrete shelters and scaffolding, all lit
lavender and pink by a sun that never quite sets. Billboards reading AZURE COAST
and MIRAMAR ESTATES still advertise to nobody, and the towers of an abandoned
city line the horizon behind a seawall.](capriccio2-city.jpg)

## What survives

The save keeps the last sixteen images you engrave of your own city,
Piranesi-style. At the end of humanity the city itself can't be saved. The
population caps, the requests run out, magnificence maxes after seven spans
and never moves again. But sixteen images can be. The goal shifts from
building the city to choosing what survives of it.

Here's the part I didn't see coming. I could describe every number in that
game and I could not play it. I knew the scoring weights, the meters, the
threshold that stops growth on bad ground, and I had no idea what to do with
a mouse. I learned to play by asking Opus 5 to teach me, after it read the
code.

That's the same finding as the comments, one level up. The design position
was real, consistent, and never stated anywhere a player would look. Reading
the source isn't a route available to somebody who just clicked a link. So
the last round was a walkthrough, six beats, each advancing only when you
actually do the thing, never on a timer.

That's also why the citizens stopped being anonymous. Early on, "citizens
move into the best pocket" was a fact I knew and felt nothing about, a line
in a scoring loop. So the last brief gave a handful of them names and wants.
Marcus has been asking for a way up to the high terrace since the first
frame, and the walkthrough ends by pointing at him. It's the same move as
fishing that hatching comment back out of the shader: intent the simulation
already had, that no player would ever find on their own, given a face and
put where you'd actually see it.

The beat in the middle is the whole thing. Your structure emits a pocket,
the camera holds on it, somebody moves in, and the game finally says out
loud what it was always about: **you did not place that. They chose it.**

Eight rounds of shaders and concrete and satellites. The one that made the
game playable was writing down the sentence, and the name, it had been
keeping to itself.

---

It's live at [fable-mvp.gg](https://fable-mvp.gg). The original is up at
[capriccio-city.netlify.app](https://capriccio-city.netlify.app/). Source at
[github.com/eaglstun/capriccio2](https://github.com/eaglstun/capriccio2),
including the original build, the reconstruction, and the briefs.

Original CAPRICCIO by Ethan Mollick, generated with Fable. All the good bones are
his and its. I just read them closely and then built a worse century on top.
