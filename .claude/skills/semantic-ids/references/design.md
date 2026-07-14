# Why the semantic IDs are built this way

Background for anyone about to change the bit layout, the encoder, or the embedding
model. Every number here was measured, not assumed. The experiment harness that produced
them lives at `~/Documents/dev/embeddings` (`npm run experiments` → `results/*.md`).

## The whole idea in one paragraph

An embedding is a piece of meaning turned into a list of numbers, arranged so that
"close in the list" means "close in meaning." `nomic-embed-text` turns a page into 768
floats. Keep only the **sign** of each number — one bit per dimension — and you get a
compact code where **Hamming distance approximates semantic distance**. That's binary
quantization. It sounds like it should destroy the signal and it mostly doesn't: nearly
all the meaning turns out to live in _which side of zero_ each dimension landed on, not
in the magnitudes. The vector is closer to a 172-question yes/no personality quiz than
to a precise coordinate.

## Mean-centering is not optional

Raw embedding dimensions are **not zero-centered**. Some are positive for essentially
every input in the corpus. Take a naive `sign(v)` and those become **dead bits** —
identical on every page, carrying exactly zero information. You'd think you had 172 bits
of address space and actually have fewer.

Measured on the test corpus:

|                        | dead bits   | avg skew from a 50/50 split | effective bits (entropy) |
| ---------------------- | ----------- | --------------------------- | ------------------------ |
| naive `sign(v)`        | 9 / 108     | 27.1%                       | 66.6                     |
| `sign(v - corpusMean)` | **0 / 108** | **4.3%**                    | **102.1**                |

One subtraction recovered ~35 bits of real capacity. This is why `data/semantic-model.json`
exists and why it must never be recomputed: the mean is the **shared origin** every ID is
measured against. Change the origin and every previously-issued ID is measured from
somewhere else.

## The trap: hex prefix as a semantic bucket

The seductive idea is `WHERE semantic_id LIKE 'a3f%'` — treat the leading characters as
a coarse topic bucket, so sorting by ID sorts by meaning and a b-tree scan becomes a
topic scan.

**It does not work.** Hamming distance and numeric distance are different animals:
`0111` and `1000` differ by 1 as integers and by 4 bits in Hamming. One flipped high bit
throws a page to the far end of the sort order while leaving it _semantically adjacent_.
Sorting a binary code gives you locality within a branch and a cliff at every boundary.
In the test corpus, the two closest pages in the entire set (`"The cat sat on the mat"`
and `"A feline rested upon the rug"`) sorted to opposite ends.

The real fix for prefix lookup is **LSH banding** (chop the code into b bands of r bits,
index each, shortlist anything matching on any one band). It was built and measured, and
on a corpus this size it buys ~3× speed at real recall cost, over a scan that already
does a million rows in 5 ms. **It is not worth it here.** Brute force.

## Encoder choice: this site uses the simplest one, deliberately

Which 172 of the 768 dimensions do you keep, and how? Four options were benchmarked at a
fixed bit budget:

| encoder  | recall@5 | what each bit sees                              |
| -------- | -------- | ----------------------------------------------- |
| **itq**  | **47%**  | all 768 dims, via a _rotated_ max-variance axis |
| truncate | 32%      | one raw dimension (the first N)                 |
| variance | 29%      | one raw dimension (the ones that move most)     |
| simhash  | 23%      | all 768 dims, via a random hyperplane           |
| pca      | 19%      | all 768 dims, via a max-variance axis           |

**ITQ wins by a mile, and this site uses `truncate` anyway.** Two reasons, and both are
about this being a _blog_ rather than a search index:

1. **ITQ can't train here.** It needs PCA, and PCA can extract at most `n-1` real
   components. With 84 pages, asking for 172 components means most of them are fitting
   noise by construction. You'd need a corpus several times the bit budget.
2. **ITQ drags a chain.** It requires persisting a 172×768 component matrix and a
   172×172 rotation — megabytes of state — _forever_, beside every ID it ever minted.
   Lose it and the IDs are unreadable. Retrain it on a grown corpus (and this corpus
   grows every time Eric publishes) and every committed ID is silently wrong.

`truncate` needs nothing but a frozen 768-float mean. For IDs that live in **git**, on a
corpus that **grows**, that stability is worth more than the recall. This is the whole
reason the design looks less clever than it could be.

Two findings worth carrying, both counterintuitive:

- **SimHash lost.** Random hyperplanes give an _unbiased_ estimator of cosine distance
  (a real theorem: a random hyperplane separates two vectors with probability exactly
  θ/π). But unbiased ≠ accurate — it's a _high-variance_ estimator needing far more bits
  before the averaging converges. `nomic-embed-text` is Matryoshka-trained, so its
  leading dimensions genuinely carry the most signal, and biased-but-lucky truncation
  beats unbiased-but-noisy at small bit budgets.
- **Plain PCA + sign is actively broken.** PCA's top axis carries ~15× the variance of
  its bottom axis — and then `sign()` flattens them all to one bit each, so Hamming
  gives a noise-tier component the same vote as the one holding the whole corpus. ITQ's
  entire contribution is a learned rotation that spreads the variance evenly first
  (measured: 15× → 1.6×), which is why it rescues PCA from 19% to 47% on an _identical_
  subspace.

## Why 192 bits / base64url and not 128 / hex

Hex spends **4 bits per character** — one nibble — and discards the other half of every
character's capacity. Base64 spends **6**. At the same 32-character width:

| encoding      | chars  | total bits | semantic bits | recall@5 (this corpus) |
| ------------- | ------ | ---------- | ------------- | ---------------------- |
| hex           | 32     | 128        | 108           | 51%                    |
| **base64url** | **32** | **192**    | **172**       | **54%**                |

The sizes land exactly: 192 bits = 24 bytes, and base64 packs 3 bytes into 4 characters,
so 24 bytes is _precisely_ 32 characters with no padding.

64 symbols rather than 62 (plain alphanumerics) because 64 is a power of two — encoding
is then pure bit-shifting rather than bignum long division, and you gain 2 bits.
base64**url**'s `-` and `_` (rather than base64's `+` and `/`) keep the IDs safe in URLs
and filenames.

## It's a filter, not a ranker

172 bits is a **coarse** instrument. On the test corpus, true paraphrases land ~36 bits
apart out of 108 while unrelated junk lands at ~54 — which is _exactly what pure chance
produces_. The entire usable signal lives in a narrow band, and the binary code is an
excellent candidate-generator and a mediocre ranker.

The correct architecture is two-stage: **sweep** with the IDs (cheap, coarse, its only
job is to not _lose_ the right answer), then **rescore** the survivors with the
full-precision float vectors (expensive, precise, and it only ever touches the
shortlist). Measured: a shortlist plus float rescoring recovers **100% of the exact
answer** a full exhaustive float scan would give, while loading the float vectors of a
tiny fraction of the corpus.

This site does **not** currently do the rescore stage, because with 84 pages the coarse
answer is good enough and there's nowhere to put the float vectors on a static site. If
related-posts quality ever disappoints, that's the lever: keep the floats around at mint
time and rescore there, before writing `related_by_meaning` into frontmatter. The visitor
never sees any of it.

## Things that would invalidate every ID on the site

- Recomputing or deleting `data/semantic-model.json` (the frozen mean).
- Changing `EMBED_MODEL` away from `nomic-embed-text`.
- Changing `SEMANTIC_BITS`, `DAY_BITS`, `HASH_BITS`, or `EPOCH`.
- Changing what text gets embedded (currently `title + summary + tags`).

Any of these is a **re-mint** (`--force`), not a migration. There is no migration. IDs
minted under different settings are not comparable to each other, and nothing will tell
you — the distances will still be numbers, they'll just be meaningless.
