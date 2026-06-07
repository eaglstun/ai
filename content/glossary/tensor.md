+++
title = "Tensor"
summary = "N-dimensional numeric array; the core ML data structure."
category = "Core concepts"
related = ["dimensions", "mlx", "transformer", "parameters"]
+++
**Tensor** is the fundamental data structure of modern [machine learning](/glossary/machine-learning/): an n-dimensional
array of numbers. It generalizes the familiar cases — a scalar is a 0-D tensor, a vector is
1-D, a matrix is 2-D — to arbitrary _rank_ (number of [dimensions](/glossary/dimensions/)), e.g. a batch of RGB
images is a 4-D tensor of shape `[batch, height, width, channels]`. Every input, weight,
activation, and gradient in a neural network is a tensor, and training is essentially a
long chain of tensor operations (matrix multiplies, additions, nonlinearities). Frameworks
like PyTorch, TensorFlow, JAX, and [MLX](/glossary/mlx/) are built around tensors and run those
operations on accelerators (GPUs/TPUs) — hardware whose whole purpose is massively parallel
tensor math. Two properties matter most in practice: _shape_ (the size along each
dimension, the usual source of bugs) and _dtype_ (numeric precision, e.g. fp32/fp16/bf16,
which trades accuracy for speed and memory). Note: the ML "tensor" is essentially a
multidimensional array and is looser than the strict mathematical/physics definition.
