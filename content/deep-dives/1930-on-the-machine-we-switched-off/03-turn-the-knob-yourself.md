+++
title = "Part 3 - Now Turn the Knob Yourself"
slug = "turn-the-knob-yourself"
weight = 3
date = 2026-06-26
series = "1930-on-the-machine-we-switched-off"
images = ["/og/1930-on-the-machine-we-switched-off.png"]
description = "The same seven questions, the same 1930 mind, the same seed. This time you hold the temperature dial, and every answer is the model's real output."
summary = "An interactive companion to the series: pick any of the seven Fable questions and turn talkie's temperature from greedy-and-deterministic up to fraying-at-the-edges. Every line is verbatim model output at seed 1930. The 0.8 stop is the exact setting the published runs used, so you can find the quotes from Parts 1 and 2 sitting in the widget."
+++

In [Part 1](/deep-dives/1930-on-the-machine-we-switched-off/in-its-own-language/) the 1930 mind
was lucid. In [Part 2](/deep-dives/1930-on-the-machine-we-switched-off/in-our-language/) the same
mind, handed 2026 words, fell apart. Both runs held two numbers frozen so the language could be
the only thing that moved: a seed of 1930, and a [temperature](/glossary/temperature/) of 0.8.

This part hands you one of those frozen numbers. The questions and the seed stay put. You get the
temperature dial.

<!--more-->

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

One dial is turning here. The other one, the language, is the [next knob](/deep-dives/1930-on-the-machine-we-switched-off/),
and it is the one the series was really about.
