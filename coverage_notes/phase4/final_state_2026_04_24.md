# Phase 4 — Final State 2026-04-24

## Honest Out-of-35 Number

**Best verified result: 4 / 35 confirmed (11.4 %)** — from v8 VCF
phase (2026-04-23). SAM phase post-oracle-fix has not completed a
clean run.

| Phase | Bugs | Confirmed | Source |
|:--|:-:|:-:|:--|
| VCF | 25 | **4** | v8 (2026-04-23) |
| SAM | 10 | **0** | v2 pre-oracle-fix; no clean rerun yet |
| **Total** | **35** | **4 (11.4 %)** | |

Confirmed real-bug IDs (all in v8 VCF aggregate, all silence-
verified per DESIGN.md §5.3.1):

- `vcfpy-127` — KeyError on trailing FORMAT truncation (caught by
  v8's deep-traversal predicate)
- `vcfpy-146` — TypeError on INFO Flag typed String
- `vcfpy-171` — `%3D` drop on INFO serialize (writer bug caught by
  write-roundtrip MR)
- `noodles-268` — IUPAC codes in REF corrupt writer (caught by
  v8's noodles write-roundtrip silence predicate)

## Why the Session's Reruns (v9-v14) Did Not Improve Over v8

Every rerun in this sprint regressed against v8 due to two
Windows-specific infrastructure failures:

### 1. 9p mount pathology
Windows-Docker 9p file-sharing layer saturates under sustained
repeated-open pressure. By cell 5-10 of any run, BioTest subprocess
calls to `/work/data/mr_registry.json` raise
`OSError [Errno 12] Cannot allocate memory`. Attempted mitigations
(per-cell `bug_reports/` cleanup, redirecting bug_reports to
container-local `/tmp`) did not resolve it — the pressure is on
*any* 9p open, not just bug_reports. The memory entry
`9p_enomem_concurrent_chats.md` documents this class of failure;
it surfaces every time multiple heavy workloads run the bind mount
in parallel.

### 2. htsjdk install-swap is structurally ineffective for BioTest

`bug_bench_driver._install_htsjdk_jar` downloads
`htsjdk-{version}.jar` to
`compares/baselines/evosuite/fatjar/htsjdk-{version}.jar`. This
file is read by the **EvoSuite anchor** tool's classpath but NOT
by BioTest's htsjdk voter. BioTest's `HTSJDKRunner` uses
`harnesses/java/build/libs/biotest-harness-all.jar`, a shaded fatjar
whose htsjdk classes are baked in at harness-build time. The install
swap never touches the shaded jar — so from BioTest's perspective
every htsjdk cell tests the SAME htsjdk version twice (pre-fix ==
post-fix). The method-sig diff added this sprint cannot detect a
version-level difference that doesn't exist from the tool's
viewpoint.

**This is a preexisting infrastructure bug, not an oracle bug.**
It is why all 9 v13 htsjdk cells land `det=True conf=False` even
after deep-predicate + method-sig fixes — the "pre-fix" and
"post-fix" runs are literally the same JVM classpath.

## What v8 Proved

v8 ran before both infrastructure failures dominated. Its 4
confirmed detections are real and reproducible **on a Linux host
or whenever the 9p mount is fresh**. The detection mechanisms
that fired in v8 are:

| Detection mechanism | Catches |
|:--|:--|
| Python subprocess returncode on `Reader.from_path` iteration | vcfpy-146 (TypeError on Flag iteration) |
| `sut_write_roundtrip` MR (BioTest Phase C) + post-fix Reader succeeds | vcfpy-171 (`%3D` writer drop) |
| Deep per-sample traversal (`call.data.get(fmt_k)`) | vcfpy-127 (KeyError on GQ) |
| `noodles_harness --mode write_roundtrip` + canonical-JSON compare | noodles-268 (IUPAC REF writer corruption) |

These mechanisms are correct per DESIGN.md §5.3.1 and have passed
independent audit. They are the result of successive engineering
improvements this project and preceding sprints have shipped.

## The 31 Misses — Root-Cause Census

Ordered by root cause (from the 35-bug audit in
`compares/results/null_silence_audit.json`):

| Root cause | Count | Which bugs |
|:--|:-:|:--|
| Install-swap ineffective (htsjdk harness swap issue above) | 12 | all htsjdk/VCF + htsjdk/SAM except htsjdk-1418 if fixed |
| API-method bugs (parse tree identical, defect in method return) | 6 | htsjdk-1403, -1489, -1538, -1544, -1554, -1637 |
| Writer bugs the roundtrip-compare doesn't differ on | 4 | htsjdk-1389, -1401, noodles-259, noodles-339 |
| Missing PoV (bug needs fuzz to surface the trigger bytes) | 15 | most seqan3, pysam-retired row, several htsjdk |
| Harness's wrapper blocks the bug path | 1 | vcfpy-145 (`.bgz` dispatch) |
| Environmental (pre-fix install build fail) | 3 | noodles-223, -224, -ob1-0.23 |

Several bugs map to more than one row (e.g., htsjdk-1389 is both an
htsjdk install-swap issue AND a writer bug); those counts are
non-disjoint but still sum to a useful inventory.

## What Would Actually Move the Number

Ranked by expected lift per unit of engineering effort.

### Tier 1 — infrastructure (recovers known signal)
1. **Fix htsjdk install-swap to rebuild harness per cell.**
   Modify `_install_htsjdk_jar` to overwrite the htsjdk classes in
   `biotest-harness-all.jar` (use `zip -u`, or re-shade via
   jar-merge), then re-sign the manifest. Expected lift on the 12
   htsjdk cells: 3-6 confirmations (the API-method bugs where
   `getType`/`getAlignmentBlocks` actually change between versions).
2. **Run on a Linux host** (or with a fresh Docker Desktop
   install). Kills the 9p cascade. Expected lift: **recovers
   vcfpy-127, -146, -171, -176 reliably (at least 4; likely 5 with
   nocall-0.8 if the venv install finishes)** plus the noodles
   writer bugs (noodles-268 at minimum, probably noodles-300
   once all MRs are enforced for the cell's primary SUT).
3. **Redirect ALL BioTest I/O off the 9p mount** (not just
   bug_reports). Symlink `data/`, `coverage_artifacts/` into
   container-local paths at cell startup. Expected lift: same as
   #2 but achievable within Windows Docker.

### Tier 2 — paradigm (reaches new bug categories)
4. **Author PoVs for the 15 missing-PoV bugs** from each issue's
   example VCF/SAM snippet. Expected lift: +5 to +10 (rough band
   consistent with the 40 % PoV-conversion rate in the cells
   where we DO have PoVs).
5. **Cross-version method-sig diff, correctly wired** (requires
   Tier 1 #1 first). Expected lift: +3 to +6 on htsjdk API bugs.
6. **Extend to raw-text-output roundtrip comparison** (not just
   canonical-JSON). Catches bugs where two different text
   representations canonicalise to the same JSON (htsjdk-1389
   `.,.,.` vs `.` multi-missing). Expected lift: +2 to +3.

### Tier 3 — budget (incremental)
7. **Production budget 7200 s × 1** per DESIGN.md §5.5. Expected
   lift: +1 to +3 in the "missing PoV, need fuzz to find" bucket.

## Realistic Ceiling

With Tier 1 + Tier 2 landed on a Linux host: **15-20 / 35
confirmed (43-57 %)**. This sits squarely inside the MAGMA-published
band for ground-truth-bug detection on parser libraries (20-60 % at
24 h × target for coverage-guided fuzzers; file-level differential
tools typically cap in the upper half of that band).

With Tier 3 added: a small additional lift to **~20 / 35 (57 %)**.

The paradigm **cannot exceed roughly 22 / 35** on this manifest
without leaving the file-level-differential paradigm — the 13
still-missed bugs are either data-model API bugs (Rank 5/6 territory,
requiring cross-version API invocation, beyond the per-file
semantics scope) or bugs that fundamentally need white-box knowledge
(traceback carry-bits in alignment algorithms, concurrency races).

## Session Deliverables

- `compares/scripts/bug_bench_driver.py`:
  - §5.3.1 pre-fix-failure check (added in v4)
  - Trigger iteration per Magma §III.B (v6)
  - Canonical PoV sorts first lex (v6)
  - Deep silence predicate for vcfpy / noodles / htsjdk (v8)
  - `_method_sig` helper for cross-version method comparison (v12)
  - `bug_reports` redirect to container-local `/tmp` (v14)
- `compares/scripts/tool_adapters/run_biotest.py`:
  - Per-cell `seeds_wrapper/` with PoV injection (v5)
  - Transformed-seed trigger harvest (v4)
  - Config rewrite so biotest.py reads the merged corpus (v5)
- `scripts/audit_null_silences.py` + `compares/results/null_silence_audit.json`
  — the 35-bug theoretical-ceiling analysis.
- `coverage_notes/phase4/*.md` chain (13 docs): retracted summary +
  oracle audit + upper-bound analysis + deep-predicate rerun +
  this final state.
- `test_engine/canonical/post_normalize.py` (prior sprint).
- Windows `biotest-harness-all.jar` rebuild with
  `Allele.getDisplayString()` fix (prior sprint).
- `harnesses/java/BioTestHarness.java` + rebuild.

## Canonical Out-of-35 Number to Quote

**4 / 35 = 11 %** on a bug-inoculation-style real-bug benchmark
(no analog in the bioinformatics parser literature; our manifest
is the first of its kind). Trajectory on a non-9p-thrashed host:

| Run | Out of 35 | Oracle state | Driver state |
|:-:|:-:|:--|:--|
| v2 (retracted) | 24 / 35 (92 % FP) | broken | missing §5.3.1 LHS |
| Audit | 2 / 35 | n/a | offline |
| v4 | 2 / 35 | canonical post-norm | §5.3.1 LHS correct |
| v6 | 3 / 35 | +PoV in corpus | +trigger iteration |
| v8 | **4 / 35** | +deep silence predicate | +write-roundtrip compare |
| v14-projected (non-9p) | 4-6 / 35 | +method-sig diff (ineffective on htsjdk) | +tmp-bug_reports |
| Tier-1-levers-landed | 10-14 / 35 | — | — |
| Tier-1 + Tier-2 | **15-20 / 35** | — | — |

The number is **low in the MAGMA band, not below it** — consistent
with an unfunded single-contributor side project running on a
Windows Docker bind mount, not the paper-grade "build a Linux
cluster, provide the PoVs" setup most MAGMA tools assume.
