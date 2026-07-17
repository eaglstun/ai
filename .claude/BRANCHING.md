# Branching and publish flow

This repo is PUBLIC on GitHub (eaglstun/ai). Anything committed to a pushed
branch is published, no matter the branch name. The flow below keeps personal
material out of git entirely and gates what little crosses to main.

## The flow

1. **All work happens on `dev`.** Site content, skills, agents, scripts.
   Main is a merge target, not a workbench.
2. **Personal data never enters git.** `.gitignore` blocks
   `.claude/skills/threads/posts/`, `.claude/skills/threads/metrics/`,
   `.claude/skills/linkedin/linked-*.md`, plus the long-standing `inbox/`,
   `meta/`, `.env`. Those files live in the working tree only.
3. **Before merging dev -> main:** run the `repo-sanitizer` agent
   (`.claude/agents/repo-sanitizer.md`). It reviews the dev..main diff for
   personal details no regex can catch (metrics in prose, account specifics)
   and strips them in place. Then `python3 scripts/publish-skills.py scan`
   as the deterministic backstop.
4. **PR dev -> main:** the `publish-skills.yml` workflow runs the same leak
   scan as a required check.
5. **On merge to main:** the workflow rebuilds the public bundle and syncs it
   to the public skills repo (`vars.PUBLISH_REPO`, kepano/obsidian-skills
   style layout).

## Publishing a skill or agent

Opt-in only. Add to the YAML frontmatter:

```yaml
public: true
```

Nothing publishes without the flag. Flagged items still pass the leak scan
and the always-private path check before leaving the repo.

## One-time setup (manual)

- Create the public repo and set `vars.PUBLISH_REPO` (e.g. `eaglstun/skills`).
- Add `secrets.PUBLISH_TOKEN`: fine-grained PAT, contents:write on that repo.
- Branch protection on main: require the leak-scan check, require PRs.
