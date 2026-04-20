# vcfpy-171 — Escaped '=' in INFO (e.

**SUT**: vcfpy
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `0.13.8` → `0.14.0`
**Confidence**: high
**Issue / PR**: https://github.com/bihealth/vcfpy/issues/171

## What the bug does

Escaped '=' in INFO (e.g., p.Lys%3D) is lost on re-write; comma is escaped but '=' is not, breaking round-trip.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
