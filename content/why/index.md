+++
title = "Why this exists"
summary = "I kept looking up the same AI words twice. This is the notebook I wish I'd had the first time."
tags = ["latent-space", "quantization", "tensor"]
semantic_id = "_H3i6-7opgaM34LeT7WpcA0IRcbs0AAB"
related_by_meaning = ["/blog/nobodys-hands-are-big-enough/", "/blog/is-that-what-you-wanted/"]
+++

I started this as a glossary for myself. I kept running into the same words,
_quantization_, _latent space_, _tensor_ - nodding along, and then quietly
looking them up again an hour later. So I wrote them down in plain language.

Then the definitions started leaking into everything else.

> You can't have a sane relationship with something you refuse to understand.

## I got tired of bluffing

Most writing about AI begins one floor above where I was standing. It explains why a
quantized checkpoint runs faster by using three other words I also have to look up. It
assumes that because I can operate the tool, I understand the machine. I often did not.

So the rule here is simple: if I cannot explain a term without hiding the hard part
behind another term, I am not done. Plain language is not baby language. It is the test
that tells me whether I understand the thing or merely recognize its vocabulary.

That test turned out to be useful well beyond a glossary. Once I understood what a
[LoRA](/glossary/lora/) could and could not change, I could run an experiment about
where a model's refusals lived. Once I understood [unified memory](/deep-dives/ctranslate2-metal-backend/unified-memory/),
I could see the one fact an entire Metal backend might hinge on. The definitions
became experiments, and the experiments became posts.

## The scary part is rarely the cinematic part

I'm not here to tell anyone to relax. Plenty of the fear around AI is earned: the disruption to
how people make a living, the flood of synthetic information nobody can verify, the concentration
of enormous power in a handful of companies. But Jason Pargin has
[a great bit](https://www.facebook.com/watch/?v=1515566466747777) about what science fiction
missed. It called the video calls and the pocket computers, and almost nobody imagined what the
_smartphone_ would actually do to us: the attention economy, the quiet collapse of privacy, the
rewiring of how we talk and think. The hardware was easy to predict. The transformation was
invisible until we were already living inside it.

AI looks the same to me. We spend our energy on the cinematic fears while the boring, structural,
everywhere-at-once changes happen somewhere we're mostly not looking, and they're hard to see
precisely because they're everywhere.

{{< nyer-panel src="lantern-at-the-door.jpg" caption="One legible patch at a time." alt="A continuous-line drawing: a small figure holds a warm lantern at the doorway of a vast dark hall, the light carving one readable patch out of the black." >}}

## The interesting part is usually one layer down

The loud questions are irresistible: Is it conscious? Will it take the jobs? Is it
safe? I keep getting more use from the smaller questions underneath them. Which part
of this result came from the model and which part came from the wrapper? What changed
when the adapter came off? Why did the bot agree with me? Who owns the off switch?

I'm not trying to tell you AI is fine, and I'm not trying to tell you to panic. I'm trying to make
the thing _legible_, because understanding is the prerequisite for everything else, whether that
ends up being fear or hope or, more likely, some uneasy mix of both.

That's all this site is. A working notebook. A glossary, some notes, the occasional deep dive. I
don't wait until I understand everything; that would be a very quiet website. I learn enough to
ask a better question, try the thing, write down what happened, and leave the machinery showing.
I'm still figuring it out myself. This is me doing that out loud.
