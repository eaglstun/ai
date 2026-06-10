+++
title = "RSS sampler"
summary = "A lightweight monitor that polls a process's Resident Set Size on a timer to chart its real-RAM footprint over time - so you see the memory cliff coming instead of OOM-ing into it."
category = "Local inference & formats"
related = ["parameters", "gguf", "ggml", "precision"]
plain = "The bathtub gauge. A single 'it overflowed' tells you nothing useful; a number ticking up every few seconds tells you whether the water's creeping or gushing - so you can cut the tap before it hits the rim instead of mopping the floor after. The 'self-monitoring' part is just the tub watching its own water line."
+++
An **RSS sampler** is a small monitor that wakes up on a timer, reads a process's **RSS**
(Resident Set Size, the slice of its memory actually resident in physical RAM, as opposed to
swapped out to disk or merely reserved on paper), and logs the number. String those readings
together and you get a memory _trajectory_: a curve of real footprint over time instead of a
single after-the-fact figure. "Self-monitoring" just means the process samples _itself_: it
spins up a little background thread that watches its own RSS while the real work runs, so you
don't need an external `top`/`ps` babysitter racing to catch the peak before it vanishes.

The reason you reach for one is the OOM cliff. A long job, say, chewing through a 730-second
audio file, can sail along for minutes and then get killed outright by the operating system
the instant its footprint crosses what the machine physically has. A lone "peak memory" number
tells you _that_ it died, not _when_ or _how fast it was climbing_. The trajectory tells you
the shape: flat and safe, a slow creep with room to spare, or a leak that ramps until it walks
off the edge. That's the difference between "fp16 halves the footprint, so the small model
should survive the file that killed the fp32 run" being a hope and being a measurement.

It pairs naturally with the memory levers on the model side. The footprint RSS measures is
driven mostly by a model's [parameters](/glossary/parameters/) and the numeric precision they're stored at, which
is exactly what quantized formats like [GGUF](/glossary/gguf/) and the engines that load them ([GGML](/glossary/ggml/)) exist
to shrink. An RSS sampler is how you check whether that shrink actually bought enough headroom
on _this_ machine, for _this_ workload, instead of trusting the arithmetic and finding out at
second 730.
