+++
title = "I Put a Language Model That Thinks It's 1930 on My Laptop"
date = 2026-05-27
draft = true
summary = "talkie is a 13B model trained only on pre-1931 text — and it ships expecting a 28 GB CUDA GPU. Here's the pipeline for converting it to GGUF and running it locally in Ollama."
+++

[talkie](https://github.com/eaglstun/talkie) is a 13B "vintage" language model trained
entirely on pre-1931 English text — etiquette manuals, letters, encyclopedias, poetry. It's
a wonderful curiosity, but the official repo wants a 28 GB CUDA GPU and bfloat16. This is the
repeatable recipe I use to get a HuggingFace model like this one down onto local
[Ollama](/glossary/llamacpp-vs-ollama/) instead.

<!--more-->

## Why bother converting

- The repo's stock path: `uv sync`, a big NVIDIA card, ~26–50 GB per model.
- What [quantization](/glossary/parameters/) buys: a 13B model in
  [GGUF](/glossary/gguf/) at 4-bit fits in well under 10 GB and runs on a Mac.

## The pipeline (works for most HF models)

1. **Download the weights** from HuggingFace (`talkie-lm/talkie-1930-13b-it`).
2. **Convert to GGUF** with llama.cpp's `convert_hf_to_gguf.py`.
3. **Quantize** to a sane level (`Q4_K_M` is the usual default).
4. **Write a `Modelfile`** — point at the `.gguf`, set the chat template and stop tokens,
   bake in default parameters.
5. **`ollama create talkie -f Modelfile`** and `ollama run talkie`.

## talkie-specific gotchas

- The chat template / instruction format for the `-it` model.
- Whether the architecture is one llama.cpp's converter already supports.
- Keeping the 1930 voice intact — sampling settings that don't drag it toward modern phrasing.

## Is it worth it

- Quality at 4-bit vs. the full bfloat16 model.
- The fun part: comparing `talkie-1930` against `talkie-web` (same architecture, modern data).
