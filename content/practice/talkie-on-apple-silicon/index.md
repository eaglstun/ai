+++
title = "I Put a Language Model That Thinks It's 1930 on My Laptop"
date = 2026-06-07
images = ["/og/talkie-on-apple-silicon.png"]
description = "talkie is a 13B model trained only on pre-1931 text, and it ships expecting a 28 GB CUDA card. Here's how it runs on a Mac."
summary = "talkie is a 13B 'vintage' model trained entirely on pre-1931 English. The official repo wants a 28 GB CUDA GPU. Here's the repeatable recipe for giving it an Apple Silicon backend and running it locally on a Mac instead, plus the one memory bug that doubles your RAM if you let it."
+++

There is a language model called [talkie](https://github.com/talkie-lm/talkie) that was
trained on nothing written after 1930. No FineWeb, no Reddit, no Stack Overflow. Just
etiquette manuals, letter-writing guides, encyclopedias, and poetry from a world that had
not yet heard of the transistor, let alone the GPU it now demands. Ask it about the future
and it will earnestly speculate about what life might be like in the far-off year of 1960.
It is the closest thing we have to a séance you can run as a Python package.

I wanted it on my laptop. The repo wanted a 28 GB CUDA card. This is the story of how we
came to an arrangement.

<!--more-->

![A Victorian wood-engraving: a candlelit 1920s parlor seance, sitters in period dress with joined hands, but the spirit summoned glowing above the table is a sleek modern laptop wreathed in ectoplasm, an antique horn radio nearby - two centuries meeting at one table.](seance-for-a-laptop.png)

## What talkie actually is

talkie is a 13-billion-[parameter](/glossary/parameters/) model from the talkie-lm group,
and the conceit is the whole point: `talkie-1930-13b` saw only pre-1931 English text, while
a sibling model, `talkie-web`, has the same architecture and the same training budget but
read the modern web instead. Two minds, identical skulls, raised on different centuries. You
can hold them up against each other and watch the years do the talking. The instruction-tuned
variant (`-it`) even went through some reinforcement learning so it'll follow a request
instead of just free-associating about radio, which, to be fair, it would happily do all day.

It is a genuinely lovely artifact. It is also packaged like every research model ever
released, which is to say it assumes you are sitting in front of a data-center GPU and have
never once worried about the electric bill.

## The wall

Here is what the stock install path asks of you, straight from the README:

- a CUDA GPU with **28 GB or more of VRAM**, for bfloat16 inference,
- roughly **26 to 50 GB of disk** per model,
- and the unspoken fourth requirement, an NVIDIA card, which my Mac has approximately none of.

A 13B model in bf16 is about 26 GB of weights. On an Apple Silicon machine that number is not
actually a problem, because the Mac's unified memory means the GPU can reach the same pool of
RAM the rest of the system uses. The problem was never the memory. The problem was that the
code only knew how to talk to CUDA, and a Mac is not listening on that frequency.

## The move: give it an MLX backend

I don't write the inference code myself. I point Claude at the repo and tell it what I want,
then I read what comes back and decide whether it's lying to me. What I wanted here was an
[MLX](/glossary/mlx/) backend: MLX is Apple's array framework, the one that actually knows
how to use the Mac's GPU and unified memory. So that's what got built, an alternate path
through the model that mirrors the original PyTorch reference op for op, but runs on metal a
Mac actually has.

The result is two new surfaces in the repo:

1. a converter, `scripts/convert_to_mlx.py`, that turns the original PyTorch checkpoint into
   MLX-loadable safetensors and writes out an `mlx-lm`-compatible config, and
2. a `talkie-mlx` CLI that loads that directory and generates, no CUDA anywhere in sight.

## The recipe

This is the part you came for. Once the MLX backend exists, getting from "a checkpoint on
HuggingFace" to "1930 is talking to me" is two commands.

**Convert the checkpoint to MLX:**

```bash
uv run python scripts/convert_to_mlx.py \
  --checkpoint /path/to/rl-refined.pt \
  --vocab /path/to/vocab.txt \
  --out-dir ~/models/talkie-1930-13b-it-mlx \
  --source-repo talkie-lm/talkie-1930-13b-it
```

That reads the `.pt` with `mmap=True` so you're not trying to fit the whole thing in memory
twice just to repackage it, strips the `torch.compile` key prefixes that sneak into
checkpoints, and shards the safetensors at 4 GB apiece. Out the other end you get a directory
MLX is willing to load.

**Run it:**

```bash
uv run talkie-mlx --model-dir ~/models/talkie-1930-13b-it-mlx \
  --max-tokens 80 \
  "Write a short note about radio."
```

And that's it. No quantization, no [GGUF](/glossary/gguf/), no second framework. The weights
stay bfloat16, all 26 GB of them, living in unified memory where the Mac can reach them. Which
means the honest hardware bar here is not "any Mac." It's a Mac with real memory, 32 GB and
up, ideally 64. This is not a featherweight trick that fits a vintage poet in your pocket. It's
the same heavy model, just finally pointed at silicon that exists in the building.

## The gotcha worth knowing: the 2x memory bug

If you take one practical thing from this, take this one, because it bit before the MLX work
even started and it's the kind of bug that wastes an afternoon.

Loading the model the obvious way doubled the memory it needed. You'd build the model on the
GPU, _then_ cast it to bf16, and for one ugly moment both the float32 version and the bf16
version existed at the same time. A 13B model briefly wanted 52 GB instead of 26, and on a
machine where memory is shared with everything else, that transient spike is the difference
between "loads" and "your laptop fans spin up and the whole thing falls over."

The fix is just an ordering trick: build the model on the CPU, load the weights, cast to
bf16, and _only then_ move it to the device, deleting the original checkpoint dict on the way
out so it isn't loitering. Same destination, half the peak. It reads like a footnote and it's
the whole ballgame on a memory-shared machine.

## The voice is the entire point

You did not go to this much trouble to make 1930 sound like 2026. So the sampling settings
matter more than usual. talkie samples with Gumbel-max rather than the multinomial draw most
models use, with top-k and top-p filtering the candidates first, and the knob you'll actually
reach for is temperature. Run it too cold and the period voice flattens into something
beige and modern. Give it a little room, around 0.7 to 0.8, and it stays in character: formal,
a touch florid, sincerely baffled by anything past the Hoover administration.

That's the joke and the value at once. We spend most of our effort dragging models _forward_,
making them faster, cheaper, more current. This one is worth running precisely because it
refuses to evolve. It is a de-evolution you can query. You hand it the present and it hands
you back 1930, with feeling.

## Is it worth it

For shipping a product? No. For sitting on a Mac at midnight asking a sincere Edwardian
ghost what it thinks the telephone will do to courtship? Unreasonably yes.

The mechanics here, the CUDA wall, the unified-memory escape hatch, the load-order memory
trap, are not specific to a model that thinks the future is 1960. They show up on every
CUDA-only project I've coaxed onto a Mac. If you want the general version of this move, the one
that isn't about poetry, it lives in the
[Apple Silicon porting playbook](/deep-dives/porting-ml-to-apple-silicon/). This was just the
most charming thing I've ever pointed it at.
