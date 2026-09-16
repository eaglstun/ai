+++
title = "I'm Putting the Beagle Bros in Two AI Marketplaces"
date = 2026-09-14
description = "One portable skill, two marketplace wrappers, and an Apple II lesson about making software feel generous."
summary = "I turned the generous, funny spirit of the Beagle Bros into one portable agent skill, then wrapped the same files for the Claude and Codex marketplaces. The manifests are different. The thing they deliver is not: software that teaches without making anyone feel small."
tags = ["prompt-engineering", "tooling"]
semantic_id = "IY8zHf3eq4uj1cIBNyZUqBhfFfc-0BFS"
related_by_meaning = ["/practice/five-agents-one-marble/", "/blog/everyone-deserves-a-mascara-treat/", "/blog/my-whole-deal-is-now-a-toggle/", "/practice/four-painters-one-brief/"]
+++

I was born in 1980, so computers arrived in my life before I had enough context to find them
strange. My dad was the hardware guy. There were machines in the house, there were disks, and
there were manuals. No internet. No tutorial video waiting in another tab. If you wanted the
machine to do something new, you read whatever came in the box and tried it.

The Beagle Bros documents were different from everything else in the pile.

They were funny, for one thing. Not funny the way a corporation becomes funny after six people
approve a joke about Mondays. They were plainly made by people who were delighted by computers
and a little suspicious of anyone trying to make them sound solemn. The catalogs looked like
Victorian patent-medicine broadsides. Tips came with pointing hands. Product names had better
timing than some sitcoms.

But the jokes are not why I kept going back to them.

I was seven or eight years old. I wanted to make silly games, and a fair amount of what I typed
was still magic-incantation territory. Those documents never made me feel stupid for being at
the beginning. They assumed I was curious, capable, and on my way. You could laugh at a line one
year, understand the trick underneath it the next, and discover something else on the third
pass.

That is the part I wanted to keep.

So I made it an agent skill. Now I am packaging the same skill for the Claude and Codex
marketplaces, which has turned into a tidy little lesson about what should be portable and what
should stay platform-specific.

<!--more-->

{{< nyer-panel src="from-apple-ii-to-agent-skills.jpg" caption="The little pointing hand was doing more than decoration. It was inviting you in." alt="A warm retro illustration of an early home computer and a modern laptop sharing a wooden desk. A young man works at the laptop while an oversized cartoon pointing hand arcs from the old machine toward him." >}}

## A sensibility, not a costume

The obvious bad version of this project would be a nostalgia filter. Sprinkle in some
old-timey language, add a manicule, call every error a confounded contraption, and congratulate
yourself on having invented 1983.

That is not what made Beagle Bros useful.

The skill is built around a few practical rules. Technical substance comes first. The joke has
to survive beside the instruction, never in place of it. Irreverence points at the machine, the
bureaucracy, or the person writing the software. It never points down at somebody who has not
learned the trick yet. Good documentation volunteers the extra tip. Product copy can have a
pulse without hiding a warning or sanding off an important detail.

In short: be funny when funny helps, be plain when plain matters, and treat the person reading
like a smart friend.

That gives the agent something more useful than an impression to perform. It can rewrite a
README, sharpen release notes, warm up a CLI, improve an error message, name a feature, sketch a
Peeks & Pokes-style tip card, or look at a design and ask whether it teaches anything besides
how proud the designer is.

The invocation is deliberately boring:

```text
Use $beaglebros to rewrite this README introduction without losing any technical detail.
```

The last six words are doing real work. A funny manual that lies is still a bad manual. It just
has a hat now.

{{< bbros title="Peek & Poke" n="1" float="right" >}}
![A Victorian-style engraving of a top-hatted beagle peeking over an old home computer and pressing one oversized keyboard key with its paw.](peek-and-poke.png)

The skill does not load every historical note, writing example, and visual reference into every
request. It starts with a short description, then opens only the reference the job needs. Even
the top hat has a context budget.
{{< /bbros >}}

## One skill, two front doors

Claude and Codex can both use the same basic skill directory. At its center is a `SKILL.md`
file with a name, a description, and the operating instructions. Detailed material lives in
separate references for history, voice, visual language, and product ethos. That keeps the
entry point small and lets the agent pull in the part that matters for the current job.

The marketplace packaging around that directory is where the platforms differ.

The [public repository](https://github.com/eaglstun/skill-beaglebros) now has this shape:

```text
.
├── skills/beaglebros/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── .claude-plugin/plugin.json
└── .codex-plugin/plugin.json
```

Both plugin manifests point at the same `skills/` tree. Claude gets the plugin description it
expects. Codex gets its own plugin manifest plus the `agents/openai.yaml` presentation layer
for the skill list, default prompt, and automatic invocation policy. The wrappers know how to
introduce the package to their respective hosts. Neither wrapper owns the actual skill.

That distinction is small enough to miss and important enough to save future me from a mess.

I could have made a Claude version and a Codex version. They would be identical on day one,
nearly identical on day thirty, and quietly disagreeing by day ninety. A new writing rule would
land in one copy. A better historical reference would land in the other. One marketplace would
be teaching generosity while the other was still wearing last month's fake mustache.

{{< nyer-panel src="two-front-doors-one-workshop.jpg" caption="Two front doors. One workbench." alt="A two-color risograph illustration of red and blue doors on opposite sides, both connected by conveyor tracks to one central computer, toolbox, floppy disk, and two playful beagles." >}}

Instead, the shared skill stays boringly canonical. Platform-specific metadata sits at the
edges. Adding another host should mean writing another thin front door, not raising another
copy of the house.

## The description is the switchboard

A skill has to be discoverable before it can be useful. Both agents see the name and description
first, then decide whether the rest of the package belongs in the current conversation.

That makes the description less like marketing copy and more like routing code written in
English. It has to say what the skill changes and when that change is welcome. Too vague, and
the agent never reaches for it. Too broad, and suddenly a database migration is wearing a straw
boater and shouting "Behold!" at the transaction log.

The current description routes writing, documentation, product copy, error messages, naming,
retro visual direction, and design gut-checks into the skill. It does not claim the Beagle Bros
should supervise everything. Nobody needs a Victorian woodcut in a TLS certificate failure.

This is one of the things I like about skills as a form. A system prompt is atmosphere. A skill
is a tool with a handle. It has a boundary, supporting material, a reason to be selected, and a
moment when it should stay on the pegboard.

## What the marketplaces are actually distributing

The package is MIT-licensed and unofficial. It is inspired by the historical Beagle Bros
software house, not affiliated with it, endorsed by it, or pretending to resurrect the company.
The marketplace listings are not live yet. The shared package and both platform wrappers are
in place; submission is the next bit of paperwork.

The code is the least interesting part. There are no heroic dependencies, no service to keep
alive, and no elaborate installer waiting to ruin a Sunday. It is Markdown, a pair of small
manifests, and enough structure for two different agents to find the same set of ideas.

What gets distributed is a decision about how software should behave around people.

It should explain the trick. It should assume curiosity instead of incompetence. It should be
willing to have a personality without making that personality somebody else's problem. It
should remember that delight is not the enemy of rigor. Sometimes delight is what gets a kid to
read the same manual for the twentieth time, long enough for the strange incantation to become
something he understands.

I am packaging the skill for two modern AI marketplaces because distribution is how a tool gets
used. I am keeping one shared copy because the principle underneath it should not change with
the storefront.

The manifests open two doors. The same little pointing hand is waiting behind both of them.
