# pysam-939 — Long-standing AlignmentFile bug in pysam <=0.

**SUT**: pysam
**Format**: SAM
**Severity**: logic bug
**Anchor**: install_version `0.21.0` → `0.22.0`
**Confidence**: medium
**Issue / PR**: https://github.com/pysam-developers/pysam/issues/939

## What the bug does

Long-standing AlignmentFile bug in pysam <=0.21; the 0.22.0 release bundled its fix together with #1214. Specific symptom deferred to trigger-folder research.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
