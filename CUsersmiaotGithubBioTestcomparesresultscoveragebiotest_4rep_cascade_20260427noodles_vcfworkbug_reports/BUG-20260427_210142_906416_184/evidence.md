# Evidence Report: VCF-BCF round-trip preserves semantics
**MR ID**: `6320bd43d214`
**Scope**: VCF.record
**Oracle**: After round-tripping VCF through BCF2 encoding and back to VCF, the SUT must produce identical canonical output. Per VCF v4.5 §6, BCF is the binary counterpart of VCF and the round-trip should be semantically lossless.

## Transform Steps
- `vcf_bcf_round_trip`

## Preconditions
- bcf_codec_available
- pysam_runtime_reachable

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1304`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > Defined this way, the dictionary of strings depends on the order and the presence of all preceding header lines.

## Ambiguity Flags

- Precision of Float values, handling of missing values, and string encoding may differ between text and binary representations.