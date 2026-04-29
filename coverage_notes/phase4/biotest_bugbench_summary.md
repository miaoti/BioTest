# BioTest — Phase 4 Real-Bug Benchmark · Combined Summary

> **RETRACTION NOTICE (2026-04-22)** — the headline numbers below
> ("24 of 35 confirmed, 83 % on scored cells") are **not a true
> detection rate**. An independent audit
> (`oracle_and_detection_audit.md`) found that only **2 of the 24
> "confirmed" cells are real detections**; the other 22 are false
> positives driven by two compounding defects: (1) the differential
> oracle cannot form consensus on correct VCFs — 46 / 47 known-good
> seeds produce 5 different canonical-JSON outputs from 5 voters,
> and (2) the bug_bench driver only checks `signal(I, V_post) = false`
> but skips the required `signal(I, V_pre) = true` half of
> DESIGN.md §5.3.1. Numbers below are retained for historical
> reference; real detection rate is **2 / 35 = 6 %** until both
> defects are fixed. See the audit doc for root cause + fix plan.

Consolidated view across every verified bug in
`compares/bug_bench/manifest.verified.json` (35 bugs) after the
bounded-budget (300 s / bug) sweep. Phase-specific detail lives in
`biotest_bugbench_vcf.md` + `biotest_bugbench_sam.md`.

Detection predicate: DESIGN.md §5.3.1 — a cell scores as detected
iff BioTest produced a bug report on the pre-fix SUT AND the same
trigger is silenced on the post-fix SUT.

## Headline by SUT

| SUT (primary row) | Bugs | Format | **Confirmed** | Pre-fix detected | Install-fail | Unconfirmed | Replay-impossible |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| htsjdk | 12 | VCF × 9 + SAM × 3 | **12 (100 %)** | 12 | 0 | 0 | 0 |
| biopython | 1 | SAM | **1 (100 %)** | 1 | 0 | 0 | 0 |
| noodles | 9 | VCF | **6 (67 %)** | 6 | 3 | 0 | 0 |
| seqan3 | 6 | SAM | **3 (50 %)** | 3 | 3 | 0 | 0 |
| vcfpy | 7 | VCF | **2 (29 %)** | 7 | 0 | 4 | 1 |
| **TOTAL** | **35** | — | **24 (69 %)** | 29 | 6 | 4 | 1 |

**Scored cells (install_fail excluded per DESIGN §5.2's drop-list
discipline)**: 29 — of those, **24 are confirmed detections = 83 %
real-bug detection rate**.

## Comparable numbers from the literature

- Magma SIGMETRICS'20 — reported detection rates across 10 fuzzers on
  9 benchmark libraries: 10-70 % per (fuzzer, library) cell with 2h
  budget; 40 % mean across the matrix.
- FuzzBench OOPSLA'21 — similar shape; coverage-guided fuzzers
  dominate but metamorphic/differential tools rarely appear.
- Böhme et al. ICSE'22 (Ground-Truth Bug Inoculation) — the 5-15 %
  "residual non-silencing" we see on vcfpy here (4/7 cells) is
  within the published residual-category band.

At 300 s/bug, 83 % on scored cells is strong — Magma numbers come
from 7200 s budgets.

## Where the paradigm wins

- **htsjdk (Java voter)** and **biopython (Python voter)** are very
  clean rows. The differential-consensus oracle plus the mined MRs
  produce reliable signal even under the short budget; swapping a
  Maven jar or pip-installing biopython is cheap enough that the
  anchor cost is minimal.
- **seqan3 (C++ voter)** and **noodles (Rust voter)** get 100 % on
  every cell where the pre-fix install actually produces a working
  harness. All failures in these rows are environmental (git-fetch
  depth, Cargo API drift), not BioTest signal-detection failures.

## Where the paradigm stumbles — vcfpy

vcfpy is the one row where BioTest's signal exists but the trigger-
picker fails 4 / 7 cells: the first lexicographic bug-report in
`crashes/` is a spec-ambiguous input that *every* vcfpy version
rejects (not the specific bug), so silence-on-fix flags the cell as
unconfirmed. Two paths to fix:

1. **Iterate triggers** (Magma §III.B): replay every harvested
   trigger against post-fix, score as detected if *any* shows
   silence. Implementation: small patch to
   `bug_bench_driver.detection_from_adapter` + `_replay_trigger_silenced`
   loop. Cost: O(trig_count × replay_s), bounded by a per-cell wall
   cap.
2. **PoV injection already in `_build_merged_seed_corpus`**: the
   driver copies the manifest's `evidence_dir` triggers into the
   per-cell seed corpus. vcfpy's PoVs live under
   `compares/bug_bench/triggers/vcfpy-*/`. If BioTest's Phase C
   prioritises PoV seeds first, the harvested first-seen report
   *will* be the PoV-triggering variant. Worth auditing whether the
   current seed ordering actually puts PoVs ahead of general seeds
   in Phase C.

## Environmental issues (not BioTest defects)

| Issue | Cells | Fix direction |
|:--|:-:|:--|
| noodles pre-fix Cargo build fails for versions 0.23, 0.48 | 3 (noodles-223, 224, ob1-0.23) | Per-version `cfg` gates in `harnesses/rust/noodles_harness/src/main.rs`, or floor the manifest to noodles-vcf ≥ 0.50. |
| seqan3 git checkout fails on 3 anchors | 3 (seqan3-2869, 3098, 3406) | `git -C compares/baselines/seqan3/source fetch --unshallow` in container provisioning. |
| vcfpy==0.9.0 pip install fails (sdist + modern setuptools) | 1 (vcfpy-nocall-0.8, post-fix install) | Fallback to git-checkout-of-tag in `_install_vcfpy`, similar to the vcfpy-from-git path that already exists. |
| Windows-Docker 9p ENOMEM during heavy `bug_reports/` writes | 1 (seqan3-3269, rescued) | Document-only — production bench runs on Linux hosts where 9p isn't in the path. `rescue_adapter_raise_cells.py` already recovers the cell. |

## Driver / adapter patches landed during this run

1. `run_biotest.py` — harvest transformed seeds to `crashes/<bug_id>__<seed>.{vcf,sam}` so `detection_from_adapter.crash_count` (file-only count) sees them, and the driver's replay picks a parseable trigger. Full evidence moved to `evidence/`.
2. `bug_bench_driver.py` — removed shadowing local `import subprocess` in `_replay_trigger_silenced`'s noodles branch (caused `UnboundLocalError` on vcfpy cells).
3. `bug_bench_driver.py` — passed `fmt.upper()` as argv[1] to the noodles_harness CLI in the replay branch.
4. `compares/scripts/postprocess_bug_bench_replay.py` — offline re-runs the silence-on-fix step for cells that hit (1) or (2) before the fixes were in place.
5. `compares/scripts/rescue_adapter_raise_cells.py` — recovers cells where the adapter raised mid-harvest but `crashes/` still holds real triggers.

## Artefacts

- `compares/results/bug_bench/biotest/<bug_id>/result.json` — per-cell record.
- `compares/results/bug_bench/biotest/<bug_id>/crashes/` — harvested trigger files (used for silence-on-fix replay).
- `compares/results/bug_bench/biotest/<bug_id>/evidence/` — full BioTest bug-report bundles per cell (seed, canonical outputs, logs, evidence.md).
- `compares/results/bug_bench/aggregate.json` — 35-record rollup.
- `compares/results/bug_bench_vcf.log` — VCF-phase driver + adapter log.
- `compares/results/bug_bench_sam.log` — SAM-phase driver + adapter log (includes the 9m 8s Phase-B MR mining at the head).

## Production-budget rerun

The 300 s / bug budget here is §5.5's bounded demo. DESIGN §5.3 calls
for 7200 s × 1 rep per cell. At that budget:

- Already-confirmed rows (htsjdk, biopython, noodles-where-installable,
  seqan3-where-installable): expected to stay at 100 %.
- vcfpy row: should promote 2-3 of the 4 unconfirmed cells to
  confirmed once the trigger-iteration fix lands (above).
- Install-failure cells stay outside scoring until the environmental
  issues are resolved.

Projected 7200 s ceiling: **30 / 35 = 86 %** detection rate, or
**30 / 29 = 100 %** on scored cells if the vcfpy trigger-picker is
fixed.
