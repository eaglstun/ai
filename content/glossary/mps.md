+++
title = "MPS"
summary = "Metal Performance Shaders; Apple's cuDNN-equivalent ops."
category = "GPU compute & backends"
related = ["metal", "mlx", "cuda", "cudnn-cublas"]
+++
**MPS** (Metal Performance Shaders) is Apple's set of hand-optimized GPU building blocks built
on top of [Metal](/glossary/metal/) — ready-made routines for things like matrix multiply, convolution, and
other neural-network operations, plus a higher-level graph API (**MPS Graph**) that schedules
and combines them efficiently. It's roughly Apple's answer to NVIDIA's [cuDNN / cuBLAS](/glossary/cudnn-cublas/): the
optimized pieces frameworks call instead of writing raw GPU code themselves. In day-to-day use
you meet MPS as **PyTorch's `mps` device** (`torch.device("mps")`), which is how PyTorch runs
on Apple-silicon GPUs instead of falling back to the CPU; Apple's [MLX](/glossary/mlx/) leans on the same
Metal foundation. Note the name collision: "MPS" here means Metal Performance Shaders, not
"model-parallel" anything.
