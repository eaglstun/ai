+++
title = "Parameters"
summary = "Learned weights; the count is model size & memory cost."
category = "Core concepts"
related = ["tensor", "transformer", "gguf", "lora", "val-loss", "gradient-descent", "rss-sampler", "precision"]
plain = "The knobs and dials. Picture a mixing board with billions of tiny dials; training is the computer nudging each one a hair every time it's right or wrong. More dials means more room for fine detail - and a bigger, heavier model."
+++
**Parameters** are the learned numbers inside a model: the weights (and biases) that training
adjusts, and that together store everything the model "knows." A label like **7B** means
roughly 7 billion of them; common sizes run 1B, 3B, 7B, 8B, 13B, 70B, on up to the hundreds of
billions for the biggest models. The count is the usual shorthand for how capable, and how
expensive, a model is: more parameters generally means more ability, but also more compute to
train and more memory to run. Those numbers are stored as [tensor](/glossary/tensor/) weight grids, most of them
in a [transformer](/glossary/transformer/)'s attention and feed-forward layers.

The figure that matters in practice is **parameters × bytes-per-parameter = memory**. At full
precision each parameter takes 2 bytes, so a 7B model needs about 14 GB just for its weights;
squeezing each one down to 4 bits (see [GGUF](/glossary/gguf/)) cuts that to roughly 3.5 GB, exactly how big
models fit onto consumer hardware. Two distinctions worth keeping straight: _parameters_ (the
model's fixed learned weights) are not _tokens_ (the chunks of text it reads and writes), and
they're not _hyperparameters_ (settings like learning rate or batch size that you pick before
training). And note [LoRA](/glossary/lora/) fine-tunes a model by training a tiny batch of _extra_ parameters
while leaving the billions of original ones frozen.
