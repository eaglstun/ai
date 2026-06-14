#!/usr/bin/env python3
"""Regenerate meta/publish-schedule.md: a chronological master list of every
blog / practice / deep-dives post, not grouped by type.

This file is OUTPUT. Do not hand-edit meta/publish-schedule.md; edit the post
frontmatter (date / draft) and re-run this script. Keeps the list in sync as
posts are made.

    python3 scripts/gen-publish-schedule.py

Status column reflects the `draft` frontmatter flag: PUBLISH = draft false
(goes live on next deploy), draft = stays hidden.
"""
import glob
import os
import re

SECTIONS = {"blog": "blog", "practice": "practice", "deep-dives": "deep-dive"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "meta", "publish-schedule.md")


def field(fm, key):
    m = re.search(r"^%s\s*=\s*(.+)$" % key, fm, re.M)
    return m.group(1).strip().strip('"') if m else ""


def collect():
    rows = []
    for f in glob.glob(os.path.join(ROOT, "content", "**", "*.md"), recursive=True):
        rel = os.path.relpath(f, os.path.join(ROOT, "content"))
        parts = rel.split(os.sep)
        if len(parts) < 2:            # top-level pages (why.md, colophon.md)
            continue
        section = parts[0]
        if section not in SECTIONS:   # skip glossary etc.
            continue
        if os.path.basename(f) == "_index.md":
            continue
        m = re.search(r"^\+\+\+(.*?)\+\+\+", open(f, encoding="utf-8").read(), re.S)
        if not m:
            continue
        fm = m.group(1)
        rows.append((field(fm, "date")[:10], SECTIONS[section],
                     "draft" if field(fm, "draft") == "true" else "PUBLISH",
                     field(fm, "title")))
    rows.sort(key=lambda r: (r[0], r[1], r[3]))
    return rows


def render(rows):
    header = ["#", "Date", "Type", "Status", "Title"]
    table = [[str(i + 1), d, t, s, ti] for i, (d, t, s, ti) in enumerate(rows)]
    widths = [max(len(r[c]) for r in [header] + table) for c in range(5)]
    line = lambda cells: "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"

    pub = sum(1 for r in rows if r[2] == "PUBLISH")
    by = {}
    for d, t, s, ti in rows:
        by.setdefault(t, [0, 0])
        by[t][0] += 1
        by[t][1] += s == "PUBLISH"
    bytype = ", ".join(f"{k} {v[0]} ({v[1]} publish)" for k, v in sorted(by.items()))

    return "\n".join([
        "# Publish schedule (master list)",
        "",
        "Every blog, practice, and deep-dives post in one chronological timeline, not grouped by",
        "type. Status is the `draft` frontmatter flag: **PUBLISH** = `draft = false`, goes live on",
        "next deploy; **draft** = stays hidden.",
        "",
        "GENERATED FILE. Do not hand-edit. Edit post frontmatter (date / draft), then re-run",
        "`python3 scripts/gen-publish-schedule.py`. Reflects the `draft` flag in the content files,",
        "which is what will publish on the next build, not necessarily what is on the live server.",
        "",
        line(header),
        sep,
        *[line(r) for r in table],
        "",
        f"**{len(rows)} posts: {pub} set to publish, {len(rows) - pub} still draft.**",
        "",
        f"By type: {bytype}.",
        "",
    ])


if __name__ == "__main__":
    rows = collect()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(render(rows))
    print(f"wrote {OUT}: {len(rows)} posts")
