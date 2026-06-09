+++
title = "GPT"
summary = "Generative pre-trained (decoder-only) transformer LLM."
category = "Architectures"
related = ["transformer", "gguf", "agi", "gelu"]
plain = "The autocomplete that ate the world. At heart it just guesses the next word over and over — but at enormous scale that simple trick turns into something that can write essays, code, and hold a conversation."
+++
**GPT** (Generative Pre-trained Transformer) is a family — and by now a whole class — of large
language models built on the "decoder" half of the [transformer](/glossary/transformer/) architecture. The name
spells out the recipe: _generative_ (it produces text), _pre-trained_ (it first learns broadly
from a huge pile of text before any task-specific tuning), and _transformer_ (the
attention-based network underneath). At its core it's a next-word predictor: given the text so
far, it guesses the most likely next chunk of text (a _token_), adds it, and repeats. At
enough scale, that simple loop yields fluent writing, reasoning, coding, and more. OpenAI's
GPT-2/3/4 and successors popularized the term, but "GPT" now gets used loosely for
decoder-only LLMs in general. One unrelated name collision worth knowing: **GPT** is also
_GUID Partition Table_, a disk-partitioning scheme — context tells them apart.
