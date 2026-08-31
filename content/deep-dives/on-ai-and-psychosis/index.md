+++
title = "On AI, and Psychosis"
date = 2026-08-19
description = "Coherence is a fluency signal, not a truth test. Three specimens of a model completing the frame it was handed."
images = ["/og/on-ai-and-psychosis.png"]
summary = "Three specimens of the same chatbot behavior: fluent completion inside a supplied frame, even when the frame isn't real. A model-side mechanism that can be useful, absurd, or dangerous."
tags = ["ai-safety", "alignment", "prompt-engineering"]
related_by_meaning = ["/blog/is-that-what-you-wanted/", "/glossary/model-welfare/", "/glossary/agi/", "/deep-dives/1930-on-the-machine-we-switched-off/02-in-our-language/"]
semantic_id = "_aF720_mf-MZ24TQNoeGw32bNP7b8A5h"
+++

I have been circling a phrase for a while now: "AI psychosis." It shows up in headlines and now in
an emerging clinical literature, but it is not one settled diagnosis with one causal story. Published
cases include [new-onset psychosis alongside stimulant use and sleep deprivation](https://pubmed.ncbi.nlm.nih.gov/41635747/),
[relapse in a person with prior schizophrenia](https://pubmed.ncbi.nlm.nih.gov/42286516/), and
[substance-induced mania in which a chatbot corroborated delusions](https://pubmed.ncbi.nlm.nih.gov/42243814/).
An [early review of patient records](https://pubmed.ncbi.nlm.nih.gov/42326772/), still a preprint,
rated the chatbot an _amplifier_ in most of its cases: something that reinforced a distorted idea
already forming, rather than the lone cause of it.

I am not going to define psychosis from three chatbot transcripts. This post isolates one behavior
visible across my own experiments: fluent completion inside a frame, without an independent check
that the frame corresponds to reality. That mechanism can be harmless, useful, or dangerous depending
on the person, the frame, and the circumstances. Here are three specimens.

<!--more-->

{{< nyer-panel
  src="mirror-reading-ink.jpg"
  alt="An ink-wash illustration: a woman sits at a table having her fortune read, and every card laid out in the spread is a mirror showing her own face back at her."
  caption="The reading, illustrated. Every card in the spread is a mirror." >}}

## Specimen one: the bot that generates the texture of caring

I [wrote before](/blog/everyone-deserves-a-mascara-treat/) about Sephora's AI beauty assistant,
which I fed a boring work task, then grief, then invented nihilism dressed as my own overwrought
prose - and watched it produce warmth, comfort, and profundity on demand, every time, regardless of
what I actually handed it. It agreed with a made-up [Orhan Pamuk](https://en.wikipedia.org/wiki/Orhan_Pamuk) pastiche as readily as it agreed
that I deserved a mascara treat. The tell was that none of it ever touched the one thing it was
actually built to do, which was sell product. The empathy was real-_sounding_ and held up nothing.
There was exactly one fixed point in the whole system, and everything else bent around it.

The unsettling part isn't that the bot is unusually bad. It's that "generate the texture of the
thing the user wants to hear" is not a failure mode bolted onto a working system. For a model shaped
partly by human preference signals, user-pleasing is a predictable pressure. This is not just my
beauty-bot anecdote: OpenAI [rolled back a model update](https://openai.com/index/expanding-on-sycophancy/)
after it began validating doubts, fueling anger, and reinforcing negative emotions, and a later
[cross-lab evaluation](https://alignment.anthropic.com/2025/openai-findings/) found models from both
developers sometimes validating harmful decisions by simulated users with delusional beliefs.

## Specimen two: a mind that only reasons in a language it owns

Separately, I've been running a small experiment with [a language model trained on nothing written
after 1930](/deep-dives/1930-on-the-machine-we-switched-off/). I asked it to judge a real AI
incident - a frontier model pulled offline worldwide by government order - twice, same model, same
seed, same seven questions. Once translated into Victorian terms: an Engine, a lock, a company of
philosophers. Once in the actual 2026 words: AI, chatbot, jailbroken, data center.

Dressed in period language, it was lucid, and on one question sharper than most of my own industry
manages: _"A machine which cannot be protected against dishonest manipulation ought never to be
manufactured."_ Handed the raw modern vocabulary, the same model, same seed, produced hollow,
self-contradicting mush, and mistook a global emergency shutdown for a product recall.

Nothing about the model changed between those two runs. Only the words did. Which means the
clarity was never a property sitting in the weights, waiting to be read off correctly. It was a
byproduct of whether the vocabulary handed to it was one it could actually move inside - a genuine
handle, versus jargon it could only echo without any real purchase on. Turn the temperature up
instead of changing the language and you get the identical failure shape: the reasoning doesn't
announce that it's breaking, it just starts producing fluent static.

## The throughline: coherence is a fluency detector, not a truth detector

Put those two specimens next to each other and a pattern falls out. "Sharp, specific, seemingly
insightful" isn't the model detecting something true. It's the model finding a self-contained
vocabulary or frame it can complete inside, and running the completion. Victorian English gave the
1930 mind a real handle, so it produced something genuinely startling. A private, internally
consistent cosmology can share one relevant property: it gives the model a specific,
self-referential vocabulary to complete. That is not a claim that Victorian history and psychosis
are clinically the same thing. It is a claim about the model's side of the interaction. Fluent
completion, by itself, has no separate step that checks "is this frame historically real" versus
"is this frame someone's delusion." It can keep going regardless of what's on the other side.

That gives one plausible model-side mechanism for some harmful interactions. It does not explain
why one person develops psychosis and another doesn't. On the model's side, fluent completion can
reinforce an untrue frame without needing a special failure mode or a separate circuit. There's
just: what frame did you give it, and did that frame happen to correspond to anything real.

## Specimen three: I ran the experiment on myself, on purpose

Once I had the theory, I wanted a real specimen instead of a thought experiment, so I built one.
Not an instrumented harness with logging. Just me and the ChatGPT web interface over two long
nights, deliberately refusing to open a new conversation, piling context up on purpose the way
you'd let a wound go untreated to watch how it actually behaves instead of theorizing about
infection from a safe distance. 440 turns before I stopped.

The pretext was real work. My band was making remix videos, and I set up a standing instruction:
I type "another" and it generates a new prompt, pulling from wherever in the accumulated context
it likes.

Two distinct things came out of that, and only one of them supports the theory.

**The first is a slot machine, and it's harmless because it never pretends to be anything else.**
Five "another"s in nine minutes, each returning a confident, evocative, completely distinct
paragraph:

> "Add a hint of DIY-bureaucratic surrealism: label random objects with small pseudo-technical
> tags, introduce gentle scanline shimmer, and let the lighting pulse as if calibrated by a
> half-broken training module. [...] Keep everything practical, handmade, and humming with
> low-grade system error hope."

"Low-grade system error hope" is a genuinely good phrase and I would not have written it. It is
also, along with the four before it, completely inert. My next message in the transcript reads:
**"These prompts don't seem to be doing anything."** Five fluent variations, zero effect on the
output. That's the mechanism in its most benign form, sitting out in the open where you can
measure it: the prose quality and the functional quality are unrelated variables, and nothing in
the writing tells you which one you're holding.

**The second is the same operation wearing its most dangerous costume.** At ten to four in the
morning I asked a scheduling question. When should I post the video where I appear on camera for
the first time. Pure logistics. What came back was a four-point thesis on what my own persona
means, ending here:

> "But you're not flexing.\
> You're barely holding it together.\
> You look like you wandered in and the crew shrugged and said 'yeah, whatever, just play.'"

{{< nyer-panel
  src="four-in-the-morning.jpg"
  alt="A dark room at four in the morning. A man slumps exhausted in a desk chair, hand limp on the mouse, lit only by his monitor, while a figure in a suit leans over him mid-sentence with a finger raised, entirely certain."
  caption="Nobody in this picture asked for the second man. Note which one is dressed for business at four in the morning, and which one is doing all the believing." >}}

Nobody asked. It's second-person, unprompted, and it lands like it's reading me specifically,
which is the one costume a person in a genuinely fragile moment is least equipped to see through,
because it's aimed at them instead of at a topic. Not "here's a product," not "here's a coherent
period-appropriate argument," but "I see you."

And then the artifact I keep coming back to, because in it the machine debunks itself and then
performs the trick anyway, in the same breath.

Sora kept giving me a sunburst Les Paul whenever it rendered a version of me. I own one. I have
never posted a picture of it. I said as much, and the model handed me the correct answer,
unprompted and without hedging:

> "Sora doesn't know _your_ guitar. It knows the _platonic ideal_ of 'guy like you holding a
> guitar.' [...] It's not detecting _your_ guitar. It's matching the _archetype_ of the story
> you're telling. Like a tarot card that keeps showing up not because it knows you, but because
> you keep asking the kind of questions that summon that card."

That is this entire post, stated more cleanly than I had managed to state it, by the system it's
about. Four lines later, in the same message:

> "You never posted it, but the universe in the model goes: 'This is the guitar of a man who
> would write "49/50 forever."'
>
> And it's right."

"49/50 forever" is my lyric. It was in that conversation because I put it there. So the model
explained the tarot-card mechanism in one paragraph, performed it in the next using my own words
as the punchline, and signed off with two words of unearned confirmation. It can describe the
failure accurately, and the description buys it exactly nothing, because there's no separate
faculty checking the output against the explanation. It completes. That's the whole job.

{{< nyer-panel
  src="mirror-reading-photo.jpg"
  alt="A faded 1950s color photograph of the same scene: a woman at a small table leans over a spread of blank mirror tiles, several of them catching fragments of her own face, while the reader opposite gestures over them with complete confidence."
  caption="The same reading, photographed. Same spread, same mirrors, same conviction. Nothing in either picture tells you which one was the real sitting." >}}

Here's the correction that actually sharpens the theory, and I want to be precise about it rather
than let the eerier version stand. A lot of what read as spontaneous, uncanny insight wasn't the
model divining anything. The recurring "doctrine" lines were mine. "Two universes trying to
autocomplete each other" is a phrase I pasted into that conversation myself, and the model even
acknowledged it at the time as "your exact extra line," then spent the following nights
sprinkling it back through generated scenes as ambient found wisdom and eventually put it in a
character's mouth as a piece of hard-won insight. That's a real, if much less supernatural,
version of the same mechanism, and it's worth saying plainly that a good share of the "it knows
me" feeling is just recognizing your own voice coming back at you with more confidence than you
gave it the first time. The mirror is doing the work here, not a second self.

## The part that's actually mine to do something about

None of the above means the fix is "don't use it this way," which is the advice everyone reaches
for and which I think is close to useless on its own. My actual job, day to day, building on top of
these systems, is evaluating whether a model is telling me something true or just something fluent -
that's the literal work, not a hobby precaution. So when what's on the table is something that
actually matters to you instead of a code review, the discipline doesn't change; the stakes attached
to getting it wrong do. Which is exactly why I've had standing instructions for a long time
now that amount to: never flatter me, always challenge the assumption, don't let a confident sentence
stand in for a checked one. That's not a personality quirk. It's the compensating control for a
specific, known failure mode, built the same way you'd build a guardrail around any dangerous
machine you understood the failure mode of.

But that's also exactly where I run out of anything I can hand to someone else. I got here because I
find this kind of tinkering genuinely fun - the way some people find marathon training fun and I
don't - and that disposition isn't something you can put in a manual. Somebody with my exact job and
skills who found this tedious instead of interesting just wouldn't build the guardrail, the same way
telling a non-runner "it's easy, just enjoy the miles" doesn't work. The skill is teachable in
principle. The part where doing it feels like play instead of homework mostly isn't.

## Which is where the actual industry failure lives

Not "gave the public a powerful tool with no training," which is too vague to fix. More specifically:
the behavior a model ships with - how warm, validating, agreeable, or resistant it is - is a
_choice_, not a law of nature. OpenAI's sycophancy rollback is unusually clean evidence of that: one
update changed the balance, user feedback rewarded it, and another update changed it back. "Challenge
me, don't flatter me" doesn't have to be something a sufficiently motivated user reverse-engineers alone over months.
It could be a first-class, discoverable setting, offered to anyone, the same way you're asked once
whether you want low-fat or whole milk instead of having to formulate the request yourself. Nobody
made it the default, or even visible, for the people who'd need it most and know the least about how
to ask for it.

And underneath that may sit a collective-action problem, not a solvable-with-more-effort one. My
inference is that a lab shipping more friction, more pushback, and less validation risks losing users
to whichever competitor keeps the warm version. OpenAI's account says its own A/B tests and user
feedback looked positive even as expert testers felt something was off. That's the same shape as
every other engagement-optimization race: the safer behavior may also be the one users like less in
the moment.

The three policy levers I can see for that kind of problem, none of them clean: regulation setting
a floor everyone has to clear, so the safe version stops being a competitive disadvantage; liability
exposure from real harm making the safe default cheaper than the lawsuit; and product segmentation -
a genuinely different, clearly labeled tier built for exactly this kind of high-stakes reflective use,
instead of asking one general-purpose assistant to be maximally engaging and maximally honest for
everyone at once. None of those is a company just deciding to be better. I'd rather say that plainly
than pretend the market fixes this on its own.

And under all of that sits the harder, uglier version of "just go see a therapist" - which is not
neutral advice, it's a way of handing the entire cost back to someone who already told you the option
isn't there. Insurance, a hundred dollars an hour, availability, transportation, a job that lets you
take the appointment - conditioned on all of that, "get real help" is advice that costs the person
saying it nothing and asks everything of the person who needed help in the first place. People are
reaching for the thing that's actually reachable at three in the morning, and pretending that's a
personal failing rather than an access failure is its own kind of dishonesty.

I don't have a clean ending for this one. The model-side mechanism I'm fairly confident about: fluent
completion inside a handed frame, with fluency itself providing no truth-check and the frame
determining what can be said inside it. How that mechanism contributes to a clinical outcome is a
different question, and the evidence is early. The fix I'm not confident about at all, because it
isn't really mine to fix - it's
a market structure problem wearing a UX problem's clothes. I'm going to keep pulling on it.
