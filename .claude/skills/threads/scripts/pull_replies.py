#!/usr/bin/env python3
"""
pull_replies.py - pull the replies YOU left on other people's threads, with engagement,
and stage the parent-post capture that the API cannot give you.

Why this exists as its own script: `/{user-id}/threads` returns ONLY your top-level posts.
Every reply you leave on someone else's thread is invisible to it, and invisible to
snapshot-metrics.sh. Since replies out-reach top-level posts by an order of magnitude on
this account, that blind spot is most of the account's actual reach.

THE HALF-A-CONVERSATION PROBLEM (measured 2026-07-26, the reason for the .md work-list):

    A reply without the post it answers is unusable. It reads as a non sequitur, you cannot
    judge whether it landed, and you certainly cannot mine it for site copy. So every pull
    MUST end with the parent posts captured. The API will not do it for you:

      - `/{user-id}/replies?fields=...,root_post{...},replied_to{...}` silently DROPS both
        fields. No error, no null, the keys are simply absent from every record. Same on a
        direct `GET /{reply-id}`. Meta appears to populate them only inside conversations
        you own.
      - curl on the reply permalink returns a ~256KB JavaScript shell: no og tags, not even
        your own reply text in the HTML.
      - `/embed` and the oEmbed paths serve that same shell.
      - WebFetch renders your reply but NOT the parent post above it.

    What is left is the logged-in browser, which is why this script stops at staging the
    work rather than pretending it finished. It writes a markdown work-list with an empty
    parent slot per reply; a browser pass fills them in. See SKILL.md, "Pulling your own
    replies."

Usage (from the repo root, so it picks up .env and meta/):
    scripts/pull-replies.sh                      # last 7 days
    scripts/pull-replies.sh --date 2026-07-25    # one local day
    scripts/pull-replies.sh --days 30
    scripts/pull-replies.sh --no-insights        # skip the per-reply calls (1 request total)

Writes (both gitignored, meta/ is its own private repo):
    meta/replies/inbound/<label>.json   raw records + insights, the archive
    meta/replies/inbound/<label>.md     the work-list, one block per reply, parent slot empty
"""

import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.request
import zoneinfo
from pathlib import Path

API = "https://graph.threads.net/v1.0"
LOCAL = zoneinfo.ZoneInfo("America/Boise")
# root_post/replied_to are requested deliberately. They come back empty today (see the
# module docstring), but asking costs nothing and the day Meta populates them this script
# starts resolving parents for free. Check `parents_from_api` in the summary.
FIELDS = ("id,text,permalink,timestamp,is_reply,has_replies,"
          "root_post{id,permalink,username,text},replied_to{id,permalink,username,text}")
METRICS = "views,likes,replies,reposts,quotes"


def get(url, timeout=45):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.load(r)


def fetch_replies(uid, token, max_pages=20):
    url = f"{API}/{uid}/replies?fields={FIELDS}&limit=100&access_token={token}"
    rows, pages = [], 0
    while url and pages < max_pages:
        try:
            d = get(url)
        except urllib.error.HTTPError as e:
            sys.exit(f"HTTP {e.code} from /replies: {e.read().decode()[:400]}")
        rows += d.get("data", [])
        # NOTE: paging.next carries the access token. Never print or commit these URLs.
        url = d.get("paging", {}).get("next")
        pages += 1
    return rows


def add_insights(rows, token):
    for r in rows:
        try:
            d = get(f"{API}/{r['id']}/insights?metric={METRICS}&access_token={token}", 30)
            r["insights"] = {m["name"]: (m.get("values") or [{}])[0].get("value", 0)
                             for m in d.get("data", [])}
        except Exception as e:  # a single dead id must not kill a 44-reply pull
            r["insights"] = {"error": str(e)[:120]}


def local_dt(r):
    return datetime.datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%S%z").astimezone(LOCAL)


def parent_of(r):
    """The parent post, if the API ever starts returning it. Empty dict when it doesn't."""
    return r.get("replied_to") or r.get("root_post") or {}


def work_list(rows, label):
    """
    The markdown work-list. One block per reply with an UNRESOLVED parent slot, because a
    reply archived without its parent is a non sequitur nobody can use six weeks from now.
    Fill `parent_author` / `parent_text` from a browser pass, then flip status to captured.
    """
    out = [f"# Replies pulled: {label}", "",
           f"{len(rows)} replies, oldest first. Times are America/Boise.", "",
           "Every block below has an UNRESOLVED parent. The API cannot supply it (see",
           "pull_replies.py's docstring). Open each permalink in the logged-in browser,",
           "read the post above the reply, and fill in `parent_author` and `parent_text`.",
           "A block still marked unresolved is half a conversation and is not archive-ready.",
           ""]
    for i, r in enumerate(rows, 1):
        p, ins = parent_of(r), r.get("insights", {})
        text = " ".join((r.get("text") or "").split())
        out += [f"## {i}. {local_dt(r).strftime('%Y-%m-%d %-I:%M %p')}", "",
                f"- permalink: {r['permalink']}",
                f"- media_id: {r['id']}",
                f"- views: {ins.get('views', '?')} | likes: {ins.get('likes', '?')} | "
                f"replies: {ins.get('replies', '?')}",
                f"- parent_author: {('@' + p['username']) if p.get('username') else 'UNRESOLVED'}",
                f"- parent_text: {p.get('text', 'UNRESOLVED')}",
                f"- status: {'captured' if p.get('username') else 'needs-parent'}",
                "", "> " + (text or "[no text]"), ""]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--date", help="a single LOCAL day, YYYY-MM-DD")
    ap.add_argument("--days", type=int, default=7, help="how many days back (default 7)")
    ap.add_argument("--no-insights", action="store_true", help="skip per-reply engagement")
    ap.add_argument("--outdir", default="meta/replies/inbound")
    args = ap.parse_args()

    try:
        token, uid = os.environ["THREADS_ACCESS_TOKEN"], os.environ["THREADS_USER_ID"]
    except KeyError as e:
        sys.exit(f"missing {e} - run via scripts/pull-replies.sh from the repo root, "
                 f"which sources .env")

    rows = fetch_replies(uid, token)
    if args.date:
        rows = [r for r in rows if local_dt(r).date().isoformat() == args.date]
        label = args.date
    else:
        cutoff = datetime.datetime.now(LOCAL) - datetime.timedelta(days=args.days)
        rows = [r for r in rows if local_dt(r) >= cutoff]
        label = f"last-{args.days}d-to-{datetime.datetime.now(LOCAL).date().isoformat()}"
    rows.sort(key=lambda r: r["timestamp"])
    if not rows:
        sys.exit(f"no replies found for {label}")

    if not args.no_insights:
        add_insights(rows, token)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{label}.json").write_text(json.dumps(rows, indent=1))
    (outdir / f"{label}.md").write_text(work_list(rows, label))

    views = [r.get("insights", {}).get("views", 0) for r in rows]
    resolved = sum(1 for r in rows if parent_of(r).get("username"))
    print(f"{len(rows)} replies -> {outdir}/{label}.json + .md")
    if views and any(views):
        print(f"views: total {sum(views):,}  median {sorted(views)[len(views)//2]}  "
              f"max {max(views):,}")
    print(f"parents_from_api: {resolved}/{len(rows)}")
    if resolved < len(rows):
        print(f"\n{len(rows) - resolved} parents UNRESOLVED. The pull is not done until "
              f"they're captured:\n  open {outdir}/{label}.md, work the permalinks in the "
              f"logged-in browser, fill parent_author/parent_text.")


if __name__ == "__main__":
    main()
