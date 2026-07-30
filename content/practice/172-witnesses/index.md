+++
title = "172 Witnesses, Each One Half-Blind"
date = 2026-07-13
description = "My site's search runs on 172 yes-or-no questions. Nobody wrote them. I went looking for what they ask."
summary = "Every page here carries 172 bits that are the meaning of the page, and the search box runs on nothing else. But nobody ever wrote the 172 questions those bits answer. So I interrogated the corpus to find out what they ask, guessed wrong about the answer, and got a better one."
images = ["/og/172-witnesses.png"]
tags = ["search", "embeddings", "latent-space"]
thumbnail = "concepts/172-witnesses/b-replicate-continuous-line.jpg"
semantic_id = "SYSBQbHDrznbRYirwbi5wA5Pial84AwV"
related_by_meaning = ["/search/", "/practice/thirty-comments-nobody-was-meant-to-read/", "/blog/i-got-substituted-on-purpose/", "/blog/nobodys-hands-are-big-enough/"]
+++

{{< nyer-panel src="the-witness-stand.jpg" caption="The star witness, under oath, pointing straight at something he cannot see." alt="A hatched courtroom illustration on cream paper: a witness in a suit stands at the podium wearing a blindfold, one arm raised, pointing confidently across the room, while rows of jurors and spectators look on from the box beside him." >}}

The search box on this site does something I want to be straight about, because the plain
version is stranger than the marketing version.

Every page here carries a 32-character string in its metadata, [this page
included](https://raw.githubusercontent.com/eaglstun/ai/main/content/practice/172-witnesses/index.md).
It is not a name for the page. It is a description of it, written in a language with no words:

```text
ifa9d7QHZ6u-LqLCkgz1Ns6LbHqZYAs9    "The Bill Comes Due"
```

Unpacked, that string is 172 yes-or-no answers, and the unpacking is not a figure of
speech. Base64 is just a denser alphabet: each of those 32 characters is six bits wearing
a single letter, so the whole thing springs open into plain ones and zeros.

```text
i      f      a      9      d      7      Q
100010 011111 011010 111101 011101 111011 010000  (and so on, all 32 letters)
```

Line them up, drop the spaces, and you have 192 bits. The last 20 are housekeeping, a date
stamp and a tiebreaker. The first 172 are the answers:

```text
1000100111110110101111010111011110110100000001110110011110101011101111100010111010100010110000101001001000001100111101010011011011001110100010110110110001111010100110010110
```

Two pages about the same thing come out
with answers that disagree in only a few places, which means "what else is like this"
stops being a question you need a search company to answer and becomes counting. That is
the whole trick, and the entire search feature is a few kilobytes of these strings and
some arithmetic your browser does before your finger leaves the key.

So a reasonable person asks the obvious follow-up, and I did too: **what are the 172
questions?**

## Nobody wrote the questions

This is the first thing I got wrong, and it took the machine about nine seconds to correct
me.

There is no list. Nobody sat down and decided that bit 12 asks "is this about GPUs" and bit
90 asks "is the author being smug again." Each bit is one axis of a language model's
768-dimensional read of the page, and the question it asks is precisely this:

> Is this page above the corpus average on axis number 37?

That's it. That's the question. Axis number 37 was not designed, was not named, and does
not correspond to anything a human being chose. It fell out of the model's training on a
pile of text that has nothing to do with me, and it was sitting there, unnamed, before this
website existed.

Which sounds like a dead end. It is not a dead end. You can't ask the questions what they
mean, but you can watch how they answer, and that turns out to be a different and much
better kind of interview.

## Every one of them is a live question

Before reading them, a sanity check, and this one matters in a way I did not
appreciate until I saw the number.

Binarizing is `sign(v - mean)`: each bit is "is this page above **average**," and the
average is a frozen reference point computed once from the corpus and never touched again.
Skip that centering, ask "is this page above **zero**," and you get bits where every single
page answers the same way. A question the whole corpus answers identically is not a
question. It is a formality. It is the census asking whether you are currently alive.

So I counted. Across 77 pages and 172 bits:

- **Dead bits, where every page answers the same:** zero.
- **Near-dead, where fewer than four pages take the minority side:** zero.
- **Median bit:** says yes for 51% of pages.

Every question is a coin flip somebody actually has to think about. Nothing is wasted. That
is the frozen average doing its job, silently, in a way that produces no error message when
you get it wrong, which is why I now treat that one file like a family heirloom.

## Reading the questions backwards

Here's the interview technique. You can't ask a bit what it wants. But you can take all the
pages that answered **yes**, put them in one pile, put the **no** pile next to it, and walk
around the two piles asking what everyone in each one has in common.

Do that and the site's own fault lines come up out of the floor:

| bit | a "yes" leans toward                | a "no" leans toward                   |
| --- | ----------------------------------- | ------------------------------------- |
| 68  | training, alignment, tooling        | apple-silicon, metal, local-inference |
| 19  | apple-silicon, metal, mps           | training, ai-safety, alignment        |
| 169 | ai-safety, alignment, ai-policy     | apple-silicon, metal, inference       |
| 13  | essays                              | glossary entries                      |
| 101 | quantization, precision, parameters | consciousness, gpt, temperature       |

The same crack keeps opening, in both directions, under bit after bit: **the machine on one
side, the mind on the other.** Metal and MPS and GGUF and getting a model to run on a
laptop over here. Alignment and policy and consciousness over there. That is the largest
single division in everything I have written on this site, and I never told it that. It
went looking through my pages and found the two things I cannot stop arguing with each
other about.

Bit 13 is doing something else, and I have developed real affection for it: it has
independently worked out the difference between an essay and a dictionary entry. Not the
topic. The _register_. It can hear when I stop performing and start defining.

And bit 101 has wandered off from the whole fight. It splits the site on _numbers versus
behavior_: on one side the pages about how the weights are stored and shrunk, quantization
and precision and how many parameters you can afford to keep; on the other, the pages about
what the model does once it runs, its voice, its temperature, whether anyone is home.
Storage on one side, personality on the other. And it barely votes with the
machine-versus-mind bits at all. Line up two bits and measure how often they point the same
way, on a scale where 1.0 is perfect lockstep, one bit a redundant copy of the other, and 0
is no relationship whatsoever: bit 101 against bits 68, 19, and 169 lands at 0.08. Call it
zero. A different witness, looking at a different thing.

## The part where I was wrong, again

Look at that table and you will believe, as I did, that those bits are redundant. Bits 68
and 19 and 169 are obviously the same question wearing different hats, and 172 of them is
therefore extravagant, and a tidy dozen labeled features would do the same work.

I went to prove that. It is false.

The most correlated **pair** of bits in the entire 172 sits at 0.51 on that same scale: even
the two most alike lean together only about half the time, nowhere near lockstep. Out of all
14,706 possible pairs, **not one** passes 0.7, the line where you would fairly start calling
two bits near-twins. They are not copies. They are 172 genuinely
different questions that happen to lean the same way on the biggest split in the corpus,
the way a room full of people can all lean left without agreeing on a single thing.

And that is the actual answer to the question I started with.

**No bit means "is this about Apple Silicon."** Not one of them. Every bit is a weak, noisy,
half-blind vote on some direction nobody can name, and the meaning does not live in any of
them. It lives in the _agreement between them_. Which is why you cannot shrink this to
twelve tidy labeled features, and why the distance function has to count all 172 every
time: it is the difference between one witness who is certain and a hundred and seventy-two
who each caught a glimpse out of the corner of an eye.

Ask any one of them what they saw and you get a shrug. Ask all of them at once and you get
a description.

## Why the search finds pages that never say the word

Which brings it back around to the box at the top of the site.

Type "conscience" and you get the two essays that use the word, and then you get an essay
about a chatbot that never uses it once, and a glossary entry on model welfare that
certainly doesn't. Nothing in that result matched your text. A hundred and seventy-two
half-blind witnesses simply agreed that those pages are describing the same thing you are.

There is one hard limit and I would rather say it than have you find it. Turning _your_
typed words into bits would need the same model that made them, and that model is 130
megabytes sitting on my laptop. It is not coming to either your phone or my $6/month server.
So the typing does a plain, dumb word match to find the page nearest what you asked for, and the bits take it from there. The word is the seed. The arithmetic is the search.

## The fine print

Everything I just told you about bits 68 and 19 and 13 is a story I told over 77 pages,
which is not a lot of pages. The fault line is real and shows up under any bit you poke.
The names I gave it are decoration, and if you double the size of this site some of my
tidier labels will quietly stop being true.

The bits will not care. They were never asking my questions in the first place.
