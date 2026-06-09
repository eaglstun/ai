+++
title = "MLX"
summary = "Apple-silicon ML framework; the Mac answer to GGUF."
category = "Local inference & formats"
related = ["gguf", "metal", "tensor"]
plain = "Apple's home-field AI framework. A toolkit Apple built specifically to run and train models fast on Mac chips, taking advantage of the way Apple shares memory between the processor and the GPU."
+++
**MLX** is Apple's open-source framework for machine learning, built specifically for Apple
silicon (M-series chips). Its headline feature is **unified memory**: the CPU and GPU share one
pool of memory, so data doesn't have to be copied back and forth between them the way it does
with [CUDA](/glossary/cuda/). Under the hood it builds on Apple's [Metal](/glossary/metal/) GPU stack. The API is deliberately
close to NumPy (with PyTorch-style building blocks for neural networks), and it only does the
actual computing when you ask for a result rather than eagerly along the way (_lazy
evaluation_). It also works out the calculus that training needs automatically, and can shrink
models to smaller number formats right on the device. For running LLMs locally on a Mac, the
companion library `mlx-lm` loads and runs models in MLX format — the native Apple-silicon
alternative to the GGUF / llama.cpp world (often noticeably faster on a Mac, but Mac-only).
