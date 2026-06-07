+++
title = "LoRA"
summary = "Low-rank adapters; parameter-efficient fine-tuning."
category = "Core concepts"
related = ["transformer", "tensor", "gguf", "parameters"]
+++
**LoRA** (Low-Rank Adaptation) is a parameter-efficient fine-tuning method: instead of
updating all of a model's weights — billions of parameters, expensive in compute and
memory — you freeze the original weights and train a small pair of low-rank matrices that
are added alongside them. The trick rests on the observation that the _change_ a fine-tune
makes to a big weight matrix is approximately low-rank, so it can be factored as `A · B`
where A and B are skinny (a chosen rank `r`, often 8–64) and together hold a tiny fraction
of the original parameter count. At inference the product is added to (or merged back into)
the frozen weights, so there's no extra latency once merged. The payoffs: you can fine-tune
a large model on a single consumer GPU, and the resulting **LoRA adapter** is a small file
(megabytes, not gigabytes) that you swap in and out on top of one base model. **QLoRA** goes
further by quantizing the frozen base to 4-bit (see [GGUF](/glossary/gguf/) for the related quantization
idea) while training the adapter in higher precision, cutting memory more still. LoRA is
most commonly applied to the attention projection matrices of a [transformer](/glossary/transformer/).
