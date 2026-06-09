+++
title = "cuDNN / cuBLAS"
summary = "NVIDIA's CUDA math & deep-learning libraries."
category = "GPU compute & backends"
related = ["cuda", "mps", "tensor"]
plain = "NVIDIA's box of pre-tuned math shortcuts. The heavy number-crunching inside AI runs on these ready-made, hand-optimized routines, so nobody has to reinvent the fast way to multiply giant grids of numbers."
+++
**cuBLAS** and **cuDNN** are NVIDIA's optimized math libraries that sit on top of [CUDA](/glossary/cuda/) and
do the heavy lifting most ML frameworks depend on. **cuBLAS** is NVIDIA's GPU version of BLAS
(Basic Linear Algebra Subprograms) — the matrix-multiply and vector routines that make up the
bulk of neural-network math. **cuDNN** (CUDA Deep Neural Network library) is a higher-level
toolkit tuned specifically for deep learning: convolutions, pooling, normalization, attention,
activation functions, and the like. Frameworks such as PyTorch and TensorFlow don't hand-write
GPU code for these — they call cuBLAS and cuDNN, which is a big reason NVIDIA hardware is so
fast and so entrenched. They're NVIDIA's counterpart to Apple's [MPS](/glossary/mps/) (and roughly what a
[Vulkan](/glossary/vulkan/) or [Metal](/glossary/metal/) backend has to rebuild to compete). Both are proprietary,
closed-source NVIDIA libraries — free to use, though cuDNN in particular needs a separate
download and registration from the base CUDA toolkit.
