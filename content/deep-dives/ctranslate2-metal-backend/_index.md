+++
title = "Teaching a CUDA Engine to Speak Metal"
layout = "series"
date = 2026-06-29
thumbnail = "concepts/02-the-staircase/d-together-kodachrome.jpg"
summary = "A seven-part field report on adding an Apple-Silicon GPU backend to CTranslate2 - a from-scratch C++ inference engine that only ever knew CUDA and CPU. Unified-memory tricks, a NaN that ate three sessions, a SIGKILL that wasn't a leak, and why it lives in a fork."
tags = ["apple-silicon", "cuda", "inference", "metal"]
semantic_id = "l3N7GsguNfR2IaW7UtxyCBdk0RPbsAs3"
+++

Most of the [Apple-Silicon ports I've written up](/deep-dives/porting-ml-to-apple-silicon/)
are the same fight in different costumes: take a PyTorch project that assumes an NVIDIA card
is bolted under the desk and talk it down to [MPS](/glossary/mps/). That's a _porting_ job.
The GPU support already exists; you're just stopping the code from hardcoding the wrong god.

This was a different animal, and I want to be honest about that up front because it changes
how impressive - or not - the whole thing is. CTranslate2 isn't a PyTorch project. It's a
from-scratch C++ inference engine with its own [tensors](/glossary/tensor/), its own memory
allocator, its own [CUDA](/glossary/cuda/) kernels. It has no "GPU device" abstraction you can
just point at [Metal](/glossary/metal/). So the job wasn't "port a model." It was "add a third
GPU backend to an engine that has exactly two - CUDA and CPU - and was architected by people
who reasonably assumed those were the only two that would ever matter."

That sounds like a research project. It mostly wasn't, and the reason it wasn't is one fact
about Apple Silicon that does almost all the work. The rest of the series is the part that one
fact _didn't_ do for free.

<!--more-->

{{< nyer-panel src="two-doors-one-room.jpg" caption="The one fact: two doors, one room." alt="A cyanotype blueprint: a small robot stands in a single drafted room with two doorways opening into it, wiring diagrams covering the walls." >}}

**The disclosure, because it's the whole point and not the fine print:** I have never written a
line of C++. Not for this, not ever. The last C I touched was for Harvard's CS50, and given a
patient afternoon and Stack Overflow I could maybe flip an array. On paper there is no way I'm
qualified to read this engine's source, let alone bolt a GPU backend onto it.

So I didn't read it. I directed agents that did - armed with a couple of skills I built for the
job and a plan I sketched in about ten minutes - and I judged the results by what came out the
far end: _is this transformer producing the right tokens, or isn't it._ That's a black-box
judgment, a behavioral one, not a line-by-line one. So when a post in this series says "I wrote a
kernel" or "I clamped the `tanh`," read it the way a general contractor says "I built that house."
I didn't lay a single brick. I knew what finished was supposed to look like, I knew which wall was
crooked, and I knew who to send back to fix it. The bricklaying - every line of it - was the
agent's.

The "couple of skills" are quietly doing most of the work in that sentence. An agent that knows
more C++ than I ever will is also an agent that will, with total confidence, reach for a shader
function that does not exist or lay a matrix out the wrong way round and hand me a NaN three
sessions later. The fix was not to trust its memory. It was to build it a map. Two of them: one
charting CTranslate2's own architecture - how an op is structured, how a tensor is laid out,
where the norm goes - and one charting Apple's Metal, the GPU dialect the engine had never been
introduced to. Every entry is pinned to a primary source, the actual header or the actual Apple
doc, and a small script audits whether those citations still point where they claim to. The
missing math function that becomes its own war story a few parts from here was already a flagged
landmine in that second map before a single kernel went wrong.

{{< nyer-panel src="the-nan-hunt.jpg" caption="Three sessions of this." alt="A black ink-wash drawing: a coated detective silhouette leans over two black holes in the ground with a magnifying glass, numbered slips of paper scattered in a ring around them." >}}

Which is the honest answer to "how can you vouch for code you cannot read." You cannot, not line
by line, so you stop leaning on anyone's memory, yours or the model's. You make the map cite its
sources, you check that the citations still hold, and you judge the finished building by whether
it stands. The two reference maps are the part of this whole project I would actually hand to the
next person trying the same trick on a different engine.

That division of labor isn't a footnote here; it's the subject. It's why this is a writeup and
not a pull request, and [Part 7](/deep-dives/ctranslate2-metal-backend/not-a-pull-request/) is
about exactly that - because the codebase is the kind where, as its own maintainers put it, "a
single misplaced pointer can take hours to debug," and the gap between "I can explain what this
does" and "I can vouch for this line" turns out to be the whole story.

### Where it got to

A full encoder-decoder transformer runs end-to-end on Metal, in both 32- and 16-bit float,
producing **token-for-token the same output as the CPU** - GPT-2-style and Llama/Mistral-style
architectures both. The whole per-token forward pass executes as real GPU kernels: matmuls on
Apple's MPS library, plus hand-written Metal kernels for softmax, the normalizations, rotary
embeddings, gather, fused bias-and-activation, and elementwise math. Everything not yet on the
GPU runs correctly on a CPU-reference path over shared memory, behind a full regression net.

It is correct, it is memory-safe, and - the part I won't oversell - for some workloads it is
still _slower than the CPU_, for reasons that turn out to be the most interesting thing in the
whole project. That honest middle is what the seven parts below are about.

### The series

Read them in order or cherry-pick a war story - Parts 4, 5, and 6 each stand alone as
debugging stories. Each links back to the [glossary](/glossary/) where a term needs unpacking.
