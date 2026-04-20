# pysam-1214 — Pre-fix AlignmentFile iteration over certain malformed-but-spec-tolerated SAM files produces records with incorrect per-record fields.

**SUT**: pysam
**Format**: SAM
**Severity**: logic bug
**Anchor**: install_version `0.21.0` → `0.22.0`
**Confidence**: medium
**Issue / PR**: https://github.com/pysam-developers/pysam/issues/1214

## What the bug does

Pre-fix AlignmentFile iteration over certain malformed-but-spec-tolerated SAM files produces records with incorrect per-record fields. Fixed together with #939 as part of a broader AlignmentFile robustness pass in 0.22.0.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
