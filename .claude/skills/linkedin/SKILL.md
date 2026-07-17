---
name: linkedin
version: 2.0.0
description: Track LinkedIn post metrics over time. LinkedIn exposes NO personal-profile analytics API, so capture is manual (read the analytics view in Chrome), storage is structured per-post JSON, and trend.py does the arithmetic. Use when Eric says "snapshot the <post>", "pull the LinkedIn metrics", "how did <post> do", or wants the trend on a post.
---

# LinkedIn metrics

There is no LinkedIn API for the numbers this skill cares about. Personal-profile
post analytics (impressions, members reached, profile views, follower gains, the
demographics breakdown) are only available in LinkedIn's own UI. Company-Page posts
have an analytics API; personal posts do not. So the loop is: read the numbers off
the page, log a structured snapshot, let the script compute deltas and trends.

Posting is deliberately NOT automated here. That funnel (draft, human publishes with
an explicit go-ahead, first-comment-with-the-link) stays manual and lives with the
`social-manager` agent. This skill only measures.

## Files

- `SKILL.md` - this file. Public (tracked in git). Never put real metrics here.
- `trend.py` - public script. Reads a post's JSON, prints the delta table + rollup.
- `posts/<slug>.json` - **gitignored**, local only. One file per post, the metric
  snapshots. This is where the real numbers live.
- `posts/<slug>.md` - **gitignored**, optional. The voice-y "Read:" narrative and the
  comment-debate log for that post (the qualitative half the JSON can't hold).
- `linked-*.md` - **gitignored**, legacy. Older prose-format metric logs. Migrate the
  numbers into `posts/<slug>.json` when you touch one.

The repo is PUBLIC on GitHub. `.gitignore` keeps `posts/` and `linked-*.md` off every
branch. If you add a new data path, gitignore it before writing a single number.

## Capturing a snapshot (read the page in Chrome)

Eric is logged into LinkedIn in Chrome. Primary capture is reading the analytics view
directly. Fallback is a pasted screenshot if the DOM is uncooperative.

1. Load the Chrome tools with one ToolSearch call (tabs_context_mcp, navigate,
   read_page / get_page_text, computer). Call `tabs_context_mcp` first.
2. Navigate to the post, or to its analytics view. LinkedIn's own-post analytics URL
   shape is `https://www.linkedin.com/analytics/post-summary/<activity-urn>/`, or open
   the post and click **View analytics**. Ask Eric for the post URL if the slug isn't
   already mapped in a `posts/<slug>.json`.
3. Read these fields off the page (expand the **Demographics** section for the
   breakdown, and the engagement row for the split):
   - Discovery: **impressions**, **members reached**
   - Profile activity: **profile viewers from this post**, **followers gained**
   - Engagement: total, then **reactions / comments / reposts / saves / sends**
   - Top demographics: job function, seniority, job title, company size, location,
     company (each is a "label: percent" pair)
4. Append the snapshot to `posts/<slug>.json` (schema below). Use array order for
   sequencing; don't invent precise clock times. Set unknown fields to `null` (e.g. an
   early "discovery only" pull has null engagement) - `trend.py` handles nulls.
5. Run `python3 trend.py posts/<slug>.json` and paste the table back to Eric with a
   short "Read:" (what the movement means for the funnel: profile-view conversion and
   credible follows matter more than raw reaction count).

## Per-post JSON schema

`posts/<slug>.json` (values below are illustrative placeholders, not real data):

```json
{
  "slug": "<kebab-slug>",
  "title": "<first line of the post>",
  "posted": "2026-01-01",
  "postUrl": "https://www.linkedin.com/feed/update/urn:li:activity:<id>/",
  "liveUrl": "https://ai.ericeaglstun.com/blog/<slug>/",
  "snapshots": [
    {
      "ts": "2026-01-01",
      "label": "first pull",
      "impressions": 0,
      "reach": 0,
      "profileViews": 0,
      "followers": 0,
      "engagements": 0,
      "reactions": 0,
      "comments": 0,
      "reposts": 0,
      "saves": 0,
      "sends": 0,
      "demographics": { "jobFunction": "Software Development 52%" }
    }
  ]
}
```

Field rules:

- `ts` is a date string; `label` disambiguates multiple pulls on one day
  ("early", "full analytics", "evening"). Snapshots are ordered by array position.
- Numeric fields are cumulative totals as shown by LinkedIn, not deltas. `trend.py`
  computes the deltas. Unknown = `null`, not `0`.
- `demographics` is a flat object of "label percent" strings; keep the latest complete
  one, older partial ones can omit it.

## trend.py

```bash
python3 trend.py posts/<slug>.json     # one post: snapshot table + deltas
python3 trend.py                        # rollup across every posts/*.json
```

Plain stdlib Python, no dependencies (repo convention). It prints a cumulative table
with per-snapshot deltas, the latest demographics, and (rollup mode) latest totals
across all tracked posts. It never writes; it only reads the JSON you logged.
