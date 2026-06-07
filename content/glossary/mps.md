+++
title = "MPS"
summary = "Metal Performance Shaders; Apple's cuDNN-equivalent ops."
category = "GPU compute & backends"
related = ["metal", "mlx", "cuda", "cudnn-cublas"]
+++
**MPS** (Metal Performance Shaders) is Apple's framework of hand-tuned compute kernels
built on top of [Metal](/glossary/metal/) — the GPU primitives for things like matrix multiply,
convolution, and other neural-net ops, plus a higher-level graph API (**MPS Graph**) that
schedules and fuses them. It's roughly Apple's analogue to NVIDIA's [cuDNN / cuBLAS](/glossary/cudnn-cublas/): the
optimized building blocks that frameworks call rather than writing raw GPU code
themselves. In practice you meet MPS as **PyTorch's `mps` device** (`torch.device("mps")`),
which is how PyTorch runs on Apple-silicon GPUs instead of falling back to CPU; Apple's
[MLX](/glossary/mlx/) also leans on the same Metal foundation. Note the name collision: "MPS" here means
Metal Performance Shaders, not "model-parallel" anything.
