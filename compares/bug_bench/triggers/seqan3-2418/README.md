# seqan3-2418 — BAM parsing forgets to consume sequence bytes when creating dummy alignments; stream iterator misaligned, corrupts subsequent record reads.

**SUT**: seqan3
**Format**: SAM
**Severity**: logic bug
**Anchor**: commit_sha `df9fd5ff64f59fdb124c4a564a4141d1f9cff22b` → `8e374d7ce7a1ce4de0077bc3698d5ae2c8e79600`
**Confidence**: high
**Issue / PR**: https://github.com/seqan/seqan3/pull/2418

## What the bug does

BAM parsing forgets to consume sequence bytes when creating dummy alignments; stream iterator misaligned, corrupts subsequent record reads.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, pysam
