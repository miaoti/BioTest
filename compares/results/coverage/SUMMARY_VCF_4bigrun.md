# BioTest 4-big-run VCF coverage — SUMMARY

- Each big run = 4 small reps (rep 0 fresh, reps 1-3 cascade-from-prev)
- 6 SUTs in DESIGN.md but this analysis focuses on the **3 VCF cells only**
- LLM: deepseek-chat (forced via per-cell config override)
- Phase D (which internally runs B+C with coverage)
- Per-big-run mean = arithmetic mean of small reps' line%
- Cross-big-run std (n=4) = sample std of the 4 big-run means

## Big-run means (line %)

| Cell           | Run 1  | Run 2  | Run 3  | Run 4  | Mean(4)  | Std(4) |
|----------------|-------:|-------:|-------:|-------:|---------:|-------:|
| htsjdk_vcf     |  36.40 |   --   |   --   |   --   |    36.40 |   --   |
| vcfpy_vcf      |  67.05 |   --   |   --   |   --   |    67.05 |   --   |
| noodles_vcf    |  23.85 |   --   |   --   |   --   |    23.85 |   --   |

## Per-big-run × per-rep matrix (line %)

Rep numbers in column header. Each cell shows line% (status=ok), or `--` if status was missing/empty.

### htsjdk_vcf

| Big run | rep 0  | rep 1  | rep 2  | rep 3  | mean   |
|---------|-------:|-------:|-------:|-------:|-------:|
| run1    |  45.90 |  33.90 |  32.90 |  32.90 |  36.40 |
| run2    |   --   |   --   |   --   |   --   |   --   |
| run3    |   --   |   --   |   --   |   --   |   --   |
| run4    |   --   |   --   |   --   |   --   |   --   |

### vcfpy_vcf

| Big run | rep 0  | rep 1  | rep 2  | rep 3  | mean   |
|---------|-------:|-------:|-------:|-------:|-------:|
| run1    |  73.50 |  64.90 |  64.90 |  64.90 |  67.05 |
| run2    |   --   |   --   |   --   |   --   |   --   |
| run3    |   --   |   --   |   --   |   --   |   --   |
| run4    |   --   |   --   |   --   |   --   |   --   |

### noodles_vcf

| Big run | rep 0  | rep 1  | rep 2  | rep 3  | mean   |
|---------|-------:|-------:|-------:|-------:|-------:|
| run1    |  39.90 |  18.60 |  18.70 |  18.20 |  23.85 |
| run2    |   --   |   --   |   --   |   --   |   --   |
| run3    |   --   |   --   |   --   |   --   |   --   |
| run4    |   --   |   --   |   --   |   --   |   --   |

## Source dirs

- **run1**: `compares/results/coverage/biotest_4rep_cascade_20260427/`
- **run2**: `compares/results/coverage/biotest_4rep_cascade_run2_20260429/`
- **run3**: `compares/results/coverage/biotest_4rep_cascade_run3_20260429/`
- **run4**: `compares/results/coverage/biotest_4rep_cascade_run4_20260429/`

## Methodology notes

- Each big run starts FRESH (no cascade across big runs).
- Within a big run, rep N inherits rep N-1's seed corpus (`kept_*`/`synthetic_*` accumulate).
- All 4 big runs use the same protocol: `max_iterations=2`, 5400s wall cap per rep.
- vcfpy_vcf reps that hit Windows `TerminateProcess` at the wall cap (status=missing) are recovered with `max_iter=1` against the cascaded seed corpus, matching run 1's recovery protocol.
- htsjdk_vcf and noodles_vcf cells reliably produce `status=ok` measurements without recovery.