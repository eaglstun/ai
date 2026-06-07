+++
title = "GGUF"
summary = "llama.cpp's single-file format for quantized local LLMs."
category = "Local inference & formats"
related = ["mlx", "ggml", "parameters"]
+++
**GGUF** (GPT-Generated Unified Format) is a single-file binary format from the
[llama.cpp](https://github.com/ggml-org/llama.cpp) project for distributing and running
quantized large language models. It superseded the older [GGML](/glossary/ggml/) format. One `.gguf` file
bundles everything needed to run the model — the weights, the tokenizer, and metadata
like the architecture, context length, and chat template — so there are no loose config
files to manage. It's designed for fast loading via memory-mapping and supports a range
of quantization levels (e.g. `Q4_K_M`, `Q5_K_M`, `Q8_0`) that trade accuracy for smaller
size and lower RAM/VRAM use, letting big models run on consumer hardware and CPUs. It's
the native format for llama.cpp, Ollama, and LM Studio.
