# seqan3-3269 — Banded alignment returns relative positions of sliced sequences instead of absolute positions of originals; off-by-prefix offset.

**SUT**: seqan3
**Format**: SAM
**Severity**: logic bug
**Anchor**: commit_sha `ca4d668390e35b4045ccd02d070927f8178ed2ce` → `11564cb3bcea39666d6d3979080bc5d8fdbe1d7e`
**Confidence**: high
**Issue / PR**: https://github.com/seqan/seqan3/pull/3269

## What the bug does

Banded alignment returns relative positions of sliced sequences instead of absolute positions of originals; off-by-prefix offset.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
