# htsjdk-1418 — Pre-fix VCF header parser throws on any '##contig=<ID=X>' header line that omits the length= attribute, even though the spec treats length as optional.

**SUT**: htsjdk
**Format**: VCF
**Severity**: crash / incorrect rejection
**Anchor**: install_version `2.20.1` → `2.21.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1418

## What the bug does

Pre-fix VCF header parser throws on any '##contig=<ID=X>' header line that omits the length= attribute, even though the spec treats length as optional. htslib accepts such files; pre-fix htsjdk rejects them.

## Trigger

See sibling files in this folder (if present):

- `original.vcf` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `uncaught_exception`
- **Compared against**: htsjdk_buggy_version
