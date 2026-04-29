# Evidence Report: Shuffle meta lines then BCF round-trip preserves query method results
**MR ID**: `44202522df4e`
**Scope**: VCF.header
**Oracle**: After shuffling ##meta-information lines (keeping ##fileformat first) and round-tripping through BCF, all public query methods on parsed records must return identical values. Per VCF v4.5, meta-information lines other than ##fileformat may appear in any order (p122). BCF2 is a binary equivalent of VCF (p1292), so the round-trip must be lossless regardless of meta-line ordering.

## Transform Steps
- `shuffle_meta_lines`
- `vcf_bcf_round_trip`

## Preconditions
- bcf_codec_available
- pysam_runtime_reachable

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::Meta-information lines::p122`
- **Section**: Meta-information lines
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — Meta-information lines] Meta-information lines are optional, but if they are present then they must be completely well-formed.
Other than |##fileformat|, they may appear in any order.
Note that BCF, the binary counterpart of VCF, requires that all entries are present.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1292`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — BCF specification] Overall, the idea behind is BCF2 is simple.
BCF2 is a binary, compressed equivalent of VCF that can be indexed with tabix and can be efficiently decoded from disk or streams.
