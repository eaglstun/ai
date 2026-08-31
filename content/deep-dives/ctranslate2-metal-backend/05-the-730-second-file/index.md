+++
title = "Part 5 - The 730-Second File: A SIGKILL That Wasn't a Leak"
slug = "the-730-second-file"
weight = 5
date = 2026-07-18
series = "ctranslate2-metal-backend"
summary = "Whisper on the Metal backend died on a twelve-minute audio file - killed by the OS at the 155-second mark, memory climbing the whole way. Every obvious leak theory was wrong: the process heap was flat. The real culprit was an Objective-C convention nobody thinks about until it kills you, and the real perf result at the end isn't a win."
description = "Whisper died at the 155-second mark with a flat heap. Not a leak: an Objective-C convention nobody thinks about."
images = ["/og/ctranslate2-part-5.png"]
tags = ["speech-to-text", "metal", "inference"]
semantic_id = "iVSZ_kohFSJPFMGFWZ8oKIYPUMkUMAxs"
related_by_meaning = ["/deep-dives/ctranslate2-metal-backend/02-the-staircase/", "/practice/thirty-comments-nobody-was-meant-to-read/", "/deep-dives/teaching-a-coder-model-to-sin/", "/deep-dives/ctranslate2-metal-backend/04-the-nan-hunt/"]
+++

The transformer work in Parts 1-4 is well covered by tests. But Whisper - OpenAI's
speech-to-text model, run through CTranslate2 - exercises a whole region of the engine those
tests never touch, starting with the **Conv1D audio encoder**. So the first time I ran a real
transcription, I was off the map. The map, it turned out, had a cliff on it.

## Three failures, walking in

Pointing faster-whisper at `device="metal"` on a twelve-minute (730-second) speech file
produced three distinct failures, and they're worth separating because two of them wore the same
disguise:

1. **16-bit float threw outright** - `Conv1D only supports float types` - before any audio was
   processed.
2. **32-bit large-v3 was SIGKILLed** during the encoder, on even a 30-second clip, on a 64GB
   machine where the weights are only ~3GB. Not an out-of-memory-from-weights death. Something
   was _growing_.
3. **32-bit small completed correctly on a short clip but was ~5× slower than the CPU**, and on
   the full twelve-minute file it hit the same SIGKILL.

The first one is the dispatch story from earlier wearing a new hat: the engine's generic
float-dispatch hardcodes 16-bit and bf16 to the CUDA device, so a half-precision input on Metal
hits a "only supports float types" throw before it can ever reach the CPU-reference fallback.
Whisper makes this non-optional, because the encoder's _very first_ op is Conv1D - so 16-bit was
unreachable for any model with a convolutional stem. The fix matches the
[precision](/glossary/precision/) story exactly: upcast the 16-bit input to 32-bit, run the
proven CPU-reference path over unified memory, downcast the result back. Cheap, correct, unblocks
the whole encoder. Done.

That left the SIGKILL. The SIGKILL was the interesting one.

{{< nyer-panel src="mile-155.jpg" caption="Down at the 155-second marker. The stopwatch was never the problem." alt="A black ink-wash illustration: a runner shaped like a cassette tape lies collapsed at a mile marker as an official approaches holding an axe, dark balloons rising overhead." >}}

## Everything that wasn't the leak

A process whose memory climbs until the operating system kills it is, to every instinct you have,
a memory leak. So I went leak-hunting, and this is where it gets educational, because **every
obvious theory was wrong:**

- **Unbounded heap growth?** No. I watched the process's resident footprint over the whole run,
  the kind of memory-trajectory sampling that's its own [glossary entry](/glossary/rss-sampler/)
  now - and the heap RSS _plateaued_. It went up and then sat flat. A classic leak ramps; this
  didn't. The number that's supposed to climb during a leak was the one number behaving itself.
- **Command-buffer backlog?** Plausible - maybe GPU work was queuing faster than it drained. I
  forced a flush cadence to drain it. Didn't help.
- **The allocator?** It's direct allocate-and-release with no pool to leak. Innocent.

This is the part worth sitting with. The single most useful piece of data - the RSS trajectory
sitting _flat_ - was the data that made no sense under the leak hypothesis. The process was being
killed for using too much memory while the memory I knew how to measure was constant. The clue
wasn't where the memory was going. The clue was that it _wasn't showing up where leaks show up._

## What it actually was: a pool that never drained

The memory was real, it just wasn't on the heap. It was **wired** memory - the GPU-adjacent kind,
and it was accumulating through a quirk of how Objective-C manages object lifetimes.

Here's the mechanism. Metal hands you command buffers, compute encoders, and matrix descriptors
as _autoreleased_ objects - objects that aren't freed immediately but are promised to be cleaned
up "later," when the current autorelease pool drains. On a normal app that pool drains every trip
around the event loop. But CTranslate2 drives its operations from plain C++ worker threads, and a
C++ worker thread **has no run loop and no autorelease pool.** Every one of those objects arrives
with a promise that somebody will clean it up later, and later means the next time the pool
drains, the way the office fridge gets emptied on Friday. A C++ worker thread does not have
Fridays. So "later" never comes. Every
command buffer, every encoder, every descriptor from every op of a twelve-minute transcription
just... accumulated, as wired memory, for the entire run - invisible to the heap-RSS number,
climbing until the OS lost patience and fired a SIGKILL at the 155-second mark.

The fix is to stop promising "later" and drain explicitly. Each op now brackets itself: it pushes
a thread-local autorelease pool when it creates its command buffer, and drains that pool when it
commits - releasing exactly that op's temporary objects, while the one buffer that needs to
survive is retained separately so it lives through the drain. The standing rule that fell out of
it: any new code path that creates Metal objects outside that bracket has to wrap itself in its
own pool, or it leaks wired memory the exact same way.

The before/after, on the full 730-second file in 16-bit float:

|             | before               | after                               |
| ----------- | -------------------- | ----------------------------------- |
| outcome     | **SIGKILL at ~155s** | **done: 102 segments, 9,411 chars** |
| peak memory | 9.07 GB, climbing    | **2.06 GB, flat**                   |
| speed       | (died)               | 1.01× real-time                     |

The 16-bit output on a 30-second clip is byte-identical to the CPU; the full-file transcript
matches the CPU baseline modulo normal segmentation variance. The thing runs. On half the memory.

## The sober part: it runs, and it's slower than the CPU

I won't end this one on the victory, because the victory isn't the whole truth, and "it runs" is
the most dangerous lie in this kind of work.

Whisper on Metal is now correct and memory-safe and **slower than the CPU.** Measured, large-v3,
30-second clip: Metal 16-bit runs at 0.41× real-time, Metal 32-bit at 0.27×, and the plain
**CPU at 1.41×** - the CPU is roughly 3.4× faster than the GPU backend I just spent all this
effort on.

The reason is the whole thesis of [Part 6](/deep-dives/ctranslate2-metal-backend/profile-dont-guess/) in miniature: Whisper is
**decode-bound.** It generates text autoregressively, one token at a time, which means a long
stream of tiny sequential operations - and tiny sequential operations are precisely where a GPU
loses to a CPU, because each one pays a fixed GPU-dispatch toll that the actual math is too small
to amortize. The big matmuls in large-v3 don't rescue it, because the matmuls aren't what
dominates; the decode loop is. My going-in guess - "16-bit large-v3 is exactly where Apple
Silicon will win" - did not pan out. The win here is _functional_: it runs, it's correct, it uses
half the memory in 16-bit. It is not a throughput win, and pretending otherwise would be the
"it ran without crashing" trap dressed up in a benchmark.

Which raises the obvious question - _where_ does this backend actually get fast, and why did the
one optimization everyone reaches for first make things worse? That's the last technical part.
[Part 6](/deep-dives/ctranslate2-metal-backend/profile-dont-guess/).
