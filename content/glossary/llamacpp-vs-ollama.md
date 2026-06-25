+++
title = "llama.cpp vs Ollama"
summary = "The local-inference engine vs the wrapper built on it."
category = "Local inference & formats"
related = ["gguf", "ggml", "metal", "cuda", "vulkan", "temperature"]
plain = "Engine vs. dashboard. llama.cpp is the bare engine that runs the model; Ollama is the friendly dashboard bolted on top so you can start a model with one command instead of wiring up the engine yourself."
+++
First, the naming: "llama" here means **llama.cpp** (the software that runs models), not Meta's
**Llama** model family. Ollama's name is a play on it, which is fitting because **Ollama is
built on top of llama.cpp**, they're not really competitors so much as different layers of the
same stack.

**llama.cpp** is the low-level C/C++ engine (powered by [GGML](/glossary/ggml/)) that actually runs [GGUF](/glossary/gguf/)
models. It's a library plus command-line tools (`llama-cli`, `llama-server`) and ships the GPU
backends: [CUDA](/glossary/cuda/), [Metal](/glossary/metal/), [Vulkan](/glossary/vulkan/), for handing work to the GPU. It's maximally
flexible and fast, but you manage everything yourself: find the right `.gguf`, pick the
quantization (how much the model is shrunk), set the context length and GPU flags, wire up the
chat template.

**Ollama** wraps that engine to make it easy to use. It adds a model catalog
(`ollama pull llama3`), automatic download and caching, sensible defaults baked into a
`Modelfile`, and a background server that other apps can talk to over a simple web API
(including an OpenAI-compatible one). You give up some fine control in exchange for not having
to think about any of the plumbing.

Rule of thumb: reach for **Ollama** when you want a model running in one command with a clean
local API; drop down to **llama.cpp** when you need the newest features, custom build options,
or to squeeze out maximum performance. (LM Studio is a third option, a point-and-click app
over the same llama.cpp core.)
