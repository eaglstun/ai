#!/usr/bin/env python3
"""Generate 6 isolated-object source images via Together FLUX.1.1-pro.
Clouds on pure white (ImageMagick keyable); products on dark grey (birefnet)."""
import json, os, sys, time, urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent
KEY = os.environ["TOGETHER_API_KEY"]

def http(url, data=None, headers=None, timeout=240):
    h = {"User-Agent": "Mozilla/5.0"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def gen(prompt, name, w=1024, h=1024):
    body = json.dumps({"model": "black-forest-labs/FLUX.1.1-pro", "prompt": prompt,
                       "width": w, "height": h, "steps": 28, "n": 1}).encode()
    r = json.loads(http("https://api.together.xyz/v1/images/generations", body,
                        {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}))
    out = OUT / name
    out.write_bytes(http(r["data"][0]["url"]))
    print(f"ok {name} ({out.stat().st_size//1024}KB)")

KODA = ("1950s mid-century American illustration, warm Kodachrome palette, soft focus, "
        "aged film grain, dreamy retro glow. ")
SUF = " No text, no words, no letters, no watermark."

JOBS = [
    # clouds on pure white
    ("cloud-1-airy.jpg", KODA + "Subject: an airy floating cluster of soft translucent "
     "coral-pink soap bubbles and one fluffy pale-pink cloud puff, delicate and weightless, "
     "glowing softly, isolated and centered on a plain pure solid white background, "
     "soft feathered fading edges, no hard edges, dreamy product-shot lighting." + SUF),
    ("cloud-2-lantern.jpg", KODA + "Subject: a dense cluster of soft coral-pink round paper "
     "lanterns and translucent pink bubbles floating together, warm inner glow, fluffy, "
     "isolated and centered on a plain pure solid white background, soft feathered fading "
     "edges, no hard edges, dreamy product-shot lighting." + SUF),
    ("cloud-3-wisp.jpg", KODA + "Subject: a small wispy delicate cluster of a few pale "
     "coral-pink bubbles and one little paper lantern, airy and light, isolated and centered "
     "on a plain pure solid white background, soft feathered fading edges, no hard edges." + SUF),
    # products on dark grey (rim-lit to pop on black)
    ("void-mascara.jpg", KODA + "Subject: a single luxury mascara tube with its brush wand "
     "beside it, tumbling and floating weightless at a gentle diagonal angle in space, soft "
     "pink rim light along the edges and a faint warm glow, luminous, isolated and centered "
     "on a plain flat medium-dark neutral grey background, cinematic product-shot lighting." + SUF),
    ("void-perfume.jpg", KODA + "Subject: a single elegant faceted glass perfume bottle "
     "tumbling and floating weightless at a gentle diagonal angle in space, soft pink rim "
     "light along the glass edges and a faint warm glow, luminous and jewel-like, isolated "
     "and centered on a plain flat medium-dark neutral grey background, cinematic product-shot "
     "lighting." + SUF),
    ("void-lipstick.jpg", KODA + "Subject: a single open lipstick tube with the coral-pink "
     "bullet extended, tumbling and floating weightless at a gentle diagonal angle in space, "
     "soft pink rim light along the metal edges and a faint warm glow, luminous, isolated and "
     "centered on a plain flat medium-dark neutral grey background, cinematic product-shot "
     "lighting." + SUF),
]

for name, prompt in JOBS:
    for attempt in (1, 2):
        try:
            gen(prompt, name); break
        except Exception as e:
            print(f"attempt {attempt} FAILED {name}: {e}", file=sys.stderr)
            if attempt == 2: print(f"GIVEUP {name}", file=sys.stderr)
            time.sleep(3)
