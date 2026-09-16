+++
title = "Checkpoint"
summary = "A saved snapshot of a model's weights partway through training, so a run can be resumed, compared, or rolled back - and the best-scoring one is not automatically the best model."
category = "Core concepts"
related = ["parameters", "val-loss", "lora", "gradient-descent", "gguf"]
plain = "The save file. You're deep into a long game, so you save, and save again, and the folder fills up with versions of yourself at different points in the fight. Two things people forget: a proper save records not just where you're standing but which way you were running, and the save with the highest score on the scoreboard is not always the one you actually want to load. Sometimes the run went best a little before the number peaked."
tags = ["checkpoint", "training", "parameters", "lora", "val-loss"]
semantic_id = "mqoNpCSl0oiicn5VmOrMwfnHLgfAoAAG"
+++
A **checkpoint** is a saved snapshot of a model's [parameters](/glossary/parameters/) at one moment during
training, written to disk so the run can be resumed, compared against other moments, or
rolled back. Training is a long downhill walk (see [gradient descent](/glossary/gradient-descent/)); a checkpoint is a
photograph of exactly where the weights were standing at step N.

A full checkpoint holds more than the weights. It also carries the optimizer state, the
running momentum and per-parameter statistics the training algorithm has built up, because
without those you can _run_ the model but you cannot cleanly _continue_ the run: restart
from weights alone and the optimizer has to rebuild its momentum from a standing start.
Weights-only files are still called checkpoints, and are what you want for inference or
publishing, just not for resuming.

Frequency is a storage tradeoff. Each checkpoint is a complete copy of the model, so a
common pattern is to save every N steps, keep only the most recent few, and separately keep
whichever one scored best. With [LoRA](/glossary/lora/) the arithmetic changes completely: the checkpoint
is the adapter alone, megabytes instead of gigabytes, which is why adapter training can
afford to keep every step it ever took.

"Best" is usually scored by [validation loss](/glossary/val-loss/), and this is the part worth knowing: the
lowest-validation-loss checkpoint is not automatically the model you want. Loss measures one
narrow thing, how surprised the model is by held-out text. A run can reach its best number
at a step where the behavior you were actually training is not there yet, or has already
been trained past. Checkpoints are the only way to see this at all, because probing several
from the same run turns "did this work" into a sequence you can watch a behavior arrive in,
or fail to.

The word does double duty. Outside of training, "checkpoint" is also the generic term for a
distributed file of trained weights, `.ckpt` and `.safetensors` files and the like, which is
the sense meant when an image or language model is described as having several checkpoints
available to download (see [GGUF](/glossary/gguf/) for the local-inference packaging of the same idea).
