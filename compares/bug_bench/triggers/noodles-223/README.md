# noodles-223 — lazy::Record::info_range returned the FILTER byte range instead of INFO; callers reading INFO saw FILTER bytes.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.48` → `0.49`
**Confidence**: high
**Issue / PR**: https://github.com/zaeleus/noodles/pull/223

## What the bug does

lazy::Record::info_range returned the FILTER byte range instead of INFO; callers reading INFO saw FILTER bytes.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
