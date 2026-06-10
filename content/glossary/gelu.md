+++
title = "GELU"
summary = "The smooth activation gate used inside GPT- and BERT-style transformers."
category = "Building blocks"
related = ["transformer", "gpt", "tensor", "relu"]
plain = "The bouncer with manners. It's the little gate between layers that decides how much of each signal to let through - instead of a hard yes/no it eases borderline cases in gently, which is why modern models prefer it."
+++
**GELU** (Gaussian Error Linear Unit) is the little nonlinear gate that sits between the
layers of most modern [transformer](/glossary/transformer/) models, deciding how much of each signal to pass
forward. You need a gate like this because without one, stacking layers is pointless,
a pile of plain linear steps just collapses back into a single linear step, so no matter
how deep the network got, it could only ever draw straight lines. The gate is what lets it
bend.

The old standby gate was ReLU, a hard bouncer: anything negative gets slammed to exactly
zero, anything positive walks through untouched. GELU is the same idea with better manners.
Instead of a hard cutoff it uses the bell curve (the _Gaussian_ in the name) to weight each
input by how likely it is to matter, so small negative values aren't thrown out, they're
quietly turned down. That smoothness gives the model gentler slopes to learn from during
training, which tends to train more stably. It runs element-wise across a [tensor](/glossary/tensor/), and
it's the default activation inside [GPT](/glossary/gpt/)-style models and BERT.
