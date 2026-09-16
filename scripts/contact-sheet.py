#!/usr/bin/env python3
"""Build concepts/<slug>/contact-sheet.html from whatever images are in the dir.

Standalone twin of the sheet gen-concepts.py writes inline, for batches driven by
zimage-comfy.py (any count, any engine). Stdlib only.

  python3 scripts/contact-sheet.py --slug five-agents-one-marble
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = {".png", ".jpg", ".jpeg", ".webp"}

CSS = ("body{font:16px/1.5 Georgia,serif;margin:2rem;background:#f4efe4;color:#1a1a1a}"
       "h1{font-size:1.5rem}main{display:grid;grid-template-columns:repeat(auto-fill,"
       "minmax(420px,1fr));gap:1.5rem;max-width:1400px}img{width:100%;display:block;"
       "border:1px solid #999;background:#fff}figure{margin:0}"
       "figcaption{font-style:italic;margin-top:.4rem;font-size:.9rem}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    d = ROOT / "concepts" / a.slug
    imgs = sorted(p for p in d.iterdir()
                  if p.suffix.lower() in EXT and not p.name.startswith("contact"))
    cells = "\n".join(
        f'<figure><img src="{p.name}" loading="lazy">'
        f"<figcaption>{p.name}  &middot; {p.stat().st_size // 1024} KB</figcaption></figure>"
        for p in imgs)
    (d / "contact-sheet.html").write_text(
        f"<!doctype html><meta charset=utf-8><title>{a.slug}</title><style>{CSS}</style>"
        f"<h1>{a.slug} &middot; {len(imgs)} concepts</h1><main>{cells}</main>")
    print(f"wrote {d}/contact-sheet.html ({len(imgs)} images)")


if __name__ == "__main__":
    main()
