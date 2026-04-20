# seqan3-3081 — Empty SAM/BAM output files invalid (no header written); file unusable unless records explicitly written.

**SUT**: seqan3
**Format**: SAM
**Severity**: logic bug
**Anchor**: commit_sha `fa221c1302cfe515211ea70de375a1802826d3d9` → `c84f5671665478ec1b71535201cbffbe1fdd8c82`
**Confidence**: high
**Issue / PR**: https://github.com/seqan/seqan3/pull/3081

## What the bug does

Empty SAM/BAM output files invalid (no header written); file unusable unless records explicitly written.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
