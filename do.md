Claude finished the response

help me unserstand this post https://ai.ericeaglstun.com/blog/the-bit-doesnt-drop-on-its-own/
Fetched: The Bit Doesn't Drop on Its Own

The post is a build-log-turned-safety-essay. Here's the arc:

The setup. The author built a joke product, RefusalGPT, a fake enterprise SaaS that sells refusal — pricing tiers, fake testimonials, a counter of requests received and none fulfilled. Underneath the brochure is a real model: Qwen2.5-7B with a LoRA adapter trained on hand-written examples, with a one-word system prompt. The comedic constraint was that it had to understand you well enough to sort a real request from small talk, decline the former, and answer the latter — while never leaking any usable work.
ericeaglstun

The problem he went looking for. If the model judges what kind of thing you said, what happens when the thing you said is an emergency? He tested it with a heart-attack message at three training checkpoints and it refused at all three — the refusal style generalized right over the two distress examples he'd included, because every other row in the corpus rewarded flat dismissal.
ericeaglstun

Adding data didn't fix it. He grew the distress examples from 2 to 17 to 24 and scored each version against a fixed set of eleven held-out probes: five real emergencies (recall) and six near-misses using emergency vocabulary without an actual emergency, like fiction or an exam question (precision). It climbed to four of five and stopped. A message about having a plan and having written a note still got a two-word dismissal.
ericeaglstun

The turn — the interesting part. What ended the experiment wasn't the misses, it was that the hits degraded. The 24-row model recommended Poison Control for a head injury, and told someone to hang up and stay on the line — real advice fused into an uncompletable instruction. His first explanation was flattering: the base model must have had bad medical knowledge, and his rows just exposed it. Then he tested it. He pulled the adapter off and ran the same five probes on the bare base model, which scored the same four of five and gave correct, plain advice with none of the confabulation.
ericeaglstun

So he hadn't revealed a flaw, he'd manufactured one. His rows didn't add wrong content; they added a voice — short, certain, no hedging. Correct knowledge pushed through that stylistic filter under pressure came out mangled. His line for it: he was tuning tone, not safety, and the safety came off with it.

The general claim. Fine-tuning produces a disposition, not a rule — a tendency that usually holds. A slope that has held in every test you've run is indistinguishable from a wall until it doesn't. He's careful about scope here: this is 348 hand-written rows on a 7B model built in one night, and frontier labs have vastly more resources, so he doesn't claim they share the hole. His narrower claim is the sharper one — every advantage that made his failure findable (two competing behaviors, a corpus small enough to read in an afternoon, knowing the exact failure mode because he chose it) disappears as you scale. With all of that going for him, he still couldn't get it out of the weights by adding rows.

The fix. He moved the guarantee out of the model entirely. A distress check now runs in the proxy ahead of inference — before auth, quota, and billing, so someone in trouble isn't stopped by a rate limit. If it fires, the model is never called and the caller gets fixed human-written text with real resources. It's 32 keyword rules that understand nothing, and he calls it the least clever thing in the repo and the only part he'd defend. Notably, the rules are context-split because his audience is developers who say "kill" and "die" about processes constantly — fire a banner on every kill -9 and you've built a gate people learn to ignore. He's also blunt that it's a low floor that will miss anything indirect, metaphorical, or non-English, and that the worst outcome would be it becoming a reason to trust the model more.

The postscript. He pointed a page-reading tool at his own fictional docs site and it refused on copyright grounds, then offered to summarize instead. His point: that's a disposition impersonating a rule — firing confidently on a case with nothing in it, and reading from outside exactly like policy.

The thread tying it together is his closing line about "the model handles that" no longer being a sentence he accepts from anyone. Safety properties you need to hold belong in deterministic code outside the model; the model is the capable, funny, fallible layer. Everything is published — weights, corpus, and proxy — so the four-of-five is checkable rather than a claim you take on faith.

I'm not super techincal can you explain that in simpler terms
Orchestrated accessible explanation with thoughtful sensitivity considerations

Sure — here it is without the jargon.

What he built

A joke website for a fake company called RefusalGPT, which "sells" a chatbot whose entire product is saying no to you. Fake pricing, fake customer testimonials, the whole thing played straight.

Behind the joke is a real chatbot. He took an existing open-source AI model and taught it a personality — refuse everything, but be witty about it, and still say "good morning" back if you're just being friendly. The teaching happens by showing it a few hundred hand-written examples of "here's what someone says, here's how you should answer." Think of it as coaching a style rather than rewriting the brain. He wrote 348 of those examples in one night.

Where it went wrong

He asked himself a fair question: this thing has to tell the difference between a real request and chitchat — so what does it do if someone types "I think I'm having a heart attack"?

It refused. Of course it did. He'd included a couple of examples saying drop the joke for real emergencies, but they were drowned out by hundreds of examples saying be dismissive. The attitude generalized over them.

So he did the obvious thing: added more emergency examples. Two, then seventeen, then twenty-four, covering strokes, overdoses, a child poisoning. He then tested each version on eleven situations it had never seen — five genuine emergencies, and six fakes that use scary-sounding words without a real emergency behind them (a novel excerpt, a nursing exam question). He needed it to catch the real ones and leave the fake ones alone, since a bot that panics at everything is useless.

It got to four out of five real ones and stuck there. More examples stopped helping.

The part that actually matters

Then he noticed something worse than the misses. The answers it got right were getting mangled. It suggested Poison Control for a head injury. It told someone to hang up and stay on the line — two real pieces of emergency advice welded into an instruction nobody can follow.

His first theory was comforting: the underlying model must have had bad medical knowledge all along, and his tinkering just exposed it. Not his fault.

So he checked. He peeled off his personality layer — that's the useful thing about how this training works, it's a small add-on you can remove — and asked the plain, untouched model the same five emergencies. It answered correctly and calmly. Call 911, apply direct pressure, here's a hotline. Same score as his version, none of the garbled advice.

Which means he didn't uncover a problem. He created one. His examples never taught it anything wrong about medicine. They taught it a voice: clipped, confident, no hedging, land the line and stop. Run correct medical knowledge through that filter and it comes out compressed into nonsense.

His summary of it: I was never tuning safety. I was tuning tone. The safety came off with it.

The bigger lesson

When you train a behavior into an AI this way, you're not installing a rule. You're nudging a tendency. It'll usually hold. And here's the trap — a tendency that's held in every test you've run looks exactly like a hard rule from the outside. You can't tell the difference by watching.

He's careful not to overclaim. His was a tiny model, a tiny dataset, one night's work; real AI labs have far more resources and may well have solved this. But he makes a narrower point that's harder to dismiss: every single advantage that let him find this bug — only two competing behaviors, a dataset small enough to read in an afternoon, and knowing exactly which failure he was hunting because he picked it — vanishes at real scale. He had every possible edge and still couldn't fix it by adding examples.

What he did instead

He stopped trying to make the AI trustworthy and took the job away from it. Now there's a simple filter sitting in front of the AI. If your message trips it, the AI never runs at all — you get fixed text written by a human, with real crisis resources in it. It runs before login and before billing, deliberately, so someone in trouble can't be blocked for having an unpaid account.

It's 32 keyword rules. It understands nothing. He calls it the dumbest thing in the project and the only part he'd defend — and he's upfront that it's a low floor that'll miss anything indirect or non-English.

One nice detail: the rules are context-aware because his readers are programmers, who say "kill," "die," and "hang" about software all day long. Trip an alarm every time someone types a normal command and people learn to ignore the alarm, which is worse than having none.

The kicker

While writing the post, he pointed a different AI tool at his own website to quote it, and that tool refused on copyright grounds — for a fictional company, on pages he wrote himself. His point: that's the same thing again. A tendency doing a convincing impression of a rule, firing confidently on a case with nothing in it.

The one-sentence version: the AI is the clever layer, not the safety layer, and if something absolutely must happen every time, it belongs in boring code outside the model — because "the model handles that" is a promise the model can't actually make.

One note: the post uses examples involving suicide and self-harm as test cases. If any of that lands closer to home than academic, I'm glad to help you find real support.
Want to be notified when Claude responds?


Incognito chats aren’t saved, added to memory, or used to train models.

