+++
title = "Hallucination"
summary = "When a model states something false as fluently and confidently as something true, because its job is to predict a plausible next token, not to say only true things - and it has no built-in signal for 'I don't know.'"
category = "Core concepts"
related = ["gpt", "token", "temperature", "alignment", "attention"]
plain = "The confident friend who never says 'I don't know.' You ask where a restaurant is and they give you crisp, detailed directions in the exact same voice whether they know the place or have never heard of it - because to them, sounding sure and being right feel like the same thing. The model has that friend's exact talent: it always produces a smooth answer, and it has no separate face it makes when it's guessing."
tags = ["hallucination", "gpt", "token", "temperature"]
semantic_id = "Xb0FG1bnL4aeCv3AcBsg07_qIQrAUAAE"
+++
A **hallucination** is when a model states something false with the same fluent confidence it uses
for something true - a made-up citation, a plausible wrong date, a function that doesn't exist, a
biography of a person who never lived. The unsettling part isn't that it's wrong; all software is
sometimes wrong. It's that nothing in the output _looks_ wrong. The model has no separate "I'm not
sure" voice; the lie and the fact come out in the same tone.

It helps to remember what the model is actually doing. A [GPT](/glossary/gpt/)-style model predicts the next
[token](/glossary/token/) over and over, and "predict the most plausible continuation" is not the same job as "say
only true things." Most of the time plausible and true point the same way, because true statements
were the bulk of what it read. But when the model doesn't know - a fact that wasn't in its training
data, a detail too specific to have a stored answer - it doesn't stop. It has no _off_ switch for
uncertainty; it produces the most likely-sounding continuation anyway, and a confident fabrication
is often more likely-sounding than an admission of ignorance. [temperature](/glossary/temperature/) can turn the dice up
or down, but the behavior is baked into the objective, not just the sampling.

This is why "hallucination" is a slightly generous word - it frames a bug as a lapse, when really
it's the machine working exactly as designed, just pointed at a question it can't answer from
memory. The practical fixes don't try to make the model _know_ more; they try to keep it from
having to guess: give it the source text in-context so the answer is in front of it (retrieval),
make it show work it can check, or wire it to tools that can look things up. None of that cures it.
It just narrows the gap between "sounds right" and "is right," which is the gap hallucination lives
in.
