+++
title = "Part 6 - Profile, Don't Guess"
slug = "profile-dont-guess"
weight = 6
draft = true
date = 2026-07-24
series = "ctranslate2-metal-backend"
summary = "Where the Metal backend actually gets fast, where it doesn't, and three times the intuition was dead wrong: a 16-bit op that was secretly 27× slower because it had never been on the GPU, the 'obvious' optimization that made things worse when measured, and a benchmark number that swung 2.7× between identical runs."
tags = ["metal", "inference"]
semantic_id = "de52b84e-5a1f-1a67-f205-f7fb5c400cc3"
+++

[Part 5](/deep-dives/ctranslate2-metal-backend/the-730-second-file/) ended on an uncomfortable fact: for Whisper, the GPU backend
loses to the CPU. This part is about _why_ that's true for some workloads and gloriously false
for others - and about the three times I was confidently, measurably wrong about which was which.
The through-line, if you want it on a sticky note: **profile, don't guess.** Every single time I
guessed, I was wrong, and the profiler was right.

{{< nyer-panel src="two-schools.jpg" caption="Two schools of performance engineering." alt="An antique woodcut engraving: a blindfolded man aims a dart while, beside him, a second man calmly measures the dartboard with calipers." >}}

## Where the GPU wins: big matmuls

Start with raw matrix-multiply throughput, because it sets up everything else. Square matmul,
GPU 16-bit float versus the Apple CPU's tuned math library:

| size | CPU    | Metal 16-bit   | Metal vs CPU |
| ---- | ------ | -------------- | ------------ |
| 256  | (fast) | slow           | 0.11×        |
| 512  | (fast) | warming up     | 0.37×        |
| 2048 | strong | **~12 TFLOPS** | **3.70×**    |

The shape of that table is the whole story of GPU acceleration. At small sizes the CPU wins
easily, because each GPU call pays a fixed overhead - commit a command buffer, set up the matmul
object, wait - and a small multiply is too little work to amortize it. At **size 2048** the GPU
is 3.7× faster and it's a stable, repeatable result. The math hardware is genuinely strong; you
just have to give it enough to chew.

> **A measurement honesty note.** The size-1024 row - right at the crossover - swung between
> 0.85× and 2.26× across four back-to-back runs on the same machine. A 2.7× spread on identical
> inputs. It straddles the point where dispatch overhead stops dominating but the GPU isn't
> saturated yet, so one unlucky iteration skews the average. I report 2048 as the first
> _dependable_ win and treat 1024 as a coin flip - because quoting the lucky draw would be
> exactly the guessing this part is against.

## Wrong guess #1: the 16-bit op that was never on the GPU

Here's the one I'm fondest of, because the intuition was so clean and so wrong.

On a real LLM (Qwen2.5-0.5B), 16-bit prefill came out _slower_ than 32-bit. That looks
diagnostic: 16-bit is supposed to be the fast path on Apple hardware, so if it's slower, MPS's
16-bit matmul must be weak, right? Reasonable. Wrong.

The profiler said the matmuls were _identical_ in both precisions. The entire regression was a
single elementwise **`Add`** - the [residual connection](/glossary/residual-connections/) - and in 16-bit it had exploded **27×**.
The cause had nothing to do with precision math: the `Add` op had **never been wired to its GPU
kernel.** It was quietly running on the CPU reference the whole time - fine in 32-bit (fast
vectorized CPU math), catastrophic in 16-bit (slow software-emulated half-precision), and forcing
a pipeline stall on every single residual, dozens of times per forward pass.

Routing `Add` to a real GPU kernel - a kernel that already _existed_, from the very first
milestone, and had simply never been connected - dropped 16-bit batched prefill from 1815ms to
559ms. A 3.2× jump that made the GPU 2.6× faster than the CPU and 4× faster than its own 32-bit
path. _This_ is where Apple Silicon gets fast. And I'd never have found it by reasoning about
MPS, because MPS was never the problem. The problem was an op that looked GPU-resident on the
architecture diagram and wasn't in the actual code.

## Wrong guess #2: the optimization everyone reaches for first

Every op currently commits its own batch of GPU work. The textbook optimization is obvious:
stop doing that, batch many ops into one submission per decode step, pay the per-commit overhead
once instead of dozens of times. It's the first thing anyone suggests, so I had it built - fully,
every cross-thread-ordering corner handled, and it passed every parity test.

Measured: **neutral on the workload it was supposed to help, and a 23% _regression_ on the
matmul-heavy ones.** So I reverted it.

The reason is the kind of thing you only learn by measuring. Committing each op separately isn't
waste - it's what lets the GPU run op N _while the CPU is busy encoding op N+1._ That overlap is
free parallelism. Batching everything into one big commit per step destroys it: the GPU sits idle
until the whole batch is submitted, and for matmul-heavy work the lost overlap costs more than the
saved commit overhead ever saved. The "obvious" win was a real loss. Per-op commit was already
near-optimal, and the commit count was never the bottleneck I assumed it was.

## What actually helps: fewer, bigger ops

The lever that _did_ work isn't doing the same work with less overhead - it's doing less work.
**Op fusion:** instead of a separate residual-add and then a normalization, one fused kernel that
reads the inputs once, writes the residual sum, and writes the normalized result in a single pass.
One fewer kernel launch, one fewer trip through memory. Measured a real, repeatable ~1.25-1.3× at
the mid-size shapes that match actual LLM hidden [dimensions](/glossary/dimensions/) - and crucially it helps _without_
killing the CPU/GPU overlap, because it reduces op count rather than batching commits. Fewer,
bigger ops is the right direction; fewer commits was a mirage.

## The shape of it: prefill wins, decode loses

Putting it together explains [Part 5](/deep-dives/ctranslate2-metal-backend/the-730-second-file/)'s Whisper result precisely. There are
two regimes:

- **Prefill** - processing a whole prompt at once - is big matmuls, the favorable end of that
  first table. The GPU wins, and in 16-bit it wins big.
- **Decode** - generating one token at a time - is a long stream of tall-skinny
  matrix-_vector_ products, each tiny, each paying the GPU-dispatch toll. The CPU wins, because
  it has no dispatch toll to pay. Having 500 million [parameters](/glossary/parameters/) doesn't
  save you; each _step_ still issues many small ops.

Whisper is decode-bound, so Whisper loses. A throughput-bound batch-translation workload is
prefill-heavy, so it wins. Same backend, opposite verdicts, and the only way to know which you're
looking at is to measure it - not to reason from the parameter count or the precision or the
TFLOPS the hardware can theoretically hit.

Three wrong guesses, three corrections, one moral: the intuitive culprit is a hypothesis, not a
finding. The profiler is the finding. (And the difference between making a model smaller by
dropping precision versus by quantizing it - which I leaned on throughout - is the
[precision](/glossary/precision/) entry, since it's the single most common thing people get
backwards about all of this.)

That's the technical arc. There's one question left, and it's not a technical one: a working GPU
backend exists - so why is it living in a fork and a blog post instead of the upstream project?
[Part 7](/deep-dives/ctranslate2-metal-backend/not-a-pull-request/).
