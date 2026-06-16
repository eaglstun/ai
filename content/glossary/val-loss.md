+++
title = "Validation loss"
summary = "Held-out validation error; the overfitting tripwire."
category = "Core concepts"
related = ["machine-learning", "parameters", "gradient-descent", "epsilon-gate"]
plain = "The pop quiz with questions it didn't study. During training you hold back some examples the model never sees, then test on those - if it aces what it studied but flunks the held-back quiz, it memorized instead of learned."
+++
**Validation loss** is how badly a model does on a _validation set_, data held back and not
used for training, measured with the same scoring used during training. Its counterpart is
_training loss_, the error on the data the model is actively learning from. The gap between the
two is the key thing to watch when training a [machine learning](/glossary/machine-learning/) model: while both keep
falling together, the model is genuinely learning; but when training loss keeps dropping while
validation loss flattens and then starts climbing, the model has begun **overfitting**:
memorizing its practice data instead of learning patterns that carry over, often a sign it has
more [parameters](/glossary/parameters/) than the data can pin down. That turning point is the usual cue for _early
stopping_ (keeping the version with the lowest validation loss) and for adjusting things like
regularization, learning rate, or dataset size. One important caveat: the validation set is
only for monitoring and tuning: a separate _test set_ is kept aside for the final, unbiased
measure of how good the model really is.
