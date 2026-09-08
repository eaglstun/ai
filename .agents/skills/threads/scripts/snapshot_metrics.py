#!/usr/bin/env python3
"""Snapshot Threads post metrics into meta/metrics/ for trend tracking.

Reads THREADS_ACCESS_TOKEN / THREADS_USER_ID from the environment. Each run:
  1. fetches every post + its insights from the Threads API,
  2. appends one timestamped record per post to data.jsonl (append-only source
     of truth — never rewritten, so the history is durable),
  3. regenerates readable views from that log: posts/<slug>.md (per-post history
     table) and index.md (latest standings, sorted by views).

Run it on whatever cadence you like; each run is one row in every post's history.

Usage:
  THREADS_ACCESS_TOKEN=... THREADS_USER_ID=... snapshot_metrics.py [out_dir]
    out_dir default: meta/metrics
"""
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

API = "https://graph.threads.net/v1.0"
METRICS = ["views", "likes", "replies", "reposts", "quotes"]
# account-level metrics Threads exposes via threads_insights. "following" is NOT
# available through the API (only the app/profile page shows it) — tracked manually.
ACCOUNT_METRICS = ["followers_count", "views", "likes", "replies", "reposts", "quotes", "clicks"]

TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
USER = os.environ.get("THREADS_USER_ID", "").strip()
if not TOKEN or not USER:
    sys.exit("set THREADS_ACCESS_TOKEN and THREADS_USER_ID (e.g. `source .env`)")

OUT = sys.argv[1] if len(sys.argv) > 1 else "meta/metrics"
CAPTURED_AT = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def _fetch_all(edge):
    """Every item on a user edge (threads | replies), following pagination."""
    items = []
    url = (f"{API}/{USER}/{edge}?"
           + urllib.parse.urlencode({
               "fields": "id,media_type,text,permalink,timestamp",
               "limit": 100, "access_token": TOKEN}))
    while url:
        d = _get(url)
        items.extend(d.get("data", []))
        url = d.get("paging", {}).get("next")
    return items


def fetch_posts():
    """Top-level posts (kind=post) + your replies on others' threads (kind=reply).

    `/{user}/threads` returns ONLY top-level posts; replies you leave elsewhere
    live on `/{user}/replies` and out-reach your own posts (they ride bigger
    accounts' threads), so both are tracked here, tagged by `kind`.
    """
    posts = [{**p, "kind": "post"} for p in _fetch_all("threads")]
    replies = [{**r, "kind": "reply"} for r in _fetch_all("replies")]
    return posts + replies


def fetch_insights(post_id):
    url = (f"{API}/{post_id}/insights?"
           + urllib.parse.urlencode({"metric": ",".join(METRICS), "access_token": TOKEN}))
    out = {m: 0 for m in METRICS}
    try:
        d = _get(url)
    except Exception:
        return out  # brand-new posts can 400 on insights; treat as zeros
    for m in d.get("data", []):
        v = m.get("total_value", {}).get("value")
        if v is None:
            vals = m.get("values") or [{}]
            v = vals[-1].get("value", 0)
        out[m["name"]] = v
    return out


def fetch_account(n_posts, n_replies):
    """One account-level snapshot: profile + insights + derived post/reply counts.

    Returns a clean dict with NO access_token in it (the raw insights response
    embeds the token in paging URLs, so only named values are lifted out).
    `following_count` is None because the Threads API does not expose it.
    """
    rec = {"captured_at": CAPTURED_AT, "post_count": n_posts, "reply_count": n_replies,
           "following_count": None}
    # following isn't in the API; read a manual count from meta/metrics/following.txt
    # if present (one integer), so it still rides the time series.
    try:
        with open(os.path.join(OUT, "following.txt"), encoding="utf-8") as f:
            rec["following_count"] = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        pass
    # profile node
    try:
        purl = (f"{API}/{USER}?"
                + urllib.parse.urlencode({"fields": "username,name,threads_biography",
                                          "access_token": TOKEN}))
        p = _get(purl)
        rec["username"] = p.get("username")
        rec["name"] = p.get("name")
        rec["biography"] = p.get("threads_biography")
    except Exception:
        pass
    # account insights — lift only named metric values, never raw paging URLs
    for m in ACCOUNT_METRICS:
        rec[m] = 0
    try:
        iurl = (f"{API}/{USER}/threads_insights?"
                + urllib.parse.urlencode({"metric": ",".join(ACCOUNT_METRICS),
                                          "access_token": TOKEN}))
        d = _get(iurl)
        for m in d.get("data", []):
            tv = m.get("total_value", {}).get("value")
            if tv is None:  # views comes back as a daily series, not a total
                vals = m.get("values") or [{}]
                tv = vals[-1].get("value", 0)
            rec[m["name"]] = tv
    except Exception:
        pass
    return rec


def append_account(rec):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "account.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def regenerate_account():
    path = os.path.join(OUT, "account.jsonl")
    if not os.path.exists(path):
        return
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if not rows:
        return
    rows.sort(key=lambda r: r["captured_at"])
    head = rows[-1]
    cols = ["followers_count", "following_count", "post_count", "reply_count",
            "clicks", "views", "likes", "replies", "reposts", "quotes"]
    lines = [f"# Account standings — @{head.get('username','?')}", "",
             f"_updated {head['captured_at']} · {len(rows)} snapshot(s) logged_", "",
             f"**Followers:** {head.get('followers_count','?')}  ·  "
             f"**Following:** {head.get('following_count') if head.get('following_count') is not None else 'n/a (not in API)'}  ·  "
             f"**Posts:** {head.get('post_count','?')}  ·  **Replies:** {head.get('reply_count','?')}",
             "",
             "| captured (UTC) | " + " | ".join(cols) + " |",
             "|---|" + "|".join(["---"] * len(cols)) + "|"]
    for r in rows:
        def cell(c):
            v = r.get(c)
            return "n/a" if (c == "following_count" and v is None) else str(v if v is not None else 0)
        lines.append("| " + r["captured_at"] + " | " + " | ".join(cell(c) for c in cols) + " |")
    with open(os.path.join(OUT, "account.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def slug_for(post):
    """Last path segment of the permalink, else the post id."""
    pl = post.get("permalink", "")
    seg = pl.rstrip("/").rsplit("/", 1)[-1] if pl else ""
    return seg or post["id"]


def append_snapshot(posts):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "data.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        for p in posts:
            rec = {
                "captured_at": CAPTURED_AT,
                "id": p["id"],
                "slug": slug_for(p),
                "posted_at": p.get("timestamp"),
                "permalink": p.get("permalink"),
                "media_type": p.get("media_type"),
                "kind": p.get("kind", "post"),
                "text": p.get("text", ""),
                **fetch_insights(p["id"]),
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_log():
    path = os.path.join(OUT, "data.jsonl")
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def regenerate(rows):
    by_post = {}
    for r in rows:
        by_post.setdefault(r["id"], []).append(r)

    # per-post history files
    posts_dir = os.path.join(OUT, "posts")
    os.makedirs(posts_dir, exist_ok=True)
    latest = []
    for pid, snaps in by_post.items():
        snaps.sort(key=lambda r: r["captured_at"])
        head = snaps[-1]
        latest.append(head)
        lines = [f"# {head['slug']}  ·  posted {head.get('posted_at','?')}", ""]
        text = (head.get("text") or "").strip()
        if text:
            lines += ["> " + text.replace("\n", "\n> "), ""]
        if head.get("permalink"):
            lines += [head["permalink"], ""]
        lines += ["| captured (UTC) | " + " | ".join(METRICS) + " |",
                  "|---|" + "|".join(["---"] * len(METRICS)) + "|"]
        for s in snaps:
            lines.append("| " + s["captured_at"] + " | "
                         + " | ".join(str(s.get(m, 0)) for m in METRICS) + " |")
        with open(os.path.join(posts_dir, f"{head['slug']}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    # index: latest standings, sorted by views desc
    latest.sort(key=lambda r: (r.get("views") or 0), reverse=True)
    n_caps = len({r["captured_at"] for r in rows})
    n_posts = sum(1 for r in latest if r.get("kind", "post") == "post")
    n_replies = len(latest) - n_posts
    idx = ["# Threads metrics — latest standings", "",
           f"_updated {CAPTURED_AT} · {n_posts} posts · {n_replies} replies · {n_caps} snapshot(s) logged_", "",
           "| kind | post | posted | " + " | ".join(METRICS) + " |",
           "|---|---|---|" + "|".join(["---"] * len(METRICS)) + "|"]
    for r in latest:
        snippet = (r.get("text") or "").replace("\n", " ").strip()
        snippet = (snippet[:47] + "…") if len(snippet) > 48 else snippet
        posted = (r.get("posted_at") or "")[:10]
        kind = r.get("kind", "post")
        link = f"[{snippet or r['slug']}]({r.get('permalink','')})"
        idx.append(f"| {kind} | {link} | {posted} | "
                   + " | ".join(str(r.get(m, 0)) for m in METRICS) + " |")
    with open(os.path.join(OUT, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    return latest, n_caps


def main():
    posts = fetch_posts()
    append_snapshot(posts)
    latest, n_caps = regenerate(load_log())
    n_reply = sum(1 for p in posts if p.get("kind") == "reply")
    n_post = len(posts) - n_reply

    acct = fetch_account(n_post, n_reply)
    append_account(acct)
    regenerate_account()

    print(f"captured {CAPTURED_AT} · {n_post} posts · {n_reply} replies · {n_caps} snapshot(s) total")
    print(f"account · {acct.get('followers_count','?')} followers · "
          f"{acct.get('clicks','?')} clicks · following n/a (not in API)")
    print(f"wrote {OUT}/data.jsonl, {OUT}/index.md, {OUT}/posts/*.md, "
          f"{OUT}/account.jsonl, {OUT}/account.md")


if __name__ == "__main__":
    main()
