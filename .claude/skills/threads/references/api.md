# Threads API — endpoint reference

Base host: `https://graph.threads.net/v1.0`. All content calls hit `graph.threads.net`; only
the OAuth _authorize_ screen is on `threads.net`. Every call needs `access_token=…`.

The scripts (`post-draft.sh`, `snapshot-metrics.sh`) wrap most of this — reach for raw curl
only for one-offs the scripts don't cover.

## Posting is two steps: create a container, then publish it

Nothing goes live in one call. Build a _media container_, then publish its id.

```bash
# 1. create the container
CREATE=$(curl -s -X POST "https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads" \
  -d "media_type=TEXT" \
  --data-urlencode "text=The wince is the lift." \
  -d "access_token=${THREADS_ACCESS_TOKEN}")
CONTAINER_ID=$(echo "$CREATE" | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

# 2. publish it
curl -s -X POST "https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads_publish" \
  -d "creation_id=${CONTAINER_ID}" \
  -d "access_token=${THREADS_ACCESS_TOKEN}"
```

Always `--data-urlencode` the `text` — em-dashes, quotes, and newlines mangle a plain `-d`.
A created-but-unpublished container is a safe way to test the publish permission without
anything going live (it just expires unused).

### Container create params (`POST /{user-id}/threads`)

| Param              | Notes                                                                                                    |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| `media_type`       | `TEXT` \| `IMAGE` \| `VIDEO` \| `CAROUSEL` (required)                                                    |
| `text`             | the post body; **500-char limit**; required for `TEXT`                                                   |
| `image_url`        | required for `IMAGE`; must be a **public** URL Meta can fetch                                            |
| `video_url`        | required for `VIDEO`; processing is async — poll status before publish                                   |
| `children`         | comma-separated container ids for `CAROUSEL` (2–20 items)                                                |
| `is_carousel_item` | `true` on each child container                                                                           |
| `reply_to_id`      | media id to reply under (see replies)                                                                    |
| `reply_control`    | `everyone` \| `accounts_you_follow` \| `mentioned_only` \| `parent_post_author_only` \| `followers_only` |
| `link_attachment`  | URL preview, **text-only** posts — good for back-linking to the site                                     |
| `topic_tag`        | 1–50 chars, no `.` or `&`                                                                                |

> Images/video need a **public URL**, not a file upload — Meta fetches the asset. Host it on
> the droplet / CDN first, then pass the URL.

## Replies

A reply is a container with `reply_to_id` set, published the same two-step way:

```bash
curl -s -X POST "https://graph.threads.net/v1.0/${THREADS_USER_ID}/threads" \
  -d "media_type=TEXT" --data-urlencode "text=Love this. One small flip…" \
  -d "reply_to_id=<THEIR_POST_MEDIA_ID>" -d "access_token=${THREADS_ACCESS_TOKEN}"
# …then /threads_publish with the returned container id
```

Getting `<THEIR_POST_MEDIA_ID>` is the hard part — the API is **your-account-scoped**, so
there's no clean "look up any public post by URL." For cold replies to others, copy-paste from
the app is often still the path.

**Read replies / conversations** (for a thread you posted):

- `GET /{media-id}/replies` — direct replies to a post
- `GET /{media-id}/conversation` — the full nested thread (returns continuations; same-second
  timestamps mean order comes from content, not the API)
- `GET /{media-id}/manage_reply` with `hide=true|false` — hide/unhide a reply

## Insights

- **Per post:** `GET /{media-id}/insights?metric=views,likes,replies,reposts,quotes&access_token=…`
- **Per account:** `GET /{user-id}/threads_insights?metric=views,likes,replies,followers_count,…`
- **All posts:** `GET /{user-id}/threads?fields=id,media_type,text,permalink,timestamp` (paginate via `paging.next`)

Insights give Threads-side engagement, **not** outbound clicks to the site. For the funnel's
"did they click" question, put `?utm_source=threads` on the link and read the site's own
analytics. `snapshot-metrics.sh` already wraps the per-post + all-posts calls into a tracked
time series.

> Account-level `threads_insights` responses include the **access token in the paging URLs** —
> don't paste those URLs anywhere.

## Rate limits

- **Publishing:** 250 published posts / rolling 24h, per user.
- **Replies:** ~1,000 / 24h (Meta's published figure — confirm in the dashboard before relying).
- **General calls:** `4800 × impressions` over 24h — more reach buys more budget. A 3–5
  post/week cadence never gets close.
