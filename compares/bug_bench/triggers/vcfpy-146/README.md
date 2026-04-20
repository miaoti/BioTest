# vcfpy-146 — INFO flag present but header declares it as String type; raises TypeError: argument of type 'bool' is not iterable.

**SUT**: vcfpy
**Format**: VCF
**Severity**: crash / incorrect rejection
**Anchor**: install_version `0.13.3` → `0.13.4`
**Confidence**: high
**Issue / PR**: https://github.com/bihealth/vcfpy/issues/146

## What the bug does

INFO flag present but header declares it as String type; raises TypeError: argument of type 'bool' is not iterable.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `uncaught_exception`
- **Compared against**: vcfpy
