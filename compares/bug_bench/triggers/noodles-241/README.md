# noodles-241 — VCF 4.

**SUT**: noodles
**Format**: VCF
**Severity**: crash / incorrect rejection
**Anchor**: cargo_version `0.58` → `0.59`
**Confidence**: high
**Issue / PR**: https://github.com/zaeleus/noodles/issues/241

## What the bug does

VCF 4.2 header with raw value starting with '<' but no ID= (e.g., ##ID=<Description="...">) raised MissingId parse error.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `uncaught_exception`
- **Compared against**: noodles
