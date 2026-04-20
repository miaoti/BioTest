# vcfpy-145 — '.

**SUT**: vcfpy
**Format**: VCF
**Severity**: crash / incorrect rejection
**Anchor**: install_version `0.13.4` → `0.13.5`
**Confidence**: medium
**Issue / PR**: https://github.com/bihealth/vcfpy/issues/145

## What the bug does

'.bgz'-suffixed bgzipped VCF not recognized by reader; open fails.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `uncaught_exception`
- **Compared against**: vcfpy
