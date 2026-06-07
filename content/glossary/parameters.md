+++
title = "Parameters"
summary = "Learned weights; the count is model size & memory cost."
category = "Core concepts"
related = ["tensor", "transformer", "gguf", "lora", "val-loss"]
+++
**Parameters** are the learned numbers inside a model — the weights (and biases) that
training adjusts and that collectively store everything the model "knows." A label like
**7B** means roughly 7 billion of them; common sizes run 1B, 3B, 7B, 8B, 13B, 70B, on up to
the hundreds of billions for frontier models. The count is the standard shorthand for a
model's capacity and cost: more parameters generally means more capability but also more
compute to train and more memory to run. Those parameters are stored as [tensor](/glossary/tensor/) weight
matrices, the bulk of them in a [transformer](/glossary/transformer/)'s attention and feed-forward layers.

The number that matters in practice is **parameters × bytes-per-parameter = memory**. At
full 16-bit precision a parameter takes 2 bytes, so a 7B model needs ~14 GB just for
weights; quantizing to 4-bit (see [GGUF](/glossary/gguf/)) cuts that to ~3.5 GB, which is exactly how big
models squeeze onto consumer hardware. Two related distinctions worth keeping straight:
_parameters_ (the model's fixed learned weights) are not _tokens_ (the units of input/output
text it processes), and they're not _hyperparameters_ (settings like learning rate or batch
size that you choose before training). Note also that [LoRA](/glossary/lora/) fine-tunes a model by
training a tiny number of _extra_ parameters while leaving the billions of base ones frozen.
