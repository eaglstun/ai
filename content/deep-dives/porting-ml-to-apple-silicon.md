+++
title = "Dragging CUDA-Only AI onto a Mac Without Losing Your Mind"
date = 2026-05-21
draft = true
summary = "The recurring moves for getting a CUDA-first PyTorch project running on an M-series Mac — device selection, MPS fallbacks, dtype landmines, and dependency archaeology. The shared groundwork behind the individual ports."
+++

Most interesting ML code was written assuming an NVIDIA GPU. Getting it onto an M-series Mac
is the same handful of moves over and over — so here they are in one place. The individual
case studies (PULSE, AudioCraft, …) link back here for the common parts instead of repeating
them.

<!--more-->

## 1. Device selection

- The `device.py` pattern: pick [MPS](/glossary/mps/) → [CUDA](/glossary/cuda/) → CPU in
  order, with an env-var override (`*_DEVICE=cpu`) for debugging.
- Stop hardcoding `.cuda()` / `device="cuda"`; thread one `DEVICE` through instead.

## 2. The MPS fallback

- `PYTORCH_ENABLE_MPS_FALLBACK=1` — what it does and why you usually need it.
- How to find the op that isn't implemented on [Metal](/glossary/metal/) yet, and decide
  whether to pin it to CPU or rewrite it.

## 3. Dtype landmines

- No `float64` on MPS — the most common crash, and the fix.
- `bf16` vs `fp16` support on Apple silicon; where precision bites
  ([tensor](/glossary/tensor/) dtype refresher).

## 4. Dependency archaeology

- `xformers`, `bitsandbytes`, `triton` — CUDA-only packages that must be made optional.
- Modernizing six-year-old pins (Python, PyTorch 2.x) without breaking the model.
- System deps that aren't pip: `ffmpeg`, dlib, etc.

## 5. Dead weights

- Hosted model links rot. Load from local files first, download only as a fallback.
- Where the canonical weights actually live now (HuggingFace, dlib's site, …).

## 6. Sanity-checking the port

- A tiny forward pass on each device; confirming MPS output matches CPU within tolerance.
- Realistic performance expectations — what [parameters](/glossary/parameters/) count is
  usable on which Mac.

---

**Case studies:**

- [Reviving PULSE on Apple Silicon](/deep-dives/reviving-pulse-apple-silicon/)
- [Running AudioCraft (MusicGen) on Apple Silicon](/deep-dives/audiocraft-apple-silicon/)
