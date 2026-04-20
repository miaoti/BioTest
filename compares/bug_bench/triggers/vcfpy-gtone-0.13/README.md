# vcfpy-gtone-0.13 — Haploid / partial-haploid GT describing only one allele parsed incorrectly.

**SUT**: vcfpy
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `0.12.1` → `0.12.2`
**Confidence**: medium
**Issue / PR**: https://github.com/bihealth/vcfpy/blob/main/CHANGELOG.md

## What the bug does

Haploid / partial-haploid GT describing only one allele parsed incorrectly.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
