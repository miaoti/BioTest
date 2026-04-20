# htsjdk-1372 — Pre-fix VCF codec fails to handle FORMAT=GL when multiple per-genotype GL values are each individually missing ('.

**SUT**: htsjdk
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `2.19.0` → `2.20.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1372

## What the bug does

Pre-fix VCF codec fails to handle FORMAT=GL when multiple per-genotype GL values are each individually missing ('.'). Throws instead of producing null, even though htslib accepts the input.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
