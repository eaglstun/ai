+++
title = "cuDNN / cuBLAS"
summary = "NVIDIA's CUDA math & deep-learning libraries."
category = "GPU compute & backends"
related = ["cuda", "mps", "tensor"]
+++
**cuBLAS** and **cuDNN** are NVIDIA's optimized math libraries that sit on top of [CUDA](/glossary/cuda/)
and do the heavy lifting most ML frameworks rely on. **cuBLAS** is NVIDIA's GPU
implementation of BLAS (Basic Linear Algebra Subprograms) — the matrix-multiply and
vector routines that dominate neural-net compute. **cuDNN** (CUDA Deep Neural Network
library) is the higher-level set of primitives tuned specifically for deep learning:
convolutions, pooling, normalization, attention, activation functions, and so on. Frameworks
like PyTorch and TensorFlow don't write raw CUDA kernels for these — they call cuBLAS and
cuDNN, which is a big part of why NVIDIA hardware is so fast and so entrenched for training
and inference. They're the NVIDIA equivalent of Apple's [MPS](/glossary/mps/) (and conceptually what a
[Vulkan](/glossary/vulkan/) or [Metal](/glossary/metal/) backend has to reimplement to compete). Note both are proprietary,
closed-source NVIDIA libraries, though free to use; cuDNN in particular requires a separate
download/registration from the base CUDA toolkit.
