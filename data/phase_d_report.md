# Phase D End-to-End Run Report — 2026-04-16 22:18:33

## Executive Summary

- Iterations completed: **3**
- Total MRs enforced: **1** (quarantined: 2)
- Total tests: **28** (DET rate: **53.6%**)
- Bug reports: **33**
- SCC: **0.63%** (2/316 rules)

## SCC Progression Across Iterations

| Iteration | SCC % | Enforced MRs | Demoted |
|-----------|-------|--------------|---------|
| 1 | 0.63% | 2 | 1 |
| 2 | 0.63% | 1 | 0 |
| 3 | 0.63% | 1 | 0 |

## MR Registry

- Enforced: **1**
- Quarantined: **2**

**Transform Step Distribution (top 10):**

| Transform | Count |
|-----------|-------|
| `shuffle_meta_lines` | 1 |

**Enforced MRs:**

| mr_id | mr_name |
|-------|---------|
| `ffbe4a62d130` | VCF Header Meta-lines Order Invariance |

## Phase C Test Execution

- Total tests: **28**
- Disagreements: **15**
- DET rate: **53.6%**

**By Test Type:**

| Type | Total | Failures | DET % |
|------|-------|----------|-------|
| metamorphic | 21 | 8 | 38.1% |
| differential | 7 | 7 | 100.0% |

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

- Total: **33**

**By Classification:**
- `metamorphic_violation`: 18
- `crash`: 15

**By Parser:**
- `pysam`: 20
- `reference`: 6
- `htsjdk`: 7

**By Severity:**
- `CRITICAL`: 33

**Top 5 MRs by Failure Count:**
- VCF Header Meta-lines Order Invariance: 24
- Ordering invariance of meta-information lines: 9
