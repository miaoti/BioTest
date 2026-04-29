# BioTest — Phase 4 Real-Bug Benchmark · Final Audit-Corrected Report

This document closes the arc of the Phase 4 oracle-fix sprint
(2026-04-21 → 2026-04-22). It supersedes the earlier headline in
`biotest_bugbench_summary.md` that carried a `[RETRACTION]` notice.

## TL;DR — the three numbers

| Measurement | htsjdk | biopython | noodles | seqan3 | vcfpy | **TOTAL** |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| **Pre-fix run (v2, flawed oracle)** | 12/12 | 1/1 | 6/9 | 3/6 | 2/7 | **24/35 (69 %)** |
| **Independent audit (per-cell V_pre replay)** | 0/12 | 0/1 | 0/9 | 0/6 | 2/7 | **2/35 (6 %)** |
| **Post-fix rerun (v4 VCF + v2 SAM)** | 0/12 | 0/1 | 0/9 | 0/6 | 2/7 | **2/35 (6 %)** ✓ |

The rerun reproduces the audit number to the cell. The driver now
enforces both halves of DESIGN.md §5.3.1's detection predicate —
`signal(I, V_pre) = true AND signal(I, V_post) = false` — so the
22 false positives the audit exposed are now demoted at scoring
time instead of requiring an offline re-scoring pass.

## What we actually found

Two real bugs, both on vcfpy (0.13.8 → 0.14.0):

| bug_id | anchor | category | evidence |
|:--|:--|:--|:--|
| vcfpy-171 | 0.13.8 → 0.14.0 | incorrect_field_value | pre-fix raises, post-fix parses cleanly; trigger in `compares/results/bug_bench/biotest/vcfpy-171/crashes/` |
| vcfpy-176 | 0.13.8 → 0.14.0 | incorrect_field_value | same pattern |

These are genuine detections. Pre-fix vcfpy 0.13.8 raises a Python
exception on the harvested trigger; vcfpy 0.14.0 parses it without
error. The differential path through BioTest's voter pool surfaces
these because vcfpy's parse-time exception is a clear subprocess-
returncode signal that doesn't depend on canonical-JSON equality.

## Why every other row is 0 / N

The pre-fix "confirmed" cells on htsjdk / biopython / noodles /
seqan3 / the other vcfpy cells were all flagged because BioTest
wrote bug_reports for them — but the bug_reports were
**canonical-JSON disagreements on spec-valid input** that every
SUT version parsed without error. When the driver's corrected
`_replay_trigger_silenced(sut, trig, "pre_fix")` step runs the
harvested trigger against the pre-fix SUT binary, the pre-fix SUT
succeeds. Per §5.3.1, without `signal(I, V_pre) = true` there is
no bug to silence — the cell is correctly demoted to
`detected=False` with an explanatory note on `result.json`.

## Breakdown by status

### Demoted by pre-fix-failure check (zeroed false positives)
- htsjdk (VCF + SAM): 9 demoted
- biopython/SAM: 1 demoted
- noodles/VCF: 6 demoted
- seqan3/SAM: 1 demoted
- **Total: 17 cells** — all would have scored `confirmed=True`
  under the old driver; now correctly show `detected=False`.

### Detected but unconfirmed (§5.3.1 null_silences)
- htsjdk/SAM: 3 cells (1489, 1538, 1561). Pre-fix htsjdk does fail
  on the trigger (real parse-path crash) **and** post-fix also
  fails. The spec-ambiguous trigger exercises a bug path in every
  htsjdk 2.x + 3.0.x minor the manifest references — not the
  specific issue the manifest anchors on.
- vcfpy/VCF: 4 cells (127, 145, 146, gtone-0.13). Same pattern —
  real pre-fix crash but post-fix also rejects. The manifest's
  anchor bug is a subtle field-value change; the harvested
  trigger happens to ALSO exercise vcfpy's general-purpose
  header/record validation, which raises on both the pre-fix and
  post-fix versions.

### Detected and replay-impossible (§5.3.1 `null`)
- vcfpy-nocall-0.8: post_fix=0.9.0 pip install fails (sdist build
  error against modern setuptools). Driver records
  `confirmed=None`; no claim made.

### Install-failed (excluded from scoring)
- noodles/VCF: 3 cells (223, 224, ob1-0.23) — pre-fix Cargo build
  fails against harness API
- seqan3/SAM: 5 cells — rebuild times / git-fetch depth issues.
  Logged under environmental gaps in `biotest_bugbench_sam.md`.

## What this means for the paradigm

The audit + rerun expose an honest truth: **BioTest's
differential/metamorphic oracle is currently only strong enough
to detect bugs that manifest as a parse-time exception visible to
a subprocess wrapper**. On the 35-bug manifest, that's a clean 2
detections on vcfpy.

The oracle was NOT detecting:
- Bugs that change field values but leave the parse tree structure
  intact (BioTest strict-mode bucketing only compares variant
  identity fields CHROM+POS+REF+ALT)
- Bugs that affect unparsed-by-all-voters inputs (the cell's
  harvested trigger would need to differentiate pre/post-fix on at
  least ONE parseable voter pair — rare for spec-violation bugs)
- Bugs inside the data-model API surface (query methods on
  post-parse objects — Rank 5/6 levers, out of scope here)

This matches the **published band** for pure file-level
differential oracles on parser libraries (Liyanage & Böhme ICSE'23
report ~20-40 % on the cleaner MAGMA corpora; our narrower 35-bug
manifest with a 300 s budget + broken-until-now canonicaliser
lands below that). Progress targets would be:

1. **Trigger iteration per §III.B of MAGMA** — iterate every
   harvested bug_report until one satisfies §5.3.1, not just the
   first. Would promote the 7 `null_silences` cells if any of
   their triggers genuinely silence on post-fix. Cost: O(trig
   count × replay wall time) per cell.
2. **Semantic-level oracle (Rank 5 mutator-method MRs)** — after
   parsing, call query methods on the parsed records and check
   cross-voter agreement. This is the lever that reaches
   data-model bugs the strict-bucket oracle can't see today.
3. **Production-budget rerun (§5.5: 7200 s × 1)** — 24× the
   current budget lets the corpus drift into genuine bug
   territory. The 2 vcfpy real detections landed inside 300 s
   because the harvest-first-trigger heuristic happened to land
   on a PoV-like input; longer budget lets the corpus accumulate.

## Artefacts landed this sprint

- `test_engine/canonical/post_normalize.py` — per-voter
  canonicalisation fix-pack
- `test_engine/oracles/tolerance.py` — strip_to_strict drops
  whole-header + narrows VCF record to variant-identity fields
- `harnesses/java/BioTestHarness.java` — `Allele.getDisplayString`
  harness fix (+ rebuild via `harnesses/java/build.sh`)
- `test_engine/runners/pysam_runner.py` — POS off-by-one removed,
  GT phase reconstruction from `phased` flag
- `compares/scripts/bug_bench_driver.py` — pre-fix-failure check
  in the main loop (§5.3.1 left-hand side); dropped shadowing
  local `import subprocess`; noodles replay CLI arg fix
- `compares/scripts/tool_adapters/run_biotest.py` — crashes_dir
  harvest counts directories, transformed seeds land as parseable
  triggers
- `compares/scripts/postprocess_bug_bench_replay.py`,
  `rescue_adapter_raise_cells.py` — offline recovery of pre-fix
  runs hit by the above bugs
- `scripts/validate_oracle_on_correct_vcfs.py`,
  `validate_oracle_on_correct_sams.py`,
  `classify_oracle_divergences.py`,
  `dump_voter_canonicals.py`,
  `audit_phase4_detections.py` — validation infrastructure
- `coverage_notes/phase4/*.md` — documentation chain:
  - `biotest_bugbench_vcf.md` — original VCF phase writeup (carries
    retraction)
  - `biotest_bugbench_sam.md` — original SAM phase writeup (carries
    retraction)
  - `biotest_bugbench_summary.md` — original combined summary
    (carries retraction)
  - `oracle_and_detection_audit.md` — what the audit found
  - `post_oracle_fix_rerun.md` — per-cell post-fix run detail
  - `final_audit_report.md` (this file) — single canonical number

## Oracle validation evidence

| Metric | Before fix-pack | After fix-pack |
|:--|:-:|:-:|
| VCF seeds with cross-voter consensus (≥ 2 voters agree) | 1 / 47 (2 %) | **46 / 47 (98 %)** |
| VCF seeds where every voter is in its own bucket | 46 / 47 (98 %) | **0 / 47** |
| SAM seeds with consensus | 39 / 72 (54 %) | **58 / 72 (81 %)** |
| SAM seeds oracle-blind | 14 / 72 (19 %) | **0 / 72** |
| Phase-4 false-positive rate | 22 / 24 confirmed (92 %) | **0 / 2** |

The oracle now actually works. The detection rate is honest at
2 / 35 = 6 %. Every method for pushing that number up is
documented in the "progress targets" section above.
