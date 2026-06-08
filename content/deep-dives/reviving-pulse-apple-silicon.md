+++
title = "Necromancy for Neural Nets: Bringing PULSE Back on a Mac"
date = 2026-05-24
draft = true
summary = "Getting a 2020 StyleGAN upsampler running on a Mac — dead download links, CUDA-only assumptions, and a six-year-old conda env, all dragged into the present."
+++

[PULSE](https://github.com/eaglstun/pulse) (CVPR'20) turns a blurry 16×16 face into a
sharp 1024×1024 one — not by inventing detail pixel-by-pixel, but by searching a
[GAN](/glossary/gan/)'s [latent space](/glossary/latent-space/) for a realistic face that,
when downscaled, matches the input. The catch: the original code assumes an NVIDIA GPU,
and its hosted model weights are long gone. This is the story of getting it running on an
M-series Mac in 2026.

<!--more-->

## What PULSE actually does

- The self-supervised trick: no paired hi-res/lo-res training data — it optimizes a latent
  vector so the _generated_ image downscales to the input.
- Why "it makes faces that don't exist" matters (the bias/identity caveat from the paper).

## The 2026 problem

- Six-year-old conda env, Python 3.7-era pins, dead Google Drive weight links.
- CUDA-only assumptions baked into the device handling.

## The fork changes

- **Device auto-select** (`device.py`): [CUDA](/glossary/cuda/),
  Apple Silicon ([MPS](/glossary/mps/) / [Metal](/glossary/metal/)), or CPU — overridable
  with `PULSE_DEVICE`.
- **Local weights**: load `synthesis.pt`, `mapping.pt`, and the dlib landmark predictor
  from the repo root instead of fetching from dead links.
- **Modernized `pulse.yml`**: PyTorch 2.x, Python 3.13, only the packages actually used.

## Running it on a Mac

The generic mechanics — device auto-select, the MPS fallback, dtype landmines — live in
[Porting ML projects to Apple Silicon](/deep-dives/porting-ml-to-apple-silicon/). The
PULSE-specific bits:

- Where to get the weights now (dlib's stock landmark model; StyleGAN weights).
- StyleGAN ops that don't have an MPS kernel, and how the latent optimization holds up on CPU
  fallback.

## Results & gotchas

- Sample transformations.
- Where the latent search wanders off (the key parameters: learning rate, steps, loss).
