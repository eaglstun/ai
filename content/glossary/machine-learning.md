+++
title = "Machine learning"
summary = "Systems that learn patterns from data instead of hand-written rules."
category = "Core concepts"
related = ["tensor", "transformer", "parameters", "val-loss"]
+++
**Machine learning (ML)** is the branch of AI where a system learns patterns from data
rather than following rules a programmer wrote by hand. Instead of coding the logic
directly, you define a model with adjustable [parameters](/glossary/parameters/) and an objective (a loss
function), then run **training**: feed in examples, measure how wrong the predictions are,
and nudge the parameters to reduce that error — repeated over and over until the model
generalizes. Once trained, using it on new inputs is **inference**. The classic split is by
what the data looks like: **supervised** learning trains on labeled examples (input →
correct output), **unsupervised** learning finds structure in unlabeled data (clustering,
[latent space](/glossary/latent-space/) embeddings), and **reinforcement** learning trains an agent via rewards
from acting in an environment. **Deep learning** is the modern subfield that uses many-layered
neural networks built from [tensor](/glossary/tensor/) operations — the [transformer](/glossary/transformer/) and [GAN](/glossary/gan/) are deep-learning
architectures — and it's what powers most of what people now call "AI." The perennial
hazard across all of it is generalization: a model that aces training data but flops on new
data has overfit, which is why you watch [validation loss](/glossary/val-loss/).
