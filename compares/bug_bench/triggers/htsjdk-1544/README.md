# htsjdk-1544 — Pre-fix VariantContext.

**SUT**: htsjdk
**Format**: VCF
**Severity**: logic bug
**Anchor**: install_version `2.24.1` → `3.0.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1544

## What the bug does

Pre-fix VariantContext.getType() mis-classifies gVCF-style <NON_REF> records, producing wrong variant-type labels for gVCF blocks. Downstream tools that filter by variant type therefore miss entire classes of records.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib, pysam
