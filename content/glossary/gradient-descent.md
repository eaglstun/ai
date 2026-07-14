+++
title = "Gradient descent"
summary = "The downhill-walking algorithm that trains models - nudge every parameter to shrink the error, then repeat."
category = "Core concepts"
related = ["machine-learning", "parameters", "val-loss", "latent-space", "norm-placement", "epsilon-gate"]
plain = "Finding the bottom of a valley in thick fog. You can't see where the lowest point is, but you can feel which way the ground slopes under your feet - so you step downhill, feel again, and repeat until it flattens out. Training a model is that same move done millions of times, with 'how wrong it is' as the hill."
tags = ["gradient-descent", "machine-learning", "training", "val-loss", "latent-space"]
semantic_id = "tk2ORXo4aIiKCm1cSqoOBeFz16emkAAL"
+++
**Gradient descent** is the basic algorithm that lets a model _learn_, the optimization engine
underneath almost all modern [machine learning](/glossary/machine-learning/). Training starts with a model that's wrong,
scores _how_ wrong with a **loss** (a single number measuring error), and then asks, for every
one of the model's [parameters](/glossary/parameters/): "which way should I nudge this, and how hard, to make the
loss a little smaller?" That whole bundle of directions-and-magnitudes is the **gradient**: the
slope of the loss. Take one small step downhill along it and the model gets slightly less wrong;
repeat millions of times and the error grinds toward a bottom.

The size of each step is the
**learning rate**: too large and the model overshoots and thrashes, too small and training
crawls. In practice you rarely use the whole dataset for each step, _stochastic gradient
descent_ (SGD) estimates the slope from one small batch at a time, and smarter variants like
_Adam_ adapt the step size per parameter as they go.

One thing worth keeping straight: gradient
descent only ever drives the _training_ loss down. Whether the model is genuinely learning
rather than memorizing is what [validation loss](/glossary/val-loss/) is there to catch.

And the machinery doesn't have to
move a model's weights at all: freeze the model and run the same descent over its _input_
instead, and you can search a [latent space](/glossary/latent-space/) for the point that produces what you want, which
is exactly how GAN-based upscalers hunt for a face that matches a blurry photo.
