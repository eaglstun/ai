+++
title = "GGUF"
summary = "llama.cpp's single-file format for quantized local LLMs."
category = "Local inference & formats"
related = ["mlx", "ggml", "parameters"]
+++
**GGUF** (GPT-Generated Unified Format) is a single-file format from the
[llama.cpp](https://github.com/ggml-org/llama.cpp) project for sharing and running quantized
large language models — models whose numbers have been shrunk to save space (see
[parameters](/glossary/parameters/)). It replaced the older [GGML](/glossary/ggml/) format. One `.gguf` file packs everything
needed to run the model — the weights, the tokenizer, and metadata like the architecture,
context length, and chat template — so there are no loose config files to juggle. It's built
to load fast and comes in a range of quantization levels (e.g. `Q4_K_M`, `Q5_K_M`, `Q8_0`)
that trade a little accuracy for smaller size and lower memory use, which is how big models
fit on everyday hardware. It's the native format for llama.cpp, Ollama, and LM Studio.
