#!/usr/bin/env python3
"""Pull the chosen draft block out of an inbox/meta markdown file.

Usage: PICK=<letter or empty> extract_pick.py <draft.md>
  - empty PICK  -> the "## ✅ Pick:" block
  - PICK=B      -> the "## B — ..." (or "## ✅ Pick: B —") block

Prints the post-ready text to stdout. Soft line-wraps are unwrapped to spaces;
blank lines are kept as paragraph breaks. Warns on stderr (does not strip) if
markdown emphasis survives, since Threads renders none.
"""
import os
import re
import sys

if len(sys.argv) != 2:
    sys.exit("usage: PICK=<letter> extract_pick.py <draft.md>")

path = sys.argv[1]
pick = os.environ.get("PICK", "").strip().upper()
lines = open(path, encoding="utf-8").read().splitlines()

# locate the start heading
start = None
for i, ln in enumerate(lines):
    if not ln.startswith("##"):
        continue
    if pick:
        # "## ✅ Pick: A — ..." or "## A — ..." — match the leading letter token
        m = re.match(r"^##\s+(?:✅\s*Pick:\s*)?([A-Za-z])\b", ln)
        if m and m.group(1).upper() == pick:
            start = i + 1
            break
    elif "Pick:" in ln:
        start = i + 1
        break

if start is None:
    sys.exit(f"could not find {'pick ' + pick if pick else 'a ## ✅ Pick: block'} in {path}")

body = []
for ln in lines[start:]:
    s = ln.strip()
    if re.fullmatch(r"\(\d+\)", s):        # the (NNN) char-count line ends the block
        break
    if s == "---" or ln.startswith("##"):  # safety: next section
        break
    body.append(re.sub(r"^\s*>\s?", "", ln))  # strip markdown quote marker

raw = "\n".join(body).strip()
if not raw:
    sys.exit("matched the heading but the block was empty")

# Unwrap soft wraps: single newline inside a paragraph = reflow artifact -> space;
# blank line = intentional break -> keep.
paras = [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", raw)]
text = "\n\n".join(paras)

# Threads renders no markdown — warn (don't mangle) if emphasis markers survive.
emphasis = r"\*\*|__|(?<!\w)_[^_]+_(?!\w)|(?<!\w)\*[^*]+\*(?!\w)"
if re.search(emphasis, text):
    sys.stderr.write(
        "⚠ markdown emphasis (_x_ / **x**) will post as literal characters "
        "— strip it if you don't want the symbols showing.\n"
    )

print(text)
