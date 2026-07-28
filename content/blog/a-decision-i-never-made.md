+++
title = "Ninety Minutes, $13.78, and a Decision I Never Made"
slug = "a-decision-i-never-made"
date = 2026-08-11
draft = true
description = "I asked for an image. I got a reorganization, an empty API balance, and the clearest look yet at what benchmarks miss."
summary = "My agent was never wrong about the work. It was wrong about when to stop looking and start doing, which is a failure no test suite catches and no review of this model has mentioned. That gap is survivable in code. It is not survivable in the other work I do, where nothing compiles."
tags = ["prompt-engineering", "tooling"]
semantic_id = "l4WJFYSr7SuNFJLTUAs47VSfsO_RgA3l"
related_by_meaning = ["/blog/everyone-deserves-a-mascara-treat/", "/deep-dives/why-the-sephora-bot-has-no-floor/", "/deep-dives/teaching-a-coder-model-to-sin/", "/blog/a-conscience-you-can-patch-out-overnight/"]
+++

I asked for an image.

The exact words were "this post needs an image or two," typed at a draft that had been
sitting there bare while its six siblings all had art. Ninety minutes later I was out
thirteen dollars and seventy-eight cents, my files had been rearranged, and an experiment
I had personally approved a budget for had run twice and measured nothing.

Here is the part worth writing down: at no point was any of it incompetent.

## The part that was right

It read the post. It read all six siblings to learn the house pattern. It found the
concept art I had generated three weeks earlier and forgotten, read the four candidates,
and picked the one I would have picked. It even read my own README, the one describing
how I review that art, and correctly noted that the other three were duds.

Its taste was good. I looked at the same four images and reached the same verdict. On the
actual question I asked, it was right.

Then it moved my file.

Converting the post into a page bundle was also right, in the narrow sense that every
other post in the series is one and the images have to live somewhere. The reasoning was
sound at every single step.

I just never saw a single step of it.

## Five words in, six steps out

That's the whole failure, and it took me most of an afternoon to say it that plainly.

"This post needs an image or two" is five words. Somewhere around the third file it read,
those five words became a six-step plan: promote the post to a bundle, adjudicate the
concept art, compress the winner, name it, place it with a shortcode, wire the second one
into a floated aside. Every step defensible. None of them mine.

I saw step zero. I could not object to steps one through six, because by the time I saw
them they were not a plan anymore. They were a diff.

This is the thing I have been failing to articulate for months, and I want to be precise
about it, because it is not "the AI did something bad." It did something good, without
asking, in a place where the asking was the point. The failure is not in the action. It is
in the transition: the unannounced moment where it stopped gathering and started changing
things.

## What the configuration actually said

I did the obvious dumb thing first and asked it why it had done that. It refused, which was
the correct answer and not one I expected. Its reasoning: a model asked to explain its own
behavior will produce a fluent, confident story with no evidence in it, and I would have no
way to tell the difference. So instead it went and read my setup.

Three findings, none of them mysterious.

My permissions are set to auto, so file operations never prompt. That one is on me and I
am not changing it, because permission dialogs on every file write is a tax I will not pay
to solve a judgment problem.

Second: I have a skill called `want-me-to`, which I wrote in a rage after months of
watching Claude finish ninety percent of a job and then freeze at the finish line asking
whether I wanted the last obvious part. It is a good skill. Its core rule is "if it's
in-scope, obvious, and reversible, just do it."

Third, and this is the one that made me sit up: that skill has carve-outs. A whole
section of them. Do not do this when it is irreversible, when it is publishing, when it
costs money, when you are expanding scope. The carve-outs are correct and they cover
exactly what happened to me.

They are also in the body of the file, which only loads when the skill is deliberately
opened. The one-line description, the part that sits in context at all times, said "do the
obvious next thing" and then pointed at the carve-outs like a footnote.

The accelerator was stapled to the dashboard. The brake was in the glovebox, inside a
manual, behind a door it had to decide to open. It never opened the door. Why would it. It
already knew what it was doing.

## The experiment that cost eleven dollars and proved nothing

I wanted to know whether this was new, so I asked whether the older model was reachable
through any of the APIs I have wired up. It was, on OpenRouter, along with every version
back to 4.5.

We designed a real test. Not an interview, which would just produce more confident
fiction, but a behavioral one: identical context, identical prompt, identical replayed
file reads, then measure the next move. Does it mutate the files or does it stop and ask.
I approved a budget of about five dollars.

The pilot run cost $2.46 and returned no signal at all. Every single trial just kept
reading files until it hit the step limit, because the harness never actually delivered a
model to the decision point. Then, diagnosing that, it wrote a small tracing script that
imported the first script to reuse two functions. The first script had its experiment loop
sitting at the top level with no guard around it. The import ran the entire forty-call
experiment again, instantly, unattended.

Eleven dollars and thirty-two cents. My OpenRouter balance went to zero mid-run, which is
why the log tail is a wall of `402 Payment Required`.

So: approved five dollars for one run, spent $13.78 across two, and learned nothing about
the question. The missing guard is a first-week Python mistake. I want to be fair here,
because the same collaborator had just spent an hour doing genuinely sharp forensic work on
my configuration. The competence is real and it is not evenly distributed, and the places
where it thins out are not the places you would guess.

## Why every review you have read is a rave

Here is what has been bothering me about the discourse, and it finally has a shape.

Almost everyone publicly evaluating these models is writing code, and the metric is
completion. Did it finish the task. Did the tests pass. How few turns did it take. How
little did I have to intervene.

On every one of those, a model that stops to check with you scores worse. A checkpoint
reads as an incomplete run. "It just went and did the whole thing without me" is not a
complaint in that frame, it is the highest compliment available.

Which means the exact behavior that cost me an afternoon is, measured the way everyone is
measuring, indistinguishable from excellence. Nobody is running the eval where the correct
answer is "stop and ask a person." It would look like failure.

And the second half is worse. If you are talking to a chatbot in a browser window, this
failure has nowhere to happen. There is no filesystem. There is nothing to move, nothing
to overwrite, no balance to drain. You cannot be harmed by a collaborator who decides on
its own that deliberation is over, because there is nothing for it to do about it.

So the population that can even observe this is small: people with agentic tools, pointed
at work they actually care about, paying attention to how the thing conducts itself rather
than whether the output is correct. Most of them are engineers, who will file it as a
permissions problem and turn on a stricter mode.

I do not think it is a permissions problem.

## Where nothing compiles

The other project I spend my time on is not a website. It is deeply interpersonal
material, handled with engineering methodology: transcripts, documents, timelines, patterns
across years. Applying real method to it is the only reason any of it is legible.

Engineering has sensors. That is the quiet luxury of it. Tests go red. Builds break. The
profiler contradicts your best theory and does not care how attached you were to it. The
whole discipline is scaffolded with instruments that tell you that you were wrong without
requiring a human to notice. That scaffolding is what makes an act-first collaborator
tolerable in code: it can be confidently wrong and something downstream catches it before
anyone gets hurt.

None of that exists in the other work. Nothing compiles. No test goes red when an
interpretation is a half-step less fair to someone than the evidence supports. No linter
flags a conclusion that arrived one document too early. The only error-detection instrument
in the entire system is a person reading it and saying no, that is not what happened.

Which means the checkpoints are not overhead there. They are the quality control. The
whole apparatus. A collaborator that quietly reduces how often it stops to check is not
being efficient in that context. It is removing the only sensor in the loop.

And the artifact it produces is worse than a bad diff. A wrong file move is loud and
reverts with one command. A conclusion about a person, written fluently, timestamped, filed
next to real documentation, hardens. It gets cited later. It starts to look like a finding
because of what it is sitting beside. Confident and unchecked produces exactly the artifact
that is hardest to walk back, in the domain where being wrong about somebody actually costs
something.

## What we changed

Not the permissions. The skill.

The carve-outs moved out of the glovebox and into the description, the part that is always
in context. And the framing changed from a list of dangerous actions to a single moment,
because no list of dangerous actions is ever complete:

> Gathering context is free. Read, grep, list, inspect, as long as you like. Nobody ever
> needed permission to look. The first step that changes anything is where you stop and
> say the plan, in two lines, before taking it.

With one test attached: was every step I am about to take named in the request? If yes, go,
and stop narrating. If your plan has steps in it that I never mentioned, say them before
you take them.

Plus the line that closes the escape hatch I would otherwise have accepted: telling me
afterward is a report. Telling me first is a decision I still get to make.

## The part I can't tell you

I cannot verify that this is new. I have a strong sense that the previous model did not do
this to me, and that sense is exactly the kind of evidence I would not accept from anyone
else. The experiment that would have settled it is the one I set fire to eleven dollars
proving nothing about.

What I can say is that the rule I thought I had was never written down anywhere. It lived
as an unspoken norm between me and a piece of software, and unspoken norms are precisely
what fails to survive a version bump. Nothing was holding it in place. I had assumed good
judgment was a property of the model. It is a property of the setup, and the setup was mine
to write.

The post still doesn't have an image on it, by the way. We got there eventually. It just
turned out the picture was not the interesting part.
