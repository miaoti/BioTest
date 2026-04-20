# vcfpy-nocall-0.8 — No-call GT (.

**SUT**: vcfpy
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `0.8.1` → `0.9.0`
**Confidence**: low
**Issue / PR**: https://github.com/bihealth/vcfpy/blob/main/CHANGELOG.md

## What the bug does

No-call GT (./.) parsed incorrectly in very early vcfpy. Install-rot risk on 0.8.1 under modern Python.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
