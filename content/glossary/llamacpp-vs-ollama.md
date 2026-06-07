+++
title = "llama.cpp vs Ollama"
summary = "The local-inference engine vs the wrapper built on it."
category = "Local inference & formats"
related = ["gguf", "ggml", "metal", "cuda", "vulkan"]
+++
First, the naming: "llama" here means **llama.cpp** (the inference engine), not Meta's
**Llama** model family. Ollama's name is a play on it, which is fitting because **Ollama is
built on top of llama.cpp** — they're not really competitors so much as different layers of
the same stack.

**llama.cpp** is the low-level C/C++ inference engine (powered by [GGML](/glossary/ggml/)) that actually
runs [GGUF](/glossary/gguf/) models. It's a library plus CLI tools (`llama-cli`, `llama-server`) and ships
the GPU backends — [CUDA](/glossary/cuda/), [Metal](/glossary/metal/), [Vulkan](/glossary/vulkan/) — for offloading layers. It's maximally
flexible and fast, but you manage everything yourself: find the right `.gguf`, pick the
quantization, set context length and GPU-offload flags, wire up the chat template.

**Ollama** wraps that engine in developer ergonomics. It adds a model registry
(`ollama pull llama3`), automatic download and caching, sensible default parameters and
templates baked into a `Modelfile`, and a persistent background server exposing a REST API
(and an OpenAI-compatible endpoint). You trade some low-level control for not having to
think about any of the plumbing.

Rule of thumb: reach for **Ollama** when you want a model running in one command and a clean
local API; drop down to **llama.cpp** when you need bleeding-edge features, custom build
flags, or to squeeze out maximum performance. (LM Studio is a third option — a GUI app over
the same llama.cpp core.)
