# htsjdk-1538 — Pre-fix SAMRecord mutation (e.

**SUT**: htsjdk
**Format**: SAM
**Severity**: logic bug
**Anchor**: install_version `2.24.0` → `2.24.1`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1538

## What the bug does

Pre-fix SAMRecord mutation (e.g. setCigar) does not invalidate the cached mAlignmentBlocks vector. Subsequent calls to getAlignmentBlocks() on the mutated record return stale data from before the CIGAR edit. Silent wrong answer on any mutation-followed-by-query pattern.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
- **Also detectable via**: metamorphic_set_cigar_then_get_blocks
