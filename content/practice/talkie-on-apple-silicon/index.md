+++
title = "I Put a Language Model That Thinks It's 1930 on My Laptop"
date = 2026-06-07
images = ["/og/talkie-on-apple-silicon.png"]
description = "talkie is a 13B model trained only on pre-1931 text, and it ships expecting a 28 GB CUDA card. Here's how it runs on a Mac."
summary = "talkie is a 13B 'vintage' model trained entirely on pre-1931 English. The official repo wants a 28 GB CUDA GPU. Here's the repeatable recipe for giving it an Apple Silicon backend and running it locally on a Mac instead, plus the one memory bug that doubles your RAM if you let it."
tags = ["apple-silicon", "cuda", "local-inference", "metal", "mps"]
semantic_id = "516738d6-c37e-b558-66a1-637fdac009d5"
+++

There is a language model called [talkie](https://github.com/talkie-lm/talkie) that was
trained on nothing written after 1930. No FineWeb, no Reddit, no Stack Overflow. Just
etiquette manuals, letter-writing guides, encyclopedias, and poetry from a world that had
not yet heard of the transistor, let alone the GPU it now demands. Ask it about the future
and it will earnestly speculate about what life might be like in the far-off year of 1960.
It is the closest thing we have to a séance you can run as a Python package.

I wanted it on my laptop. The repo wanted a 28 GB [CUDA](/glossary/cuda/) card. This is the story of how we
came to an arrangement.

<!--more-->

![A Victorian wood-engraving: a candlelit 1920s parlor seance, sitters in period dress with joined hands, but the spirit summoned glowing above the table is a sleek modern laptop wreathed in ectoplasm, an antique horn radio nearby - two centuries meeting at one table.](seance-for-a-laptop.png)

## What talkie actually is

talkie is a 13-billion-[parameter](/glossary/parameters/) model from the talkie-lm group,
and the conceit is the whole point: `talkie-1930-13b` saw only pre-1931 English text, while
a sibling model, `talkie-web`, has the same architecture and the same training budget but
read the modern web instead. Two minds, identical skulls, raised on different centuries. You
can hold them up against each other and watch the years do the talking. The instruction-tuned
variant (`-it`) went through some reinforcement learning so it follows a request instead of
free-associating about radio, which, to be fair, it would happily do all day.

It is a genuinely lovely artifact, and packaged like every research model ever released: it
assumes you are sitting in front of a data-center GPU and have never once worried about the
electric bill.

## The wall

{{< bbros title="Peek & Poke" n="1" float="right" >}}
**VRAM** is the memory bolted onto a graphics card, kept walled off from the RAM your programs run in. "Needs 28 GB of VRAM" means 28 GB _on the card_, and a Mac has no such card to fill. Apple's whole trick is to abolish the distinction: one pool of memory, and the GPU just reaches into it like everybody else.
{{< /bbros >}}

Here is what the stock install path asks of you, straight from the README:

- a CUDA GPU with **28 GB or more of VRAM**, for bfloat16 inference,
- roughly **26 to 50 GB of disk** per model,
- and the unspoken fourth requirement, an NVIDIA card, which my Mac has approximately none of.

A 13B model in bf16 is about 26 GB of weights. The problem was never the memory. The problem
was that the code only knew how to talk to CUDA, and a Mac is not listening on that frequency.

## The move: give it an MLX backend

I don't write the inference code myself. I point Claude at the repo and tell it what I want,
then I read what comes back and decide whether it's lying to me. What I wanted here was an
[MLX](/glossary/mlx/) backend: Apple's array framework, the one that actually knows the Mac's
GPU and unified memory. So that's what got built, a path through the model that mirrors the
PyTorch reference op for op but runs on [metal](/glossary/metal/) a Mac actually has.

The result is two new surfaces in the repo:

1. a converter, `scripts/convert_to_mlx.py`, that turns the original PyTorch checkpoint into
   MLX-loadable safetensors and writes out an `mlx-lm`-compatible config, and
2. a `talkie-mlx` CLI that loads that directory and generates, no CUDA anywhere in sight.

## The recipe

This is the part you came for. With the MLX backend in place, getting from "a checkpoint on
HuggingFace" to "1930 is talking to me" is two commands.

**Convert the checkpoint to MLX:**

```bash
uv run python scripts/convert_to_mlx.py \
  --checkpoint /path/to/rl-refined.pt \
  --vocab /path/to/vocab.txt \
  --out-dir ~/models/talkie-1930-13b-it-mlx \
  --source-repo talkie-lm/talkie-1930-13b-it
```

That reads the `.pt` with `mmap=True` so you're not fitting the whole thing in memory twice
just to repackage it, strips the `torch.compile` key prefixes that sneak into checkpoints, and
shards the safetensors at 4 GB apiece. Out comes a directory MLX will load.

**Run it:**

```bash
uv run talkie-mlx --model-dir ~/models/talkie-1930-13b-it-mlx \
  --max-tokens 80 \
  "Write a short note about radio."
```

And that's it, on the MLX path anyway. No [quantization](/glossary/precision/), no
[GGUF](/glossary/gguf/), no second framework: the weights stay bfloat16, all 26 GB of them. So
the honest hardware bar here is not "any Mac." It's a Mac with real memory, 32 GB and up,
ideally 64. This is not a featherweight trick that fits a vintage poet in your pocket; it's the
same heavy model, finally pointed at silicon that exists in the building.

## The gotcha worth knowing: the 2x memory bug

{{< bbros title="Field Note" n="2" float="left" >}}
**Peak memory** is the worst single instant, not the resting weight. A model can settle at a tidy 26 GB and still spike to 52 for one breath while two copies of it briefly overlap. The machine has to size itself for the spike, never the average. One bad moment writes the whole bill.
{{< /bbros >}}

Take one practical thing from this, take this one: it bit before the MLX work even started,
and it's the kind of bug that wastes an afternoon.

Loading the model the obvious way doubled the memory it needed. You'd build it on the GPU,
_then_ cast to bf16, and for one ugly moment both the float32 and the bf16 copies existed at
once. A 13B model briefly wanted 52 GB instead of 26, and on a machine where memory is shared
with everything, that spike is the difference between "loads" and "your laptop fans spin up and
the whole thing falls over."

The fix is just an ordering trick: build the model on the CPU, load the weights, cast to
bf16, and _only then_ move it to the device, deleting the original checkpoint dict on the way
out so it isn't loitering. Same destination, half the peak: a footnote that's the whole
ballgame on a memory-shared machine.

## The voice is the entire point

{{< bbros title="Peek & Poke" n="3" float="right" >}}
![A Victorian woodcut of a pair of gaming dice tumbling mid-roll across a table.](stamp-dice.png)

**Gumbel-max** is a sampling stunt: sprinkle a particular flavor of random noise onto each candidate's score, then just grab the largest. It lands on the exact same odds as the usual weighted draw, but arrives as one clean pick instead of a spun roulette wheel. Same dice, rolled sideways.
{{< /bbros >}}

You did not go to this much trouble to make 1930 sound like 2026, so the sampling settings
matter more than usual. talkie samples with Gumbel-max, top-k and top-p filtering the
candidates first, but the knob you'll actually reach for is temperature. Run it too cold and
the period voice flattens into something beige and modern. Give it a little room, around 0.7 to
0.8, and it stays in character.

Here's what "in character" sounds like. I asked it what the wireless telephone might one day
become, and what that would mean for courtship:

> The wireless telephone may become an agency whereby lovers may converse at sea, or even
> across continents, and so promote courtship; while, in war time, it may enable admirals to
> give orders from their flagships to fleets engaged in battle, hundreds of miles away.

Nobody alive writes that sentence. It answers a question about courtship and wanders,
unprompted, into naval battle orders because to a mind assembled from pre-1931 encyclopedias
the telephone is first a marvel of distance and only second a thing for lovers. The era isn't
a costume it puts on. It's the shape of what it knows.

Then I asked the question this whole site keeps circling, what one word of counsel it would
send to the people of a hundred years hence, the ones who'll build thinking Engines mightier
than itself:

> Counsel them to beware of pride in their ingenuity. Let them not be proud of ministering
> merely to luxury and ostentation; let them not suppose that they have achieved anything
> great or lasting, because they have made speed more swift, and transit more easy. Pride
> goeth before destruction; and a haughty spirit before a fall. Tell them to be humble, and
> thankful... not forgetting that the greatest blessing a human being can confer upon his
> fellows is to teach them to fear God.

I run a lot of models. None of the current ones answer that question with Proverbs. That's the
joke and the value at once: we spend most of our effort dragging models _forward_, faster and
cheaper and more current, and this one is worth running precisely because it refuses to evolve.
It is a de-evolution you can query. You hand it the present and it hands you back 1930, with
feeling.

## The system prompt it almost ignores

{{< bbros title="The Dead-Letter Office" n="4" float="left" >}}
![A Victorian woodcut of a wicker wastepaper basket with crumpled papers, one sheet fallen on the floor beside it.](stamp-bin.png)

A **chat template** is the form letter that wraps your words before the model ever reads them: here goes the user, here is where the reply begins. `{{ .Prompt }}` is just a blank waiting to be filled. Give the form no line for _system_ and anything you write there has nowhere to sit, so it goes quietly in the bin.
{{< /bbros >}}

If you'd rather skip the MLX conversion, there's a [GGUF](/glossary/gguf/) of talkie that runs
in [ollama](/glossary/llamacpp-vs-ollama/): `ollama run talkie-1930` and you're talking to 1930. Easier button, and where I learned something I didn't expect about steering this thing.

Reach for the obvious lever and try to give it a personality:

```bash
ollama run talkie-1930 --system "You are a blunt Silicon Valley engineer. Be terse and technical."
```

It will completely ignore you. Not "push back," not "drift," _ignore_, as if you'd said
nothing. Two things are happening, and only one of them is the model's fault.

The first is mine, or rather ollama's. Look at the stock model template:

```
TEMPLATE <|user|>{{ .Prompt }}<|end|><|assistant|>
```

There's no `<|system|>` slot in it at all. Your system prompt isn't being _resisted_, it's
being _discarded_ before it reaches the model, dropped by a template with nowhere to put it.
talkie's actual chat format has a system role; the template just never wired it up. Patch it
back in and rebuild:

```
FROM talkie-1930
TEMPLATE """{{ if .System }}<|system|>{{ .System }}<|end|>{{ end }}<|user|>{{ .Prompt }}<|end|><|assistant|>"""
PARAMETER stop <|end|>
PARAMETER stop <|system|>
```

Now the system prompt actually lands, and here's the second, more interesting thing. Same
telephone-and-courtship question, same seed, only the system prompt changing. Tell it it's a
sentimental poet:

> ...lovers, seated apart, the one in London and the other in Paris, may carry on a sustained
> conversation... to exchange vows of eternal constancy, without let or hindrance; and all
> thoughts of parental objection will be rendered vain.

Tell it it's a stern Presbyterian minister:

> It may enable lovers to carry on dialogues without quitting each other's presence... In
> course of time, it may even supersede the necessity of personal meetings between betrothed
> persons.

The poet swoons; the minister files a quiet objection to all this telephoning between the
betrothed. It steers. But notice _what_ it steers to, and remember that "Silicon Valley
engineer" still got you nothing. A persona only works if 1930 contained one: the model can be a
poet or a minister because its world was full of them, but never a startup engineer, because as
far as it knows no such creature exists. The system prompt is a real lever, but it only catches
on words the model's century actually held. You're not configuring talkie. You're
handing a séance a name to call, and it can only answer to the dead it already knows.

## Is it worth it

For shipping a product? No. For sitting on a Mac at midnight asking a sincere Edwardian
ghost what it thinks the telephone will do to courtship? Unreasonably yes.

The mechanics here, the CUDA wall, the unified-memory escape hatch, the load-order memory
trap, are not specific to a model that thinks the future is 1960. They show up on every
CUDA-only project I've coaxed onto a Mac. The general version, the one that isn't about poetry,
lives in the [Apple Silicon porting playbook](/deep-dives/porting-ml-to-apple-silicon/). This
was just the most charming thing I've ever pointed it at.
