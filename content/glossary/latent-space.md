+++
title = "Latent space"
summary = "The hidden vector space where geometry encodes meaning."
category = "Core concepts"
related = ["gan", "dimensions", "embeddings", "gradient-descent"]
plain = "The secret organizing closet. Picture a walk-in closet sorted not by color but by vibe - leather jackets near combat boots, tuxedos near silk ties. It's the AI's internal closet where similar ideas get stored near each other so it can find them later."
image = "/glossary-img/latent-space.webp"
image_alt = "A dreamy aerial photograph of a misty valley at dawn, softly glowing clustered forms floating in fog with similar shapes gathered together - a map of meaning."
tags = ["latent-space", "embeddings", "diffusion", "gan", "image-generation"]
semantic_id = "5DhGa3ZUVrXLLh6-wbAr_N3yKb5gEAAM"
+++
**Latent space** is the abstract, usually much smaller space in which a model holds the
compressed "essence" of its input. Rather than work with raw pixels or words, the model maps
each input to a point (a vector) in this space, where each axis captures some feature the
model _learned_ on its own rather than one a human labeled, hence _latent_, meaning hidden.
The useful part is that geometry turns into meaning: similar inputs land near each other, and
moving in a particular direction can correspond to a meaningful change (the classic
"king − man + woman ≈ queen" with word embeddings). Many kinds of models rely on it:
autoencoders, diffusion models, embedding models, and generative models (a [GAN](/glossary/gan/), say) work
by picking or nudging a point in latent space and then translating it back out into an image,
text, or audio.
