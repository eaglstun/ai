+++
title = "Transformer"
summary = "The self-attention architecture behind modern LLMs."
category = "Architectures"
related = ["attention", "gpt", "tensor", "lora"]
+++
**Transformer** is the neural-network architecture that underpins virtually all modern
large language models (and much else). Introduced in the 2017 paper _"Attention Is All You
Need,"_ its key innovation is **self-[attention](/glossary/attention/)**: for each token in a sequence, the model
weighs how much every other token should influence it, letting it capture long-range
relationships directly instead of marching through the sequence step by step like an RNN.
Because those attention computations happen in parallel across the whole sequence, the
architecture trains efficiently on GPUs and scales to enormous models and datasets — the
practical reason it won. Transformers come in three flavors: **encoder-only** (e.g. BERT,
good for understanding/classification), **decoder-only** (e.g. the [GPT](/glossary/gpt/) family, good for
text generation), and **encoder-decoder** (e.g. T5, good for translation and other
seq-to-seq tasks). Everything happens via [tensor](/glossary/tensor/) operations stacked into repeated
attention + feed-forward layers.
