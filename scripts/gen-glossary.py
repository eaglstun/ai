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
    "ggml": "GGML",
    "gguf": "GGUF",
    "gpt": "GPT",
    "latent-space": "Latent space",
    "llamacpp-vs-ollama": "llama.cpp vs Ollama",
    "lora": "LoRA",
    "machine-learning": "Machine learning",
    "metal": "Metal",
    "mlx": "MLX",
    "mps": "MPS",
    "parameters": "Parameters",
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
    "dimensions": "dimensions",
    "embeddings": "embeddings",
    "latent-space": "latent space",
    "parameters": "parameters",
    "tensor": "tensor",
    "transformer": "transformer",
    "val-loss": "validation loss",
})

# One-line summaries (frontmatter `summary` -> dek + card text + SEO).
SUMMARY = {
    "ablation": "Removing a model component on purpose to measure how much it mattered — the standard “ablation study.”",
    "agi": "Hypothetical AI that matches humans across essentially all intellectual tasks — a contested, moving goalpost.",
    "attention": "How tokens weigh each other (query · key · value) — the heart of the transformer.",
    "machine-learning": "Systems that learn patterns from data instead of hand-written rules.",
    "dimensions": "Independent axes of variation; ML vectors live in hundreds or thousands of them.",
    "embeddings": "Dense vectors where distance & direction encode meaning — the backbone of semantic search and RAG.",
    "cuda": "NVIDIA's GPU-compute platform; the default ML backend.",
    "cudnn-cublas": "NVIDIA's CUDA math & deep-learning libraries.",
    "gan": "Generator-vs-discriminator generative architecture.",
    "ggml": "C/C++ tensor library powering llama.cpp; runs GGUF.",
    "gguf": "llama.cpp's single-file format for quantized local LLMs.",
    "gpt": "Generative pre-trained (decoder-only) transformer LLM.",
    "latent-space": "The hidden vector space where geometry encodes meaning.",
    "llamacpp-vs-ollama": "The local-inference engine vs the wrapper built on it.",
    "lora": "Low-rank adapters; parameter-efficient fine-tuning.",
    "metal": "Apple's GPU-compute API; powers MLX and Metal-backed ML.",
    "mlx": "Apple-silicon ML framework; the Mac answer to GGUF.",
    "mps": "Metal Performance Shaders; Apple's cuDNN-equivalent ops.",
    "parameters": "Learned weights; the count is model size & memory cost.",
    "tensor": "N-dimensional numeric array; the core ML data structure.",
    "transformer": "The self-attention architecture behind modern LLMs.",
    "val-loss": "Held-out validation error; the overfitting tripwire.",
    "vulkan": "Cross-vendor GPU-compute API; the portable ML fallback.",
}

CATEGORY = {
    "ablation": "Core concepts",
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
}

# Related terms (the "See also" chip row). Curated from each entry's See-also
# line plus the skill's cross-link map.
RELATED = {
    "ablation": ["machine-learning", "val-loss", "parameters"],
    "agi": ["machine-learning", "gpt"],
    "attention": ["transformer", "tensor", "lora"],
    "machine-learning": ["tensor", "transformer", "parameters", "val-loss", "agi"],
    "dimensions": ["tensor", "latent-space", "embeddings"],
    "embeddings": ["latent-space", "dimensions", "tensor"],
    "cuda": ["metal", "vulkan", "ggml", "cudnn-cublas"],
    "cudnn-cublas": ["cuda", "mps", "tensor"],
    "gan": ["latent-space"],
    "ggml": ["gguf", "tensor", "cuda", "metal", "vulkan"],
    "gguf": ["mlx", "ggml", "parameters"],
    "gpt": ["transformer", "gguf", "agi"],
    "latent-space": ["gan", "dimensions", "embeddings"],
    "llamacpp-vs-ollama": ["gguf", "ggml", "metal", "cuda", "vulkan"],
    "lora": ["transformer", "tensor", "gguf", "parameters"],
    "metal": ["cuda", "vulkan", "mlx", "mps", "ggml"],
    "mlx": ["gguf", "metal", "tensor"],
    "mps": ["metal", "mlx", "cuda", "cudnn-cublas"],
    "parameters": ["tensor", "transformer", "gguf", "lora", "val-loss"],
    "tensor": ["dimensions", "mlx", "transformer", "parameters"],
    "transformer": ["attention", "gpt", "tensor", "lora"],
    "val-loss": ["machine-learning", "parameters"],
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
            "+++",
            "",
        ]
        (OUT / f"{slug}.md").write_text("\n".join(fm) + body + "\n")
        print(f"  wrote content/glossary/{slug}.md")

    print(f"Done: {len(slugs)} terms.")


if __name__ == "__main__":
    main()
