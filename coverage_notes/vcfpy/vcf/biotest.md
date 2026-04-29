# BioTest — vcfpy / VCF line coverage

Source-of-truth for every BioTest coverage measurement taken against the
**vcfpy** SUT (bihealth/vcfpy 0.14.2, pure-Python VCF parser) in **VCF**
mode. All numbers use the five-path weighted filter defined in
`biotest_config.yaml: coverage.target_filters.VCF.vcfpy`:

```
vcfpy/reader
vcfpy/parser
vcfpy/header
vcfpy/record
vcfpy/writer
```

This is the same scope DESIGN.md §3.2 / §3.3 uses when grading any Python
SUT on the VCF row — Atheris and Pure Random are measured against the
identical five buckets, so BioTest's numerator compares to those
baselines line-for-line. The filter excludes `bgzf.py` (BGZF
compression, not exercised by plain `.vcf` tests) and `tabix.py` (random
access indexing, not tested), matching the same "only what BioTest
actually exercises" rationale documented in the config comments.

Run-by-run snapshots are archived as
`coverage_artifacts/coveragepy_post_run{N}_vcfpy.db` (SQLite
`.coverage` file from `coverage.py`) and
`coverage_artifacts/coveragepy_vcfpy_run{N}.json` (exported via
`coverage json`).

---

## Timeline

| Run | Date       | Wall     | Iters | **Weighted VCF** | Covered / Total | Enforced MRs | SCC | DET | Notes |
|:-:|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:--|
| **1** | **2026-04-21** | **~80 m** (stopped mid-iter-2 synth) | **1** | **73.4 %** | **863 / 1 176** | **14 / 21** | **4.75 %** | **34.3 %** | Fresh-corpus vcfpy/VCF baseline. All 7 Phase B themes mined against vcfpy with Rank 5 (10 query methods discovered). Phase D iter 1 completed, iter 2 synth running when stopped. |

---

## Cross-tool comparison — BioTest vs Atheris under the SAME DESIGN filter

Atheris's primary Phase-2 run on vcfpy is archived at
`compares/results/coverage/atheris/vcfpy/REPORT.md`. The headline number
in that report — **55.06 %** (`893 / 1 622`) — is NOT directly
comparable to the BioTest number above, because the two reports used
different denominators. Atheris's REPORT.md measured
`source=['vcfpy']` (all 10 files in the installed `vcfpy/` package),
while BioTest's number applies the DESIGN §3.2 fairness filter from
`biotest_config.yaml` (only the five parse / header / record / writer
modules BioTest actually exercises).

To make the comparison apples-to-apples, apply the same filter to both
tools' per-file tables:

| File | Total stmts | **BioTest** covered / % | **Atheris** covered / % | Δ (pp) |
|:--|:-:|:-:|:-:|:-:|
| `vcfpy/reader.py` |  62  |  45 / **72.6 %** |  45 / **72.6 %** |  0.0 |
| `vcfpy/parser.py` | 372  | 307 / **82.5 %** | 325 / **87.4 %** | −4.9 |
| `vcfpy/header.py` | 364  | 251 / **69.0 %** | 238 / **65.4 %** | +3.6 |
| `vcfpy/record.py` | 279  | 174 / **62.4 %** | 149 / **53.4 %** | +9.0 |
| `vcfpy/writer.py` |  99  |  86 / **86.9 %** |  24 / **24.2 %** | **+62.7** |
| **OVERALL (DESIGN filter)** | **1 176** | **863 / 73.4 %** | **781 / 66.4 %** | **+7.0** |

Atheris row recomputed from `compares/results/coverage/atheris/vcfpy/REPORT.md`
section 3 (terminal per-file table, rep 0 at t = 7 200 s). The BioTest
row is Run 1's `measure_coverage.py` output verbatim.

### Where the +7 pp comes from

- `writer.py` (+62.7 pp): BioTest's `sut_write_roundtrip` MRs (DESIGN §3.3)
  re-serialize each accepted parse through `vcfpy.Writer`, exercising
  formatter branches atheris's read-only harness never hits. This is
  the single biggest driver of the gap.
- `record.py` (+9.0 pp): BioTest's `api_query_invariance` MRs (Rank 5)
  call the 10 discovered query methods (`is_variant`, `is_het`,
  `gt_bases`, etc.) on every parsed record, reaching accessor lines
  atheris's input-mutation loop doesn't cover.
- `header.py` (+3.6 pp): BioTest's header-ordering / meta-line
  invariance MRs permute header structure and re-parse, exercising
  alternate dispatch paths in `HeaderLine` subclasses.
- `parser.py` (−4.9 pp): atheris's random-input mutation surfaces more
  malformed-line branches than BioTest's 33-seed corpus + Rank 3
  rejection MRs do in one iteration. Iter 2-4 of Phase D would close
  some of this gap, since the iter-1-only run under-exercises
  rejection paths.
- `reader.py` (0.0 pp): identical — both tools drive `.from_path()`
  exactly the same way on non-bgzipped input.

### Why the raw numbers *look* more different than they are

Atheris's `REPORT.md` headline 55.06 % folds in three large files that
the DESIGN filter drops for the fair comparison:

| Dropped file | Atheris line % | Why DESIGN filter excludes it |
|:--|:-:|:--|
| `vcfpy/bgzf.py`  | 17.16 % (35 / 180) | BGZF compression — scope tests plain `.vcf`, not `.vcf.gz` |
| `vcfpy/tabix.py` | 16.76 % (49 / 238) | Tabix indexing — no random-access tests |
| `vcfpy/writer.py`| 18.99 % (24 / 99)  | KEPT in the DESIGN filter (BioTest's +62.7 pp lift lives here) |

BGZF + tabix together add 418 uncovered statements to the atheris
denominator, mechanically dragging its headline from ~66 % down to
~55 %. They are the same 418 statements BioTest excludes by design —
both tools ignore them equally, so removing them from both sides is
the only fair comparison.

### How to reproduce this comparison

```bash
# 1. Re-export atheris's .coverage as coverage.py JSON
#    (works on Linux / inside biotest-bench — on Windows the source
#    paths aren't resolvable because atheris recorded /opt/... paths)
cd compares/results/coverage/atheris/vcfpy/run_0
python3.12 -m coverage json --ignore-errors \
    -o /tmp/atheris_vcfpy_run0.json \
    --data-file=.coverage

# 2. Grade it under the same BioTest filter
py -3.12 compares/scripts/measure_coverage.py \
    --report /tmp/atheris_vcfpy_run0.json \
    --report coverage_artifacts/coveragepy_vcfpy_run1.json \
    --sut vcfpy --format VCF \
    --label "Atheris run_0 (DESIGN filter)" \
    --label "BioTest Run 1"
```

`measure_coverage.py` reads the filter rules once from
`biotest_config.yaml: coverage.target_filters.VCF.vcfpy` and applies
them to both reports identically, so the pp-level comparison is
grounded in the same definition on both sides.

---

## Run 1 detailed breakdown (2026-04-21)

First fresh-corpus vcfpy/VCF baseline. Config changes from the prior
htsjdk/SAM Run 10 state:

```diff
-  primary_target: htsjdk
+  primary_target: vcfpy
-  format_filter: SAM
+  format_filter: VCF
```

State reset before the run:

- `data/mr_registry.json` → reset to `data/mr_registry.baseline.json`
  (1 enforced, 0 quarantine). Gave Phase B a clean slate to mine VCF
  MRs against vcfpy without carrying over the SAM registry from Run 10.
- `data/feedback_state.json` + `data/rule_attempts.json` → removed so
  Phase D's iteration counter started at 0.
- `coverage_artifacts/.coverage` → removed so coverage.py wrote a fresh
  SQLite DB.

Seed corpus: **33 VCF seeds** (tier-1 + tier-2 htsjdk / htslib /
bcftools / gatk-imported; `spec_example.vcf` + `minimal_single.vcf`
+ `minimal_multisample.vcf` + real-world imports). No synthetic
seeds carried over.

### Invocation

```bash
py -3.12 biotest.py --phase B,C,D
```

Phase A cached (specs already ingested into ChromaDB from prior runs).
Phase B re-mined because the registry was empty; Phase C fed Phase D's
consensus oracle; Phase D iter 1 wrote the coverage number.

### Pipeline timing

| Phase | Wall | Output |
|:--|:-:|:--|
| A  Spec ingest       | cached | ChromaDB intact from prior VCF/SAM runs |
| B  MR mining (initial) | **6 m 22 s** | 24 new MRs across 7 themes; deepseek-chat; 10 vcfpy query methods discovered for Rank 5 |
| C  Cross-execution (initial, explicit) | **29 m 47 s** | 20 MRs × 33 seeds × ~5 voters = ~3 168 tests; 1 087 disagreements (DET 34.3 %) |
| D  Feedback loop iter 1 | ~42 m | Phase B re-mine (more MRs across all 7 themes), Phase C re-dispatch on ~41 MRs × 33 seeds = 1 353 tests, coverage collected at 19:02 |
| **Total (stopped mid iter-2 Rank 1 synth)** | **~80 m** | |

Stopped manually after iter 1's coverage-collection write so a second
Phase D iteration (~40 min more) didn't run unnecessarily — the user
only asked for a vcfpy baseline; further iterations can re-use the
saved state to extend the curve.

### Phase B throughput

| Theme | MRs mined |
|:--|:-:|
| `ordering_invariance` | 4 |
| `semantics_preserving_permutation` | 1 |
| `normalization_invariance` | 3 |
| `rejection_invariance` | 5 |
| `coordinate_indexing_invariance` | 4 |
| `round_trip_invariance` | 3 |
| `api_query_invariance` | 4 |
| **Total (initial)**   | **24** |

All seven themes produced at least one MR on the first attempt (no
retries). Phase D iter 1's internal re-mine added ~17 more (final
registry = 14 enforced + 7 quarantine = 21 post-oracle-triage), same
re-mining pattern documented in the htsjdk/VCF Run 6 baseline.

### Coverage against the DESIGN filter

```bash
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/coveragepy_vcfpy_run1.json \
    --sut vcfpy --format VCF \
    --label "BioTest Run 1 (vcfpy, Phase B+C+D iter 1)"
```

Output (verbatim — same fairness path that will grade Atheris + Pure
Random on the vcfpy row per DESIGN §4.1):

```
=== BioTest Run 1 (vcfpy, Phase B+C+D iter 1) (vcfpy/VCF) ===
  Report:  coverage_artifacts\coveragepy_vcfpy_run1.json
  Filter rules (from biotest_config.yaml):
    - vcfpy/reader
    - vcfpy/parser
    - vcfpy/header
    - vcfpy/record
    - vcfpy/writer

  Bucket                          Covered/Total       %
  vcfpy/reader                         45/62     ( 72.6%)
  vcfpy/parser                        307/372    ( 82.5%)
  vcfpy/header                        251/364    ( 69.0%)
  vcfpy/record                        174/279    ( 62.4%)
  vcfpy/writer                         86/99     ( 86.9%)
  OVERALL (weighted)                  863/1176   ( 73.4%)
```

**Weighted overall: 73.4 % (863 / 1 176 statements)** — well above the
htsjdk/VCF Run 6 baseline of 46.9 % and the biopython/SAM Run 2 ceiling
of 49.7 %. Two reasons the number is higher:

1. **Purely Python, pip-installed vcfpy = coverage.py traces every
   module with zero build-config overhead**. No JaCoCo JAR rebuild
   gaps, no Cython gymnastics, no gcovr link-step blockers. The five
   modules in the filter were imported live in-process through
   `VcfpyRunner` and traced line-for-line.
2. **vcfpy has a much smaller, tighter surface** than htsjdk's VCF
   package (1 176 statements vs 3 760 lines). No JEXL filter engine,
   no BCF2 binary codec, no dictionary / tabix path inside the filter
   scope — so fewer "structurally unreachable via file I/O" lines to
   drag the denominator up.

### Per-module reading

| Bucket | % | Covered / Total | What moves the number |
|:--|:-:|:-:|:--|
| `vcfpy/writer` | **86.9 %** | 86 / 99 | Smallest module; exercised by every `sut_write_roundtrip` MR. A handful of edge-case formatters (alt-allele symbolic reprs, breakend shorthand) are the residual missing lines. |
| `vcfpy/parser` | **82.5 %** | 307 / 372 | Main parsing path — header line → `HeaderLine` + body line → `Record`. Heavily exercised by Phase C's 3 168-test volume. Uncovered residual is error-handling branches for malformed VCF that the 33-seed corpus doesn't hit (the rejection-invariance MRs add some but not all). |
| `vcfpy/reader` | **72.6 %** | 45 / 62 | Small file-open wrapper. Uncovered lines 99-103, 155-164 are compressed-file branches (`.vcf.gz` via bgzf) that BioTest deliberately skips — scope excludes `bgzf.py`, so these reader dispatchers stay unexecuted. |
| `vcfpy/header` | **69.0 %** | 251 / 364 | Header meta-line classes. ~113 uncovered lines cluster around field-level accessors and `__repr__` / `__eq__` of structured sub-header types — API-only paths analogous to htsjdk's `VCFHeaderLine` subclasses. |
| `vcfpy/record` | **62.4 %** | 174 / 279 | Data-model bucket. Same pattern as htsjdk/VCF Run 6 `variantcontext` (34.6 %): `Record` gets constructed during parse but most of its `is_monomorphic`, `is_snv`, `is_indel`, `call_for_sample` etc. accessors only fire when an `api_query_invariance` MR exercises them. 10 query methods were discovered for Rank 5 but with iter 1 only, not all landed. |

Uncovered-regions head (first 20, from `data/coverage_report.json`):

```
reader.py:99-103, 155-156, 158, 161, 163-164, …+5 more
record.py:77, 132, 149, 157-160, 169-175, …+57 more
header.py:68-69, 73-74, 78, 81, 84, …+80 more
```

### Oracle signal (Phase C)

From `data/det_report.json` after the explicit Phase C pass:

| Metric | Run 1 Phase C |
|:--|:--:|
| Total tests | **3 168** |
| Disagreements (any-voter) | **1 087** |
| DET rate | **34.3 %** |
| Bug reports written | ~1 346 (Phase D iter 1 added more) |
| MRs in scope | 21 (14 enforced + 7 quarantined) |

Top-DET MRs (head of `by_mr`):

```
fb5a105d7c9c   Missing value representation round-trip invariance    DET=0.818
9746c6e5c109   (unnamed query)                                        DET=0.691
2af5800ea12a   ALT allele permutation with GT and Number=R            DET=0.551
bc124d1e4573   Structured meta-line key-value pair ordering           DET=0.497
ffbe4a62d130   Meta-information lines ordering invariance (baseline)  DET=0.473
```

The 34.3 % DET rate is in the expected band for VCF-primary runs
(Run 6 baseline was ~11 %, but that was Tier-0 defaults with 4
voters). With 5 voters (htsjdk / pysam / biopython / vcfpy /
noodles / reference / htslib — biopython skips VCF so effectively
4-5 for VCF) and the new VCF MR set, ~34 % is consistent.

### Rank 5 (API-query MRs) signal

```
Discovered 10 query methods on primary vcfpy for Rank 5
```

The `VcfpyRunner` exposes 10 concrete query methods on `Record` / `Call`
(is_variant, is_het, gt_bases, etc.). Phase B's `api_query_invariance`
theme mined 4 `query_method_roundtrip` MRs that populate these method
names — same MANDATORY-wording pattern shipped for htsjdk/VCF Run 6
(`mr_engine/dsl/models.py::_query_methods_required_when_query_transform`
validator active). Sample API-query failure in the log:

```
[WARNING] API-QUERY FAILURE [query_changed]: vcfpy on
  real_world_bcftools_plugin_setGT.vcf
  (seed=1715441092) — methods that changed:
  ['is_variant', 'is_het', 'gt_bases']
```

Real vcfpy query-method behaviour diverged under the MR's transform on
this seed. This is the exact signal `query_method_roundtrip` MRs are
designed to surface — grammar-legal input through an
equivalence-preserving transform, a query method now returns a different
answer, transform is suspect OR vcfpy has a query-method bug.

### SCC

```
SCC Progression: 4.75%  (1 iter)
Final SCC: 4.75 %   (1 iter, 21 rules covered across 453 testable VCF rules)
```

SCC at 4.75 % on the first iteration matches the early-Phase-D band
observed in htsjdk/VCF Run 3 (3.8 → 4.4 %) and biopython/SAM Run 2
(0.7 %). Since the SCC denominator is the full CRITICAL + ADVISORY
VCF rule set (453 rules), and 21 rules is about what a single iter's
MR set can cover, no surprise here.

The Top-5 uncovered blindspots surfaced to iter 2's ticket were all
**BCF-specification** rules:

```
VCFv4.5.tex::BCF specification::p1297 / p1301 / p1292
VCFv4.5.tex::Overall file organization::p1396
VCFv4.5.tex::Header::p1400
```

BCF (binary VCF) is explicitly out of scope for the current vcfpy
filter — vcfpy ships without BCF codec support — so these rules
are structurally unreachable via the vcfpy VCF parser. Same
"reachability filter should sink these" issue noted under the
biopython/SAM Run 2 writeup; the reachability-filter wiring on
biotest.py line 102-188 handles Java/Python but does not yet tag
BCF-spec rules as structurally unreachable for a VCF-only SUT.
Adding that mapping would push SCC's top-5 slot to something the
vcfpy parser can actually reach.

---

## Structural ceiling — where the 73.4 % number sits

vcfpy 0.14.2's five-module filter has **1 176 executable statements**.
Run 1 covered 863 of them — 313 lines uncovered. Same pattern as
htsjdk/VCF (where the 1 995 uncovered out of 3 760 split into
reachable + unreachable buckets), adapted to vcfpy's surface:

| Uncovered cluster | Approx lines | Reachable via file-I/O MR? |
|:--|:-:|:-:|
| `record.py` data-model accessors (`is_*`, `call_for_sample`, CNV sub-accessors) | ~60 | Partial — Rank 5 API-query MRs reach these; iter 1 only ran 4 query MRs, more iterations move this bucket. |
| `header.py` structured-meta accessors + `__repr__` / `__eq__` / pickling | ~80 | API-only — not reached by plain parse/write. |
| `reader.py` compressed-file (`.vcf.gz` / bgzf) dispatchers | ~12 | No — filter excludes `bgzf.py`, the dispatchers that would hit it never execute. |
| `parser.py` malformed-input rejection branches not covered by Rank 3 | ~40 | Partial — rejection-invariance mined 5 MRs, more Rank 3 themes + malformed mutators would close this. |
| Writer edge-case allele formatters (symbolic, breakend long-form) | ~10 | Partial — `sut_write_roundtrip` fires but few seeds carry symbolic / breakend alts. |
| Misc. (closed-file guards, defensive `raise`s, import-only lines) | ~35 | No — unreachable via `parse(x) → JSON`. |
| **Structurally unreachable via file I/O** | **~120** | — |
| **Reachable with more seed diversity + more iterations** | **~193** | Yes |

Which means the realistic ceiling for BioTest-on-vcfpy is in the
**~85-90 %** band once iter 2+ + Rank 5 + corpus expansion land.
Run 1's 73.4 % is already well above the "one-iter baseline" numbers
for the other SUTs; continuing Phase D to iter 4 should cash in the
~120 reachable-but-missed lines from expanded Rank 3/5 coverage.

---

## Next levers (not applied yet)

1. **Continue to iter 2-4.** `max_iterations=4` (VCF default) lets
   Phase D mine Rank 1 synthetic seeds targeting the uncovered
   `record.py` / `header.py` accessors — the exact lever htsjdk/VCF
   Run 3-4 used to land +1.7 pp on the `variantcontext` bucket.
2. **Expand the reachability filter** to tag `BCF specification::*`
   rules as structurally unreachable for a VCF-text-only SUT like
   vcfpy (and noodles-vcf). Low effort; pushes SCC's Top-K queue to
   rules vcfpy can actually reach.
3. **Enable Rank 6 (MR synthesis)**: flip
   `feedback_control.mr_synthesis.enabled: true`. Unlike htsjdk/VCF
   Run 7, where Rank 6 only added wall-time without moving coverage,
   vcfpy's smaller surface means each new MR is more likely to land
   on still-uncovered record/header accessors.

---

## Methodology — how coverage is computed

Follows the same recipe documented in `compares/scripts/README.md`
(the cross-tool fairness path — measure every tool under the same
filter from `biotest_config.yaml`):

```bash
# 1. Run BioTest with primary_target=vcfpy, format_filter=VCF.
#    PythonCoverageContext wraps Phase C and writes
#    coverage_artifacts/.coverage (SQLite) on exit.
py -3.12 biotest.py --phase B,C,D

# 2. Snapshot the SQLite DB for reproducibility
cp coverage_artifacts/.coverage \
   coverage_artifacts/coveragepy_post_run{N}_vcfpy.db

# 3. Export JSON (the DESIGN §3.2 cross-tool format)
py -3.12 -m coverage json \
    --data-file=coverage_artifacts/.coverage \
    -o coverage_artifacts/coveragepy_vcfpy_run{N}.json

# 4. Apply the DESIGN filter via the cross-tool fairness script
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/coveragepy_vcfpy_run{N}.json \
    --sut vcfpy --format VCF \
    --label "BioTest Run {N}"
```

Step 4 reads `coverage.target_filters.VCF.vcfpy` from the config,
walks the coverage.py JSON's `files[]` entries (dict-shaped, as
distinct from gcovr's list-shape), keeps only files whose path
basename matches any of `{vcfpy/reader, vcfpy/parser, vcfpy/header,
vcfpy/record, vcfpy/writer}`, then sums `summary.covered_lines` and
`summary.num_statements` per bucket. This is the **same reader**
(`_measure_coveragepy_json`) biopython/SAM is graded through, so the
comparison is apples-to-apples by construction.

`PythonCoverageContext`'s `source_pkgs` derivation evicts any already-
imported vcfpy modules from `sys.modules` before starting the tracer,
so the first import inside the context is re-instrumented (same
"tracer-install race" fix that unblocked biopython/SAM Run 1 —
documented in `test_engine/feedback/coverage_collector.py`).

---

## Artifacts

| File | Purpose |
|:--|:--|
| `coverage_artifacts/.coverage` | Live SQLite DB from the most recent run (currently Run 1) |
| `coverage_artifacts/coveragepy_post_run1_vcfpy.db` | Run 1 snapshot (SQLite — 73.4 %) |
| `coverage_artifacts/coveragepy_vcfpy_run1.json` | Run 1 exported JSON (466 KB) |
| `data/coverage_report.json` | Live Phase D report (primary=vcfpy, Python, 863/1 176, 73.4 %) |
| `data/det_report.json` | Phase C DET report (3 168 tests, 34.3 % DET, 21 MRs) |
| `data/feedback_state.json` | Phase D state (iter 1, SCC=4.75 %, enforced=14, demoted=0) |
| `data/mr_registry.json` | MR registry after iter 1 (14 enforced + 7 quarantine) |
| `data/run_vcfpy_vcf_phase_bcd_iter1.log` | Full stdout/stderr of the ~80-min run |
| `data/mr_registry.json.pre_vcfpy` | Pre-run registry backup (the Run 10 SAM state) |
| `biotest_config.yaml.backup_vcfpy` | Pre-run config backup (restore via `cp backup config`) |

---

## Kill switches (same as biopython/SAM + htsjdk/VCF — all rank levers SUT-agnostic)

| Lever | Disable |
|:------|:--------|
| Rank 1 seed synth | `feedback_control.seed_synthesis.enabled: false` |
| Rank 2 htslib corpus | skip `seeds/fetch_real_world.py` |
| Rank 3 malformed MRs | drop `rejection_invariance` from `phase_b.themes` |
| Rank 4 `target()` directive | drop `Phase.target` from orchestrator phases |
| Rank 5 API-query MRs | drop `api_query_invariance` from `phase_b.themes` or set vcfpy runner's `supports_query_methods=False` |
| Rank 6 MR synthesis | already off by default: `feedback_control.mr_synthesis.enabled: false` |

---

## Re-run recipe

```bash
# 1. Set primary target + format
sed -i 's/^  primary_target: .*/  primary_target: vcfpy/' biotest_config.yaml
sed -i 's/^  format_filter: .*/  format_filter: VCF/'      biotest_config.yaml

# 2. Clean state for a fresh baseline
rm -f coverage_artifacts/.coverage
cp data/mr_registry.baseline.json data/mr_registry.json
rm -f data/feedback_state.json data/rule_attempts.json

# 3. Run (includes Phase B since the registry was reset)
py -3.12 biotest.py --phase B,C,D

# 4. Measure
cp coverage_artifacts/.coverage \
   coverage_artifacts/coveragepy_post_run{N}_vcfpy.db
py -3.12 -m coverage json \
    --data-file=coverage_artifacts/.coverage \
    -o coverage_artifacts/coveragepy_vcfpy_run{N}.json
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/coveragepy_vcfpy_run{N}.json \
    --sut vcfpy --format VCF \
    --label "BioTest Run {N}"
```
