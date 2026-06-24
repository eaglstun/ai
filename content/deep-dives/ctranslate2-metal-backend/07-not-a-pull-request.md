+++
title = "Part 7 - The Thing This Didn't Become: A Pull Request"
slug = "not-a-pull-request"
weight = 7
draft = true
date = 2026-07-23
series = "ctranslate2-metal-backend"
summary = "There's a working Apple-Silicon GPU backend at the end of this, built by someone who has never written a line of C++. It is not going upstream as one big pull request, and the honest reason is the most interesting lesson in the project - about what 'understand it and defend every line' means when the line-level understanding genuinely isn't yours, and why a fork is the right home, not a consolation prize."
+++

I'll close on the part that makes this a series of blog posts instead of a contribution, because
it's the most interesting _non_-technical thing I learned, and because it's the same idea this
whole site is built on.

There is, at the end of all this, a working GPU backend. Full transformer, two precisions,
correct against the CPU, memory-safe, with a real performance story. The obvious next move is a
pull request to CTranslate2. I'm not making one. Here's the honest why.

## The maintainers' policy, and why it's correct

CTranslate2's contributing guidelines have an explicit, reasonable rule about AI-assisted code:
disclose it, fully understand it, be ready to defend every line. And "assisted" is generous for
what this is - the agent didn't _assist_ me, it wrote the entire thing; I never typed a line, as
[stated up front on the hub](/deep-dives/ctranslate2-metal-backend/). However you label it, the
policy aims squarely at work like this. And the policy is right.

This is a performance-critical, low-level C++ engine. Its own maintainers warn that a single
misplaced pointer can cost hours of debugging - and having spent [an entire afternoon on two
allocator early-returns](/deep-dives/ctranslate2-metal-backend/the-staircase/) and [three sessions on a `tanh`](/deep-dives/ctranslate2-metal-backend/the-nan-hunt/), I can
confirm the warning is not decorative. In a codebase like that, **reviewing a large change for
correctness is more work than writing it was.** A whole GPU backend dropped as one pull request
is more surface area than any maintainer can responsibly vet on faith - no matter who, or what,
wrote it. Declining it isn't gatekeeping. It's the only sane response to a 50-file diff in a
place where pointers bite.

## The policy asks for something I genuinely can't give

Here's where I have to be straight, because the policy is precise about it. It doesn't merely ask
a contributor to _disclose_ the AI assistance. It asks them to _fully understand_ the change and
be ready to _defend every line._ And I can't. As I said on [the hub](/deep-dives/ctranslate2-metal-backend/):
I have never written C++. I can't read this engine's source, and I certainly can't stand behind a
specific line of a Metal kernel and tell you why it is _correct_ - as opposed to merely producing
the right numbers on every input I've tried so far.

What I _can_ do is explain the shape. The unified-memory cheat code, why Metal rides the CPU
dispatch case, the two load-bearing allocator exceptions, why a `tanh` overflowed at layer 23, why
decode loses to prefill - I understand all of that well enough to have just written six posts
about it. But "I can explain the architecture" and "I can defend the implementation" are different
sentences, and the maintainers are asking for the second one. They are right to. Architectural
understanding is what let me _judge_ this backend - point it at Gemma2, see the `<pad>` collapse,
know that's wrong, drive the bisection. It is emphatically not what lets anyone _vouch_ for a line
of it. A reviewer needs someone who can vouch, in this language, in this codebase - and honestly,
that person isn't me.

So the gap the policy protects isn't the flattering version, "I'm confident and you just can't
afford my confidence." It's plainer and more honest than that: the policy wants line-by-line
ownership, and what I have is behavioral judgment. Those are two different goods. Pretending they
were the same - shipping a fifty-file diff under my name with a shrug where the line-level
understanding is supposed to be - is the exact thing the rule exists to stop. Declining that PR
wouldn't be gatekeeping. It would be the system working as designed.

## So it lives in a fork - which is the correct home anyway

So the work lives out-of-tree: a public fork, and these seven posts. The more I sit with that,
the less it reads as a runner-up prize. A _separate GPU backend_ - a self-contained third leg
that doesn't touch the existing two - is arguably most correctly a fork in the first place. The
maintainers keep their codebase and its review burden bounded. Anyone on Apple Silicon who wants
the backend builds from the fork. And I keep the working engine, the understanding, and the part
that outlasts any merged commit: the explanation you're reading.

(The cheap, high-welcome move still on the table - and the one I'd actually start with - isn't the
backend at all. It's offering the _docs_: the design writeup, the build recipe, the benchmark
findings. Contributing-guidelines everywhere explicitly invite that, it builds the trust a future
backend conversation would need, and it costs a reviewer almost nothing to accept. Land the small
defensible thing first.)

## The loop closes where it opened

[Part 1](/deep-dives/ctranslate2-metal-backend/unified-memory/) opened on a cheat code: Apple Silicon's unified memory hands you a
correct-but-slow engine _for free_, because the hardware erases the boundary between CPU memory
and GPU memory. Almost everything good in this project flows from that one gift - the dispatch
trick, the bisection method that caught the NaN, the upcast-over-unified-memory fix that unblocked
Whisper. The hardware kept handing me things for free.

The one thing it couldn't hand me for free is the thing this last part is about: **somebody else's
confidence.** Unified memory erases the boundary between two kinds of RAM. It does nothing about
the boundary between "I can explain this" and "you can afford to trust that I vouch for it" - and
that boundary doesn't have a cheat code, least of all for someone who can't read the language it's
written in. You close it the slow way, in public, one explained decision at a time. Which is what
this whole site is, and what these seven parts were: not a pull request, but the work made legible
enough that the judgment behind it could be evaluated instead of taken on faith.

That's a fair trade, and here's the honest shape of it. The hardware gave me the engine for free.
The agent wrote every line of it. And this - the explanation, the only artifact in the whole
project with my actual fingerprints on it - is the part that was mine to make. I can't write the
kernel. I can tell you exactly why it's there, what it cost to find, and whether it works. On this
site, that's the job.

---

_The backend is an ongoing fork; the milestones, benchmarks, and war stories here are accurate as
of mid-2026 and will drift as the work continues. If you're doing something similar on Apple
Silicon and want to compare notes, that's exactly the kind of thing this site exists for._
