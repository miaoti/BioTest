# Phase 2 - Coverage Growth Report

Generated 2026-04-20 21:22 UTC by `compares/scripts/render_phase2_report.py` from
`compares/results/coverage/*/growth_*.json`. One sub-directory per
`(tool, SUT)` cell. Every per-rep JSON conforms to DESIGN.md section 4.5:

```json
{
  "tool", "sut", "format", "phase", "run_index", "time_budget_s",
  "seed_corpus_hash",
  "coverage_growth": [{ "t_s", "line_pct", "branch_pct" }]
}
```

Aggregate mean + 95% CI across reps lives in each cell's
`growth_aggregate.json`. This report renders both tiers as tables.

## Cell index

| Tool | SUT | Format | Budget/rep | Reps | Status |
|:-----|:----|:------:|-----------:|-----:|:------|
| `aflpp` | `seqan3` | SAM | 60 s | 3 | PASS (3 reps + aggregate) |
| `atheris` | `biopython` | SAM | 300 s | 3 | PASS (3 reps + aggregate) |
| `cargo_fuzz` | `noodles` | VCF | 1800 s | 2 | PARTIAL (2 reps) |
| `pure_random` | `biopython` | SAM | 7200 s | 3 | PASS (3 reps + aggregate) |
| `pure_random` | `htsjdk_sam` | SAM | 7200 s | 3 | PASS (3 reps + aggregate) |
| `pure_random` | `htsjdk_vcf` | VCF | 7200 s | 3 | PASS (3 reps + aggregate) |
| `pure_random` | `noodles` | VCF | 7200 s | 3 | PASS (3 reps + aggregate) |
| `pure_random` | `seqan3` | SAM | 7200 s | 3 | PASS (3 reps + aggregate) |
| `pure_random` | `vcfpy` | VCF | 7200 s | 3 | PASS (3 reps + aggregate) |


## `aflpp` x `seqan3`

- **Format**: `SAM`
- **Budget per rep**: `60` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4a782127948c933...`
- **Output dir**: `compares/results/coverage/aflpp/seqan3/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 77.70 % | 77.70 % | 77.70 % | 40.96 % | 40.96 % | 40.96 % |
| 10 | 79.11 % | 79.11 % | 79.11 % | 44.54 % | 44.54 % | 44.88 % |
| 60 | 79.11 % | 79.11 % | 79.11 % | 44.54 % | 44.54 % | 44.88 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 77.70 % | 77.70 - 77.70 | 40.96 % | 40.96 - 40.96 |
| 10 | 79.11 % | 79.11 - 79.11 | 44.65 % | 44.43 - 44.88 |
| 60 | 79.11 % | 79.11 - 79.11 | 44.65 % | 44.43 - 44.88 |


## `atheris` x `biopython`

- **Format**: `SAM`
- **Budget per rep**: `300` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4a782127948c933...`
- **Output dir**: `compares/results/coverage/atheris/biopython/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 50.17 % | 50.17 % | 50.17 % | 41.81 % | 41.72 % | 41.47 % |
| 10 | 51.34 % | 51.67 % | 51.67 % | 43.65 % | 44.40 % | 43.81 % |
| 60 | 54.68 % | 54.68 % | 53.85 % | 47.24 % | 47.32 % | 46.74 % |
| 300 | 54.68 % | 54.68 % | 53.85 % | 47.24 % | 47.32 % | 56.69 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 50.17 % | 50.17 - 50.17 | 41.67 % | 41.47 - 41.87 |
| 10 | 51.56 % | 51.34 - 51.78 | 43.95 % | 43.51 - 44.40 |
| 60 | 54.40 % | 53.86 - 54.95 | 47.10 % | 46.74 - 47.46 |
| 300 | 54.40 % | 53.86 - 54.95 | 50.42 % | 44.27 - 56.56 |


## `cargo_fuzz` x `noodles`

- **Format**: `VCF`
- **Budget per rep**: `1800` s
- **Reps**: 2
- **Seed-corpus hash**: `sha256:1c714f9b8c775a6...`
- **Output dir**: `compares/results/coverage/cargo_fuzz/noodles/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 0 branch | rep 1 branch |
|----:|----:|----:|----:|----:|
| 1 | 15.71 % | 15.45 % | 0.00 % | 0.00 % |
| 10 | 17.01 % | 17.49 % | 0.00 % | 0.00 % |
| 60 | 19.52 % | 19.95 % | 0.00 % | 0.00 % |
| 300 | 21.77 % | 21.81 % | 0.00 % | 0.00 % |
| 1800 | 22.94 % | 22.78 % | 0.00 % | 0.00 % |


## `pure_random` x `biopython`

- **Format**: `SAM`
- **Budget per rep**: `7200` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4a782127948c933...`
- **Output dir**: `compares/results/coverage/pure_random/biopython/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 0.50 % | 0.50 % | 0.50 % | 0.00 % | 0.00 % | 0.00 % |
| 10 | 0.50 % | 0.50 % | 0.50 % | 0.00 % | 0.00 % | 0.00 % |
| 60 | 0.50 % | 0.50 % | 0.50 % | 0.00 % | 0.00 % | 0.00 % |
| 300 | 0.50 % | 0.50 % | 0.50 % | 0.00 % | 0.00 % | 0.00 % |
| 1800 | 0.50 % | 0.50 % | 2.51 % | 0.00 % | 0.00 % | 1.33 % |
| 7200 | 2.51 % | 0.50 % | 2.51 % | 1.33 % | 0.00 % | 1.33 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 0.50 % | 0.50 - 0.50 | 0.00 % | 0.00 - 0.00 |
| 10 | 0.50 % | 0.50 - 0.50 | 0.00 % | 0.00 - 0.00 |
| 60 | 0.50 % | 0.50 - 0.50 | 0.00 % | 0.00 - 0.00 |
| 300 | 0.50 % | 0.50 - 0.50 | 0.00 % | 0.00 - 0.00 |
| 1800 | 1.17 % | -0.14 - 2.48 | 0.44 % | -0.43 - 1.32 |
| 7200 | 1.84 % | 0.53 - 3.15 | 0.89 % | 0.02 - 1.76 |


## `pure_random` x `htsjdk_sam`

- **Format**: `SAM`
- **Budget per rep**: `7200` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4a782127948c933...`
- **Output dir**: `compares/results/coverage/pure_random/htsjdk_sam/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 1.85 % | 1.87 % | 1.85 % | 0.63 % | 0.67 % | 0.63 % |
| 10 | 1.85 % | 1.87 % | 1.85 % | 0.63 % | 0.67 % | 0.63 % |
| 60 | 1.88 % | 1.87 % | 1.85 % | 0.68 % | 0.67 % | 0.63 % |
| 300 | 1.88 % | 1.89 % | 1.88 % | 0.68 % | 0.69 % | 0.68 % |
| 1800 | 1.89 % | 1.89 % | 2.34 % | 0.69 % | 0.70 % | 0.77 % |
| 7200 | 1.89 % | 2.34 % | 2.34 % | 0.70 % | 0.78 % | 0.78 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 1.86 % | 1.84 - 1.87 | 0.65 % | 0.62 - 0.67 |
| 10 | 1.86 % | 1.84 - 1.87 | 0.65 % | 0.62 - 0.67 |
| 60 | 1.87 % | 1.85 - 1.89 | 0.66 % | 0.63 - 0.69 |
| 300 | 1.88 % | 1.88 - 1.89 | 0.68 % | 0.68 - 0.69 |
| 1800 | 2.04 % | 1.74 - 2.34 | 0.72 % | 0.67 - 0.77 |
| 7200 | 2.19 % | 1.90 - 2.49 | 0.75 % | 0.71 - 0.80 |


## `pure_random` x `htsjdk_vcf`

- **Format**: `VCF`
- **Budget per rep**: `7200` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4cd63425582d21a...`
- **Output dir**: `compares/results/coverage/pure_random/htsjdk_vcf/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 1.46 % | 1.46 % | 1.46 % | 0.30 % | 0.30 % | 0.30 % |
| 10 | 1.46 % | 1.46 % | 1.46 % | 0.30 % | 0.30 % | 0.30 % |
| 60 | 1.46 % | 1.46 % | 1.46 % | 0.30 % | 0.30 % | 0.30 % |
| 300 | 1.46 % | 1.46 % | 1.46 % | 0.30 % | 0.30 % | 0.30 % |
| 1800 | 1.46 % | 1.46 % | 1.46 % | 0.30 % | 0.30 % | 0.30 % |
| 7200 | 1.46 % | 1.54 % | 1.46 % | 0.30 % | 0.46 % | 0.30 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 1.46 % | 1.46 - 1.46 | 0.30 % | 0.30 - 0.30 |
| 10 | 1.46 % | 1.46 - 1.46 | 0.30 % | 0.30 - 0.30 |
| 60 | 1.46 % | 1.46 - 1.46 | 0.30 % | 0.30 - 0.30 |
| 300 | 1.46 % | 1.46 - 1.46 | 0.30 % | 0.30 - 0.30 |
| 1800 | 1.46 % | 1.46 - 1.46 | 0.30 % | 0.30 - 0.30 |
| 7200 | 1.49 % | 1.44 - 1.54 | 0.35 % | 0.26 - 0.45 |


## `pure_random` x `noodles`

- **Format**: `VCF`
- **Budget per rep**: `7200` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4cd63425582d21a...`
- **Output dir**: `compares/results/coverage/pure_random/noodles/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % |
| 10 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % |
| 60 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % |
| 300 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % |
| 1800 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % |
| 7200 | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 0.00 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 0.00 % | 0.00 - 0.00 | 0.00 % | 0.00 - 0.00 |
| 10 | 0.00 % | 0.00 - 0.00 | 0.00 % | 0.00 - 0.00 |
| 60 | 0.00 % | 0.00 - 0.00 | 0.00 % | 0.00 - 0.00 |
| 300 | 0.00 % | 0.00 - 0.00 | 0.00 % | 0.00 - 0.00 |
| 1800 | 0.00 % | 0.00 - 0.00 | 0.00 % | 0.00 - 0.00 |
| 7200 | 0.00 % | 0.00 - 0.00 | 0.00 % | 0.00 - 0.00 |


## `pure_random` x `seqan3`

- **Format**: `SAM`
- **Budget per rep**: `7200` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4a782127948c933...`
- **Output dir**: `compares/results/coverage/pure_random/seqan3/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 25.44 % | 25.44 % | 25.44 % | 9.79 % | 9.79 % | 9.79 % |
| 10 | 25.44 % | 25.44 % | 25.44 % | 9.79 % | 9.79 % | 9.79 % |
| 60 | 25.44 % | 25.44 % | 25.44 % | 9.79 % | 9.79 % | 9.79 % |
| 300 | 68.64 % | 25.44 % | 25.44 % | 35.74 % | 9.79 % | 10.21 % |
| 1800 | 25.44 % | 79.29 % | 73.37 % | 9.79 % | 43.19 % | 40.43 % |
| 7200 | 69.23 % | 84.61 % | 81.06 % | 36.60 % | 48.51 % | 44.47 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 25.44 % | 25.44 - 25.44 | 9.79 % | 9.79 - 9.79 |
| 10 | 25.44 % | 25.44 - 25.44 | 9.79 % | 9.79 - 9.79 |
| 60 | 25.44 % | 25.44 - 25.44 | 9.79 % | 9.79 - 9.79 |
| 300 | 39.84 % | 11.62 - 68.06 | 18.58 % | 1.76 - 35.40 |
| 1800 | 59.37 % | 25.95 - 92.78 | 31.13 % | 10.16 - 52.11 |
| 7200 | 78.30 % | 69.19 - 87.42 | 43.19 % | 36.34 - 50.05 |


## `pure_random` x `vcfpy`

- **Format**: `VCF`
- **Budget per rep**: `7200` s
- **Reps**: 3
- **Seed-corpus hash**: `sha256:4cd63425582d21a...`
- **Output dir**: `compares/results/coverage/pure_random/vcfpy/`

### Per-rep ticks

| t_s | rep 0 line | rep 1 line | rep 2 line | rep 0 branch | rep 1 branch | rep 2 branch |
|----:|----:|----:|----:|----:|----:|----:|
| 1 | 1.70 % | 1.70 % | 1.70 % | 0.34 % | 0.34 % | 0.34 % |
| 10 | 1.70 % | 1.70 % | 1.70 % | 0.34 % | 0.34 % | 0.34 % |
| 60 | 1.70 % | 1.70 % | 1.70 % | 0.34 % | 0.34 % | 0.34 % |
| 300 | 1.70 % | 2.72 % | 1.70 % | 0.34 % | 0.67 % | 0.34 % |
| 1800 | 2.72 % | 2.72 % | 1.70 % | 0.67 % | 0.67 % | 0.34 % |
| 7200 | 2.72 % | 2.72 % | 2.72 % | 0.67 % | 0.67 % | 0.67 % |

### Aggregate (mean + 95% CI)

| t_s | line mean | line 95% CI | branch mean | branch 95% CI |
|----:|----------:|:------------|------------:|:--------------|
| 1 | 1.70 % | 1.70 - 1.70 | 0.34 % | 0.34 - 0.34 |
| 10 | 1.70 % | 1.70 - 1.70 | 0.34 % | 0.34 - 0.34 |
| 60 | 1.70 % | 1.70 - 1.70 | 0.34 % | 0.34 - 0.34 |
| 300 | 2.04 % | 1.37 - 2.71 | 0.45 % | 0.23 - 0.67 |
| 1800 | 2.38 % | 1.71 - 3.05 | 0.56 % | 0.34 - 0.78 |
| 7200 | 2.72 % | 2.72 - 2.72 | 0.67 % | 0.67 - 0.67 |

## Methodology

- **Tick ladder** (DESIGN section 3.2 primary regime):
  `{1, 10, 60, 300, 1800, 7200}` seconds.
- **Regime**: cells with 300 s budget ran the DESIGN section 3.2
  *secondary* regime, ticks `{1, 10, 60, 300}`. Cells with 7200 s
  budget ran the *primary* regime, all six ticks. Intermediate
  budgets (for example 1800 s on `cargo_fuzz x noodles`) are
  spot samples meant to surface the curve without blocking on
  the full 6 h overnight window.
- **Coverage backends**: JaCoCo (htsjdk), `coverage.py` (vcfpy,
  biopython), `cargo-llvm-cov` (noodles-vcf), gcovr (seqan3).
  Pure-random uses each SUT's own backend unchanged; scope is the
  whitelist in `biotest_config.yaml: coverage.target_filters`.
- **Schema**: every `growth_<rep>.json` validates against DESIGN
  section 4.5. The sibling `run_<rep>/harness_growth.json` carries
  the richer per-tick record (`covered_lines`, `total_lines`,
  `covered_branches`, `total_branches`, `wall_s`) for audit.
- **Aggregates**: `growth_aggregate.json` per cell reports mean +
  95% CI across reps (`mean +/- 1.96 * sigma / sqrt(n)`).

## Status legend

- **PASS (3 reps + aggregate)**: 3 complete reps + a rebuilt
  `growth_aggregate.json`; ready for the Phase 6 report.
- **PASS (3 reps, no aggregate)**: 3 reps on disk but
  `growth_aggregate.json` not yet regenerated; rerun the
  per-cell aggregator.
- **PARTIAL**: fewer than 3 reps landed; the sampler was cut short
  (manual SIGINT, docker restart, host reboot, ...) and the
  remaining reps should be re-queued before Phase 6 consumes
  this row.

## Cells still queued (not in this report)

- **Jazzer x htsjdk (VCF + SAM)** - primary 7200 s x 3 rep slot
  launched via `compares/scripts/phase2_jazzer_htsjdk.sh`. Raw
  per-tick `.exec` files land under `jazzer/htsjdk_{vcf,sam}/
  run_<n>/jacoco_exec/`; the rolled-up `growth_<n>.json` only
  materialises after the `jacococli report` post-pass the
  sampler runs at rep end. Expected wall-time approx 6 h.
- **libFuzzer x seqan3** - 7200 s x 3 rep run in flight. See
  `libfuzzer/seqan3/_STATUS.md`.
- **Atheris x vcfpy** - primary 7200 s x 3 rep run in flight.
  See `atheris/vcfpy/rep{0,1,2}_sampler.log`.
- **Atheris x biopython PRIMARY (7200 s x 3 reps)** - queued via
  `bash compares/scripts/phase2_atheris_biopython.sh`. This
  session captured the 300 s x 3 rep *secondary* regime (shown
  above); the primary run is intentionally overnight.
- **BioTest x every SUT** - the tool-under-evaluation row is
  executed by the main BioTest Phase-C pipeline, not by
  `coverage_sampler.py`. Its curves merge into this report at
  Phase 6 aggregation.

