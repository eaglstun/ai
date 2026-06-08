+++
title = "CUDA"
summary = "NVIDIA's GPU-compute platform; the default ML backend."
category = "GPU compute & backends"
related = ["metal", "vulkan", "ggml", "cudnn-cublas"]
+++
**CUDA** (Compute Unified Device Architecture) is NVIDIA's software platform for running
general-purpose number-crunching — not just graphics — on NVIDIA GPUs. It's the default
engine for machine learning: rather than write low-level GPU code yourself, you almost always
lean on libraries like cuDNN and cuBLAS (see [cuDNN / cuBLAS](/glossary/cudnn-cublas/)) and the CUDA-powered builds of
PyTorch and TensorFlow, which spread the work across the GPU's thousands of cores. NVIDIA's
grip on the field comes less from the chips than from this software head start — the mature
ecosystem everyone targets first. The catch: CUDA is NVIDIA-only. It won't run on Apple, AMD,
or Intel GPUs, which is exactly the gap [Metal](/glossary/metal/) and [Vulkan](/glossary/vulkan/) fill on other hardware. In
the local-inference world, [GGML](/glossary/ggml/) ships a CUDA backend so `.gguf` models can hand work to an
NVIDIA GPU instead of grinding away on the CPU.
