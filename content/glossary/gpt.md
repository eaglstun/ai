+++
title = "GPT"
summary = "Generative pre-trained (decoder-only) transformer LLM."
category = "Architectures"
related = ["transformer", "gguf"]
+++
**GPT** (Generative Pre-trained Transformer) is a family — and now a general class — of
large language models built on the decoder side of the [transformer](/glossary/transformer/) architecture. The
name unpacks the recipe: _generative_ (it produces text), _pre-trained_ (it first learns
broadly from a huge corpus before any task-specific tuning), and _transformer_ (the
attention-based network underneath). At its core it's an autoregressive next-token
predictor — given the text so far, it predicts the most likely next token, then repeats —
which, at sufficient scale, yields fluent writing, reasoning, coding, and more. The lineage
(OpenAI's GPT-2/3/4 and successors) popularized the term, but "GPT" is now used loosely for
decoder-only LLMs in general. Note the unrelated collision: **GPT** also stands for _GUID
Partition Table_, a disk-partitioning scheme — context disambiguates.
