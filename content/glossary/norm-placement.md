+++
title = "Norm placement"
summary = "Where LayerNorm sits in a transformer block - pre, post, or sandwiched - and why it decides whether a deep model trains at all."
category = "Building blocks"
related = ["residual-connections", "transformer", "gradient-descent", "tensor"]
plain = "Where you put the leveler in a chain of guitar pedals. It's the box that keeps the signal from clipping or fading as it runs through a long effects chain - and whether you put it before each pedal, after, or both changes how clean the whole chain stays. Modern models put it before (pre-norm); the original put it after (post-norm); the cautious ones do both (sandwich)."
tags = ["norm-placement", "transformer", "residual-connections", "gradient-descent", "training"]
semantic_id = "ExCnaByAGEVZld_nDXhN5bGipCuCgAAF"
+++
**Norm placement** is the question of _where_ you put the normalization step inside a
[transformer](/glossary/transformer/) block, and it sounds like a plumbing detail until you realize it's the
difference between a model that trains and one that quietly falls apart. Normalization
(usually **LayerNorm**) is the leveling stage that re-centers and re-scales the numbers
flowing through the network so they don't blow up to infinity or shrink to nothing as they
pass through layer after layer. Every block has two moving parts wrapped in
[residual connections](/glossary/residual-connections/): the attention sublayer and the feed-forward sublayer, and norm
placement is just: do you level the signal _before_ each part, _after_ it, or _both_?

Picture a long chain of guitar pedals with a leveling box that keeps the signal from
clipping or fading. **Post-norm** (the original 2017 setup) puts the leveler _after_ the
pedal, right on the main signal path, downstream of the residual add. It works, but the
unnormalized residual highway lets the signal swell as the chain gets long, so deep
post-norm models are touchy: they need careful learning-rate warmup or they diverge.

**Pre-norm** (the modern default from [GPT](/glossary/gpt/)-2 onward) moves the leveler _inside_ the
pedal's own branch, so the residual highway stays clean and untouched all the way through.
That clean highway is exactly what lets you stack dozens of layers and still train stably,
because the [gradient descent](/glossary/gradient-descent/) signal flows straight back through it without fading. The tradeoff: pre-norm can
get a little lazy in its deepest layers.

**Sandwich-norm** is the belt-and-suspenders move:
a leveler both before _and_ after each branch, used in some very large or very deep models
(CogView, a few big ones since) to keep the numbers tame when even pre-norm starts to wobble.
Mechanically all three are the same cheap [tensor](/glossary/tensor/) operation; only the wiring around the
residual add changes, and that wiring decides whether the thing learns.
