+++
title = "ReLU"
summary = "The simplest activation gate: zero out negatives, pass positives through."
category = "Building blocks"
related = ["gelu", "transformer", "tensor", "residual-connections"]
plain = "The simplest bouncer there is. One rule: negative numbers get turned away at the door, positive numbers walk right in unchanged. Crude, but cheap and effective - and for years it was the default gate inside neural networks."
image = "/glossary-img/relu.webp"
image_alt = "A claymation still: a scowling plasticine bouncer sends grumpy blue blobs shuffling away from the door while cheerful yellow ones head on in - negatives turned away, positives let through unchanged."
tags = ["relu", "machine-learning", "training"]
semantic_id = "v2:JWh-9M8wz4a0BSqLgVQrbaxP19Jw7Ptf"
+++
**ReLU** (Rectified Linear Unit) is the simplest useful activation function, the little
nonlinear gate that sits between the layers of a neural network and decides how much of each
signal to pass forward. Its whole rule fits in one line: if a number is negative, output
zero; if it's positive, leave it alone. That's it. Negative gets bounced, positive walks
right through.

You need a gate like this because without one, stacking layers is pointless: a pile of
plain linear steps just collapses back into a single linear step, so the network could only
ever draw straight lines. ReLU's hard kink is enough to break that and let the model bend.
It became the default for years because it's dirt cheap to compute and it sidesteps an old
training headache (the "vanishing gradient," signals shrinking to nothing as they pass back
through a deep stack). Its one quirk is that a unit stuck on the negative side outputs zero
forever and stops learning (a "dead" unit), which is part of why smoother successors like
[GELU](/glossary/gelu/) took over inside big [transformer](/glossary/transformer/) models. It runs element-wise across a
[tensor](/glossary/tensor/).
