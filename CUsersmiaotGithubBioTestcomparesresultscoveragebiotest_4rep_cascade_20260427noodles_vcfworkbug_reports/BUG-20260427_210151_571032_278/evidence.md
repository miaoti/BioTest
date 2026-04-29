# Evidence Report: trim_common_affixes_invariance
**MR ID**: `4af3f36f15b2`
**Scope**: VCF.record
**Oracle**: After trimming shared prefix/suffix bases between REF and ALT and adjusting POS accordingly, the variant must be recognized as equivalent to the original by a spec-compliant parser. The canonical normalized representation (parsimonious, left-anchored) must produce identical variant semantics.

## Transform Steps
- `trim_common_affixes`

## Preconditions
- alt_count==1
- len(REF)>=2 OR len(ALT)>=2
- REF[0]==ALT[0] OR REF[-1]==ALT[-1]

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

- The VCF v4.5 spec does not explicitly define normalization rules for trimming common affixes; this MR is based on the Tan, Abecasis, Kang (2015) canonical representation paper rather than a direct VCF spec requirement