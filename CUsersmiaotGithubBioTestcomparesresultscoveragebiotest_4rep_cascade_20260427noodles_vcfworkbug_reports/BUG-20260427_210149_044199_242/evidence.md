# Evidence Report: ALT allele permutation with consistent remapping of GT, Number=A, and Number=R fields
**MR ID**: `2af5800ea12a`
**Scope**: VCF.record
**Oracle**: After permuting ALT alleles and consistently remapping GT indices (0=REF unchanged) and reordering Number=A and Number=R INFO/FORMAT values to match the new ALT order, the resulting VCF record must be semantically equivalent to the original. Any parser that re-serializes the record must produce the same set of variant calls.

## Transform Steps
- `choose_permutation`
- `permute_ALT`
- `remap_GT`
- `permute_Number_A_R_fields`

## Preconditions
- alt_count >= 2
- format_has_gt OR header_has_info_number_a OR header_has_info_number_r OR header_has_format_number_a OR header_has_format_number_r

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::The VCF specification::p16`
- **Section**: The VCF specification
- **Severity**: CRITICAL
- **Quote**:
  > A: The field has one value per alternate allele. The values must be in the same order as listed in the ALT column (described in section data-lines). R: The field has one value for each possible allele, including the reference. The order of the values must be the reference allele first, then the alternate alleles as listed in the ALT column.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::Information field format::p158`
- **Section**: Information field format
- **Severity**: CRITICAL
- **Quote**:
  > R: The field has one value for each possible allele, including the reference. The order of the values must be the reference allele first, then the alternate alleles as listed in the ALT column.

### Evidence 3
- **Chunk ID**: `VCFv4.5.tex::Data lines::p226`
- **Section**: Data lines
- **Severity**: INFORMATIONAL
- **Quote**:
  > AC		    A		    Integer	    Allele count in genotypes, for each ALT allele, in the same order as listed

### Evidence 4
- **Chunk ID**: `VCFv4.5.tex::Data lines::p230`
- **Section**: Data lines
- **Severity**: INFORMATIONAL
- **Quote**:
  > AF		    A		    Float		    Allele frequency for each ALT allele in the same order as listed (estimated from primary data, not called genotypes)
