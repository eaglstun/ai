#!/usr/bin/env python3
"""Generate concept images on the LOCAL ComfyUI Z-Image Turbo graph.

Mirrors the blueprint "Text to Image (Z-Image-Turbo).json": Qwen3-4B text
encoder (CLIPLoader type `lumina2`), z_image_turbo_bf16 UNET, ae VAE,
ModelSamplingAuraFlow shift 3, KSampler 8 steps / cfg 1.0 / res_multistep /
simple. Free, local, ~40s an image on this Mac.

  python3 scripts/zimage-comfy.py --slug <post-slug> --jobs jobs.json

Stdlib only, same discipline as gen-concepts.py. See concepts/README.md.
"""
import argparse, json, random, time, urllib.parse, urllib.request
from pathlib import Path

HOST = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
W, H, STEPS, CFG = 1216, 832, 8, 1.0

STYLES = {
    "gag-panel": "Single-panel magazine cartoon, black ink and soft gray wash, generous "
                 "white space, one clear witty visual idea, minimal background detail",
    "continuous-line": "Sophisticated editorial illustration drawn as one continuous "
                       "unbroken black line on cream paper, abstract, witty, mid-century",
    "kodachrome": "1950s mid-century American illustration, warm Kodachrome palette, "
                  "aged paper grain, cheerful retro-futurist",
    "woodcut": "Antique woodcut engraving, dense cross-hatching, Victorian scientific "
               "catalog energy, black ink on aged cream paper",
    "ink-wash-dark": "Moody ink wash illustration, deadpan gothic humor, soft gray "
                     "washes with deep blacks, quiet menace played straight",
    "editorial-photo": "Sharp modern editorial photograph, 85mm lens, dramatic "
                       "single-source raking light in a dark room, deep shadows, "
                       "shallow depth of field",
    "kodachrome-photo": "Faded 1950s Kodachrome color photograph, 35mm film grain, "
                        "warm saturated dye-transfer palette, slight vignetting, "
                        "natural available light, candid documentary realism",
    "flash-documentary": "Direct on-camera flash documentary photograph, harsh light "
                         "falloff into black, 1970s color negative stock, unposed and "
                         "slightly awkward, snapshot framing",
    "polaroid": "Vintage instant Polaroid SX-70 snapshot, soft low-contrast "
                "pastel color, milky washed-out blacks, heavy orange and magenta "
                "light leaks streaking across the frame, blown highlights, dust "
                "and emulsion flaws, slight softness, casual snapshot framing",
    "large-format": "Large-format 4x5 color portrait photograph, soft north-facing "
                    "window light, muted desaturated palette, extremely fine detail, "
                    "formal stillness, shallow depth of field",
}
SUFFIX = " No text, no words, no letters, no watermark."


def graph(prompt, seed, w=W, h=H):
    return {
        "28": {"class_type": "UNETLoader",
               "inputs": {"unet_name": "z_image_turbo_bf16.safetensors",
                          "weight_dtype": "default"}},
        "30": {"class_type": "CLIPLoader",
               "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2",
                          "device": "default"}},
        "29": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "27": {"class_type": "CLIPTextEncode",
               "inputs": {"text": prompt, "clip": ["30", 0]}},
        "33": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["27", 0]}},
        "11": {"class_type": "ModelSamplingAuraFlow",
               "inputs": {"shift": 3, "model": ["28", 0]}},
        "13": {"class_type": "EmptySD3LatentImage",
               "inputs": {"width": w, "height": h, "batch_size": 1}},
        "3":  {"class_type": "KSampler",
               "inputs": {"seed": seed, "steps": STEPS, "cfg": CFG,
                          "sampler_name": "res_multistep", "scheduler": "simple",
                          "denoise": 1, "model": ["11", 0], "positive": ["27", 0],
                          "negative": ["33", 0], "latent_image": ["13", 0]}},
        "8":  {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["29", 0]}},
        "9":  {"class_type": "SaveImage",
               "inputs": {"filename_prefix": "seance-concept", "images": ["8", 0]}},
    }


def post(path, payload):
    req = urllib.request.Request(HOST + path, json.dumps(payload).encode(),
                                 {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def run(prompt, seed, out, w=W, h=H):
    pid = post("/prompt", {"prompt": graph(prompt, seed, w, h)})["prompt_id"]
    t0 = time.time()
    while True:
        if time.time() - t0 > 600:
            raise TimeoutError("gave up after 600s")
        h = json.loads(urllib.request.urlopen(f"{HOST}/history/{pid}", timeout=30).read())
        if pid in h:
            imgs = h[pid]["outputs"]["9"]["images"][0]
            q = urllib.parse.urlencode({"filename": imgs["filename"],
                                        "subfolder": imgs.get("subfolder", ""),
                                        "type": imgs["type"]})
            data = urllib.request.urlopen(f"{HOST}/view?{q}", timeout=120).read()
            out.write_bytes(data)
            return time.time() - t0
        time.sleep(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--jobs", required=True, help="JSON list of {letter,style,subject,seed}")
    a = ap.parse_args()
    outdir = ROOT / "concepts" / a.slug
    outdir.mkdir(parents=True, exist_ok=True)
    jobs = json.loads(Path(a.jobs).read_text())
    log = []
    for j in jobs:
        style = j["style"]
        seed = j.get("seed") or random.randrange(1, 2**31)
        prompt = f"{STYLES[style]}. {j['subject']}{SUFFIX}"
        name = f"{j['letter']}-zimage-{style}.png"
        print(f"-> {name}  seed={seed}", flush=True)
        try:
            secs = run(prompt, seed, outdir / name,
                       j.get("w", W), j.get("h", H))
            print(f"   ok {secs:.0f}s", flush=True)
            log.append((name, style, seed, prompt, f"{secs:.0f}s"))
        except Exception as e:
            print(f"   FAIL {e}", flush=True)
            log.append((name, style, seed, prompt, f"FAILED: {e}"))
    print(json.dumps(log, indent=1))


if __name__ == "__main__":
    main()
