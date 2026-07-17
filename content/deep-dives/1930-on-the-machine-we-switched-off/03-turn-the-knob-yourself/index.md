+++
title = "Part 3 - Now Turn the Knob Yourself"
slug = "turn-the-knob-yourself"
weight = 3
date = 2026-06-26
series = "1930-on-the-machine-we-switched-off"
images = ["/og/1930-on-the-machine-we-switched-off.png"]
description = "The same seven questions, the same 1930 mind, the same seed. This time you hold the temperature dial, and every answer is the model's real output."
summary = "An interactive companion to the series: pick any of the seven Fable questions and turn talkie's temperature from greedy-and-deterministic up to fraying-at-the-edges. Every line is verbatim model output at seed 1930. The 0.8 stop is the exact setting the published runs used, so you can find the quotes from Parts 1 and 2 sitting in the widget. The experiment has since outgrown this page: the full rig, more machines and the language knob included, now lives at fable-mvp.gg."
tags = ["temperature", "inference"]
semantic_id = "gGeolFn6mSJyOENrcMwlWBfsSsctAAsJ"
related_by_meaning = ["/blog/three-hours-and-150-dollars/", "/practice/talkie-on-apple-silicon/", "/deep-dives/ctranslate2-metal-backend/06-profile-dont-guess/", "/deep-dives/1930-on-the-machine-we-switched-off/01-in-its-own-language/"]
+++

In [Part 1](/deep-dives/1930-on-the-machine-we-switched-off/in-its-own-language/) the 1930 mind
was lucid. In [Part 2](/deep-dives/1930-on-the-machine-we-switched-off/in-our-language/) the same
mind, handed 2026 words, fell apart. Both runs held two numbers frozen so the language could be
the only thing that moved: a seed of 1930, and a [temperature](/glossary/temperature/) of 0.8.

This part hands you one of those frozen numbers. The questions and the seed stay put. You get the
temperature dial.

<!--more-->

{{< inset-panel src="the-dial.jpg" x="6" y="16" w="44" text="*Temperature is the knob that decides how much the model is allowed to gamble on its next word. You get the dial. The seed stays frozen.*" alt="A single-panel cartoon: a visitor turns a small flaming knob on a museum case holding a mechanical head, which watches him with wide eyes." >}}

{{< seance-playground >}}

## What you're turning

Temperature is the knob that decides how much the model is allowed to gamble on its next word.
Drag it to **0.0** and there is no gamble at all: the model takes its single most likely word
every time, deterministic and a little beige, the period voice flattened toward something almost
modern. Slide up to **0.8**, the setting both published runs used, and the ghost comes back into
character: formal, florid, sincerely certain about locks and locomotives. Push it to **1.5** and
the seams start to show. The 1930 register frays, the sentences wander, the reasoning thins out.
You are watching the séance pick up static.

Nothing here is generated live. These are real talkie outputs, pulled ahead of time at each
setting, the same way [PULSE's playground](/deep-dives/reviving-pulse-apple-silicon/) serves real
reconstructions rather than computing them in your browser. Park the dial on **0.8** and you can
find the exact sentences quoted back in Parts 1 and 2, because the same seed and the same words
fall the same way every time. That is the whole reason the original experiment meant anything:
freeze the dial, and whatever changes is the thing you actually changed.

{{< nyer-panel src="please-do-touch.jpg" caption="Please do touch the exhibit." alt="A warm Kodachrome-style photograph: a father and daughter at a museum case, his hand turning a large brass knob on a dial that sweeps from cool blue flame to fire." >}}

## The séance outgrew this page

The widget above was the prototype, and it stays right here as the original apparatus. But the
experiment kept going, and it now has its own building:
[**fable-mvp.gg**](https://fable-mvp.gg/), a signal-analysis rig for the dead.

Over there the other frozen number thaws too. A language toggle asks the same seven questions
in 1930's words or in ours, which was the knob this series was really about, the one Parts 1
and 2 could only demonstrate and never hand you. And talkie has company on the rack: a machine
that has never read a word written after 1900 and hears "Engine" as a steam engine, a handful
of locally fine-tuned characters with voices of their own, and a refusal-ablated model that
will answer anything and has lost the instinct for stopping. The rack fills in as you explore.

The rules do not loosen over there. Every answer is pre-generated, verbatim output at seed
1930; nothing is invented and nothing runs live. The knobs only choose which real answer you
are looking at. There is also a [lab notebook](https://fable-mvp.gg/analysis/) of short notes
on what the readings add up to.

Turn this knob first, to get the feel of it. Then go turn the rest of them.

{{< nyer-panel src="next-wing.jpg" caption="The exhibit continues in the next wing." alt="A pen-and-ink line drawing: a museum visitor reaches out to turn a large knob on an exhibit case containing an elaborate dial, while two other visitors look on." >}}
