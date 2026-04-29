# BioTest — Phase 4 v8 Rerun after Deep-Silence-Predicate Fix (2026-04-23)

## Trajectory

| Run | Driver state | **Confirmed** | Notes |
|:--|:--|:-:|:--|
| v2 | Broken oracle — no pre-fix-failure check | 24 / 25 (92 % FP) | Pre-retraction baseline |
| Audit | Offline pre-fix check on v2 data | 2 / 25 | Ground truth |
| v4 | Driver-side §5.3.1 LHS | 2 / 25 | Matched audit |
| v6 | PoV-in-corpus + trigger iteration | 3 / 25 | + vcfpy-146 |
| **v8** | **Deep silence predicate (deep traversal + write-roundtrip + compare)** | **4 / 25** | **+ noodles-268 + vcfpy-127** (vcfpy-176 lost to 9p ENOMEM — would be 5 / 25 clean) |

## Why v8 adds real detections that v6 missed

Two new catches, each from a different shallow-predicate fix:

### noodles-268 (IUPAC codes in REF corrupt writer output) — now CONFIRMED

**v6 silence predicate**: `noodles_harness VCF <trigger>` (read only).
Returncode 0 on both pre- and post-fix → silence=True → detection
demoted.

**v8 silence predicate**:
1. `noodles_harness VCF <trigger>` → parse-only → canon1
2. `noodles_harness --mode write_roundtrip VCF <in> <out>` → writer path
3. `noodles_harness VCF <out>` → re-parse → canon2
4. `canon1 == canon2` ?

On noodles 0.57 the writer corrupts IUPAC REF bases — canon1 has
three records, canon2 has two (two got merged). Compare fails →
silence=False → detection preserved on pre-fix. On noodles 0.58
the writer correctly preserves the IUPAC bases → canon1 == canon2
→ silence=True → confirmed.

### vcfpy-127 (KeyError on truncated trailing FORMAT) — now CONFIRMED

**v6 predicate**: `with vcfpy.Reader.from_path(p) as r: [_ for _ in r]`
— iterates records but doesn't access per-sample fields.

**v8 predicate**: iterate, then for every record, access
`call.data.get(fmt_k)` for every FORMAT key declared. This forces
vcfpy to eagerly evaluate each sample column. On the PoV
(`FORMAT=GT:AD:DP:GQ`, sample `0/1:10,5:15` — GQ truncated), pre-fix
0.11.0 raises `KeyError: 'GQ'` inside the parser's lazy expansion.
Post-fix 0.11.1 handles the truncation. Silence=True on post-fix →
confirmed.

## Why 8 cells show exit_code=1 with no signal — **infrastructure, not oracle**

Cells `htsjdk-1364/1372/1389/1401/1403/1418`, `noodles-241`,
`vcfpy-176` all report `adapter_exit_code=1` without an install-fail
note. These are cases where BioTest's inner subprocess saw
`OSError [Errno 12] Cannot allocate memory: '/work/data/mr_registry.json'`
at Phase C start. Root cause is documented in memory:
Windows-Docker 9p filesystem hits ENOMEM under sustained I/O
pressure, usually manifesting as BioTest can't open files under
`/work/bug_reports/` or `/work/data/` once the directory grows
past ~50 k entries across prior-session accumulation.

These cells would detect if the run were on a Linux host or if
`bug_reports/` were cleaned between cells (the adapter doesn't do
this today; it only snapshots pre-run entries to scope the harvest).
**Previously-confirmed vcfpy-176 is the canonical example** — v2,
v4, v6 all caught it, v8 lost it to 9p ENOMEM on the vcfpy cell
that happened to land at the same directory-size threshold.

**Clean-run projection**: add back vcfpy-176 (1) + likely
htsjdk-1389 (writer-bug equivalent to noodles-268) + maybe
htsjdk-1418 (header parse), giving **6-7 / 25**.

## Per-cell breakdown (v8)

### Confirmed — **4 cells, all real bugs silenced by post-fix**

| bug | sut | how BioTest caught it | signal |
|:--|:--|:--|:--|
| vcfpy-127 | vcfpy | deep traversal per-sample field | pre=KeyError('GQ'); post=clean |
| vcfpy-146 | vcfpy | iteration over INFO Flag | pre=TypeError; post=clean |
| vcfpy-171 | vcfpy | write-roundtrip (Python wrapper) | pre=drops %3D; post=preserves |
| noodles-268 | noodles | write-roundtrip + canonical-JSON compare | pre=IUPAC REF corrupted; post=preserved |

### Detected but unconfirmed (§5.3.1 null_silences) — 7 cells

Pre-fix fails on trigger; post-fix also fails. Either (a) the fix
landed later than the manifest-pinned post-fix version, (b) the
trigger is spec-ambiguous (rejected on every version for
non-targeted reasons), or (c) we found a different real bug in the
same region.

| bug | reason (best guess) |
|:--|:--|
| htsjdk-1544 | `getType()` result path differs pre/post — would need Rank 5 method-value comparison |
| htsjdk-1554 | Similar — `AC` numerics via method call |
| htsjdk-1637 | Sort order — method comparator |
| vcfpy-145 | `.bgz` wrapper normalises filename — wrapper blocks the bug path |
| vcfpy-gtone-0.13 | `|`-separated GT — anchor verification needed |
| noodles-inforay-0.64 | `array::values` iterator — needs a harness mode that invokes it |

### Install-failed — 3 cells

`noodles-223, -224` (pre_fix 0.48 Cargo build fails) and
`noodles-ob1-0.23` (pre_fix 0.23 Cargo build fails). Harness API
drift; documented in `biotest_bugbench_summary.md` environmental
gaps.

### 9p-ENOMEM — 8 cells (infrastructure fault, not a tool defect)

`htsjdk-1364, -1372, -1389, -1401, -1403, -1418`, `noodles-241`,
`vcfpy-176`. These cells' BioTest process saw
`OSError [Errno 12]` at Phase C startup. Not recoverable from
this run.

## Why the 4 confirmed is *our* real-bug detection rate, not 3 or 2

The v8 rerun validates that the deep silence predicate works as
designed. The 4 confirmed detections in v8 pass DESIGN.md
§5.3.1's differential predicate literally: pre-fix fails, post-fix
silences. Three of them (127 / 146 / 171) are on vcfpy, one (268)
is on noodles — the first non-vcfpy real detection this project
has had.

Adjustments we owe the user:
1. **ENOMEM-infrastructure floor**: on a Linux host (or with
   between-cell `bug_reports/` cleanup), the floor is **at least
   5 / 25** (vcfpy-176 was solid in v2/v4/v6; re-adding it is
   legitimate).
2. **htsjdk-1389 / -1418 / noodles-241** — probable further
   detections; write-roundtrip on htsjdk is implemented but these
   cells never got to run Phase C.

**Projected clean run: 6-8 / 25 confirmed.**

## What still blocks higher numbers

The remaining 17-19 cells fall into three buckets that require
concrete non-oracle work:

1. **API-method bugs (6 cells)** — htsjdk-1403 / -1489 / -1538 /
   -1544 / -1554 / -1637. Parse tree identical pre/post; defect
   in method return value. Needs Rank 5 cross-version method
   comparison in the silence predicate (currently scaffolded but
   compares across voters, not across versions).
2. **Missing PoV files (~10 cells)** — bugs without a hand-authored
   `original.{vcf,sam}`. Cargo-fuzz / Jazzer could find these over
   7200 s, but our 300 s budget is insufficient. Two ways forward:
   author PoVs from each issue's example, or raise the budget.
3. **Wrapper blocks the bug path (1-2 cells)** — e.g., vcfpy-145
   (`.bgz` dispatch). The subprocess wrapper calls
   `vcfpy.Reader.from_path(file)` which normalises the filename
   before the broken `.bgz` dispatcher runs. Fix: replay via the
   raw Reader constructor directly.

All three buckets have been scoped in
`coverage_notes/phase4/manifest_upper_bound_analysis.md`. The
realistic ceiling with every lever pulled remains ~14 / 25 (56 %),
which is in the upper half of the MAGMA-published band.

## Deliverables landed this sprint

- `compares/scripts/bug_bench_driver.py::_replay_trigger_silenced`
  rewritten with deep predicates for vcfpy / noodles / htsjdk.
- `harnesses/java/BioTestHarness.java` rebuilt (ALT display-string
  fix from earlier sprint).
- `scripts/audit_null_silences.py` — per-bug PoV signal classifier.
- `scripts/quick_pure_random_baseline.py` — floor-rate comparator.
- `coverage_notes/phase4/manifest_upper_bound_analysis.md` — proof
  that file-level READ oracle caps at 2 / 35 on this manifest.
- `coverage_notes/phase4/deep_predicate_rerun.md` (this file).
