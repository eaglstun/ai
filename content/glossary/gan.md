+++
title = "GAN"
summary = "Generator-vs-discriminator generative architecture."
category = "Architectures"
related = ["latent-space"]
+++
**GAN** (Generative Adversarial Network) is a type of generative [machine learning](/glossary/machine-learning/) model —
introduced by Ian Goodfellow and colleagues in 2014 — built from two neural networks set
against each other. The **generator** starts from a random vector in [latent space](/glossary/latent-space/) and
tries to produce realistic fakes (say, images). The **discriminator** is shown a mix of real
and fake samples and tries to tell them apart. They train as rivals — the generator keeps
getting better at fooling the discriminator while the discriminator keeps getting better at
catching it — until, ideally, the fakes are indistinguishable from the real thing. GANs drove
an era of photorealistic face generation (StyleGAN) and image-to-image translation, but
they're notoriously finicky to train (a common failure is _mode collapse_, where the
generator churns out the same few outputs). For general image generation they've largely been
overtaken by diffusion models, though they still shine where fast, one-shot sampling matters.
