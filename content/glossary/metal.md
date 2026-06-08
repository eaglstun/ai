+++
title = "Metal"
summary = "Apple's GPU-compute API; powers MLX and Metal-backed ML."
category = "GPU compute & backends"
related = ["cuda", "vulkan", "mlx", "mps", "ggml"]
+++
**Metal** is Apple's low-level interface for graphics and GPU computing — its answer to
[CUDA](/glossary/cuda/) and [Vulkan](/glossary/vulkan/), but exclusive to Apple hardware (Mac, iPhone, iPad). For ML it matters
because Apple-silicon chips share one pool of memory between CPU and GPU (unified memory), so
Metal lets models use the GPU without copying their weights across the slow link that
separates the CPU and GPU on a typical PC. The compute side is exposed through **[MPS](/glossary/mps/)**
(Metal Performance Shaders) and the higher-level MPS Graph; PyTorch's `mps` device and [MLX](/glossary/mlx/)
both sit on top of it. In local inference, [GGML](/glossary/ggml/) ships a Metal backend, which is how
llama.cpp and Ollama speed up `.gguf` models on a Mac instead of falling back to the CPU.
