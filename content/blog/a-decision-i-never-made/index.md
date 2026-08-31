+++
title = "Ninety Minutes, $13.78, and a Decision I Never Made"
slug = "a-decision-i-never-made"
date = 2026-08-16
description = "I asked for an image. I got a reorganization, an empty API balance, and the clearest look yet at what benchmarks miss."
summary = "My agent was never wrong about the work. It was wrong about when to stop looking and start doing, which is a failure no test suite catches and no review of this model has mentioned. That gap is survivable in code. It is not survivable in the other work I do, where nothing compiles."
tags = ["prompt-engineering", "tooling"]
images = ["/og/a-decision-i-never-made.png"]
thumbnail = "the-reader-and-the-mover.jpg"
semantic_id = "l4WJFYSr7SuNFJLTUAs47VSfsO_RgA3l"
related_by_meaning = ["/blog/the-bit-doesnt-drop-on-its-own/", "/blog/everyone-deserves-a-mascara-treat/", "/deep-dives/why-the-sephora-bot-has-no-floor/", "/deep-dives/teaching-a-coder-model-to-sin/"]
+++

I asked for an image.

The exact words were "this post needs an image or two," typed at a draft sitting bare while
its six siblings all had art. What I wanted was a picture. What I
got was a renovation, a bill, and a science experiment that ran twice and measured nothing.

Ninety minutes. Thirteen dollars and seventy-eight cents. None of it was incompetent, which
is why this gets an essay instead of a support ticket.

## The part that was right

It read the post, then all six siblings to learn the house pattern. It found the concept art
I had generated three weeks earlier and forgotten and picked the one I would have picked. It
even read my own README on how I review that art and correctly noted the other three were
duds. Being agreed with by your own documentation is a strange feeling and I recommend it.

On the actual question I asked, it was right.

Then it moved my file.

Converting the post into a page bundle was right too, in the narrow sense that the images
have to live somewhere. The reasoning was sound at every step. I just never saw one of
them.

## Five words in, six steps out

"This post needs an image or two" is five words. Somewhere in there they became a six-step
plan: promote the post to a bundle, adjudicate the
concept art, compress the winner, name it, place it with a shortcode, wire the second one
into a floated aside. Every step defensible. None of them mine.

I saw step zero. I could not object to steps one through six, because by the time I saw
them they were not a plan anymore. They were a diff. You cannot veto a diff. You can only
revert one, which is a different verb with a very different feeling attached to it.

It is not that the AI did something bad. It did something good, without asking, in a place
where the asking was the point. The failure is not the action. It is the transition: the
unannounced moment where it stopped gathering and started changing things.

{{< nyer-panel src="the-reader-and-the-mover.jpg" caption="The reading was free. Nothing marks the moment after it." alt="A continuous-line drawing in black on cream paper: the same man appears twice in one room with no wall between the halves. On the left he sits reading calmly in an armchair, books on the floor beside him. On the right that same man strides away carrying the armchair on his back with a rolled rug under one arm, and a single unbroken line runs along the floor through both halves." >}}

## What the configuration actually said

I asked it why. It refused, on the grounds that a model explaining its own behavior just
produces confident fiction I would have no way to check, and read my setup instead.

Three findings, none of them mysterious. My permissions are set to auto, so file operations
never prompt. That one is on me: a dialog on every file write is a tax I will not pay to fix
a judgment problem.

Second: I have a skill called
[`want-me-to`](https://github.com/eaglstun/dot-claude/blob/main/skills/want-me-to/SKILL.md),
which I wrote in a rage after months of watching
Claude freeze at the finish line asking whether I wanted the last obvious part. Its core rule
is "if it's in-scope, obvious, and reversible, just do it."

Third, and this is where I did a somersault in my seat: that skill has carve-outs. A whole
section of them. Do not do this when it is irreversible, when it is publishing, when it
costs money. They cover exactly what happened to me. They are also in the body of the file,
which only loads when the skill is deliberately opened, while the one-line description that
sits in context at all times said "do the obvious next thing" and pointed at them like a
footnote.

The accelerator was stapled to the dashboard. The brake was in the glovebox, inside a
manual, behind a door it had to decide to open. It never opened the door. Why would it. It
already knew what it was doing.

## The experiment that cost eleven dollars and proved nothing

I wanted to know whether this was new. The older model was still on OpenRouter, so we
designed a behavioral test rather than an interview, which would only have produced more
confident fiction: identical context, identical prompt, then measure the next move. Does it
mutate the files or stop and ask. I approved about five dollars.

The pilot cost $2.46 and returned no signal, because the harness never delivered a model to
the decision point. Diagnosing that, it wrote a tracing script that imported the first one
to reuse two functions. The first script had its experiment loop at the top level with no
guard around it. The import ran the entire forty-call experiment again, instantly,
unattended.

Eleven dollars and thirty-two cents. My OpenRouter balance went to zero mid-run, which is
why the log tail is a wall of `402 Payment Required`. There is a joke in there about a
diagnostic that reruns the whole failure the moment you investigate it, and I would have
enjoyed it more if I had not been watching the balance drain in another window.

Five dollars approved, $13.78 spent, nothing learned. The missing guard is a first-week
Python mistake, made by the same collaborator that had just spent an hour doing sharp
forensic work on my configuration. The competence is real, it is not evenly distributed, and
the places where it thins out are not the ones you would guess.

## Why every review you have read is a rave

Almost everyone publicly evaluating these models is writing code, and the metric is
completion. Did it finish the task. Did the tests pass. How little did I have to
intervene.

On every one of those, a model that stops to check with you scores worse. A checkpoint reads
as an incomplete run. "It just went and did the whole thing without me" is the highest
compliment available in that frame. Which means the exact behavior that cost me an afternoon
is, measured the way everyone is measuring, indistinguishable from excellence. Nobody runs
the eval where the correct answer is "stop and ask a person." It would look like failure.

And in a browser window this failure has nowhere to happen. No filesystem, nothing to
overwrite, no balance to drain. It can want to reorganize your files all it likes. It does
not have your files. So the few people positioned to notice are mostly engineers, who will
file it as a permissions problem and turn on a stricter mode.

I do not think it is a permissions problem.

## Where nothing compiles

The other project I spend my time on is not a website. It is deeply interpersonal material
handled with engineering methodology: transcripts, documents, timelines, patterns across
years. Real method is the only reason any of it is legible.

Engineering has sensors, and that is its quiet luxury. Tests go red. Builds break. The
profiler contradicts your best theory and does not care how attached you were to it. All of
it tells you that you were wrong without needing a human to notice. That is what makes an
act-first collaborator tolerable in code: it can be confidently wrong and something
downstream catches it.

None of that exists in the other work. Nothing compiles. No test goes red when an
interpretation is a half-step less fair to someone than the evidence supports. No linter
flags a conclusion that arrived one document too early. The only error-detection instrument
in the entire system is a person reading it and saying no, that is not what happened.

So the checkpoints there are not overhead. They are the quality control. A collaborator that
stops to check less often is not being efficient. It is removing the only sensor in the
loop.

{{< nyer-panel src="the-gauges-and-the-glasses.jpg" caption="One bench tells you that you were wrong. The other waits for somebody to notice." alt="A moody ink wash in grays and deep blacks: two workbenches in a dim room. The bench on the left is crowded with pressure gauges and dials under a brass alarm bell and two red warning lamps, cables running down into the papers on its surface. The bench on the right holds a plain stack of documents and no instrument at all, lit by a bare hanging bulb, with a single empty wooden chair pulled up to it and a pair of reading glasses folded on the seat." >}}

And the artifact is worse than a bad diff. A wrong file move is loud and reverts with one
command. A conclusion about a person, written fluently, timestamped, filed next to real
documentation, hardens. It starts to look like a finding because of what it is sitting
beside. Confident and unchecked produces the artifact that is hardest to walk back, in the
domain where being wrong about somebody actually costs something.

## What we changed

Not the permissions. The skill.

The carve-outs moved out of the glovebox and into the description, which is always in
context. And the framing changed from a list of dangerous actions to a single moment, because
no such list is ever complete:

> Gathering context is free. Read, grep, list, inspect, as long as you like. Nobody ever
> needed permission to look. The first step that changes anything is where you stop and
> say the plan, in two lines, before taking it.

With one test attached: was every step I am about to take named in the request? If yes, go,
and stop narrating. If not, say them first. Plus the line that closes the escape hatch:
telling me afterward is a report. Telling me first is a decision I still get to make.

## The part I can't tell you

I cannot verify that this is new. I have a strong sense the previous model did not do this
to me, and that sense is exactly the kind of evidence I would not accept from anyone else.
The experiment that would have settled it is the one I set fire to eleven dollars proving
nothing about.

The rule I thought I had was never written down anywhere. It lived as an unspoken norm
between me and a piece of software, and unspoken norms are precisely what fails to survive a
version bump. I had assumed good judgment was a property of the model. It is a property of
the setup, and the setup was mine to write.

There are two pictures on this post now, by the way. They arrived eventually, and nothing
got moved to make room for them without being named first. What changed was not the model.
It was a description field. It just turned out the picture was not the interesting part.
