+++
title = "Embeddings"
summary = "Dense vectors where distance & direction encode meaning — the backbone of semantic search and RAG."
category = "Core concepts"
related = ["latent-space", "dimensions", "tensor"]
+++
**Embeddings** are learned, dense vector representations of discrete things — words,
sentences, images, products, users — positioned so that _distance and direction encode
meaning_. Instead of representing a word as an arbitrary ID or a giant sparse one-hot vector
(all zeros but a single 1, which says nothing about similarity), an embedding maps it to a
few hundred or few thousand real numbers (e.g. 768 [dimensions](/glossary/dimensions/)) where semantically
related items land near each other. They're produced by training a model on a task and
reading out an internal layer; the resulting vectors live in a [latent space](/glossary/latent-space/), which is
what makes the famous "king − man + woman ≈ queen" arithmetic work. Practically, embeddings
are the backbone of semantic search, recommendation, clustering, and **RAG**
(retrieval-augmented generation): you embed a query and find the nearest stored vectors by
cosine similarity. The vectors themselves are just [tensor](/glossary/tensor/)s, and at scale they're kept in
a **vector database** built for fast nearest-neighbor lookup.
