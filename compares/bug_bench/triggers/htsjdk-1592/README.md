# htsjdk-1592 — CRAM 'SC' scores misdecoded during normalization

**Severity**: logic bug (silent quality-score corruption).
**Format**: CRAM (binary).
**Anchor**: pre_fix = htsjdk 2.24.1, post_fix = htsjdk 3.0.0.
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1592

## What the bug does

The CRAM `SC` (scores) data series carries quality values as a
delta-from-reference stream. htsjdk 2.x's normalization pass
(applied after per-block decoding, before handing records to the
caller) misapplies the delta direction for records where the
scores-quality block is empty. The resulting `BAQ` / `QUAL` fields
on the decoded SAMRecord show quality values that are off by a
constant offset — the data isn't lost, it's just shifted, so it
looks plausible but doesn't match what htslib produces.

## Trigger

Same shape as htsjdk-1590 — binary CRAM with the SC block populated
and at least one read whose per-base quality array is empty. Plain
SAM has no SC encoding; must round-trip through `samtools view -C`
with a reference to generate.

Use either:

1. hts-specs CRAM compliance fixtures that exercise SC.
2. `samtools view -T ref.fa --output-fmt-option store_md=1 -C -o out.cram in.sam`
   on a SAM whose records have QUAL=`*` (missing quality) interleaved
   with records that have real quality arrays. The CRAM encoder uses
   SC + an empty-quality delta for the `*` rows.

PR #1592's regression test uses a test resource; grab it from
`test/resources/htsjdk/samtools/cram/hts-specs/` in htsjdk's tree at
the fix commit.

## Detection criterion

- **Expected signal**: `differential_disagreement` on the QUAL column.
  Parse the CRAM with pre-fix htsjdk 2.24.1 vs htslib; the QUAL
  arrays differ by a systematic offset on SC-encoded reads.
