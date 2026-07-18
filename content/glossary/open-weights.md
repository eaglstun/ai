+++
title = "Open weights"
summary = "A model whose trained parameters are published for download, so you can run it offline and fine-tune it - narrower than 'open source,' which would also include the training data and recipe."
category = "Core concepts"
related = ["parameters", "qwen", "gguf", "lora", "mixture-of-experts"]
plain = "Getting the finished dish, not the recipe. A closed model is a restaurant - you order through the window and never enter the kitchen. An open-weight model is the whole cooked meal handed to you in a to-go box: you can eat it anywhere, reheat it, chop it up and remix it, and nobody can ever tell you the kitchen's closed. You just don't get the ingredient list, and you can't run the exact same kitchen yourself."
tags = ["open-weights", "fine-tuning", "quantization", "local-inference"]
semantic_id = "R3mrIN6hFtzvAGmkRn8LriOt70rGgAAK"
+++
**Open weights** means the company that trained a model published the actual trained
[parameters](/glossary/parameters/) - the billions of numbers that _are_ the model - so you can download the file and
run it on your own hardware instead of renting the model through someone else's API. Qwen, Llama,
Mistral, DeepSeek, and Gemma are open-weight; GPT-4 and Claude are not.

It is a narrower thing than "open source," and the difference matters. Open source, in the
traditional sense, means you get everything you'd need to rebuild the thing yourself: for a model
that would be the training data, the training code, and the recipe. Open _weights_ usually means
you get only the finished numbers - the cake, not the ingredient list or the instructions. You can
eat it, slice it, even re-frost it with a [LoRA](/glossary/lora/) fine-tune, but you can't rebake it from scratch,
and you often can't see what went into it. Many "open" models also ship with a license that
restricts commercial use or bans certain applications, which is a further step away from what open
source classically meant.

What you _can_ do with open weights is most of what people actually want: run the model offline
with no API bill and no data leaving your machine, inspect and measure its behavior directly,
shrink it with [quantization](/glossary/quantization/) into a [GGUF](/glossary/gguf/) file that fits on a laptop, fine-tune it into a
narrower or weirder version of itself, and keep running it unchanged for as long as you like - no
vendor can deprecate a model you already have on disk. That last point is the quiet one: an
open-weight model is the only kind nobody can take away from you.
