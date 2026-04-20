# noodles-ob1-0.23 — Genotype parser silently dropped sample values after the last FORMAT key; header without trailing newline triggered an infinite loop.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.23` → `0.24`
**Confidence**: medium
**Issue / PR**: https://github.com/zaeleus/noodles/blob/master/noodles-vcf/CHANGELOG.md

## What the bug does

Genotype parser silently dropped sample values after the last FORMAT key; header without trailing newline triggered an infinite loop.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
