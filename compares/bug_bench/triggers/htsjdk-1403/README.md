# htsjdk-1403 — Regression in VariantContextBuilder introduced in htsjdk 2.

**SUT**: htsjdk
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `2.20.0` → `2.20.1`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1403

## What the bug does

Regression in VariantContextBuilder introduced in htsjdk 2.20.0 — the builder emits incorrect field values under certain chains; hotfix in 2.20.1 reverts the regression.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
