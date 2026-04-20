# htsjdk-1364 — Pre-fix VCF codec rejects QUAL / INFO float values spelled with non-lowercase 'nan' or 'inf' (e.

**SUT**: htsjdk
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `2.19.0` → `2.20.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1364

## What the bug does

Pre-fix VCF codec rejects QUAL / INFO float values spelled with non-lowercase 'nan' or 'inf' (e.g. 'NaN', 'Inf', 'Infinity'), which htslib accepts per the VCF spec's float production rule. Causes differential disagreement on any VCF where upstream tools emit mixed-case float literals.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, pysam
