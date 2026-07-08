#!/usr/bin/env python3
"""Finish birefnet cutouts -> shipped fx-*.webp.
Clouds: trim + slight alpha feather + resize + webp q80.
Products: trim + subtle warm pink glow halo + resize + webp q80."""
from PIL import Image, ImageFilter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BF = HERE / "bf"
DST = Path("/Users/eeaglstun/Documents/web/ericeaglstun-ai/content/blog/everyone-deserves-a-mascara-treat")

def bbox_trim(im, thresh=8):
    a = im.split()[3]
    bb = a.point(lambda v: 255 if v > thresh else 0).getbbox()
    return im.crop(bb) if bb else im

def save_webp(im, path, w):
    r = w / im.width
    im = im.resize((w, round(im.height * r)), Image.LANCZOS)
    im.save(path, "WEBP", quality=80, method=6)
    kb = path.stat().st_size / 1024
    print(f"  {path.name}: {im.width}x{im.height}  {kb:.0f}KB")

def do_cloud(src, out, w):
    im = Image.open(BF / src).convert("RGBA")
    im = bbox_trim(im)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(0.6))  # soften any residual crispness
    im.putalpha(a)
    save_webp(im, DST / out, w)

def do_product(src, out, w, glow=(255, 156, 132)):
    im = Image.open(BF / src).convert("RGBA")
    im = bbox_trim(im)
    pad = 64
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    canvas.paste(im, (pad, pad))
    im = canvas
    ga = im.split()[3].filter(ImageFilter.GaussianBlur(20))
    ga = ga.point(lambda v: int(v * 0.45))  # subtle
    glow_layer = Image.new("RGBA", im.size, glow + (0,))
    glow_layer.putalpha(ga)
    out_im = Image.alpha_composite(glow_layer, im)
    out_im = bbox_trim(out_im, thresh=4)  # trim excess transparent pad
    save_webp(out_im, DST / out, w)

print("clouds:")
do_cloud("c1.png", "fx-cloud-1.webp", 700)
do_cloud("c2.png", "fx-cloud-2.webp", 500)
do_cloud("c3.png", "fx-cloud-3.webp", 380)
print("products:")
do_product("vmasc.png", "fx-void-mascara.webp", 340)
do_product("vperf.png", "fx-void-perfume.webp", 320)
do_product("vlip.png", "fx-void-lipstick.webp", 300)
