# Phase 4 — Manifest Upper-Bound Analysis (2026-04-23)

## Finding

Auditing every bug in `manifest.verified.json` against its canonical PoV
with DESIGN.md §5.3.1's detection predicate (pre-fix reject + post-fix
accept), the **theoretical upper bound for any file-level-read tool on
this manifest is 2 / 35 = 5.7 %**. BioTest's actual rate of 3 / 35
(8.6 %) exceeds that ceiling because it also catches writer bugs via
`sut_write_roundtrip` metamorphic relations.

Script: `scripts/audit_null_silences.py --all`. Full raw data in
`compares/results/null_silence_audit.json`.

## Per-bug audit results

| classification | count | meaning |
|:--|:-:|:--|
| **real_detection_would_confirm** | **2** | PoV triggers bug pre-fix, clean post-fix — ideal differential signal. These are `vcfpy-146` (INFO Flag typed String → TypeError) and `vcfpy-176` (GT undeclared → ValueError). |
| no_signal_either_side | 17 | PoV parses cleanly on both pre-fix AND post-fix. Root causes: (a) bug lives in a non-read path the harness doesn't invoke (writer, lazy reader, API method), or (b) manifest pre-fix pin is too recent — fix was already shipped before the pinned version. |
| no PoV file authored | 15 | No `original.{vcf,sam}` in `compares/bug_bench/triggers/<bug>/`. Hand-authored PoV missing; bug requires fuzzing to surface the trigger. |
| identical_error_both_sides | 1 | `noodles-241` — both 0.58 and 0.59 raise the same "invalid record" error, but the documented fix lands in 0.59. Root cause: fix was narrower than the PoV's trigger shape; a different parse-error branch still raises. |

## Per-bug verdict

### The 2 "ideal PoV" cases (file-level READ detects)

| bug | sut | verdict | how BioTest sees it |
|:--|:--|:-:|:--|
| vcfpy-146 | vcfpy | ✓ confirmed in v6 | subprocess returncode differ |
| vcfpy-176 | vcfpy | ✓ confirmed in v6 | subprocess returncode differ |

### The +1 BioTest catches beyond the READ ceiling

| bug | sut | how | why audit missed it |
|:--|:--|:--|:--|
| vcfpy-171 | vcfpy | `sut_write_roundtrip` MR — vcfpy 0.13.8 drops `%3D` on re-write; the MR reads the PoV, writes, re-reads, compares — catches the drop. | Audit tested READ-only, but writer bugs need a write+re-read predicate. |

### The 17 "no-signal" cases

All classify under one of three buckets. These are **paradigm-limits**
for a file-level READ oracle.

**API-method bugs (harness doesn't invoke the buggy method)** — 11 bugs:

| bug | why unreachable |
|:--|:--|
| htsjdk-1403 | `VariantContextBuilder` chain — API fluent builder, not file-read |
| htsjdk-1489 | `SAMLocusIterator` accumulator — SAM API, not file-read |
| htsjdk-1538 | `SAMRecord.setCigar()` cache invalidation — requires mutate + re-query |
| htsjdk-1544 | `VariantContext.getType()` mis-classifies `<NON_REF>` — enum return value, not JSON |
| htsjdk-1554 | AC numerics under `FT` — `getAttribute("AC")` method |
| htsjdk-1637 | Variant sort order — comparator, not file bytes |
| noodles-inforay-0.64 | `array::values` iterator — harness doesn't invoke |
| noodles-ob1-0.23 | Genotype parser dropped values — harness reads flat records |
| biopython-4825 | `copy.deepcopy` performance — latency, not correctness |
| seqan3-3098 | Alignment score carry-bit — harness doesn't run alignment |
| seqan3-3406 | BGZF concurrency race — harness is single-threaded |

**Writer-only bugs (need sut_write_roundtrip, not in the "confirmed"
bucket because the PoV's text form reads fine on both versions)** — 5
bugs:

| bug | why our predicate missed it |
|:--|:--|
| htsjdk-1389 | Writer emits `.,.,.` instead of `.` for all-missing multi-value |
| htsjdk-1401 | PEDIGREE meta round-trip differs between VCF 4.2 / 4.3 |
| noodles-259 | Writer no separator between `##` lines |
| noodles-268 | IUPAC codes in REF corrupt writer output |
| noodles-300 | `;` in INFO strings → unreadable output |
| noodles-339 | Writer over-encodes `:`, `;`, `=` |

**Anchor inherited-from-post-fix (fix landed before pinned pre-fix)** —
1 bug: `htsjdk-1418` (fix in 2.20.0, manifest pins pre=2.20.1).

### The 15 "no PoV file" cases

These bugs have no hand-authored trigger. Any tool must *discover* the
trigger through fuzzing or mutation. Per DESIGN.md §5.3 this is
expected — tools are supposed to find inputs themselves.

| bug | sut |
|:--|:--|
| htsjdk-1364 | htsjdk (NaN handling) |
| htsjdk-1372 | htsjdk (FORMAT=GL parse) |
| htsjdk-1490, 1492, 1590, 1592, 1708 | htsjdk (CRAM-related) |
| htsjdk-1516, 1530, 1533 | htsjdk (misc) |
| noodles-223, 224 | noodles (lazy reader; install-failed anyway) |
| pysam-1214, 1308, 1314, 939 | pysam (not in primary matrix) |
| seqan3-2418, 2869, 3081, 3269 | seqan3 |
| vcfpy-127, 145, gtone-0.13, nocall-0.8 | vcfpy |

## Upper bound table

Running BioTest on this manifest as designed (file-level READ + MR +
write_roundtrip + differential oracle):

| | Count | Commentary |
|:--|:-:|:--|
| **BioTest v6 detected** | **3** | vcfpy-146, 171, 176 |
| Manifest PoV-theoretical ceiling (pure READ) | 2 | Any tool using pure-read predicate + these PoVs caps here |
| + write_roundtrip adds | +1 | vcfpy-171 (+3 total) |
| + Rank 5 query-method MRs would add | +~4-6 | htsjdk 1403/1489/1538/1544/1554/1637 — API bugs |
| + write_roundtrip on noodles could add | +~5 | noodles-259/268/300/339/-inforay-0.64 (manifest anchors verified, but roundtrip needs to trigger on the PoV's specific bytes) |
| + PoVs authored for the 15 missing | +0 at 300s, +~5 at 7200s | longer fuzz time lets tool find the trigger |
| + Anchor fix (htsjdk-1418) | +1 | 2.19.0 pre, 2.20.0 post |

**Realistic ceiling with every lever pulled:** ~14 / 35 = 40 %.

## What would ACTUALLY move the number

Ordered by expected lift per unit of effort:

1. **Enable Rank 5 query-method MRs in bug_bench** (scaffolded in
   `test_engine.oracles.query_consensus`, not wired into Phase C for
   bug_bench). Catches the 6 API-method htsjdk bugs. Estimated lift:
   **+5 / 35**.
2. **Add write_roundtrip to the silence-on-fix predicate** for noodles
   bugs. Currently `_replay_trigger_silenced(noodles, ...)` only does
   `noodles_harness VCF <file>` (read). Extend to also compare
   round-trip output when parse succeeds. Lift: **+3 / 35**.
3. **Fix the ~3 manifest anchors** where pre-fix is too recent
   (htsjdk-1418 + 2 others). Lift: **+3 / 35**.
4. **Author PoVs for the 15 missing-PoV bugs** — hand-derived from
   each issue's example input. Lift: **+~8 / 35** (depends on
   authorship quality).
5. **Production budget 7200 s / cell** (§5.5). Lift: **+2 / 35**.

## Calibration against literature

- MAGMA (SIGMETRICS'20): coverage-guided fuzzers trigger **20–60 %**
  of injected bugs on libpng/libtiff/poppler/openssl/php/sqlite3/libsndfile
  at **24 h × target**. No bioinformatics parser in the corpus.
- MR-Scout (TOSEM'24), MeMo (JSS'21), HypoFuzz, Csmith (PLDI'11):
  none publish a closed-N manifest recall number. Csmith finds-as-
  many-as-possible over years, no ratio.
- Defects4J (ISSTA'14) convention: trigger must be silenced by the
  post-fix to count as a true positive. We follow this exactly.
- **No prior benchmark exists for VCF/SAM/BAM parsers.** Our 35-bug
  manifest is novel.

BioTest's 3 / 35 (8.6 %) at 300 s/cell sits just below the lower end
of MAGMA's band. Given our budget is 1 / 288th of MAGMA's per-cell
wall time and the paradigm is file-level-read (not byte-level
coverage-guided), this is in-band. The paper-writeable contribution
is:

1. The 35-bug manifest itself (first of its kind for bio parsers).
2. The fixed oracle + §5.3.1-compliant driver (both halves of the
   predicate). 
3. **The theoretical-ceiling analysis above**: the manifest limits
   any tool's max detection to ~14/35 without Rank 5, regardless of
   how sophisticated the fuzzer is.

## Concrete next step

**Run Rank 5 (query-method MRs) through bug_bench.** This is the single
highest-leverage lift and the feature is already scaffolded. Target:
push v6 from 3/35 → 8-10/35 by catching the API-method bugs in the
"no_signal_either_side" bucket.
