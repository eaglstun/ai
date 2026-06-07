+++
title = "CUDA"
summary = "NVIDIA's GPU-compute platform; the default ML backend."
category = "GPU compute & backends"
related = ["metal", "vulkan", "ggml", "cudnn-cublas"]
+++
**CUDA** (Compute Unified Device Architecture) is NVIDIA's proprietary parallel-computing
platform and API for running general-purpose work on NVIDIA GPUs. It's the dominant
backend for ML: you write kernels (or, far more often, use libraries like cuDNN and cuBLAS
(see [cuDNN / cuBLAS](/glossary/cudnn-cublas/)) and the CUDA-backed builds of PyTorch/TensorFlow) that fan computation out across the
GPU's thousands of cores. Its lock on the field comes less from the hardware than from
the software moat — the mature library ecosystem and tooling that everyone targets first.
The catch is it's NVIDIA-only: it won't run on Apple, AMD, or Intel GPUs, which is exactly
the gap that [Metal](/glossary/metal/) and [Vulkan](/glossary/vulkan/) fill on other hardware. In the local-inference
world, [GGML](/glossary/ggml/) ships a CUDA backend so `.gguf` models can offload layers to an NVIDIA
GPU instead of grinding on the CPU.
