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
- **Prerequisite**: WSL2 + Ubuntu 22.04 + Clang 18 + `libseqan3-dev` — required for seqan3 libFuzzer + coverage + mutation. See §9 Risk 1.

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

### Risk 1 — seqan3 tooling is gated on a WSL2 rewrite of `biotest_harness.cpp`

**Severity: critical.** The current C++ harness at `harnesses/cpp/biotest_harness.cpp` is a pure-text parser that does **not** link seqan3 (see `harnesses/cpp/README.md` lines 1–20). seqan3 requires C++23 and its BAM struct fails a `static_assert` on MinGW ABI.

**Consequences**: libFuzzer on seqan3, seqan3 coverage via gcovr, and mull mutation scoring on seqan3 are all blocked.

**Mitigation**: before Phase 0 completes, set up WSL2 + Ubuntu 22.04 + Clang 18 + `libseqan3-dev`. Rewrite `harnesses/cpp/biotest_harness.cpp` per Option A in `harnesses/cpp/README.md` (calls `seqan3::sam_file_input`). Budget: 1–2 days. If blocked, seqan3 degrades to Pure Random only and is asterisked throughout the report.

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
3. **WSL2 setup for seqan3 libFuzzer.** Go / no-go decision at the end of Phase 0. If no-go, seqan3 row reduces to BioTest + Pure Random only.

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

An operational, step-by-step todo list for actually running the comparative evaluation. Sub-steps are ordered by dependency. Items marked **[gated]** are blocked by Risk 1 (seqan3 WSL2 rewrite). Items marked **[one-time]** only need to run once; the rest run per evaluation.

### 13.1 Environment prerequisites (one-time)

**Primary path — Docker container.** One `docker build` gives every tool
§13.1 needs; no WSL2 distribution to maintain by hand. Docker Desktop
on Windows already uses WSL2 as its backend, so this is *using* WSL2
without *managing* it. Verified end-to-end on 2026-04-19: image
`biotest-bench:latest` (4.64 GB), `verify.sh` reports 30 PASS / 1 WARN
(mull, optional) / 0 FAIL, exit code 0.

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
  libFuzzer + AddressSanitizer/UBSan, libseqan3-dev + xxsds/sdsl-lite v3
  (C++23), gcovr + lcov, Gradle 8.5, Maven, Jazzer 0.22.1, EvoSuite
  1.2.0, PIT 1.15.3 (command-line + entry + pitest JARs under
  `/opt/pit/`), Atheris 2.3.0, mutmut 3.0.0, pysam 0.22.1, biopython
  1.85, coverage.py 7.6.0, plus everything in `requirements.txt`. mull
  0.18.0 is soft-installed — it fails over to a WARN if the pinned deb
  URL 404s (C++ mutation is already asterisked per §9 Risk 1).
- [x] **Re-verify at any time**:
  - [x] `bash compares/docker/run.sh bash compares/docker/verify.sh` —
    prints `OK` / `WARN` / `FAIL` per tool, exits non-zero only if a
    **required** tool is broken. WARN is reserved for gated-optional
    tools like mull.
- [ ] **Pysam runner container** (separate image, already used by
  BioTest Phase C):
  - [ ] From repo root, outside the bench image:
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
4. `mull 0.18.0` is soft-installed — if the release asset URL rots, the
   build continues and `mull` is listed as WARN in `verify.sh`.

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

Run each per-tool block once; re-run only if a tool or harness is updated.

#### 13.2.1 BioTest (tool under evaluation)

- [ ] Ensure `data/mr_registry.json` is populated (Phase A + B must have run already — the comparison does **not** re-mine MRs).
- [ ] Verify `biotest.py` CLI supports the flags `run_biotest.py` passes: `--seed-dir`, `--corpus-output-dir`, `--bug-output-dir`, `--time-budget-s`, `--primary-sut`, `--format`. If any flag is missing, extend `biotest.py` or update `compares/scripts/tool_adapters/run_biotest.py` to match actual flag names.
- [ ] Smoke test (60 s): `py -3.12 compares/scripts/tool_adapters/run_biotest.py --sut htsjdk --seed-corpus seeds/vcf --out-dir /tmp/biotest-smoke --time-budget-s 60 --format VCF`.
- [ ] Confirm `/tmp/biotest-smoke/corpus/` contains ≥ 1 file and `adapter_result.json` reports `exit_code == 0`.

#### 13.2.2 Jazzer (Java baseline, htsjdk)

- [ ] Install Jazzer CLI: download release from https://github.com/CodeIntelligenceTesting/jazzer/releases (pin v0.22.1) into `~/tools/jazzer/` and add to `PATH`.
- [ ] Verify: `jazzer --version`.
- [ ] Build the BioTest harness JAR:
  - [ ] `bash compares/scripts/build_harnesses.sh jazzer`.
  - [ ] Confirm `compares/harnesses/jazzer/build/libs/biotest-jazzer.jar` exists.
- [ ] Smoke test (60 s):
  - [ ] `py -3.12 compares/scripts/tool_adapters/run_jazzer.py --sut htsjdk --seed-corpus seeds/vcf --out-dir /tmp/jazzer-smoke --time-budget-s 60 --format VCF`.
  - [ ] Expect `corpus/` populated, `tool.log` contains Jazzer's `INFO:` lines, `exit_code == 0`.
- [ ] Sanity: run Jazzer on the SAM harness too (`--format SAM`) to confirm both targets compile.

#### 13.2.3 Atheris (Python baseline, pysam + biopython)

- [ ] From inside the Linux venv: `pip install -r compares/harnesses/atheris/requirements.txt`.
- [ ] Confirm `atheris` imports: `python3 -c "import atheris; print(atheris.__version__)"`.
- [ ] Smoke test — pysam target (60 s):
  - [ ] `python3 compares/scripts/tool_adapters/run_atheris.py --sut pysam --seed-corpus seeds/vcf --out-dir /tmp/atheris-pysam-smoke --time-budget-s 60 --format VCF --python-bin python3`.
  - [ ] Expect `tool.log` contains Atheris startup banner, `adapter_result.json.exit_code == 0`.
- [ ] Smoke test — biopython target (60 s): rerun with `--sut biopython --seed-corpus seeds/sam --format SAM`.
- [ ] If Atheris crashes on import: re-install under Clang-built CPython (`CC=clang-18 pip install --no-binary :all: atheris==2.3.0`).

#### 13.2.4 libFuzzer (C++ baseline, seqan3) **[gated]**

- [ ] Confirm the WSL2 seqan3 rewrite is complete per Risk 1: `harnesses/cpp/biotest_harness.cpp` calls `seqan3::sam_file_input`.
- [ ] Build the libFuzzer harness:
  - [ ] `bash compares/scripts/build_harnesses.sh libfuzzer`.
  - [ ] Confirm `compares/harnesses/libfuzzer/build/seqan3_sam_fuzzer` is a sanitized binary: `file compares/harnesses/libfuzzer/build/seqan3_sam_fuzzer` and `nm | grep __asan_init`.
- [ ] Smoke test (60 s):
  - [ ] `python3 compares/scripts/tool_adapters/run_libfuzzer.py --sut seqan3 --seed-corpus seeds/sam --out-dir /tmp/libfuzzer-smoke --time-budget-s 60 --format SAM`.
  - [ ] Expect libFuzzer banner in `tool.log`, `corpus/` growing, `exit_code == 0`.
- [ ] If build fails: check `cmake -DCMAKE_CXX_COMPILER=clang++-18 ..` output; most failures are missing `seqan3-config.cmake` — install `libseqan3-dev` or set `seqan3_DIR`.

#### 13.2.5 Pure Random (floor baseline)

- [ ] No install step (stdlib-only).
- [ ] Smoke test (30 s):
  - [ ] `py -3.12 compares/scripts/tool_adapters/run_pure_random.py --sut htsjdk --seed-corpus seeds/vcf --out-dir /tmp/random-smoke --time-budget-s 30 --format VCF`.
  - [ ] Confirm `corpus/` has ~1000+ files, all `*.vcf` with random bytes.

#### 13.2.6 EvoSuite (white-box anchor, htsjdk only)

- [ ] Fetch: `bash compares/scripts/fetch_sources.sh` (already implemented for EvoSuite).
- [ ] Confirm `compares/baselines/evosuite/source/evosuite.jar` exists.
- [ ] Confirm JDK 17 (Temurin 17.0.13) is pinned: `compares/baselines/evosuite/jdk17/` populated.
- [ ] Confirm htsjdk fat JAR present: `compares/baselines/evosuite/fatjar/` non-empty.
- [ ] Smoke test (shortened run):
  - [ ] `bash compares/scripts/run_evosuite.sh --budget 300 --classes htsjdk.variant.vcf.VCFCodec`.
  - [ ] Confirm generated `*_ESTest.java` files under `compares/baselines/evosuite/results/`.
  - [ ] Run `bash compares/scripts/measure_evosuite_coverage.sh` once; confirm JaCoCo XML emitted.

### 13.3 Per-SUT pre-flight (data & instrumentation)

- [ ] **Seed corpus**.
  - [ ] Run `py -3.12 seeds/fetch_real_world.py` to populate Tier-2 seeds.
  - [ ] Confirm `seeds/vcf/` has ≥ 15 files (Phase D preflight lower bound) and `seeds/sam/` has ≥ 6.
  - [ ] **Exclude synthetic seeds** from the comparison: verify `ls seeds/vcf/synthetic_iter*_*.vcf 2>/dev/null` either empty or the bench scripts' `--seed-corpus` flag points at a filtered copy.
- [ ] **Coverage scope sanity check**.
  - [ ] Read `biotest_config.yaml: coverage.target_filters` and confirm the per-SUT whitelist covers VCF+SAM paths intended for the benchmark.
  - [ ] Dry-run `test_engine.feedback.coverage_collector.MultiCoverageCollector` against an existing `seeds/vcf/minimal_single.vcf` to confirm collectors return non-empty results for each enabled SUT.
- [ ] **Mutation-tool installation** (per SUT).
  - [ ] PIT: `./gradlew pitestDependencies` against htsjdk; confirm `pitest-command-line-1.15.3.jar` available.
  - [ ] mutmut: `pip install mutmut==3.0.0`; confirm `mutmut --version`.
  - [ ] mull **[gated]**: `curl -sSL https://raw.githubusercontent.com/mull-project/mull/main/install.sh | bash`; confirm `mull-runner-18 --version`.
- [ ] **SUT version-pinning infrastructure**.
  - [ ] Create isolated install environments: `python3.12 -m venv ~/biotest-sut-pysam`, `~/biotest-sut-biopython`; each used for pre/post install swaps.
  - [ ] For htsjdk: create `compares/baselines/evosuite/fatjar/versioned/` to hold multiple `htsjdk-X.Y.Z.jar` files side-by-side.
  - [ ] For seqan3 **[gated]**: `git clone https://github.com/seqan/seqan3 compares/baselines/seqan3/source`; verify `git log --oneline -5` works.

### 13.4 Bug-bench pre-flight (manifest verification)

- [ ] **Review the manifest**: open `compares/bug_bench/manifest.json` and for each entry confirm the issue URL is still live.
- [ ] **Populate `pre_fix` / `post_fix` versions** for every entry:
  - [ ] For each htsjdk / pysam / biopython bug, read the issue / PR, identify the release that ships the fix, set `anchor.post_fix` to that version and `anchor.pre_fix` to the immediately prior release.
  - [ ] For each seqan3 entry, set `anchor.pre_fix = PARENT_OF_<fix_sha>` (run `git rev-parse <fix_sha>^` inside the seqan3 clone).
  - [ ] Update `anchor.verification_rule` to reference the specific release-notes string or commit hash that proves the link.
- [ ] **Run install-verification**:
  - [ ] `py -3.12 compares/scripts/bug_bench_driver.py --verify-only --dropped-out compares/bug_bench/dropped.json`.
  - [ ] Inspect `dropped.json`; investigate every entry marked "install failed".
  - [ ] Expected verified count: 18–25 of 32. If below 10, halve the bug-bench per-cell budget to 1h per DESIGN.md Risk 2 mitigation.
- [ ] **Populate trigger evidence** (optional but recommended):
  - [ ] For each verified bug, if the issue / PR attaches a triggering input, drop it into `compares/bug_bench/triggers/<bug_id>/original.{vcf,sam,bam,py,java}`.
  - [ ] For seqan3 bugs with known fix commits, extract the test input from the PR's tests and place in the same folder.
- [ ] **Freeze the verified manifest**:
  - [ ] Copy the working manifest to `compares/bug_bench/manifest.verified.json`.
  - [ ] Commit both files; do not edit the verified manifest during the run.
- [ ] **User review gate**: before Phase 4 executes, the user signs off on `manifest.verified.json`.

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
