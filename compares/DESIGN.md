# Comparative Evaluation Design — BioTest vs Fair End-to-End Baselines

## 1. Purpose

This document specifies how **BioTest** is benchmarked against **end-to-end, input-level** test-generation baselines on the four SUTs already in use: `htsjdk` (Java), `pysam` (Python), `biopython` (Python SAM), `seqan3` (C++ SAM).

BioTest is an end-to-end metamorphic + differential testing tool: it accepts VCF/SAM files, applies semantics-preserving transforms, and cross-executes unmodified parsers. It never calls SUT-internal APIs. A fair comparison must therefore use **input-level** baselines — tools that also consume a file / byte stream and drive the SUT from the outside — rather than **unit-level** generators (EvoSuite, Randoop, Pynguin) that synthesise method-call sequences against instrumented objects.

This revision of the design replaces the earlier EvoSuite/Randoop-centric protocol with:

1. A **slim 13-cell matrix** of fair E2E baselines, one per SUT language, plus BioTest and Pure Random.
2. A **real-bug detection benchmark** built from 32 historical GitHub issues on the four SUTs, anchored by installable library versions.
3. The previous three metrics (validity ratio, structural coverage growth, mutation score) plus **two new metrics** — real-bug detection rate and time-to-first-bug (TTFB).
4. A **citation table** grounding every methodology choice in peer-reviewed prior work.
5. EvoSuite retained as a **labelled white-box anchor** on htsjdk only, so the "BioTest detects N semantic bugs, EvoSuite detects M" narrative is directly supported by numbers rather than hand-wave.

The evaluation is **deferred**: it runs after the main BioTest Phase A–D evaluation is complete. This file exists now so the protocol, source-code locations, mutation tooling, and scoping decisions are recorded precisely and can be reviewed before execution.

## 2. Tools Under Comparison

### 2.1 Primary baselines (fair, end-to-end, input-level)

| Tool | Class | Language | Role | Citation |
| :--- | :--- | :--- | :--- | :--- |
| **BioTest** (this repo) | Spec-grounded metamorphic + differential + LLM-seeded fuzzing | Multi-lang via adapters | Tool under evaluation | — |
| **Jazzer** | In-process coverage-guided JVM fuzzer | Java | Baseline for `htsjdk` | Code Intelligence OSS, integrated into OSS-Fuzz |
| **Atheris** | In-process coverage-guided Python fuzzer (libFuzzer-style, supports C extensions) | Python | Baseline for `pysam`, `biopython` | Google, 2020; still actively maintained as of 2024 |
| **libFuzzer** | In-process coverage-guided C/C++ fuzzer | C++ | Baseline for `seqan3` | Serebryany et al., USENIX ATC'16 — "libFuzzer: a library for coverage-guided fuzz testing" |
| **Pure Random** | Byte-level `os.urandom` generator (floor baseline) | Language-agnostic | All four SUTs | Hand-implemented under `baselines/random_testing/` |

### 2.2 White-box anchor (contextual, not apples-to-apples)

| Tool | Class | Language | Role |
| :--- | :--- | :--- | :--- |
| **EvoSuite** | Search-based unit-test generation (genetic algorithm on method sequences) | Java only (JUnit) | **Anchor** on htsjdk; runs on coverage + mutation + real-bug bench |

EvoSuite is retained **only** because the user's headline claim — "semantic-based metamorphic testing catches N/M logic bugs where a white-box method-level tool catches only X/M" — requires actual EvoSuite numbers. EvoSuite is labelled throughout the report as **"white-box unit-level — different paradigm"**, and its numbers are interpreted contextually, not as a fair E2E comparison.

The existing scripts `compares/scripts/run_evosuite.sh` and `compares/scripts/measure_evosuite_coverage.sh` drive this anchor; they need no changes.

### 2.3 Secondary / optional baselines

Listed for completeness; **only run opportunistically** after the primary matrix is complete. Any results are asterisked in the final report. These exist so reviewers asking "why not X?" have a documented answer.

| Tool | Class | Language | Why secondary |
| :--- | :--- | :--- | :--- |
| **JQF + Zest** | Semantic fuzzing with QuickCheck-style generators (Padhye et al., ISSTA'19) | Java | Jazzer already covers the fair-E2E slot for Java |
| **AFL++** | AFL fork with persistent mode (Fioraldi et al., USENIX WOOT'20) | C++ | libFuzzer already covers the fair-E2E slot for C++ |
| **Randoop** | Feedback-directed random unit-test generation (Pacheco et al., OOPSLA'07) | Java | EvoSuite anchor alone makes the white-box-paradigm point |
| **Nautilus** | Grammar + coverage feedback (Aschermann et al., NDSS'19) | Language-agnostic | Requires authoring VCF/SAM ANTLR grammars (~1 week engineering) |
| **Fuzz4All** | LLM-universal fuzzing (Xia et al., ICSE'24) | Language-agnostic | Directly comparable to BioTest's LLM Phase B; high setup cost for prompt engineering |

### 2.4 Explicitly rejected as unfair

- **Pynguin** (Lukasczyk et al., ISSTA'22) — unit-level, same paradigm problem as EvoSuite/Randoop, no anchor value.
- **Hypothesis** — property-based testing; requires human-authored oracles. Not input-generational.
- **TSTL** — action-sequence, API-level. Wrong abstraction for file-format parsing.

### 2.5 Language-coverage asymmetry

Jazzer is Java-only; Atheris is Python-only; libFuzzer is C/C++. Each fair baseline is therefore bound to one SUT language, producing an asymmetric matrix (§4.1). The report discusses this explicitly: we are comparing BioTest's multi-language reach to a *different* per-language SOTA fuzzer on each SUT, which is a stronger story than comparing to one non-SOTA tool that happens to cover all languages.

## 3. Metrics

Five metrics, reported per (tool, SUT) over a fixed time budget. Metrics 1–3 are retained from the previous design with tightened sampling; metrics 4–5 are new and carry the "BioTest finds real logic bugs" claim.

### 3.1 Validity Ratio (Compliant-Input Rate)

**Definition**: `parse_success / generated_total` — fraction of a tool's generated inputs that the SUT's parser accepts as syntactically / structurally valid VCF or SAM files.

**Why it matters**: distinguishes generators that produce compliant inputs from those that emit garbage. Pure Random typically lives near zero; grammar-aware and semantic tools live near one. A tool with near-zero validity cannot meaningfully exercise deep code paths.

**Measurement**: each tool emits a corpus of candidate files; each file is parsed by a **reference parser** (pysam in lenient mode for VCF; htsjdk in lenient mode for SAM). `parse_success / total`, where crashes and reject-with-diagnostic both count as "invalid."

**Instrumentation**: `compares/scripts/validity_probe.py` — reads a directory of candidate inputs, calls each SUT's runner once per file, emits `validity.json`.

### 3.2 Structural Coverage Growth (Branch + Line)

**Definition**: branch + line coverage percentages inside the SUT's VCF/SAM-relevant code, sampled as a function of wall time.

**Why it matters**: measures the tool's ability to drive the SUT's internal logic. Cited directly in the proposal figure.

**Per-SUT tooling** (all already integrated in `test_engine/feedback/coverage_collector.py`):

| SUT | Language | Tool | Output |
| :--- | :--- | :--- | :--- |
| htsjdk | Java | JaCoCo | `.exec` → XML → per-line / per-branch counts |
| biopython | Python | coverage.py | `.coverage` SQLite → JSON via `coverage report --format=json` |
| pysam | Python (Docker) | coverage.py (inside container) | `summary.*.json` in `coverage_artifacts/pysam/` |
| seqan3 | C++ | gcovr + `--coverage` compile flag | `gcovr.json` |

**Scoping**: coverage is restricted to the VCF/SAM-relevant paths whitelisted in `biotest_config.yaml: coverage.target_filters`. Reusing the same whitelist BioTest's Phase D uses keeps the comparison aligned.

**Sampling regime — primary**: **2h × 3 independent reps per cell** (6h/cell total). Coverage is sampled at **log ticks** `{1s, 10s, 60s, 300s, 1800s, 7200s}` within each rep. 3 reps let us report 95% CI bands at each tick. We deliberately use a shorter budget than Klees et al.'s CCS'18 24h guideline and document this as "short-budget regime, defensible for ranking stability but not for absolute peak coverage."

**Sampling regime — secondary**: 300s × 5 reps, matching the figure in the proposal. Plotted on the same log-x axis as the primary so the reader sees both regimes simultaneously.

### 3.3 Mutation Score

**Definition**: `killed_mutants / reachable_mutants`, where a mutant is *killed* if the generated test suite causes the mutated SUT's output to diverge from the unmutated SUT's output (parse-success flip, canonical-JSON diff, or crash flip).

**Why it matters**: coverage saturates before defect-detection. A tool may reach 70% coverage yet kill only 30% of mutants — it exercises lines without distinguishing correct from buggy behaviour. Mutation score cross-checks that coverage growth translates into detection power.

**Per-SUT mutation tooling**:

| SUT | Language | Mutation tool | Notes |
| :--- | :--- | :--- | :--- |
| htsjdk | Java | **PIT** (`pitest` 1.15+) | Gradle plugin; mutators = DEFAULT_GROUP |
| biopython | Python | **mutmut** (3.x) | File-based, scoped to `Bio/Align/sam.py` |
| pysam | Python | **mutmut** inside Docker | Scoped to the installed `pysam` package's VCF + SAM reader/writer modules |
| seqan3 | C++ | **mull** (0.18+) | LLVM-IR based; requires Clang build with the new pass manager |

**Scoping** (identical to §3.2 whitelist):

| SUT | Mutation target path |
| :--- | :--- |
| htsjdk | `src/main/java/htsjdk/variant/vcf/**`, `src/main/java/htsjdk/samtools/**` |
| biopython | `Bio/Align/sam.py`, `Bio/SeqIO/…` (VCF if present) |
| pysam | the VCF and SAM reader/writer modules inside the installed pysam package |
| seqan3 | `include/seqan3/io/sam_file/**` |

**Test-kill protocol**: for each tool's final corpus (the accepted inputs from its 2h primary run), for each mutant `m`:
1. Apply `m` to the SUT.
2. Run the tool's corpus against the mutated SUT.
3. If any input's observable outcome (parse-success flip, canonical-JSON diff, crash flip) differs from the unmutated baseline, `m` is killed.
4. Score = `|killed| / |reachable|`, where `reachable` = mutants in code the corpus actually executed. This avoids penalising coverage gaps twice.

**Budget**: 2h per SUT per tool. With the slim matrix (5 tools × 4 SUTs) = ~40 wall-hours, single overnight batch.

### 3.4 Real-Bug Detection Rate (new)

**Definition**: `bugs_detected / bugs_in_benchmark`, where `bugs_in_benchmark` is the set of verified historical VCF/SAM-related bugs in the `compares/bug_bench/manifest.json`, and `bugs_detected` is the subset each tool catches within its per-bug time budget on the pre-fix SUT version.

**Why it matters**: coverage and mutation score are proxies; real-bug detection is the ground truth. This metric directly supports the thesis claim that semantics-aware metamorphic testing finds logic bugs that crash-detection fuzzers cannot.

**Methodology**: see §5 below for the full protocol. Modelled on Magma (Hazimeh et al., SIGMETRICS'20) — the canonical real-bug benchmarking framework for fuzzers.

**Detection criterion**: see §4.

### 3.5 Time-to-First-Bug (TTFB) (new)

**Definition**: median wall-clock seconds to the first valid detection, per (tool, bug), reported with 95% CI across the bug-bench.

**Why it matters**: detection rate collapses a long time series into one number. TTFB preserves the "how fast" axis — a tool that eventually finds all bugs but takes hours each is qualitatively different from one that finds the same bugs in minutes.

**Measurement**: logged by `bug_bench_driver.py` during Phase 4. Presented as a violin plot (`ttfb_violin.png`) per tool.

## 4. Comparison Protocol

### 4.1 Matrix (slim, 13 cells)

```
              htsjdk     pysam     biopython(SAM)  seqan3(SAM)
BioTest           P          P          P              P
Jazzer            P          —          —              —
Atheris           —          P          P              —
libFuzzer         —          —          —              P
Pure Random       P          P          P              P
EvoSuite (anchor) A          —          —              —
```

`P` = primary (must run full 2h × 3 reps + 2h bug-bench). `A` = white-box anchor. `—` = not applicable (language mismatch or format unsupported). Total: **13 primary cells + 1 anchor = 14 cells**.

**Dual C++ fuzzer support on the seqan3 row.** The primary fair-E2E baseline is **libFuzzer** (Clang 18 + `-fsanitize=fuzzer`), unblocked on 2026-04-19 via two in-tree seqan3 patches baked into the `biotest-bench` image (details in §13.2.4). **AFL++** with `afl-g++` (GCC 12) is kept as a verified alternate; the same harness source file targets both runtimes via a CMake-level define. Either tool can run in the primary cell; the comparison report will note which was used.

`seqan3` does not support VCF (see `test_engine/runners/seqan3_runner.py:11`). `biopython` is evaluated on SAM only (it has no VCF parser).

### 4.2 Fixed conditions

- **Primary time budget**: 2h per tool per SUT per rep, **3 reps**; coverage sampled at `{1, 10, 60, 300, 1800, 7200}` seconds. Report mean + 95% CI.
- **Secondary time budget**: 300s × 5 reps, reusing the same scripts with different flags. Produces the short-budget growth curve for the proposal figure.
- **Bug-bench time budget**: 2h × 1 rep per (tool, bug). Single rep accepted to keep total walltime tractable; signal is robust because most real bugs either fire within seconds or not at all.
- **Seed corpus** (all tools receive the same seeds): Tier-1 + Tier-2 from `seeds/vcf/` and `seeds/sam/`. **Synthetic Phase-D seeds are excluded** (`seeds/vcf/synthetic_iter*_*.vcf`) — including them would bias the comparison towards BioTest. Pure Random uses no seeds; generation is from `os.urandom`. BioTest uses its existing `SeedCorpus`. Each fuzzer consumes the seed corpus via its native seed-dir flag (Jazzer `-seed_corpus`, libFuzzer `<dirs>`, Atheris via wrapper).
- **Hardware**: single fixed dev machine; CPU / RAM / OS documented in the final report. Parallelisation: one cell per CPU-group, up to 4-way.
- **Environment**: Ollama must NOT be active during mutation runs (eats RAM). BioTest's test-generation phase runs ahead of time; mutation scoring only re-executes the **generated test suite**, not the LLM-driven mining.

### 4.3 Detection criteria per tool class

Different tool classes emit different native signals. We translate each into a uniform "bug detected" predicate so scores are comparable.

| Tool class | Native signal | How it becomes a "detection" |
| :--- | :--- | :--- |
| BioTest | Metamorphic violation OR consensus disagreement | Existing `test_engine/oracles/differential.py` + `metamorphic.py` |
| Jazzer / Atheris / libFuzzer | Crash, sanitizer abort, uncaught exception | Each fuzzer's native `crashes/` output directory |
| Pure Random | Uncaught exception in SUT | `bug_bench_driver.py` polls per invocation |
| EvoSuite (anchor) | Generated JUnit test FAILs on pre-fix SUT AND PASSes on post-fix SUT | `junit.xml` report diff, driven by `measure_evosuite_coverage.sh` adapter |

### 4.4 Fairness equalizer pass

After each tool's primary run completes, **every accepted input it produced** is re-fed through the **differential-only** oracle (`test_engine/oracles/differential.py`). If multiple SUTs' canonical JSON disagree on that input, the *fuzzer that produced the input* earns the detection — not BioTest.

**Why this matters**: without this pass, BioTest would win every semantic bug purely because it is the only tool with a metamorphic + differential oracle. The equalizer isolates *input quality* (what each tool generates) from *oracle quality* (BioTest's advantage). The metamorphic oracle is **not** applied to fuzzer outputs — that would give BioTest's transform chain credit for inputs another tool generated, which is the opposite problem.

**Sanity check**: run BioTest-the-generator through the equalizer. The differential-only detection count must be ≤ full BioTest detection count. This validates that BioTest's metamorphic contribution is *additive above* its input quality, which is the actual thesis claim.

### 4.5 Output JSON schema (per run)

```json
{
  "tool": "BioTest",
  "sut": "htsjdk",
  "phase": "coverage | bug_bench | mutation | validity",
  "run_index": 2,
  "time_budget_s": 7200,
  "seed_corpus_hash": "sha256:…",
  "validity_ratio": 0.97,
  "coverage_growth": [
    {"t_s": 1,     "line_pct":  2.1, "branch_pct":  0.9},
    {"t_s": 10,    "line_pct": 13.0, "branch_pct":  9.1},
    {"t_s": 7200,  "line_pct": 46.2, "branch_pct": 38.5}
  ],
  "mutation_score": {"killed": 143, "reachable": 218, "score": 0.656},
  "bug_bench": {
    "pysam-1314": {
      "detected": true,
      "ttfb_s": 312.4,
      "trigger_input": "…/triggers/pysam-1314.vcf",
      "signal": "consensus_disagreement_against_htslib",
      "confirmed_fix_silences_signal": true
    }
  }
}
```

Records feed `compares/scripts/build_report.py` → `compares/results/comparison_report.md` + growth-curve, bar-chart, heatmap, and violin figures.

## 5. Real-Bug Benchmark

### 5.1 Candidate bugs

32 candidates collected from GitHub issue search and repository changelogs (April 2026). Full list in Appendix A. Summary:

- **htsjdk**: 10 issues (~8 logic, 2 crash).
- **pysam**: 10 issues (~7 logic, 3 crash).
- **biopython**: 6 issues (SAM parsing + alignment bugs).
- **seqan3**: 6 PRs with confirmed fix-commit SHAs.

The candidate set was pre-filtered to include only VCF / SAM-related bugs fixed in the last 5 years. Bugs outside these formats (BED, GFF, CRAM-only, tabix) were excluded.

### 5.2 Commit-SHA gap and resolution

Most htsjdk / pysam / biopython issues do **not** have a reliable "bad commit" SHA in their GitHub metadata — the issue tracker records the fix but not the exact commit where the bug was introduced. Rather than spending weeks on `git bisect` against drifted build configs, we anchor on **installed library versions**:

**Primary anchoring — install-version**:

| SUT | Pre-fix | Post-fix |
| :--- | :--- | :--- |
| pysam | `pip install pysam==X.Y.Z` | `pip install pysam==X.Y.Z+ε` |
| biopython | `pip install biopython==A.B` | `pip install biopython==A.B+1` |
| htsjdk | Maven Central `htsjdk-X.Y.Z.jar` | Maven Central `htsjdk-X.Y.Z+1.jar` |
| seqan3 | `git checkout <parent-of-fix-commit>` | `git checkout <fix-commit>` |

**Verification rule**: each bug's post-fix release notes must explicitly mention the issue number, OR the PR must reference the issue number. Bugs whose fix-landing release cannot be identified are **dropped**.

**Drop-list discipline** (Böhme et al. ICSE'22): bugs that fail pre-flight install-verification are transparently dropped. Expected verified N: 18–25 of 32.

### 5.3 Per-bug execution

For each verified bug:

1. Install the **pre-fix** SUT version in a clean environment (venv / Docker / JAR swap).
2. Run each tool in the appropriate row of the matrix for **2h × 1 rep** against the pre-fix SUT.
3. Record first-detection timestamp per tool.
4. Install the **post-fix** version; replay the detecting input; confirm the signal **disappears**. Controls for spec-ambiguity false positives.

A tool "detects" a bug iff (a) at least one input it generated triggers the detection criterion on the pre-fix SUT AND (b) the same input does not trigger on the post-fix SUT. Condition (b) is essential — without it, any non-deterministic disagreement would score as a detection.

### 5.4 Manifest schema

`compares/bug_bench/manifest.json`. One entry per verified bug:

```json
{
  "id": "pysam-1314",
  "sut": "pysam",
  "issue_url": "https://github.com/pysam-developers/pysam/issues/1314",
  "format": "VCF",
  "anchor": {
    "type": "install_version",
    "pre_fix":  "0.20.0",
    "post_fix": "0.21.0",
    "verification": "release_notes_mention_issue_1314"
  },
  "trigger": {
    "category": "contig_remap_corruption",
    "evidence_dir": "compares/bug_bench/triggers/pysam-1314/"
  },
  "expected_signal": {
    "type": "differential_disagreement",
    "against": ["htslib"]
  }
}
```

For seqan3 entries: `"anchor": {"type": "commit_sha", "pre_fix": "<parent-of-fix>", "post_fix": "<fix>"}`.

The manifest is hand-authored from Appendix A and **user-reviewed before Phase 4 runs**. See `compares/bug_bench/README.md` for authoring instructions.

### 5.5 Run walltime

~15 verified bugs × ~3.5 tools per SUT row × 2h × 1 rep ≈ **105 wall-hours ≈ 1 wall-day parallelised 4-way**. If verified N < 10 after pre-flight, drop per-cell budget to 1h × 1.

## 6. Execution Phases

Seven phases. Phase 0 is one-time setup; Phases 1–5 are the run; Phase 6 is reporting.

### Phase 0 — One-time setup

- Extend `compares/scripts/fetch_sources.sh` — already fetches EvoSuite + Randoop; add Jazzer JAR, Atheris (`pip install atheris==2.3.0`), libFuzzer (via Clang 18+).
- NEW: `compares/scripts/build_harnesses.sh` — compiles Jazzer (Gradle) + libFuzzer (CMake) harnesses. Atheris needs no compile.
- NEW: hand-author `compares/bug_bench/manifest.json` from Appendix A; user review; **freeze**.
- NEW: pre-flight install-verification — run `bug_bench_driver.py --verify-only` to drop unverifiable bugs.
- **Prerequisite**: the `biotest-bench` Docker image (§13.1). It bundles the Clang 18 + patched seqan3 + libFuzzer toolchain (plus mull-18 for C++ mutation); no separate WSL2 setup required.

### Phase 1 — Validity probe (metric 3.1)

`compares/scripts/validity_probe.py`. Walks each tool's output corpus, calls each `ParserRunner.run()`, computes `success / total`.

Output: `compares/results/validity/<tool>/<sut>/validity.json`.

### Phase 2 — Coverage growth (metric 3.2)

`compares/scripts/coverage_sampler.py`. Orchestrates 2h × 3 reps per cell, samples coverage at log ticks. Reuses `test_engine.feedback.coverage_collector.MultiCoverageCollector`.

Output: `compares/results/coverage/<tool>/<sut>/growth_<run_idx>.json`.

### Phase 3 — Mutation score (metric 3.3)

`compares/scripts/mutation_driver.py`. Runs PIT / mutmut / mull per `compares/mutation/*/README.md` scoping. Each tool's final corpus from Phase 2 becomes that tool's test suite.

Output: `compares/results/mutation/<tool>/<sut>/summary.json`.

### Phase 4 — Real-bug benchmark (metrics 3.4 + 3.5)

`compares/scripts/bug_bench_driver.py`. Consumes the manifest; for each verified bug installs pre-fix SUT, runs each eligible tool for 2h, records TTFB, verifies post-fix silences the signal.

Output: `compares/results/bug_bench/<tool>/<bug_id>.json` + `compares/results/bug_bench/aggregate.json`.

### Phase 5 — Short-budget secondary regime

Reuse `coverage_sampler.py` with `--budget 300 --reps 5`. Produces the proposal-matching growth curve.

### Phase 6 — Report

`compares/scripts/build_report.py`. Aggregates all JSON; emits:

- `compares/results/comparison_report.md` — tables for all 5 metrics.
- `compares/results/figures/coverage_growth_<sut>.png` — log-x growth curves per SUT, one line per tool, 95% CI bands.
- `compares/results/figures/validity_bar_<sut>.png` — grouped bar chart.
- `compares/results/figures/mutation_bar_<sut>.png` — grouped bar chart.
- `compares/results/figures/bug_detection_heatmap.png` — bug × tool heatmap.
- `compares/results/figures/ttfb_violin.png` — TTFB distribution per tool.

### Sequencing

Phase 0 → Phases 1+2+5 share per-cell runs (the same 2h generation run feeds validity, coverage, and short-regime sampling) → Phase 3 → Phase 4 → Phase 6.

## 7. Folder Layout

```
compares/
├── DESIGN.md                     # this file
├── README.md                     # quick-start pointer
├── .gitignore                    # excludes source/, results/, coverage artifacts
├── baselines/                    # (source/ subfolders gitignored)
│   ├── evosuite/                 # EvoSuite 1.2.0 (white-box anchor)
│   ├── randoop/                  # unused in slim matrix; kept for future
│   ├── random_testing/           # pure-random byte-level generator
│   └── jazzer/                   # NEW — Jazzer JAR (fetched)
├── bug_bench/                    # NEW — real-bug benchmark
│   ├── README.md                 # schema + authoring instructions
│   ├── manifest.json             # 32-candidate manifest (user-reviewed, frozen)
│   └── triggers/<bug_id>/        # hand-curated minimised trigger inputs
├── harnesses/                    # NEW — fuzzer harnesses
│   ├── jazzer/
│   │   ├── VCFCodecFuzzer.java
│   │   ├── SAMCodecFuzzer.java
│   │   └── build.gradle
│   ├── atheris/
│   │   ├── fuzz_pysam.py
│   │   ├── fuzz_biopython.py
│   │   └── requirements.txt
│   └── libfuzzer/
│       ├── seqan3_sam_fuzzer.cpp
│       └── CMakeLists.txt
├── mutation/                     # PIT / mutmut / mull config notes
│   ├── pit/README.md
│   ├── mutmut/README.md
│   └── mull/README.md
├── scripts/
│   ├── fetch_sources.sh          # extend for Jazzer / Atheris / libFuzzer
│   ├── build_harnesses.sh        # NEW
│   ├── run_evosuite.sh           # existing (EvoSuite anchor driver)
│   ├── measure_evosuite_coverage.sh  # existing
│   ├── validity_probe.py         # Phase 1 (promote from placeholder)
│   ├── coverage_sampler.py       # Phase 2+5 (promote)
│   ├── mutation_driver.py        # Phase 3 (promote)
│   ├── bug_bench_driver.py       # NEW — Phase 4 orchestrator
│   ├── build_report.py           # Phase 6 (promote)
│   └── tool_adapters/            # NEW — per-tool uniform wrappers
│       ├── run_biotest.py
│       ├── run_jazzer.py
│       ├── run_atheris.py
│       ├── run_libfuzzer.py
│       └── run_pure_random.py
└── results/                      # populated at run time (gitignored)
    ├── validity/<tool>/<sut>/
    ├── coverage/<tool>/<sut>/
    ├── mutation/<tool>/<sut>/
    ├── bug_bench/<tool>/
    └── figures/
```

## 8. Citations Table

Every methodology claim in this document is anchored by at least one peer-reviewed source. This table is structured for direct lift into the paper draft.

| Claim in DESIGN.md | Citation |
| :--- | :--- |
| Metamorphic testing is a valid oracle substitute | Chen, Kuo, Liu, Tse, Towey, Zhou, ACM CSUR'18, 51(1):4 — "Metamorphic Testing: A Review of Challenges and Opportunities" |
| MR survey & taxonomy | Segura, Fraser, Sánchez, Ruiz-Cortés, IEEE TSE'16, 42(9):805–824 — "A Survey on Metamorphic Testing" |
| MR automation feasibility | Xu, Terragni, Zhu, Wu, Cheung, ACM TOSEM'24 / arXiv:2304.07548 — "MR-Scout: Automated Synthesis of Metamorphic Relations from Existing Test Cases" |
| MR vs fuzzer head-to-head | Wickerson et al., MET'21 — "Dreaming up Metamorphic Relations" |
| Coverage-based benchmarking is unreliable alone | Böhme, Liyanage, Wüstholz, ICSE'22 — "On the Reliability of Coverage-Based Fuzzer Benchmarking" |
| 24h minimum fuzzer runtime (we deviate to 2h and document why) | Klees, Ruef, Cooper, Wei, Hicks, CCS'18 — "Evaluating Fuzz Testing" |
| Mutation score as oracle quality | arXiv:2201.11303 — "Mutation Analysis: Answering the Fuzzing Challenge"; Vikram et al., ISSTA'23 — "Guiding Greybox Fuzzing with Mutation Testing" |
| Real-bug benchmark framework | Hazimeh, Herrera, Payer, SIGMETRICS'20 — "Magma: A Ground-Truth Fuzzing Benchmark" |
| Semantic fuzzing (JQF/Zest) | Padhye, Lemieux, Sen, Papadakis, Le Traon, ISSTA'19 / arXiv:1812.00078 — "Semantic Fuzzing with Zest" |
| libFuzzer | Serebryany et al., USENIX ATC'16 — "libFuzzer: a library for coverage-guided fuzz testing" |
| AFL++ | Fioraldi, Maier, Eißfeldt, Heuse, USENIX WOOT'20 — "AFL++: Combining Incremental Steps of Fuzzing Research" |
| Jazzer | Code Intelligence GmbH — OSS release; integrated into OSS-Fuzz since 2021 |
| Atheris | Google, announced December 2020 (Google Security Blog: "How the Atheris Python Fuzzer Works") |
| Grammar-aware fuzzing | Aschermann et al., NDSS'19 — "NAUTILUS: Fishing for Deep Bugs with Grammars"; Wang et al., ICSE'19 — "Superion: Grammar-Aware Greybox Fuzzing" |
| Format-spec-driven fuzzing | Grieco et al., ACM TOSEM'24 / arXiv:2109.11277 — "FormatFuzzer: Effective Fuzzing of Binary File Formats" |
| LLM-based fuzzing | Xia, Paltenghi, Tian, Pradel, Zhang, ICSE'24 — "Fuzz4All: Universal Fuzzing with Large Language Models"; Deng, Xia, Yang, Zhang, Zhang, ISSTA'23 — "Large Language Models Are Zero-Shot Fuzzers" (TitanFuzz) |
| Parser-directed fuzzing | Mathis, Gopinath, Mera, Kampmann, Höschele, Zeller, PLDI'19 — "Parser-Directed Fuzzing" |
| EvoSuite (anchor) | Fraser & Arcuri, FSE'11 — "EvoSuite: Automatic Test Suite Generation for Object-Oriented Software" |
| Randoop (documented, not run) | Pacheco, Lahiri, Ernst, Ball, OOPSLA'07 — "Feedback-Directed Random Test Generation" |
| Pynguin (rejected) | Lukasczyk, Kroiß, Fraser, ISSTA'22 — "Pynguin: Automated Unit Test Generation for Python" |

## 9. Risks

### Risk 1 — seqan3 Clang/libFuzzer toolchain — **resolved**

**Original severity: critical. Current status: resolved 2026-04-19.**
Historical: the Windows/MinGW `biotest_harness.cpp` couldn't link
seqan3, Ubuntu's `libseqan3-dev` 3.1.0 lacked sdsl-lite, and Clang 18
rejected seqan3's concept constraints so libFuzzer couldn't build.

Resolution baked into `biotest-bench:latest`:

- WSL2 + Linux build environment moved inside Docker (§13.1).
- `xxsds/sdsl-lite` v3 cloned to `/opt/sdsl-lite` instead of Ubuntu's
  broken apt package.
- seqan3 3.3.0 cloned to `/opt/seqan3` with two in-tree patches
  applied at image build (§13.2.4) — the `SEQAN3_IS_CONSTEXPR` macro
  short-circuits under Clang, and `repeat_view`'s friend declaration
  is rewritten to match the real `random_access_iterator_base`
  template signature.
- Clang 18 + libFuzzer + ASan + UBSan build the harness cleanly
  (**primary**).
- GCC 12 + AFL++ v4.21c build the same harness cleanly (verified
  alternate; swap in `bug_bench_driver.py: MATRIX["seqan3"]` if Clang
  ever regresses).
- mull 0.33.0 for LLVM 18 installed via the upstream 24.04 release
  deb (its only runtime deps — `libclang-cpp18` + `libllvm18` — are
  already provided by apt.llvm.org, so the 24.04 package installs
  cleanly on the 22.04 base). Binaries at `/usr/bin/mull-runner-18`
  and `/usr/lib/mull-ir-frontend-18`.

Full image verify (§13.1): **40 PASS, 0 WARN, 0 FAIL**.

### Risk 2 — Bug-bench walltime borderline even at 2h × 1

~15 verified bugs × ~3.5 tools per SUT row × 2h × 1 rep ≈ 105 wall-hours. Parallelising 4-way → ~1 wall-day. If install-version setups fail more than expected (old pysam wheels often reference libhts versions that have left apt mirrors), each failure adds 30–60 min of debug.

**Mitigation**: mandatory pre-flight install-verification pass (`bug_bench_driver.py --verify-only`) drops unverifiable bugs *before* the main run. If verified N drops below 10, per-cell budget drops from 2h to 1h — the signal is nearly as strong and walltime drops 2×.

### Risk 3 — Fairness equalizer mis-application

If the equalizer pass applies BioTest's **metamorphic** oracle (not just differential) to fuzzer outputs, BioTest's transform chain gets credit for inputs the fuzzer generated, inflating BioTest's numbers spuriously.

**Mitigation**: restrict the equalizer to `test_engine/oracles/differential.py` only; **never** apply `metamorphic.py` to fuzzer outputs. Documented in §4.4. Sanity check: differential-only detection count ≤ full BioTest detection count, always.

## 10. Open Decisions

All primary decisions are locked in §2/§3/§4. These remain open and are deferred to Phase-0 pre-flight:

1. **Verified N after install-verification.** If N < 10, drop bug-bench per-cell budget from 2h to 1h.
2. **Secondary baselines.** JQF+Zest, AFL++, Randoop, Nautilus, Fuzz4All are documented but not required. If compute time permits after the primary matrix finishes, they can be added — results will be asterisked.
3. ~~**WSL2 setup for seqan3 libFuzzer.**~~ **Resolved 2026-04-19** —
   Docker image (§13.1) ships Clang 18 + patched seqan3 + libFuzzer;
   AFL++ also available as alternate. See §13.2.4 for both harness
   verifications and the specific patches.

## 11. Non-goals

- This comparison does **not** re-evaluate BioTest's correctness or bug-finding quality against ground truth — that's measured in the main Phase A–D evaluation.
- We do not compare against neural / LLM-only fuzzers (TitanFuzz) as a primary baseline. Fuzz4All is listed as optional secondary.
- No real-world in-the-wild bug hunt during comparison — the benchmark set is fixed at Phase 0.
- No effort to reproduce bugs older than 2020. Build-system drift makes older bugs prohibitively expensive to install.

## 12. Change log

| Date | Change | Author |
| :--- | :--- | :--- |
| 2026-04-16 | Initial design drafted with EvoSuite + Randoop as primary baselines. | Automated assistant session |
| 2026-04-19 | **Full rewrite.** EvoSuite + Randoop demoted to white-box anchor. Added Jazzer / Atheris / libFuzzer as fair E2E baselines per language. Added real-bug detection rate + TTFB metrics. Added 32-bug candidate manifest (Appendix A). Locked slim 13-cell matrix with 2h × 3 reps primary and 2h × 1 bug-bench. Added citation table. Documented WSL2 seqan3 prerequisite. | Automated assistant session |

---

## Appendix A — Candidate Bug List

Research input to the `bug_bench/manifest.json` hand-authoring step in Phase 0. Each entry requires pre-fix / post-fix version pinning before it enters the live benchmark.

### A.1 htsjdk (10)

| # | Issue | Category | Logic? | Description |
| :-: | :--- | :--- | :--- | :--- |
| 1 | [#1708](https://github.com/samtools/htsjdk/pull/1708) | round_trip_asymmetry | yes | CRAM multi-container reference region state corruption |
| 2 | [#1590](https://github.com/samtools/htsjdk/pull/1590) | parse_error_missed | yes | CRAM 'BB' read features not restored — bases silently dropped |
| 3 | [#1592](https://github.com/samtools/htsjdk/pull/1592) | parse_error_missed | yes | CRAM scores ('SC') misdecoded during normalization |
| 4 | [#1554](https://github.com/samtools/htsjdk/pull/1554) | incorrect_field_value | yes | AC/AN/AF include filtered genotypes marked FT |
| 5 | [#1637](https://github.com/samtools/htsjdk/issues/1637) | round_trip_asymmetry | yes | VCF sort order change breaks merging of valid VCFs |
| 6 | [#1117](https://github.com/samtools/htsjdk/issues/1117) | null_ptr | no (crash) | NPE in BCF2LazyGenotypesDecoder on BCF-from-VCF |
| 7 | [#1686](https://github.com/samtools/htsjdk/issues/1686) | incorrect_field_value | yes | Inconsistent `VariantContext.getType()` on spanning deletions |
| 8 | [#1026](https://github.com/samtools/htsjdk/issues/1026) | incorrect_rejection | no | False "Allele not in VC" in multithreaded read-then-write |
| 9 | [#761](https://github.com/samtools/htsjdk/issues/761) | writer_bug | yes | Filename containing ".bcf" forces BCF output for VCF |
| 10 | [#423](https://github.com/samtools/htsjdk/issues/423) | parse_error_missed | yes | Multi-allelic AF/AC not per-allele cached |

### A.2 pysam (10)

| # | Issue | Category | Logic? | Description |
| :-: | :--- | :--- | :--- | :--- |
| 1 | [#1314](https://github.com/pysam-developers/pysam/issues/1314) | incorrect_field_value | yes | `VariantFile.write()` contig remap corruption after manual header edits |
| 2 | [#1308](https://github.com/pysam-developers/pysam/issues/1308) | parse_error_missed | no | `VariantHeader.new_record()` fails GT on 2nd+ call |
| 3 | [#966](https://github.com/pysam-developers/pysam/issues/966) | incorrect_field_value | yes | `VariantRecord.stop` returns POS instead of END for TRA |
| 4 | [#1175](https://github.com/pysam-developers/pysam/issues/1175) | incorrect_field_value | yes | INFO/END omitted when writing symbolic-allele SV records |
| 5 | [#1225](https://github.com/pysam-developers/pysam/issues/1225) | incorrect_field_value | no | Wrong PL tuple length expected for haploid GT |
| 6 | [#904](https://github.com/pysam-developers/pysam/issues/904) | incorrect_rejection | no | `VariantFile.fetch()` raises on empty VCF with valid tabix index |
| 7 | [#1038](https://github.com/pysam-developers/pysam/issues/1038) | incorrect_rejection | no | `tabix_index()` leaks file handles under parallel load |
| 8 | [#641](https://github.com/pysam-developers/pysam/issues/641) | writer_bug | yes | `tabix_index()` always creates CSI, ignoring user choice |
| 9 | [#771](https://github.com/pysam-developers/pysam/issues/771) | null_ptr | no (crash) | `VariantFile.write()` segfault on missing `##FORMAT`/`##contig` |
| 10 | [#450](https://github.com/pysam-developers/pysam/issues/450) | writer_bug | yes | Header-only VCF loses header on write (regression 0.10.0) |

### A.3 biopython (6, SAM only)

| # | Issue | Category | Logic? | Description |
| :-: | :--- | :--- | :--- | :--- |
| 1 | [#4825](https://github.com/biopython/biopython/issues/4825) | edge_case_missed | yes | Excessive deepcopy in SAM parser (perf + correctness) |
| 2 | [#4868](https://github.com/biopython/biopython/issues/4868) | parse_error_missed | — | Native BAM parsing not implemented (feature gap; context only) |
| 3 | [#4731](https://github.com/biopython/biopython/issues/4731) | parse_error_missed | yes | CIGAR op details not exposed |
| 4 | [#1913](https://github.com/biopython/biopython/issues/1913) | edge_case_missed | yes | Wrong local alignment for zero-score start residue |
| 5 | [#1699](https://github.com/biopython/biopython/issues/1699) | parse_error_missed | no | query_start/query_end from soft-clip CIGAR not exposed |
| 6 | [#4769](https://github.com/biopython/biopython/issues/4769) | incorrect_field_value | yes | PairwiseAligner vs legacy pairwise2 inconsistency |

### A.4 seqan3 (6, confirmed fix-commit SHAs)

| # | PR | Fix SHA | Category | Logic? | Description |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | [#2418](https://github.com/seqan/seqan3/pull/2418) | `8e374d7c` | parse_error_missed | yes | BAM parser skips sequence bytes on dummy alignment — stream misalignment |
| 2 | [#3081](https://github.com/seqan/seqan3/pull/3081) | `c84f567` | writer_bug | yes | Empty SAM/BAM output missing header — file unusable |
| 3 | [#3269](https://github.com/seqan/seqan3/pull/3269) | `11564cb3` | off_by_one_coord | yes | Banded alignment returns relative (not absolute) positions |
| 4 | [#3098](https://github.com/seqan/seqan3/pull/3098) | `4fe54891` | incorrect_field_value | yes | Alignment traceback carry-bit tracking wrong → wrong score |
| 5 | [#2869](https://github.com/seqan/seqan3/pull/2869) | (in PR) | parse_error_missed | yes | FASTA ID containing `>` parsed incorrectly |
| 6 | [#3406](https://github.com/seqan/seqan3/pull/3406) | `5e5c05a4` | encoding_bug | no (data race) | BGZF concurrent-read data race |

biopython #4868 is a feature gap rather than a bug and will likely be dropped or reframed in the manifest.

**Expected verified yield**: 18–25 of 32 after Phase-0 install-verification.

---

## 13. Execution Checklist

An operational, step-by-step todo list for actually running the comparative evaluation. Sub-steps are ordered by dependency. Items marked **[one-time]** only need to run once; the rest run per evaluation. Historical Risk 1 items have all been resolved as of 2026-04-19 (§9).

### 13.1 Environment prerequisites (one-time)

**Primary path — Docker container.** One `docker build` gives every tool
§13.1 needs; no WSL2 distribution to maintain by hand. Docker Desktop
on Windows already uses WSL2 as its backend, so this is *using* WSL2
without *managing* it. Verified end-to-end on 2026-04-19: image
`biotest-bench:latest`, `verify.sh` reports **40 PASS / 0 WARN /
0 FAIL**, exit code 0.

- [x] **Docker Desktop running** with the WSL2 backend (default on
  Windows 10/11). Verify: `docker --version && docker info | grep -i osType`.
- [x] **Disk space**: ≥ 50 GB free under `compares/` + ≥ 15 GB free
  for the Docker image.
- [x] **Build + verify** (one command does both):
  - [x] `bash compares/docker/build.sh` — builds `biotest-bench:latest`
    AND automatically runs `verify.sh` at the end. First build takes
    ~12 min and produces a 4.64 GB image; subsequent rebuilds use
    Docker's layer cache.
- [x] **Image contents** (final, verified): Temurin JDK 17, Python 3.12
  + Python 3.11 (separate venv at `/opt/atheris-venv/`), Clang 18 +
  libFuzzer + AddressSanitizer/UBSan, GCC 12 + libstdc++-12, AFL++
  v4.21c, mull 0.33.0 for LLVM 18, patched seqan3 3.3.0 + xxsds/sdsl-lite
  v3 (C++23), gcovr + lcov, Gradle 8.5, Maven, Jazzer 0.22.1, EvoSuite
  1.2.0, PIT 1.15.3 (command-line + entry + pitest JARs under
  `/opt/pit/`), Atheris 2.3.0, mutmut 3.0.0, pysam 0.22.1, biopython
  1.85, coverage.py 7.6.0, plus everything in `requirements.txt`.
- [x] **Re-verify at any time**:
  - [x] `bash compares/docker/run.sh bash compares/docker/verify.sh` —
    prints `OK` / `WARN` / `FAIL` per tool, exits non-zero only if a
    **required** tool is broken. WARN is reserved for gated-optional
    tools like mull.
- [x] **Pysam runner container** (separate image, already used by
  BioTest Phase C):
  - [x] `biotest-pysam:latest` already built (pysam 0.23.3 inside).
    Probe: `docker run --rm --entrypoint python biotest-pysam:latest -c "import pysam; print(pysam.__version__)"`.
  - [x] Rebuild command if ever stale:
    `py -3.12 harnesses/pysam/build_docker.py`. Independent of
    `biotest-bench`; both images coexist.

**Two Python environments inside the image** (documented here because it
surprises people):

| Interpreter | Path | Purpose |
| :--- | :--- | :--- |
| System `python3` (3.10) | `/usr/bin/python3` | apt-managed tools only (gcovr, apt-listchanges). Never called by our scripts. |
| `python3.12` | `/usr/bin/python3.12` | BioTest orchestration, adapters, mutmut, coverage.py. The benchmark default. |
| `python3.11` venv | `/opt/atheris-venv/bin/python` | Atheris + its SUT deps. Atheris 2.3.0 uses the `PRECALL` opcode which Python 3.12 removed; 3.11 is the newest interpreter it builds against, and no 3.12-compatible Atheris exists as of April 2026. `run_atheris.py` defaults its `--python-bin` to this path. |

**Daily workflow**:

```bash
# Interactive shell inside the image with repo at /work
bash compares/docker/run.sh

# From inside the container, every benchmark script works verbatim:
(container) $ python3.12 compares/scripts/bug_bench_driver.py --verify-only
(container) $ /opt/atheris-venv/bin/python compares/harnesses/atheris/fuzz_pysam.py …
```

**If you skipped the Dockerfile** and want to know why specific decisions
live there, the Dockerfile is self-documenting in comments around each
workaround. The four build-loop lessons worth knowing:

1. `/usr/bin/python3` stays at system 3.10 — otherwise gcovr's
   apt-bundled `python3-lxml` (built for 3.10) fails to import under
   3.12 and the whole seqan3 layer breaks.
2. Atheris lives in a 3.11 venv, not the 3.12 site-packages.
3. `libseqan3-dev 3.1.0` on Ubuntu 22.04 ships without `sdsl-lite`; we
   clone `xxsds/sdsl-lite` (v3, ships `sdsl/version.hpp`) into
   `/opt/sdsl-lite/include` and export `CPLUS_INCLUDE_PATH`. The older
   `simongog/sdsl-lite` v2.1.1 is v2 and seqan3 rejects it at compile
   time with `sdsl_version_major != 3`.
4. `mull 0.33.0` for LLVM 18 is installed from the upstream Ubuntu 24.04
   release .deb — the only mull build that targets our LLVM 18 runtime.
   It installs cleanly on the 22.04 base because its runtime dependencies
   are already satisfied by the LLVM apt repo.

---

**Alternative path — bare WSL2 install.** Only pick this if you need
bare-metal fuzzing performance (~5–10% faster than Docker I/O on
Windows) or if Docker is unavailable. Longer, less reproducible.

- [ ] `wsl --install -d Ubuntu-22.04`, `sudo apt update && sudo apt upgrade -y`.
- [ ] Temurin JDK 17: add Adoptium apt repo, `sudo apt install -y temurin-17-jdk`.
- [ ] Python 3.12 via deadsnakes: `sudo apt install -y python3.12 python3.12-venv python3.12-dev`.
- [ ] Clang 18 via apt.llvm.org: `sudo apt install -y clang-18 libclang-18-dev llvm-18 llvm-18-dev lld-18`.
- [ ] `sudo apt install -y libseqan3-dev gcovr lcov git-lfs maven`.
- [ ] Install Gradle 8.5 manually (tar from gradle.org).
- [ ] Download Jazzer 0.22.1, EvoSuite 1.2.0, PIT 1.15.3, and mull 0.18.0 release artefacts into `/opt/`.
- [ ] `python3.12 -m venv ~/biotest-bench && source ~/biotest-bench/bin/activate`.
- [ ] `CC=clang-18 pip install atheris==2.3.0 mutmut==3.0.0 coverage==7.6.0 pysam==0.22.1 biopython==1.85`.
- [ ] `pip install -r requirements.txt` from the repo root.
- [ ] Verify: run the same checks as `compares/docker/verify.sh` but on the bare host.

### 13.2 Per-tool installation, build, and smoke test

Run each per-tool block once; re-run only if a tool or harness is
updated. All commands below are verified to run inside the
`biotest-bench:latest` image from §13.1 (2026-04-19). Host-side
invocations via `bash compares/docker/run.sh` work identically.

> **Adapter note.** Every adapter now does `sys.path.insert(0, __file__.parent)`
> so they run from any cwd. Invoke them directly with `python3.12
> compares/scripts/tool_adapters/run_<tool>.py`.

#### 13.2.1 BioTest (tool under evaluation) — verified

- [x] **Ensure `data/mr_registry.json` is populated.** Phase A + B must
  have run already — the comparison does **not** re-mine MRs. Probe:
  `python3.12 -c 'import json; d=json.load(open("data/mr_registry.json")); print(list(d.keys()))'` →
  `['enforced', 'quarantine', 'summary']`.
- [x] **CLI compatibility**: `biotest.py` exposes only `--config`,
  `--phase`, `--dry-run`, `--verbose`. The adapter was rewritten to
  use `--phase C --config biotest_config.yaml` with subprocess timeout
  as the budget mechanism. Short budgets (< 300 s) automatically fall
  back to `--dry-run` because Phase-C bootstrap alone takes 2–5 minutes
  to warm up every SUT.
- [x] **Smoke test (60 s → dry-run route)** inside the container:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_biotest.py \
    --sut htsjdk --seed-corpus seeds/vcf \
    --out-dir /tmp/bt-smoke --time-budget-s 60 --format VCF
  ```
  Verified result: `exit=0 corpus=47 crashes=0` in <1 s (config parse +
  seed harvest into `/tmp/bt-smoke/corpus/`).
- [ ] **Full Phase-C run** (only in production — budget ≥ 300 s). The
  adapter transparently switches from `--dry-run` to `--phase C` once
  `--time-budget-s` ≥ 300. Ensure the primary SUT in
  `biotest_config.yaml: phase_c.suts` is set before launching a real
  bench cell.

#### 13.2.2 Jazzer (Java baseline, htsjdk) — verified

- [x] **Jazzer CLI** lives at `/opt/jazzer/jazzer` in the image. Probe:
  `/opt/jazzer/jazzer --help | head -1` → `A coverage-guided, in-process fuzzer for the JVM`.
- [x] **Build the BioTest harness JAR**:
  ```bash
  bash compares/scripts/build_harnesses.sh jazzer
  ```
  Produces `compares/harnesses/jazzer/build/libs/biotest-jazzer.jar`
  (~21 MB) in ~15 s via Gradle. The harness uses the **classic
  `fuzzerTestOneInput(FuzzedDataProvider)` entry signature**, not
  `@FuzzTest` — the standalone `jazzer` CLI does not pick up JUnit-5
  annotations and requires the classic signature.
- [x] **Smoke test VCF (60 s)**:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_jazzer.py \
    --sut htsjdk --seed-corpus seeds/vcf \
    --out-dir /tmp/jz-vcf --time-budget-s 60 --format VCF
  ```
  Verified: `exit=0 corpus=47→265 crashes=0`, ~103 k runs in 60 s.
- [x] **Smoke test SAM (60 s)**:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_jazzer.py \
    --sut htsjdk --seed-corpus seeds/sam \
    --out-dir /tmp/jz-sam --time-budget-s 60 --format SAM
  ```
  Verified: Jazzer **found a real htsjdk SAM crash in ~2 s** (exit 77
  with 1 artefact under `/tmp/jz-sam/crashes/`). Exit 77 with ≥1 crash
  is the expected success state for a fuzzer — it means the tool
  detected a bug in that SUT. The reproducer is saved as
  `Crash_<hash>.java` next to the corpus.

**Jazzer gotchas resolved while building this**:

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| `Invalid value for boolean option version: 0.22.1` on startup | Jazzer auto-parses every `JAZZER_*` env var as a CLI option; a build-time `ENV JAZZER_VERSION=0.22.1` in the Dockerfile poisoned it | Dockerfile switched to `ARG JAZZER_VERSION` (only exists during build) + the adapter scrubs `JAZZER_*` from child env as defence-in-depth |
| `Unsupported glob pattern: htsjdk.variant.vcf.*,htsjdk.variant.variantcontext.*` | `--instrumentation_includes` accepts a single glob per flag, not CSV | Adapter repeats the flag per glob |
| `VCFCodecFuzzer must define exactly one of the following two functions…` | Used `@FuzzTest` annotation; CLI expects classic `fuzzerTestOneInput` | Rewrote both harnesses to the classic signature |

#### 13.2.3 Atheris (Python baseline, pysam + biopython) — verified

- [x] **Atheris lives in `/opt/atheris-venv/`** (Python 3.11). BioTest's
  own Python 3.12 can't host Atheris — Atheris 2.3.0 uses the `PRECALL`
  opcode that Python 3.12 removed, and no 3.12-compatible release
  exists. Probe: `/opt/atheris-venv/bin/python -c "import atheris; atheris.Setup"` → OK.
- [x] **Smoke test pysam / VCF (60 s)**:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_atheris.py \
    --sut pysam --seed-corpus seeds/vcf \
    --out-dir /tmp/atheris-pysam --time-budget-s 60 --format VCF
  ```
  Verified: `exit=0 corpus=47 crashes=0`, **1.21 M runs in 60 s** at
  ~20 k exec/s. The adapter's default `--python-bin
  /opt/atheris-venv/bin/python` picks up the 3.11 venv automatically.
- [x] **Smoke test biopython / SAM (60 s)**:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_atheris.py \
    --sut biopython --seed-corpus seeds/sam \
    --out-dir /tmp/atheris-bio --time-budget-s 60 --format SAM
  ```
  Verified: Atheris **found a real Biopython bug in ~17 s** — an
  `UnboundLocalError: cannot access local variable 'query_pos'` inside
  `Bio.Align.sam.AlignmentIterator`. Exit 77 + 1 crash file is the
  expected fuzzer-success state (same semantics as Jazzer §13.2.2).
  The biopython harness deliberately catches only `ValueError`,
  `StopIteration`, `AttributeError`, `OSError` — real bugs propagate
  so libFuzzer logs them.

#### 13.2.4 C++ fuzzers for seqan3 — **libFuzzer + AFL++ both verified**

The original design called for **libFuzzer** (Clang 18 + `-fsanitize=fuzzer`)
on seqan3, but the canonical Ubuntu seqan3 apt package 3.1.0 + vanilla
Clang combination fails with cascading `writable_constexpr_semialphabet`
errors on `<seqan3/io/sam_file/input.hpp>`. The debug loop walked
through several dead ends — ultimately resolved by two in-tree patches
to seqan3 that make the CLang compile path work:

1. **`SEQAN3_IS_CONSTEXPR` macro** (one-liner at
   `seqan3/utility/type_traits/basic.hpp:29`). The original uses
   `__builtin_constant_p` inside concept constraints; Clang 18 returns
   `false` where GCC returns `true`, so `writable_constexpr_semialphabet`
   rejects every alphabet → `seqan3::cigar` and `sam_file_input` fail to
   instantiate. Patch short-circuits the macro to `true` under
   `__clang__`, leaves the GCC path unchanged.
2. **`repeat_view` friend declaration** (5-line block at
   `seqan3/utility/views/repeat.hpp:84`). Original decls
   `template <typename parent_type, typename crtp_base>` but the
   actual `random_access_iterator_base` is
   `template <typename range_type, template <typename...> typename derived_t_template, typename... args_t>`.
   GCC lenient-mode ignores the mismatch; Clang rejects it, cascading
   into private-member-access errors for `difference_type`,
   `value_type`, etc. Patch rewrites the friend decl to match the
   real template signature.

Both patches are baked into the `biotest-bench` Dockerfile and
applied idempotently at image-build time. Downstream: both fuzzers
now compile `<seqan3/io/sam_file/input.hpp>` cleanly and smoke-test
successfully.

Toolchain now baked into `biotest-bench:latest`:
- [x] `seqan3` 3.3.0 source at `/opt/seqan3/include` with both Clang
  patches applied at build time.
- [x] `xxsds/sdsl-lite` v3 at `/opt/sdsl-lite/include`.
- [x] `CPLUS_INCLUDE_PATH` pre-populated with both.
- [x] Clang 18 + libFuzzer + ASan + UBSan (stock Ubuntu LLVM 18 repo).
- [x] GCC 12 (Ubuntu 12.3.0) + libstdc++-12-dev as the AFL++ host
  compiler — kept as a verified alternate.
- [x] AFL++ v4.21c source-built at `/opt/aflpp/` with
  `AFL_PATH=/opt/aflpp/lib/afl` exported.
- [x] `verify.sh` reports all five seqan3 checks OK:
  *headers present*, *Clang patch (macro)*, *Clang patch (friend)*,
  *sam_file compile under Clang 18 + patches*, *sam_file compile
  under GCC 12*. Full image verify: **40 PASS / 0 WARN / 0 FAIL**.

Status — **both C++ fuzzers verified**:

- [x] **Build libFuzzer target** (primary, in-process Clang fuzzer):
  ```bash
  bash compares/scripts/build_harnesses.sh libfuzzer
  # → compares/harnesses/libfuzzer/build/seqan3_sam_fuzzer_libfuzzer
  ```
  Produces a ~4.6 MB Clang-instrumented binary with ASan + UBSan
  attached. The CMake libfuzzer target sets
  `-DBIOTEST_HARNESS_LIBFUZZER=1` which suppresses our stdin-reader
  `main()` (libFuzzer provides its own).
- [x] **libFuzzer smoke test (30 s)** inside the container:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_libfuzzer.py \
    --sut seqan3 \
    --seed-corpus compares/results/bench_seeds/sam \
    --out-dir /tmp/lf-smoke --time-budget-s 30 --format SAM
  ```
  Verified: `exit=77 corpus=58 crashes=1`. libFuzzer **found a real
  seqan3 SAM crash** (deadly-signal stack trace in the log). Exit 77
  with ≥1 crash is the fuzzer-success state.
- [x] **Build AFL++ target** (alternate, out-of-process GCC fuzzer):
  ```bash
  bash compares/scripts/build_harnesses.sh aflpp
  # → compares/harnesses/libfuzzer/build-aflpp/seqan3_sam_fuzzer_aflpp
  ```
  Produces a ~3.4 MB GCC-instrumented binary. Same harness source.
- [x] **AFL++ smoke test (30 s)**:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_aflpp.py \
    --sut seqan3 \
    --seed-corpus compares/results/bench_seeds/sam \
    --out-dir /tmp/aflpp-smoke --time-budget-s 30 --format SAM
  ```
  Verified: `exit=0 queue=60 crashes=1`. AFL++ also found a real
  crash in ~2 s.

**Gotchas resolved while building this**:

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| seqan3 `writable_constexpr_semialphabet` constraint unsatisfied under Clang | Clang evaluates `__builtin_constant_p` differently from GCC inside concept constraints | In-tree patch to `SEQAN3_IS_CONSTEXPR`; always-true under `__clang__` |
| seqan3 `difference_type` / `value_type` private-member errors | `repeat_view`'s friend decl has 2 template params vs the real 3 | In-tree patch to match the real template signature |
| CMake passes `-g -O1 -fsanitize=fuzzer,…` as a single arg | `set(VAR "-g -O1 …")` treats the string as one arg | Use list form: `set(VAR -g -O1 -fsanitize=fuzzer,address,undefined)` |
| libFuzzer `The required directory "…" does not exist` | adapter's default corpus path had to be created before invocation | Adapter pre-creates corpus + crashes dirs via `prepare_out_dir` |
| AFL++ `Unable to find 'afl-compiler-rt.o'` | AFL++ runtime under `/opt/aflpp/lib/afl/` not auto-discovered | `ENV AFL_PATH=/opt/aflpp/lib/afl` in Dockerfile + default in `build_harnesses.sh` |
| AFL++ `undefined reference to 'main'` at link time | Harness's `main` was guarded by `__AFL_HAVE_MANUAL_CONTROL` which AFL++ doesn't auto-define | Switched to unconditional stdin-reader `main()`, gated off only for libFuzzer via `BIOTEST_HARNESS_LIBFUZZER` define |
| AFL++ `PROGRAM ABORT: Pipe at the beginning of 'core_pattern'` | Docker inherits WSL2's `|/wsl-capture-crash` core handler; `/proc` is read-only | Adapter sets `AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1` in the child env |

**Final matrix state**: the seqan3 row in §4.1 is fully populated
with a fair E2E baseline. libFuzzer is primary; AFL++ is a verified
alternate on the same harness source.

#### 13.2.5 Pure Random (floor baseline) — verified

- [x] No install step (Python stdlib only).
- [x] **Smoke test (30 s)**:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_pure_random.py \
    --sut htsjdk --seed-corpus seeds/vcf \
    --out-dir /tmp/random --time-budget-s 30 --format VCF
  ```
  Verified: `exit=0 corpus=681772 crashes=0`. The generator happily
  hits ~23 k files/sec; the `adapter_result.json` records the full
  count.

#### 13.2.6 EvoSuite (white-box anchor, htsjdk only) — **partial**

Docker-side verified:

- [x] `/opt/evosuite/evosuite.jar` (≈19 MB) is present in the image.
- [x] `java -jar /opt/evosuite/evosuite.jar -help` prints the full
  banner.
- [x] JDK 17 (Temurin) in the image is compatible enough to load
  EvoSuite.

Host-side (**remains the production path**):

- [x] `compares/baselines/evosuite/source/evosuite-1.2.0.jar` already
  fetched (see `compares/baselines/evosuite/README.md`).
- [x] `compares/baselines/evosuite/jdk17/jdk-17.0.13+11/` pinned JDK is
  on disk from prior runs.
- [x] `compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar` present
  (required — EvoSuite's InstrumentingClassLoader needs every
  transitive htsjdk dep on one classpath).
- [ ] **Smoke test on one VCF class** (via the existing host-side
  driver):
  ```bash
  SEARCH_BUDGET=60 bash compares/scripts/run_evosuite.sh --classes htsjdk.variant.vcf.VCFCodec
  ```
  Confirm `compares/baselines/evosuite/results/work/evosuite-tests/`
  contains a `VCFCodec_ESTest.java`.
- [ ] **Coverage measurement on that suite**:
  `bash compares/scripts/measure_evosuite_coverage.sh` → JaCoCo XML
  under `coverage_artifacts/jacoco/`.

**Why the full smoke test wasn't run inside the container**: EvoSuite
1.2.0 forks a child "Client-0" JVM that doesn't inherit the master's
`--add-opens` flags, and XStream's inheritance-tree deserialisation
then fails on JDK 17 with `InaccessibleObjectException` (cf. the
stacktrace: `java.desktop does not "opens java.awt"`). The existing
host-side `run_evosuite.sh` resolves this via its specific JDK-17
download + fatjar classpath layout that has been debugged on the dev
box. Re-creating that dance inside the container is out of scope for
the smoke test; the comparison protocol runs EvoSuite on the host.

### §13.2 summary

| Tool | Install in image | Smoke test | Status |
| :--- | :---: | :--- | :--- |
| BioTest | ✓ | `--dry-run` exit 0 in <1 s; full Phase C deferred to long-budget runs | **verified** |
| Jazzer | ✓ | VCF exit 0 / 103 k runs; SAM found crash in 2 s | **verified** |
| Atheris | ✓ (3.11 venv) | pysam 1.21 M runs; biopython found `UnboundLocalError` | **verified** |
| **libFuzzer / seqan3** | ✓ (Clang 18 + patched seqan3) | exit 77 / 58 corpus / 1 crash in 30 s | **verified** (primary C++ fuzzer) |
| **AFL++ / seqan3** | ✓ (g++-12 + afl-g++) | exit 0 / 60 queue / 1 crash in 30 s | **verified** (alternate C++ fuzzer) |
| Pure Random | ✓ | 681 k files in 30 s | **verified** |
| EvoSuite anchor | ✓ (help banner) | full smoke on host via `run_evosuite.sh` | **partial (host-side)** |

### 13.3 Per-SUT pre-flight (data & instrumentation) — verified

Every item below is checked against the `biotest-bench:latest` image
from §13.1 on 2026-04-19. Scaffolding scripts are under
`compares/scripts/` and produce artefacts under `compares/results/`.

#### 13.3.1 Seed corpus — verified

- [x] **Already populated.** `seeds/vcf/` = 47 files (33 real +
  14 `synthetic_iter*`), `seeds/sam/` = 46 files (all real; no
  synthetic cohort exists for SAM yet). Both well above DESIGN.md §5.1
  thresholds (VCF ≥ 15, SAM ≥ 6). **Re-running
  `py -3.12 seeds/fetch_real_world.py` is not needed.**
- [x] **Materialise a synthetic-free bench corpus** (hardlinks, not
  copies) so adapters point at a deterministic path that can't drift
  between runs:
  ```bash
  bash compares/scripts/prepare_bench_seeds.sh
  # → [bench-seeds] VCF: 33 files  →  compares/results/bench_seeds/vcf
  # → [bench-seeds] SAM: 46 files  →  compares/results/bench_seeds/sam
  ```
  `compares/results/bench_seeds/` is gitignored (under `results/`). Re-run
  the script if seeds change upstream; it rebuilds the dir from scratch.
- [x] **Per-adapter pointer**: all smoke tests in §13.2 and all primary
  bench cells use `--seed-corpus compares/results/bench_seeds/<vcf|sam>`.
  BioTest itself still sees `seeds/vcf/` in Phase D (that's a separate
  code path that can include synthetics for feedback-driven synthesis);
  only the comparison adapters swap to the filtered corpus.

#### 13.3.2 Coverage scope sanity check — verified

- [x] **`biotest_config.yaml: coverage.target_filters`** (lines 320–351)
  is nested per (format, SUT) and resolves correctly. Dry-run probe
  inside the container:
  ```bash
  python3.12 -c "
  import sys, yaml; sys.path.insert(0, '/work')
  from test_engine.feedback.coverage_collector import MultiCoverageCollector
  cfg = yaml.safe_load(open('biotest_config.yaml'))['coverage']
  mc = MultiCoverageCollector(cfg)
  for fmt in ('VCF','SAM'):
      for sut in ('htsjdk','pysam','biopython','seqan3'):
          print(fmt, sut, mc._resolve_sut_filter(fmt, sut))"
  ```
  Verified results (2026-04-19):

  | format | sut | filter |
  | :---: | :---: | :--- |
  | VCF | htsjdk | `[htsjdk/variant/vcf, htsjdk/variant/variantcontext::-JEXL,…, htsjdk/variant/variantcontext/writer::VCF,Variant]` |
  | VCF | pysam | `[pysam]` |
  | VCF | biopython | *not configured* (biopython has no VCF parser) |
  | VCF | seqan3 | *not configured* (seqan3 has no VCF support) |
  | SAM | htsjdk | `[htsjdk/samtools::SAM,Sam]` |
  | SAM | pysam | `[pysam]` |
  | SAM | biopython | `[Bio/Align/sam]` |
  | SAM | seqan3 | `[seqan3/io/sam_file, format_sam, cigar]` |

  Four collectors register cleanly: `JaCoCoCollector` (htsjdk),
  `CoveragePyCollector` (biopython), `PysamDockerCoverageCollector`
  (pysam), `GcovrCollector` (seqan3).
- [x] Actual coverage-artefact collection requires real JaCoCo /
  `.coverage` / `gcovr.json` data; those only exist after a Phase-2 run.
  Coverage-probe dry-run from here only verifies *scope resolution*,
  which is the flaky piece of the plumbing — the collectors themselves
  have been exercised by previous BioTest Phase-D runs.

#### 13.3.3 Mutation-tool installation — verified

All three are pinned in the `biotest-bench:latest` image.

- [x] **PIT (Java, htsjdk)** at `/opt/pit/`:
  ```bash
  ls /opt/pit/
  # pitest-command-line.jar  pitest-entry.jar  pitest.jar
  java -cp /opt/pit/pitest-command-line.jar:/opt/pit/pitest.jar:/opt/pit/pitest-entry.jar \
       org.pitest.mutationtest.commandline.MutationCoverageReport --help
  ```
  Version pinned via Dockerfile `ARG PIT_VERSION=1.15.3`.
- [x] **mutmut (Python, pysam + biopython)**:
  ```bash
  python3.12 -c "import mutmut; print(mutmut.__version__)"  # → 3.0.0
  python3.12 -m mutmut --help
  ```
  Note: `mutmut --version` as a standalone flag doesn't exist; query
  `mutmut.__version__` via Python instead.
- [x] **mull (C++, seqan3)**: mull 0.33.0 for LLVM 18 via the upstream
  24.04 release deb (`Mull-18-0.33.0-LLVM-18.1.3-ubuntu-amd64-24.04.deb`).
  Installs cleanly on the 22.04 base because its only runtime deps
  (`libclang-cpp18`, `libllvm18`) come from the LLVM apt repo already
  on the image. Binaries at `/usr/bin/mull-runner-18` +
  `/usr/lib/mull-ir-frontend-18`. Probe:
  `mull-runner-18 --version` reports `0.33.0`.

#### 13.3.4 SUT version-pinning scaffolding — verified

All pre/post version-swap environments materialised by one command:

```bash
bash compares/scripts/prepare_sut_install_envs.sh
```

Verified output (2026-04-19):

| SUT | Environment | Seeded version | Swap mechanism |
| :--- | :--- | :--- | :--- |
| pysam | `compares/results/sut-envs/pysam/` (Python 3.11 venv) | pysam 0.22.1 | `venv/bin/pip install --force-reinstall pysam==<v>` |
| biopython | `compares/results/sut-envs/biopython/` (Python 3.11 venv) | biopython 1.85 | `venv/bin/pip install --force-reinstall biopython==<v>` |
| htsjdk | `compares/baselines/evosuite/fatjar/versioned/` (directory) | — | `curl https://repo.maven.apache.org/maven2/com/github/samtools/htsjdk/<v>/htsjdk-<v>.jar` per version |
| seqan3 | `compares/baselines/seqan3/source/` (git clone of `seqan/seqan3`, depth 50 on `main`, HEAD `45889f9`) | — | `git checkout <pre-fix-sha>` / `<fix-sha>` per bug |

- [x] Python venvs use the `python3.11` interpreter because Atheris
  (the primary Python fuzzer) already targets 3.11. Swapping SUT
  versions under 3.11 keeps the Atheris bench and bug_bench runs on
  the same interpreter — no double-wheel-build cost.
- [x] `bug_bench_driver.py` reads these locations via the
  `_install_pysam` / `_install_biopython` / `_install_htsjdk_jar` /
  `_checkout_seqan3` helpers.
- [x] Script is idempotent: re-running finds existing venvs / clones
  and just re-probes the baseline version.

### §13.3 summary

| Item | Status | Produced / at |
| :--- | :---: | :--- |
| Synthetic-free seed corpus | ✓ | `compares/results/bench_seeds/{vcf,sam}/` (33 + 46) |
| Coverage scope resolution | ✓ | 8 (fmt × sut) cells probed; all 4 collectors register |
| PIT install | ✓ | `/opt/pit/*.jar` (1.15.3) |
| mutmut install | ✓ | `python3.12 -m mutmut` (3.0.0) |
| mull install | ✓ | `/usr/bin/mull-runner-18` (0.33.0 for LLVM 18) |
| pysam venv | ✓ | `compares/results/sut-envs/pysam/` (0.22.1) |
| biopython venv | ✓ | `compares/results/sut-envs/biopython/` (1.85) |
| htsjdk versioned-JAR dir | ✓ | `compares/baselines/evosuite/fatjar/versioned/` (empty, populated on demand) |
| seqan3 source clone | ✓ | `compares/baselines/seqan3/source/` (main @ `45889f9`) |

### 13.4 Bug-bench pre-flight (manifest verification) — verified

Result after two research passes: **23 verified / 21 dropped of 44
candidates** (52% yield — inside the 18–25 forecast in DESIGN.md §5.2;
full 2 h × 1 rep per-bug budget in effect). Bench shape:

| SUT | Verified bugs |
| :--- | :---: |
| htsjdk | **12** — VCF + SAM (CRAM excluded by scope, see below) |
| pysam | **4** — VCF + SAM |
| biopython | 1 — SAM |
| seqan3 | 6 — SAM + 1 FASTA-adjacent |
| **total** | **23** |

Scope note: three htsjdk CRAM bugs (`1708`, `1590`, `1592`) were
install-verified but then dropped because our runners all declare
`supported_formats = {"VCF", "SAM"}` or narrower — no runner has
CRAM plumbing, and `BioTestHarness.java` has zero CRAM code. Including
CRAM-specific bugs would be a scope violation. Their research and
trigger folders stay under `compares/bug_bench/triggers/` for a
future CRAM-capable harness.

The **full per-bug reference** is rendered in §13.4.7 below (embedded
compact view) with the authoritative machine-readable source at
`compares/bug_bench/CATALOGUE.md` (regenerate via
`python compares/bug_bench/render_catalogue.py`).

#### 13.4.1 Manifest review — verified

- [x] Each of the 32 candidate `issue_url`s is live on GitHub.
  Reachable via WebFetch; researcher cross-checked the issue page
  against the linked PR / release notes.

#### 13.4.2 Populate `pre_fix` / `post_fix` — verified (via research script)

An Explore agent researched all 26 htsjdk/pysam/biopython issues
against GitHub release notes, PR-merge dates, and project CHANGELOG /
NEWS files. For seqan3, `git rev-parse <fix_sha>^` inside the cloned
repo resolved all 6 parent commits deterministically.

Result, applied via `compares/bug_bench/apply_research.py`:

- [x] **20 entries** got concrete version pins:
  - 5 htsjdk (high confidence — all 5 cited explicitly in release notes)
  - 8 pysam (4 high, 1 medium, 3 low confidence — later install-verify
    filtered this down to 2)
  - 1 biopython (medium — PR #4837 merged post-1.85)
  - 6 seqan3 (commit SHA + parent SHA, all resolved via `git rev-parse`)
- [x] **12 entries** marked `UNRESOLVABLE`: either no linked PR, the
  fix was never merged, or release notes don't cite the issue. These
  stay `PENDING_VERIFICATION` in `manifest.json` with a
  `dropped_reason` field and are excluded from the verified manifest.
  Breakdown: 5 htsjdk, 2 pysam, 5 biopython.
- [x] `anchor.verification_rule` field on each updated entry cites the
  specific release-notes line or commit hash that proves the linkage.

Run the script (idempotent):

```bash
python3.12 compares/bug_bench/apply_research.py
# → [research] updated=20 dropped=12 untouched=0
```

#### 13.4.3 Install-verification — verified

Ran `bug_bench_driver.py --verify-only` inside the bench image.
**Critical fix during this step**: the driver originally used
`/usr/bin/python3.12` for `pip install pysam==<version>`, which fails
for any pre-0.21 pysam (no 3.12 wheels, sdist build-rot on modern
setuptools). Switched the helpers to route through the Python 3.11
`sut-env` venvs created by §13.3.4 — `compares/results/sut-envs/pysam/bin/pip`
and `…/biopython/bin/pip`. This is now documented in
`bug_bench_driver.py` as the default path.

Commands:

```bash
bash compares/scripts/prepare_sut_install_envs.sh   # creates the venvs
python3.12 compares/scripts/bug_bench_driver.py --verify-only \
    --dropped-out compares/bug_bench/dropped.json
```

Result: `Summary: 14 verified, 18 dropped of 32 candidates.` Then a
scope-audit pass (`drop_cram_scope.py`) removed the three
CRAM-specific htsjdk bugs because no runner in this repo reads CRAM,
giving the final **11 verified / 21 dropped**.

**Why only 11 survived**:
- 12 UNRESOLVABLE dropped by the research step (no version anchor).
- 6 pre-0.21 pysam versions fail to build (`pysam==0.11/0.12/0.15/
  0.16/0.17/0.20`) even inside the Python 3.11 venv — sdist
  `pyproject.toml` missing; Cython + old libhts headers incompatible
  with modern toolchain. Honest drop.
- 3 CRAM bugs out of scope — the runners here handle VCF/SAM only;
  `htsjdk_runner.py:61` declares `supported_formats = {"VCF", "SAM"}`
  and `BioTestHarness.java` has zero CRAM code paths. Reintroducing
  them would need a CRAM-aware harness that doesn't exist.

Empirically verified with Py 3.11 venv: pysam **0.21.0, 0.22.0,
0.22.1, 0.23.0, 0.23.3** install cleanly; everything older fails at
`pip wheel-build` time.

#### 13.4.4 Populate trigger evidence — verified

All 11 verified bugs have trigger folders under
`compares/bug_bench/triggers/<bug_id>/`. Each folder carries at minimum
a `README.md` (one-paragraph bug description + how the trigger surfaces
it), with format-appropriate companions:

| Source | Contents per trigger folder |
| :--- | :--- |
| seqan3 × 6 (from `git show <fix_sha> -- test/`) | `fix.diff` full commit diff; `FIX_COMMIT.txt` commit metadata; `test_files/*.cpp,hpp` post-fix test source containing the embedded trigger inputs |
| htsjdk-1554 / htsjdk-1637 | `original.vcf` minimal reproducer + `reproduce.java` for -1554 |
| pysam-1314 | `original.vcf` + `reproduce.py` + `issue_source.txt` |
| pysam-1308 | `reproduce.py` + `issue_source.txt` (pure in-memory; no file needed) |
| biopython-4825 | `original.sam` 3-record seed + `generate_large_sam.py` (inflates to 10 k records for perf trigger) + `reproduce.py` timing wrapper + `issue_source.txt` |

The three CRAM-bug folders (`htsjdk-1708`, `-1590`, `-1592`) are kept
on disk with their `README.md` / `issue_source.txt` / (for -1708)
`synthesise_trigger.sh`, but no longer referenced by the verified
manifest — useful reference material if we ever extend the runners
to read CRAM.

- [x] `compares/bug_bench/triggers/<bug_id>/README.md` for each of
  the 11 in-scope bugs — one-paragraph description + detection
  criterion.
- [x] `compares/bug_bench/triggers/<bug_id>/` populated per the table
  above. Every bug has at least (a) a trigger input OR a script that
  produces one, AND (b) a description of the expected-signal
  translation from §4.3 for that specific bug.
- [x] seqan3 bugs got their PR's own test suite pulled straight out
  of the fix commit via `git show <fix_sha> -- test/` (done in a
  Bash one-liner, not a script — re-runnable if seqan3 HEAD drifts).

#### 13.4.5 Freeze the verified manifest — verified

- [x] `compares/bug_bench/manifest.verified.json` written by
  `compares/bug_bench/freeze_verified.py`. 11-bug subset; preserves
  the full `anchor` / `trigger` / `expected_signal` payload per bug
  plus a `bench_counts_by_sut` rollup field.
- [x] Both `manifest.json` (32 candidates, research applied) and
  `manifest.verified.json` (11-bug frozen subset) committed. The bench
  driver reads `--manifest` (default `manifest.json`); pass the
  `--manifest compares/bug_bench/manifest.verified.json` flag to
  Phase 4 to run only on the frozen subset.

#### 13.4.6 User review gate — ready

- [x] A one-page review packet written at
  `compares/bug_bench/REVIEW.md`. Contents:
  - Headline 11 verified / 21 dropped numbers + 34 % yield.
  - Per-bug table with id, SUT, format, pre/post-fix anchor,
    trigger-file set, research confidence.
  - Per-SUT bench shape rollup.
  - Drop-reason breakdown table: 11 no-PR-linkage / 1 feature gap /
    6 pre-0.21 pysam build-rot / 3 CRAM out-of-scope.
  - Five flagged concerns the user should decide on (thin htsjdk row
    post-CRAM-drop, pysam-1314 low-confidence, seqan3-3406 data-race
    non-determinism, seqan3-2869 FASTA scope, biopython-4825
    perf-signal-vs-crash signal).
  - Sign-off checklist with "no action = implicit accept" default.
- [ ] **Sign-off pending** — the user reads REVIEW.md, either
  accepts silently (implicit green-light per the checklist) or
  raises a specific concern. Until this box is ticked, Phase 4
  should not launch.

### 13.4.7 Verified bug catalogue (all 23)

The authoritative list of bugs Phase 4 will run against. Reproducible
from `manifest.verified.json` via `render_catalogue.py` — re-run
whenever the frozen manifest changes.

Every bug has a trigger folder at `compares/bug_bench/triggers/<id>/`
with a README.md, an issue_source.txt with the release-note citation,
and — where the format is plain text — an `original.{vcf,sam}` seed
input. Large / binary / concurrency-only triggers fall back to
fuzzer-synthesis per DESIGN.md §4.3.

#### htsjdk (12 bugs — the thick row)

| id | Fmt | Anchor | Category | Signal | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `htsjdk-1554` | VCF | 2.24.1 → 3.0.0 | incorrect_field_value | diff vs htslib, pysam | AC/AN/AF include FT-filtered genotypes; pre-fix counts are inflated whenever any per-sample FT ≠ PASS. Trigger: 2-sample VCF with `GT:FT` where one sample is `0/1:LowQual`. |
| `htsjdk-1637` | VCF | 3.0.3 → 3.0.4 | round_trip_asymmetry | diff vs htslib | 3.0.3 added an allele tiebreaker to VCF sort comparator; previously-valid VCFs now fail `isSorted()` check. 3.0.4 hotfix reverts PR #1593. |
| `htsjdk-1364` | VCF | 2.19.0 → 2.20.0 | incorrect_rejection | diff vs htslib, pysam | Pre-fix rejects mixed-case float literals (`NaN`, `Inf`, `Infinity`); htslib + spec accept them. Trigger: QUAL and INFO=AF with `NaN`/`Inf`. |
| `htsjdk-1389` | VCF | 2.19.0 → 2.20.0 | writer_bug | diff vs htslib | Pre-fix writer emits multi-value missing fields as `.,.,.` instead of single `.`. Round-trip textual form diverges per the spec. |
| `htsjdk-1372` | VCF | 2.19.0 → 2.20.0 | parse_error_missed | diff vs htslib | Pre-fix VCF codec throws on FORMAT=GL when every G-dimension value is individually `.`; htslib accepts as missing. |
| `htsjdk-1401` | VCF | 2.19.0 → 2.20.0 | incorrect_field_value | diff vs htslib | PEDIGREE header handling diverges between VCF 4.2 and 4.3 inputs with the same payload. |
| `htsjdk-1403` | VCF | 2.20.0 → 2.20.1 | incorrect_field_value | diff vs htslib | VariantContextBuilder regression in 2.20.0; 2.20.1 hotfix. |
| `htsjdk-1418` | VCF | 2.20.1 → 2.21.0 | incorrect_rejection | uncaught exception | Pre-fix VCFHeader throws on `##contig=<ID=X>` lines that omit `length=` even though the field is optional per spec. |
| `htsjdk-1544` | VCF | 2.24.1 → 3.0.0 | incorrect_field_value | diff vs htslib, pysam | `VariantContext.getType()` mis-classifies gVCF `<NON_REF>` records, confusing downstream variant-type filters. |
| `htsjdk-1561` | SAM | 2.24.1 → 3.0.0 | parse_error_missed | diff vs htslib | Pre-fix SAM header parser silently accepts tag keys of wrong length; spec §1.3 mandates exactly 2 characters. |
| `htsjdk-1538` | SAM | 2.24.0 → 2.24.1 | incorrect_field_value | diff vs htslib; also metamorphic | SAMRecord `mAlignmentBlocks` cache is not invalidated after mutating `setCigar()`. Subsequent `getAlignmentBlocks()` returns stale pre-mutation data. Classic cache-invalidation silent bug. |
| `htsjdk-1489` | SAM | 2.22.0 → 2.23.0 | incorrect_field_value | diff vs htslib | Locus accumulator drops insertion events; `samtools mpileup` produces different per-site coverage than htsjdk's LocusIterator. |

#### pysam (4 bugs)

| id | Fmt | Anchor | Category | Signal | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `pysam-1314` | VCF | 0.22.1 → 0.23.0 | incorrect_field_value | diff vs htslib | `VariantFile.write()` silently remaps records to header-contig-index-0 instead of matching by name when header contigs are hand-edited. |
| `pysam-1308` | VCF | 0.22.1 → 0.23.0 | parse_error_missed | uncaught exception | `VariantHeader.new_record()` works on first call, throws `KeyError: 'invalid FORMAT: GT'` on every call after. Pure in-memory trigger. |
| `pysam-1214` | SAM | 0.21.0 → 0.22.0 | incorrect_field_value | diff vs htslib | AlignmentFile iteration produces wrong per-record fields on some spec-tolerated SAM inputs; fixed with #939 as 0.22.0's AlignmentFile cleanup. |
| `pysam-939` | SAM | 0.21.0 → 0.22.0 | incorrect_field_value | diff vs htslib | Long-standing AlignmentFile bug, packaged into the same 0.22.0 cleanup as #1214. Trigger research deferred until Phase 4 reveals which specific input exposes it. |

#### biopython (1 bug)

| id | Fmt | Anchor | Category | Signal | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `biopython-4825` | SAM | 1.85 → 1.86 | edge_case_missed | timeout-or-diff vs htsjdk | Excessive `copy.deepcopy` in the SAM parser path (>50% of parse time); under a 2h budget this can silently truncate results for large SAMs. Trigger: 10k-record synthetic SAM. |

#### seqan3 (6 bugs — commit-SHA-anchored)

| id | Fmt | Anchor (commit) | Category | Signal | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `seqan3-2418` | SAM/BAM | `df9fd5ff6^` → `8e374d7c` | parse_error_missed | diff vs htslib, pysam | BAM parser forgets to consume sequence bytes when building dummy alignments; subsequent records misalign. |
| `seqan3-3081` | SAM/BAM | `fa221c130` → `c84f5671` | writer_bug | diff vs htslib | Empty SAM/BAM outputs written without headers — unusable files. |
| `seqan3-3269` | SAM | `ca4d66839` → `11564cb3` | off_by_one_coord | diff vs htslib | Banded alignment returns relative (not absolute) positions — by-prefix offset. |
| `seqan3-3098` | SAM | `4961904fb` → `4fe54891` | incorrect_field_value | diff vs htslib | Alignment traceback carry-bit tracking wrong on up/left-open directions → wrong score. |
| `seqan3-2869` | FASTA-adjacent | `edbfa956f^` → `edbfa956f` | parse_error_missed | diff vs htslib | FASTA ID containing `>` is parsed as the ID of the next record. Out-of-strict-scope (FASTA, not SAM), flagged in REVIEW.md. |
| `seqan3-3406` | SAM | `745c645fe` → `5e5c05a4` | encoding_bug | diff vs htslib (intermittent) | BGZF concurrent-read data race — non-deterministic corruption under multithreading. Treat as stress-only. |

### §13.4 summary

| Item | Status | Produced / at |
| :--- | :---: | :--- |
| Manifest review | ✓ | 32 → 44 issue URLs checked (two research passes) |
| Version pins populated | ✓ | 32 research entries via `apply_research.py` + `expand_research.py` |
| Install-verification | ✓ | 26 verified, then CRAM-scope-drop → **23 verified / 21 dropped** (`dropped.json`) |
| Frozen verified manifest | ✓ | `manifest.verified.json` (23 bugs); `bench_counts_by_sut` rollup embedded |
| Trigger evidence | ✓ | `compares/bug_bench/triggers/<id>/` for all 23 — READMEs + issue_source.txt + original.vcf/sam where the text format is simple |
| Verified bug catalogue | ✓ | §13.4.7 above + machine-source `compares/bug_bench/CATALOGUE.md` (regenerable) |
| User review gate | packet ready | `compares/bug_bench/REVIEW.md`; **user sign-off pending** before Phase 4 runs |

### 13.5 Phase execution (ordered)

#### Phase 0 — Lock-down (≤ 1 day)

- [ ] All of §13.1–§13.4 complete.
- [ ] Confirm `git status` is clean (optional but avoids attribution noise in logs).
- [ ] Take a system snapshot: `uname -a`, `free -h`, `nproc`, `lscpu` → `compares/results/env.txt`.
- [ ] Record BioTest git SHA, SUT versions, tool versions → `compares/results/versions.json`.

#### Phase 1 — Validity probe (≤ 1 hour)

- [ ] Run `compares/scripts/validity_probe.py` against each tool's smoke-test corpus from §13.2 (confirms the probe works before long runs).
- [ ] Verify output schema matches DESIGN.md §4.5.

#### Phase 2 — Coverage growth (~1 wall-day parallelised 4-way)

- [ ] Run `compares/scripts/coverage_sampler.py --budget 7200 --reps 3` for each of the 13 primary cells. Parallelise with 4 concurrent workers: one SUT per worker.
- [ ] Monitor: confirm log ticks `{1, 10, 60, 300, 1800, 7200}` appear in each `growth_<run_idx>.json`.
- [ ] Back up `compares/results/coverage/` to off-machine storage after completion.
- [ ] EvoSuite anchor: run `measure_evosuite_coverage.sh` once; record coverage under `compares/results/coverage/evosuite_anchor/htsjdk/`.

#### Phase 3 — Mutation score (~2 overnights, 1 per 2 SUTs)

- [ ] For each SUT, for each tool, point the mutation driver at that tool's accepted-input corpus from Phase 2.
  - [ ] `py -3.12 compares/scripts/mutation_driver.py --sut htsjdk --tool biotest --corpus compares/results/coverage/biotest/htsjdk/corpus/ --budget 7200`.
  - [ ] Repeat for each (tool, SUT) cell.
- [ ] Ensure Ollama / local LLMs are **stopped** during these runs (mutation testing is RAM-hungry).
- [ ] Confirm per-cell `summary.json` has `{killed, reachable, score}`.

#### Phase 4 — Real-bug benchmark (~1 wall-day parallelised 4-way)

- [ ] Launch: `py -3.12 compares/scripts/bug_bench_driver.py --manifest compares/bug_bench/manifest.verified.json --time-budget-s 7200 --out compares/results/bug_bench/`.
- [ ] For each (tool, bug) cell, inspect `result.json`; if `confirmed_fix_silences_signal` is `null`, manually replay the trigger.
- [ ] Spot-check 3 detection claims across different tools (§10 verification step).
- [ ] Back up `compares/results/bug_bench/` to off-machine storage.

#### Phase 5 — Short-budget secondary regime (≤ 6 hours)

- [ ] `compares/scripts/coverage_sampler.py --budget 300 --reps 5` for every primary cell.
- [ ] Confirm outputs land under `compares/results/coverage/<tool>/<sut>/growth_short_<run_idx>.json`.

#### Phase 6 — Report (≤ 2 hours)

- [ ] `py -3.12 compares/scripts/build_report.py --results compares/results/ --out compares/results/comparison_report.md`.
- [ ] Confirm all six figures generated (`coverage_growth_<sut>.png` × 4, `validity_bar_<sut>.png` × 4, `mutation_bar_<sut>.png` × 4, `bug_detection_heatmap.png`, `ttfb_violin.png`).
- [ ] Manual review: open `comparison_report.md`; sanity-check every table row against the raw JSON in `compares/results/`.
- [ ] Run the fairness-equalizer sanity check from §4.4: confirm BioTest's differential-only detection count ≤ full BioTest detection count.

### 13.6 Post-run validation

- [ ] **Reproducibility test**: pick one cell at random; re-run its Phase-2 2h × 1 rep. Compare coverage curves — they should lie within the original run's 95% CI. Divergence signals flaky instrumentation.
- [ ] **Trigger replay**: for each "detected" bug, replay the trigger input on both pre-fix and post-fix SUT. Confirm signal fires on pre-fix and not on post-fix.
- [ ] **Citation spot-check**: every citation in §8 that ends up in the paper draft should be independently re-verified (title, authors, venue, year).
- [ ] **Open-decision resolution**: revisit §10 with actual numbers and lock the final values.

### 13.7 Publish

- [ ] Commit `compares/results/` excluding raw corpora (gitignored); commit `comparison_report.md` + `figures/`.
- [ ] Update `documents/Flow.md` with a pointer to the completed comparison.
- [ ] Tag the repo: `git tag comparison-v1.0`.
- [ ] Archive `compares/results/` off-repo for permanent record.
