# BioTest — Oracle + Phase-4 Detection Audit (2026-04-22)

**TL;DR**: The previous Phase-4 writeup reported "24 of 35 confirmed
detections (69 %)". An independent audit finds **only 2 of those 24
are real detections (8 %)**. The remaining 22 are false positives —
the pre-fix SUT parses the trigger cleanly, so silence-on-fix was
vacuously satisfied. Root cause: (a) the differential oracle cannot
find consensus on known-correct VCFs (46 / 47 seeds produce zero
cross-voter agreement), and (b) the driver's detection predicate
checks only the `signal(I, V_post) = false` half of DESIGN.md
§5.3.1, skipping the required `signal(I, V_pre) = true` half.

## Part 1 — Oracle sanity check on known-correct VCFs

**Script**: `scripts/validate_oracle_on_correct_vcfs.py`. Feeds every
`seeds/vcf/*.vcf` through every available VCF voter (htsjdk, vcfpy,
pysam, noodles, reference — htslib not available in this env), buckets
each seed's outputs by canonical-JSON hash equality, and counts
consensus.

**Result** (5 voters, 47 seeds):

| Metric | Count | Percentage |
|:--|:-:|:-:|
| Seeds with a consensus of ≥ 2 voters | **1 / 47** | **2 %** |
| Seeds where every successful voter lands in its own bucket | **46 / 47** | **98 %** |
| Seeds where any voter matches the primary (noodles) | **0 / 47** | **0 %** |

For a representative input — `seeds/vcf/spec_example.vcf`, the
canonical specification example — the pairwise canonical-JSON diffs
between voters:

| Pair | Diffs |
|:--|:-:|
| noodles vs reference | 6 (top-level schema keys completely differ) |
| noodles vs vcfpy | 6 (same schema mismatch) |
| pysam vs reference | 57 (quoted-string `Description` handling + per-field `IDX`) |
| pysam vs vcfpy | 66 (same + `Number` type str vs int) |
| reference vs vcfpy | 16 (`Number` str vs int; `fileDate`/`phasing` str vs list) |

Specific structural disagreements on the spec example:

- **noodles emits Rust `Debug`-format strings**: e.g.
  `header.fileformat = "FileFormat { major: 4, minor: 3 }"` while every
  other voter normalises to `"VCFv4.3"`. Noodles also uses totally
  different top-level keys (`records_read` + `sample_count`) vs the
  others' (`records` + `samples.*`). Noodles and everyone else are
  effectively reporting different schemas — they can never agree.
- **pysam keeps CSV-`Description` values quoted**:
  `FILTER.q10.Description = '"Quality below 10"'` vs the others' bare
  `'Quality below 10'`. pysam also adds per-entry `IDX` numeric tags
  that no one else carries.
- **`Number` type inconsistency**: reference keeps `"1"`, vcfpy emits
  `1` (int), others disagree again.

The per-voter canonicalisers are independent implementations with no
shared normalization layer for VCF. On 47 / 47 seeds at least one
voter diverges; on 46 / 47 *all* voters diverge simultaneously.

**Implication**: BioTest's differential oracle fires on every VCF
seed, regardless of whether any SUT has a bug. The `differential`
branch of `orchestrator.py` that creates `bug_reports/` is being
triggered by canonicalisation drift, not by real SUT defects.

Full dump: `compares/results/oracle_validation_vcf.json`.  
Per-voter canonical dumps for `spec_example.vcf`:
`compares/results/voter_canonicals/spec_example__<voter>.json`.

## Part 2 — Manual audit of Phase-4 "confirmed" detections

**Script**: `scripts/audit_phase4_detections.py`. For each cell where
the previous writeup reported `confirmed_fix_silences_signal=True`, it
installs the **pre-fix** SUT version and runs the harvested trigger
through that SUT's runner. The detection predicate per DESIGN.md §5.3.1
is:

> `detects(T, B) := ∃ I : signal(I, V_pre) = true AND signal(I, V_post) = false`

The bug_bench driver only ever evaluated the right-hand side. The
audit fills in the left-hand side by checking whether the pre-fix SUT
actually fails on the trigger.

**Result** (24 cells audited — every confirmed cell from the original
Phase-4 run):

| Classification | Count | % of confirmed cells |
|:--|:-:|:-:|
| **real_detection** (pre-fix fails, post-fix succeeds) | **2** | **8 %** |
| **false_positive** (pre-fix parses cleanly; silence vacuous) | **22** | **92 %** |

### The 2 real detections

| bug_id | SUT | pre_fix | trigger | reason classified real |
|:--|:--|:--|:--|:--|
| **vcfpy-171** | vcfpy | 0.13.8 | `BUG-20260422_045119_943747_1__T_bcftools_test.vcf` | vcfpy==0.13.8 raises when the trigger is parsed; vcfpy==0.14.0 parses cleanly. Matches the manifest's `incorrect_field_value` category. |
| **vcfpy-176** | vcfpy | 0.13.8 | `BUG-20260422_044419_700846_1__T_bcftools_test.vcf` | Same anchor, same pattern. These are the two bugs fixed together in the vcfpy 0.14.0 release. |

Both survive because vcfpy's parse-time exception is a clear signal
(Python exception → `subprocess.run(...).returncode != 0`), so the
`signal(I, V_pre) = true AND signal(I, V_post) = false` predicate
evaluates correctly for them — bypassing the broken canonical-JSON
path that the differential oracle uses for every other cell.

### The 22 false positives

Every single htsjdk cell (9), every "confirmed" noodles cell (6),
every seqan3 cell (3), the biopython cell (1), and 4 of 7 vcfpy cells
failed the pre-fix-failure check. For all 22, **pre-fix runner.run()
returned `success=True`** — the SUT parsed the trigger without error,
meaning:

- The trigger is a structurally-valid VCF/SAM.
- Pre-fix and post-fix both accept it.
- The "detection" was pure cross-voter canonicalisation variance.
- `confirmed_fix_silences_signal=True` was meaningless because there
  was no pre-fix signal to silence.

Full per-cell audit: `compares/results/phase4_audit.json`.

## Root cause — two compounding defects

### A. The oracle is broken

Each voter has its own canonicaliser. These emit structurally
different JSON on the same input: different keys, different scalar
type encodings (str vs int vs list), different quoting conventions.
`test_engine/oracles/consensus.py` then buckets by exact-JSON
equality, which produces a new bucket per voter on essentially every
input. `test_engine/canonical/vcf_normalizer.py` is the missing
layer — it should post-process every voter's output to a common
schema before bucketing.

Phase-3 (VCF Run 6-8) and Phase-2 coverage runs worked despite this
because those metrics only score coverage counters, not oracle
verdicts. Phase-4 is the first scoring that depends on the oracle
being correct, and the defect surfaced immediately.

### B. The driver skips half of the detection predicate

`compares/scripts/bug_bench_driver.py::detection_from_adapter` marks a
cell as detected based only on `crash_count > 0` (= BioTest wrote any
bug_report). It never checks whether the **pre-fix** SUT actually
crashes on the harvested trigger. The silence-on-fix step does check
post-fix, but the right-hand side alone cannot distinguish a real bug
from cross-voter variance.

Required fix: before scoring a cell as detected, the driver must
install pre-fix SUT, re-run the trigger, confirm it fails, THEN install
post-fix and confirm silence. Both halves of §5.3.1 must evaluate to
true.

## Honest restatement of Phase-4 results

The previous writeup in `biotest_bugbench_summary.md` claimed:

> 24 of 35 real bugs detected (69 %); scored rate 24 / 29 = 83 %.

The audit-corrected numbers are:

| SUT | Bugs | Confirmed (audited) | Previous writeup (pre-audit) | Δ |
|:--|:-:|:-:|:-:|:-:|
| htsjdk | 12 | **0** | 12 | −12 |
| biopython | 1 | **0** | 1 | −1 |
| noodles | 9 | **0** | 6 | −6 |
| seqan3 | 6 | **0** | 3 | −3 |
| vcfpy | 7 | **2** | 2 | 0 |
| **TOTAL** | **35** | **2 (6 %)** | 24 (69 %) | −22 |

The only rows that produce correct detections today are those where
the pre-fix SUT raises a native parse exception the subprocess layer
can see (non-zero exit, Python exception): **vcfpy** and potentially
**pysam** (unused for VCF Phase-4). Every other row is dominated by
canonical-JSON noise that BioTest's oracle can't filter.

## What needs to change before Phase-4 is rerun

1. **Unify VCF canonicalisation across voters.** Write a
   `test_engine/canonical/vcf_normalizer.post_normalize()` step that is
   applied to *every* voter's raw output. Until the voters emit the
   same schema on the same correct input, the oracle cannot produce
   usable signal. Minimum requirements: same top-level keys
   (`header`, `records`), same scalar types (`Number` as int, Booleans
   as `true/false`), stripped CSV quotes on `Description`, no
   implementation-specific fields (`IDX`, `records_read`, etc.),
   normalised `fileformat` string.

2. **Fix the detection predicate in the driver.** Add the
   pre-fix-install + pre-fix-failure check (left-hand side of §5.3.1)
   before scoring any cell. Draft in
   `scripts/audit_phase4_detections.py::_run_sut` — move that logic
   into `bug_bench_driver.detection_from_adapter`.

3. **Re-run Phase 4** after both fixes, with the 300 s / bug budget
   first (to confirm the signal is real) and then the 7200 s / bug
   production budget.

Until both (1) and (2) land, **the only trustworthy detection numbers
are the 2 vcfpy cells**. The aggregate and per-SUT summaries in
`biotest_bugbench_{vcf,sam,summary}.md` should be read with the audit
in mind.

## Deliverables

- `scripts/validate_oracle_on_correct_vcfs.py` — re-runnable oracle
  sanity check.
- `scripts/dump_voter_canonicals.py` — per-seed per-voter canonical
  dump + pairwise diff.
- `scripts/audit_phase4_detections.py` — pre-fix-failure audit of
  confirmed cells.
- `compares/results/oracle_validation_vcf.json` — oracle sanity raw
  data.
- `compares/results/phase4_audit.json` — per-cell audit result.
- `compares/results/voter_canonicals/spec_example__*.json` — per-voter
  canonical JSON on the spec example.
