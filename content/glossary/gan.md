+++
title = "GAN"
summary = "Generator-vs-discriminator generative architecture."
category = "Architectures"
related = ["latent-space"]
+++
**GAN** (Generative Adversarial Network) is a generative [machine learning](/glossary/machine-learning/) architecture,
introduced by Ian Goodfellow and colleagues in 2014, built from two neural networks locked
in competition. The **generator** takes a random vector from [latent space](/glossary/latent-space/) and tries to
produce realistic fake samples
(e.g. images); the **discriminator** is shown a mix of real and generated samples and tries
to tell which is which. They train against each other in a minimax game — the generator
gets better at fooling the discriminator while the discriminator gets better at catching it
— until, ideally, the fakes are indistinguishable from real data. GANs powered an era of
photorealistic face generation (StyleGAN) and image-to-image translation, but are
notoriously unstable to train (mode collapse, non-convergence) and have largely been
overtaken by diffusion models for general-purpose image generation, though they remain
useful where fast, single-pass sampling matters.
