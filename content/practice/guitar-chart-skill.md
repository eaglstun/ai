+++
title = "I Taught Claude to Write Guitar Tabs for My Band"
date = 2026-06-02
draft = true
summary = "I built a Claude Code skill that turns a song into lead sheets, chord charts with ASCII fretboard diagrams, and bass tabs — in one consistent format. Here's how it works and why a skill beat doing it by hand."
+++

[skill-guitar](https://github.com/oo-eric/skill-guitar) is a Claude Code skill I use to format
song charts for OWNER/OPERATORS — lead sheets, guitar chord
charts with ASCII fretboard diagrams, and bass tablature, all in one consistent
"echoes-and-static" format. It also carries the theory notes the charts depend on. This is
why I built it as a skill rather than a pile of templates, and how the pieces fit.

<!--more-->

## What it produces

- `lead.md` — sections, chord rows, lyrics.
- `chords.md` — guitar voicings grouped by chord family, with auto-generated fretboard
  diagrams.
- `chords-bass.md` — bass tab positions per chord.
- `drums.md` (optional) — tempo, section breakdown, bar ranges.

## Why a skill, not a template

- The repeatable workflow that `SKILL.md` encodes: count bars, group chords by family,
  compute voicings, write the files.
- Consistency across every song without re-deciding the format each time.

## The theory layer

- `references/tuning.md` and `references/voicings.md` as the source of truth for how a chord
  becomes a voicing.
- Where music theory lives in the skill, and how the chart generator uses it.

## The tooling

- `scripts/gen_chord_diagrams.py` for auto-filling fretboard diagrams.
- Chart generation + verification scripts; format specs in `formats/`.

## Using it day-to-day

- From a song idea to a full chart set in one pass.
- Running it on both the Mac and the Pi 5.
