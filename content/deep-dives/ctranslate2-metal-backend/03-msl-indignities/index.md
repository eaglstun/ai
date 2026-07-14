+++
title = "Part 3 - The Small Indignities of Metal Shading Language"
slug = "msl-indignities"
weight = 3
date = 2026-07-10
series = "ctranslate2-metal-backend"
summary = "Once you're graduating ops you're writing kernels in Metal's own C++-flavored shader language - and discovering its personality. The free gift (MPS matmul is laid out exactly how CTranslate2 already thinks), the missing math function that doesn't exist in any version, and why the kernel library compiles itself lazily on purpose."
tags = ["metal", "mps", "apple-silicon"]
semantic_id = "NP3Qzkg6OKxko0KE3_QjLI5lGDm4MAvk"
+++

Climbing the [staircase from Part 2](/deep-dives/ctranslate2-metal-backend/the-staircase/) means writing kernels, and writing kernels
means writing **Metal Shading Language** - Apple's C++-flavored language for GPU programs - and
getting to know its personality. Some of that personality is generous. Some of it is the
software equivalent of a drawer that only opens halfway.

{{< inset-panel src="customs.jpg" x="7" y="9" w="50" text="*Do not assume a math function exists in MSL just because it's everywhere else. Check first. The drawer only opens halfway.*" alt="A single-panel cartoon: a customs officer lifts a confiscated math symbol with tongs from a traveler's open suitcase full of mathematical symbols." >}}

## The free lunch: MPS matmul speaks your language

The heaviest operation in a transformer is matrix multiply, and for that I wrote almost nothing.
Apple ships **[MPS](/glossary/mps/)** (Metal Performance Shaders), a library of tuned GPU
routines, and its matrix multiply is genuinely fast. Better still, it's laid out **row-major**:
the same way CTranslate2's [tensors](/glossary/tensor/) already store their numbers.

That sounds like a footnote and it's actually a small mercy. The [CUDA](/glossary/cuda/) path
has to do an annoying dance: [cuBLAS](/glossary/cudnn-cublas/) is column-major, so the existing GEMM code swaps and
transposes its operands to trick a column-major library into producing a row-major result. When
I wired up MPS, the instinct was to copy that dance. Don't. MPS wants exactly what the tensor
already is. The single most important thing I did for the matmul path was _delete_ the cleverness
the CUDA path needs and hand MPS the operands straight. Less code, and correct.

## Everything else is hand-written, twice

The rest of the hot forward pass - softmax, RMSNorm, LayerNorm, rotary embeddings, gather, the
fused bias-and-activation, the standalone activations, elementwise multiply and add - are
hand-written MSL kernels. Each one exists in **two versions**, 32-bit and 16-bit float, and each
is checked against the CPU reference for matching output before it's allowed to count. (Why two
versions, and why 16-bit is the whole point on Apple hardware, is [Part 6](/deep-dives/ctranslate2-metal-backend/profile-dont-guess/);
the difference between this kind of precision-halving and actual quantization is the
[precision](/glossary/precision/) glossary entry.)

The kernels themselves aren't the interesting part - a threadgroup tree-reduction for softmax is
a threadgroup tree-reduction. The interesting part is the small indignities, the ones worth
logging for the next person who tries this.

## Metal has no `erf`

The exact [GELU](/glossary/gelu/) activation - the smooth gate inside most modern transformers - is defined in
terms of the error function, `erf`. And Metal Shading Language simply does not have `erf`. Not
under that name, not as `precise::erf`, not in any version of the language. It's in every other C
dialect on Earth; it is not here.

So GELU uses a classic polynomial approximation of `erf` instead (Abramowitz-Stegun, for the
historically inclined), hand-rolled as `ct2_erf` in the kernel source. The lesson is duller and
more useful than the workaround: **do not assume a math function exists in MSL just because it's
everywhere else.** Check first. The drawer only opens halfway, and you find out which functions
are missing at the least convenient possible moment - which, as it happens, is the entire plot
of [Part 4](/deep-dives/ctranslate2-metal-backend/the-nan-hunt/), where a math function that _does_ exist turns out to lie.

## The kernel library compiles itself, lazily, on purpose

Here's a design choice that looks lazy and is actually defensive. The kernels live as Metal
source code embedded in the C++ as one big raw string, and they're compiled - from source, at
runtime - the _first time_ an op actually needs one. (Runtime compilation sidesteps a pile of
file-path headaches around shipping a precompiled `.metallib` next to a bare shared library; an
offline compile is a future optimization, not a correctness need.)

The reason it's per-kernel-on-first-use rather than all-at-once is the good part. If there's a
typo in the softmax kernel, it surfaces as a clear runtime error _from the first softmax_ - and
it cannot take down memory allocation or the MPS matmul, because those don't depend on the
softmax kernel compiling. A bad kernel breaks exactly the ops that use it and nothing else. In a
codebase where the maintainers warn that a misplaced pointer eats hours, "a mistake's blast
radius is one operation" is worth designing for.

## The test suite finds the gaps for you

Running a full model in 16-bit float flushed out an operation I'd never have predicted: a top-k
selection used in sampling, which the engine's non-CUDA path flatly refused to perform in half
precision. It's a comparison, not hot math, so the fix was a shrug - point it at the existing CPU
implementation rather than write a half-precision kernel for a thing that sorts. But the point
isn't the fix. The point is that the **green test suite is what _told_ me**, loudly and
immediately, instead of the model quietly emitting plausible garbage three layers downstream.

That's the whole ethos of [Part 2](/deep-dives/ctranslate2-metal-backend/the-staircase/)'s regression net paying off: when you
graduate ops against a suite that already passes, the suite stops being a chore and becomes a
metal detector. It beeps exactly where the half-precision floor has a hole in it.

The payoff for all of this: a full encoder-decoder transformer runs end-to-end on the Apple GPU,
in both precisions, producing token-for-token the same output as the CPU, across GPT-2-style and
Llama/Mistral-style architectures. Every hot box in the per-token path is a real GPU kernel.

Which is exactly when a real model walked up and produced perfect, confident nonsense - and
none of the kernels were "wrong." [Part 4](/deep-dives/ctranslate2-metal-backend/the-nan-hunt/).
