+++
title = "Vulkan"
summary = "Cross-vendor GPU-compute API; the portable ML fallback."
category = "GPU compute & backends"
related = ["cuda", "metal", "ggml"]
+++
**Vulkan** is a low-level, cross-platform graphics and GPU-compute API from the
[Khronos Group](https://www.vulkan.org/) — the open, vendor-neutral counterpart to
[CUDA](/glossary/cuda/) and [Metal](/glossary/metal/). It's an open, royalty-free _standard_ rather than a single piece
of "open-source software": the specification and reference tooling (headers, validation
layers, conformance tests) are openly published, and driver implementations range from
fully open source (AMD/Intel via Mesa's RADV and ANV) to proprietary (NVIDIA's). Its draw for ML is
exactly that neutrality: a single Vulkan compute backend runs on NVIDIA, AMD, Intel, and
many mobile/embedded GPUs, so it's the portable fallback when you can't assume an NVIDIA
card (and thus CUDA) is present. The trade-off is that it's lower-level and verbose, and its
ML-library ecosystem is far thinner than CUDA's, so it usually delivers less peak throughput
on NVIDIA hardware than CUDA does. In local inference, [GGML](/glossary/ggml/) ships a Vulkan backend,
which is what lets llama.cpp accelerate `.gguf` models on AMD and Intel GPUs that CUDA and
Metal can't touch.
