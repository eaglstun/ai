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

TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
USER = os.environ.get("THREADS_USER_ID", "").strip()
if not TOKEN or not USER:
    sys.exit("set THREADS_ACCESS_TOKEN and THREADS_USER_ID (e.g. `source .env`)")

OUT = sys.argv[1] if len(sys.argv) > 1 else "meta/metrics"
CAPTURED_AT = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def fetch_posts():
    """All posts, following pagination."""
    posts = []
    url = (f"{API}/{USER}/threads?"
           + urllib.parse.urlencode({
               "fields": "id,media_type,text,permalink,timestamp",
               "limit": 100, "access_token": TOKEN}))
    while url:
        d = _get(url)
        posts.extend(d.get("data", []))
        url = d.get("paging", {}).get("next")
    return posts


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
    idx = ["# Threads metrics — latest standings", "",
           f"_updated {CAPTURED_AT} · {len(latest)} posts · {n_caps} snapshot(s) logged_", "",
           "| post | posted | " + " | ".join(METRICS) + " |",
           "|---|---|" + "|".join(["---"] * len(METRICS)) + "|"]
    for r in latest:
        snippet = (r.get("text") or "").replace("\n", " ").strip()
        snippet = (snippet[:47] + "…") if len(snippet) > 48 else snippet
        posted = (r.get("posted_at") or "")[:10]
        link = f"[{snippet or r['slug']}]({r.get('permalink','')})"
        idx.append(f"| {link} | {posted} | "
                   + " | ".join(str(r.get(m, 0)) for m in METRICS) + " |")
    with open(os.path.join(OUT, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    return latest, n_caps


def main():
    posts = fetch_posts()
    append_snapshot(posts)
    latest, n_caps = regenerate(load_log())
    print(f"captured {CAPTURED_AT} · {len(posts)} posts · {n_caps} snapshot(s) total")
    print(f"wrote {OUT}/data.jsonl, {OUT}/index.md, {OUT}/posts/*.md")


if __name__ == "__main__":
    main()
