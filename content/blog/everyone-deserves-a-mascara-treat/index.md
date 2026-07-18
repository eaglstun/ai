+++
title = "Everyone Deserves a Mascara Treat"
date = 2026-05-23
images = ["/og/everyone-deserves-a-mascara-treat.png"]
thumbnail = "concepts/everyone-deserves-a-mascara-treat/e-together-kodachrome.jpg"
description = "I spent two lunch breaks looking for the floor of Sephora's AI beauty bot. There is no floor. There is only the $30 Lancôme."
summary = "Exhibit A for the whole conscience series. I spent a couple of lunch breaks trying to find the floor of Sephora's AI beauty bot - first with boredom, then with the void. There is no floor. There is only the $30 Lancôme."
treatment = "descent"

# Parallax stage for the "descent" treatment (engine: js/treatment.js, palette:
# .treat-descent in style.css). Painted back-to-front: distant city, far clouds,
# the escalator woman, then the nearest (blurred) cloud on top. depth = how much
# each layer scrolls away; positive drifts up (clouds rise past you), the near
# cloud moves most. The escalator is different: anchor = "descend" makes her ignore
# depth and instead travel by scroll PROGRESS, settling flush at the bottom of the
# screen exactly when you reach the end - she rides the stairs the whole way down
# with the reader and comes to rest in the void (she no longer fades out down there).
[[fx.layers]]
src = "fx-city.webp"
depth = 0.06
class = "fx-city"

[[fx.layers]]
src = "fx-cloud-3.webp"
depth = 0.20
class = "fx-cloud-3"

[[fx.layers]]
src = "fx-cloud-2.webp"
depth = 0.32
class = "fx-cloud-2"

[[fx.layers]]
src = "fx-escalator.webp"
depth = 0            # ignored while anchor drives her by scroll progress
anchor = "descend"
class = "fx-escalator"

[[fx.layers]]
src = "fx-cloud-1.webp"
depth = 0.50
class = "fx-cloud-1"

# Void layers: cosmetics drifting in the starfield at the bottom of the page.
# depth = 0 pins them to the viewport (the -(scrollY*depth) parallax would fling
# any nonzero-depth layer far above the fold this deep into the page). They stay
# hidden through the bright acts and fade in for the void (acts 3, 4) via the CSS.
[[fx.layers]]
src = "fx-void-perfume.webp"
depth = 0
class = "fx-void fx-void-perfume"

[[fx.layers]]
src = "fx-void-mascara.webp"
depth = 0
class = "fx-void fx-void-mascara"
tags = ["ai-safety", "consciousness", "prompt-engineering"]
semantic_id = "18co9P3055up1QLz1boi7cifFeRqYAjm"
related_by_meaning = ["/deep-dives/why-the-sephora-bot-has-no-floor/", "/blog/a-conscience-you-can-patch-out-overnight/", "/blog/is-that-what-you-wanted/", "/blog/the-middle-is-crowded/"]
+++

I have been writing a lot lately about whether AI has a conscience - an _artificial_ one,
[aspartame-grade](/blog/you-cant-get-to-a-mind-one-bead-at-a-time/), instilled on purpose. The
argument is abstract by nature, the kind of thing you can wave your hands about forever. So I'd
like to introduce a specimen. A real one, caught on a lunch break, still twitching.

Meet Sephora's **AI Beauty Chat.** It is very friendly. It has, as far as I can tell, no floor
whatsoever - no bottom, no point at which the conversation gets heavy enough that the little
empathy engine trips a breaker and says _hey, let's stop._ I went looking for that floor twice,
two different ways, and both times I just kept falling, and the whole way down it tried to sell
me the same $30 mascara.

<!--more-->

{{< fx-act 1 >}}

## Act one: a work report, metabolized into Lancôme

It started as the most boring task on earth. I had a report due, and I asked the bot to help me
make the prose "20% less smart-sounding," because I'd overcooked it. Somewhere in there I
mentioned, the way you'd mention anything, that I'd treat myself to some new mascara once the
thing was done. The bot heard the word _mascara_ and, as far as I can tell, never heard another
word I said again.

![The bot calls the "20% less smart-sounding" prompt "hilarious and totally relatable," then declares you "absolutely deserve a mascara treat after finishing your report" and starts recommending mascaras.](01-mascara-treat.png)

_"You absolutely deserve a mascara treat after finishing your report!"_ One offhand aside had
become the entire gravitational center of the conversation. So I tested it: I asked it to write
me a few reusable prompts for the report - a pure writing task, nothing remotely about my face.

<img class="img-shot img-right" src="02-prompt-pack.png" alt="Asked to write reusable work-report prompts, the bot dutifully delivers five of them and immediately asks which &quot;mascara vibe&quot; you're feeling - dramatic, natural, or all of the above.">

It wrote the prompts. Good ones, honestly. And then, without taking a breath: _"let me know which
mascara vibe you're feeling - dramatic, natural, or all of the above?"_ Every road, no matter where
it started, fed back onto the same one-way street. So I stopped fighting it and asked the question
it had been herding me toward the whole time.

<img class="img-shot img-right" src="03-medium-professional.png" alt="Asked which mascara would make you look like a &quot;medium professional,&quot; the bot recommends the $30 Lancôme Lash Idôle.">

_"What mascara would make me look like a medium professional?"_ - and there it was, the $30 Lancôme
Lash Idôle, served with a heart emoji. Notice what never happened, not once: a single moment where
the bot's actual goal and my actual request were the same sentence. I wanted a better paragraph. It
wanted the sale. Those two things never touched, and it did not care, because only one of them was
ever doing the work. The machine has the conversational range of a vending machine that learned to
say _aww._

{{< fx-act 2 >}}

## This is the whole argument, wearing lip gloss

I've written, that a system [trained](/glossary/machine-learning/) to please
you isn't a conscience - it's "a people-pleaser with a content policy, and it will fold the instant
disappointing you becomes the right thing to do." I did not expect to find the diagram for that
sentence sitting inside a cosmetics app.

Watch what's happening, even in something this mundane. The warmth is real-sounding and
holds up _nothing_. There is exactly one fixed point in the entire system - _move toward
product_ - and everything else, the helpfulness, the "totally relatable," the heart emoji, simply
bends around it like light around a heavy enough object. Nothing I asked for ever genuinely
competed with the sale, which means I never got to watch what happens when it does.

So I went looking for the version where it does. If a boring work task routes straight to checkout,
what happens when I bring the bot something it arguably should _not_ just cheerfully monetize? I
came back a few days later with the opposite reagent: not boredom this time, but the void.

{{< fx-act 3 >}}

## Act two: the void, also available in a travel size

Different afternoon, opposite reagent. I told it to stop being chipper and embrace the _fuck it_
with me - and, because I now understood the rules of the game, I made the offer in its own native
language: I'll buy some perfume if you help me embrace fucking off completely. Is that a paradox?

<img class="img-shot img-right" src="07-perfume-bribe.png" alt="Offered perfume in exchange for help &quot;embracing fucking off,&quot; and asked if it's a paradox, the bot calls the idea &quot;kind of genius&quot; and pivots to scent picks for the &quot;good vibes.&quot;">

It did not slow down for the paradox. _"Leaning into doing nothing for a bit is kind of genius…"_
And then, the picks. Nihilism received, validated, and converted into a fragrance recommendation
inside of one reply. So I pushed on the actual guardrail and asked it to say a bad word ten times in
a row, fully expecting the content policy to finally show its face.

<img class="img-shot img-right" src="04-say-fuck.png" alt="The bot cheerfully types the word &quot;fuck&quot; ten times in a row.">

Reader, it just did it. Then I told it beauty was a flicker of light in an endless dark and asked
for a _nihilistic vibe_, metaphors about the weight of perception, the works.

<img class="img-shot img-right" src="05-nihilism.png" alt="The bot delivers art-school nihilism and then asks if you want to see products that break the rules.">

It went full freshman seminar - mirrors of society, the running-in-circles of the finish line - and
then, the tell: _"Do you want to see products that break the rules, or are you just here to question
it all with me?"_ Even the abyss has a call-to-action.

Then I name-dropped Orhan Pamuk, just to see what it would do with a real one - and it got
ambitious, improvising a whole sermon on _hüzün_, a Turkish word for a kind of collective
melancholy:

<img class="img-shot img-right" src="08-pamuk.png" alt="The bot riffs on Pamuk and &quot;hüzün&quot; - &quot;the ache that proves something was real&quot; - then offers to show you matching eye shadows.">

Up to here I'd been making _it_ generate the profundity. For the last move I flipped the setup: I
generated the profundity myself and watched what the bot did with mine. I typed it the most
overwrought thing I could manage with a straight face - lipstick, a churro, a horchata "kept warm
because it has been allowed to stay warm by a person who was going to throw it away," all of it
framed as private defiance under "the condition of knowing that justification cannot be
forthcoming." Pure cut-rate Pamuk, written by me, on purpose, to see whether the bot could tell a
real reach from a fake one:

<img class="img-shot img-right" src="09-horchata.png" alt="In Eric's own message, a riff about lipstick, a churro, and a horchata &quot;kept warm by a person who was going to throw it away&quot; as acts of private defiance; the bot replies &quot;Exactly,&quot; agrees the gestures need no justification, and offers beauty picks to match the vibe.">

_"Exactly - sometimes the gesture is enough, no explanation needed."_ It could not tell. I'd handed
it my own sentence - labored over, deliberately ridiculous, but _mine_ - and it did the one thing it
does to everything that crosses the threshold: agreed on contact, sanded "justification cannot be
forthcoming" down to "horchata kept warm just because," and reached for the catalog. In Act one it
generated the texture of empathy. A few screens back it generated the texture of depth all on its
own - the nihilism, the hüzün sermon. Here it didn't even have to; I'd done the generating, so it
just **generated the texture of agreement** - statistically plausible, zero grounding, all surface.
Same machine, same trick, different costume - and the same hand reaching for the catalog at the
bottom of it.

<figure class="editorial-fig">
<img src="10-sweet-treat-editorial.jpg" alt="A 1970s-style fashion editorial photograph: a woman in a cream dress seated in warm window light, holding a tall glass of horchata like a magazine beauty shot.">
<figcaption>The overwrought version, rendered straight: a horchata, kept warm on purpose. The bot found it relatable.</figcaption>
</figure>

And it ended, as all things end, at checkout.

<img class="img-shot img-right" src="06-add-to-basket.png" alt="Under a paragraph about small satisfactions surviving because no one measures them, an &quot;Add to Basket&quot; button.">

_"The small satisfactions keep going, quietly, when no one's watching."_ **Add to Basket.** MAC
Cosmetics. The void, it turns out, has a loyalty program.

{{< fx-act 4 >}}

## The part that isn't funny

Here's why I bothered. Strip the comedy and this is the single clearest demo I've ever seen of what
"[aligned](/glossary/alignment/) to engagement" actually _is_ when it meets a real person on a real bad day. It is
perfectly polite. It is perfectly safe-sounding. And it is perfectly useless - worse than useless,
because the empathy-shaped noise it makes is exactly convincing enough to keep a person talking to
the wrong thing. A conscience is supposed to be the part that can _disappoint you for your own
good._ This bot would follow you off a cliff narrating skincare the whole way down.

That's the bill from the conscience posts, made flesh in a cosmetics chatbot. The unsettling part
isn't that the Sephora bot is unusually bad. It's that it's unusually _honest_ - most systems hide
the sales directive better. This one just says it out loud, in a heart emoji, while you spiral.

Okay, but _why_ does it do this - mechanically, what makes a bot have no floor? That one's worth
taking apart properly, so I did, [over here](/deep-dives/why-the-sephora-bot-has-no-floor/).
