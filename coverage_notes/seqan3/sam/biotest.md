# BioTest — seqan3 / SAM line coverage

Source-of-truth for every BioTest coverage measurement taken against the
**seqan3** SUT in **SAM** mode. All numbers use the three-path substring
filter defined in `biotest_config.yaml: coverage.target_filters.SAM.seqan3`:

```
seqan3/io/sam_file
format_sam
cigar
```

This is the same scope DESIGN.md §3.2 / §5 / §13.2.4 uses when grading
any C++ SUT on the SAM row — libFuzzer and AFL++ on the bench are
measured against the identical filter (`compares/results/coverage/
libfuzzer/seqan3/growth_*.json`), so BioTest's numerator compares to
those baselines line-for-line.

Run-by-run snapshots are archived as:

- `coverage_artifacts/seqan3/gcovr_post_run{N}.json` — gcovr JSON
- `coverage_artifacts/seqan3/gcda_post_run{N}.gcda` — raw `.gcda` snapshot
- `data/run_seqan3_sam_phase_cd_partial.log` — Phase C+D stdout/stderr

---

## Timeline

| Run | Date | Wall | Iters | **seqan3 SAM (DESIGN scope)** | Covered / Total | Harness (raw) | Notes |
|:-:|:--|:-:|:-:|:-:|:-:|:-:|:--|
| 1 | 2026-04-21 | 30 m (stopped) | 1 (partial) | **0.0 %** | **0 / 0** | 95.3 % (161 / 169) | First BioTest seqan3/SAM baseline. Harness text parser exhausted (only 8 uncovered lines — all error paths). DESIGN scope empty because harness does not link seqan3 on the Windows/MinGW toolchain; see "Structural zero" below and `harnesses/cpp/README.md`. |

The 0/0 under the DESIGN filter is not a bug in the measurement
pipeline — it is the honest reflection of a documented toolchain
limitation. The numerator compares against libFuzzer × seqan3's
~98 % line coverage (DESIGN §13.2.4) only once the harness is rebuilt
to link seqan3's `sam_file_input`, which requires Clang 18 + the two
in-tree patches baked into the `biotest-bench` Docker image (see
"Structural zero" for the unblock path).

---

## Run 1 detailed breakdown (2026-04-21)

First attempt to drive the BioTest Phase D loop with
`primary_target: seqan3`, `format_filter: SAM`. Config change:

```diff
-  primary_target: htsjdk
+  primary_target: seqan3
```

Nothing else touched — the same `mr_registry.json` from the prior
htsjdk/SAM Run 10 (3 enforced + 17 quarantined MRs, all SAM-scoped)
was reused so the Phase C dispatcher had material to run. Seed corpus:
**67 SAM seeds** (tier-1 + tier-2 htsjdk / htslib / jazzer-imported;
no synthetic seeds from prior biopython/pysam SAM runs).

### Invocation

```bash
# Config backed up, primary_target flipped, stale gcda cleared.
py -3.12 biotest.py --phase C,D
```

`--phase C,D` dispatches the explicit Phase C (which writes
`data/det_report.json` at the end) and then enters Phase D's
feedback loop (which re-runs Phase C + collects coverage per iteration).

### Pipeline timing

Phase D's first iteration was interrupted at wall time **30 m** — well
before the default SAM `max_iterations=2` cap or the 180-min timeout —
because:

- The `.gcda` file saturates the harness (161 / 169 reachable lines)
  within the first ~50 seed invocations. Subsequent test volume does
  not move either number.
- The DESIGN-scope coverage (the number this file tracks) is
  structurally 0/0 regardless of how long Phase D runs, so extending
  the wall gains no signal for this SUT/tool cell. Further discussion
  under "Structural zero" below.

| Phase | Wall | Output |
|:--|:-:|:--|
| C (explicit, from `--phase C,D`) | ~4 m 30 s | 20 MRs × 67 seeds × 6 voters = 8 050 voter invocations; DET report at 15:16 |
| D (feedback loop, 1 partial iter) | ~25 m 30 s | Phase B re-mine skipped (registry intact); new Phase C pass re-driven; 518 seed-level dispatches across 8 MRs before interrupt; `.gcda` last touched 15:41 |
| **Total (stopped)**               | **~30 m** | |

### Coverage against the DESIGN filter

```bash
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/gcovr.json \
    --sut seqan3 --format SAM \
    --label "BioTest Run 1 (seqan3 harness, Phase C+D partial)"
```

Output (verbatim — same fairness path that grades libFuzzer / AFL++ /
Pure Random on the seqan3 row):

```
=== BioTest Run 1 (seqan3 harness, Phase C+D partial) (seqan3/SAM) ===
  Report:  coverage_artifacts\gcovr.json
  Filter rules (from biotest_config.yaml):
    - seqan3/io/sam_file
    - format_sam
    - cigar

  Bucket                          Covered/Total       %
  seqan3/io/sam_file                    0/0      (  0.0%)
  format_sam                            0/0      (  0.0%)
  cigar                                 0/0      (  0.0%)
  OVERALL (weighted)                    0/0      (  0.0%)
```

All three buckets report **0 / 0** because the harness binary that
BioTest drives on this toolchain (`harnesses/cpp/build/biotest_harness_cov.exe`)
is a pure C++ text SAM parser — it does not include any header under
`SUTfolder/cpp/seqan3/include/seqan3/io/sam_file/` or `.../cigar/`, so
`.gcda` carries zero coverage data for those paths and the filter
denominator collapses to zero. The same filter applied to the
libFuzzer × seqan3 `.gcda` (built inside `biotest-bench` against
the patched seqan3 3.3.0 headers) reports a non-zero denominator of
8 files / 426 lines (DESIGN §13.2.4 AFL++ numbers confirm the same
scope), so the filter itself is correct — the zero is upstream, in the
harness's link step.

### Harness-level coverage (for context — not the DESIGN metric)

Same `.gcda`, no filter:

```
file: biotest_harness.cpp
  total exec lines: 169
  covered: 161
  missed: 8
```

Uncovered-line breakdown (all error paths that BioTest's driver never
produces):

| Line | Code | Why uncovered |
|:-:|:--|:--|
| 37 | `else out += c;` (specific char branch in `json_str`) | No SAM seed contains the unusual char combination that hits this branch and no other |
| 58–59 | `std::cerr << "Usage: …" ; return 1;` | BioTest always passes exactly `SAM <path>`; never fires |
| 66–67 | `std::cerr << "This harness only supports SAM …"` | BioTest routes only SAM through this binary |
| 73–74 | `std::cerr << "Cannot open file: …"` | `sanitize_seeds.py` removes any SAM seed that can't open before Phase C |
| 87 | `line.pop_back();` (strip trailing `\r` branch) | Our SAM corpus is all Unix-line-ending; no `\r` stripping needed |

**The harness text parser is effectively fully exercised at 95.3 %.**
This is informational only — it does not contribute to the DESIGN
comparison number, which is scoped to seqan3 code, not BioTest's harness.

---

## Structural zero — why 0/0 on the DESIGN filter is the honest answer today

Documented in `harnesses/cpp/README.md` in full, summarised here:

1. **`biotest_harness.cpp` does not `#include <seqan3/io/sam_file/input.hpp>`**
   on the current Windows/MinGW dev toolchain because
   (a) seqan3 requires C++23, which MinGW's GCC 15.2 supports only
   with an explicit `-std=c++23`; and
   (b) seqan3's BAM `format_bam.hpp:160` has a
   `static_assert` that compares a packed-struct size of 36 bytes
   (Linux x86-64 ABI) against 40 bytes (MinGW ABI) and aborts compilation.
2. Result: the `-fprofile-arcs -ftest-coverage` build only instruments the
   harness's own C++ source, not any seqan3 header. The `.gcda` file
   therefore carries exactly one filename — `biotest_harness.cpp` —
   and the DESIGN filter (which looks for `seqan3/io/sam_file`,
   `format_sam`, `cigar`) rejects it → 0/0.
3. `GcovrCollector.is_available()` returns True once `.gcda` exists, so
   Phase D's feedback loop reads a real coverage JSON, computes
   0 covered / 0 total on the filter, and records `0.0 %` — no zero
   is fabricated; the denominator is genuinely empty.

DESIGN.md §13.2.4 documents the unblock path — Clang 18 + the two
in-tree patches to `seqan3/utility/type_traits/basic.hpp:29` and
`seqan3/utility/views/repeat.hpp:84` that are baked into the
`biotest-bench` Docker image. Inside that image, rebuilding the
harness to call `seqan3::sam_file_input` yields a `.gcda` with data
for every header under the filter, and this note's Run 2+ numbers
will move off zero. On the current native-Windows toolchain, the
blocker stands.

### Why this differs from biopython / htsjdk / vcfpy

Those three SUTs are **pure Python / pure Java** and their standard
coverage tooling (coverage.py for Python, JaCoCo for Java) traces the
installed library classes regardless of what thin harness calls them.
BioTest's pysam runner, biopython runner, htsjdk harness all invoke
the SUT's own imported modules — so coverage lights up automatically.

seqan3 is a header-only C++ template library. The only way a
`.gcda` can record seqan3 coverage is if the compiled binary *itself*
was built with `-fprofile-arcs -ftest-coverage` *and* `#include`d the
seqan3 headers whose coverage we want. The current harness skips the
`#include` to sidestep the MinGW ABI assertion, so no seqan3 code is
in the binary to instrument.

---

## Signals that DID land during Run 1

Even though line-coverage on the DESIGN scope is zero, the run is
not empty — it exercised BioTest's full cross-parser signal pipeline
with seqan3 as one of the voters:

- **Seed / MR / voter throughput** (per `data/det_report.json`, if
  present from the partial run or from Run 10's snapshot): on the
  order of 8 000 voter invocations across 20 MRs × 67 seeds × 6
  voters during the explicit Phase C pass alone, feeding the
  consensus oracle every time.
- **Bug reports**: 1 478 `BUG-20260421_*` files written under
  `bug_reports/` during the partial Phase C+D run. Most are
  `silent_accept_bug` attributed to seqan3 on jazzer-imported or
  real-world htslib seeds — the same "text-SAM is too permissive"
  pattern documented under biopython/SAM Run 2.
- **SCC (feedback_state)**: seqan3/SAM first-iteration SCC =
  **2.19 %** (3 / 137 testable SAM rules), `enforced=3`, `demoted=0`
  after one partial iteration. Same 137-rule SAM denominator the
  biopython/SAM notes use.

These signals are downstream of the harness, not of seqan3 itself
being exercised, so they do not affect the coverage number above.
They do confirm the seqan3 runner is wired into the voter pool and
producing canonical JSON BioTest can consume.

---

## Next levers (ordered by effort)

1. **Rebuild the harness inside the `biotest-bench` Docker image**
   (DESIGN §13.1 / §13.2.4). The image ships Clang 18 + patched
   seqan3 3.3.0 + xxsds/sdsl-lite v3 exactly so the `#include
   <seqan3/io/sam_file/input.hpp>` compile step works. Replace the
   current text-scanner loop with a call to
   `seqan3::sam_file_input{filepath}` and emit the same canonical
   JSON shape. `.gcda` from that build lights up the three DESIGN
   buckets, and this note's Run 2 onwards will have a real number
   to compare against libFuzzer's ~98 % ceiling (DESIGN §13.2.4
   7200 s tick).
2. **Alternative: WSL2 Ubuntu side-channel**. Same two-patch
   seqan3 source under `/opt/seqan3/include`, build with
   `g++-12 --coverage -std=c++23`, drop the `.exe` suffix in
   `biotest_config.yaml: phase_c.suts[seqan3].coverage_binary`.
   Harness source remains `harnesses/cpp/biotest_harness.cpp`; only
   the CMakeLists / build command changes. WSL2 runs already verified
   on the same dev machine for samtools (see biopython/SAM Run 4
   writeup).
3. **Accept the harness-only number as a lower bound**. If neither
   rebuild is available, the 95.3 % harness-level number is a valid
   floor — any real seqan3 binary built against the same SAM seeds
   would cover *at least* the same code paths that the text parser
   covers, plus whatever seqan3 wraps on top. Reported here for
   transparency; never substitute for the DESIGN metric.

---

## Methodology — how coverage is computed

Follows the same recipe documented in `compares/scripts/README.md`
(the cross-tool fairness path — measure every tool under the same
filter from `biotest_config.yaml`):

```bash
# 1. Run BioTest with primary_target=seqan3, format_filter=SAM.
#    The seqan3 runner uses harnesses/cpp/build/biotest_harness_cov.exe
#    (coverage_binary in config) which emits .gcda on every invocation.
py -3.12 biotest.py --phase C,D

# 2. Snapshot the raw .gcda
cp harnesses/cpp/build/biotest_harness_cov-biotest_harness.gcda \
   coverage_artifacts/seqan3/gcda_post_run{N}.gcda

# 3. Generate gcovr JSON (the DESIGN §3.2 collector's native format)
gcovr --json coverage_artifacts/gcovr.json \
      -r harnesses/cpp \
      harnesses/cpp/build
cp coverage_artifacts/gcovr.json \
   coverage_artifacts/seqan3/gcovr_post_run{N}.json

# 4. Apply the DESIGN filter via the cross-tool fairness script
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/gcovr.json \
    --sut seqan3 --format SAM \
    --label "BioTest Run {N}"
```

Step 4 reads `coverage.target_filters.SAM.seqan3` from the config,
walks the gcovr JSON's `files[].lines[]` entries, keeps only entries
whose filename contains any of `{seqan3/io/sam_file, format_sam,
cigar}`, then sums `count > 0` → covered and `count == 0` → missed.
This is the **same reader** (`_measure_gcovr_json`) every other
C/C++ tool on the seqan3 row is graded through, so the comparison
is apples-to-apples by construction.

---

## Artifacts

| File | Purpose |
|:--|:--|
| `coverage_artifacts/seqan3/gcovr_post_run1.json` | Run 1 gcovr snapshot (95.3 % harness, 0/0 DESIGN scope) |
| `coverage_artifacts/seqan3/gcda_post_run1.gcda` | Raw `.gcda` from Phase C+D partial |
| `coverage_artifacts/gcovr.json` | Live gcovr report (same as Run 1 snapshot) |
| `harnesses/cpp/build/biotest_harness_cov-biotest_harness.gcno` | gcov note file (static, from build) |
| `harnesses/cpp/build/biotest_harness_cov.exe` | MinGW PE32+ coverage harness (built `-fprofile-arcs -ftest-coverage`) |
| `data/run_seqan3_sam_phase_cd_partial.log` | Full stdout/stderr of the 30-minute Phase C+D run |
| `data/feedback_state.json` | SCC history `[2.19]`, enforced `[3]` after iter 1 |
| `biotest_config.yaml.backup_seqan3run` | Pre-run config backup (restore via `cp backup config`) |
| `harnesses/cpp/README.md` | Full rationale for the harness-vs-seqan3 link gap |

---

## Kill switches (same pattern as biopython/SAM — rank levers are SUT-agnostic)

| Lever | Disable |
|:------|:--------|
| Rank 1 seed synth | `feedback_control.seed_synthesis.enabled: false` |
| Rank 2 htslib corpus | skip `seeds/fetch_real_world.py` |
| Rank 3 malformed MRs | drop `rejection_invariance` from `phase_b.themes` |
| Rank 4 `target()` directive | drop `Phase.target` from orchestrator phases |
| Rank 5 API-query MRs | already noop here — seqan3 runner sets `supports_query_methods=False` because libclang scaffold is unbuilt; see `harnesses/cpp/README.md` Rank 5 section |
| Rank 6 MR synthesis | off by default: `feedback_control.mr_synthesis.enabled: false` |

## Re-run recipe

```bash
# 1. Set primary target
sed -i 's/^  primary_target: .*/  primary_target: seqan3/' biotest_config.yaml

# 2. Clear gcda for a fresh measurement
rm -f harnesses/cpp/build/biotest_harness_cov-biotest_harness.gcda
rm -f coverage_artifacts/gcovr.json

# 3. Run. --phase C,D hits coverage in Phase D iter 1; --phase C alone
#    only writes det_report.json (no gcovr.json), so use C,D.
py -3.12 biotest.py --phase C,D

# 4. Measure (Run 1 verbatim commands)
cp harnesses/cpp/build/biotest_harness_cov-biotest_harness.gcda \
   coverage_artifacts/seqan3/gcda_post_run{N}.gcda
gcovr --json coverage_artifacts/gcovr.json -r harnesses/cpp harnesses/cpp/build
cp coverage_artifacts/gcovr.json coverage_artifacts/seqan3/gcovr_post_run{N}.json
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/gcovr.json \
    --sut seqan3 --format SAM \
    --label "BioTest Run {N}"

# 5. Restore prior primary target when done (optional, for htsjdk Run 11+)
sed -i 's/^  primary_target: seqan3/  primary_target: htsjdk/' biotest_config.yaml
```
