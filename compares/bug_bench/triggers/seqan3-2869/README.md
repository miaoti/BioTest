# seqan3-2869 — FASTA parser fails on IDs containing '>' character; treats '> >MyID' as ID 'MyID' instead of '>MyID'.

**SUT**: seqan3
**Format**: SAM
**Severity**: logic bug
**Anchor**: commit_sha `edbfa956f^` → `edbfa956f`
**Confidence**: high
**Issue / PR**: https://github.com/seqan/seqan3/pull/2869

## What the bug does

FASTA parser fails on IDs containing '>' character; treats '> >MyID' as ID 'MyID' instead of '>MyID'.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
