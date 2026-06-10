#!/usr/bin/env python3
"""Generate Hugo glossary content from the ai-dev skill's source entries.

Re-runnable: dump new/updated terms into the skill, tweak the maps below, re-run.
For each source file it:
  - drops the leading `# Heading` (Hugo renders the title from frontmatter)
  - lifts the trailing `**See also:**` paragraph into a `related` frontmatter list
    (the theme renders those as chips), removing it from the body
  - rewrites every `[[slug]]` wikilink into a real `[text](/glossary/slug/)` link
  - writes frontmatter (title, summary, category, related, weight-by-alpha)
"""
import re
import sys
from pathlib import Path

SRC = Path("/Users/eeaglstun/.claude/skills/ai-dev/references/glossary")
OUT = Path(__file__).resolve().parent.parent / "content" / "glossary"

# Page titles (frontmatter / cards / chips).
TITLE = {
    "ablation": "Ablation",
    "agi": "AGI",
    "attention": "Attention",
    "cuda": "CUDA",
    "cudnn-cublas": "cuDNN / cuBLAS",
    "dimensions": "Dimensions",
    "embeddings": "Embeddings",
    "gan": "GAN",
    "gelu": "GELU",
    "ggml": "GGML",
    "gguf": "GGUF",
    "gpt": "GPT",
    "gradient-descent": "Gradient descent",
    "latent-space": "Latent space",
    "llamacpp-vs-ollama": "llama.cpp vs Ollama",
    "lora": "LoRA",
    "machine-learning": "Machine learning",
    "metal": "Metal",
    "mlx": "MLX",
    "mps": "MPS",
    "norm-placement": "Norm placement",
    "parameters": "Parameters",
    "precision": "Floating-point precision",
    "relu": "ReLU",
    "residual-connections": "Residual connections",
    "rss-sampler": "RSS sampler",
    "tensor": "Tensor",
    "transformer": "Transformer",
    "val-loss": "Validation loss",
    "vulkan": "Vulkan",
}

# Link text used when a [[slug]] appears inline in prose (reads more naturally
# lowercased for common nouns).
INLINE = dict(TITLE)
INLINE.update({
    "ablation": "ablation",
    "attention": "attention",
    "machine-learning": "machine learning",
    "norm-placement": "norm placement",
    "dimensions": "dimensions",
    "embeddings": "embeddings",
    "gradient-descent": "gradient descent",
    "latent-space": "latent space",
    "parameters": "parameters",
    "precision": "floating-point precision",
    "tensor": "tensor",
    "transformer": "transformer",
    "val-loss": "validation loss",
    "residual-connections": "residual connections",
})

# One-line summaries (frontmatter `summary` -> dek + card text + SEO).
SUMMARY = {
    "ablation": "Removing a model component on purpose to measure how much it mattered - the standard “ablation study.”",
    "agi": "Hypothetical AI that matches humans across essentially all intellectual tasks - a contested, moving goalpost.",
    "attention": "How tokens weigh each other (query · key · value) - the heart of the transformer.",
    "machine-learning": "Systems that learn patterns from data instead of hand-written rules.",
    "dimensions": "Independent axes of variation; ML vectors live in hundreds or thousands of them.",
    "embeddings": "Dense vectors where distance & direction encode meaning - the backbone of semantic search and RAG.",
    "cuda": "NVIDIA's GPU-compute platform; the default ML backend.",
    "cudnn-cublas": "NVIDIA's CUDA math & deep-learning libraries.",
    "gan": "Generator-vs-discriminator generative architecture.",
    "gelu": "The smooth activation gate used inside GPT- and BERT-style transformers.",
    "ggml": "C/C++ tensor library powering llama.cpp; runs GGUF.",
    "gguf": "llama.cpp's single-file format for quantized local LLMs.",
    "gpt": "Generative pre-trained (decoder-only) transformer LLM.",
    "gradient-descent": "The downhill-walking algorithm that trains models - nudge every parameter to shrink the error, then repeat.",
    "latent-space": "The hidden vector space where geometry encodes meaning.",
    "llamacpp-vs-ollama": "The local-inference engine vs the wrapper built on it.",
    "lora": "Low-rank adapters; parameter-efficient fine-tuning.",
    "metal": "Apple's GPU-compute API; powers MLX and Metal-backed ML.",
    "mlx": "Apple-silicon ML framework; the Mac answer to GGUF.",
    "mps": "Metal Performance Shaders; Apple's cuDNN-equivalent ops.",
    "norm-placement": "Where LayerNorm sits in a transformer block - pre, post, or sandwiched - and why it decides whether a deep model trains at all.",
    "parameters": "Learned weights; the count is model size & memory cost.",
    "precision": "How many bits each number uses - fp32 vs fp16 vs bf16. Halving precision halves the footprint, and is not the same thing as quantizing.",
    "relu": "The simplest activation gate: zero out negatives, pass positives through.",
    "residual-connections": "Skip-ahead wiring that lets networks go very deep without the signal falling apart.",
    "rss-sampler": "A lightweight monitor that polls a process's Resident Set Size on a timer to chart its real-RAM footprint over time - so you see the memory cliff coming instead of OOM-ing into it.",
    "tensor": "N-dimensional numeric array; the core ML data structure.",
    "transformer": "The self-attention architecture behind modern LLMs.",
    "val-loss": "Held-out validation error; the overfitting tripwire.",
    "vulkan": "Cross-vendor GPU-compute API; the portable ML fallback.",
}

# "In plain English" callout - the analogy-first take that leads each term page,
# for readers who want the gist before the precise definition. One vivid analogy each.
PLAIN = {
    "ablation": "The Jenga test. Pull one block out of the standing tower and watch whether the whole thing topples or just wobbles - that's how you find out which part was actually holding the model up.",
    "agi": "The 'does everything' robot from the movies - one AI that matches a person at basically any mental task, not just the one it was trained for. It doesn't exist yet, and people can't even agree on where the finish line is.",
    "attention": "Context clues. Instead of reading a sentence one word at a time, the model looks at the whole thing at once and works out which words are talking about each other - so in 'the bank was muddy from the river,' it knows 'bank' means riverbank, not the place with your money.",
    "cuda": "The translator that lets AI software talk to NVIDIA graphics cards. NVIDIA's chips are the industry-standard engines for AI, and CUDA is the language nearly everyone uses to drive them.",
    "cudnn-cublas": "NVIDIA's box of pre-tuned math shortcuts. The heavy number-crunching inside AI runs on these ready-made, hand-optimized routines, so nobody has to reinvent the fast way to multiply giant grids of numbers.",
    "dimensions": "The number of separate sliders it takes to describe something. 'Tall/short' is one slider; add 'old/young' and 'loud/quiet' and you're at three. AI describes a word or image with hundreds or thousands of these sliders at once.",
    "embeddings": "Turning words into coordinates. Every word, sentence, or image gets pinned to a spot on a giant map where similar things land near each other - so 'king' sits close to 'queen,' and the computer can measure meaning with a ruler.",
    "gan": "Forger vs. detective. One AI fakes convincing images, another tries to spot the fakes, and they train against each other until the forger gets so good the detective can't tell - and that's when you get realistic generated pictures.",
    "gelu": "The bouncer with manners. It's the little gate between layers that decides how much of each signal to let through - instead of a hard yes/no it eases borderline cases in gently, which is why modern models prefer it.",
    "ggml": "The engine block. The low-level code that actually loads a model's numbers into memory and grinds through the math, so a GGUF file has something to run inside on your own machine.",
    "gguf": "Zipping a model down to fit. AI models are huge; this is like saving a giant photo as a JPEG - one tidy compressed file, shrunk enough to run smoothly on a normal laptop instead of a data-center server.",
    "gpt": "The autocomplete that ate the world. At heart it just guesses the next word over and over - but at enormous scale that simple trick turns into something that can write essays, code, and hold a conversation.",
    "gradient-descent": "Finding the bottom of a valley in thick fog. You can't see where the lowest point is, but you can feel which way the ground slopes under your feet - so you step downhill, feel again, and repeat until it flattens out. Training a model is that same move done millions of times, with 'how wrong it is' as the hill.",
    "latent-space": "The secret organizing closet. Picture a walk-in closet sorted not by color but by vibe - leather jackets near combat boots, tuxedos near silk ties. It's the AI's internal closet where similar ideas get stored near each other so it can find them later.",
    "llamacpp-vs-ollama": "Engine vs. dashboard. llama.cpp is the bare engine that runs the model; Ollama is the friendly dashboard bolted on top so you can start a model with one command instead of wiring up the engine yourself.",
    "lora": "Sticky notes instead of rewriting the book. Rather than retrain a giant model from scratch to teach it something new, you clip on a small set of adjustments - cheap to make, easy to swap in and out, and you can keep a whole drawer of them.",
    "machine-learning": "Teaching by examples instead of rules. Instead of writing out every rule for 'what a cat looks like,' you show the computer thousands of cat photos and let it work out the pattern itself.",
    "metal": "Apple's version of the AI-to-GPU translator. It's the language software uses to drive the graphics chip inside a Mac - Apple's homegrown answer to NVIDIA's CUDA.",
    "mlx": "Apple's home-field AI framework. A toolkit Apple built specifically to run and train models fast on Mac chips, taking advantage of the way Apple shares memory between the processor and the GPU.",
    "mps": "Apple's drawer of ready-made math moves. The pre-built, hand-tuned operations that do the actual number-crunching on a Mac's GPU - Apple's counterpart to NVIDIA's cuDNN.",
    "norm-placement": "Where you put the leveler in a chain of guitar pedals. It's the box that keeps the signal from clipping or fading as it runs through a long effects chain - and whether you put it before each pedal, after, or both changes how clean the whole chain stays. Modern models put it before (pre-norm); the original put it after (post-norm); the cautious ones do both (sandwich).",
    "parameters": "The knobs and dials. Picture a mixing board with billions of tiny dials; training is the computer nudging each one a hair every time it's right or wrong. More dials means more room for fine detail - and a bigger, heavier model.",
    "precision": "How many decimal places you bother writing down. fp32 records pi as 3.1415927; fp16 shrugs and writes 3.14 - same number, fewer digits, half the paper. Quantization is the different move: instead of writing the number at all, you round everyone to the nearest slot on a tiny price menu and just remember the slot. One turns down the resolution; the other changes the medium.",
    "relu": "The simplest bouncer there is. One rule: negative numbers get turned away at the door, positive numbers walk right in unchanged. Crude, but cheap and effective - and for years it was the default gate inside neural networks.",
    "residual-connections": "The express lane. Instead of forcing every layer to redraw the whole picture, you let the original pass straight through and each layer just clips on a note of what to change - which is how networks stack hundreds of layers deep without the signal getting mangled.",
    "rss-sampler": "The bathtub gauge. A single 'it overflowed' tells you nothing useful; a number ticking up every few seconds tells you whether the water's creeping or gushing - so you can cut the tap before it hits the rim instead of mopping the floor after. The 'self-monitoring' part is just the tub watching its own water line.",
    "tensor": "A spreadsheet that can run in more than two directions. One number is a dot, a list is a row, a grid is a table - a tensor just keeps going into more directions, and it's the basic container AI uses to hold all its numbers.",
    "transformer": "The architecture behind nearly every modern AI. Its trick is reading everything at once and letting each piece decide which other pieces matter - that's what powers ChatGPT, image generators, and the rest.",
    "val-loss": "The pop quiz with questions it didn't study. During training you hold back some examples the model never sees, then test on those - if it aces what it studied but flunks the held-back quiz, it memorized instead of learned.",
    "vulkan": "The universal remote. A one-size-fits-all translator that lets AI software talk to graphics chips from any brand - not as finely tuned as NVIDIA's or Apple's own, but it works almost everywhere.",
}

CATEGORY = {
    "ablation": "Core concepts",
    "gradient-descent": "Core concepts",
    "machine-learning": "Core concepts",
    "dimensions": "Core concepts",
    "embeddings": "Core concepts",
    "agi": "Core concepts",
    "attention": "Architectures",
    "gguf": "Local inference & formats",
    "ggml": "Local inference & formats",
    "mlx": "Local inference & formats",
    "llamacpp-vs-ollama": "Local inference & formats",
    "cuda": "GPU compute & backends",
    "cudnn-cublas": "GPU compute & backends",
    "metal": "GPU compute & backends",
    "mps": "GPU compute & backends",
    "vulkan": "GPU compute & backends",
    "transformer": "Architectures",
    "gpt": "Architectures",
    "gan": "Architectures",
    "tensor": "Core concepts",
    "latent-space": "Core concepts",
    "parameters": "Core concepts",
    "lora": "Core concepts",
    "val-loss": "Core concepts",
    "gelu": "Building blocks",
    "relu": "Building blocks",
    "residual-connections": "Building blocks",
    "norm-placement": "Building blocks",
    "rss-sampler": "Local inference & formats",
    "precision": "Local inference & formats",
}

# Related terms (the "See also" chip row). Curated from each entry's See-also
# line plus the skill's cross-link map.
RELATED = {
    "ablation": ["machine-learning", "val-loss", "parameters"],
    "agi": ["machine-learning", "gpt"],
    "attention": ["transformer", "tensor", "lora"],
    "machine-learning": ["tensor", "transformer", "parameters", "val-loss", "agi", "gradient-descent"],
    "dimensions": ["tensor", "latent-space", "embeddings"],
    "embeddings": ["latent-space", "dimensions", "tensor"],
    "cuda": ["metal", "vulkan", "ggml", "cudnn-cublas"],
    "cudnn-cublas": ["cuda", "mps", "tensor"],
    "gan": ["latent-space"],
    "gelu": ["transformer", "gpt", "tensor", "relu"],
    "ggml": ["gguf", "tensor", "cuda", "metal", "vulkan", "rss-sampler"],
    "gguf": ["mlx", "ggml", "parameters", "rss-sampler", "precision"],
    "gpt": ["transformer", "gguf", "agi", "gelu"],
    "gradient-descent": ["machine-learning", "parameters", "val-loss", "latent-space", "norm-placement"],
    "latent-space": ["gan", "dimensions", "embeddings", "gradient-descent"],
    "llamacpp-vs-ollama": ["gguf", "ggml", "metal", "cuda", "vulkan"],
    "lora": ["transformer", "tensor", "gguf", "parameters"],
    "metal": ["cuda", "vulkan", "mlx", "mps", "ggml"],
    "mlx": ["gguf", "metal", "tensor"],
    "mps": ["metal", "mlx", "cuda", "cudnn-cublas"],
    "norm-placement": ["residual-connections", "transformer", "gradient-descent", "tensor"],
    "parameters": ["tensor", "transformer", "gguf", "lora", "val-loss", "gradient-descent", "rss-sampler", "precision"],
    "relu": ["gelu", "transformer", "tensor", "residual-connections"],
    "residual-connections": ["transformer", "relu", "tensor", "norm-placement"],
    "precision": ["gguf", "parameters", "rss-sampler", "tensor"],
    "rss-sampler": ["parameters", "gguf", "ggml", "precision"],
    "tensor": ["dimensions", "mlx", "transformer", "parameters", "gelu", "relu", "residual-connections", "norm-placement", "precision"],
    "transformer": ["attention", "gpt", "tensor", "lora", "gelu", "relu", "residual-connections", "norm-placement"],
    "val-loss": ["machine-learning", "parameters", "gradient-descent"],
    "vulkan": ["cuda", "metal", "ggml"],
}

WIKILINK = re.compile(r"\[\[([a-z0-9-]+)\]\]")


def toml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert_links(text: str) -> str:
    def repl(m):
        slug = m.group(1)
        if slug not in TITLE:
            print(f"  ! unknown wikilink target: {slug}", file=sys.stderr)
            return m.group(0)
        return f"[{INLINE[slug]}](/glossary/{slug}/)"
    return WIKILINK.sub(repl, text)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    slugs = sorted(TITLE)
    for slug in slugs:
        src = SRC / f"{slug}.md"
        if not src.exists():
            print(f"  ! missing source: {src}", file=sys.stderr)
            continue
        raw = src.read_text()

        # Drop the trailing "See also" paragraph from the body.
        body = re.split(r"\n\s*\*\*See also:\*\*", raw, maxsplit=1)[0]

        # Drop the leading "# Heading" line.
        lines = body.splitlines()
        if lines and lines[0].lstrip().startswith("#"):
            lines = lines[1:]
        body = "\n".join(lines).strip()
        body = convert_links(body)

        related = RELATED.get(slug, [])
        rel_toml = "[" + ", ".join(toml_str(r) for r in related) + "]"

        fm = [
            "+++",
            f"title = {toml_str(TITLE[slug])}",
            f"summary = {toml_str(SUMMARY[slug])}",
            f"category = {toml_str(CATEGORY[slug])}",
            f"related = {rel_toml}",
        ]
        if PLAIN.get(slug):
            fm.append(f"plain = {toml_str(PLAIN[slug])}")
        fm += [
            "+++",
            "",
        ]
        (OUT / f"{slug}.md").write_text("\n".join(fm) + body + "\n")
        print(f"  wrote content/glossary/{slug}.md")

    print(f"Done: {len(slugs)} terms.")


if __name__ == "__main__":
    main()
