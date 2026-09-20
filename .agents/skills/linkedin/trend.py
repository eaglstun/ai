#!/usr/bin/env python3
"""LinkedIn post metrics: turn logged JSON snapshots into a trend table.

No dependencies (stdlib only). LinkedIn exposes no personal-post analytics API,
so this reads what you hand-captured into posts/<slug>.json and does the arithmetic
you'd otherwise do on a Saturday.

    python3 trend.py posts/<slug>.json   # one post: cumulative table + deltas
    python3 trend.py                      # rollup across every posts/*.json
"""

import glob
import json
import os
import sys

# Cumulative metrics we track, in display order: (json key, column header).
METRICS = [
    ("impressions", "impr"),
    ("reach", "reach"),
    ("profileViews", "p.views"),
    ("followers", "fllw"),
    ("engagements", "engmt"),
    ("reactions", "react"),
    ("comments", "cmts"),
    ("reposts", "repst"),
    ("saves", "saves"),
    ("sends", "sends"),
]

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    with open(path) as f:
        return json.load(f)


def fmt_cell(value, prev):
    """A cell as 'total (+delta)'. Blank for missing; no delta on the first row
    or when either side is unknown."""
    if value is None:
        return ""
    if prev is None:
        return str(value)
    delta = value - prev
    sign = "+" if delta >= 0 else ""
    return "{} ({}{})".format(value, sign, delta)


def render_table(rows):
    """rows: list of dicts of already-formatted strings keyed by column header.
    Prints a left-aligned, padded table."""
    headers = ["when"] + [h for _, h in METRICS]
    widths = {h: len(h) for h in headers}
    for row in rows:
        for h in headers:
            widths[h] = max(widths[h], len(row.get(h, "")))

    def line(cells):
        return "  ".join(cells.get(h, "").ljust(widths[h]) for h in headers)

    print(line({h: h for h in headers}))
    print("  ".join("-" * widths[h] for h in headers))
    for row in rows:
        print(line(row))


def post_rows(post):
    """Build formatted table rows (with deltas) for one post's snapshots."""
    rows = []
    prev = {}
    for snap in post.get("snapshots", []):
        when = snap.get("ts", "?")
        if snap.get("label"):
            when += " " + snap["label"]
        row = {"when": when}
        for key, header in METRICS:
            row[header] = fmt_cell(snap.get(key), prev.get(key))
        rows.append(row)
        # carry last-known value forward so a partial pull doesn't blank the delta
        for key, _ in METRICS:
            if snap.get(key) is not None:
                prev[key] = snap[key]
    return rows


def show_post(path):
    post = load(path)
    title = post.get("title", post.get("slug", os.path.basename(path)))
    print("\n{}".format(title))
    if post.get("posted"):
        print("posted {}   {}".format(post["posted"], post.get("liveUrl", "")))
    print()

    snaps = post.get("snapshots", [])
    if not snaps:
        print("(no snapshots logged yet)")
        return

    render_table(post_rows(post))

    latest = snaps[-1]
    demo = latest.get("demographics") or {}
    if demo:
        print("\nlatest demographics ({}):".format(latest.get("ts", "?")))
        for k, v in demo.items():
            print("  {:<14} {}".format(k, v))


def rollup():
    paths = sorted(glob.glob(os.path.join(HERE, "posts", "*.json")))
    if not paths:
        print("No posts/*.json found. Log a snapshot first (see SKILL.md).")
        return
    print("\nLinkedIn rollup ({} post{}) - latest totals:\n".format(
        len(paths), "" if len(paths) == 1 else "s"))
    rows = []
    for path in paths:
        post = load(path)
        snaps = post.get("snapshots", [])
        latest = snaps[-1] if snaps else {}
        row = {"when": post.get("slug", os.path.basename(path))[:24]}
        for key, header in METRICS:
            v = latest.get(key)
            row[header] = "" if v is None else str(v)
        rows.append(row)
    render_table(rows)


def main(argv):
    if len(argv) > 1:
        show_post(argv[1])
    else:
        rollup()


if __name__ == "__main__":
    main(sys.argv)
