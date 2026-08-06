+++
title = "Context window"
summary = "How much text a model can hold in view at once, counted in tokens - input and output share the budget, its cost grows with the square of its size, and 'in the window' doesn't guarantee 'actually attended to.'"
category = "Core concepts"
related = ["token", "attention", "transformer", "embeddings"]
plain = "How much fits on the desk at once. The model doesn't have a filing cabinet it can rummage through - it can only reason about the papers physically spread out in front of it right now. Slide a new page on and, once the desk is full, one slides off the far edge and is gone from view. A bigger desk holds more of the project at once, but papers crowded into the middle still get glanced at less than the ones right under its nose."
tags = ["attention", "context-window", "token", "transformer"]
semantic_id = "ApbcdyyQmbFxJ9m5cdHd6YNXCGniEAAL"
+++
A model's **context window** is the amount of text it can hold in view at once - everything it's
currently "thinking about," measured in [token](/glossary/token/)s. It's the sum of what you put in _and_ what it
writes back: the system prompt, your question, any documents you pasted, the conversation so far,
and the reply it's generating all have to fit inside the same budget. Run past it and the oldest
material falls out of view; the model doesn't remember the start of a long chat, it just no longer
sees it.

The window exists because of how [attention](/glossary/attention/) works. In a [transformer](/glossary/transformer/), every token attends to
every other token in view, so the cost of the mechanism grows with the _square_ of the window -
double the context and you roughly quadruple the work. That quadratic wall is why context length
was small for years (a couple thousand tokens) and why stretching it to the hundreds-of-thousands
or millions you see advertised now took real engineering, not just a bigger number in a config
file. It's also why a long context is slower and more expensive per query: you're paying for all
that all-pairs comparison.

A big window is genuinely useful - you can drop a whole codebase or a long document in and ask
about it - but "fits in the window" and "actually used well" aren't the same thing. Models famously
attend unevenly across a long context, gripping the beginning and end and going vague in the middle
(the "lost in the middle" problem), so a fact buried at token 400,000 may be technically present
and effectively ignored. The window is how much the model _can_ see at once; it says nothing about
how evenly it looks.
