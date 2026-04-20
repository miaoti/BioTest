# htsjdk-1489 — Pre-fix SAM locus accumulator drops certain insertion events, under-counting coverage at insert positions.

**SUT**: htsjdk
**Format**: SAM
**Severity**: logic bug
**Anchor**: install_version `2.22.0` → `2.23.0`
**Confidence**: medium
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1489

## What the bug does

Pre-fix SAM locus accumulator drops certain insertion events, under-counting coverage at insert positions. Downstream pileup statistics computed via htsjdk disagree with samtools mpileup at these sites.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
