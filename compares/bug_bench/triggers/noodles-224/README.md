# noodles-224 — Lazy reader read past end-of-record into next line when optional trailing fields were missing, corrupting the buffer.

**SUT**: noodles
**Format**: VCF
**Severity**: logic bug
**Anchor**: cargo_version `0.48` → `0.49`
**Confidence**: high
**Issue / PR**: https://github.com/zaeleus/noodles/pull/224

## What the bug does

Lazy reader read past end-of-record into next line when optional trailing fields were missing, corrupting the buffer.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, htsjdk
