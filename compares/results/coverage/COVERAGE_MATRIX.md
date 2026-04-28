# Coverage Matrix — every tool × SUT × format cell

Compact visual overview of every coverage cell that has landed measurements
under `compares/results/coverage/` (plus every BioTest run under
`coverage_notes/<sut>/<format>/biotest.md`).

One table per format. Rows = SUT, columns = tool. Cells show the final
line- or branch-coverage **mean** at the cell's own terminal tick, with a
10-block bar (each block ≈ 10 %, quarter / half / three-quarter sub-blocks
for finer granularity). For full per-tick tables + CI bands see the
sibling `ALL_SUT_COVERAGE.md`.

## Legend

| Symbol | Meaning |
|:--|:--|
| `/` | Tool does not target this SUT's language (out of scope by design — e.g. `jazzer × noodles` is Java fuzzer vs Rust SUT). |
| `—` | Cell is in-scope but not yet run. |
| `█▌▎▊░` | 10-block bar. `░░░░░░░░░░` = 0 %; `█████░░░░░` = 50 %; each block ≈ 10 %; `▎ ▌ ▊` = 25/50/75 % of a block. |
| `@<n>s×<k>r` | Final tick (s) and rep count this cell was sampled at. |
| `†` | **BioTest rows are end-of-run snapshots, not log-tick samples.** The wall time is **not** aligned to `{1, 10, 60, 300, 1800, 7200}` s the way every other tool's data is — see "§3 BioTest coverage — scale + re-run plan" below. |

Scope (per-SUT line filter) is identical across every tool in the same
row — it comes from `biotest_config.yaml: coverage.target_filters`. Line
percentages are therefore directly comparable within a row; see DESIGN
§4.5 + Appendix B for the fairness rules.

---

## 1. SAM

### 1a. Final line coverage (mean %)

| SUT ↓ / tool → | jazzer | atheris | libfuzzer | aflpp | cargo_fuzz | pure_random | biotest |
|:--|:--|:--|:--|:--|:--|:--|:--|
| **htsjdk**    | `██▌░░░░░░░` 25.47  @7200s×3r | / | / | / | / | `▎░░░░░░░░░` 2.19  @7200s×3r | `██▌░░░░░░░` 24.7 †  Run 11, 320 m |
| **biopython** | / | `█████▌░░░░` 54.40  @300s×3r  | / | / | / | `▎░░░░░░░░░` 1.84  @7200s×3r | `█████░░░░░` 49.7 †  Run 2, 44 m  |
| **seqan3**    | / | / | `█████████▊` 98.45  @7200s×3r | `███████▊░░` 79.11  @60s×3r | / | `███████▊░░` 78.30  @7200s×3r | `░░░░░░░░░░` 0.0 †  Run 1 (DESIGN scope, see §3) |

### 1b. Final branch coverage (mean %)

| SUT ↓ / tool → | jazzer | atheris | libfuzzer | aflpp | cargo_fuzz | pure_random | biotest |
|:--|:--|:--|:--|:--|:--|:--|:--|
| **htsjdk**    | `██░░░░░░░░` 21.20  @7200s×3r | / | / | / | / | `░░░░░░░░░░` 0.75  @7200s×3r | n/a † (JaCoCo line-only in notes) |
| **biopython** | / | `█████░░░░░` 50.42  @300s×3r  | / | / | / | `░░░░░░░░░░` 0.89  @7200s×3r | n/a † (coverage.py line-only in notes) |
| **seqan3**    | / | / | `█████▊░░░░` 57.29  @7200s×3r | `████▌░░░░░` 44.65  @60s×3r | / | `████▎░░░░░` 43.19  @7200s×3r | n/a † |

### 1c. SAM cell metadata (rep min – max, source)

| Cell | Line [min – max] | Branch [min – max] | Budget × reps | growth_aggregate.json |
|:--|:--:|:--:|:--:|:--|
| jazzer × htsjdk × SAM       | 25.10 – 25.84 | 20.88 – 21.51 | 7200 s × 3 | `jazzer/htsjdk_sam/growth_aggregate.json` |
| atheris × biopython × SAM   | 53.86 – 54.95 | 44.27 – 56.56 |  300 s × 3 | `atheris/biopython/growth_aggregate.json` (short-regime) |
| libfuzzer × seqan3 × SAM    | 97.79 – 98.90 | 55.18 – 61.53 | 7200 s × 3 | `libfuzzer/seqan3/growth_{0,1,2}.json` (aggregate stale, 3 reps landed; means recomputed here) |
| aflpp × seqan3 × SAM        | 79.11 – 79.11 | 44.43 – 44.88 |   60 s × 3 | `aflpp/seqan3/growth_aggregate.json` (short-regime) |
| pure_random × htsjdk × SAM  |  1.90 –  2.49 |  0.71 –  0.80 | 7200 s × 3 | `pure_random/htsjdk_sam/growth_aggregate.json` |
| pure_random × biopython × SAM |  0.53 –  3.15 |  0.02 –  1.76 | 7200 s × 3 | `pure_random/biopython/growth_aggregate.json` |
| pure_random × seqan3 × SAM  | 69.19 – 87.42 | 36.34 – 50.05 | 7200 s × 3 | `pure_random/seqan3/growth_aggregate.json` |
| biotest × htsjdk × SAM      | 21.0 / 21.9 / 24.7 (Runs 9/10/11) | — | non-tick, 225/402/320 m wall | `coverage_notes/htsjdk/sam/biotest.md` |
| biotest × biopython × SAM   | 44.0 / 49.7 / 49.7 (Runs 1/2/4)  | — | non-tick,  14/44/57 m wall  | `coverage_notes/biopython/sam/biotest.md` |
| biotest × seqan3 × SAM      | 0.0 (DESIGN scope) — harness 95.3 % | — | non-tick, 30 m wall | `coverage_notes/seqan3/sam/biotest.md` |

---

## 2. VCF

### 2a. Final line coverage (mean %)

| SUT ↓ / tool → | jazzer | atheris | libfuzzer | aflpp | cargo_fuzz | pure_random | biotest |
|:--|:--|:--|:--|:--|:--|:--|:--|
| **htsjdk**  | `███▌░░░░░░` 35.13  @7200s×3r | / | / | / | / | `▎░░░░░░░░░` 1.49  @7200s×3r | `████▊░░░░░` 46.9 †  Run 6, 170 m |
| **vcfpy**   | / | `█████▌░░░░` 55.01  @7200s×3r | / | / | / | `▎░░░░░░░░░` 2.72  @7200s×3r | `███████▎░░` 73.4 †  Run 1, 80 m  |
| **noodles** | / | / | / | / | `██▎░░░░░░░` 22.72 @1800s×3r | `░░░░░░░░░░` 0.00  @7200s×3r | `████░░░░░░` 39.6 †  Run 12, 64 m |

### 2b. Final branch coverage (mean %)

| SUT ↓ / tool → | jazzer | atheris | libfuzzer | aflpp | cargo_fuzz | pure_random | biotest |
|:--|:--|:--|:--|:--|:--|:--|:--|
| **htsjdk**  | `███░░░░░░░` 30.98  @7200s×3r | / | / | / | / | `░░░░░░░░░░` 0.35  @7200s×3r | n/a † |
| **vcfpy**   | / | `████▌░░░░░` 44.85  @7200s×3r | / | / | / | `░░░░░░░░░░` 0.67  @7200s×3r | n/a † |
| **noodles** | / | / | / | / | `░░░░░░░░░░` 0.00 @1800s×3r | `░░░░░░░░░░` 0.00  @7200s×3r | n/a † |

### 2c. VCF cell metadata

| Cell | Line [min – max] | Branch [min – max] | Budget × reps | growth_aggregate.json |
|:--|:--:|:--:|:--:|:--|
| jazzer × htsjdk × VCF       | 34.85 – 35.42 | 30.53 – 31.43 | 7200 s × 3 | `jazzer/htsjdk_vcf/growth_aggregate.json` |
| atheris × vcfpy × VCF       | 54.97 – 55.06 | 44.48 – 45.22 | 7200 s × 3 | `atheris/vcfpy/growth_aggregate.json` |
| cargo_fuzz × noodles × VCF  | 22.42 – 23.01 |  0.00 –  0.00 | 1800 s × 3 | `cargo_fuzz/noodles/growth_aggregate.json` (short-regime; branch = 0 is llvm-cov limitation, not true zero) |
| pure_random × htsjdk × VCF  |  1.44 –  1.54 |  0.26 –  0.45 | 7200 s × 3 | `pure_random/htsjdk_vcf/growth_aggregate.json` |
| pure_random × vcfpy × VCF   |  2.72 –  2.72 |  0.67 –  0.67 | 7200 s × 3 | `pure_random/vcfpy/growth_aggregate.json` |
| pure_random × noodles × VCF |  0.00 –  0.00 |  0.00 –  0.00 | 7200 s × 3 | `pure_random/noodles/growth_aggregate.json` |
| biotest × htsjdk × VCF      | 46.9 / 48.0 / 47.6 (Runs 6/7/8) | — | non-tick, 170/330/267 m wall | `coverage_notes/htsjdk/vcf/biotest.md` |
| biotest × vcfpy × VCF       | 73.4 (Run 1)                    | — | non-tick, 80 m wall | `coverage_notes/vcfpy/vcf/biotest.md` |
| biotest × noodles × VCF     | 39.6 (Run 12)                   | — | non-tick, 64 m wall | `coverage_notes/noodles/vcf/biotest.md` |

---

## 3. BioTest coverage — scale + re-run plan

**The seven BioTest cells above are not measured on the same time axis
as the other tools.** `coverage_notes/<sut>/<format>/biotest.md` records
*end-of-Phase-D* line coverage (JaCoCo / coverage.py / gcovr / llvm-cov),
not a tick-sampled growth curve. Wall times vary from 14 min (biopython
Run 1) to 402 min (htsjdk/SAM Run 10) — nowhere near the uniform
`{1, 10, 60, 300, 1800, 7200}` s grid the other tools share.

### 3a. What the BioTest numbers mean (as recorded today)

| SUT × format | run(s) with data | final line % | wall time (run)    |
|:--|:--|:--|:--|
| htsjdk × SAM     | 9, 10, 11       | 21.0 / 21.9 / **24.7** | 225 / 402 / 320 m |
| htsjdk × VCF     | 6, 7, 8         | 46.9 / 48.0 / 47.6   | 170 / 330 / 267 m |
| biopython × SAM  | 0, 1, 2, 3, 4   | 0 † / 44.0 / **49.7** / aborted / 49.7 | — / — / 44 / 7 / 57 m |
| vcfpy × VCF      | 1               | **73.4**             | 80 m |
| seqan3 × SAM     | 1               | 0.0 (DESIGN scope) ‡ | 30 m |
| noodles × VCF    | 12              | **39.6**             | 64 m |

† Run 0 on biopython was a Windows path-sep collector bug (filter
dropped everything); fixed in the re-filtered Run 1. See
`coverage_notes/biopython/sam/biotest.md` §Bug found & fixed.

‡ Run 1 on seqan3 ran Phase D, but the BioTest harness doesn't link the
seqan3 in-tree `sam_file_input` on the host toolchain, so the
DESIGN-scope numerator is structurally 0/0. Harness-level coverage on
the standalone text parser is 95.3 % (161/169). Rebuilding the harness
inside `biotest-bench:latest` against the image-baked seqan3 would
unblock this; see `coverage_notes/seqan3/sam/biotest.md` §Structural
zero.

### 3b. Why this matters for fair comparison

Every baseline tool's 7200 s × 3 reps row answers:

> *"Given a 2-hour budget, with three seeds, what line coverage
>    ceiling does this tool reach?"*

BioTest's rows today answer:

> *"Given a Phase-D loop that stops on plateau / timeout, what line
>    coverage did the particular run produce?"*

These are different questions. The second number **cannot** be plotted
on the same `t_s` axis as the first, and using it as the 7200-s column
entry for BioTest would silently fold two confounders together: (i) a
different saturation criterion, (ii) a different wall time.

### 3c. What a BioTest re-run needs to produce tick-aligned growth

To fill in the `@300s / @1800s / @7200s` columns for BioTest, one of the
following two changes is required:

**Option A — wrap BioTest in `coverage_sampler.py`** (minimal code change).
Invoke the existing sampler with `--tool biotest` and the same
`--budget 7200 --reps 3 --ticks 1,10,60,300,1800,7200`. The sampler
already does tick-level snapshots via the language-native coverage
backend; the gap is that `compares/scripts/tool_adapters/run_biotest.py`
doesn't emit per-tick coverage yet — it only reports final
`coverage_artifacts/` after `biotest.py` exits. The adapter would need
a poll loop that re-runs `measure_coverage.py` at each tick against the
accumulating corpus (same as the libFuzzer adapter does via its
live-corpus coverage replay).

- Pro: same tooling, same ticks, same scope, same CI recipe.
- Con: biotest's Phase C bootstrap alone takes 2–5 minutes (LLM Phase B
  mine + spec ingest + seed indexing), so ticks `{1, 10, 60}` will
  register as 0 and rendering will look wrong for short regimes. The
  300 / 1800 / 7200 ticks are usable.
- Action: implement a `_tick_snapshot()` hook in `run_biotest.py` that
  calls `measure_coverage.py` on the live
  `coverage_artifacts/.coverage` / JaCoCo / gcda at each tick; at t_s
  milestones, write one `{t_s, line_pct, branch_pct}` row to
  `growth_<rep>.json` matching the DESIGN §4.5 schema.

**Option B — instrument Phase D to emit its own tick samples**
(in-process). Inside `LoopController` (the Phase-D feedback loop), after
each iteration's coverage collection, check wall clock against the
configured ticks and write a row. This is closer to how biotest already
works (iteration-level coverage history is already persisted in
`IterationState.coverage_history`) but needs a time-aware bridge.

- Pro: no subprocess restart per tick; lower overhead; captures the
  real Phase-D growth curve.
- Con: biotest.py changes, not purely a comparison-harness change.
  Requires Phase D to keep running for 7200 s (currently plateau-
  terminates — see htsjdk/VCF §3 Plateau termination).

**Recommended**: Option A. Time-box it to ≤ 1 day of adapter work; then
re-run the six BioTest × SUT × format cells at 7200 s × 3 reps. Expected
wall cost ≈ 6 cells × 7200 s × 3 reps / 4-way parallel ≈ **11 h**.

After the re-run, this file's BioTest columns become directly
comparable to every other column (no `†` marker needed).

---

## 4. Cross-tool saturation note

Line coverage saturates very differently across tools on the same SUT.
For example on **seqan3 × SAM (7200 s × 3 reps)**:

| tick (s) | libfuzzer mean | aflpp mean | pure_random mean |
|:--:|:--:|:--:|:--:|
| 1    | 82.51 | 77.70 | 25.44 |
| 10   | 87.86 | 79.11 | 25.44 |
| 60   | 91.88 | 79.11 | 25.44 |
| 300  | 94.25 | —     | 39.84 |
| 1800 | 96.62 | —     | 59.37 |
| 7200 | **98.45** | — | **78.30** |

(aflpp was run at short-regime 60 s only — if re-run at 7200 s it
would continue past the 79.11 point, presumably toward libfuzzer's
98 % asymptote.)

The "**pure_random catches up at 7200 s**" pattern on seqan3 is
documented in `ALL_SUT_COVERAGE.md` §4: seqan3's scope is narrow (8
files / 426 lines) so random bytes that happen to produce a valid
SAM header exercise ~25 % immediately, and lucky reps push much
higher. On every other SUT (htsjdk, biopython, vcfpy, noodles),
pure_random flatlines near 0–3 %.

For the corresponding VCF comparison on **htsjdk × VCF (7200 s × 3 reps)**:

| tick (s) | jazzer mean | pure_random mean |
|:--:|:--:|:--:|
| 1    | 0.00  | 1.46 |
| 10   | 31.37 | 1.46 |
| 60   | 33.65 | 1.46 |
| 300  | 34.86 | 1.46 |
| 1800 | 35.04 | 1.46 |
| 7200 | **35.13** | **1.49** |

jazzer saturates near 35 % by t = 60 s — the seed corpus carries most
of the reachable VCF surface, and later fuzzing adds only a few
branches. Adding BioTest at tick-aligned 7200 s would let us say
whether BioTest × htsjdk × VCF at Run 6 (46.9 %, end-of-Phase-D)
is actually dominating jazzer's 35.13 % or whether the 12 pp gap is
inflated by the different stopping criterion.

---

## 5. Caveats

- **Short-regime cells.** aflpp × seqan3 (60 s), atheris × biopython
  (300 s), cargo_fuzz × noodles (1800 s) were sampled below the
  DESIGN §3.2 primary 7200 s × 3 reps; their "final" values are
  lower-bound estimates, not the saturated ceiling.
- **pure_random × noodles = 0.00 %.** noodles-vcf's strict parser
  rejects random bytes before they enter any coverage-measurable
  line — this is the expected floor, not a bug.
- **libfuzzer × seqan3 `growth_aggregate.json` is stale.** It says
  `reps: 1` from when rep 0 first landed; rep 1 and rep 2 landed
  later but the aggregator wasn't re-run. All three per-rep files
  are present; the mean shown in §1 (98.45) is recomputed here from
  the three growth_{0,1,2}.json files directly. Re-running
  `build_coverage_report.py` will refresh the aggregate on disk.
- **cargo_fuzz branch % = 0.** llvm-cov on the fuzz-instrumented
  Rust binary does not emit branch counters in our current recipe —
  the 0 means "not measured", not "zero branches covered". Line
  coverage is the usable signal.
- **Branch coverage unavailable for some tools via the current
  aggregator.** jazzer (JaCoCo) reports both; coverage.py reports
  both; gcovr reports both; cargo-llvm-cov reports line only in the
  current pipeline. Compare branch rows only where both sides have
  a non-zero reading.
- **BioTest rows (†).** See §3 — end-of-run, not tick-aligned. Do
  not treat as directly comparable to baseline tools' 7200-s values
  until a tick-aligned re-run per §3c lands.

---

## 6. Data sources

- Baseline tool cells: `compares/results/coverage/<tool>/<cell>/growth_aggregate.json`
  (or per-rep `growth_{0,1,2}.json` where the aggregate is stale).
- BioTest cells: `coverage_notes/<sut>/<format>/biotest.md` timelines.
- Scope filters: `biotest_config.yaml: coverage.target_filters`.
- Methodology: `DESIGN.md` §4.5 + Appendix B;
  `compares/scripts/measure_coverage.py`, `compares/scripts/coverage_sampler.py`.
- Per-tick / per-rep narrative: `ALL_SUT_COVERAGE.md` (this file's
  long-form sibling).
