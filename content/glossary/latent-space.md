+++
title = "Latent space"
summary = "The hidden vector space where geometry encodes meaning."
category = "Core concepts"
related = ["gan", "dimensions", "embeddings"]
+++
**Latent space** is the abstract space — usually of far fewer [dimensions](/glossary/dimensions/) than the raw
input — in which a model represents the compressed, encoded "essence" of its input data. Instead of working with raw pixels or
tokens, the model maps each input to a point (a vector) in this space, where each dimension
captures some learned feature rather than a human-labeled one — hence _latent_, meaning
hidden. The useful property is that geometry becomes meaning: inputs that are semantically
similar land near each other, and directions in the space can correspond to interpretable
changes (the classic "king − man + woman ≈ queen" with word embeddings). Autoencoders,
diffusion models, and embedding models all rely on it; generative models (a [GAN](/glossary/gan/), say)
work by sampling or steering points in latent space and then decoding them back into images,
text, or audio.
