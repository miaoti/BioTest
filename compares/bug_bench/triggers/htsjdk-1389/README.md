# htsjdk-1389 — Pre-fix VCF writer serialises multi-value missing fields as '.

**SUT**: htsjdk
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `2.19.0` → `2.20.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1389

## What the bug does

Pre-fix VCF writer serialises multi-value missing fields as '.,.,.' (one dot per value) instead of the spec-canonical single '.' for fully-missing values. Round-trip through pre-fix htsjdk changes INFO/FORMAT string representation.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
