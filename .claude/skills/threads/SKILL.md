---
name: threads
description: Post, reply, and read on Eric's Threads account via Meta's official Threads API (graph.threads.net). Use when publishing a post or reply from the inbox/meta workspace, automating the draft→post funnel for ai.ericeaglstun.com, tracking post metrics over time, or refreshing the OAuth token.
metadata: meta
version: 1.1.0
---

# Threads API (Eric's account)

Posting, replying, and reading metrics on `@eaglstun.ai` via Meta's official Threads API.
Turns a draft in `inbox/*.md` / `meta/posts/` into a live post **as Eric**, and serves the
funnel from `meta/strategy.md`: **post → someone feels something → they click → they read the
site.**

**Status: live.** Token is in `.env` (`THREADS_ACCESS_TOKEN` / `THREADS_USER_ID`), all five
scopes ready, account wired as a Threads Tester. Token is 60-day — **refresh before it
expires** (see `references/setup.md`).

## The two scripts are the interface

Reach for raw curl only for one-offs; otherwise use these (run from repo root, they read
`.env`):

```bash
# Post or reply from a draft's "## ✅ Pick:" block. DRY-RUN BY DEFAULT.
scripts/post-draft.sh inbox/yugshende94.md            # preview the ✅ Pick block
scripts/post-draft.sh --pick B inbox/graelanf.md      # preview a specific A/B/C block
scripts/post-draft.sh --reply-to <MEDIA_ID> draft.md  # stage a reply
scripts/post-draft.sh --post inbox/yugshende94.md     # ACTUALLY PUBLISH (as Eric)

# Snapshot every post's metrics into meta/metrics/ (append-only time series).
scripts/snapshot-metrics.sh
```

`post-draft.sh` extracts the chosen block (`extract_pick.py`), strips `>` markers, unwraps
soft line-wraps, enforces the 500-char limit, and warns on markdown emphasis (Threads renders
none). `snapshot-metrics.sh` appends to `meta/metrics/data.jsonl` and regenerates
`index.md` + `posts/<slug>.md`. Both `meta/` and `.env` are gitignored.

## Before you publish

- **No undo.** A publish is public and permanent, and it posts **as Eric** — confirm the exact
  text, and never `--post` without an explicit go-ahead.
- **Dry-run first.** It's the default for a reason; eyeball the preview + char count.
- **500-char limit.** The pick block's `(NNN)` count is the pre-check.

## Drafts: the pick format

`inbox/*.md` replies and `meta/posts/` drafts use a `## ✅ Pick:` heading over the chosen text,
with a `(NNN)` char count under it (see `inbox/graelanf.md`, `inbox/yugshende94.md`). A/B/C
alternates live under `## B —` / `## C —` headings. `post-draft.sh --pick <LETTER>` selects one.

## Load on demand

- **`references/setup.md`** — auth, scopes, the token lifecycle + **how to refresh/rebuild the
  token**, app/account IDs, callback URLs, the Meta-dashboard setup that was done, security.
  Read this for anything token- or account-config-related.
- **`references/api.md`** — raw endpoint reference: the two-step create→publish, container
  params, replies, reading conversations, insights, rate limits. Read this for curl details the
  scripts don't cover.
