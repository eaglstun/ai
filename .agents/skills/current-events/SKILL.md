---
name: current-events
description: Turn recent AI/ML news into post hooks in Eric's voice for ai.ericeaglstun.com (blog, Threads, deep-dives). Use when Eric asks "what's happening in AI", "any post ideas from the news", "what should I write about", "give me a hook", wants to react to a release/paper/drama, or wants to refresh the seed list. Sweeps the news, filters for what's hook-worthy for HIS angle, ties each idea back to existing site content, and writes post seeds. Research + judgment, not auto-posting.
metadata: meta
version: 1.0.0
public: true
---

# Current events to post hooks

A scout for the content funnel. The job is not "summarize the news." It is: find the
two or three things in recent AI/ML that Eric could say something **only Eric would say**
about, and hand back ready-to-write seeds that already know which site page they link to.

The funnel never changes (see `meta/strategy.md`): a post, someone feels something, they
click, they read the site. So a good seed is one where Eric's angle naturally pulls the
reader toward a glossary term, a past post, or a deep-dive. A clever take with nowhere to
click is half a seed.

## What makes a hook worth surfacing (the filter)

Most AI news is noise for this purpose. Keep only items that pass at least one:

- **Eric has a weird-but-true analogy for it.** The mechanism maps onto something human,
  artistic, or absurd (Devo, magicians, karaoke, de-evolution). If the analogy writes
  itself, surface it.
- **It contradicts the hype consensus.** Eric's voice is "I go to magicians to be surprised,
  not to learn the trick." Counter-narratives and deflations beat breathless recaps.
- **It touches Anthropic, and there's a principled critique to make.** Thoughtful criticism of
  Anthropic is what a credible, independent AI thinker does, so it's an ASSET on this site (and it
  serves the downstream Anthropic hiring outcome too), not a risk. Do not soften it.
  A sharp, fair critique of an Anthropic decision is among the highest-value seeds here.
- **It connects to something already on the site.** A new release that makes an existing
  glossary term suddenly concrete, or extends a past post's argument, is gold: the click is
  built in.

Reject: pure funding/headcount churn, vendor press releases with no idea inside, anything
that needs Eric to pretend expertise he does not claim (he plans and judges, he does not
write the math, see authorship honesty below).

## How to run it

1. **Sweep.** Use WebSearch with recency for the last 1 to 2 weeks. Cover several angles in
   parallel, do not rely on one query: major lab releases (Anthropic, OpenAI, Google, Meta,
   Mistral, DeepSeek, Qwen), notable papers/benchmarks, on-device / Apple-Silicon / local-model
   news (Eric's home-lab beat), and the AI discourse itself (what people are actually arguing
   about on Threads/HN). WebFetch the primary source before trusting a headline; treat any
   single summary as ~95% reliable, verify a claim before Eric would publish it.
2. **Filter** the haul through the criteria above. Aim for 2 to 4 keepers, not a digest.
3. **Connect each keeper to the site.** Search `content/glossary/` and `content/blog/` +
   `content/deep-dives/` for the term or theme it touches. Name the exact page the seed
   should link to. If nothing on the site fits, say so (that itself may be a glossary gap
   worth noting).
4. **Write the seed** in the format below.
5. **Cross-check dates.** Anything Eric would publish that says "this week" or names a date
   gets pinned to an absolute date, per the repo's date-anchoring convention.

## Seed format

Surface seeds in chat, and (unless told otherwise) write every sweep to this skill's own
archive at `archive/YYYY-MM-DD.md` (relative to this skill's base dir), so the run history
travels with the skill. One file per sweep; if a file for today already exists, append a new
`## <HH:MM UTC>` section to it rather than overwriting. One seed looks like:

```
### <attention-grabbing working title, voice-forward, not a summary>
- **The news:** one line, with the primary source URL and the date it broke.
- **Eric's angle:** the take only he would have. The analogy, the contrarian read, the
  Anthropic critique. 2 to 3 sentences.
- **The click:** which site page it links to (/glossary/<slug>/, a past post) and why the
  reader would want to go there.
- **Route:** blog | practice | deep-dive | Threads reply  (per the routing rules in CLAUDE.md)
- **Freshness:** how date-sensitive it is (a "react now" beat vs an evergreen idea).
```

Good titles hook and carry voice (the project memory holds blessed examples). When a line is
sharper than the post that would hold it, drop it in `inbox/quote-bank.md` instead.

## Voice and honesty guardrails

- Write seeds and any drafted copy under the `site-voice` rules. Load that skill before
  writing prose that ships under Eric's name. No em dashes anywhere in this repo, by hand.
- **Authorship honesty:** in technical takes, never imply Eric writes or reads the code. He
  plans, builds skills, and judges behavior (general-contractor framing). Attribute code to
  the agent.
- The voice is artist/communicator: weird analogies, non sequiturs, the Devo / de-evolution
  motif as a sanctioned recurring bit. It is brand-building. The voice is the product.

## This skill does not post

It produces seeds and drafts only. Publishing to Threads is the `threads` skill's job, and a
publish is always an explicit, separate, human-approved step. Keep the two apart.
