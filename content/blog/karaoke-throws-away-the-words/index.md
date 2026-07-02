+++
title = "My Karaoke Machine Throws Away Every Word It Hears"
date = 2026-07-07
description = "WhisperX mishears every lyric, so my band's karaoke tool keeps its timing and throws the words out. Right words, right time."
images = ["/og/karaoke-throws-away-the-words.png"]
summary = "I built my band a karaoke video maker, and the trick that makes it work is refusing to trust the one part everyone assumes you'd trust: the transcription. The machine listens to the singing, mishears most of it, and I keep only its sense of timing - never its words. A small lesson in using a model that lies, plus why the fakery around the edges is what makes it feel real."
+++

My band, OWNER/OPERATORS, makes songs that a reasonable number of people will go their
whole lives without hearing. So naturally I spent a night building us a karaoke machine.
Nobody asked. But a song you can sing along to is a song that happened to somebody, and I
wanted ours to have happened.

The obvious way to build one is to hand the whole job to a [model](/glossary/machine-learning/): here's the audio,
transcribe the words, time them, drop a bouncing ball on top. That is exactly the approach
that does not work, and the reason it doesn't is the most useful thing I learned the entire
week.

<!--more-->

![A Victorian wood-engraving: a man at a great brass phonograph horn that transcribes a singer onto a long paper ribbon, the ribbon spilling into a heap of scattered, discarded scraps of words on the floor, while a tall metronome stands beside it keeping perfect, exact time - the machine throws the words away and keeps only the timing.](karaoke-machine.png)

## The machine that can't be trusted with words

To put a word on screen at the moment it's sung, something has to actually hear the singing.
So the skill takes two exports of the same performance. One is the instrumental, no vocals,
and that's the track you hear in the finished video, because the whole point of karaoke is
that you supply the voice. The other is the vocal mix, and you never hear it at all. It
exists for one listener: a speech-to-text model named WhisperX, which I let eavesdrop on the
singing purely to find out where in time each word lives.

Here's the part that matters. WhisperX is a transcription model, and pointed at a sung vocal
it produces a transcript that is, charitably, a cousin of the actual lyrics. It hears
"LOSS LEADER" as "lost leader." It hears an ad-libbed throwaway as a word I would never put
in a song. Proper nouns mutate into other proper nouns. Anything stylized, which in a band
is roughly everything, comes back a little wrong. If I trusted that transcript, every video
would quietly, permanently misquote my own songs.

So I don't trust the transcript. I throw the whole thing away.

That's the move, and it's the one I'd keep if you took everything else: WhisperX is bad at
_what_ I sang and good at _when_ I sang it. The words are guesses. The timestamps are
measurements. A model can be a fabulist about content and a stopwatch about timing in the
very same breath, and the trick to using one is knowing which of those two things you're
actually holding. So I keep the clock and bin the dictionary. The skill lifts only
WhisperX's timings and lays them onto the song's canonical `lyrics.md` - the words I already
know are right, because I wrote them - letting each real word inherit the start and end of
whatever nonsense the machine heard in that slot. The gaps it missed get interpolated. Right
words, right time. The machine never gets a vote on the lyrics. It only gets to say when.

## You already know this trick, you just call it other things

I keep running into the same shape, and this was the cleanest version of it I've built. A
model is not a single instrument you either trust or don't. It's a drawer full of them, and
some are precise and some are liars, and your whole job is to reach past the liars for the
one that measures. Ask it the narrow question it can answer. Anchor everything else to ground
truth you already own. I didn't let WhisperX decide my lyrics any more than I'd let it decide
my bank balance. I let it do the one thing it's genuinely better at than I am: listen to four
minutes of singing and tell me, to the centisecond, when each syllable landed. I'd have been
there all night with a stopwatch. It did it in a couple of minutes and got the timing
honest, which is all I ever wanted from it.

## The part nobody warns you is mostly fakery

Once the timing is solved, the rest of the work is a magic trick, and like every magic trick
it's ninety percent stage dressing. I learned that a karaoke video without a title card reads
like a rough cut. So the skill always opens on the band name and the song, and always closes
on real credits: album, label, the little circled-P and the year, the website. None of that
is functional. All of it is the difference between "a file rendered correctly" and "a thing
that feels like it came from somewhere."

Real karaoke taught me the rest. The old labels each had a signature look - the clean blue
discs, the bouncing-ball retro decks, the lo-fi bootleg tapes that looked dubbed nine times -
so the skill carries "brands" you pick per song: a clean one, a loud retro one, a degraded
VHS one. And because OWNER/OPERATORS already has a house style - our site runs a writhing
WebGL glitch, hue drift and scanlines and a vignette - the default brand echoes that in cheap
video filters, with little RGB-split stabs gated to the section changes so the picture tears
exactly when the song turns. There's even a true datamosh option, the real thing, where you
re-encode the background with no keyframes so every hard cut blooms the previous shot's motion
into the next. Not a filter pretending to glitch. An actual one, invited in on purpose. Which,
if you know what de-evolution is supposed to mean, is the most on-brand thing in the whole
project.

## What "I built" is doing in that sentence

I should be honest about the verb. When I say I built a karaoke machine, I mean it the way a
general contractor says he built your house: I didn't pour the concrete. I do not write the
ffmpeg filtergraphs that burn the lyrics over the instrumental, and I could not sit down and
author the subtitle-timing format from memory if you asked. The agent writes that. What I
actually did was decide that the words and the timing are two different problems, that the
machine should be trusted with exactly one of them, and that the credits matter more than they
have any right to. Then I watched what came back and said yes, or no, or "the eyeball clip
goes in the instrumental gap, not the chorus." The skill is the plan and the judgment written
down so the next song is faster. The taste is the part with my fingerprints on it.

And the machine, the one doing the listening, hears every word and is trusted with none of
them. It sits there with perfect ears and no say, a session musician I hired strictly for his
sense of time and specifically asked not to sing. Best collaborator I've got. He never once
tried to rewrite the song.
