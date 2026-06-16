+++
title = "Epsilon gate"
summary = "A convergence threshold (eps) used as a hard pass/fail gate - and the silent failure it causes when the same code runs on different hardware."
category = "Core concepts"
related = ["gradient-descent", "precision", "mps", "val-loss"]
plain = "The high-jump bar that forgot to move. Set the bar at an exact height: clear it and you're in, graze it and you're out, even if you jumped higher than anyone in the room. Now hold the contest on a slightly springier floor, and a great jumper keeps nicking the bar by a hair - so the system records zero winners instead of just nudging the bar down a touch. An epsilon gate is that rigid bar: a tiny 'good enough' cutoff that quietly throws out near-perfect answers the moment the conditions shift."
+++
An **epsilon gate** is a pass/fail check built around a number that's supposed to be _almost_
zero. Many iterative algorithms stop when some error measure drops below a tiny threshold called
**epsilon** (often written `eps`, a value like `0.002`): close enough, declare success, hand back
the answer. The trouble starts when the code treats that threshold as a hard gate, returning a
result _only_ if the error makes it under epsilon. Anything that lands a hair short gets thrown
away, even when it's a perfectly good answer.

That's fine until the arithmetic shifts underneath it. The same computation run on a different
backend, [CUDA](/glossary/cuda/) versus [MPS](/glossary/mps/) versus the CPU, will not produce bit-identical numbers, because
[floating-point precision](/glossary/precision/) and the order of operations differ from one machine to the next. A search that used
[gradient descent](/glossary/gradient-descent/) to reach `0.0019` on the GPU it was tuned for might settle at `0.0021`
somewhere else: the same quality of answer, missing the gate by a rounding error. If epsilon was
hardcoded for one machine, the program can silently produce _nothing_ on another. No crash, no
warning, just an empty output folder and a confusing afternoon.

The fix is to stop treating epsilon as a _publication gate_ and treat it as a _stopping hint_:
keep going until the error is under the threshold _or_ you run out of steps, then always return
the best result the run actually found. Epsilon decides when to _stop looking_, not whether the
answer is allowed to exist. A hardcoded convergence threshold is a close cousin of any magic
number tuned on one setup, the kind of buried assumption that turns into a silent failure the
moment the ground moves: a new GPU, a different [floating-point precision](/glossary/precision/), a fresh library version.
