# htsjdk-1561 — Pre-fix SAM header parser silently accepts @HD / @SQ / @RG / @PG lines with tag keys longer or shorter than 2 characters (SAM spec §1.

**SUT**: htsjdk
**Format**: SAM
**Severity**: logic bug
**Anchor**: install_version `2.24.1` → `3.0.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1561

## What the bug does

Pre-fix SAM header parser silently accepts @HD / @SQ / @RG / @PG lines with tag keys longer or shorter than 2 characters (SAM spec §1.3 mandates exactly 2). Malformed headers pass through pre-fix and produce SAMFileHeader objects with garbage-keyed attributes.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
