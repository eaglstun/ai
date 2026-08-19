+++
title = "I Gave Five Agents One Marble and Told Them to Stay in Their Lane"
date = 2026-08-29
images = ["/og/five-agents-one-marble.png"]
description = "MARBLE has five specialist agents. Their job descriptions are mostly lists of things they are forbidden to improve."
summary = "MARBLE MAGNIFICENCE has specialist agents for level shape, block geometry, rendering, criticism, and music. The useful part isn't what each one knows. It's what each one is forbidden to touch - and why the critic has to leave the bug broken when it finds one."
tags = ["prompt-engineering", "tooling"]
+++

I am building a game called [MARBLE
MAGNIFICENCE](https://marble.baby/). The title screen
says that, anyway. The bundle still says `Marble`, which is one of several small indignities
standing between it and TestFlight.

It is an isometric 3D marble roller that keeps derailing into other games. You roll down a
mountain, fall through a trapdoor under a Roman statue, ride a tunnel beneath the island, and
occasionally get abducted into skeeball or a Pac-Man-shaped maze. There is an ice course, a
rainbow hall, an Escher loop where gravity changes its mind, and a mode where the marble stops
rolling entirely and borrows your face from the front camera. The game is written in native
Swift, rendered with SceneKit, and driven by a hand-written sphere solver running at 120 Hz,
because a general-purpose physics engine has standards and the marble does not.

The project also has five specialist coding agents:

- one shapes levels;
- one invents the blocks levels are made from;
- one controls materials, light, color, shadows, and camera framing;
- one composes the soundtrack;
- and one walks in afterward looking for holes everyone else missed.

The useful thing about them is not that each has a colorful little job title. The useful thing
is that every job description is mostly a list of things the agent is **not allowed to do**.

<!--more-->

## Five jobs and a lot of no

The level-shaping agent owns the mountain: terraces, routes, chutes, statues, rails, fences,
furniture. It may arrange the pieces. It may not invent a new piece because the route would be
easier to build if only there were a special little wedge right here.

The block-kit agent owns the pieces: ramps, corners, curves, funnels, arches. It may perform the
unpleasant arithmetic that makes a folded surface tile cleanly on an integer grid. It may not
place the new block in a level, even if the perfect spot is obvious and practically begging.

The rendering agent owns the look: materials, palette, light, shadows, procedural textures,
camera framing. It may not repair a hole by making the hole the same color as the floor. If the
geometry is wrong, it has to say the geometry is wrong and put the paintbrush down.

The soundtrack agent writes and auditions music in TidalCycles, then carries an approved piece
through the deterministic Swift synthesis pipeline. It may not change the course because the
bridge would sound better if the marble arrived four seconds earlier. That is a request, not a
license to move the bridge.

The geometry critic is the strangest one. It may inspect the baked level, probe the collision
surface, rank defects, and write regression tests. It may **not fix anything it finds**.

That last boundary sounds wasteful until you watch what happens without it. The same agent that
writes the bug can explain why the bug is not really a bug with astonishing fluency. Give the
critic permission to repair its own finding and the investigation quietly becomes a negotiation:
perhaps this notch is structural; perhaps the marble was always supposed to catch here; perhaps
the new test could sample two inches to the left where everything is beautiful.

So the critic leaves a failing test on the floor like a chalk outline. The level agent or the
block agent has to make it pass. The witness is not also the defendant's tailor.

{{< nyer-panel
  src="the-locked-toolbox.png"
  caption="The critic may point at the hole. The toolbox belongs to somebody else."
  alt="A flash-lit instant photograph of a dark wooden workshop floor. A small square hole is surrounded by a large chalk outline, while a padlocked wooden toolbox sits beyond it under a bare bulb."
>}}

## Every real hole lived at the edge

The critic's instructions contain the best sentence in the whole setup:

> Assume the suite is green and the level is still broken, because that has been true every time.

MARBLE's mountain is generated from tables: terrace radii, heights, ramp faces, offsets. Render
and collision meshes are baked from the same placements so the world you see and the world you
hit cannot drift apart. There are hundreds of tests. A surprising number of those tests were once
walking politely down the center of a ramp while the actual defects waited at both shoulders.

A hipped ramp cut notches into its own entrance. A chute stranded one raised finger of ground
with a slot beside it. Cubes added to plug a gap stood proud of the terrace exactly where the
marble rolled on. Every one looked fine from the center line. Every one was obvious when someone
finally swept across the full width.

That history is now part of the critic's contract:

- probe the baked mesh, not the table that generated it;
- sweep across a route, not only along it;
- sample seams on purpose;
- count the samples, because a loop that accidentally checks nothing still passes very quickly;
- break the feature once to prove the new test has teeth.

{{< nyer-panel
  src="the-critic-and-the-hole.png"
  caption="The critic has located the problem. Nobody cross the velvet rope until the correct trade arrives."
  alt="A grainy, sodium-orange photograph of a person in white coveralls standing behind velvet ropes and looking into a perfectly black hole in the floor. A paint roller is tucked behind their back and a bucket sits nearby."
>}}

This is the difference between giving an agent a role and giving it a trade. "Review the level"
is a role. "Every previous defect hid at an edge, use this surface probe, leave a failing test,
and do not fix the source" is a trade. One sounds capable. The other comes back with coordinates.

## The generator keeps the mountain; my mouse gets a vote

The levels are code-generated, which is wonderful until you want to put one statue three cells
to the left because it looks lonely.

There is now a companion Mac app called `MarbleEditor`. Pick a block or prop, move the ghost with
the mouse, rotate it, click it against the top of a terrace or the side of a wall, save. It is the
normal pleasant scene-editor interaction that makes a person briefly forget the mountain is
otherwise several thousand lines of decisions made by Swift.

The editor does not save a level. It saves a **diff**.

`MountainLevel.make()` remains in charge of the mountain's shape. The editor records only what I
added and removed, and the game applies that small overlay at the next build. If an agent widens
every terrace by changing one number, the generator can still do that. My hand-placed urns and
gargoyles survive on top. Neither side has to flatten the other into a giant JSON settlement.

{{< nyer-panel
  src="the-mountain-and-the-overlay.png"
  caption="The generator keeps the mountain. My mouse gets the cat and the urn."
  alt="An antique woodcut of a huge terraced circular mountain, partially covered by a visibly pasted sheet bearing a small cat and an urn, like hand-authored objects layered over a generated world."
>}}

This turns out to be a useful pattern beyond games: keep the system that can make broad,
repeatable changes authoritative; store human taste as a narrow overlay. The machine keeps the
map. The person gets a pencil, not a competing map department.

## Give the agents something they can actually see

Coding agents are very good at reading code and extremely willing to infer a picture from it.
The second ability should not be encouraged.

`MarbleCore` imports nothing Apple-specific. Physics, camera math, levels, modes, rides, and music
live in a portable Swift package with more than 250 tests. It builds on Linux through a tiny
compatibility layer for Apple's SIMD types. The renderer lives somewhere else. That split began
as ordinary architecture and became the reason an agent can verify almost the entire game
without booting an iPhone simulator and hoping the marble appears cheerful.

The repo also generates its own evidence:

- an elevation-shaded map of the mountain;
- an interactive browser level viewer with top-down and isometric projections;
- camera and ride profiles as SVG and CSV;
- a gallery rendered from every real block mesh;
- deterministic game screenshots;
- and a `-demo` launch mode that drives the marble and camera with scripted input.

The simulator cannot inject the game's two simultaneous touches. Without the demo driver, an
automated screenshot proves only that a marble can sit very still. With it, the render agent can
compare two frames, crop the ninety-pixel sphere, and check whether its painted detail actually
reads as rolling instead of merely receiving a nice comment in the source code.

Some things remain stubbornly human. Touch latency, thumb occlusion, whether the camera makes you
slightly seasick in the funny way or deeply seasick in the refund way: those require the game on
an iPad and a person with a vestibular system. The automated loop ends where the body begins.

## What I would steal from this

Five agents is not a magic number. The soundtrack could be one job or twelve; the marble does not
care. The useful pieces are smaller:

1. **Give every specialist one owned layer.** "Visuals" is vague. "Materials and lighting, never
   geometry" can make a decision.
2. **Write the handoff into the prohibition.** If the rendering agent finds broken geometry, it
   names the geometry owner. It does not just stop and look concerned.
3. **Separate finding from fixing when the failure is slippery.** A critic that leaves a failing
   test gives the fixer a target and cannot grade its own homework back to green.
4. **Turn scars into instructions.** The critic sweeps edges because real bugs lived there. A
   generic best-practices paragraph would never have guessed the shoulder of a hipped ramp.
5. **Generate inspectable artifacts.** Maps, profiles, screenshots, and sampled meshes give an
   agent evidence. Source code gives it a story about evidence.
6. **Name the physical boundary.** The build can prove that the game runs. Only thumbs can prove
   that it plays.

The usual pitch for agent teams is additive: more expertise, more parallel work, more little
digital employees bustling around the org chart. MARBLE's version works mostly by subtraction.
Each agent knows exactly which tempting improvement belongs to somebody else. The critic cannot
fix. The painter cannot pave. The composer cannot move the bridge. The level designer cannot
whittle a bespoke block behind the kit's back.

The game is allowed to become skeeball without warning. The people building the ramp are not.
