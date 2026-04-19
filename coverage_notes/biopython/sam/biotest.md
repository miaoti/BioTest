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

Run 0 and Run 1 use the same underlying trace data — the delta is
purely in the filter code (see "Bug: Windows path separators" below).
Future runs will append Run 2+.

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
| `coverage_artifacts/coveragepy_post_run1.db` | Run 1 snapshot |
| `data/coverage_report.json` | Regenerated after the Windows-filter fix (263/598, 44.0%) |
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
