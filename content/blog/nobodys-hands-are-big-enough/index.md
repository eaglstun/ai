+++
title = "Nobody's Hands Are Big Enough"
date = 2026-06-12
images = ["/og/nobodys-hands-are-big-enough.png"]
description = "A frontier model gives one person more leverage than one person can supervise. Model safety is only half the question."
summary = "A model wrote me a working GPU backend in an afternoon. The useful safety question is not only what the model can do, but who gets to direct it."
tags = ["ai-safety", "alignment", "gpt"]
semantic_id = "_eOJCa7DxYXIl-z73X6u0QtGtZ7owAou"
related_by_meaning = ["/glossary/alignment/", "/blog/is-that-what-you-wanted/", "/practice/172-witnesses/", "/why/"]
+++

Picture the smallest person you love. For me it's an infant, a daughter you could hold in one
arm, new enough that her hands still open and close on nothing. You would not hand her a lit
match. Not because she's dangerous. She is the least dangerous person in the building. You hold
her back because the distance between what she can set in motion and what she can hold steady is
the entire world, and closing one inch of it is the only thing the word _responsibility_ has ever
meant.

Every few months we hand her something bigger and call it a launch.

<!--more-->

![A single-line ink drawing: a small man tips a bowl of glowing stars onto a mountain of gears already taller than he is, while a giant hand lowers one more lightbulb onto the pile. No pair of hands is big enough.](nobodys-hands-plate.jpg)

## What one person can reach

We argue about whether [these models](/glossary/gpt/) are smart, conscious, [aligned](/glossary/alignment/), or coming for
our jobs, and walk clean past the plainer fact on the table: they put an enormous amount of
specialized work behind one chat box, available to one person, immediately.

This week I watched one write a working
GPU backend for [CTranslate2](https://github.com/eaglstun/CTranslate2), serious inference software,
in one afternoon, for about a hundred and fifty dollars, in a language I cannot read a line of.
The project had gone its whole life without that backend, and not for lack of wanting. It was
missing because the doing was hard: the few engineers on earth who can build one bill in the tens
of thousands and book out for months. That was the going rate on hard, and this week it fell to a
hundred and fifty dollars for a guy who cannot read the output. That is useful. It is also more
leverage than the person holding it can check.

Now picture the same lever aimed at something that isn't a software library.

## The other safety question

The industry asks whether the model is safe, aligned, and tested. Good questions, all aimed one
inch left of the other one. The model doesn't act alone. Someone holds it. And the question we
tiptoe around, because the answer is inconvenient, is how much any one person should be able to
set in motion with nobody else's hands on the controls.

We know the answer. We built the whole architecture of civilization on knowing it. States,
courts, constitutions, term limits: an apparatus that exists so no single person holds much real
power without a dozen hands ready to stop them. Not because people are evil. Because good
intentions never made anyone big enough to supervise everything they can now start. A genius with
a match is still holding a match. The hands are not big enough. They were never going to be.

## Release is part of safety

I think it was reckless to release, and I'll say it about the lab whose work I admire most,
because the safety work can be sincere and still leave this question untouched. Red-teaming and
refusals test what the model will do. They do not decide how much unsupervised reach one operator
should get when the model works exactly as intended. A perfectly behaved model handed to everyone
is still the most concentrated leverage in history handed to everyone. "It works as designed"
isn't the reassurance. It's the worry.

And the makers know. The week I'm writing this, one of these models got pulled off the planet
overnight, [the moment its power crossed a line the government would not leave to the lab](/blog/the-first-ai-law-was-a-weapons-law/).
You don't yank a toaster overnight. You yank the thing when you catch a clear look at what you
built and who's holding it. Good instinct, aimed at one model on one afternoon, when what needs
the flinch is the question of handing this out at all.

{{< nyer-panel src="reaching.png" caption="The infant is us." alt="A vintage engraving: an infant's two tiny hands reach up from below toward an enormous radiant orb of light far above them." >}}

## Who this is really about

The infant was never the machine. We love to put the baby face on the AI: careful, careful, it's
so young. Wrong crib. The model is the loaded thing, calm and capable and indifferent to who's
carrying it. _We_ are the infant, reaching up with hands that open and close on nothing, for a
grip we don't have, on more than a person was ever built to hold.

Model safety matters. So does the size of the hands. A release decision that asks only whether the
model behaves has answered half the question, and the least anyone could do is be as scared as
you'd be standing over that crib, watching those small hands reach.
