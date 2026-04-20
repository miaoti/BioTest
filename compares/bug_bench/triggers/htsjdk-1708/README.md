# htsjdk-1708 — CRAM multi-container reference-region corruption

**Severity**: logic bug (silent data corruption).
**Format**: CRAM (binary).
**Anchor**: pre_fix = htsjdk 4.1.0, post_fix = htsjdk 4.1.1.
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1708

## What the bug does

CRAM 3.0.0 and later caches the full-sequence reference region fetch
between containers. When the reader transitions across containers that
all start at reference position 1 (common for alignments mapped to the
beginning of a contig), the cached region is not invalidated correctly.
The SerialState transition logic then reads a stale reference region
and the decoded bases are silently corrupt. Nothing crashes, nothing
logs — the reader returns wrong sequences.

## Trigger

The PR's test case (`CRAMReferenceRegionTest.testSerialStateTransitions`)
builds a CRAM file with **three containers of reads all at position 1**
by replicating a single read ~20 000 times. That's the minimum number
needed to straddle CRAM's 10 000-read-per-container default.

Because CRAM is binary and requires a reference FASTA + header, the
harness can't easily construct one from scratch. The PR ships
`mitoAlignmentStartTest_3_containers_aligned_to_pos_1.cram` (~1.1 MB)
under `test/resources/htsjdk/samtools/cram/`. For the bench run, the
driver should either:

1. Clone htsjdk at a recent tag, grab that test resource, and use it
   as the trigger (preferred; same file the PR's regression test uses).
2. Synthesise a CRAM via `samtools view -T <ref.fa> -o out.cram` from
   a large SAM repeating one read ~20 000 times.

See `synthesise_trigger.sh` for the synthesis path.

## Detection criterion

- **Expected signal**: `differential_disagreement` against `htslib`.
  Parse the CRAM with htsjdk 4.1.0 AND with `samtools view` — the two
  should produce the same SAM text on a fixed reference, but the
  buggy htsjdk drops/corrupts bases for reads in containers 2 and 3.
- **Fuzzer alternate**: any coverage-guided fuzzer that reaches
  `CRAMReferenceRegion.getSequenceAt()` with enough read volume will
  eventually flip a SAN sanitizer or a content assertion.
