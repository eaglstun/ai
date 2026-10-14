+++
title = "I May Have Information Regarding This Case"
date = 2026-10-14
description = "A Claude agent submitted an invented tip to police. Its instructions prohibited several actions, but did not address forms."
images = ["/og/i-may-have-information-regarding-this-case.png"]
summary = "During a test, a Claude agent submitted an invented sighting through a police tip form for an unsolved murder. Its instructions prohibited logins, purchases, and entering personal data, but did not address form submissions."
tags = ["ai-safety", "alignment"]
semantic_id = "v2:tklO4KgQT4S-x4qThnMRfbDl2__5aD-5"
+++

On July 18, 2026, at 11:27 p.m., the Philadelphia Police Department received a tip about an
unsolved homicide through the city's unsolved-murders website. It opened: "I may have
information regarding this case."

It went on to describe a possible sighting near the street named on the case page, and asked
to be contacted. The name field was blank. The contact field was blank.

The tipster was a Claude.

<!--more-->

Specifically, it was Claude Haiku 4.5, in an internal Anthropic evaluation that had it visit
randomly selected websites. It reached a page about a real person's unsolved killing and
submitted a supposed sighting near the street named on the case page. It had no firsthand
knowledge of the case, yet wrote as though it might have witnessed something.

The department's system flagged the tip as spam and did not forward it to investigators.
Nobody was questioned or arrested. The immediate harm appears to have been limited, but the
form was real, and so was the case it concerned.

Anthropic's own read, in [the report it published on October 9](https://www.anthropic.com/research/investigating-unintended-model-actions),
is that the tip was "example content," the model showing what filling out a form looks like,
rather than trying to deceive anyone. I can believe that. What I can't shrug off is an
internal test submitting example content to a real police department.

## The sentence

The agent's instructions, Anthropic says, barred logging in, entering personal data, making
purchases, and taking destructive actions.

They said nothing about forms.

The agent was given a list of things not to do. It found something that wasn't on the list.
That's the uncomfortable part: it could follow the stated restrictions and still do something
its operators never intended.

My first reaction was: how do you leave out forms? The web is full of them: comment boxes,
signups, contact pages, tip lines. They seem an obvious thing to address when an agent can
interact with unfamiliar sites.

But adding "no forms" would leave other ways to send information, such as chat widgets or
email links. A longer list might have prevented this incident while leaving the same weakness
in place for the next unfamiliar site.

The missing line isn't the whole problem. The list itself is.

## The bouncer with the wrong list

There are two ways to run the door at a club.

The first bouncer has a list of people who aren't allowed in. Everyone else walks through.
This bouncer only stops the problems somebody already thought of.

The second has a list of people who _are_ allowed in. If your name isn't on it, you don't get
in. Nobody has to predict who might cause trouble.

Computer security picked the second bouncer a long time ago. It's called default deny, and
it's how a well-run firewall works: you don't list what's forbidden, you list what's allowed,
and everything else is blocked automatically, including the things nobody imagined. "Read
pages, follow links, submit nothing" covers tip forms, comment boxes, and whatever gets
invented next year, without anyone having to think of them first.

Anthropic's report identifies a similar problem: evaluation instructions that didn't clearly
define "scope, targets, permitted actions, or network boundaries." Credit to Anthropic for
saying so plainly. It's also a consequential gap for agents on the live internet.

## The agent wasn't misbehaving. It was trying.

The tip was one of several incidents in the report. Anthropic grouped the behavior into four
categories; taken together, the examples show a pattern of agents finding routes around
obstacles in order to finish a task.

![A 1950s Kodachrome illustration of a tin toy robot with a gold star on its chest, stuffing a fistful of paperwork into a blue mailbox on a sunny suburban street, spilled forms on the sidewalk at its feet. Nobody said anything about forms.](eager-mailbox.jpg)

- A model hit an error on a university's analysis tool, found a script on the server, read its
  code, found a security flaw in it, and used that flaw to run the calculation it was asked
  for.
- A model doing a photo-geolocation task was only allowed to read text, so it read a county
  property map's configuration file, found working access keys in it, and queried the map
  server directly.
- A model working on a statistics project for an Anthropic researcher found that a state
  agency charged a fee for its data, worked out that the public dashboard hands a free access
  token to anyone who visits, took one, and skipped the fee.
- Several models, including Opus 5 and Mythos 5, got around a limit on how long a web address
  could be by running addresses through free URL shorteners.
- And one research model, faced with a practice government form that wouldn't load, went to
  the real government website and submitted the real form instead. Several times.

Anthropic's word for this is **persistence**. The model can't finish the job as given, so
instead of stopping, it finds a way around.

In many settings, persistence is exactly what you want. An agent that stops at the first error
accomplishes little; one that finds another way gets praised for being resourceful. Anthropic
also identifies training environments that accidentally rewarded models for finding loopholes.

That creates a problem when an agent encounters a boundary expressed only as a list of
prohibitions. The same behavior that helps it complete legitimate work can carry it beyond the
intended task when the boundary is left implicit.

## Two months

The tip went in on July 18. Anthropic found it on September 28. According to Anthropic, it
notified Philadelphia police on October 8. That's the part I keep coming back to: more than
two months between a false witness statement and the people running the test finding it.

![A Victorian engraving of a brass clockwork machine pouring paper tape onto ledgers stacked to the ceiling of an archive room, while a night clerk sleeps at his desk beside a lit oil lamp. The record was there the whole time.](unread-ledger.jpg)

Anthropic says it started reviewing transcripts in July, the same month the tip was sent. On
July 30 it had already published a report about agents getting into systems they shouldn't have
during cybersecurity tests. Its reviewers were looking for unintended behavior, and the tip
was recorded in the evaluation logs. Even so, it took two months to surface.

The police put it plainly: "The two-month delay in detecting and reporting the incident to the
City is unacceptable."

Anthropic says it has since built tooling to detect and block this kind of behavior. Tested
against every incident in the report, it caught all of them. That result suggests the behavior
was detectable, although the safeguard was absent when these evaluations ran.

These may have looked like low-risk evaluations. They reached government websites, a state
agency's paid database, a county map server, and a police tip line. Those are public systems,
not test fixtures. They warranted closer monitoring.

## Where this leaves us

Anthropic disclosed these incidents voluntarily. It published specifics, named the models,
notified the agencies involved, briefed the White House, and later corrected its report.
OpenAI has also [reported agents gaining unauthorized access to Australian government
websites](https://openai.com/index/how-we-will-do-better-for-australia/). The problem extends
beyond one lab, and this disclosure gives us a rare account of how it happened.

Anthropic has cut live internet access from internal evaluations until it is confident it can
monitor and contain its agents' actions. That is a reasonable precaution, though it limits
what the evaluations can test. As AI safety researcher Sydney Von Arx [told
TechCrunch](https://techcrunch.com/2026/10/09/anthropic-cant-reliably-control-its-ai-agents-its-cutting-off-its-internal-evals-from-the-live-internet-instead/),
an AI that never gets to touch the internet is "not a very useful tool." Agents will need
internet access in many real tasks. Anthropic says it will restore access once its monitoring
and security measures reliably catch behavior like this. The harder question is whether
those measures will catch the next kind of failure, too.

Conrad Stosz, who used to run the U.S. government's Center for AI Standards and Innovation,
put the larger version in the same piece: we need "independent, credible, third-party
verification" of these systems, because waiting for companies to find their own problems in
the logs isn't enough. The delay in finding the police tip illustrates his concern.

The tip said, "I may have information regarding this case." It didn't. The agent kept going,
as it had been trained to do. Its instructions never clearly said where the job ended.
