# noodles-339 — Writer over-encoded ':' in INFO values and ';'/'=' in sample values, producing non-round-trippable output.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.81` → `0.82`
**Confidence**: high
**Issue / PR**: https://github.com/zaeleus/noodles/issues/339

## What the bug does

Writer over-encoded ':' in INFO values and ';'/'=' in sample values, producing non-round-trippable output.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
