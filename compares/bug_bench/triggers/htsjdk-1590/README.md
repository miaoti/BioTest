# htsjdk-1590 — CRAM 'BB' read features silently drop bases

**Severity**: logic bug (silent data loss).
**Format**: CRAM (binary).
**Anchor**: pre_fix = htsjdk 2.24.1, post_fix = htsjdk 3.0.0.
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1590 (parent issue #1379)

## What the bug does

CRAM encodes streaks of bases using a `BB` data series. htsjdk 2.x's
CRAM reader reconstructs a read's sequence by iterating read features
(SC, BB, BF, etc.) and appending decoded bases to the output. The BB
branch of `ReadFeatureDecoder` under 2.x fails to forward the decoded
bases into the accumulator — they are read off the stream correctly
but never placed into the returned sequence. The result: any read
whose CRAM encoding includes a BB feature returns a sequence shorter
than its CIGAR would imply, with the BB-encoded bases silently
missing.

The bug was caught by the hts-specs compliance test suite (#1587)
which cross-validates htsjdk against htslib on spec-provided CRAM
fixtures.

## Trigger

CRAM's BB feature is only emitted by an encoder when contiguous
matching bases appear in a pattern the reference-based delta encoder
determines is worth packing as a "bases-as-string" run rather than
a delta-from-reference sequence. Minimal reproducers in plain text
aren't possible — the trigger is a binary CRAM with the BB feature
populated.

The harness reproduces this by:

1. Grabbing one of the hts-specs compliance CRAM fixtures (preferred)
   from `https://github.com/samtools/hts-specs/tree/master/test/cram`.
2. Or constructing one with `samtools view -T ref.fa -C --output-fmt-option no_ref out.cram in.sam` on a SAM with long soft-clipped runs that the encoder packs as BB.

For the bench run, use the test CRAM that PR #1590 ships as a
regression fixture:
`test/resources/htsjdk/samtools/cram/hts-specs/cram_3.0/<BB-feature.cram>`.
(Path approximate; check the PR's exact file layout.)

## Detection criterion

- **Expected signal**: `differential_disagreement` against `htslib`
  and `pysam`. On the pre-fix SUT the returned sequence will be
  strictly shorter than on htslib / pysam / post-fix htsjdk — the
  dropped bases show up as a length mismatch.
