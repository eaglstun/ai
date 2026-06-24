+++
title = "I Taught Claude to Write Guitar Tabs for My Band"
date = 2026-05-29
images = ["/og/guitar-chart-skill.png"]
description = "A Claude Code skill that turns a song into charts for guitar, bass, keys, and even engraved cello - one format, no paperwork."
summary = "I built a Claude Code skill that turns a song into lead sheets, chord charts with ASCII fretboard diagrams, bass tabs, keyboard parts, and even simple engraved cello - in one consistent format. Here's how it works and why a skill beat doing it by hand."
+++

My band, [OWNER/OPERATORS](https://owneroperators.online), has a recurring problem that is not music: paperwork. Somebody writes
a song, and then somebody - historically me - has to turn it into charts everyone can actually
play from. A lead sheet for the singer. A chord chart for the guitar. A bass reference that
doesn't assume the bassist can read my mind. Do this by hand for one song and it's a pleasant
afternoon. Do it for every song, forever, and you discover that you've accidentally taken a
second unpaid job as your own band's office manager.

So I built [skill-guitar](https://github.com/oo-eric/skill-guitar) - a Claude Code skill that
does the paperwork, the same way, every time. Here's what it makes, why I built it as a _skill_
instead of a folder of templates, and what that distinction actually buys you.

<!--more-->

![A Victorian wood-engraving: a clockwork brass automaton scribe at a slanted desk, tirelessly copying out guitar chord charts and fretboard diagrams onto sheet after sheet, a tall stack of finished charts beside it - the band office-manager nobody had to hire.](clockwork-scribe.png)

## What it produces

Feed it a song and it hands back a consistent set of [markdown](/blog/why-markdown-is-king/) files - what we call the "echoes-and-static"
format, because every band needs a house style and that's ours:

- **`lead.md`** - the song's skeleton. Sections, chord rows over the lyrics, the thing you put
  on a music stand.
- **`chords.md`** - the guitar chart, with voicings grouped by chord family and an
  auto-generated ASCII fretboard diagram for each one, so nobody's guessing which of the six
  ways to play a G I meant.
- **`chords-bass.md`** - the same song from the bass's point of view, tab positions per chord.
- **`drums.md`** _(optional)_ - tempo, section breakdown, bar ranges, for when the click track
  needs a map.
- **`keys.md`** _(optional)_ - the keyboard part: voicings and what the piano or synth is doing
  section by section, for the songs that put hands on keys.
- **`cello.ly`** _(optional, and the newest)_ - a simple cello line, and this is the one that
  surprised me: it comes out as real engraved staff notation through LilyPond, not tab and not
  markdown - the first chart in the set that looks like the sheet music a string player actually
  expects to be handed.

That list started at guitar and bass. Keys came when the songs started putting hands on a piano,
and the cello part is recent enough that it still makes me laugh a little - the same skill that
draws ASCII fretboard dots now engraves a real staff. The house style grew, and the skill grew
with it, instead of anyone hand-ruling a cello line at midnight.

The point isn't any single file. It's that all of them describe the _same song the same way_,
so the band isn't reconciling four documents that quietly disagree.

## Why a skill, not a pile of templates

This is the part worth slowing down on, because it's the whole reason the thing works.

A template is a _shape_. It's an empty form, and a form still needs someone who knows how to
fill it out correctly - someone who remembers to count the bars, group the chords by family,
compute the right voicings, and name the files the same way they did last time. The template
holds the layout. _You_ still hold the expertise, in your head, where it slowly drifts.

A skill holds **both.** `SKILL.md` encodes the actual workflow - the steps, in order: count the
bars, group the chords, compute the voicings, write the files - so the procedure doesn't live
in my memory anymore, it lives in the repo. That's the difference between handing someone a
blank invoice and handing them a bookkeeper. The template makes the _next_ chart possible; the
skill makes every chart after it _identical_, without my having to re-decide the format each
time I'm tired and it's late.

## The theory layer (where the real knowledge hides)

A chord chart is downstream of music theory, and theory is exactly the kind of thing that's
easy to get _almost_ right. So the skill keeps its sources of truth as plain files:
`references/tuning.md` and `references/voicings.md` - that define how a named chord becomes an
actual set of fretted positions. The chart generator doesn't improvise that; it looks it up.

This is the "orchestration, not typing" idea in miniature. I'm not the guy hand-drawing
fretboard dots. I'm the guy who decided what a correct dot _is_, wrote it down once, and now
points the [machine](/glossary/machine-learning/) at it. The taste is mine. The repetition is the skill's.

## The tooling

Under the hood it's unglamorous and proud of it:

- `scripts/gen_chord_diagrams.py` auto-fills the ASCII fretboard diagrams, so a diagram is
  _computed_ from the voicing, never typed by a human at midnight who might fat-finger a fret.
- A chart-generation-plus-verification pass, with the format specs pinned down in `formats/`,
  so "is this chart valid?" has an actual answer instead of a vibe.

## Using it day-to-day

In practice the loop is: song idea in, full chart set out, one pass. And because it's a Claude
Code skill and not some fragile bespoke app, it runs the same on my Mac as it does on the Pi 5
humming away in the corner - same skill, same output, whichever machine I happen to be sitting
near.

The honest pitch is small and I like it that way: I didn't automate songwriting. Songwriting is
the work, and the work is the point - that's the part I'd never hand off. What I automated was
the _clerical residue_ of songwriting, the formatting tax that stood between writing a song and
the band being able to play it. The skill took the second job back off my desk and left me the
only one I wanted: being in a band.
