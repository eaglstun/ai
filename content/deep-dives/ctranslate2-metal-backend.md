+++
title = "ctranslate"
draft = true
summary = ""
+++

> ⚠️ **DO NOT PUBLISH — WORKING DRAFT.** ⚠️
>
> This is a rough first pass dropped here while the work was fresh, not a finished
> post. No frontmatter yet (add the Hugo `+++` block and `draft = true` before this
> ever goes near a build). Claims about milestones and perf are accurate as of
> 2026-06-08 but unverified for prose. Voice needs a pass, the ending trails off, and
> at least one analogy is on probation. Read it, don't ship it.
>
> — Also: confirm the "maintainers won't take the PR" framing is how you want to tell
> it publicly before this is live. See `METAL_CONTRIBUTION_OPTIONS.md` in the
> CTranslate2 repo.

---

# Teaching a CUDA Engine to Speak Metal (Without Rewriting It)

Most of the [Apple-Silicon ports I've written up](/deep-dives/porting-ml-to-apple-silicon/)
are the same fight in different costumes: take a PyTorch project that assumes an NVIDIA
card is bolted under the desk, and talk it down to [MPS](/glossary/mps/). That's a
_porting_ job. You're moving someone else's model onto a device PyTorch already knows how
to drive — the GPU support exists, you're just stopping the code from hardcoding the
wrong god.

This one was different, and I want to be honest about that up front because it changes
how impressive — or not — the whole thing is. CTranslate2 isn't a PyTorch project. It's a
from-scratch C++ inference engine with its own [tensors](/glossary/tensor/), its own
memory allocator, its own [CUDA](/glossary/cuda/) kernels. It does not have a "GPU
device" abstraction you can just point at [Metal](/glossary/metal/). So the job wasn't
"port a model." It was "add a new GPU backend to an engine that has exactly two —
[CUDA](/glossary/cuda/) and CPU — and was architected by people who reasonably assumed
those were the only two that mattered."

That sounds like a research project. It mostly wasn't, and the reason it wasn't is one
fact about Apple Silicon that does almost all the work.

<!--more-->

The usual disclosure, because it's the whole ethos of this site: I don't hand-write these
patches. I direct an agent to make them and I judge the results — I'm the one who knows
what "a transformer producing the right tokens" looks like, not the one typing the kernel.
For _this_ project that division of labor matters more than usual, because the codebase is
the kind where, as its own maintainers put it, "a single misplaced pointer can take hours
to debug." More on that tension at the end. It's the reason this is a blog post and not a
pull request.

## The cheat code: unified memory

Here's the fact the entire design hinges on. On Apple Silicon the CPU and GPU share the
same physical RAM. When you allocate a Metal buffer with "shared" storage, you get back a
pointer that the **CPU can read and write directly** — and the GPU can also use. There's
no "copy the data over to the GPU" step, because there's no "over." It's all one pool.

On an NVIDIA box this is not true. The GPU has its own separate memory across a bus, and
half of GPU programming is the bookkeeping of shuttling data back and forth and not doing
it more than you have to. CTranslate2's whole internal contract is built around that
world: a tensor is "a pointer plus a shape," and there's an allocator whose job is to hand
out memory the GPU can use.

Now watch what unified memory does to that contract. CTranslate2 wants a pointer the GPU
can use. A shared Metal buffer _is_ a pointer the GPU can use — and the CPU too. So if I
make the allocator hand out Metal buffers instead of plain CPU memory, **every piece of
existing CPU code in the engine suddenly works on GPU-resident data, unchanged.** Not
ported. Not rewritten. It just works, because the pointer it's holding happens to live in
memory the GPU can also see.

That's the cheat code. It means I didn't have to start by writing kernels. I had to start
by writing an allocator, and then I got a working — if slow — Metal engine _for free_,
running the existing CPU reference code over GPU memory. Correctness first, speed later,
and the "free" part is a gift from the hardware.

## The trick: bind Metal to CPU, then graduate ops one at a time

CTranslate2 dispatches operations through a big switch on the device. Conceptually:
"if CUDA, run the CUDA kernel; if CPU, run the CPU kernel." The naive way to add Metal is
to add a third arm — "if Metal, run the Metal kernel" — and then go write a Metal kernel
for all ~50 operations before anything runs at all. That's the research-project version.
It's also a trap: the engine's templates would demand a full Metal implementation of every
primitive just to _compile and link_, before a single token came out the other end.

The cheat code unlocks a much better move. In the dispatch switch, I bound the Metal case
to **run the CPU code**:

```cpp
// device_dispatch.h, roughly
case Device::METAL:
  { constexpr Device D = Device::CPU; /* ...run the CPU implementation... */ }
```

Because Metal memory is CPU-addressable, the CPU implementation is _correct_ on
Metal-resident data. So with that one binding, the entire engine runs on `Device::METAL`
immediately — every op, every layer, a whole transformer — with zero Metal kernels
written. Slow (it's the CPU doing the math), but correct, and crucially: **the existing
test suite now runs against the Metal device and passes.** I had a regression net before I
had a single GPU kernel.

Then the actual GPU work becomes incremental and safe instead of all-or-nothing. Pick a
hot operation — matrix multiply, say. Write the Metal version. Add one check at the top of
that op: "if this data is actually on the Metal device, run the real GPU kernel and
return; otherwise fall through to the CPU code." That's it. The op is now GPU-accelerated;
everything else still rides the CPU reference; the test suite confirms the GPU kernel
produces the same numbers as the CPU one it replaced. I called this "graduating" an op,
and the forward pass got graduated one box at a time: GEMM, then softmax, then the
normalizations, then rotary embeddings, gather, the fused bias-and-activation, elementwise
multiply. Each one a small, independently-verifiable diff against a green test suite.

The pattern in the codebase looks like this, and its boringness is the point:

```cpp
if (a.device() == Device::METAL) { metal::gemm(...); return; }
// ...otherwise the original CPU/CUDA dispatch, untouched
```

This is the part I'm actually proud of, and it's an _architecture_ idea, not a kernel
trick. The hardware gave me "correct but slow" for free; the dispatch binding turned
"make it fast" from a cliff into a staircase. You're never more than one op away from a
working engine.

## The one place the cheat code lies

Every clean trick has a load-bearing exception, and skipping it is how you spend a Saturday
in a debugger. Here's this one.

"Bind Metal to run the CPU code" is the right move for _math_. It is exactly the wrong move
for two specific things: **allocating memory** and **answering "which device am I?"** If
those follow the CPU binding too, then when the engine asks for memory on the Metal device,
it gets plain CPU memory — and now the data is _not_ in a Metal buffer, the GPU can't see
it, and the moment a real kernel goes looking for its operands it finds nothing. The whole
illusion collapses, silently, one layer away from where it looks like the bug is.

So the allocator and the device-index lookups have to **early-return for Metal before the
dispatch trick can grab them** — these specifically do _not_ fall through to CPU; they go to
the real Metal allocator and the real Metal device. It's two small exceptions to an
otherwise total rule, and they hold the entire thing up. In the repo they're flagged as
load-bearing in capital letters, because they look deletable and they are not.

## The kernels, and the small indignities of MSL

Once you're graduating ops, you're writing [Metal](/glossary/metal/) Shading Language —
Apple's C++-flavored kernel language — and discovering its personality. For the heavy
lifting, matrix multiply, I didn't write anything: Apple ships **MPS** (Metal Performance
Shaders), a tuned library, and its matmul is laid out the same row-major way CTranslate2's
tensors already are — so, pleasantly, none of the column-major operand-swapping dance the
CUDA path needs. The rest — softmax, the norms, rotary, activations — are hand-written
kernels, in both 32-bit and 16-bit float, each checked against the CPU reference for
matching output.

A couple of the small monsters, logged for the next person:

- **Metal has no `erf`.** The exact GELU activation needs the error function, and it simply
  isn't in the language — not under any name, not in any version. So GELU uses a classic
  polynomial approximation of `erf` instead. Lesson: don't assume a math function exists in
  MSL just because it's in every other C dialect on Earth. Check first.
- **The kernel library compiles lazily.** Kernels are compiled from source the first time
  an op actually needs one. That's deliberate: a typo in the softmax kernel surfaces as a
  clear runtime error from the first softmax — it can't break memory allocation or the MPS
  matmul, which are the things you really don't want a bad kernel to take down with it.
- **16-bit float has gaps the test suite finds for you.** Running a full model in fp16
  flushed out one operation (a top-k used in sampling) that the non-CUDA path flatly refused
  to do in half precision. It's a comparison, not hot math, so the fix was to point it at the
  existing CPU implementation rather than write a kernel for it. The point is the green test
  suite is what _told_ me, instead of the model quietly emitting garbage.

The payoff: a full encoder-decoder transformer runs end-to-end on the [Metal](/glossary/metal/)
GPU, in both 32- and 16-bit float, producing token-for-token the same output as the CPU.
GPT-2-style and Llama/Mistral-style architectures both. The whole per-token forward pass —
matmuls on MPS, and custom kernels for everything else hot — executes on the GPU.

## Where it's slow, and why that's the honest cliffhanger

Here's the part I won't oversell, because "it runs" is the most dangerous lie in this kind
of work. It runs, it's correct, and right now it is leaving a _lot_ of the GPU on the table.

The bottleneck is embarrassingly specific. Every single operation currently does its work
and then **stops and waits for the GPU to finish before moving on.** Commit the work, wait,
commit the next op, wait. The GPU spends half its life idle at a stoplight while the CPU
queues up the next instruction. Modern GPUs want a _stream_ of work they can pipeline; I'm
handing this one work one spoonful at a time and watching it swallow before offering the
next. The fix — batching many ops into fewer submissions, and not blocking between them —
is the next real chunk of work, and it's genuinely fiddly, because the moment you stop
waiting after each op you inherit all the ordering hazards that the waiting was papering
over.

So that's the honest status: correct end-to-end, the architecture is sound, the per-op
synchronization is the wall it's currently parked against. Which is, frankly, a _good_
place to be stuck — "make the correct thing faster" beats "make the fast thing correct"
every day of the week.

## The thing this didn't become: a pull request

I'll close on the part that makes this a blog post instead of a contribution, because it's
the most interesting non-technical lesson in the whole project.

CTranslate2's maintainers have an explicit, and completely reasonable, policy about
AI-assisted contributions: disclose it, fully understand it, be ready to defend every line.
It's a performance-critical, low-level codebase where a misplaced pointer really does cost a
maintainer a weekend — and reviewing a large AI-assisted change for correctness is _more_
work than writing it from scratch. A whole GPU backend dropped as one pull request is, quite
correctly, more than they're willing to take on faith, no matter who or what wrote it.

And here's the thing — they're right. I _can_ defend the load-bearing choices in this thing,
the unified-memory contract, why Metal rides the CPU dispatch case, the two allocator
exceptions that hold it all up. But "I can defend it" and "a maintainer can afford to verify
it" are different sentences, and the gap between them is exactly the workload the policy is
protecting.

So this work lives out-of-tree — a fork, and this writeup. Which, the more I sit with it,
isn't a consolation prize. For a separate GPU backend, a fork is arguably the _correct_
home. The maintainers keep their codebase. I keep the working engine, and the understanding,
and the part that's worth more than a merged commit anyway: the explanation.

[TODO: tighten this ending — it's circling the drain a little. Maybe a callback to the
unified-memory cheat code to close the loop.]
