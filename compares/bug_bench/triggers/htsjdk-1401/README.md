# htsjdk-1401 — Pre-fix VCF header parser produces inconsistent PEDIGREE entries between VCF 4.

**SUT**: htsjdk
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `2.19.0` → `2.20.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1401

## What the bug does

Pre-fix VCF header parser produces inconsistent PEDIGREE entries between VCF 4.2 and 4.3 inputs; the same semantic pedigree record round-trips differently depending on declared fileformat version.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
