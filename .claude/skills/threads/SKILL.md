---
name: threads
description: Post, reply, and read on your Threads account via Meta's official Threads API (graph.threads.net). Use when publishing a post or reply from the inbox/meta workspace, automating the draft-to-post funnel, tracking post metrics over time, or refreshing the OAuth token.
metadata: meta
version: 1.1.0
---

# Threads API

Posting, replying, and reading metrics on your account via Meta's official Threads API.
Turns a draft in `inbox/*.md` / `meta/posts/` into a live post **as you**, and serves the
funnel from `meta/strategy.md`: a post, someone feels something, they click, they read the
site.

**Status: live once wired.** Token is in `.env` (`THREADS_ACCESS_TOKEN` / `THREADS_USER_ID`),
all five scopes ready, account wired as a Threads Tester. The token is 60-day, so **refresh
before it expires** (see `references/setup.md`).

## The three scripts are the interface

Reach for raw curl only for one-offs; otherwise use these (run from repo root, they read
`.env`):

```bash
# Post or reply from a draft's "## ✅ Pick:" block. DRY-RUN BY DEFAULT.
scripts/post-draft.sh inbox/<handle>.md               # preview the ✅ Pick block
scripts/post-draft.sh --pick B inbox/<handle>.md      # preview a specific A/B/C block
scripts/post-draft.sh --reply-to <MEDIA_ID> draft.md  # stage a reply
scripts/post-draft.sh --post inbox/<handle>.md        # ACTUALLY PUBLISH (as you)

# Snapshot every post's metrics into meta/metrics/ (append-only time series).
scripts/snapshot-metrics.sh

# Pull the replies YOU left on other people's threads, with engagement. Read-only.
scripts/pull-replies.sh --date 2026-07-25    # one local day
scripts/pull-replies.sh --days 30
```

`post-draft.sh` extracts the chosen block (`extract_pick.py`), strips `>` markers, unwraps
soft line-wraps, enforces the 500-char limit, and warns on markdown emphasis (Threads renders
none). `snapshot-metrics.sh` appends to `meta/metrics/data.jsonl` and regenerates
`index.md` + `posts/<slug>.md`. Both `meta/` and `.env` are gitignored.

## Before you publish

- **No undo.** A publish is public and permanent, and it posts **as you**, so confirm the exact
  text, and never `--post` without an explicit go-ahead.
- **Dry-run first.** It's the default for a reason; eyeball the preview + char count.
- **500-char limit.** The pick block's `(NNN)` count is the pre-check.

## Drafts: the pick format

`inbox/*.md` replies and `meta/posts/` drafts use a `## ✅ Pick:` heading over the chosen text,
with a `(NNN)` char count under it. A/B/C alternates live under `## B —` / `## C —` headings
(these em-dash headings are a parser token; leave them as-is). `post-draft.sh --pick <LETTER>`
selects one.

**Only the post text goes under the heading.** The extractor takes every line between the
heading and the `(NNN)` count (or `---` / next `##`), so a "why this one" rationale paragraph
sitting under a pick heading gets published as part of the post. Put rationale ABOVE the pick
headings, in the draft's preamble. (Learned on post 006: the dry-run came back 739/500 with
the bucket notes glued to the top. The dry-run default exists precisely to catch this.)

## Pulling your own replies: ALWAYS capture the parent posts

`/{user-id}/threads` returns only top-level posts, so the replies you leave on other people's
threads are invisible to it and to `snapshot-metrics.sh`. Since replies out-reach own posts by
an order of magnitude here, that blind spot is most of the account's real reach. Pull it with
`scripts/pull-replies.sh`.

**A pull is not finished when the script exits.** It gives you your half of every conversation
and the API cannot give you the other half: `root_post` / `replied_to` come back populated
**only when the parent is your own post**, and are silently absent otherwise (a small
fraction on the day this was measured). curl, `/embed`, oEmbed, and WebFetch all fail to
recover it too. The full autopsy is in `references/api.md`, "The API will not give you the
post you replied to."

So every reply pull ends with a browser pass, no exceptions:

1. Run `scripts/pull-replies.sh --date <YYYY-MM-DD>` (or `--days N`). It writes
   `meta/replies/inbound/<label>.json` (archive) and `<label>.md` (work-list, one block per
   reply, `status: needs-parent`).
2. Open each block's permalink in the **logged-in browser** (Chrome tools preferred; the
   devtools inspector-paste fallback below works when the extension is offline) and read the
   post sitting above your reply.
3. Fill `parent_author` and `parent_text` in the block, flip `status:` to `captured`.

**Never report a reply pull as done while blocks are still `needs-parent`.** Say how many are
unresolved and why. A reply without its parent is a non sequitur: you cannot tell whether it
landed, cannot mine it for site copy, and six weeks on nobody can reconstruct what it answered.
If the browser is unavailable, hand back the numbers plus the unresolved count, and say the
capture is pending rather than calling it finished.

## Capturing an external post to reply to

The official API reads **your own** content; it can't pull an arbitrary third party's post
by its URL shortcode. So to capture someone else's post (to draft a reply to), use **WebFetch**,
not the API:

1. `WebFetch` the post URL (`https://www.threads.com/@handle/post/<SHORTCODE>`) with a prompt
   asking for verbatim author, post text (preserve line breaks), timestamp, and like/reply
   counts, and to say what's present if the content is JS-gated. Public posts come back via
   the page's og/embedded data.
2. **Caveat: WebFetch extracts with a small model, so treat wording as ~95% not 100%.** For
   anything you'll quote publicly, verify against the live post (open it in the browser). Record
   the fetch date; engagement counts are point-in-time.
3. **The reply thread is JS-gated.** WebFetch/og data returns only the comment _count_, not the
   comments. To capture the actual replies (often the most useful part, they reveal whether a
   post is earnest or a bit), pick one:
   - **Browser (preferred):** drive the live page with the Chrome tools and read the rendered
     comments. Needs the extension connected, so launch Chrome with it enabled.
   - **Inspector-paste fallback (browser offline):** in a browser, open the post, expand the
     replies, and copy the rendered comment block from devtools (right-click, Inspect on the
     thread container, Copy, Outer/Inner HTML) into `meta/replies/<SHORTCODE>.html`. Then parse
     it with stdlib `html.parser` (no bs4 needed): mark each `<a href="/@handle">` as an author,
     emit text nodes in order (skip `<script>`/`<style>`), and reconstruct who-said-what.
     Caveat: the dump only contains replies that were actually loaded in the DOM (scroll/expand
     first; lazy-loaded ones below the fold won't be there).
4. Write the capture to `meta/replies/<SHORTCODE>.md`: frontmatter (`source`, `shortcode`,
   `author`, `fetched`, `reply_to_media_id`, `status`), the quoted **Original post**, a **Replies**
   list (author + verbatim text + the OP's `· Author` responses), a short **The read** (genre +
   your angle), and a **Reply drafts** section in the `## ✅ Pick:` format above.
5. **To actually post the reply** you need the target's **numeric media ID** (`reply_to_media_id`).
   The URL shortcode is not it, and the API has no clean shortcode-to-id lookup for other people's
   posts. Resolve it (or reply from the app) before `post-draft.sh --reply-to`.

## Load on demand

- **`references/setup.md`** for auth, scopes, the token lifecycle + **how to refresh/rebuild the
  token**, app/account IDs, callback URLs, the Meta-dashboard setup, and security.
  Read this for anything token- or account-config-related.
- **`references/api.md`** for the raw endpoint reference: the two-step create-then-publish,
  container params, replies, reading conversations and your own replies' metrics, insights, and
  rate limits. Read this for curl details the scripts don't cover.
