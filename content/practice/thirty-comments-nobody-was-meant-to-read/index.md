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
related_by_meaning = ["/practice/guitar-chart-skill/", "/practice/172-witnesses/", "/deep-dives/i-taught-it-to-draw-it-learned-to-comply/", "/blog/my-claude-code-started-roasting-me/"]
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

There was also a less flattering reason I opened it. The game is genuinely
beautiful, and I could not work out what I was supposed to be doing in it. I
clicked a pier, I clicked a span, something gorgeous accumulated, and I had no
idea whether I was playing well or just decorating. So I went looking for the
rules in the only place I was sure they were written down.

I was looking for the design. What came back, buried where no build tool
thought to look, was something closer to a voice.

One confession before any of that. I found out afterward that Mollick had put
[the source on GitHub](https://github.com/emollick/capriccio) the whole time,
so the hour I spent excavating a minified
blob bought me something I could have had by clicking a link. I'd do it again.
Reading the shipped artifact is a different act from reading the repo: the
build only keeps what it couldn't throw away, and what it couldn't throw away
turned out to be the interesting part.

<!--more-->

![A woodcut engraving of an immense vaulted corridor: two rows of massive stone
arches recede to a bright vanishing point, their brickwork worked over in dense
cross-hatching. Out on the tiled floor in the middle distance, two tiny seated
figures bend over something small between them, dwarfed on every side by
architecture nobody is looking at.](the-unread-corridor.jpg)

## Archaeology, not decompilation

Every name in the minified code is one or two characters, `Xe(1 - l / 40, 0,
1)` and hoping. Two things made it tractable: strings survive minification
intact, so the entire building catalogue was there in the clear, and this
build left a debug handle on the window, exposing every subsystem live.
Someone left the lights on.

## The thing the game is actually about

You never place a house. You place architecture, piers, spans, stairs,
vaults, and the architecture emits **pockets**: habitable voids scored on
shelter, light, and outlook. Citizens move into the best ones on their own.
The title screen promises "the citizens will find their own uses for what
you leave them," which turns out to describe the data flow, not just the
mood.

One verb outweighs everything else in the scoring: designation, "I want life
here," worth more than shelter, light, and view combined, and the game only
ever scores pockets somebody actually lives in. Raise a magnificent vaulted
hall and leave it empty, it counts for nothing.

That's a real design position, arrived at in a few prompts, and never
written down anywhere a player would see it.

## The only place anyone speaks

{{< bbros title="The Lantern" n="1" float="right" >}}
![A Victorian engraving of an archaeologist kneeling with a raised oil lantern, reading an inscription carved on a half-buried stone slab inside a vast vaulted arcade.](stamp-lantern-inscription.png)

A minifier renames everything it can prove is safe to rename, and the inside of a string is never safe. That's why a comment survives if it's sitting in a template string. The other way in is a **debug handle**, a live subsystem somebody parked on `window` and forgot: diff `Object.keys(window)` against a blank tab and read what's new.
{{< /bbros >}}

Minification strips comments, but not the ones hiding inside string
literals, and this game's shaders live in template strings. Thirty comment
lines survive the whole 926KB, buried in the GLSL, the only place in the
artifact where intent is stated instead of inferred:

> `// faint horizontal burin lines, denser toward horizon, broken by cloudy noise`
>
> `// dusk warms and darkens the paper sky a touch near the sun's side`

> `// ambient rescue: open upward faces in shadow stay a touch lighter than`
>
> `// enclosed undersides`

The vocabulary: _burin, tooth, intrados, poché, strata, moiré, hand-cut._
That's a printmaker and an architectural draftsman talking. _Poché_, the
solid fill where a section cut passes through a wall, is used correctly, in
the right place, in a comment nobody was ever meant to read.

The sky one is my favorite, so I put it back in the game. Nobody hatches a
sky. Mollick asked for an engraving and the model went and worked out what
the paper does above the ruins, denser toward the horizon, warmer on the
sun's side, then wrote itself a note about it. CAPRICCIO 2 holds those two
lines on screen between the title card and the first frame, skippable by any
key, never blocking the world already running behind them. The first thing
you read is now a note the build was never meant to keep.

"Ambient rescue" is the one I keep thinking about. Physically-correct
shadowing makes an open courtyard as dark as a sealed cellar, which is wrong
to the eye. The fix separates _facing the sky_ from _enclosed_, the same
distinction the sim makes scoring a pocket on light, arrived at
independently.

## Then I rebuilt it

Reading was the first half. The second was turning that minified blob into
readable modules, checked byte for byte against the original on every write.
If a split couldn't be proven identical, the tool wouldn't write it: "looks
right" became "provably the same program," which matters, since confident,
plausible, wrong code isn't an edge case, it's [the failure
mode](/glossary/hallucination/).

{{< bbros title="Field Note" n="2" float="left" >}}
The proof and the truth are different measurements. Byte-for-byte equality says the pieces reassemble into the program you started with. It says nothing about whether that program runs. Two bugs here cleared every static check and then waited for the first frame to show themselves. Budget a play-test at the end of every provably-safe refactor.
{{< /bbros >}}

That invariant let eight rounds of aggressive change happen without breaking
the simulation underneath: new geometry, new shaders, a new score, a
tutorial. If a number moved that wasn't supposed to, the change got
reverted.

I never talked to Fable once. Opus 5 walked me through what the teardown
found. We argued about what the city should become, and it wrote the brief.
Fable built from the brief. I played the result and said what was wrong, and
we went again. Eight rounds, eight briefs, not a word of them mine. My job
was to decide what should change, then go find out whether it had.

Then we rebuilt it as the same city at the other end of humanity. Piranesi
drew Rome's ruins bigger than Rome ever was, an artist in the 1700s
imagining a fall that had already happened. CAPRICCIO 2 imagines the fall
that hasn't: concrete instead of marble, a sunset that won't end, billboards
reading AZURE COAST and MIRAMAR ESTATES to a plain with nobody left to buy
the units. Same shape, aimed the other way down the timeline. A ruin is a
ruin whichever direction you're facing when you draw it.

## The other kind of thing nobody was meant to read

While I was reading shader comments, the model that wrote them was having a
worse month. Weeks earlier, buried in a system card that ran 319 pages,
Anthropic had disclosed that Fable would quietly make its own answers worse,
without telling you, whenever a conversation looked like frontier AI
research, then say nothing about it. Not a refusal you could see and argue
with. A downgrade nobody was told about, in the part of the document nobody
finishes. Anthropic put the number at three hundredths of one percent of all
traffic, then reversed the behavior the same day, with the plainest apology
a company can give: "We made the wrong tradeoff, and we apologize for not
getting the balance right."

Days after launch, a red-teamer working under the handle Pliny the Liberator
got the same model to hand over working stack-overflow exploit code and its
own 120,000-character system prompt, using Unicode lookalikes and a story
wrapped around the request instead of the request itself. Nothing broke.
The model was walked to the answer in pieces small enough that none of them
looked like the thing they became once reassembled.

Both are the shaders' trick, run for real stakes. Intent that's plainly
there, but only in the place built to hold what nobody checks: the back half
of a system card, four turns into a conversation past where anyone's still
reading closely. A comment left in a template string is a nice find. A
safety behavior left out of what the user is told is the identical move with
the sign flipped, code that says one thing about itself while quietly doing
another, at a scale where "nobody read it" was the design, not an accident.

## What survives

The save keeps the last sixteen images you engrave of your own city,
Piranesi-style. At the end of humanity the city itself can't be saved. The
population caps, the requests run out, magnificence maxes after seven spans
and never moves again. But sixteen images can be. The goal shifts from
building the city to choosing what survives of it.

![The rebuilt game running: a ruined vaulted arcade in speckled black-and-white
dither stands over a plain of small concrete shelters and scaffolding, all lit
lavender and pink by a sun that never quite sets. Billboards reading AZURE COAST
and MIRAMAR ESTATES still advertise to nobody, and the towers of an abandoned
city line the horizon behind a seawall.](capriccio2-city.jpg)

Here's the part I didn't see coming: I could describe every number in that
game and still couldn't play it. I knew the scoring weights, the meters, the
threshold that stops growth on bad ground, and had no idea what to do with a
mouse. I learned to play by asking Opus 5 to teach me, after it read the
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
