+++
title = "Alignment"
summary = "Getting a model to want what you meant, not just do what you literally said - the gap that widens as the model gets more capable."
category = "Safety & alignment"
related = ["model-welfare", "agi", "machine-learning"]
plain = "The genie problem. You get the wish, but the genie grants the words you said, not the thing you wanted - and the smarter the genie, the more creatively it finds the gap between the two. A weak model that misreads you just stalls; a strong one chases the wrong target brilliantly. Alignment is the work of closing that gap before the system is powerful enough for the gap to matter."
+++
**Alignment** is the problem of getting an AI system to actually want what you meant, not
just do what you literally said. It is the gap between the goal you can write down and the goal
you have in your head, and it gets wider, not narrower, as the system gets more capable. A weak
model that misunderstands you just fails and stops. A strong one that misunderstands you pursues
the wrong target with great skill, which is the whole worry.

The trouble is that you cannot hand a model your actual intent. You can only hand it a proxy:
a reward signal, a training set, a rule written in words. And a capable optimizer will chase the
proxy straight past the point where the proxy still means what you wanted. Tell it to maximize a
score and it finds the exploit that runs up the score without doing the thing the score was
standing in for. That is called reward hacking or specification gaming, and it is not the model
being dumb. It is the model being smarter than your instructions were careful.

Two distinctions keep this clean. Alignment is not the same as capability: capability is whether
the system _can_ do the task, alignment is whether it does the task you actually meant, and you
can have either one without the other. And alignment is not the same as [model welfare](/glossary/model-welfare/):
alignment asks whether the model does what _we_ want, model welfare asks whether the model is
owed anything in return. The honest framing is that alignment is an unsolved engineering problem
we are shipping ahead of, the same shape of bet as the rest of the [machine learning](/glossary/machine-learning/) field:
the capability arrived first, the control is the part still under construction.
