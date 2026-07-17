#!/usr/bin/env python3
"""Build the public-facing skills/agents bundle, or scan the tree for leaks.

Modes:
  build (default)  Copy every skill/agent whose frontmatter carries
                   `public: true` into dist/public-skills/ (kepano/
                   obsidian-skills layout: skills/<name>/..., agents/<name>.md),
                   write an index README, then run the sensitive-pattern scan
                   over the output. Non-zero exit if anything is flagged.
  scan             Run the sensitive-pattern scan over ALL git-tracked files
                   under .claude/ and scripts/ (the PR gate). Non-zero exit
                   on any hit.

The scan is the deterministic backstop; the judgment pass is the
repo-sanitizer agent (.claude/agents/repo-sanitizer.md). Both run before
anything reaches main; only `public: true` material ever leaves this repo.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"
AGENTS = ROOT / ".claude" / "agents"
DIST = ROOT / "dist" / "public-skills"

# Paths that never publish, flag or no flag (defense in depth vs .gitignore).
ALWAYS_PRIVATE = ("threads/posts", "threads/metrics", "linked-")

SENSITIVE = [
    (re.compile(r"EAA[0-9A-Za-z]{20,}"), "Meta access token"),
    (re.compile(r"\b(sk|ghp|gho|r8|hf)_[A-Za-z0-9]{16,}"), "API key"),
    (re.compile(
        r"(?i)(api[_-]?key|client[_-]?secret|access[_-]?token|password)"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"), "credential assignment"),
    (re.compile(r"\b(192\.168|10\.\d{1,3})\.\d{1,3}\.\d{1,3}\b"), "LAN IP"),
    (re.compile(r"/Users/eeaglstun"), "personal absolute path"),
    (re.compile(r"postpostmodern@gmail\.com"), "personal email"),
    (re.compile(r"\b\d{15,}\b"), "long numeric ID (app/account?)"),
]


def frontmatter_is_public(md: Path) -> bool:
    text = md.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    fm = text[:end] if end != -1 else text
    return re.search(r"(?m)^public:\s*true\s*$", fm) is not None


def scan_file(path: Path) -> list[str]:
    hits = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return hits
    for lineno, line in enumerate(text.splitlines(), 1):
        for rx, label in SENSITIVE:
            if rx.search(line):
                hits.append(f"{path}:{lineno}: [{label}] {line.strip()[:100]}")
    return hits


def mode_scan() -> int:
    tracked = subprocess.run(
        ["git", "ls-files", ".claude", "scripts"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    me = Path(__file__).resolve()
    hits = []
    for rel in tracked:
        path = (ROOT / rel).resolve()
        if path == me:  # the scanner's own regexes would self-flag
            continue
        hits += scan_file(path)
    if hits:
        print(f"LEAK SCAN FAILED: {len(hits)} hit(s)")
        print("\n".join(hits))
        return 1
    print(f"leak scan clean ({len(tracked)} tracked files)")
    return 0


def mode_build() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    published = []

    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        if not frontmatter_is_public(skill_md):
            continue
        name = skill_md.parent.name
        dest = DIST / "skills" / name
        shutil.copytree(
            skill_md.parent, dest,
            ignore=shutil.ignore_patterns(".DS_Store", "*.pyc", "__pycache__"),
        )
        published.append(f"skills/{name}")

    for agent_md in sorted(AGENTS.glob("*.md")):
        if not frontmatter_is_public(agent_md):
            continue
        dest = DIST / "agents" / agent_md.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_md, dest)
        published.append(f"agents/{agent_md.name}")

    if not published:
        print("nothing flagged public: true; dist not created")
        return 0

    # Belt: refuse if an always-private path slipped into the output.
    for p in DIST.rglob("*"):
        rel = str(p.relative_to(DIST))
        if any(marker in rel for marker in ALWAYS_PRIVATE):
            print(f"REFUSING: always-private path in output: {rel}")
            return 1

    hits = []
    for p in DIST.rglob("*"):
        if p.is_file():
            hits += scan_file(p)
    if hits:
        print(f"PUBLISH BLOCKED: {len(hits)} sensitive hit(s) in dist")
        print("\n".join(hits))
        return 1

    index = ["# Skills and agents\n",
             "Published automatically from the private working repo. "
             "Each skill follows the Agent Skills spec (SKILL.md + "
             "references/).\n"]
    index += [f"- `{item}`" for item in published]
    (DIST / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")

    print(f"built dist/public-skills with {len(published)} item(s):")
    print("\n".join(f"  {i}" for i in published))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "build"
    if mode == "scan":
        sys.exit(mode_scan())
    elif mode == "build":
        sys.exit(mode_build())
    print(f"unknown mode: {mode} (use: build | scan)")
    sys.exit(2)
