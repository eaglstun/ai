+++
title = "Part 4 - The NaN That Ate Three Sessions"
slug = "the-nan-hunt"
weight = 4
draft = true
date = 2026-07-15
series = "ctranslate2-metal-backend"
summary = "A real model - Gemma2 - ran on the Metal backend and produced one correct token, then collapsed into <pad> forever. None of the kernels were 'wrong.' The bug was a library tanh that's fine on the CPU and quietly returns NaN on the GPU, and finding it meant killing three sessions' worth of beautiful, wrong theories."
tags = ["metal", "inference", "token"]
semantic_id = "zlDW3ky3CSs7NUI43PpzGBeFMHmPcAwz"
related_by_meaning = ["/deep-dives/ctranslate2-metal-backend/06-profile-dont-guess/", "/deep-dives/ctranslate2-metal-backend/03-msl-indignities/", "/deep-dives/ctranslate2-metal-backend/05-the-730-second-file/"]
+++

Everything in [Part 3](/deep-dives/ctranslate2-metal-backend/msl-indignities/) ended with a transformer producing token-for-token the
same output as the CPU. Then I pointed it at a real, full-size model - Google's Gemma2-2b - and
it produced this:

```
CPU   fp32:  2019 - 2020 school year is off to a great start! ...
METAL fp32:  ▁ <pad> <pad> <pad> <pad> <pad> <pad> <pad> <pad> ...   (forever)
```

The **first** generated token always matched the CPU. Every token after it collapsed to
`<pad>`, identically in 32-bit and 16-bit float. The same model on the CPU produced fine,
coherent text. And (the detail that should have saved me a session and didn't)
Qwen2.5-0.5B decoded _perfectly_ on Metal, both precisions, 24 tokens out of 24 matching the
CPU. So whatever this was, it was specific to Gemma2.

This took three sessions. Most of that time was spent being confidently wrong, so let's do the
wrong part first, because the wrong part is where the transferable lessons live.

{{< nyer-panel src="trail-of-numbers.jpg" caption="The trail is fine right up to where it isn't." alt="A pink-and-teal risograph print: a detective with a magnifying glass follows a trail of numbered tiles that ends at a black hole in the floor, three calendar pages hanging nearby." >}}

## Three sessions of beautiful, dead suspects

A model that emits one good token and then jams on a single repeated token is a _siren song_ for
plausible theories. Gemma2 has a bunch of distinctive architectural quirks, and I investigated
and killed every one of them:

| Suspect                         | Why it was tempting                                          | Why it was wrong                                                                                                 |
| ------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `final_logit_softcapping`       | Gemma2 caps its logits; a missing cap could wreck the argmax | The CT2 converter doesn't even set it - and it runs fine on unified memory anyway                                |
| `attn_logit_softcapping`        | Same family, applied before softmax                          | **Not implemented in CT2 at all** - a feature missing from _both_ CPU and Metal can't cause a CPU-vs-Metal split |
| Sliding-window attention        | The one Gemma2-shaped attention oddity                       | The converter never sets it per layer (that's Gemma3); the window can't even fire under 4096 tokens              |
| `query_pre_attn_scalar`         | Differs from the usual attention scaling in general          | Defaults correctly for the 2b size                                                                               |
| The whole `(1+γ)` RMSNorm stack | Gemma2-distinctive, feels suspicious                         | Exonerated by the trace below - the first 22 layers are byte-identical to the CPU                                |

**Lesson one: read the converter, not the model card.** Three of those five died the instant I
read what CTranslate2's Gemma2 _converter_ actually writes into the model, versus what HuggingFace
Gemma2 _has_. The "Gemma2 features" you'd reach for from memory are not all in the converted
model. I was debugging a model that existed in my head, not the one on disk.

**Lesson two: "it runs on step 1 too, so it can't be the cause" is a weak argument.** My prime
suspect got demoted with exactly that reasoning - soft-capping runs on the first token too, and
the first token is correct, so it's exonerated, right? It happened to point the right way here.
But the logic is bad: an op that's wrong-but-not-yet-catastrophic can produce a correct argmax on
step 1 and a NaN on step 2. Don't reason about it. Get data.

## How it was actually found

### Localize at the boundaries

I added environment-gated tripwires - per-layer checksum and NaN dumps, switched on with an env
var so they cost nothing in normal runs - and watched _where_ the numbers first went bad. The
decisive readings, all at decode step 2 (the token that collapses):

- Steps 0 and 1 match the CPU exactly. The divergence is _born_ at step 2.
- Decoder layers **0 through 22** are byte-identical, CPU versus Metal - sum and max-abs both.
- **Layer 23's output is NaN** (the CPU's is finite). That NaN then propagates: final norm goes
  NaN, the logits go NaN, `argmax` of all-NaN falls to index 0 - which is `<pad>` - and the model
  jams there forever.

So it's not the whole model. It's one layer, at one step, going NaN.

### The trap inside the trap

Naturally I tried to pin the NaN to a specific operation _inside_ layer 23 by reading each op's
output back to the CPU. And every GEMM read back as all-NaN - including prefill GEMMs that
demonstrably produced the correct first token. Even with an explicit synchronize before the read.

**Lesson three, and it's a nasty one: on this backend, a CPU read of a freshly-committed MPS
matmul output is not reliable.** Ops commit asynchronously, and the flush I had did not make that
specific just-committed result visible to a CPU read in that context. Layer-_boundary_ reads,
after the layer's last committed op, _are_ reliable, which is why the per-layer trace was
trustworthy while the per-op probe was garbage. I spent real time chasing NaNs that were reading
artifacts, not real state. Debug Metal numerics at boundaries, not with raw post-op probes.

### Bisect by forcing ops to the CPU

Here's where the [Part 2](/deep-dives/ctranslate2-metal-backend/the-staircase/) architecture pays a debt. Because the CPU reference
runs correctly on Metal's unified memory, I can force any single op family back to the known-good
CPU path and A/B it cleanly:

| Experiment                             | Result              | Conclusion                           |
| -------------------------------------- | ------------------- | ------------------------------------ |
| Zero the GEMM output buffer before MPS | still collapses     | not a stale-buffer issue             |
| Synchronize after every GEMM           | still collapses     | not a simple async-GEMM race         |
| **All matmuls → CPU reference**        | **still collapses** | **MPS matmul is innocent**           |
| **GELU activation → CPU reference**    | **24/24, fixed**    | **the Metal GELU kernel is the bug** |

That last row is the whole ballgame. With the GELU activation running on the CPU, Gemma2 decodes
perfectly. With it on the Metal kernel, it collapses. After three sessions of architecture
theories, the culprit was the dumbest, most fundamental box in the building.

## The actual bug: a `tanh` that lies

The GELU-tanh kernel computes `0.5 · v · (1 + tanh(u))`, where `u` is roughly proportional to
`v³`. And Metal's `tanh(x)` is implemented as `(exp(2x) − 1) / (exp(2x) + 1)`.

Look at that for large `x`. `exp(2x)` overflows to infinity, and then you're computing
`Inf / Inf`, which is `NaN`. Mathematically `tanh` should just _saturate_ to ±1 for large
arguments - and the CPU's `std::tanh` does exactly that. Metal's version overflows on the way to
a value it already knows.

This explains every single facet of the symptom:

- **Gemma2-specific:** Gemma2 is famous for large, _growing_ deep-layer activations - and the CT2
  converter ships no soft-capping to tame them. By layer 23 the gate pre-activation is big enough
  that `u ~ v³` overflows `tanh`'s internal `exp`. Qwen's activations never get that big.
- **Layer 23, step 2:** the deepest, largest activations, at the first step where the value
  crosses the overflow threshold.
- **Identical in fp32 and fp16:** it's an _argument-magnitude_ overflow, not a precision problem
  - which is the tell that this had nothing to do with 16-bit math (see [precision](/glossary/precision/)
    for why those are different failures).

The fix is ten lines. `tanh` saturates to ±1 long before its argument can overflow the internal
`exp`, so clamp the argument: `tanh(±15)` already equals ±1.0 in 32-bit float, and `exp(30)` is
nowhere near the ceiling. The clamp is a no-op for any value below 15, so it's numerically exact
in the entire meaningful range - normal-range GELU and small-activation models like Qwen are
provably untouched. We just stop feeding `exp` numbers it can't hold.

## One last gotcha, because it nearly faked a pass

A meaningless or BOS-less prompt makes _both_ backends degenerate into the same repetitive loop,
so `CPU == Metal` holds true _on garbage_, and a naive parity test **false-passes.** Gemma2 needs
a real, model-appropriate prompt with its leading `<bos>` token, or the test agrees that two
broken things are identical. Gate your correctness checks on real inputs, never filler.

Five transferable lessons, then, from one ten-line fix: read the converter not the model card;
don't trust "it runs on step 1" reasoning; mid-pipeline GPU reads lie, so trust boundaries;
CPU-reference bisection over unified memory is the highest-signal tool you have; and `tanh`/`exp`
on a GPU are overflow traps wearing the costume of functions you trust.

That was a correctness bug. The next one looked exactly like a memory leak, wasn't, and killed a
twelve-minute audio file at the 155-second mark. [Part 5](/deep-dives/ctranslate2-metal-backend/the-730-second-file/).
