+++
title = "LoRA"
summary = "Low-rank adapters; parameter-efficient fine-tuning."
category = "Core concepts"
related = ["transformer", "tensor", "gguf", "parameters", "qwen", "quantization"]
plain = "Sticky notes instead of rewriting the book. Rather than retrain a giant model from scratch to teach it something new, you clip on a small set of adjustments - cheap to make, easy to swap in and out, and you can keep a whole drawer of them."
tags = ["fine-tuning", "lora", "transformer", "quantization"]
semantic_id = "gttJKL84XeBrUl6Op2-qcwm6yxIWYAAK"
+++
**LoRA** (Low-Rank Adaptation) is a cheap way to fine-tune a large model. Normally fine-tuning
updates all of a model's weights, billions of numbers, costly in compute and memory. LoRA
instead freezes the original weights and trains a small add-on alongside them. The trick: the
_change_ a fine-tune makes to a big grid of weights turns out to be simple enough to capture
with two much smaller grids multiplied together (`A · B`), which together hold a tiny fraction
of the original numbers (their size is set by a chosen _rank_ `r`, often 8–64). At run time
that product is added back onto the frozen weights, so once merged there's no speed penalty.

The payoff is twofold: you can fine-tune a large model on a single consumer GPU, and the
resulting **LoRA adapter** is a small file (megabytes, not gigabytes) that you swap in and out
on top of one base model.

**QLoRA** goes further by also shrinking the frozen base model to
4-bit (the same quantization idea behind [GGUF](/glossary/gguf/)) while training the adapter at higher
precision, saving even more memory. LoRA is most often applied to the attention weights of a
[transformer](/glossary/transformer/).
