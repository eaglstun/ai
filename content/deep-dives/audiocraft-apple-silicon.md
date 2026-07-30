+++
title = "Teaching My MacBook to Write Music (No NVIDIA Required)"
date = 2026-08-09
draft = true
summary = "Meta's MusicGen and AudioGen assume CUDA and xformers. Here's getting them generating audio on an M-series Mac - what ports cleanly to MPS, and what falls back to the CPU."
tags = ["apple-silicon", "music-generation", "mps", "transformer"]
semantic_id = "cDVwp8E6PRQG8aNhbveXU8LHSdT7EAsO"
related_by_meaning = ["/practice/talkie-on-apple-silicon/", "/deep-dives/porting-ml-to-apple-silicon/", "/glossary/metal/", "/deep-dives/ctranslate2-metal-backend/03-msl-indignities/"]
+++

[AudioCraft](https://github.com/oo-eric/audiocraft) is Meta's PyTorch library for audio
generation - **MusicGen** (text- and melody-conditioned music) and **AudioGen** (sound
effects), both built on a [transformer](/glossary/transformer/) that predicts audio tokens,
plus the **EnCodec** neural codec that turns waveforms into those tokens. Out of the box it
leans on CUDA and `xformers`. This is getting it running on an M-series Mac.

<!--more-->

## How MusicGen works (the short version)

- EnCodec compresses audio into discrete tokens; MusicGen is a
  [transformer](/glossary/transformer/) language model _over those tokens_.
- Text conditioning via a separate text encoder; melody conditioning via chromagrams.

## The Apple Silicon path

The general moves - [MPS](/glossary/mps/) device selection, the CPU fallback,
[tensor](/glossary/tensor/) dtype landmines - are covered in
[Porting ML projects to Apple Silicon](/deep-dives/porting-ml-to-apple-silicon/). The
AudioCraft-specific bits:

- `xformers` is optional and skipped automatically on macOS ARM - what replaces it, and the
  attention path that runs without it.
- EnCodec vs. the MusicGen transformer: which one actually wants the GPU.

## Performance reality

- CPU works for every model but is slow (minutes for medium); MPS speedup in practice.
- Which model size ([parameters](/glossary/parameters/)) is actually usable on a given Mac.

## Generating something

- Minimal MusicGen script: prompt → wav.
- `ffmpeg` setup, sample rate / duration knobs, melody conditioning.
