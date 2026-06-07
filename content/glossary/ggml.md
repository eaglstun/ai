+++
title = "GGML"
summary = "C/C++ tensor library powering llama.cpp; runs GGUF."
category = "Local inference & formats"
related = ["gguf", "tensor", "cuda", "metal", "vulkan"]
+++
**GGML** is a C/C++ tensor library written by Georgi Gerganov for machine-learning
inference, with a deliberate bias toward running models efficiently on CPUs and consumer
hardware (though it also supports GPU backends like [CUDA](/glossary/cuda/), [Metal](/glossary/metal/), and [Vulkan](/glossary/vulkan/)). It's the
engine underneath [llama.cpp](https://github.com/ggml-org/llama.cpp) and
[whisper.cpp](https://github.com/ggml-org/whisper.cpp): it defines the tensor
operations, the computation graph, and crucially the integer **quantization** schemes
that let large models fit in limited RAM/VRAM. Confusingly, "GGML" was also the name of
an early single-file model format from the same project — that _format_ was deprecated
and replaced by [GGUF](/glossary/gguf/), but the _library_ lives on and is what actually executes the
math when you run a `.gguf` model. So today: GGML = the inference library, GGUF = the
file format it loads.
