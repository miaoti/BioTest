# Phase D End-to-End Run Report — 2026-04-17 01:31:06

## Executive Summary

- Iterations completed: **2**
- Total MRs enforced: **0** (quarantined: 5)
- Total tests: **0** (DET rate: **0.0%**)
- Bug reports: **75**
- SCC: **0.00%** (0/316 rules)

## SCC Progression Across Iterations

| Iteration | SCC % | Enforced MRs | Demoted |
|-----------|-------|--------------|---------|
| 1 | 0.00% | 2 | 2 |
| 2 | 0.00% | 0 | 0 |

## MR Registry

- Enforced: **0**
- Quarantined: **5**



## Phase C Test Execution

- Total tests: **0**
- Disagreements: **0**
- DET rate: **0.0%**


## Code Coverage — Primary Target: htsjdk (format scope: VCF)

_Per Flow.md Phase D §1.3, feedback-driven runs measure coverage for the **primary target only** (`htsjdk`). Other SUTs participate as differential oracles and are intentionally not instrumented for coverage._

| SUT | Coverage | Lines | Status |
|-----|----------|-------|--------|
| htsjdk (Java) | 33.9% | 858/2532 | OK |

## Top 10 SCC Blind Spots (Uncovered Spec Rules)

1. **[CRITICAL]** Alternative allele field format
   > [VCF v4.5 — Alternative allele field format] Structural Variants In symbolic alternate alleles for structural variants, ...
2. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] Overall, the idea behind is BCF2 is simple. BCF2 is a binary, compressed equivalent of VC...
3. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] * All BCF2 files must have fully specified contigs definitions.   No record may refer to ...
4. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] * All INFO and GENOTYPE fields must be fully typed in the BCF2 header to enable type-spec...
5. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] Defined this way, the dictionary of strings depends on the order and the presence of all ...
6. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] In BCF2, the original VCF records are converted to binary and encoded as BGZF blocks. Eac...
7. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] Field    	Type    	Notes   l_shared     uint32_t     Data length from CHROM to the end of...
8. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] Bit     Meaning   5,6,7,8 bits     The number of elements of the upcoming type.  For atom...
9. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] Character values are not explicitly typed in BCF2. Instead, VCF Character values must be ...
10. **[CRITICAL]** BCF specification
   > [VCF v4.5 — BCF specification] Vectors of mixed length — In some cases genotype fields may be vectors whose length diffe...

## Bug Reports

- Total: **75**

**By Classification:**
- `metamorphic_violation`: 30
- `crash`: 45

**By Parser:**
- `pysam`: 34
- `reference`: 11
- `htsjdk`: 30

**By Severity:**
- `CRITICAL`: 75

**Top 5 MRs by Failure Count:**
- Header field ordering invariance: 41
- VCF Header Meta-lines Order Invariance: 34
