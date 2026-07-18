+++
title = "Part 1 - The Cheat Code: Unified Memory"
slug = "unified-memory"
weight = 1
date = 2026-06-29
series = "ctranslate2-metal-backend"
description = "On Apple Silicon the CPU and GPU share one pool of RAM. That single fact turned a new GPU backend into an afternoon."
images = ["/og/ctranslate2-part-1.png"]
summary = "The one fact about Apple Silicon that turns 'add a whole new GPU backend' from a research project into an afternoon: the CPU and GPU share the same RAM, so a GPU buffer is also a CPU pointer - and CTranslate2's entire internal contract is built on pointers."
tags = ["apple-silicon", "metal", "tensor"]
semantic_id = "11N70iBulX70L6tMXl6yGgLllEO7sAs-"
related_by_meaning = ["/deep-dives/ctranslate2-metal-backend/06-profile-dont-guess/", "/deep-dives/ctranslate2-metal-backend/07-not-a-pull-request/", "/blog/three-hours-and-150-dollars/", "/practice/talkie-on-apple-silicon/"]
+++

Here's the fact the entire design hinges on. On Apple Silicon the CPU and GPU share the same
physical RAM. When you allocate a [Metal](/glossary/metal/) buffer with "shared" storage, you
get back a pointer that the **CPU can read and write directly** - and the GPU can use the same
buffer. There's no "copy the data over to the GPU" step, because there's no "over." It's all
one pool.

![A vintage big-letter postcard reading GREETINGS FROM UNIFIED MEMORY: a CPU and a GPU, each a grinning retro computer on a pool float, clinking drinks in the same motel swimming pool. There is no second pool.](greetings-from-unified-memory.jpg)

On an NVIDIA box this is not true. The GPU has its own separate memory across a bus, and half
of GPU programming is the bookkeeping of shuttling data back and forth and not doing it more
than you have to. CTranslate2's whole internal contract is built around that world: a
[tensor](/glossary/tensor/) is "a pointer plus a shape," and there's an allocator whose job is
to hand out memory the GPU can use.

Now watch what unified memory does to that contract.

CTranslate2 wants a pointer the GPU can use. A shared Metal buffer _is_ a pointer the GPU can
use - and the CPU too. So if I make the allocator hand out Metal buffers instead of plain CPU
memory, **every piece of existing CPU code in the engine suddenly works on GPU-resident data,
unchanged.** Not ported. Not rewritten. It just works, because the pointer it's holding happens
to live in memory the GPU can also see.

That's the cheat code. It means I didn't have to start by writing kernels. I had to start by
writing an allocator - and then I got a working (if slow) Metal engine _for free_, running the
existing CPU reference code over GPU memory. Correctness first, speed later, and the "free"
part is a gift from the hardware.

## The allocator is the whole trick

{{< bbros title="Peek & Poke" n="1" float="right" >}}
`MTLResourceStorageModeShared` is the whole spell. Allocate a buffer with it, PEEK the result with `[buffer contents]`, and you get an ordinary CPU pointer into the exact bytes the GPU reads. One allocation, two audiences, zero copies.
{{< /bbros >}}

The real work of Part 1 is one file, `src/metal/allocator.mm`. It specializes CTranslate2's
allocator for the new `Device::METAL`. Each allocation becomes an `MTLBuffer` with shared
storage; the allocator returns `[buffer contents]` - the CPU-addressable pointer into that
buffer - and that pointer satisfies the existing pointer-based contract with nothing else
changed. Host-to-device copies, which on CUDA are a whole `cudaMemcpy` ceremony, collapse into
a plain `memcpy`, because both sides are the same memory.

{{< bbros title="Field Note" n="2" float="left" >}}
Metal refuses a bare interior pointer. It wants the owning buffer plus a byte offset, the way a post office refuses "the third door down the hall" and demands a street address. The allocator's side table is the street directory.
{{< /bbros >}}

There's exactly one wrinkle, and it's the kind of thing that's invisible until it isn't.
CTranslate2 doesn't only hand around pointers to the _start_ of an allocation. It takes
sub-views into a tensor, and strided-batch GEMM hands the matrix-multiply routine pointers that
land in the _middle_ of a buffer. Metal, though, wants to bind the **buffer object**, plus a
byte offset - it can't take a raw interior pointer and work out which buffer you meant.

So the allocator keeps a side table: an address-ordered map of every allocation it's handed
out. When some op shows up later holding an interior pointer, a range lookup
(`buffer_and_offset`) walks that map, finds the allocation the pointer falls inside, and hands
back the owning `MTLBuffer` plus the offset. It's a small piece of bookkeeping that exists
entirely to translate between CTranslate2's "everything is a raw pointer" worldview and Metal's
"name me a buffer" worldview. (And it's manual retain/release, not ARC - the `.mm` files manage
their own Objective-C object lifetimes throughout, which becomes its own story later in this
series.)

## What "for free" actually buys you

The temptation, when you set out to add a GPU backend, is to think the deliverable is _kernels_:
the hand-written GPU programs that do the math fast. And eventually it is. But the cheat code
reframes the whole project. The first deliverable isn't speed; it's a correct engine that
happens to be slow, standing up on day one, with the entire existing test suite passing against
the new device.

That matters because it inverts the usual order of pain. The normal way to add a backend is to
write fifty kernels and then spend weeks finding out which three of them are subtly wrong. The
cheat code lets you stand up "correct but slow" first, then make it fast one piece at a time,
with a green test suite watching your back the whole way. You're never debugging "is it broken
because the math is wrong or because the plumbing is wrong" - the plumbing was proven correct
before any math moved to the GPU.

How you go from "correct but slow" to "fast, one op at a time" without ever breaking that green
test suite is the actual architecture of this thing - and it's [Part 2](/deep-dives/ctranslate2-metal-backend/the-staircase/).
