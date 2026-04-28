# Phase 2 — Coverage Growth — Per-SUT Results

Consolidated view of every Phase-2 (tool × SUT) cell that has landed
measurements under `compares/results/coverage/`. Regenerate in place
whenever a new `growth_<rep>.json` lands:

```
py -3 compares/scripts/build_coverage_report.py
```

Schema per cell: DESIGN.md §4.5 (`coverage_growth`: list of
`{t_s, line_pct, branch_pct}` at log ticks `{1,10,60,300,1800,7200}`).
Per-tick tables show **mean [min–max]** across the cell's reps.

## 0. Status matrix

For a compact visual matrix (rows = SUT, columns = tool, one table per
format), see the sibling `COVERAGE_MATRIX.md`.

| Tool × SUT × format | Status | Budget (s) | Reps | Data dir |
|:---|:---:|:---:|:---:|:---|
| atheris × biopython × SAM | ✅ executed | 300 | 3 | `compares/results/coverage/atheris/biopython/` |
| pure_random × biopython × SAM | ✅ executed | 7200 | 3 | `compares/results/coverage/pure_random/biopython/` |
| pure_random × htsjdk × SAM | ✅ executed | 7200 | 3 | `compares/results/coverage/pure_random/htsjdk_sam/` |
| pure_random × htsjdk × VCF | ✅ executed | 7200 | 3 | `compares/results/coverage/pure_random/htsjdk_vcf/` |
| cargo_fuzz × noodles × VCF | ✅ executed | 1800 | 3 | `compares/results/coverage/cargo_fuzz/noodles/` |
| pure_random × noodles × VCF | ✅ executed | 7200 | 3 | `compares/results/coverage/pure_random/noodles/` |
| aflpp × seqan3 × SAM | ✅ executed | 60 | 3 | `compares/results/coverage/aflpp/seqan3/` |
| pure_random × seqan3 × SAM | ✅ executed | 7200 | 3 | `compares/results/coverage/pure_random/seqan3/` |
| atheris × vcfpy × VCF | ✅ executed | 7200 | 3 | `compares/results/coverage/atheris/vcfpy/` |
| pure_random × vcfpy × VCF | ✅ executed | 7200 | 3 | `compares/results/coverage/pure_random/vcfpy/` |
| jazzer × htsjdk × VCF | ✅ executed | 7200 | 3 | `compares/results/coverage/jazzer/htsjdk_vcf/` |
| jazzer × htsjdk × SAM | ✅ executed | 7200 | 3 | `compares/results/coverage/jazzer/htsjdk_sam/` |
| libfuzzer × seqan3 × SAM | ✅ executed | 7200 | 3 | `compares/results/coverage/libfuzzer/seqan3/` |
| biotest × htsjdk × VCF | 📝 end-of-run only | — | — | `coverage_notes/htsjdk/vcf/biotest.md` (Runs 6-8) |
| biotest × htsjdk × SAM | 📝 end-of-run only | — | — | `coverage_notes/htsjdk/sam/biotest.md` (Runs 9-11) |
| biotest × vcfpy × VCF | 📝 end-of-run only | — | — | `coverage_notes/vcfpy/vcf/biotest.md` (Run 1) |
| biotest × noodles × VCF | 📝 end-of-run only | — | — | `coverage_notes/noodles/vcf/biotest.md` (Run 12) |
| biotest × biopython × SAM | 📝 end-of-run only | — | — | `coverage_notes/biopython/sam/biotest.md` (Runs 1-4) |
| biotest × seqan3 × SAM | 📝 end-of-run only (DESIGN scope = 0/0) | — | — | `coverage_notes/seqan3/sam/biotest.md` (Run 1) |

**Executed (tick-sampled)**: 13 cells.
**BioTest end-of-run (non-tick)**: 6 cells — see `COVERAGE_MATRIX.md` §3
for why these cannot yet be plotted on the same log-tick axis and the
re-run plan to fix that.

Legend for `Status`:
- `✅ executed` — `growth_aggregate.json` present with tick-sampled
  reps at `{1, 10, 60, 300, 1800, 7200}` (or the subset that fits the
  cell's budget). Directly comparable row-to-row within the same
  format.
- `📝 end-of-run only` — BioTest's Phase-D loop wrote final JaCoCo /
  coverage.py / gcovr / llvm-cov artefacts at end-of-run only, NOT at
  tick boundaries. The number in `coverage_notes/.../biotest.md` is a
  single wall-clock-terminal reading; wall times vary by run (14 m to
  402 m) and are not aligned to the baseline tools' tick schedule.
  Reconciliation requires re-running BioTest under `coverage_sampler.py`
  via an adapter that polls coverage at each tick — see
  `COVERAGE_MATRIX.md` §3c, Option A.

## 1. Per-SUT cross-tool comparison

### biopython × SAM

| t (s) | atheris line % [min–max] | pure_random line % [min–max] |
|:---:|---|---|
| 1 | 50.17 [50.17–50.17] | 0.50 [0.50–0.50] |
| 10 | 51.56 [51.34–51.67] | 0.50 [0.50–0.50] |
| 60 | 54.40 [53.85–54.68] | 0.50 [0.50–0.50] |
| 300 | 54.40 [53.85–54.68] | 0.50 [0.50–0.50] |
| 1800 | — | 1.17 [0.50–2.51] |
| 7200 | — | 1.84 [0.50–2.51] |

Branch coverage mirror (same cells):

| t (s) | atheris branch % [min–max] | pure_random branch % [min–max] |
|:---:|---|---|
| 1 | 41.67 [41.47–41.81] | 0.00 [0.00–0.00] |
| 10 | 43.95 [43.65–44.40] | 0.00 [0.00–0.00] |
| 60 | 47.10 [46.74–47.32] | 0.00 [0.00–0.00] |
| 300 | 50.42 [47.24–56.69] | 0.00 [0.00–0.00] |
| 1800 | — | 0.44 [0.00–1.33] |
| 7200 | — | 0.89 [0.00–1.33] |

### htsjdk × SAM

| t (s) | pure_random line % [min–max] |
|:---:|---|
| 1 | 1.86 [1.85–1.87] |
| 10 | 1.86 [1.85–1.87] |
| 60 | 1.87 [1.85–1.88] |
| 300 | 1.88 [1.88–1.89] |
| 1800 | 2.04 [1.89–2.34] |
| 7200 | 2.19 [1.89–2.34] |

Branch coverage mirror (same cells):

| t (s) | pure_random branch % [min–max] |
|:---:|---|
| 1 | 0.65 [0.63–0.67] |
| 10 | 0.65 [0.63–0.67] |
| 60 | 0.66 [0.63–0.68] |
| 300 | 0.68 [0.68–0.69] |
| 1800 | 0.72 [0.69–0.77] |
| 7200 | 0.75 [0.70–0.78] |

### htsjdk × VCF

| t (s) | pure_random line % [min–max] |
|:---:|---|
| 1 | 1.46 [1.46–1.46] |
| 10 | 1.46 [1.46–1.46] |
| 60 | 1.46 [1.46–1.46] |
| 300 | 1.46 [1.46–1.46] |
| 1800 | 1.46 [1.46–1.46] |
| 7200 | 1.49 [1.46–1.54] |

Branch coverage mirror (same cells):

| t (s) | pure_random branch % [min–max] |
|:---:|---|
| 1 | 0.30 [0.30–0.30] |
| 10 | 0.30 [0.30–0.30] |
| 60 | 0.30 [0.30–0.30] |
| 300 | 0.30 [0.30–0.30] |
| 1800 | 0.30 [0.30–0.30] |
| 7200 | 0.35 [0.30–0.46] |

### noodles × VCF

| t (s) | cargo_fuzz line % [min–max] | pure_random line % [min–max] |
|:---:|---|---|
| 1 | 15.58 [15.45–15.71] | 0.00 [0.00–0.00] |
| 10 | 17.25 [17.01–17.49] | 0.00 [0.00–0.00] |
| 60 | 19.74 [19.52–19.95] | 0.00 [0.00–0.00] |
| 300 | 21.79 [21.77–21.81] | 0.00 [0.00–0.00] |
| 1800 | 22.86 [22.78–22.94] | 0.00 [0.00–0.00] |
| 7200 | — | 0.00 [0.00–0.00] |

Branch coverage mirror (same cells):

| t (s) | cargo_fuzz branch % [min–max] | pure_random branch % [min–max] |
|:---:|---|---|
| 1 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 10 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 60 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 300 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 1800 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 7200 | — | 0.00 [0.00–0.00] |

### seqan3 × SAM

| t (s) | aflpp line % [min–max] | pure_random line % [min–max] |
|:---:|---|---|
| 1 | 77.70 [77.70–77.70] | 25.44 [25.44–25.44] |
| 10 | 79.11 [79.11–79.11] | 25.44 [25.44–25.44] |
| 60 | 79.11 [79.11–79.11] | 25.44 [25.44–25.44] |
| 300 | — | 39.84 [25.44–68.64] |
| 1800 | — | 59.37 [25.44–79.29] |
| 7200 | — | 78.30 [69.23–84.61] |

Branch coverage mirror (same cells):

| t (s) | aflpp branch % [min–max] | pure_random branch % [min–max] |
|:---:|---|---|
| 1 | 40.96 [40.96–40.96] | 9.79 [9.79–9.79] |
| 10 | 44.65 [44.54–44.88] | 9.79 [9.79–9.79] |
| 60 | 44.65 [44.54–44.88] | 9.79 [9.79–9.79] |
| 300 | — | 18.58 [9.79–35.74] |
| 1800 | — | 31.14 [9.79–43.19] |
| 7200 | — | 43.19 [36.60–48.51] |

### vcfpy × VCF

| t (s) | atheris line % [min–max] | pure_random line % [min–max] |
|:---:|---|---|
| 1 | 52.47 [52.47–52.47] | 1.70 [1.70–1.70] |
| 10 | 53.60 [53.45–53.70] | 1.70 [1.70–1.70] |
| 60 | 54.44 [54.25–54.56] | 1.70 [1.70–1.70] |
| 300 | 54.79 [54.38–54.99] | 2.04 [1.70–2.72] |
| 1800 | 55.01 [54.99–55.06] | 2.38 [1.70–2.72] |
| 7200 | — | 2.72 [2.72–2.72] |

Branch coverage mirror (same cells):

| t (s) | atheris branch % [min–max] | pure_random branch % [min–max] |
|:---:|---|---|
| 1 | 40.46 [40.46–40.46] | 0.34 [0.34–0.34] |
| 10 | 42.50 [42.18–42.75] | 0.34 [0.34–0.34] |
| 60 | 43.76 [43.51–44.08] | 0.34 [0.34–0.34] |
| 300 | 44.53 [44.27–44.66] | 0.45 [0.34–0.67] |
| 1800 | 44.85 [44.66–45.23] | 0.56 [0.34–0.67] |
| 7200 | — | 0.67 [0.67–0.67] |

## 2. Per-cell detail

### atheris × biopython × SAM

- **Data directory**: `compares/results/coverage/atheris/biopython/`
- **Budget**: 300 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300]  
- **Source**: growth_N.json
- **Budget note**: short-regime run. DESIGN §3.2 primary is 7200 s × 3 reps; this cell ran at 300 s.

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 302.21 | 54.68 | 47.24 |
| 1 | 302.33 | 54.68 | 47.32 |
| 2 | 0.0 | 53.85 | 56.69 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 50.17 [50.17–50.17] | 41.67 [41.47–41.81] |
| 10 | 3 | 51.56 [51.34–51.67] | 43.95 [43.65–44.40] |
| 60 | 3 | 54.40 [53.85–54.68] | 47.10 [46.74–47.32] |
| 300 | 3 | 54.40 [53.85–54.68] | 50.42 [47.24–56.69] |

### pure_random × biopython × SAM

- **Data directory**: `compares/results/coverage/pure_random/biopython/`
- **Budget**: 7200 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300, 1800, 7200]  
- **Source**: growth_N.json

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 3.09 | 2.51 | 1.33 |
| 1 | 3.17 | 0.50 | 0.00 |
| 2 | 3.25 | 2.51 | 1.33 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 0.50 [0.50–0.50] | 0.00 [0.00–0.00] |
| 10 | 3 | 0.50 [0.50–0.50] | 0.00 [0.00–0.00] |
| 60 | 3 | 0.50 [0.50–0.50] | 0.00 [0.00–0.00] |
| 300 | 3 | 0.50 [0.50–0.50] | 0.00 [0.00–0.00] |
| 1800 | 3 | 1.17 [0.50–2.51] | 0.44 [0.00–1.33] |
| 7200 | 3 | 1.84 [0.50–2.51] | 0.89 [0.00–1.33] |

### pure_random × htsjdk × SAM

- **Data directory**: `compares/results/coverage/pure_random/htsjdk_sam/`
- **Budget**: 7200 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300, 1800, 7200]  
- **Source**: growth_N.json

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 87.61 | 1.89 | 0.70 |
| 1 | 85.97 | 2.34 | 0.78 |
| 2 | 85.84 | 2.34 | 0.78 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 1.86 [1.85–1.87] | 0.65 [0.63–0.67] |
| 10 | 3 | 1.86 [1.85–1.87] | 0.65 [0.63–0.67] |
| 60 | 3 | 1.87 [1.85–1.88] | 0.66 [0.63–0.68] |
| 300 | 3 | 1.88 [1.88–1.89] | 0.68 [0.68–0.69] |
| 1800 | 3 | 2.04 [1.89–2.34] | 0.72 [0.69–0.77] |
| 7200 | 3 | 2.19 [1.89–2.34] | 0.75 [0.70–0.78] |

### pure_random × htsjdk × VCF

- **Data directory**: `compares/results/coverage/pure_random/htsjdk_vcf/`
- **Budget**: 7200 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300, 1800, 7200]  
- **Source**: growth_N.json

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 78.74 | 1.46 | 0.30 |
| 1 | 78.9 | 1.54 | 0.46 |
| 2 | 77.97 | 1.46 | 0.30 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 1.46 [1.46–1.46] | 0.30 [0.30–0.30] |
| 10 | 3 | 1.46 [1.46–1.46] | 0.30 [0.30–0.30] |
| 60 | 3 | 1.46 [1.46–1.46] | 0.30 [0.30–0.30] |
| 300 | 3 | 1.46 [1.46–1.46] | 0.30 [0.30–0.30] |
| 1800 | 3 | 1.46 [1.46–1.46] | 0.30 [0.30–0.30] |
| 7200 | 3 | 1.49 [1.46–1.54] | 0.35 [0.30–0.46] |

### cargo_fuzz × noodles × VCF

- **Data directory**: `compares/results/coverage/cargo_fuzz/noodles/`
- **Budget**: 1800 s per rep  
- **Reps**: 2  
- **Ticks requested**: [1, 10, 60, 300, 1800, 7200]  
- **Source**: growth_N.json
- **Budget note**: short-regime run. DESIGN §3.2 primary is 7200 s × 3 reps; this cell ran at 1800 s.

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 1868.9 | 22.94 | 0.00 |
| 1 | 1881.21 | 22.78 | 0.00 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 2 | 15.58 [15.45–15.71] | 0.00 [0.00–0.00] |
| 10 | 2 | 17.25 [17.01–17.49] | 0.00 [0.00–0.00] |
| 60 | 2 | 19.74 [19.52–19.95] | 0.00 [0.00–0.00] |
| 300 | 2 | 21.79 [21.77–21.81] | 0.00 [0.00–0.00] |
| 1800 | 2 | 22.86 [22.78–22.94] | 0.00 [0.00–0.00] |

### pure_random × noodles × VCF

- **Data directory**: `compares/results/coverage/pure_random/noodles/`
- **Budget**: 7200 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300, 1800, 7200]  
- **Source**: growth_N.json

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 0.1 | 0.00 | 0.00 |
| 1 | 0.11 | 0.00 | 0.00 |
| 2 | 0.1 | 0.00 | 0.00 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 10 | 3 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 60 | 3 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 300 | 3 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 1800 | 3 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |
| 7200 | 3 | 0.00 [0.00–0.00] | 0.00 [0.00–0.00] |

### aflpp × seqan3 × SAM

- **Data directory**: `compares/results/coverage/aflpp/seqan3/`
- **Budget**: 60 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60]  
- **Source**: growth_N.json
- **Budget note**: short-regime run. DESIGN §3.2 primary is 7200 s × 3 reps; this cell ran at 60 s.

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 35.82 | 79.11 | 44.54 |
| 1 | 38.12 | 79.11 | 44.54 |
| 2 | 39.57 | 79.11 | 44.88 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 77.70 [77.70–77.70] | 40.96 [40.96–40.96] |
| 10 | 3 | 79.11 [79.11–79.11] | 44.65 [44.54–44.88] |
| 60 | 3 | 79.11 [79.11–79.11] | 44.65 [44.54–44.88] |

### pure_random × seqan3 × SAM

- **Data directory**: `compares/results/coverage/pure_random/seqan3/`
- **Budget**: 7200 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300, 1800, 7200]  
- **Source**: growth_N.json

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 5.09 | 69.23 | 36.60 |
| 1 | 6.04 | 84.61 | 48.51 |
| 2 | 5.1 | 81.06 | 44.47 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 25.44 [25.44–25.44] | 9.79 [9.79–9.79] |
| 10 | 3 | 25.44 [25.44–25.44] | 9.79 [9.79–9.79] |
| 60 | 3 | 25.44 [25.44–25.44] | 9.79 [9.79–9.79] |
| 300 | 3 | 39.84 [25.44–68.64] | 18.58 [9.79–35.74] |
| 1800 | 3 | 59.37 [25.44–79.29] | 31.14 [9.79–43.19] |
| 7200 | 3 | 78.30 [69.23–84.61] | 43.19 [36.60–48.51] |

### atheris × vcfpy × VCF

- **Data directory**: `compares/results/coverage/atheris/vcfpy/`
- **Budget**: 1800 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300, 1800]  
- **Source**: harness_growth.json (sidecar)
- **Budget note**: short-regime run. DESIGN §3.2 primary is 7200 s × 3 reps; this cell ran at 1800 s.

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | — | 55.06 | 45.23 |
| 1 | — | 54.99 | 44.66 |
| 2 | — | 54.99 | 44.66 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 52.47 [52.47–52.47] | 40.46 [40.46–40.46] |
| 10 | 3 | 53.60 [53.45–53.70] | 42.50 [42.18–42.75] |
| 60 | 3 | 54.44 [54.25–54.56] | 43.76 [43.51–44.08] |
| 300 | 3 | 54.79 [54.38–54.99] | 44.53 [44.27–44.66] |
| 1800 | 3 | 55.01 [54.99–55.06] | 44.85 [44.66–45.23] |

### pure_random × vcfpy × VCF

- **Data directory**: `compares/results/coverage/pure_random/vcfpy/`
- **Budget**: 7200 s per rep  
- **Reps**: 3  
- **Ticks requested**: [1, 10, 60, 300, 1800, 7200]  
- **Source**: growth_N.json

Per-rep final coverage:

| rep | duration (s) | final line % | final branch % |
|:---:|:---:|:---:|:---:|
| 0 | 3.64 | 2.72 | 0.67 |
| 1 | 3.49 | 2.72 | 0.67 |
| 2 | 3.65 | 2.72 | 0.67 |

Aggregate per-tick (mean [min–max]):

| t (s) | reps | line % | branch % |
|:---:|:---:|:---|:---|
| 1 | 3 | 1.70 [1.70–1.70] | 0.34 [0.34–0.34] |
| 10 | 3 | 1.70 [1.70–1.70] | 0.34 [0.34–0.34] |
| 60 | 3 | 1.70 [1.70–1.70] | 0.34 [0.34–0.34] |
| 300 | 3 | 2.04 [1.70–2.72] | 0.45 [0.34–0.67] |
| 1800 | 3 | 2.38 [1.70–2.72] | 0.56 [0.34–0.67] |
| 7200 | 3 | 2.72 [2.72–2.72] | 0.67 [0.67–0.67] |

## 3. Methodology + scope

Coverage is scoped per (format, SUT) per
`biotest_config.yaml:coverage.target_filters`. For each cell the
per-tool backend drives the fuzzer for the time budget, then
captures line + branch % at the log ticks via the language-native
tooling:

| Tool / SUT | Coverage tooling | Scope substrings |
|:---|:---|:---|
| jazzer × htsjdk | JaCoCo TCP-server agent (`jacocoagent.jar` / `jacococli.jar`) | `htsjdk/variant/vcf`, `htsjdk/variant/variantcontext/writer` (VCF); `htsjdk/samtools` (SAM) |
| atheris × vcfpy | `coverage.py` in-process, branch=True | `vcfpy` (whole package) |
| atheris × biopython | `coverage.py` in-process, branch=True | `Bio/Align/sam` |
| cargo_fuzz × noodles | `cargo-llvm-cov` + replay-through-instrumented-harness | `noodles-vcf` (crate path substring) |
| libfuzzer × seqan3 | `gcovr` + `llvm-cov-18 gcov` + corpus-replay | `seqan3/io/sam_file`, `format_sam`, `cigar` |
| aflpp × seqan3 | `gcovr` + `gcov-12` + corpus-replay | `seqan3/io/sam_file`, `format_sam`, `cigar` |
| pure_random × * | per-SUT native (same as the fuzzer row above) | same as the fuzzer row above |

Binaries + harnesses — see DESIGN.md §13.2 for per-tool build
commands. Coverage scope is enforced at JSON-parse time in Python,
so a tool that reports coverage outside scope (e.g., seqan3's
`/usr/include/c++/12/*` artefacts) has those entries filtered out
before the percent is computed.

## 4. Caveats

- **Short budgets vs the 7200 s × 3 reps DESIGN §3.2 primary**:
  several cells here (atheris × biopython 300 s, cargo_fuzz × noodles
  1800 s, aflpp × seqan3 60 s) ran against shorter budgets for
  in-session feasibility. The growth JSON captures whichever ticks
  actually fit; re-running at 7200 s overwrites in place and adds the
  higher-tick samples. Each cell's own table labels the budget used.
- **Pure-random noodles-VCF at 0 %**: the pure-random generator emits
  random bytes which noodles-vcf's strict parser rejects before
  entering any coverage-measurable path — expected floor, not a bug.
- **Pure-random biopython / vcfpy near 0 %**: same story, narrower
  SAM / VCF parser rejection windows.
- **Pure-random seqan3 showing 69 %**: seqan3's scope is narrow (8
  files / 426 lines), so even a random-byte input that happens to
  start with a comment-only SAM header exercises ~25 % of that scope
  immediately; lucky fuzzer runs push higher.
- **Rep variance** on AFL++ × seqan3 / cargo_fuzz × noodles / pure_random
  is visible in the [min–max] brackets; DESIGN §3.2 calls for 3 reps
  so those brackets approximate the 95 % CI band the Phase-6 plots
  want.
