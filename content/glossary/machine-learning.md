+++
title = "Machine learning"
summary = "Systems that learn patterns from data instead of hand-written rules."
category = "Core concepts"
related = ["tensor", "transformer", "parameters", "val-loss", "agi", "gradient-descent"]
plain = "Teaching by examples instead of rules. Instead of writing out every rule for 'what a cat looks like,' you show the computer thousands of cat photos and let it work out the pattern itself."
+++
**Machine learning (ML)** is the branch of AI where a system _learns_ patterns from data
instead of following step-by-step rules a programmer wrote out. Rather than code the logic
directly, you set up a model with adjustable [parameters](/glossary/parameters/) (its internal dials) and a way to
score how wrong it is (a _loss function_), then run **training**: show it examples, measure
the error, and nudge the dials to shrink that error — over and over, until the model works on
examples it hasn't seen before. Using a trained model on new input is called **inference**.
The classic split is by what the data looks like: **supervised** learning trains on labeled
examples (input → correct answer), **unsupervised** learning finds structure in unlabeled data
(grouping things, building [latent space](/glossary/latent-space/) embeddings), and **reinforcement** learning trains
an agent through rewards as it acts in some environment. **Deep learning** is the modern flavor
that stacks many layers of [tensor](/glossary/tensor/) math into neural networks — the [transformer](/glossary/transformer/) and
[GAN](/glossary/gan/) are deep-learning designs — and it's what powers most of what people now call "AI."
The constant hazard everywhere in ML is generalization: a model that aces its practice data
but flops on new data has **overfit**, which is why you keep an eye on [validation loss](/glossary/val-loss/).
