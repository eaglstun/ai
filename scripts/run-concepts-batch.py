#!/usr/bin/env python3
"""Batch driver: run gen-concepts.py over concepts/manifest.json.

Resume-able: a post whose concepts/ dir already holds 4+ concept jpgs is
skipped. After each post, builds contact-sheet.jpg (2x2, no fonts needed).
Serial on purpose: Draw Things is a local GPU queue of one.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "concepts" / "manifest.json"


def sheet(outdir):
    imgs = sorted(str(p) for p in outdir.glob("[a-d]-*.jpg"))
    if len(imgs) < 2:
        return
    half = (len(imgs) + 1) // 2
    rows = []
    for i, group in enumerate([imgs[:half], imgs[half:]]):
        row = outdir / f"row{i}.png"
        cmd = ["magick"]
        for p in group:
            cmd += ["(", p, "-resize", "640x", "-bordercolor", "#f4efe4",
                    "-border", "8", ")"]
        cmd += ["+append", str(row)]
        subprocess.run(cmd, check=True)
        rows.append(str(row))
    subprocess.run(["magick", *rows, "-append", "-background", "#f4efe4",
                    str(outdir / "contact-sheet.jpg")], check=True)
    for r in rows:
        Path(r).unlink()


def main():
    entries = json.loads(MANIFEST.read_text())
    total = len(entries)
    for i, e in enumerate(entries, 1):
        outdir = ROOT / "concepts" / e["slug"]
        have = len(list(outdir.glob("[a-d]-*.jpg"))) if outdir.exists() else 0
        if have >= 4:
            print(f"[{i}/{total}] {e['slug']}: already has {have}, skip",
                  flush=True)
            continue
        print(f"[{i}/{total}] {e['slug']} ...", flush=True)
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "gen-concepts.py"),
             "--slug", e["slug"], "--brief", e["brief"],
             "--pairs", e["pairs"]],
            capture_output=True, text=True)
        print(r.stdout.strip(), flush=True)
        if r.returncode != 0:
            print(f"  DRIVER: gen-concepts failed: {r.stderr.strip()[:300]}",
                  flush=True)
            continue
        try:
            sheet(outdir)
            print(f"  sheet ok", flush=True)
        except Exception as ex:
            print(f"  sheet failed: {ex}", flush=True)
    print("BATCH DONE", flush=True)


if __name__ == "__main__":
    main()
