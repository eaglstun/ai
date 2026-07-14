+++
title = "Transformer"
summary = "The self-attention architecture behind modern LLMs."
category = "Architectures"
related = ["attention", "gpt", "tensor", "lora", "gelu", "relu", "residual-connections", "norm-placement", "qwen", "temperature", "token"]
plain = "The architecture behind nearly every modern AI. Its trick is reading everything at once and letting each piece decide which other pieces matter - that's what powers ChatGPT, image generators, and the rest."
tags = ["attention", "datasets", "gpt", "machine-learning", "model-welfare", "parameters"]
semantic_id = "0b5ac35e-19c9-ee40-5362-9730a1c0000a"
+++
**Transformer** is the neural-network design behind virtually all modern large language models
(and much more). Introduced in the 2017 paper _"Attention Is All You Need,"_ its key idea is
**self-[attention](/glossary/attention/)**: for each word in a sequence, the model weighs how much every other word
should influence it, so it can connect distant words directly instead of marching through them
one at a time like older "recurrent" networks did. Because those weighings happen in parallel
across the whole sequence, transformers train efficiently on GPUs and scale up to enormous
models and datasets, the practical reason they won out. They come in three flavors:
**encoder-only** (e.g. BERT, good at understanding and classifying text), **decoder-only**
(e.g. the [GPT](/glossary/gpt/) family, good at generating text), and **encoder-decoder** (e.g. T5, good at
tasks like translation that turn one sequence into another). It all runs on [tensor](/glossary/tensor/)
operations stacked into repeated attention and feed-forward layers.
