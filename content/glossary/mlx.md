+++
title = "MLX"
summary = "Apple-silicon ML framework; the Mac answer to GGUF."
category = "Local inference & formats"
related = ["gguf", "metal", "tensor"]
+++
**MLX** is Apple's open-source array framework for machine learning, built specifically
for Apple silicon (M-series chips). Its headline feature is **unified memory**: the CPU
and GPU share the same memory pool, so arrays don't have to be copied back and forth
between "host" and "device" the way they do with [CUDA](/glossary/cuda/). Under the hood it builds on
Apple's [Metal](/glossary/metal/) GPU stack. The API is deliberately NumPy-like
(with PyTorch-style neural-net modules), and it uses lazy evaluation — computations are
only materialized when you actually need the result. It supports automatic differentiation
and on-device quantization. For local LLM work on a Mac, the companion library `mlx-lm`
loads and runs models in MLX format, making it the native Apple-silicon alternative to the
GGUF / llama.cpp ecosystem (often noticeably faster on Mac, but Mac-only).
