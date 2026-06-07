+++
title = "Attention"
summary = "How tokens weigh each other (query · key · value) — the heart of the transformer."
category = "Architectures"
related = ["transformer", "tensor", "lora"]
+++
**Attention** is the mechanism at the heart of the [transformer](/glossary/transformer/): it lets a model decide,
for each token, how much every other token should influence it — so meaning can flow
directly between distant words instead of being passed along step by step. Each token is
projected into three vectors: a **query**, a **key**, and a **value**. A token's query is
compared (dot product) against every token's key to produce relevance scores; those scores
are scaled, passed through a softmax to become weights that sum to 1, and used to take a
weighted average of the value vectors. That's **scaled dot-product attention**, often
written `softmax(QKᵀ / √dₖ)·V`. In practice models run several of these in parallel —
**multi-head attention** — so different heads can specialize in different kinds of
relationships (syntax, coreference, position). When the queries, keys, and values all come
from the same sequence it's **self-attention** (a token attending to its own context); when
queries come from one sequence and keys/values from another it's **cross-attention** (e.g.
a decoder attending to an encoder's output). The catch is cost: comparing every token to
every other is O(n²) in sequence length, which is why long context windows are expensive
and why so much research targets cheaper attention variants. The Q/K/V projections are just
[tensor](/glossary/tensor/) matrix multiplies — and they're exactly the weights [LoRA](/glossary/lora/) usually adapts when
fine-tuning.
