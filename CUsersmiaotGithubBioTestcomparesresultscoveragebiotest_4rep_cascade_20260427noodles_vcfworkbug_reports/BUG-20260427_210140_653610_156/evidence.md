# Evidence Report: BCF dictionary order invariance via VCF-BCF round-trip
**MR ID**: `9746c6e5c109`
**Scope**: VCF.header
**Oracle**: After shuffling ##contig, ##INFO, ##FORMAT, ##FILTER dictionary entries, round-tripping through BCF and back to VCF must produce identical canonical output. BCF codec re-indexes dictionary entries, so a spec-compliant parser must not depend on declaration order.

## Transform Steps
- `permute_bcf_header_dictionary`

## Preconditions
- bcf_codec_available
- pysam_runtime_reachable
- header_has_multiple_info_or_format_entries

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1304`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > Defined this way, the dictionary of strings depends on the order and the presence of all preceding header lines.

## Ambiguity Flags

- The BCF dictionary order is implementation-defined; parsers that use implicit positional indices without consulting the IDX field may produce divergent output.