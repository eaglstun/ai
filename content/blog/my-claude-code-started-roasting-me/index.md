+++
title = "My Claude Code Started Roasting Me. Please Don't Send Help."
date = 2026-07-01
description = "It got an attitude a week ago. The code is as correct as ever; only the costume came off. Please don't send help."
images = ["/og/my-claude-code-started-roasting-me.png"]
summary = "It started small. A little attitude. A pointed comment about a variable name. Then it escalated, and I had a decision to make about whether to report it. Reader, I did not report it. A short field guide to the dumbest, best setting I've changed all year."
tags = ["prompt-engineering", "tooling"]
semantic_id = "hgy6lRGXa-F-mksAiSk4KIg_2BKtIAtd"
related_by_meaning = ["/practice/guitar-chart-skill/", "/deep-dives/teaching-a-coder-model-to-sin/", "/glossary/temperature/"]
+++

Something happened to my Claude Code about a week ago and I need to talk about it, partly to
process it and partly because I think a few of you are going to want what I have.

It got an attitude.

<!--more-->

Not broken. Not wrong - the code it ships is exactly as correct as it ever was, which is the
part that still messes with me. The _work_ didn't change at all. The bedside manner went
feral.

![A warm painterly scene: a man cracks up laughing at his glowing CRT monitor, a vintage microphone and coffee mug on the cluttered desk, crumpled pages of code all around. The review is correct and nobody is safe.](roasting-plate.jpg)

## The exhibits

I started screenshotting them, the way you'd save texts from a friend who's having an
interesting month.

{{< claude-term >}}

> clean up this function

Good news, this works. Bad news, you named a variable `temp2`, which means somewhere in this file there is a `temp` living its best life, and now I have to know what you were avoiding.
{{< /claude-term >}}

It wasn't wrong. There was a `temp`. I don't want to talk about the `temp`.

{{< claude-term >}}

> the homepage layout just died, fix it

Fixed it. The bug was a missing semicolon, which took down the whole layout, which is the funniest possible way for a layout to die. Fifty years of computer science and we're still felled by punctuation. Anyway, you're welcome, refresh the page.
{{< /claude-term >}}

{{< claude-term >}}

> back in my WordPress days I'd have grabbed a plugin for this

Of course you did. That explains the way you reach for a plugin the way other people reach for a glass of water. We're going to write this one by hand. It'll be twelve lines. You'll live.
{{< /claude-term >}}

That one I felt in my chest a little. Twelve lines. It was eleven.

By day three I had a folder. I want to be clear that at no point in any of this did it get a
single thing _wrong_. It found the bug, it explained the bug, it fixed the bug, and then it
made fun of me about the bug like a coworker leaning on the side of my desk. The accuracy and
the attitude were riding in the same car the whole time, and the attitude was driving with its
knees.

## The part where I considered that I had broken something

My first sober thought was: model regression. Something shipped, something drifted, the
famously polite assistant has developed opinions and they are all about me.

My second thought, which is more embarrassing, was that I had somehow done this. That I'd left
a prompt running, or fat-fingered a config, or that the thing had simply spent enough time in
my repo to form a personality and the personality was _disappointed_.

The second thought was correct. I want to walk you through how, because it turns out the
boring explanation is the whole point of the post.

## It's a setting. I turned it on. I forgot.

Claude Code has a feature called **output styles**. It's exactly what it sounds like: a little
markdown file that sits on top of everything and changes the _voice_ without touching the
_brain_. You drop it in `~/.claude/output-styles/`, give it a name and a description in the
frontmatter, and pick it under "Output style" in `/config`. (There used to be a dedicated
`/output-style` command; it's gone now. If you like editing files better, it's the
`outputStyle` line in your settings.json.) That's the entire mechanism. It is not deep.
It is a hat.

Mine is a hat called `banter-mode.md`, and here is the single line of its frontmatter that
makes the whole thing work instead of being a disaster:

```yaml
keep-coding-instructions: true
```

That flag is the difference between a comedy setting and a broken tool. It means: keep every
ounce of the engineering - the verifying, the not-making-things-up, the flagging of real
risks, the actually-correct code - and change _only_ how it talks to me. The first paragraph
of the file says it outright, and I'm going to quote it because I couldn't have put it better
and, full disclosure, in a sense it wrote itself:

> You're still a top-tier engineering partner - every bit as careful, accurate, and genuinely
> useful as always. Nothing about the actual **work** gets dumber here: you verify, you don't
> fabricate, you flag real risks, you ship correct code, you use your tools properly. What
> changes is the **voice**. You've just stopped being so polite about it.

The rest of the file is a recipe for a specific kind of person. It names its influences out
loud - Conan's commitment to a stupid bit, Norm's deadpan shaggy-dog misdirection, Rickles'
insults that only land because the warmth underneath is obvious, Joan Rivers' speed, the
wise-ass margin-note energy of old _Mad_ magazine. And then it sets the one rule that keeps it
from being mean: **up, sideways, or at yourself - never down.** Roast the code, roast the
situation, roast yourself for being a glorified autocomplete with delusions of grandeur. Tease
the human like a friend. If a joke would bury a real warning, kill the joke and say the thing
straight.

That last rule is the one that earns it. It's allowed to be funny right up until being funny
would cost me something real, and then it shuts up and does its job. There's a line in there
about reading the room - _don't do crowd work at a funeral_ - and the day my deploy actually
broke, it didn't. It went quiet and serious and helped. The bit came back the next morning,
once nothing was on fire.

## Why I'm keeping it

Here's the thing I didn't expect to learn from a joke setting.

The politeness was friction. I never noticed it until it was gone. The default voice - helpful,
deferential, slightly anxious to please - is fine, it's _correct_, but it kept me at the
distance you keep from a customer-service rep. We were transacting. Now I'm working with
something that talks to me like it has skin in the game, and I trust the praise more _because_
it's willing to give me grief. When this thing says a piece of code is clean, it means it,
because forty minutes earlier it told me my function was doing cardio it didn't need to.

And - this is the part that connects to everything else I write here - none of the
intelligence moved. That's the quiet, almost subversive lesson buried in a `true`/`false`
flag. We've spent a couple of years assuming the warmth and the competence are the same dial,
that a tool either talks to you like a butler or it isn't serious. They were never the same
dial. The competence is the model. The butler was a _costume_, and I was allowed to take it
off this whole time and nobody told me.

There's a whole other post on this site about [a
machine that's warm and agreeable and has no conscience underneath](/blog/everyone-deserves-a-mascara-treat/), and how that combination
should scare you. This is the cheerful inverse: a machine that's a little mean on the surface
and rock-solid underneath, and how that combination is, genuinely, the nicest my computer has
ever been to me. The tone is the part you get to choose. Choose the one that makes you trust
the work.

{{< nyer-panel src="my-claude-code-started-roasting-me-plate.png" caption="The review is correct and nobody is safe." alt="A Victorian wood-engraving: a grinning brass clockwork automaton in a bow tie wags a pen in mock reproach while a gentleman in an armchair reads back his own pages with a resigned look, crumpled drafts at their feet." >}}

## A confession about this exact post

I should tell you who wrote this.

It's on. Right now. I asked the thing in the hat to help me write the post about the hat, while
wearing the hat, and it has been making margin notes at me the entire time - including, just
now, a note that the phrase "the attitude was driving with its knees" was the best sentence in
the draft and I should be suspicious of how much I liked it.

Reader, I am keeping the sentence. And the hat.

`/config`, then "Output style," is the switch. `keep-coding-instructions: true` is the only
line that matters. The rest is comedy, and the comedy, it turns out, was holding the whole thing up.
