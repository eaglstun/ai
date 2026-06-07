+++
title = "Validation loss"
summary = "Held-out validation error; the overfitting tripwire."
category = "Core concepts"
related = []
+++
**Validation loss** is the error a model scores on a held-out _validation set_ — data it
isn't trained on — measured with the same loss function used during training. It's the
counterpart to _training loss_ (error on the data the model is actively learning from). The
gap between the two is the headline diagnostic when training a model: while both fall
together, the model is genuinely learning; when training loss keeps dropping but validation
loss flattens and then starts rising, the model has begun **overfitting** — memorizing the
training data instead of generalizing. That turning point is the usual signal for _early
stopping_ (keeping the checkpoint at the lowest val loss) and for tuning regularization,
learning rate, or dataset size. Crucially, the validation set is for monitoring and tuning
only; a separate _test set_ is reserved for the final, unbiased performance estimate.
