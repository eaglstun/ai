+++
title = "GGML"
summary = "C/C++ tensor library powering llama.cpp; runs GGUF."
category = "Local inference & formats"
related = ["gguf", "tensor", "cuda", "metal", "vulkan", "rss-sampler", "quantization"]
plain = "The engine block. The low-level code that actually loads a model's numbers into memory and grinds through the math, so a GGUF file has something to run inside on your own machine."
tags = ["ggml", "gguf", "quantization", "inference", "tensor"]
semantic_id = "YmOG1DpvmQ4Fv-Gf53WDHKfhyaAzgAAH"
+++
**GGML** is a C/C++ library, written by Georgi Gerganov, for _running_ machine-learning models
(as opposed to training them), with a deliberate focus on getting good performance out of
ordinary CPUs and consumer hardware, though it also supports GPU backends like [CUDA](/glossary/cuda/),
[Metal](/glossary/metal/), and [Vulkan](/glossary/vulkan/). It's the engine under
[llama.cpp](https://github.com/ggml-org/llama.cpp) and
[whisper.cpp](https://github.com/ggml-org/whisper.cpp): it defines the math operations, the
order they run in, and (crucially) the **quantization** schemes that shrink the model's
numbers to fewer bits so large models fit in limited memory. One confusing wrinkle: "GGML"
was also the name of an early single-file model format from the same project. That _format_
was retired and replaced by [GGUF](/glossary/gguf/), but the _library_ lives on and is what actually crunches
the numbers when you run a `.gguf` model. So today: GGML = the engine, GGUF = the file it
loads.
