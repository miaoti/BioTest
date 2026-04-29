# Evidence Report: left_align_indel_invariance
**MR ID**: `5179a1122537`
**Scope**: VCF.record
**Oracle**: After left-shifting an indel in a homopolymer run by decrementing POS by 1 and preserving the first base of REF/ALT, the variant must be recognized as equivalent to the original by a spec-compliant parser per canonical normalization principles.

## Transform Steps
- `left_align_indel`

## Preconditions
- alt_count==1
- len(REF)!=len(ALT)
- REF[0]==REF[-1]
- pos>=2

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::The VCF specification::p63`
- **Section**: The VCF specification
- **Severity**: CRITICAL
- **Quote**:
  > Genotype fields
If genotype information is present, then the same types of data must be present for all samples.
First a FORMAT field is given specifying the data types and order (colon-separated FORMAT keys matching the regular expression \^[A-Za-z\_][0-9A-Za-z\_.]*\$, duplicate keys are not allowed).
This is followed by one data block per sample, with the colon-separated data corresponding to the types specified in the format.
The first key must always be the genotype (GT) if it is present.

## Ambiguity Flags

- The VCF v4.5 spec does not define left-alignment normalization rules; this MR is based on the Tan, Abecasis, Kang (2015) canonical representation paper rather than a direct VCF spec requirement