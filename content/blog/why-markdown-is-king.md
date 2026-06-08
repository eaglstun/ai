+++
title = "Markdown Won. Here's Why — and How to Speak It"
date = 2026-06-05
draft = true
summary = "Plain text that reads fine raw and renders everywhere — and, not coincidentally, the language LLMs speak. Why Markdown won, and the handful of syntax you actually need."
+++

If you work with AI at all, you're already swimming in Markdown — it's what you type into a
chat and what the model types back, what every README and agent-instruction file is written
in. That's not an accident. Markdown is plain text that's readable raw _and_ renders cleanly
everywhere, which makes it the closest thing we have to a universal format for writing. Here's
why it won, and the basics to get going.

<!--more-->

## Why it's king

- **It's just text.** No proprietary format, no lock-in; openable in anything, forever.
- **Readable both ways.** The raw file is legible on its own; rendered, it's clean.
- **Diff-friendly.** Plays perfectly with git — you can see exactly what changed.
- **Renders everywhere.** GitHub, this site, notes apps, chat windows.
- **The format AI speaks.** LLMs are trained on mountains of it, so they read and write it
  natively — it's the path of least friction between you and a model.

## The basics you actually need

- **Headings:** `#`, `##`, `###` …
- **Emphasis:** `*italic*`, `**bold**`.
- **Lists:** `-` for bullets, `1.` for numbered.
- **Links & images:** `[text](url)` and `![alt](url)`.
- **Code:** `` `inline` `` and triple-backtick fenced blocks (with a language for highlighting).
- **Blockquotes:** `>`.
- **Tables:** pipes and dashes.

## Where to go from here

- Flavors: CommonMark vs. GitHub-Flavored Markdown (task lists, tables, strikethrough).
- Front matter (the `+++`/`---` block) for metadata — how this very site works.
- When to reach for it vs. a real word processor.
