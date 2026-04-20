# noodles-259 — Writer emitted multiple '##'-prefixed header records without separator newlines, producing a malformed header.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.55` → `0.56`
**Confidence**: high
**Issue / PR**: https://github.com/zaeleus/noodles/issues/259

## What the bug does

Writer emitted multiple '##'-prefixed header records without separator newlines, producing a malformed header.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
