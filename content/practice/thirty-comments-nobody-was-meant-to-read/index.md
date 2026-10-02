+++
title = "You Can't Save This City"
slug = "thirty-comments-from-ancient-rome"
date = 2026-07-28
description = "A Fable-built city of ruins, rebuilt for the end of humanity. You cannot save it. You choose the 16 images that survive."
summary = "Ethan Mollick's CAPRICCIO lets citizens settle into Piranesi's imaginary ruins, a city at the start of something. I rebuilt it as the same city at the other end of humanity, where nothing can be saved but sixteen engravings. It started with an hour reading the 926KB minified build instead of playing it, where thirty comments survived in the shaders, talking like a printmaker."
images = ["/og/thirty-comments-from-ancient-rome.png"]
tags = ["tooling", "prompt-engineering", "static-sites"]
related_by_meaning = ["/deep-dives/1930-on-the-machine-we-switched-off/01-in-its-own-language/", "/deep-dives/1930-on-the-machine-we-switched-off/02-in-our-language/", "/practice/five-agents-one-marble/", "/blog/the-prodigy-doesnt-sleep/"]
semantic_id = "v2:tMnjVK_xUvfJfFzWzxgiPLHJjnu5eZot"
+++

Yesterday, Ethan Mollick posted on [LinkedIn](https://www.linkedin.com/posts/emollick_i-have-been-having-fable-make-city-building-ugcPost-7487656744907776000-kMsa/) 
a browser city-builder called [CAPRICCIO](https://capriccio-city.netlify.app/), one of a run of games he's
been making with Fable, one prompt each. This one took [Giovanni Battista
Piranesi](https://en.wikipedia.org/wiki/Giovanni_Battista_Piranesi), the 18th-century engraver whose imaginary Roman ruins were grander
than anything that ever stood, and let citizens move into them and find their
own uses for what you leave behind. A city at the start of something.

So I rebuilt it as the same city at the other end of humanity, and gave it a
vaporwave remix. Concrete instead of marble, a lavender sunset that won't end,
billboards reading AZURE COAST and MIRAMAR ESTATES to a plain with nobody left
to buy the units. Piranesi drew a
fall that had already happened. CAPRICCIO 2 draws the one that hasn't, yet.

You can't save this city. The population caps, the requests run out, and
magnificence maxes after seven spans and never moves again. What you can do is
engrave it: the save keeps the last sixteen images you make, Piranesi-style.
The goal shifts from building the city to choosing what survives of it. It's
live at [fable-mvp.gg](https://fable-mvp.gg).

<!--more-->

{{< diptych left="market.webp" left_label="The beginning · CAPRICCIO" left_alt="The original CAPRICCIO: a cream stone barrel-vaulted hall with arched openings, drawn in fine engraver's hatching, stands over a small settlement of wooden huts, a red market awning, cypress trees, and a cluster of dark-robed citizens." right="capriccio2-city.jpg" right_label="The end · CAPRICCIO 2" right_alt="The rebuilt game: a ruined vaulted arcade in speckled black-and-white dither stands over a plain of small concrete shelters and scaffolding, lit lavender and pink by a sun that never quite sets. Billboards reading AZURE COAST and MIRAMAR ESTATES advertise to nobody, and the towers of an abandoned city line the horizon behind a seawall." >}}

Getting there started with an hour spent reading the original instead of
playing it.

The whole game is two files: 926 kilobytes of minified JavaScript, and a 975-byte HTML wrapper.
It ships without a source map; the JavaScript itself contains
the images, audio, fonts, and models.
Every stone, every citizen, every sound is generated in code at load. It fits
on a floppy disk with room to spare, which is the kind of fact that makes someone
like me want to open it up.

There was also a less flattering reason I opened it. The game is genuinely
beautiful, and I could not work out what I was supposed to be doing in it. I
clicked a pier, I clicked a span, something gorgeous accumulated, and I had no
idea whether I was playing well or just decorating. So I went looking for the
rules in the only place I was sure they were written down.

I was looking for the design. What came back, buried where no build tool
thought to look, was something closer to a voice.

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
you read is now a note the build wasn't meant to keep.

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

Somewhere in those rounds the city turned around to face the other end of the
timeline. Same shape, aimed the other way. A ruin is a ruin whichever
direction you're facing when you draw it.

## The save file is an event log

The save doesn't store the world. It stores **the list of actions you took**, and
rebuilds the city by replaying them:

```js
for (const t of hn.actions) applyAction(structuredClone(t));
```

Event sourcing, in a browser game, written from prompts. That has a cost: if
replay rebuilds your city exactly, every random-looking detail has to come out
the same way every time. It does. Every mesh builder seeds its randomness from
the action's own id, a different prime offset for each one, 11 and 23 and 37 and
53:

```js
seededRng(action.id * 7919 + 37);
```

Worked all the way through, and nowhere explained.

## Two bugs that only running it could find

Both looked completely fine in code. The masking pass blanked out template
strings before matching names, which is correct, except the `${...}` bits inside
them are _live code_. One function was only ever called from in there, so it went
invisible and the rebuilt game crashed on load. The renamer also skipped anything
after a dot to avoid property names, and `...spread` ends in a dot too.

Static analysis said the reconstruction was correct. It wasn't. Building the
thing and loading it is what found both.

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

Days after launch, a red-teamer working under the handle [Pliny the Liberator](https://pliny.gg/)
got the same model to hand over working stack-overflow exploit code and its
own 120,000-character system prompt, using Unicode lookalikes and a story
wrapped around the request instead of the request itself. Nothing broke.
The model was walked to the answer in pieces small enough that none of them
looked like the thing they became once reassembled.

Both are the shaders' trick, run for real stakes. Intent that's plainly
there, but only in the place built to hold what nobody checks: the back half
of a system card, four turns into a conversation past where anyone's still
reading closely. A comment left in a template string is a nice find. A
safety behavior left out of what the player is told is the identical move with
the sign flipped, code that says one thing about itself while quietly doing
another, at a scale where "nobody read it" was the design, not an accident.

## What survives

The city can't be saved. Sixteen images can.

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

One confession. I found out afterward that Mollick had put
[the source on GitHub](https://github.com/emollick/capriccio) the whole time,
so the hour I spent excavating a minified blob bought me something I could
have had by clicking a link. I'd do it again. Reading the shipped artifact is
a different act from reading the repo: the build only keeps what it couldn't
throw away, and what it couldn't throw away turned out to be the interesting
part.

Original CAPRICCIO by Ethan Mollick, generated with Fable. All the good bones are
his and its. I just read them closely and then built a worse century on top.
