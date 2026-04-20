# noodles-inforay-0.64 — array::values iterator mis-counted entries and didn't terminate on empty lists; wrong length / infinite loop for INFO/FORMAT arrays.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.63` → `0.64`
**Confidence**: medium
**Issue / PR**: https://github.com/zaeleus/noodles/blob/master/noodles-vcf/CHANGELOG.md

## What the bug does

array::values iterator mis-counted entries and didn't terminate on empty lists; wrong length / infinite loop for INFO/FORMAT arrays.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
