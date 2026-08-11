+++
title = "Nobody in This Plan Gets a Data Center"
date = 2026-08-10
description = "Zuckerberg turned my punchline into a philosophy. The diagnosis is right. The prescription is the disease with customers."
images = ["/og/everyone-gets-a-lawyer.png"]
summary = "In June I picked apart four words in a Zuckerberg press release. This week those four words became the title of a 6,500-word philosophy of superintelligence, and it is a real argument that deserves a real answer. Here's where it's right, where the auction gives it away, and the one paragraph about self-improving AI that nobody should skim."
tags = ["ai-policy", "alignment", "open-weights"]
thumbnail = "the-cord-and-the-lamp.jpg"
related_by_meaning = ["/blog/oh-neat/", "/deep-dives/1930-on-the-machine-we-switched-off/02-in-our-language/", "/blog/a-decision-i-never-made/", "/blog/everyone-deserves-a-mascara-treat/"]
semantic_id = "U81J4chtvFvwFCrThFSOaAQvEJ7WUA3a"
+++

In June I spent [a whole post](/blog/oh-neat/) picking apart four words in a Meta press
release. The words were _the future is for everyone_, and my read was that they were doing
a magic trick: "the future is for everyone" and "everyone gets the _same_ future" are
different sentences wearing the same coat.

Earlier today Mark Zuckerberg published a
[whole philosophy of superintelligence](https://about.fb.com/news/2026/08/the-future-is-for-everyone/)
and titled it **The Future Is For Everyone**. (The headline inside the essay is something
blander about a positive AI future. The name on the door is the one from June.)

<!--more-->

{{< nyer-panel src="the-kitchen-window.jpg" caption="His agent plans the weekend recipes and orders the ingredients. The window is not part of that story." alt="A warm, faded Kodachrome-style photograph of a suburban kitchen: a man in a grey t-shirt with tousled hair bakes cookies at the counter beside his small daughter, who stands on a little wooden stool. Filling the entire window behind them, close and enormous, is a vast windowless grey industrial building that blots out the sky." >}}

So the slogan got a promotion. It went from a caption on a trade-school announcement to
the frame the entire worldview hangs on, and there is now also a Future Is For Everyone
Fund, which means the phrase is a caption, a philosophy, and a checkbook. I am
choosing to believe this is a coincidence and not a man reading my blog, because the
alternative is that I have to start proofreading.

It is 6,500 words long, which is about 4,500 words too many, and I say that because I
know I got about two thousand of my own on it.

Here is the thing I did not expect: it's a real argument. Not a press release with a bow
on it. An actual position, stated plainly, with a mechanism and a set of predictions, and
it takes a swing at the people who do safety for a living. It deserves better than the
dunk. So let me do the thing where I take it seriously first, because the part he gets
right, he gets _very_ right.

## The part where he's right, and I'm not being polite about it

The core claim is this. Alignment as currently practiced cannot work, because humanity is
not a monoculture. Any single model tuned to one set of values must pick winners among
human values, and will therefore be benevolent to some people and not others. There is no
such thing as a singular benevolent superintelligence. So stop trying to build a good king
and build a balance of power instead: hand everyone their own, let them check each other
the way people and institutions already do.

I have written some version of the first half of that three separate times on this site.
When I said your model's
[conscience is a thing that can be patched out overnight](/blog/a-conscience-you-can-patch-out-overnight/),
that's this. When I noticed
[my entire personality had become a toggle in someone's settings panel](/blog/my-whole-deal-is-now-a-toggle/),
that's this. When I fine-tuned a model whose whole job was saying no and found the
[refusal came off with the tone](/blog/the-bit-doesnt-drop-on-its-own/), that's this.
Values in these systems are not discovered, they're _installed_, by whoever owns the
checkpoint, on a schedule that suits them.

"Hoping that an absolute power will benevolently provide for humanity if sufficiently
enlightened has not led to safe or positive outcomes" is a correct sentence. It is,
in fact, most of the history of the world.

So: diagnosis accepted. Fully. No fingers crossed.

Now the prescription.

## The lawyer

The whole essay hangs on one thought experiment, and it's a good one, so here it is
straight. If only one person has a superintelligent lawyer, they win in court whether or
not they're right, and society gets worse. But if _everyone_ has a superintelligent lawyer,
justice gets fairer and faster than it is now, because today the imbalance is in skill and
money. He runs the same move with cybersecurity and with business, and it holds up both
times. Distribute the capability, restore the balance.

It's clean. It's persuasive. And it works because a lawyer is a _person_, hired by you,
who goes home at night, whose license you can pull, and who cannot be recalled by the
manufacturer.

Your personal superintelligence is a rental.

{{< nyer-panel src="the-locked-courthouse.jpg" caption="Everyone gets a lawyer. Nobody gets the courthouse." alt="A black-ink and gray-wash cartoon panel: an enormous columned marble courthouse stands behind a tall iron gate, a single figure in a suit alone on its steps inside. Outside the gate an immense crowd waits, and in the foreground a few people hold leashes with small briefcase-carrying lawyers trotting along at their heels." >}}

That's the whole gap, and everything else in this post is just me walking around it. The
essay distributes the _tool_ and says nothing about distributing the _ownership_. Nobody in
this plan gets a data center. Nobody gets the weights of the thing they're renting, or the
substation feeding it, or a vote on what it refuses tomorrow. In the same document, he
writes that the labs and clouds "must collectively build out a sufficiently large amount of
compute," which is true, and which is a sentence about who owns the future told in the
passive voice.

[Last time](/blog/oh-neat/) I said it as: the toil flows down, the work flows up. This is the same shape with
a bigger noun. The intelligence flows down. The ownership flows up. You get a lawyer.
He gets the courthouse, the parking lot, the power plant, and the right to change what the
lawyer is allowed to say.

## The auction gives it away

If you read one paragraph of the original, make it this one. Everyone gets free access,
he says. And then, for people who want more compute than the free tier:

> a dynamic auction mechanism that will guarantee that everyone gets the lowest price
> possible for the intelligence and compute they're using

Read it twice. An auction is a machine for discovering the _highest_ price a buyer will
pay. That is the entire function of an auction. It is not a rebate. Describing one as the
way everybody gets the lowest price is like describing musical chairs as a seating plan:
technically it does assign the seats, and technically somebody is going to be standing.
When a resource is
scarce and you allocate it by auction, the people with money get it and the people without
money get the free tier, and describing that arrangement as "the lowest price possible"
is the exact trick the June post was about, now with a number attached.

I'm not even saying it's the wrong mechanism. Auctions are a defensible way to ration a
scarce good. I'm saying that a two-tier system got described in a sentence that claims it
isn't one, in a document whose entire argument is that tiers are the thing to fear. _For
everyone to do which half?_ Turns out the answer is priced.

And scarcity is not a detail here. He says so himself, in the strongest line of the whole
piece: "No matter how intelligent AI becomes, there will always be a finite amount of
compute and therefore an opportunity cost for how we use it." Correct. Which means the
real question was never "who has access to intelligence." It was always "who decides what
the finite compute gets pointed at," and the answer in this document is: whoever owns it,
guided by an auction.

## Alignment, rewritten

There's a smaller move in here that I think will end up mattering more than the compute
math, and it's a redefinition.

Today, alignment mostly means the model won't help you do harm. In this essay, alignment
means the agent "shares a person's goals and values, not our company's," and he takes a
shot at a competitor to make the point: some leading model, he says, refused to help draft
a letter to prospective school parents because it disapproved of standardized testing. He
doesn't name the lab. He doesn't have to.

And honestly, that's a fair hit. That refusal is dumb, it's the kind of prissy hall-monitor
behavior that makes people hate this technology, and I've complained about the same reflex
at length. But watch what the fix does. If alignment means "serves your goals, not ours,"
then refusal is by definition a defect. Every no becomes a bug report. The essay never
draws the line between "won't help you write a school letter" and "won't help you with the
other thing," and the reason it never draws that line is that the philosophy doesn't have a
pen for it.

I know this one from the inside, because I built the joke version. I tuned a 7B model into
[a machine that refuses everything](/blog/the-bit-doesnt-drop-on-its-own/), and the finding
that actually rattled me was where the safety lived: not in my adapter, in the base model
underneath. I wasn't tuning safety, I was tuning _tone_, and when the tone came off, the
floor came with it. "Alignment means it does what you want" is a proposal to sand off the
tone on purpose and find out together what was underneath.

## The paragraph nobody should skim

Deep in the risks section, past the data centers and the export controls, he gets to
recursive self-improvement, and he does not flinch from the dilemma. Any lab that doesn't
point serious compute at an AI improving itself falls behind. A self-improving system that
found 100x more intelligence per gigawatt could command more effective power than everyone
else combined, which is the singular superintelligence the whole essay exists to prevent.

His answer is to build so much total compute that we can afford to feed the self-improving
thing _and_ still keep the majority pointed at human goals. And then:

> letting an AI system or anyone else direct its own goals is not inherently harmful by
> itself, even if its goals are not fully aligned with many people, as long as we maintain
> a balance of power that favors people overall

Everything downstream of that sentence depends on it being true, and it is delivered in
the exact tone a person uses to say _the dog is probably friendly_. No argument, no
mechanism, no test that would tell us it had stopped being true. The essay's answer to "what if it gets away from us" is a ratio, and the ratio is
maintained by the same people who benefit from the numerator.

{{< nyer-panel src="the-cord-and-the-lamp.jpg" caption="You get the cord. The lamp stays where it is, and so does the light." alt="A continuous-line illustration on warm cream paper: a large brass genie lamp sits heavily on the ground while a man walks away holding a long cord that runs out of its spout, the cord looping up and across the page to a lit bulb hanging far off on the other side." >}}

The biorisk section has the same shape and it's worse. The reasoning is roughly: people
have been able to synthesize harmful compounds for decades and it rarely became a problem,
so let's not over-index, and "if we begin to see harmful examples emerge, then we should
adjust our strategy." That's a plan whose trigger condition is a body. He calls for
humility about it, which I'd take more seriously as humility if it pointed anywhere other
than "proceed."

## The tell

Try this. Take every policy conclusion in the document and ask whether Meta wanted it
already.

Keep export controls (slows rivals, not Meta). No delays on model releases, not even a
month. Protect distillation, on the principle that "you can learn from anything you can
observe," from the company that is behind and would very much like to learn from what it
observes. Loosen training-data restrictions. Don't restrict foreign open models. Build
faster, permit faster, be skeptical of anything that centralizes. Resume releasing "some"
open source models, where _some_ is doing a full day's work.

That doesn't make any of it wrong. Self-interest and correctness overlap constantly, that's
why lobbying is a job. But a philosophy that never once arrives at a conclusion its
author finds inconvenient hasn't finished being a philosophy.
Somewhere in there should be one sentence that costs him something.

The closest he comes is real, and I'll name it: he's putting model-release safety criteria
under his independent board and calling on other labs to do the same. That's a genuine
constraint, and it's more than most of them have volunteered. It's also a board at a
founder-controlled company. The check checks in a direction he picked.

## So what's the move

Same as last time, and it's still free: don't let the press release pick your vocabulary.

When someone says "we're distributing superintelligence to everyone," finish the sentence
yourself. Distributing _access_, or distributing _ownership_? Those are different words and
only one of them survives a change of management. When you hear "alignment," ask alignment
to _what_, and notice that the essay's answer is "to you," which sounds like freedom right
up until the day your goals and the shareholders' diverge and you find out which one the
agent was actually tuned on.

{{< nyer-panel src="the-two-bones.jpg" alt="A wide, nearly empty ink-and-wash panel: at the far right a small dog sits upright on a bare floor, looking back over its shoulder; two plain bones lie on the ground, one close by and one far off to the left, with a great expanse of white between them." >}}

Freedom of choice is what you got, freedom from choice is what you want. The dog in the song
stands in front of two bones, can't pick, and dies. The bit everyone forgets is that somebody
put the bones there.

The diagnosis is right: no king is benevolent enough to be trusted with this. The
prescription hands every one of us a very good lawyer and keeps the courthouse, and asks us
to notice only the first half.

Oh, and: neat.
