# noodles-268 — IUPAC ambiguity codes in REF caused writer to emit corrupted / truncated lines (e.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.57` → `0.58`
**Confidence**: high
**Issue / PR**: https://github.com/zaeleus/noodles/issues/268

## What the bug does

IUPAC ambiguity codes in REF caused writer to emit corrupted / truncated lines (e.g. two records merged).

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
