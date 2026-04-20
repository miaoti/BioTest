# vcfpy-176 — Sample GT value '0|0' with GT undeclared in header causes a list artefact to leak into _genotype_updated, raising ValueError: invalid literal for int() with base 10: "['0".

**SUT**: vcfpy
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `0.13.8` → `0.14.0`
**Confidence**: high
**Issue / PR**: https://github.com/bihealth/vcfpy/issues/176

## What the bug does

Sample GT value '0|0' with GT undeclared in header causes a list artefact to leak into _genotype_updated, raising ValueError: invalid literal for int() with base 10: "['0".

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `uncaught_exception`
- **Compared against**: vcfpy
