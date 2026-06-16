+++
title = "Qwen"
summary = "Alibaba's family of open-weight LLMs - decoder-only transformers you can download, run offline, and fine-tune, from phone-sized up to huge."
category = "Architectures"
related = ["gpt", "transformer", "gguf", "lora"]
plain = "The open-source car you can pop the hood on. The big-name chatbots are rentals - you drive them through an API and never see the engine - but Qwen is a model Alibaba hands you the keys and the schematics to: download it, take it apart, tune it, drive it around with no internet. That's why so many local and hobby projects start here."
+++
**Qwen** is a family of open-weight large language models from Alibaba Cloud (the name is short
for Tongyi Qianwen, 通义千问). Like a [GPT](/glossary/gpt/), each Qwen model is a decoder-only [transformer](/glossary/transformer/)
trained to predict the next token. The part that matters in practice is the _open-weight_ part:
Alibaba publishes the actual trained [parameters](/glossary/parameters/), much of the family under the permissive
Apache 2.0 license, so anyone can download a Qwen model and run it on their own hardware instead
of renting it through someone else's API.

The family comes in generations (Qwen, Qwen1.5, Qwen2, Qwen2.5, Qwen3) and a wide spread of
sizes, from tiny half-billion-parameter models that fit on a phone up to very large
mixture-of-experts models in the hundreds of billions. There are specialized branches too:
**Qwen-Coder** for programming, **Qwen-VL** for images-plus-text, **Qwen-Audio** for sound, and
reasoning-focused variants. Because the weights are open and even the small sizes are genuinely
capable, Qwen has become one of the most common starting points for running models locally: it
ships in [GGUF](/glossary/gguf/) form for llama.cpp and Ollama, and it's a frequent base for [LoRA](/glossary/lora/) fine-tunes
that teach it a narrower job or a particular voice.

If [GPT](/glossary/gpt/) is the closed model you reach through an API, Qwen is the open one you can actually
hold: download it, inspect it, fine-tune it, run it offline. That difference is most of why it
turns up so often in local-inference and hobbyist projects, where the few flagship Qwen models
that stay API-only matter far less than the dozens you can just pull down and run.
