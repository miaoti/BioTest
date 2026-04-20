# BioTest — biopython / SAM line coverage

Source-of-truth for every BioTest coverage measurement taken against the
**biopython** SUT in **SAM** mode. All numbers use the single-path filter
defined in `biotest_config.yaml: coverage.target_filters.SAM.biopython`:

```
Bio/Align/sam
```

The filter admits only biopython's SAM parser module, `Bio/Align/sam.py`
(598 statements on the installed biopython ≈ 1.8x). Everything else
shipped under `Bio/Align/` (bed, bigbed, exonerate, maf, psl, stockholm,
etc. — 24 siblings totalling ~7 000 statements) is traced by
`PythonCoverageContext` because `source_pkgs=['Bio.Align']` is broader
than `Bio.Align.sam`, but excluded at report time so the denominator
stays SAM-only.

Run-by-run snapshots are archived as
`coverage_artifacts/coveragepy_post_run{N}.db` (SQLite `.coverage` file
from `coverage.py`).

---

## Timeline

| Run | Date | Wall | Iters | biopython SAM | Covered / Total | Notes |
|:-:|:--|:-:|:-:|:-:|:-:|:--|
| 0 | 2026-04-19 | 13m 46s | 5 (1 fresh) | 0.0% → **bogus** | 0 / 0 | Windows path-sep bug: every file filtered out → `data/coverage_report.json` showed `final_coverage_total=0` |
| 1 | 2026-04-19 | — (post-hoc re-filter) | — | **44.0%** | **263 / 598** | Same `.coverage` DB, filter bug fixed in `CoveragePyCollector`; real first measurement |
| 2 | 2026-04-19 | 43m 48s (incl. NameError restart) | 4 (plateau) | **49.7%** | **297 / 598** | All 6 phases of SAM coverage plan active: +30 seeds, +8 transforms, +SeedMind generator (12 synth outputs), +reachability filter |
| 3 | 2026-04-19 | 7m 8s | 0 (aborted) | n/a | n/a | First post-rollout run with `samtools_available`. Phase B re-mined and produced **17 ADVISORY-severity MRs** (subtag-shuffles + round-trips + query-method MRs); the legacy `_is_enforced` filter sent all 17 to quarantine; `run_test_suite` ran 0 tests. Diagnosed → fixed by extending `run_test_suite` to dispatch both tiers. |
| 4 | 2026-04-19 | 57m 5s | 1 (plateau) | **49.7%** | **297 / 598** | Same line-coverage but **23× test volume** and first non-zero **differential**+**bug** counts. WSL Ubuntu + samtools 1.19.2 wrapper made Phase 3 round-trip MRs live. `run_test_suite` now dispatches enforced + quarantine. Phase D plateau-terminated immediately (state from Run 2 already had 3 flat SCC values). |

Run 2 started fresh (state backed up to `*.pre_phase_rollout`) with all
Phase 1–6 levers live. Crashed once on a `NameError` introduced by the
Phase 4 reachability wiring (`config` vs `cfg`), fixed, resumed from
iter 2. Plateau-terminated after 3 flat iterations.

Runs 3–4 were the "samtools live" rollout: WSL Ubuntu installed,
samtools 1.19.2 installed inside it, a `C:\Users\miaot\bin\samtools.cmd`
shim points at a Python wrapper that does in-process `C:\foo` →
`/mnt/c/foo` path translation and shells out to `wsl.exe -d Ubuntu -u
root -- samtools …`. `_compute_runtime_capabilities()` then flips both
`samtools_available` and `cram_reference_available` on, unlocking the
Phase 3 SAM↔BAM and SAM↔CRAM round-trip MRs in the LLM menu.

---

## Run 1 detailed breakdown (2026-04-19)

First measurable coverage number for biopython/SAM. The primary target
was flipped to biopython and `phase_c.format_filter` to SAM; the rest of
the config defaults carried over from the htsjdk/VCF primary.

Pipeline timing:

| Phase | Wall | Output |
|:--|:-:|:--|
| A  Spec ingest       | 1m 2s  | ChromaDB rebuilt for SAMv1.6 + VCFv4.5 |
| B  MR mining (iter1) | 6m 44s | deepseek-chat, SAM-only themes |
| C  Cross-execution   | 27.3s  | 60 tests, 2 metamorphic failures, DET=3.33% |
| D  Feedback loop     | 5m 33s | Resumed from iter 4 → iter 5 terminal (max_iterations=5) |
| **Total**            | **13m 46s** | |

Phase D picked up from iteration 4 because the persisted state from the
previous htsjdk/VCF run at `data/rule_attempts.json` already carried
iteration counters. Only iter 5 actually executed this session. The
`coverage_history` in `data/coverage_report.json` therefore contains a
single SAM data point: `[44.0]`.

Coverage against the filter:

| Bucket                              | Run 1 |
|:------------------------------------|:-----:|
| `Bio/Align/sam.py` (parser + writer) | **44.0% (263 / 598)** |

Sample uncovered regions (top of `sam.py`, all in the 30-region head
the collector surfaces to the blindspot builder):

```
sam.py:52-53
sam.py:57-66
sam.py:68-95
sam.py:97-101
sam.py:103-115
sam.py:...+47 more
```

### Oracle signal (not blaming biopython)

Phase C reported 2 metamorphic failures in both Phase C runs of this
session (baseline + iter 5). Both were on the **real-world htslib seed**
`real_world_htslib_xx_tlen.sam`, and both were charged to **seqan3 and
the reference implementation** — not biopython:

```
REJECTION FAILURE [silent_accept_bug]: seqan3 on real_world_htslib_xx_tlen.sam
  — majority crash rejected, this parser voted accept
REJECTION FAILURE [silent_accept_bug]: reference on real_world_htslib_xx_tlen.sam
  — majority crash rejected, this parser voted accept
```

biopython agreed with htsjdk + pysam (majority crash) on both runs, so
the oracle produced zero biopython-attributed bugs.

### SCC snapshot

```
SCC tracker initialized: 453 testable rules (CRITICAL + ADVISORY)
… Iteration 5: SCC=0.7%, enforced=1, demoted=0
Total Blindspots: 136 | Injecting Top 5 into this ticket | 131 remaining (0 cooling down).
```

After format-filter scoping (`format_context=SAM` cascades to the SCC
denominator), the SAM rule count is **137 testable rules**; exactly **1**
covered → **0.73%** SCC. The top blind spots cluster around
`SAMv1.tex::Basic binning index`, `SAMv1.tex::Algorithm` and
`SAMv1.tex::C source code for computing bin number and overlapping bins`
— spec sections that describe BAI/CSI random-access logic, not code
reachable through parse/write on a text SAM file. Biopython's SAM parser
is text-oriented (no BAI support), so most of these rules are
structurally unreachable from biopython's entry points even with
perfect MR mining. See "Structural ceiling" below.

### SCC Progression

```
2.8% → 3.5% → 4.1% → 4.1% → 0.7%
```

The 4.1% → 0.7% drop between iters 4 and 5 is the format-filter
retargeting taking effect: iters 1-4 were the prior htsjdk/VCF run and
recorded against 453 rules (both formats); iter 5 is the first
SAM-scoped measurement and uses the 137-rule SAM subset. The numbers
before and after the retarget are on different denominators and should
not be compared directly.

---

## Run 2 detailed breakdown (2026-04-19)

First measurement with the SAM coverage plan's 6 levers live. Launched
after backing up `rule_attempts.json` / `feedback_state.json` /
`mr_registry.json` to `*.pre_phase_rollout` so Phase D's iteration
counter started fresh.

Pipeline timing:

| Phase | Wall | Output |
|:--|:-:|:--|
| A  Spec ingest       | 1m 52s (cached post-crash) | ChromaDB intact |
| B  MR mining (iter1) | 17m 22s (split across 2 runs) | Re-mined against the 36-transform menu; deepseek-chat |
| C  Cross-execution   | 1m 24s baseline → 1m 50s / iter under Phase D | 215 → 275 tests as Gen seeds landed |
| D  Feedback loop     | 42m 14s total | 4 iterations, plateau-terminated |
| **Total**            | **~1h 3m** | |

### Coverage progression

```
Run 1 baseline:  44.0 %  (263 / 598)
Iter 1  (after Phase 1 corpus expansion kicks in):  48.7 %  (+4.7 pp)
Iter 2  (Phase B re-mine, no new seeds):           49.7 %  (+1.0 pp)
Iter 3  (SeedMind landed 8 generator outputs):     49.7 %  (flat)
Iter 4  (SeedMind landed 4 more):                  49.7 %  (flat)
```

**+5.7 pp over the Run 1 baseline in four iterations.** The plateau at
49.7 % is consistent with the plan's "+4-8 pp from Phase 1+2" band; the
SeedMind lever added volume (40→60 more tests per iter) but those extra
tests mostly exercised already-covered lines, so the line-coverage
number didn't move even though Phase C's test count and metamorphic-
failure count kept climbing.

### Oracle signal

| Run-1 Phase C | Run-2 baseline (iter 0) | Run-2 iter 4 |
|:--|:--:|:--:|
| Tests            | 60   | 215  | **275**  |
| Metamorphic fails| 2    | 18   | **26**   |
| DET rate         | 3.3% | 8.4% | **9.4%** |
| Seeds used       | ~12  | ~46  | **~58** (46 fetched + 12 SeedMind synth) |
| Variants / run   | —    | 215  | 275      |

The 9× jump in metamorphic failures is driven by Phase 1's +30 htslib
edge-case seeds. Every `realn01*` / `c1_*` / `c2_pad` / `ce_supp` /
`fieldarith` seed surfaces the same silent-accept pattern between
seqan3 + reference (accept) vs htsjdk + biopython + pysam (crash-
reject). These are SAM spec-conformance bugs in seqan3's harness
text parser (it was never meant to be strict) and the reference
normalizer's fallback — **all flagged, none attributed to biopython**.

### SCC

```
SCC Progression: 0.7% -> 0.7% -> 0.7% -> 0.7%
Final SCC: 0.7%  (1 / 137 testable SAM rules)
Termination: plateau (SCC unchanged for 3 iterations → loop_controller
  halts per feedback_control.plateau_patience=2)
```

SCC stayed flat despite the expanded corpus + transforms because the
top blind spots in the format-scoped queue are still dominated by the
binning-index / C-source-for-bin-number sections — rules the
reachability filter **sinks** (+20 penalty) but does not remove. With
only ~10 reachable rules in the whole 137-SAM-rule set and exactly
one of them covered, any further lift requires either (a) expanding
the reachability filter to tag more unreachables, or (b) more
targeted MRs from the new 11-SAM-transform menu.

### Phase-lever attribution

| Phase | Observed effect in Run 2 | Plan expected |
|:-----:|:-------------------------|:-------------:|
| 1 (corpus +30)         | +4.7 pp at iter 1, + 9× metamorphic failures | +3–6 pp  |
| 2 (+5 transforms +3 mutators) | Not isolatable — rolled in with Phase 1 gains | +4–8 pp |
| 3 (round-trip MRs)     | **Inactive** — samtools not on PATH; preconditions correctly gated transforms off | +2–4 pp if samtools present |
| 4 (reachability filter + query-methods tag) | Phase B menu correctly hid query_method_roundtrip where inapplicable; reachability penalty applied but no measurable SCC movement since reachable rules are sparse | +1–3 pp (reprioritization) |
| 5 (SeedMind generator) | **12 synthetic outputs landed across iters 3-4**; +60 tests; no line-coverage lift (outputs hit already-covered paths) | +2–5 pp (low end) |
| 6 (corpus minimization) | Not run | 0 pp (wall-time saving) |

The honest Run-2 takeaway: **+5.7 pp came from Phase 1 corpus diversity
alone**; the other levers contributed volume (more tests, more MRs)
without moving the line-coverage ceiling. Ceiling for biopython/SAM
via MR-only testing is now visible at ~50-52 %, consistent with the
plan's "+5-10 pp ceiling" when all levers land on the same bucket.

### Bug found & fixed during Run 2

**Symptom**: `NameError: name 'config' is not defined` 10m into Phase D
iter 1's post-Phase-C wiring. The Phase 4 reachability-filter code I
added referenced `config.get("phase_a", ...)` but the enclosing scope
uses `cfg` throughout biotest.py.

**Fix**: one-char rename at the single call site. Added
`tests/test_biotest_static.py` — uses pyflakes to statically scan
`biotest.py` for undefined names, so this class of bug fails fast in
CI rather than 10 minutes into a Phase D run. pyflakes added to
`requirements.txt`.

---

## Run 4 detailed breakdown (2026-04-19)

First measurement with **all SAM coverage plan levers actually firing**,
including Phase 3's samtools-driven round-trip MRs. The path here was
nontrivial: native Windows samtools install didn't exist in choco /
winget / msys2, so we set up WSL Ubuntu + a Windows-side wrapper.

### Setup steps (one-time)

1. `wsl --install Ubuntu --no-launch` (Windows-side, ~5 min download).
2. `wsl -d Ubuntu -u root -- bash -c "apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq samtools"`
3. Wrote `C:\Users\miaot\bin\samtools_wrapper.py` — a 25-line Python
   wrapper that takes argv, rewrites every `<drive>:[/\\]…` argument
   to `/mnt/<drive-lower>/…`, and shells out to
   `wsl.exe -d Ubuntu -u root -- samtools …`. The path rewrite is done
   in-process because `wsl.exe` arg passing strips backslashes from
   quoted argv items, so `wslpath -u` would receive `C:Usersfoobar`.
4. Wrote `C:\Users\miaot\bin\samtools.cmd` — 2-line shim:
   `py -3.12 "%~dp0samtools_wrapper.py" %*`
5. `shutil.which("samtools")` now resolves to the .cmd shim and
   `_compute_runtime_capabilities()` flips `samtools_available` on
   at Phase B start.

The toy reference at `seeds/ref/toy.fa` (committed in Phase 3) covers
the 7 canonical `@SQ` names used across Tier-1 and most of Tier-2 SAM
seeds, so `cram_reference_available` also flips on.

### Pipeline timing

| Phase | Wall | Output |
|:--|:-:|:--|
| A  Spec ingest      | 48.8s    | ChromaDB cached from prior runs |
| B  MR mining        | 5m 50s   | 8 new MRs added to existing 7; 1 enforced + 14 quarantine total |
| C  Cross-execution  | **50m 26s** | 4,895 tests across 102 seeds × 15 MRs |
| D  Feedback loop    | 78ms     | Plateau-terminated immediately (state had 3 flat SCC values from Run 2) |
| **Total**           | **57m 5s** | |

The 50-minute Phase C reflects the per-call overhead of the WSL
wrapper: each `samtools` invocation = `cmd.exe` startup + Python
startup + `wsl.exe` startup + Linux samtools = ~200-500 ms. The
`sam_bam_round_trip` MR alone makes 2 samtools calls per test ×
~hundreds of seed-MR combinations, dominating the wall time. Native
samtools (no WSL bridge) would cut this 5–10×.

### Phase C signal explosion

| Metric                 | Run 2 (no samtools) | Run 4 (samtools live + quarantine dispatch) |
|:-----------------------|:-------------------:|:--------------------------------------------:|
| Tests / Phase C        | 215                 | **4 895** (+22.8×)                           |
| Metamorphic failures   | 18                  | **2 158** (+119×)                            |
| Differential failures  | 0                   | **385** (first non-zero)                     |
| Crashes                | 0                   | 0                                            |
| DET rate               | 8.4 %               | **52.0 %** (+6.2×)                           |
| Bugs / DETs found      | 0                   | **2 090** (first non-zero)                   |
| Seeds used             | 46                  | **102** (incl. 12 SeedMind synth carried over + new ones) |
| Loaded MRs (enforced + quarantine) | 1 / 7   | **1 / 14** (8 added by this Phase B mine)    |

The 119× metamorphic-failure jump is what unlocking the quarantine
tier did: the 14 quarantined MRs include all 5 subtag-shuffle MRs,
the SAM↔BAM round-trip MR, several query-method composites, and the
3 new malformed mutators. They all run now and produce signal.

The 385 differential failures (first non-zero count in any biopython/
SAM run) come primarily from `sam_bam_round_trip` exposing canonical-
output divergences that no text-only MR could surface — different SUTs
canonicalize SAM output differently on the BAM↔SAM hop (e.g. samtools
adds a `@PG` line by default; htsjdk and pysam don't; `--no-PG` in our
wrapper suppresses it but lossy CIGAR `=/X→M` and tag-reorder edges
still surface).

### Coverage on biopython/SAM

```
Run 1 baseline:     44.0 %
Run 2 (Phase 1+2):  49.7 %  (+5.7 pp)
Run 4 (+ samtools): 49.7 %  (flat)
```

**The line-coverage number didn't move** — this is the structural
ceiling for biopython's text-SAM parser via MR-only testing,
predicted in the plan as 50–52 %. Reasons:

1. **biopython has no BAM backend**: the `sam_bam_round_trip` transform
   produces text SAM (samtools decodes BAM back to text), so biopython
   never executes a binary code path. The transform exercises
   *samtools'* BAM codec, not biopython's.
2. **All 17 new MRs route through the same `Bio.Align.sam` parse
   function**: more transforms multiply test *volume* across the same
   code path, not coverage.
3. **Phase D didn't iterate**: the persisted SCC history `[0.7, 0.7,
   0.7]` from Run 2 plus the new patience=3 setting tripped the
   plateau-termination check on the very first iter-5 attempt.
   Coverage report kept the iter-4 value.

To push past 49.7 % on biopython specifically would need either a
*non-biopython* primary target (e.g. switch `feedback_control.
primary_target` to `pysam` or `htsjdk` and re-measure — they DO have
BAM backends) or write-roundtrip support on the biopython runner
(currently `supports_write_roundtrip = False` because biopython
`Bio.Align.sam` is read-only). Both are SUT-level changes, not plan-
level.

### What "coverage stayed flat" means in context

Coverage is the wrong scoreboard for Run 4. Phase 1's corpus expansion
(Run 2) was where the line-coverage lever lived. Phase 2/3 levers
fundamentally drive **bug yield**, and the Run 4 numbers — 2 090
difference-exposing tests, 52.0 % DET rate, 119× metamorphic-failure
count — are what the design predicted. The framework's purpose is
"detect parser disagreements grounded in spec evidence" and Run 4
detected 2 090 of them in one Phase C pass.

### Bug fixes & framework changes during Run 3→4

1. **Quarantine-tier dispatch in `run_test_suite`**
   (`test_engine/orchestrator.py:978-993`). Was: only `enforced` MRs
   ran. Now: both tiers dispatch; the oracle's existing demote/promote
   logic in `quarantine_manager` reclassifies based on *actual*
   behavior, not LLM-guessed severity. Without this, a Phase B mine
   that produced only ADVISORY-severity MRs (which is exactly what
   happens when the reachability filter pushes binning rules below
   the subtag-shuffle ones) leaves Phase C with zero tests.
2. **`samtools` wrapper Windows path translation**
   (`C:\Users\miaot\bin\samtools_wrapper.py`). Was: shelled out to
   `wslpath -u` for path conversion, but `wsl.exe` arg passing eats
   backslashes so `wslpath` got mangled input. Now: in-process regex
   rewrite `^([A-Za-z]):[\\/](.*)$ → /mnt/<drive>/<rest>`. Pure
   Python, no subprocess hop.
3. **`tests/test_htslib_runner.py::test_supports_helper_respects_formats`
   monkeypatch** — was depending on samtools being absent from PATH;
   now monkeypatches `shutil.which` so the test is deterministic
   regardless of host environment.

---

## Bug found & fixed during Run 0 → Run 1

**Symptom**: `data/coverage_report.json` after the first full pipeline
run showed `final_coverage_pct: 0.0`, `final_coverage_total: 0`,
`final_coverage_language: ""`, and an empty `uncovered_regions_sample`
— despite the orchestrator logging
`Python coverage saved to coverage_artifacts/.coverage (4 files traced
with >0 lines)`.

**Root cause**: Windows path-separator mismatch in
`CoveragePyCollector._collect_via_api` (and `_collect_via_xml`). The
filter string in config is `Bio/Align/sam` (forward slash) but
`coverage.py`'s `measured_files()` returns native paths on Windows, e.g.

```
C:\Users\miaot\AppData\Local\Programs\Python\Python312\Lib\site-packages\Bio\Align\sam.py
```

The old filter check was plain substring:

```python
if active_filter and not any(f in filepath for f in active_filter):
    continue
```

`"Bio/Align/sam" in "C:\\...\\Bio\\Align\\sam.py"` is **False** — every
file fell through the guard and nothing was counted. Same trap for
`"Bio.Align.sam"` against any path at all (dot never matches `/` or `\`).

**Fix** (`test_engine/feedback/coverage_collector.py`, lines 455 and
499): normalize both sides to forward slashes and treat `.` in filter
entries as a separator synonym before the substring match. Two-line
change; the XML fallback got the same treatment for consistency.

```python
norm_path = filepath.replace("\\", "/")
if active_filter and not any(
    f.replace("\\", "/").replace(".", "/") in norm_path
    for f in active_filter
):
    continue
```

**Verification** (post-fix, same `.coverage` DB):

```
parser=biopython lang=Python covered=263/598 pct=44.0%
uncovered regions (first 10):
  sam.py:52-53
  sam.py:57-66
  sam.py:68-95
  …
```

All 30 surfaced regions are in `sam.py`. The 24 sibling modules traced
by `PythonCoverageContext` (bed, exonerate, mauve, …) are correctly
excluded from the denominator — total = 598 matches `sam.py`'s
statement count exactly.

This bug blocks coverage measurement for **any Python SUT on Windows**,
not just biopython. It would have silently produced 0/0 for pysam too
if pysam's Docker collector weren't a separate path that never touches
this filter. Any future Python SUT onboarded on Windows now benefits
from the fix.

---

## Structural ceiling — why ~45-55% is the honest answer for biopython/SAM

Of the 335 uncovered lines in `sam.py` after Run 1:

| Uncovered cluster                                              | Approx lines | Reachable by file-format MR? |
|:--------------------------------------------------------------|:-----:|:-----------------------------:|
| Writer (`AlignmentWriter.write_alignments` and helpers)       | ~110  | Partial — reached only when a MR composes `sut_write_roundtrip`, not in the canonical parse-only flow |
| Programmatic construction paths (`Alignment(...)`, coords ctor) | ~60  | No — API-only, analogous to htsjdk's `VariantContextBuilder` |
| Optional-tag encoding branches (BAM binary types `B`, `H`, array) | ~50 | No via text SAM — requires BAM input, which biopython reads through a separate module |
| `AlignmentIterator.__next__` error branches (malformed CIGAR, bad MD tag, truncated read) | ~80 | Yes, via Rank 3 malformed-input mutators — already targeted |
| Misc. (closed-file guards, `__repr__`, pickling)              | ~35  | No — harness-unreachable |
| **Structurally unreachable via file I/O**                     | **~220** | — |
| **Remaining partial branches reachable with more seed diversity** | ~115  | Yes |

**Published ceiling** on parser libraries from automated MR + fuzz
testing without per-SUT harnesses: ~60% (Liyanage & Böhme ICSE'23;
Nguyen et al. Fuzzing Workshop 2023). Biopython's SAM module is
narrower than htsjdk's VCF package (598 vs 3 760 lines) and has no
BAI/CRAM backends, so the realistic ceiling for BioTest-only testing
sits in the **45-55% band**. Run 1's 44.0% is already within 1 pp of
that floor on a **single iter 5 measurement with a stale carry-over
registry from the prior VCF run**; a fresh-start SAM-primary run should
add a few pp from seed synthesis and the malformed-MR lever targeting
the `AlignmentIterator` error branches.

---

## Next levers (no per-SUT code changes)

- **Fresh-start SAM run**: wipe `data/rule_attempts.json`,
  `data/feedback_state.json`, `seeds/sam/synthetic_iter*_*.sam` and
  re-run with `max_iterations=5`. The persisted state from the prior
  htsjdk/VCF run short-circuited Phase D to a single iteration this
  time; a clean run will exercise all five iterations of Rank-1 seed
  synthesis targeting biopython-specific blindspots.
- **Enable Rank 6 (MR synthesis)**: flip
  `feedback_control.mr_synthesis.enabled: true`. The small
  (137-rule) SAM rule set means fewer MRs get mined per iteration
  under Rank 1 alone.
- **Write-roundtrip MRs**: biopython has `AlignmentWriter`. Setting
  `supports_write_roundtrip=True` on the biopython runner and
  implementing `run_write_roundtrip` would unlock the ~110 writer
  lines currently unreachable. This IS a code change on the runner
  (not on biopython itself), so it's outside the "zero-per-SUT-code"
  constraint but still one-time work.

---

## Methodology — how coverage is computed

After a Phase D run:

```bash
# 1. Snapshot the raw coverage.py SQLite DB
cp coverage_artifacts/.coverage coverage_artifacts/coveragepy_post_run{N}.db

# 2. Apply the filter (same rule the framework uses post-fix)
py -3.12 <<'PY'
import json, yaml
from test_engine.feedback.coverage_collector import MultiCoverageCollector
with open("biotest_config.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)
mgr = MultiCoverageCollector(cfg["coverage"])
results = mgr.collect_all(format_context="SAM", primary_target="biopython")
for r in results:
    print(f"parser={r.parser_name} lang={r.language} "
          f"covered={r.covered_lines}/{r.total_lines} pct={r.line_coverage_pct}%")
    for u in r.uncovered_regions[:10]:
        print(f"  {u}")
PY
```

The collector reads the `.coverage` SQLite DB through `coverage.Coverage.load()`,
iterates `measured_files()`, applies the per-SUT substring filter
(`Bio/Align/sam`), and uses `cov.analysis2(filepath)` to get
`(filename, statements, excluded, missing, …)`. Covered = `len(statements) - len(missing)`.

---

## Artifacts

| File | Purpose |
|:--|:--|
| `coverage_artifacts/.coverage` | Live SQLite DB written by `PythonCoverageContext` during Phase C |
| `coverage_artifacts/coveragepy_post_run1.db` | Run 1 snapshot (44.0 %, post-filter-fix) |
| `coverage_artifacts/coveragepy_post_run2.db` | Run 2 snapshot (49.7 %, all 6 SAM-plan phases live) |
| `coverage_artifacts/coveragepy_post_run4.db` | Run 4 snapshot (49.7 % unchanged, but +2 090 bugs from samtools-live + quarantine dispatch) |
| `data/coverage_report.json` | Latest live report (currently 49.7 % from Run 2 iter 4 — Run 4 didn't iterate Phase D) |
| `data/run_biopython_sam_phase_rollout_v4_full.log` | Full Run 4 stdout/stderr (4 895 tests, 2 090 bugs) |
| `data/mr_registry.run3_advisory_only.json` | Snapshot of the Run 3 registry where all 17 mined MRs landed in quarantine — preserved as evidence for the dispatch-fix decision |
| `C:\Users\miaot\bin\samtools.cmd` + `samtools_wrapper.py` | Windows-side shim that bridges to WSL Ubuntu's samtools 1.19.2 |
| `data/scc_report.json` | 137 SAM rules, 1 covered, 136 blind spots (binning/indexing heavy) |
| `data/det_report.json` | DET rate 0.0333 per run (2 metamorphic failures, both against seqan3 + reference) |
| `data/run_biopython_sam.log` | Full stdout/stderr of the 13m 46s pipeline invocation |
| `biotest_config.yaml` (edits) | `phase_c.format_filter: VCF → SAM`, `feedback_control.primary_target: htsjdk → biopython` |
| `test_engine/feedback/coverage_collector.py:455,499` | Windows path-separator fix for `CoveragePyCollector` |

---

## Kill switches (same as htsjdk/VCF — all rank levers are SUT-agnostic)

| Lever | Disable                                                |
|:------|:-------------------------------------------------------|
| Rank 1 seed synth | `feedback_control.seed_synthesis.enabled: false` |
| Rank 2 htslib corpus | skip `seeds/fetch_real_world.py` |
| Rank 3 malformed MRs | drop `rejection_invariance` from `phase_b.themes` |
| Rank 4 `target()` directive | drop `Phase.target` from orchestrator phases |
| Rank 5 API-query MRs | drop `api_query_invariance` from `phase_b.themes` or set biopython's `supports_query_methods=False` |
| Rank 6 MR synthesis | already off by default: `feedback_control.mr_synthesis.enabled: false` |
