# vcfpy-127 — Incomplete trailing FORMAT fields (e.

**SUT**: vcfpy
**Format**: VCF
**Severity**: crash / incorrect rejection
**Anchor**: install_version `0.11.0` → `0.11.1`
**Confidence**: medium
**Issue / PR**: https://github.com/bihealth/vcfpy/issues/127

## What the bug does

Incomplete trailing FORMAT fields (e.g. GATK 3.8 truncated output) raises KeyError: 'GQ'.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `uncaught_exception`
- **Compared against**: vcfpy
