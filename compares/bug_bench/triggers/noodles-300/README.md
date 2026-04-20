# noodles-300 — Writing an INFO String containing ';' produced unreadable VCF; round-trip broke.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.63` → `0.64`
**Confidence**: high
**Issue / PR**: https://github.com/zaeleus/noodles/issues/300

## What the bug does

Writing an INFO String containing ';' produced unreadable VCF; round-trip broke. Fix: percent-decoding of string/char values.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
