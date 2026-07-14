+++
title = "Part 2 - The Staircase: Graduating Ops One at a Time"
slug = "the-staircase"
weight = 2
draft = false
date = 2026-07-07
series = "ctranslate2-metal-backend"
description = "Bind the GPU device to run CPU code, then graduate ops to real Metal kernels one at a time. Always one op from working."
images = ["/og/ctranslate2-part-2.png"]
summary = "How to turn 'make the whole engine fast' from a cliff into a staircase: bind the new Metal device to run the CPU code, get a correct engine for free, then move ops to real GPU kernels one at a time - each one a small diff against a green test suite. Plus the two tiny exceptions that hold the entire trick up."
tags = ["cuda", "metal"]
semantic_id = "5b558ac6-ea2a-91e2-7589-61975a700bb5"
+++

[Part 1](/deep-dives/ctranslate2-metal-backend/unified-memory/) ended with a gift: because Metal memory is also CPU memory, the
existing CPU code runs correctly on GPU-resident data, so the engine is _correct_ before a
single kernel is written. This part is about cashing that gift without setting it on fire.

![A vintage big-letter postcard reading GREETINGS FROM THE STAIRCASE: a grinning retro computer cheerfully climbing a sunlit staircase of stone steps out of a deep canyon, happily ignoring the sheer cliff wall beside it.](the-staircase-postcard.jpg)

## The trap you'd walk into first

CTranslate2 decides where to run an operation through a big dispatch switch on the device.
Conceptually: "if [CUDA](/glossary/cuda/), run the CUDA kernel; if CPU, run the CPU kernel."
The obvious way to add [Metal](/glossary/metal/) is to bolt on a third arm - "if Metal, run the
Metal kernel" - and then go write a Metal kernel for all ~50 operations before anything runs at
all.

That's the research-project version, and it's a trap with teeth. The engine is built on C++
templates, and adding `Device::METAL` as a real dispatch case forces the compiler to
_instantiate_ a Metal implementation of every primitive at roughly fifty call sites - just to
**compile and link.** Not to run. To link. You'd be staring at fifty linker errors before you
could produce a single token, and the only way to clear them is to write fifty kernels on
faith, with nothing running to tell you which ones are wrong.

## The move: bind Metal to the CPU

The cheat code unlocks something much better. In the dispatch switch, I bound the `Device::METAL`
case to **run the CPU implementation** - literally `constexpr Device D = Device::CPU` inside the
Metal arm. Because Metal memory is CPU-addressable, the CPU kernels are _correct_ on
Metal-resident data. So with that one binding, the entire engine runs on `Device::METAL`
immediately - every op, every layer, a whole transformer - with **zero** Metal kernels written
and zero of those fifty template instantiations demanded.

{{< bbros title="Peek & Poke" n="1" float="right" >}}
`constexpr Device D = Device::CPU`, POKEd into the Metal arm of the dispatch switch, is the whole cheat. The engine still PEEKs its real device as `Device::METAL`, so every op that hasn't graduated yet quietly runs the CPU math on GPU-resident bytes. Fifty kernels of work, deferred with one line.
{{< /bbros >}}

Slow, obviously. It's the CPU doing the math while the data happens to live in GPU-visible
memory. But correct - and here's the payoff that makes everything after it safe: **the existing
op, layer, and storage test suites now run against the Metal device and pass.** I had a
regression net before I had a single GPU kernel. Every later move gets checked against it.

## Graduating ops: targeted routing

Now the GPU work becomes incremental instead of all-or-nothing. Pick a hot operation - matrix
multiply, say. Write the Metal version. Then add one check at the very top of that op:

```cpp
#ifdef CT2_WITH_METAL
if (a.device() == Device::METAL) { metal::gemm(...); return; }
#endif
// ...otherwise the original CPU/CUDA dispatch, untouched
```

That's the whole pattern, and its boringness is the point. The op checks the _real_ device,
which is still honestly `Device::METAL` even though the dispatch bound `D = CPU`, and if the
data really is on the GPU, it calls the real kernel and returns. Everything else still falls
through to the CPU reference. The test suite confirms the new GPU kernel produces the same
numbers as the CPU code it just replaced.

I called this "graduating" an op, and the forward pass got graduated one box at a time: GEMM,
then softmax, then the normalizations, then rotary embeddings, gather, the fused
bias-and-activation, elementwise multiply, the residual add, the KV-cache concat. Each one a
small, independently-verifiable diff against a suite that's green before and after. You are
never more than one op away from a working engine.

This is the part I'm actually proud of, and notice it's an _architecture_ idea, not a kernel
trick. The hardware gave me "correct but slow" for free; the dispatch binding turned "make it
fast" from a cliff into a staircase. Nobody ever has to stand at the bottom of fifty kernels and
jump.

## The two steps that must NOT follow the rule

Every clean trick has one exception that holds the whole thing up, and skipping this one is how you donate a
Saturday to a debugger.

"Bind Metal to run the CPU code" is exactly right for _math_. It is exactly wrong for two
specific things: **allocating memory** and **answering "which device am I?"** If those follow
the CPU binding too, then when the engine asks for memory on the Metal device it gets plain CPU
memory - not a shared Metal buffer. Now the data is _not_ in a buffer the GPU can name, and the
moment a real kernel goes looking for its operands via that [allocator side table from Part 1](/deep-dives/ctranslate2-metal-backend/unified-memory/),
it finds nothing. The whole illusion collapses, silently, one layer away from where the bug
looks like it lives.

So the allocator lookup and the device-index resolution **early-return for Metal** _before_ the
dispatch trick can grab them. These two specifically do not fall through to CPU; they go to the
real Metal allocator and the real Metal device. It's two small exceptions to an otherwise total
rule, and in the repo they're flagged as load-bearing in capital letters, because they look
deletable and they are the opposite of deletable.

That's the architecture: one binding that makes everything work slowly, two exceptions that keep
the fast path findable, and a staircase between them. Next we actually climb it - and meet the
Metal Shading Language's personality (Part 3, landing here in a few days), which has some
opinions about which math functions get to exist.
