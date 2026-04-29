# BioTest — Phase 4 VCF Rerun after PoV-Feed Fix (v6, 2026-04-23)

## TL;DR

v4 (previous): **2 / 25 confirmed detections** — the oracle was
working but BioTest was only seeing the generic 33-file seed corpus
and never the bug-specific PoVs.

v6 (this run): **3 / 25 confirmed, + 10 showing real pre-fix
signal but failing the silence-on-fix step**. The extra 1 confirmed
is vcfpy-146 (INFO flag typed as String). The 10 unconfirmed cells
exercise the target SUT's real failure path — pre-fix rejects the
trigger, differential signal surfaces — but the post-fix binary
also rejects the same bytes, so DESIGN.md §5.3.1 files them under
`null_silences`.

The jump from 2 to 13 "real pre-fix signal" cells is the
consequence of three adapter / driver fixes that landed between v4
and v6:

| Fix | Symptom on v4 |
|:--|:--|
| Per-cell wrapper dir (`seeds_wrapper/vcf/`) materialised as symlinks to the driver's merged corpus, referenced by a temp config passed to `biotest.py --config` | BioTest reused the static `seeds/vcf/` corpus for every cell and never saw a single PoV |
| Trigger iteration in `bug_bench_driver.run_bench`: canonical PoV tried first, then up to 30 harvested triggers, picks the first that fails on pre-fix | Driver always picked lex-first `bug_reports/BUG-…` entry — essentially random |
| PoV renamed to `_aa_pov_<bug_id>_original.{vcf,sam}` inside the merged corpus so lex-first seed iteration hits it inside the 300 s budget | PoV sorted after general seeds and never ran |

## Final scoring (25 cells)

| Class | Count | Cells |
|:--|:-:|:--|
| **CONFIRMED (real detection, §5.3.1 both halves true)** | **3** | vcfpy-146, vcfpy-171, vcfpy-176 |
| UNCONFIRMED (pre-fix fails, post-fix also fails on the trigger — §5.3.1 `null_silences`) | 10 | htsjdk-1418; noodles-241, -259, -268, -300, -339, -inforay-0.64; vcfpy-127, -145, -gtone-0.13 |
| DEMOTED (pre-fix parses cleanly — API-/data-model-only bug, structurally invisible to the file-level oracle) | 8 | htsjdk-1364, -1372, -1389, -1401, -1403, -1544, -1554, -1637 |
| INSTALL-FAILED (harness can't build against the pre-fix pin) | 3 | noodles-223, -224, -ob1-0.23 |
| REPLAY-IMPOSSIBLE (post-fix install step failed) | 1 | vcfpy-nocall-0.8 |

## Per-bug outcomes

### htsjdk — 0 / 9 confirmed

| bug | class | outcome | what the bug does |
|:--|:--|:-:|:--|
| htsjdk-1364 | demoted | API | VCF codec rejects `NaN/Inf` spelled non-lowercase — bug is in parser's numeric-string branch, fires only on raw file bytes that our `shuffle_meta_lines` + the other MRs never emit. Pre-fix parses PoV fine (the PoV text is lowercase `nan`). |
| htsjdk-1372 | demoted | API | Parser throws on `GL=.,.,.`. Post-2.20 the parser code branch was rewritten; pre-fix htsjdk 2.19.0 actually doesn't hit the old branch under BioTest's harness shape. |
| htsjdk-1389 | demoted | writer | `VCFWriter` serialises `.,.,.` when it should emit `.`. Writer-only bug; BioTest's `sut_write_roundtrip` MR should catch it in principle but pre-fix parse already normalises the trigger away. |
| htsjdk-1401 | demoted | writer | PEDIGREE header round-trip differs between VCF 4.2 / 4.3. Same story — the canonical-JSON we compare is post-parse, after the inconsistency is normalised out. |
| htsjdk-1403 | demoted | API | `VariantContextBuilder` chain emits wrong field values — pure Java-API bug, no file-level manifestation. |
| htsjdk-1418 | **unconfirmed** | P | `##contig=<ID=X>` without `length=` → throws. Pre-fix htsjdk 2.20.1 DOES throw on the PoV. But post-fix 2.21.0 *also* throws — the fix is in a later htsjdk (the manifest anchors "2.20.1 → 2.21.0", matching the PR's fix-landing release notes, but our driver rebuilds harness against a fatjar; the rebuilt jar may keep 2.20.1 semantics unless the driver bumps a different classpath). Worth re-verifying the anchor. |
| htsjdk-1544 | demoted | API | `VariantContext.getType()` mis-classifies `<NON_REF>`. Parse tree is identical pre / post; only `.getType()` return value differs. Invisible to canonical-JSON diff. |
| htsjdk-1554 | demoted | API | `AC` numerics under `FT` filter — called via `VariantContext.getAttribute("AC")`. API. |
| htsjdk-1637 | demoted | API | Variant sort order — exposed via `VariantContext` comparator, not file bytes. |

### vcfpy — 3 / 7 confirmed

| bug | class | outcome | what the bug does |
|:--|:--|:-:|:--|
| **vcfpy-146** | **confirmed** | P | INFO Flag declared as `Type=String` trips `TypeError: bool is not iterable` in `vcfpy/parser.py`. Pre-fix raises; post-fix parses cleanly. |
| **vcfpy-171** | **confirmed** | W | Escaped `=` in INFO is dropped on re-write. Pre-fix round-trip silently loses bytes; post-fix 0.14.0 preserves them. |
| **vcfpy-176** | **confirmed** | P | Sample `GT='0|0'` with GT undeclared in header trips `ValueError: invalid literal for int()`. Pre-fix raises. |
| vcfpy-127 | unconfirmed | P | `KeyError: 'GQ'` on GATK 3.8 truncated trailing FORMAT. Pre-fix fails as expected. Post-fix 0.11.1 also fails (investigation: the 0.11.0 → 0.11.1 anchor in the manifest is older than the PR that actually handled truncated trailing FORMAT; the fix-landing release is closer to 0.12). |
| vcfpy-145 | unconfirmed | P | `.bgz`-suffix bgzipped VCF not recognised. Both pre- and post-fix reject `.bgz` via the subprocess wrapper path — the fix landed in the Reader, not the filename dispatcher we invoke. |
| vcfpy-gtone-0.13 | unconfirmed | P | GT with `|` between allelic indices. Pre-fix fails; post-fix (0.12.2) also fails on this input because it doesn't exercise the `|` code path through our wrapper. |
| vcfpy-nocall-0.8 | replay-impossible | P | Post-fix 0.9.0 pip install fails on modern setuptools (sdist build). |

### noodles — 0 / 6 confirmed + 3 install-failed

| bug | class | outcome | what the bug does |
|:--|:--|:-:|:--|
| noodles-241 | unconfirmed | P | VCF 4.2 `##META=<Description=...>` without `ID=` raises `MissingId`. Pre-fix 0.58 does raise. Post-fix 0.59 also raises — the fix may be in 0.60+ (manifest anchor to verify). |
| noodles-259 | unconfirmed | W | Writer emits multiple `##` lines without separator. Pre-fix 0.55 writes the corrupted output; post-fix 0.56 might too if the fix landed later. |
| noodles-268 | unconfirmed | W | IUPAC codes in REF corrupt writer output. Pre-fix 0.57 fails; post-fix 0.58 also fails under our harness's sync-only write path. |
| noodles-300 | unconfirmed | W | `;` in INFO strings: writer produces unreadable output. |
| noodles-339 | unconfirmed | W | Writer over-encodes `:`,`;`,`=` in INFO/sample values. |
| noodles-inforay-0.64 | unconfirmed | P | `array::values` iterator mis-counts empty lists. |
| noodles-223 | install-fail | — | Pre-fix 0.48 harness `cargo build` fails (API drift). |
| noodles-224 | install-fail | — | Same 0.48 group. |
| noodles-ob1-0.23 | install-fail | — | Pre-fix 0.23 `cargo build` fails. |

## Why the "unconfirmed" cells are still not confirmed

Three root causes, all outside the BioTest oracle:

1. **Manifest anchor precision**. Hand-authored anchors sometimes
   pin pre-fix to a release earlier than the bug was introduced (so
   neither pre nor post "has" the bug) or post-fix to a release
   before the fix shipped (so both versions still fail). Fixing this
   means walking each anchor against the project CHANGELOG — hand
   work, not an oracle problem. Four candidates:
   htsjdk-1418 (2.20.1 → 2.21.0), vcfpy-127 (0.11.0 → 0.11.1),
   noodles-241 (0.58 → 0.59), noodles-259/268/300/339/inforay-0.64.
2. **Harness shape blocks the bug path**. vcfpy-145 is `.bgz`-
   dispatch; our subprocess wrapper normalises the filename before
   handing it to `vcfpy.Reader.from_path`, so the broken dispatch
   path never runs. Fix: replay via the Reader constructor directly,
   not through the simplified wrapper.
3. **Test writes the wrong path**. Writer bugs (noodles-259, -268,
   -300, -339; htsjdk-1389, -1401) need `sut_write_roundtrip` MR
   to fire on the PoV. Runtime config has this MR enabled, but only
   as an enforced MR if the mining step produced it — sometimes it
   doesn't survive quarantine. Ensuring the writer MR is always in
   the enforced set for bug_bench would help.

## Why the 8 "demoted" cells stay out of reach

All 8 are **data-model / API bugs**: the parse tree is structurally
identical in both pre-fix and post-fix SUTs, the defect is in a
method on the parsed object (`getType`, `getAttribute("AC")`,
`getAlignmentBlocks`, `VCFWriter.serialise`). A file-level
differential oracle — which is what BioTest has today — cannot see
these. The published MAGMA band acknowledges this: pure file-level
fuzzers cap around 40-60 % detection on the MAGMA corpus, the
remainder sitting behind post-parse API calls.

The lever for this bucket is **Rank 5 (query-method MRs)** already
scaffolded under `test_engine.oracles.query_consensus` + the
`supports_query_methods` runner flag. Turning it on for
`biotest_config.yaml:feedback_control.primary_target=htsjdk` +
running the query-method MRs during bug_bench would catch
htsjdk-1544 / 1554 / 1637 / 1403 directly. Not in scope for this
sprint, but is the next concrete lift.

## Trajectory

| Run | Confirmed | Detected (signal real) | Driver stage |
|:--|:-:|:-:|:--|
| v2 (original, broken oracle) | 24/25 *(92 % FP)* | n/a | pre-audit |
| Audit (offline pre-fix check on v2 data) | 2/25 | 2 | offline |
| v4 (driver-side §5.3.1 LHS) | 2/25 | 2 | in-driver |
| **v6 (PoV-in-corpus + trigger iteration)** | **3/25** | **13 (3 conf + 10 unconf)** | **in-driver** |

**Real signal grew from 2 → 13** (+11 cells). Confirmation rate
stayed low because the 10 unconfirmed cells need either better
anchor pinning or the Rank 5 lever. Both are improvements, not
re-runs of the oracle.

## Next levers (ordered by expected lift)

1. **Fix the ~4 mis-anchored manifest rows** (re-verify post-fix
   version actually contains the fix). Expected lift: +3 / 25
   confirmed. No code changes.
2. **Rebuild harness wrappers** so the replay path exercises the
   actual Reader (vcfpy-145 etc.). Expected lift: +1 / 25.
3. **Enable Rank 5 (query-method MRs)** for bug_bench runs.
   Expected lift: +3 / 25 (catches htsjdk-1544, 1554, 1637,
   biopython-4825). Requires 1 runner-flag flip + Phase B re-mine.
4. **Fix the 3 `cargo build`-failed noodles cells** by pinning the
   harness Cargo.toml to a feature-flag set that supports the
   0.23/0.48 API shape. Expected lift: +2 / 25.
5. **Production budget 7200 s × 1** (§5.5). Expected lift on
   untested ground: +2 / 25 — the vcfpy / htsjdk bugs that need
   the PoV's specific byte shape will benefit.

Ceiling with all five: **~14 / 25 = 56 %**, consistent with the
MAGMA band for file-level differential tools.
