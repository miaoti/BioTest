# Evidence Report: BCF header dictionary permutation preserves query method results after BCF round-trip
**MR ID**: `4e6946a02a58`
**Scope**: VCF.header
**Oracle**: After permuting the order of ##contig/##INFO/##FORMAT/##FILTER header dictionary entries and round-tripping through BCF, all public query methods on parsed records must return identical values. Per VCF v4.5 §6.2.1, dictionary orderings are implementation-defined; a spec-compliant parser must produce identical results regardless of dictionary entry order. The BCF2 spec requires fully specified contig definitions (p1296) and fully typed INFO/GENOTYPE fields (p1297), ensuring the round-trip is lossless.

## Transform Steps
- `permute_bcf_header_dictionary`
- `vcf_bcf_round_trip`

## Preconditions
- bcf_codec_available
- pysam_runtime_reachable
- header_has_multiple_info_or_format_entries

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1296`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — BCF specification] * All BCF2 files must have fully specified contigs definitions.
  No record may refer to a contig not present in the header itself.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1297`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — BCF specification] * All INFO and GENOTYPE fields must be fully typed in the BCF2 header to enable type-specific encoding of the fields in records.
  An error must be thrown when converting a VCF to BCF2 when an unknown or not fully specified field is encountered in the records.

### Evidence 3
- **Chunk ID**: `VCFv4.5.tex::Meta-information lines::p122`
- **Section**: Meta-information lines
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — Meta-information lines] Meta-information lines are optional, but if they are present then they must be completely well-formed.
Other than |##fileformat|, they may appear in any order.
Note that BCF, the binary counterpart of VCF, requires that all entries are present.
