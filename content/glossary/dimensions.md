+++
title = "Dimensions"
summary = "Independent axes of variation; ML vectors live in hundreds or thousands of them."
category = "Core concepts"
related = ["tensor", "latent-space"]
+++
**Dimensions** are independent axes of variation — each one a separate number you need to
pin down a point. A point on a line takes 1, on a map 2, in a room 3; in ML a data point
is usually a vector with hundreds or thousands of dimensions, one per feature (a word
embedding might live in 768-D, an image flattened into many thousands). The number of
dimensions of a [tensor](/glossary/tensor/) is its _rank_, and the rich geometry of [latent space](/glossary/latent-space/) is
exactly this: meaning encoded as position in a high-dimensional space.

**How to imagine more than 3 or 4.** The honest answer: you don't picture it — you stop
trying to _see_ it and start reasoning about it. A few tricks that actually work:

- **It's just a longer list.** A 100-D point isn't a mysterious shape; it's a list of 100
  numbers. "Add a dimension" = "track one more independent number." Most operations
  (distance, dot product, averaging) are just the 2-D/3-D formulas with more terms summed.
- **Reason by analogy, then generalize.** Work out what's true in 2-D and 3-D — a sphere,
  the corners of a cube, the distance between two points — and trust the algebra to carry
  it to N-D, even when the mental picture gives out. Hinton's half-joke captures the spirit:
  "to deal with a 14-dimensional space, visualize a 3-D space and say 'fourteen' to yourself
  very loudly."
- **Expect high-D to be weird.** Intuition built in 3-D actively misleads you up there.
  Almost all of a high-dimensional cube's volume sits in its corners, randomly chosen points
  are nearly all the same distance apart, and volume concentrates near the surface of a
  sphere. This bundle of surprises is the **curse of dimensionality** — and it's why
  reasoning beats visualizing.
