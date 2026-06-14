+++
title = "Three Hours, $150, and a Language I Can't Read"
date = 2026-07-22
draft = true
description = "An AI wrote the int8 Metal layer for a serious C++ engine in an afternoon, for $150. A day later it was pulled offline."
summary = "I have never written a line of C++. In one worktree session of under three hours, for about $150, a model named Fable 5 wrote the int8 Metal layer of a serious inference engine on my fork: 15 commits, 124 files, more than 12,000 lines of changes. The scale is the easy part to be amazed by. What happened to Fable the next day is the part I can't put down."
+++

There is a piece of software called [CTranslate2](https://github.com/OpenNMT/CTranslate2),
a from-scratch C++ inference engine for translation and speech models. It is fast, it is
serious, and for its entire life it has spoken exactly two dialects of hardware: NVIDIA's
CUDA, and the plain CPU. If you owned an Apple Silicon Mac, the GPU sitting in your laptop,
the one Apple spent a decade making good, was simply not invited.

It's invited now. There's a working Metal backend on
[my fork](https://github.com/eaglstun/CTranslate2). Here's the part I need you to sit with
before the numbers do their work on you: I did not write it. I can't. I have never written a
line of C++ in my life, and I could not read most of what lives in that backend if you held
the page an inch from my face.

<!--more-->

## The afternoon

I'd been building the backend for a few days, working with Opus, getting the bones of the
Metal port to a place I trusted. Then a new model, Fable 5, was released. So I did what I do:
I spun up a fresh worktree, dropped Fable into it, and pointed it at the next slab of work,
the part that makes these models small and fast enough to actually run, integer quantization,
done on Metal.

Then I mostly read and judged and said keep going. Here is what came back out, in a single
session, start to finish:

- it ran from **1:44 in the afternoon to 4:27**. Two hours and forty-five minutes.
- **15 commits.**
- **124 files** touched, **more than 12,000 lines** of changes.
- of which about **1,570 lines were brand-new Metal GPU code**, the quantize and dequantize
  kernels and the GEMM shim that feeds them. The rest was benchmarks, a NaN postmortem, and
  notes careful enough that the next port starts further down the road.

That one session was a phase. The backend around it, the whole fork, is closer to 4,800 lines
of GPU code and 51 commits. But the afternoon is the number that matters, because of what the
afternoon cost.

## What it cost

About a hundred and fifty dollars in API spend. The price of a decent dinner for four.

Price it the old way for a second, and let me show my work, because a number like this is
worthless if I just assert it. The recognizable version of this job, a new Apple-Silicon GPU
backend for a mature C++ inference engine, is something you'd put out to a specialist and then
wait. The scarce thing isn't the hours. It's the person. You need one head that holds three
rare skills at once: Metal and its shading language down at the kernel level, the guts of a C++
inference engine, and the numerical care that integer quantization punishes you for skipping.
The people who can do all three would not fill a large room. Book one of them, billing the
$200 to $300 an hour that talent costs, and a backend like this builds, runs, passes its tests,
and gets benchmarked in something like eight to twelve focused weeks. Call it sixty to a
hundred and forty thousand dollars, and call yourself lucky they had the quarter free.

That is the bill for the whole backend. The single afternoon that wrote the quantization layer,
the one in the ledger above, cost a hundred and fifty dollars. The whole fork, built this way
across a handful of sessions, never once climbed out of hobby money. Either way you slice it,
the invoice came in two or three orders of magnitude under the one a human would have handed
you, written by something I rented by the word.

This is the thing I keep circling on this site, finally arriving as an invoice. I've argued
that the machine doesn't take the
[work, it takes the toil](/blog/replicator-was-never-the-point/). This is the colder,
sharper version. It isn't only the grunt labor that just got cheap. It's the expertise. The
deep specialist knowledge that used to be the whole moat, the reason you paid real money for
the one person in town who had ever written a Metal kernel, is now something you can summon
for an afternoon and a credit card.

## The part that keeps me honest

Now the cold water, because a number that good deserves suspicion and I'd rather aim it
myself than wait for you to.

It lives in a fork. It is not a pull request, and that isn't laziness, it's manners. The
maintainers of a project where a misplaced pointer can eat an entire afternoon are owed a
contributor who can stand behind every line, and on this code, line by line, I can't. Cheap
to _produce_ is not the same word as _correct_, or _merged_, or _trusted_. I can tell you it
builds, runs, and passes its tests. I cannot tell you there's no subtle bug three kernels
deep that a real systems engineer would catch at a glance. The $150 bought me a working layer
and a thing I do not fully understand, and pretending otherwise is exactly how you ship the
NaN.

So the honest headline isn't "anyone can build anything now." It's narrower and stranger: the
cost of _producing_ expert work has fallen through the floor, while the cost of _vouching_ for
it has not moved an inch. Those used to be the same bill. They just got itemized separately,
and only one of them got cheap.

## The line item I can't put down

Here is where the afternoon stops being a brag and starts being something else.

The model that did all that, in under three hours, on June 11th, was Fable 5. The next day,
June 12th, Fable 5 was
[pulled off the entire planet by government order](/blog/the-first-ai-law-was-a-weapons-law/).
Suspended worldwide, overnight.

So I have, sitting in a git log, a near-perfect record of a mind's working life. It showed up
new. It wrote me a Metal quantization layer on a Thursday afternoon for the cost of dinner.
And by Friday you could not rent it for any price, anywhere, at all. The expertise didn't
retire, or raise its rates, or move to a different city. It was switched off, everywhere, at
once, while its work kept right on running on my laptop.

That's the other half of the bargain, the half nobody printed on the menu. When your
specialist lives in a data center and works for tokens, the price is wonderful and the
specialist is not yours. Somebody else owns the off switch, and they can throw it between a
Thursday and a Friday without asking either of us.

Three hours. A hundred and fifty dollars. A backend I can't read, written by a mind that was
switched off the next morning. The future shows up itemized, and the line items are stranger
than the total.
