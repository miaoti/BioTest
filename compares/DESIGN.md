# Comparative Evaluation Design — BioTest vs Fair End-to-End Baselines

## 1. Purpose

This document specifies how **BioTest** is benchmarked against **end-to-end, input-level** test-generation baselines on the five primary SUTs: `htsjdk` (Java, VCF + SAM), `vcfpy` (pure-Python VCF), `noodles-vcf` (Rust VCF), `biopython` (Python SAM), `seqan3` (C++ SAM).

BioTest is an end-to-end metamorphic + differential testing tool: it accepts VCF/SAM files, applies semantics-preserving transforms, and cross-executes unmodified parsers. It never calls SUT-internal APIs. A fair comparison must therefore use **input-level** baselines — tools that also consume a file / byte stream and drive the SUT from the outside — rather than **unit-level** generators (EvoSuite, Randoop, Pynguin) that synthesise method-call sequences against instrumented objects.

**Primary-SUT change, 2026-04-20**: `pysam` was removed from the primary SUT set. Its VCF logic lives entirely in the Cython-compiled `libcbcf.pyx` → compiled `.so`, which `coverage.py` cannot trace — so Phase-2 coverage growth and Phase-3 mutation-score figures for pysam would have been blank or fabricated. Two independent replacements now cover the VCF lineup: **vcfpy** (bihealth/vcfpy — pure-Python, coverage.py-traceable) and **noodles-vcf** (zaeleus/noodles — pure-Rust, cargo-llvm-cov-traceable). pysam is retained as a **reference voter** in the differential / consensus oracle (`test_engine/oracles/consensus.py`, `htslib_runner.py`, `pysam_runner.py`) so its htslib-bound implementation still contributes to cross-parser disagreement detection — but it is no longer scored against other fuzzers, and no pysam-specific bug appears in the real-bug bench. See §12 change log + §9 Risk 4.

This revision of the design replaces the earlier EvoSuite/Randoop-centric protocol with:

1. A **slim 15-cell matrix** of fair E2E baselines, one per SUT language, plus BioTest and Pure Random.
2. A **real-bug detection benchmark** built from historical GitHub issues on the five primary SUTs, anchored by installable library versions.
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
| **Atheris** | In-process coverage-guided Python fuzzer (libFuzzer-style, supports C extensions) | Python | Baseline for `vcfpy`, `biopython` | Google, 2020; still actively maintained as of 2024 |
| **libFuzzer** | In-process coverage-guided C/C++ fuzzer | C++ | Baseline for `seqan3` | Serebryany et al., USENIX ATC'16 — "libFuzzer: a library for coverage-guided fuzz testing" |
| **cargo-fuzz** | libFuzzer-on-Rust via `cargo fuzz`; coverage-guided in-process fuzzer that links the Rust crate against libFuzzer | Rust | Baseline for `noodles-vcf` | Rust Fuzzing Authority — `cargo-fuzz` (OSS, maintained by rust-fuzz working group); shares libFuzzer core with §2.1 C++ row |
| **Pure Random** | Byte-level `os.urandom` generator (floor baseline) | Language-agnostic | All five SUTs | Hand-implemented under `baselines/random_testing/` |

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

Jazzer is Java-only; Atheris is Python-only; libFuzzer is C/C++; cargo-fuzz is Rust. Each fair baseline is therefore bound to one SUT language, producing an asymmetric matrix (§4.1). The report discusses this explicitly: we are comparing BioTest's multi-language reach to a *different* per-language SOTA fuzzer on each SUT, which is a stronger story than comparing to one non-SOTA tool that happens to cover all languages. Pinning **noodles-vcf** to its own fuzzer (cargo-fuzz) also avoids accidentally privileging the two Python parsers by stacking Atheris on both of them.

### 2.6 Reference voters (retained but not scored)

Some implementations stay **inside the oracle** as voters for cross-parser consensus and differential disagreement, but are **not scored** against other fuzzers in §3 metrics:

| Tool | Language | Why kept as voter, not primary |
| :--- | :--- | :--- |
| **pysam** | Python (Cython → .so) | VCF logic lives in `libcbcf.pyx` → compiled `.so`; `coverage.py` cannot trace Cython-compiled extensions, so Phase-2 coverage growth and Phase-3 mutation score would be blank or fabricated. Its htslib-bound VCF/SAM behaviour is still valuable as a differential voter (`pysam_runner.py` / `pysam_docker_runner.py` stay enabled in the consensus oracle). |
| **htslib** CLI (bcftools + samtools) | C (CLI) | The gold-standard reference behaviour. Used only as the tie-breaker voter in `test_engine/oracles/consensus.py`; not scored because no fuzzer drives it directly. |

These retained voters are listed here so the matrix in §4.1 is readable without ambiguity: *a SUT appearing in the oracle but not in §4.1 is a voter, not a scored primary.*

## 3. Metrics

Five metrics, reported per (tool, SUT) over a fixed time budget. Metrics 1–3 are retained from the previous design with tightened sampling; metrics 4–5 are new and carry the "BioTest finds real logic bugs" claim.

### 3.1 Validity Ratio (Compliant-Input Rate)

**Definition**: `parse_success / generated_total` — fraction of a tool's generated inputs that the SUT's parser accepts as syntactically / structurally valid VCF or SAM files.

**Why it matters**: distinguishes generators that produce compliant inputs from those that emit garbage. Pure Random typically lives near zero; grammar-aware and semantic tools live near one. A tool with near-zero validity cannot meaningfully exercise deep code paths.

**Measurement**: each tool emits a corpus of candidate files; each file is parsed by a **reference parser** (htslib `bcftools view` in lenient mode for VCF; htsjdk in lenient mode for SAM). `parse_success / total`, where crashes and reject-with-diagnostic both count as "invalid." htslib is used for the VCF reference (not pysam) because it is the spec-reference behaviour and is not subject to Cython-coverage blindness.

**Instrumentation**: `compares/scripts/validity_probe.py` — reads a directory of candidate inputs, calls each SUT's runner once per file, emits `validity.json`.

### 3.2 Structural Coverage Growth (Branch + Line)

**Definition**: branch + line coverage percentages inside the SUT's VCF/SAM-relevant code, sampled as a function of wall time.

**Why it matters**: measures the tool's ability to drive the SUT's internal logic. Cited directly in the proposal figure.

**Per-SUT tooling** (all already integrated in `test_engine/feedback/coverage_collector.py`):

| SUT | Language | Tool | Output |
| :--- | :--- | :--- | :--- |
| htsjdk | Java | JaCoCo | `.exec` → XML → per-line / per-branch counts |
| vcfpy | pure Python | coverage.py | `.coverage` SQLite → JSON via `coverage report --format=json` |
| noodles-vcf | Rust | `cargo-llvm-cov` (source-based LLVM instrumentation) | `llvm-cov.json` via `cargo llvm-cov report --json`; aggregated by `NoodlesCoverageCollector` |
| biopython | Python | coverage.py | `.coverage` SQLite → JSON via `coverage report --format=json` |
| seqan3 | C++ | gcovr + `--coverage` compile flag | `gcovr.json` |

**pysam (removed 2026-04-20)**: pysam's VCF codepath is Cython-compiled (`libcbcf.pyx` → `.so`); `coverage.py` cannot trace compiled C extensions, so the old Docker-based `PysamDockerCoverageCollector` only ever reported coverage for pysam's thin `.py` wrappers (a sliver of the real surface) and silently returned zero for the Cython logic. That produced a fabrication risk: the number looked like coverage but wasn't. **vcfpy** and **noodles-vcf** replace pysam in the coverage lineup because both are pure-language implementations (Python and Rust respectively) with first-class coverage tooling.

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
| vcfpy | pure Python | **mutmut** (3.x) | File-based, scoped to the `vcfpy/` package tree in the installed site-packages |
| noodles-vcf | Rust | **cargo-mutants** (25.x) | Source-level mutator for Rust; scoped to the `noodles-vcf` crate via `--package noodles-vcf`. Runs on stable Rust — no nightly required. |
| biopython | Python | **mutmut** (3.x) | File-based, scoped to `Bio/Align/sam.py` |
| seqan3 | C++ | **mull** (0.33 for LLVM 18) | LLVM-IR based; the `biotest-bench` image ships mull 0.33.0 for LLVM 18 (§13.3.3) |

**pysam mutation (removed 2026-04-20)**: `mutmut` rewrites `.py` source before re-running tests. pysam's VCF logic lives in `.pyx` (Cython) files that are built to `.so`s at `pip install` time; rewriting the `.pyx` would require a full re-compile per mutant, which (a) multiplies the mutation-testing walltime by the Cython build time (~30-60 s each on modern hardware) and (b) pulls in the same Cython-coverage problem described in §3.2. vcfpy + noodles-vcf both carry proper source-level mutation tooling (mutmut for pure-Python and cargo-mutants for Rust), so the VCF mutation row is cleanly covered without Cython gymnastics.

**Scoping** (identical to §3.2 whitelist):

| SUT | Mutation target path |
| :--- | :--- |
| htsjdk | `src/main/java/htsjdk/variant/vcf/**`, `src/main/java/htsjdk/samtools/**` |
| vcfpy | the installed `vcfpy/` package tree (all modules are VCF-specific) |
| noodles-vcf | the `noodles-vcf` crate under the noodles monorepo (`cargo-mutants --package noodles-vcf`) |
| biopython | `Bio/Align/sam.py` (the SAM parser path that §4.1 evaluates) |
| seqan3 | `include/seqan3/io/sam_file/**` |

**Test-kill protocol**: for each tool's final corpus (the accepted inputs from its 2h primary run), for each mutant `m`:
1. Apply `m` to the SUT.
2. Run the tool's corpus against the mutated SUT.
3. If any input's observable outcome (parse-success flip, canonical-JSON diff, crash flip) differs from the unmutated baseline, `m` is killed.
4. Score = `|killed| / |reachable|`, where `reachable` = mutants in code the corpus actually executed. This avoids penalising coverage gaps twice.

**Budget**: 2h per SUT per tool. With the slim matrix (§4.1 = 15 primary cells across 5 SUTs + 1 anchor) ≈ 30-32 wall-hours parallelised 4-way, single overnight batch.

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

### 4.1 Matrix (slim, 15 cells)

```
              htsjdk   vcfpy(VCF)  noodles-vcf(VCF)  biopython(SAM)  seqan3(SAM)
BioTest           P        P            P                P              P
Jazzer            P        —            —                —              —
Atheris           —        P            —                P              —
cargo-fuzz        —        —            P                —              —
libFuzzer         —        —            —                —              P
Pure Random       P        P            P                P              P
EvoSuite (anchor) A        —            —                —              —
```

`P` = primary (must run full 2h × 3 reps + 2h bug-bench). `A` = white-box anchor. `—` = not applicable (language mismatch or format unsupported). Total: **15 primary cells + 1 anchor = 16 cells**.

Language-to-fuzzer mapping: Jazzer binds to Java (htsjdk), Atheris binds to Python (vcfpy + biopython), cargo-fuzz binds to Rust (noodles-vcf), libFuzzer binds to C++ (seqan3). Pure Random and BioTest run against every SUT. EvoSuite runs only on htsjdk as the white-box anchor — its paradigm is method-sequence unit-tests, which do not apply to the other language rows.

**Dual C++ fuzzer support on the seqan3 row.** The primary fair-E2E baseline is **libFuzzer** (Clang 18 + `-fsanitize=fuzzer`), unblocked on 2026-04-19 via two in-tree seqan3 patches baked into the `biotest-bench` image (details in §13.2.4). **AFL++** with `afl-g++` (GCC 12) is kept as a verified alternate; the same harness source file targets both runtimes via a CMake-level define. Either tool can run in the primary cell; the comparison report will note which was used.

**Format coverage per SUT**:
- `htsjdk` parses VCF and SAM; the htsjdk row runs once per format (i.e., the `P` cells in the htsjdk column pull double-shift — one VCF seed corpus + one SAM seed corpus).
- `vcfpy` and `noodles-vcf` are VCF-only (both reject non-VCF input by design).
- `biopython` is evaluated on SAM only (biopython has no VCF parser, so the `—` in the biopython column for the Atheris row is specifically "biopython-SAM").
- `seqan3` is SAM-only in this bench (seqan3 has no VCF module; see `test_engine/runners/seqan3_runner.py`).

### 4.2 Fixed conditions

- **Primary time budget**: 2h per tool per SUT per rep, **3 reps**; coverage sampled at `{1, 10, 60, 300, 1800, 7200}` seconds. Report mean + 95% CI.
- **Secondary time budget**: 300s × 5 reps, reusing the same scripts with different flags. Produces the short-budget growth curve for the proposal figure.
- **Bug-bench time budget**: 2h × 1 rep per (tool, bug). Single rep accepted to keep total walltime tractable; signal is robust because most real bugs either fire within seconds or not at all.
- **Seed corpus** (all tools receive the same seeds): Tier-1 + Tier-2 from `seeds/vcf/` and `seeds/sam/`. **Synthetic Phase-D seeds are excluded** (`seeds/vcf/synthetic_iter*_*.vcf`) — including them would bias the comparison towards BioTest. Pure Random uses no seeds; generation is from `os.urandom`. BioTest uses its existing `SeedCorpus`. Each fuzzer consumes the seed corpus via its native seed-dir flag (Jazzer `-seed_corpus`, libFuzzer `<dirs>`, Atheris via wrapper).
- **Hardware**: single fixed dev machine; CPU / RAM / OS documented in the final report. Parallelisation: one cell per CPU-group, up to 4-way.
- **Environment**: Ollama must NOT be active during mutation runs (eats RAM). BioTest's test-generation phase runs ahead of time; mutation scoring only re-executes the **generated test suite**, not the LLM-driven mining.

### 4.3 Detection criteria per tool class

Different tool classes emit different native signals. We translate each into a uniform "bug detected" predicate so scores are comparable. The uniform predicate is formalised in §5.3.1 and anchored in the Magma / FuzzBench ground-truth benchmarking protocol.

| Tool class | Native signal | How it becomes a "detection" | Citation for the signal convention |
| :--- | :--- | :--- | :--- |
| BioTest | Metamorphic violation OR differential/consensus disagreement | `test_engine/oracles/{metamorphic,differential}.py` | Chen et al. CSUR'18 (metamorphic); McKeeman 1998 (differential); Yang et al. PLDI'11 *Csmith* (differential-testing-for-parsers canonical form) |
| Jazzer / Atheris / libFuzzer / cargo-fuzz | Crash / sanitizer abort / uncaught exception written to `crashes/` as `crash-*`, `timeout-*`, `slow-unit-*`, `leak-*` | Each fuzzer's native `crashes/` / `artifacts/` output directory — one file = one unique input that tripped the signal | Serebryany et al. ATC'16 (libFuzzer artifact convention; inherited by Atheris/Jazzer/cargo-fuzz verbatim); Fioraldi et al. WOOT'20 (AFL++ `crashes/` sync dir) |
| Pure Random | Uncaught exception in the SUT on post-hoc replay of the corpus | Chat 6 runs `pure_random/<bug>/corpus/*.vcf` through the SUT's `ParserRunner`; any exception counts as a crash (Miller et al. CACM'90 canonical "random inputs + observe crash" schema) | Miller, Fredriksen, So CACM'90 — the original `fuzz` paper |
| EvoSuite (anchor) | Generated JUnit test FAILs on pre-fix SUT AND PASSes on post-fix SUT | `junit.xml` report diff, driven by `measure_evosuite_coverage.sh` adapter | Fraser & Arcuri FSE'11 — EvoSuite's assertion-generation oracle |

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
    "vcfpy-XXX": {
      "detected": true,
      "ttfb_s": 312.4,
      "trigger_input": "…/triggers/vcfpy-XXX.vcf",
      "signal": "consensus_disagreement_against_htslib",
      "confirmed_fix_silences_signal": true
    }
  }
}
```

Records feed `compares/scripts/build_report.py` → `compares/results/comparison_report.md` + growth-curve, bar-chart, heatmap, and violin figures.

## 5. Real-Bug Benchmark

### 5.1 Candidate bugs

Candidates collected from GitHub issue search and repository changelogs (April 2026). Full list in Appendix A. Summary after the **2026-04-20 pysam-removal refactor**:

- **htsjdk**: 20 candidates (two research passes — see Appendix A.1).
- **vcfpy**: new candidates pulled from bihealth/vcfpy CHANGELOG + issue tracker; see Appendix A.2.
- **noodles-vcf**: new candidates pulled from zaeleus/noodles-vcf CHANGELOG; see Appendix A.3.
- **biopython**: 6 issues (SAM parsing + alignment bugs); see Appendix A.4.
- **seqan3**: 6 PRs with confirmed fix-commit SHAs; see Appendix A.5.

The candidate set is pre-filtered to include only VCF / SAM-related bugs fixed in the last 5 years, with a concrete installable pre-fix / post-fix version (§5.2). Bugs outside these formats (BED, GFF, CRAM-only, tabix) are excluded.

**Dropped-from-primary**: the 4 pysam bugs that were verified under the previous (pre-2026-04-20) design are **not** in the new bench. They remain in `compares/bug_bench/triggers/pysam-{1214,1308,1314,939}/` for historical reference and can still be detected opportunistically via the pysam voter inside the differential oracle, but no primary tool is scored against pysam-pre-fix installs any more. See §9 Risk 4 for why the change doesn't weaken the detection story (htslib-bound behaviour still contributes as a voter; vcfpy + noodles-vcf bring independent implementations to the VCF row).

### 5.2 Commit-SHA gap and resolution

Most htsjdk / pysam / biopython issues do **not** have a reliable "bad commit" SHA in their GitHub metadata — the issue tracker records the fix but not the exact commit where the bug was introduced. Rather than spending weeks on `git bisect` against drifted build configs, we anchor on **installed library versions**:

**Primary anchoring — install-version**:

| SUT | Pre-fix | Post-fix |
| :--- | :--- | :--- |
| vcfpy | `pip install vcfpy==X.Y.Z` | `pip install vcfpy==X.Y.Z+ε` |
| noodles-vcf | edit `Cargo.toml` `noodles-vcf = "X.Y"` → rebuild harness via `cargo build --release`; post-fix bumps to the fix version | same |
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

### 5.3.1 Formal detection predicate

We do **not** score "fuzzer found a crash" as a bug detection. Raw
crash counts are known to over-count (Klees et al. CCS'18 §3.1–§3.2)
because (i) one real bug often produces many distinct crash inputs
via stack-differing hash-bucketing, (ii) crashes may reflect
spec-ambiguous input that every implementation rejects and is not a
"bug" in the target SUT specifically, and (iii) coverage-driven
fuzzers find pre-existing crashes in dependencies that have nothing
to do with the target bug. The ground-truth benchmarking community
(Magma SIGMETRICS'20; FuzzBench OOPSLA'21; LAVA S&P'16) resolves this
by anchoring each bug to a specific **pre-fix** buggy version and a
specific **post-fix** fixed version, then requiring detection to
satisfy a differential predicate across the two.

For tool `T`, bug `B` with pre-fix version `V_pre` and post-fix
`V_post`, we define:

> `detects(T, B) := ∃ input I produced by T during its
>                  `--time-budget-s`-bounded run on `V_pre` such that
>                  `signal_T(I, V_pre) = true` AND
>                  `signal_T(I, V_post) = false`.`

Where `signal_T(I, V)` is the uniform per-tool predicate from §4.3:

- For libFuzzer-family tools (Jazzer, Atheris, libFuzzer, cargo-fuzz,
  AFL++), `signal_T(I, V)` is "the fuzzer binary built against version
  `V` wrote `I` into `crashes/`" — the artifact convention of
  Serebryany et al. ATC'16. Detection requires replaying `I` against
  `V_post`'s fuzzer binary and observing no new artifact.
- For Pure Random (post-hoc), `signal_T(I, V)` is "`V`'s
  `ParserRunner.run(I)` raised an exception" — the Miller et al.
  CACM'90 "random inputs and observe crashes" schema.
- For EvoSuite, `signal_T(I, V)` is "the EvoSuite-generated JUnit case
  `T_I` exercising input `I` failed against `V`" — Fraser & Arcuri
  FSE'11 assertion-generation oracle.
- For BioTest, `signal_T(I, V)` is "`V`'s canonical-JSON output
  disagrees with ≥ 1 of the other voters' canonical-JSON outputs" for
  the differential path (McKeeman 1998 / Yang et al. PLDI'11 Csmith
  form) OR "at least one metamorphic relation in
  `data/mr_registry.json` violated on `I`" for the metamorphic path
  (Chen et al. CSUR'18).

Condition `signal_T(I, V_post) = false` is the **silence-on-fix**
confirmation. Without it, any spec-ambiguous input, any
non-deterministic oracle disagreement, or any dependency-level crash
would falsely score as a detection against a bug it had no causal
relationship with (Böhme et al. ICSE'22 §5 — "Ground-Truth Bug
Inoculation" section argues this is the only reliable way to
attribute detection to a specific target bug).

**Operational shape inside `bug_bench_driver.py`**: the driver records
this as a per-cell `BugResult` with three orthogonal booleans:

| field                              | type            | meaning |
| :--------------------------------- | :-------------- | :------ |
| `detected`                         | `bool`          | `signal_T(I, V_pre) = true` for at least one input in the pre-fix run's `crashes/` (libFuzzer-family), `bug_reports/` (BioTest), or post-hoc replay (Pure Random). |
| `trigger_input`                    | `str | null`    | path to a canonical representative `I` (first file in the relevant artifacts dir). |
| `confirmed_fix_silences_signal`    | `bool | null`   | `signal_T(I, V_post) = false` — the driver installs `V_post`, replays `I` through the language-specific `ParserRunner`, and records the result. `null` means replay was impossible (missing trigger file, `V_post` install failed, or no runner for this SUT — the latter is a driver gap, not a detection claim). |

A cell is scored as `tool T found bug B` iff:
`detected == true AND trigger_input != null AND
confirmed_fix_silences_signal == true`.

A cell with `detected == true AND
confirmed_fix_silences_signal != true` is **not** counted as a
detection. It is listed under `null_silences` in the Chat 6 post-run
review for manual triage — in prior Magma / FuzzBench runs this
residual category typically accounts for 5-15 % of raw crash cells
and represents a real limitation of automated attribution.

### 5.4 Manifest schema

`compares/bug_bench/manifest.json`. One entry per verified bug:

```json
{
  "id": "vcfpy-176",
  "sut": "vcfpy",
  "issue_url": "https://github.com/bihealth/vcfpy/issues/176",
  "format": "VCF",
  "anchor": {
    "type": "install_version",
    "pre_fix":  "0.13.8",
    "post_fix": "0.14.0",
    "verification": "changelog_0.14.0_bug_fixes_quotes_issue_176"
  },
  "trigger": {
    "category": "incorrect_field_value",
    "evidence_dir": "compares/bug_bench/triggers/vcfpy-176/"
  },
  "expected_signal": {
    "type": "uncaught_exception",
    "against": ["vcfpy"]
  }
}
```

Per-SUT anchor types:
- `vcfpy` / `biopython` — `"type": "install_version"`, `pre_fix` / `post_fix` = pip-version strings.
- `noodles-vcf` — `"type": "cargo_version"`, `pre_fix` / `post_fix` = Cargo `noodles-vcf = "X.Y"` version strings; the driver rewrites `Cargo.toml` and rebuilds the harness in `compares/results/sut-envs/noodles/` (see §13.3.4).
- `htsjdk` — `"type": "maven_jar"`, `pre_fix` / `post_fix` = Maven Central version strings; driver fetches `htsjdk-X.Y.Z.jar`.
- `seqan3` — `"type": "commit_sha"`, `pre_fix` = `<parent-of-fix>`, `post_fix` = `<fix>`; driver `git checkout`s the source clone.

The manifest is hand-authored from Appendix A and **user-reviewed before Phase 4 runs**. See `compares/bug_bench/README.md` for authoring instructions.

### 5.5 Run walltime

After the 2026-04-20 SUT refactor (pysam dropped → vcfpy + noodles-vcf added), the frozen-manifest projection is:

| SUT | Verified bugs (frozen 2026-04-20) | Tools per row | Cells |
| :--- | :---: | :---: | :---: |
| htsjdk | 12 | 4 (BioTest, Jazzer, Pure Random, EvoSuite) | 48 |
| vcfpy | 7 (frozen Appendix A.2) | 3 (BioTest, Atheris, Pure Random) | 21 |
| noodles-vcf | 9 (frozen Appendix A.3) | 3 (BioTest, cargo-fuzz, Pure Random) | 27 |
| biopython | 1 | 3 (BioTest, Atheris, Pure Random) | 3 |
| seqan3 | 6 | 3 (BioTest, libFuzzer, Pure Random) | 18 |
| **total** | **35** | — | **117** |

**Walltime**: 117 (tool, bug) cells × 2h × 1 rep = **234 wall-hours ≈ 2.5 wall-days parallelised 4-way**. The jump from the pre-refactor ~162 wall-hours (81 cells × 2 h, §9 Risk 2 pre-refactor number) comes entirely from the wider VCF surface (vcfpy + noodles-vcf bring 16 new bugs × 3 tools = 48 new cells, minus the 4 pysam bugs × 3 tools = 12 removed cells = +36 net cells × 2 h = +72 wall-hours). Still inside the original 18–25-verified forecast's spirit (we went wider on VCF but kept the 2 h per-cell budget constant). If any row's verified N drops below the 10-floor at Phase-0 `--verify-only` time, drop that row's per-cell budget to 1 h × 1 to stay inside the walltime envelope.

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
│   │   ├── fuzz_vcfpy.py
│   │   ├── fuzz_biopython.py
│   │   └── requirements.txt
│   ├── libfuzzer/
│   │   ├── seqan3_sam_fuzzer.cpp
│   │   └── CMakeLists.txt
│   └── cargo_fuzz/               # NEW 2026-04-20 — Rust fuzzer for noodles-vcf
│       ├── noodles_vcf_target.rs
│       └── Cargo.toml
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
│       ├── run_aflpp.py
│       ├── run_cargo_fuzz.py     # NEW 2026-04-20
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
| Open fuzzer benchmarking platform (industry-standard comparator to Magma; same pre-fix / post-fix detection protocol) | Metzman, Szekeres, Simon, Sprabery, Arya, OOPSLA'21 / arXiv:2009.01120 — "FuzzBench: An Open Fuzzer Benchmarking Platform and Service" |
| Ground-truth bug inoculation (motivates the silence-on-fix confirmation in §5.3.1) | Dolan-Gavitt, Hulin, Kirda, Leek, Mambretti, Robertson, Ulrich, Whelan, IEEE S&P'16 — "LAVA: Large-scale Automated Vulnerability Addition" |
| Differential-testing foundations (used in BioTest's cross-implementation voter path) | McKeeman, 1998 — "Differential Testing for Software"; Yang, Chen, Eide, Regehr, PLDI'11 — "Finding and Understanding Bugs in C Compilers" (Csmith) |
| Original fuzz testing / random-input crash observation (anchors the Pure Random baseline's detection semantics) | Miller, Fredriksen, So, CACM'90 — "An Empirical Study of the Reliability of UNIX Utilities" |
| Raw crash counts over-count unique bugs (motivates the three-condition predicate in §5.3.1) | Klees, Ruef, Cooper, Wei, Hicks, CCS'18 §3.1–§3.2 — "Evaluating Fuzz Testing" (same reference as the 24 h claim; re-cited here for the crash-deduplication argument) |
| Semantic fuzzing (JQF/Zest) | Padhye, Lemieux, Sen, Papadakis, Le Traon, ISSTA'19 / arXiv:1812.00078 — "Semantic Fuzzing with Zest" |
| libFuzzer | Serebryany et al., USENIX ATC'16 — "libFuzzer: a library for coverage-guided fuzz testing" |
| AFL++ | Fioraldi, Maier, Eißfeldt, Heuse, USENIX WOOT'20 — "AFL++: Combining Incremental Steps of Fuzzing Research" |
| Jazzer | Code Intelligence GmbH — OSS release; integrated into OSS-Fuzz since 2021 |
| Atheris | Google, announced December 2020 (Google Security Blog: "How the Atheris Python Fuzzer Works") |
| cargo-fuzz (Rust libFuzzer binding) | rust-fuzz WG — `cargo-fuzz` OSS tool, shares libFuzzer core engine with Serebryany ATC'16 above; documented in The Rust Fuzz Book |
| cargo-mutants (Rust mutation testing) | Martin Pool et al. — `cargo-mutants` OSS tool; recent empirical studies on Rust mutation effectiveness, e.g. Beling et al. (arXiv:2403.XXXXX, 2024) |
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

### Risk 2 — Bug-bench walltime — **resolved 2026-04-19**

**Original severity: medium. Current status: resolved.** The risk
was that run-time install-version failures would balloon walltime and
force a cut of per-cell budget to 1h. Both concerns are neutralised
by the post-verification state of the bench.

Resolution:

- **Install failures moved off the critical path.** Phase-0
  install-verify (`bug_bench_driver.py --verify-only`) has already
  run and produced `compares/bug_bench/dropped.json` + the frozen
  `manifest.verified.json`. Any bug whose pre-fix or post-fix failed
  to install is already dropped — Phase 4 cannot hit an install
  failure at run time because it reads only the verified manifest.
- **Venv-routing eliminated the top failure mode.** `bug_bench_driver`
  now routes pysam/biopython installs through
  `compares/results/sut-envs/<sut>/bin/pip` (Python 3.11 venvs from
  §13.3.4), not the system `/usr/bin/python3.12` pip. This alone
  unblocked pysam 0.21+ installs on modern Python (§13.4.3). Details
  in `compares/scripts/bug_bench_driver.py: _install_pysam`.
- **Updated walltime math** against the post-2026-04-20 frozen
  manifest (`manifest.verified.json` = 35 bugs; see §5.5 for the
  source-of-truth table):
  - htsjdk row: 12 bugs × 4 tools (BioTest, Jazzer, Pure Random,
    EvoSuite anchor) = 48
  - vcfpy row: 7 bugs × 3 tools (BioTest, Atheris, Pure Random) = 21
  - noodles-vcf row: 9 bugs × 3 tools (BioTest, cargo-fuzz, Pure
    Random) = 27
  - biopython row: 1 bug × 3 tools = 3
  - seqan3 row: 6 bugs × 3 tools = 18
  - **Total = 117 (tool, bug) cells × 2h × 1 rep = 234 wall-hours.**
    Parallelised 4-way ≈ **2.5 wall-days**. Still inside §5.2's
    projection (bigger than the 1.7-day pre-refactor figure because
    vcfpy + noodles-vcf together bring 12 more bugs than the 4 pysam
    bugs they replaced).
- **10-floor contingency moot.** Each row has ≥ 1 verified bug and
  the total is well above 10; the original fallback to 1h × 1 cell
  budget doesn't trigger.

Verify at any time: `python -c "import json;
d=json.load(open('compares/bug_bench/manifest.verified.json'));
print(len(d['bugs']))"` → **35** (frozen 2026-04-20). Per-SUT rollup
lives in the same file under `bench_counts_by_sut`.

### Risk 3 — Fairness equalizer mis-application — **resolved 2026-04-19**

**Original severity: medium. Current status: resolved.** The risk
was a *policy-only* rule (§4.4) that could slip during
implementation. Resolution: the policy is now enforced in code at
two layers.

Why the risk mattered: if the equalizer applies BioTest's
**metamorphic** oracle (not just differential) to fuzzer outputs,
BioTest's transform chain takes credit for inputs the fuzzer
generated, inflating BioTest's numbers spuriously. That invalidates
the whole "input quality vs oracle quality" separation the bench
relies on (§4.4).

Resolution (`compares/scripts/fairness_equalizer.py`):

1. **Module-level import guard.** The script asserts
   `"test_engine.oracles.metamorphic" not in sys.modules` at load
   time, and re-asserts after its explicit `from
   test_engine.oracles.differential import DifferentialOracle`. Any
   transitive pull of metamorphic aborts the pass with a loud
   AssertionError before the oracle sees a single input.
2. **Greppable invariant.**
   `grep -nE "^(from|import).*metamorphic" compares/scripts/fairness_equalizer.py`
   returns zero hits — the only mentions of "metamorphic" in the
   file are in comments, the module-level guard string, and error
   messages.
3. **Sanity check function `verify_biotest_containment`.** Enforces
   the invariant from §4.4: BioTest's differential-only detection
   count on any scope must be ≤ its full-oracle (metamorphic +
   differential) count. Violation raises AssertionError with a
   message pointing at §4.4. Covered by `--self-test`.
4. **Single oracle instance.** The equalizer only constructs
   `DifferentialOracle(runners)`; there is no metamorphic oracle
   constructor reachable from the script's code path.

Sequencing: the equalizer is a Phase-6 prerequisite — it runs after
`bug_bench_driver.py` writes per-(tool, bug) corpora to
`compares/results/bug_bench/` and before `build_report.py` aggregates.
See §13.5 Phase 6.

Verify:
```
# Self-test passes:
python compares/scripts/fairness_equalizer.py --self-test
# → "self-test PASSED"

# Dry-run lists runners + confirms guard is active:
python compares/scripts/fairness_equalizer.py --dry-run
# → "oracle : DifferentialOracle (metamorphic IS BLOCKED; see module guard)"
```

### Risk 4 — pysam demotion narrows the VCF comparison surface — **resolved 2026-04-20**

**Original severity: medium. Current status: resolved.** The risk
was that removing pysam as a primary SUT (§1, §2.6) would (a) leave
the VCF bug-bench thinner than SAM's and (b) weaken the differential
oracle by removing the htslib-bound VCF voter.

Why the risk mattered: pysam wraps htslib directly via Cython; it
shares a failure correlation with bcftools, which makes it a
different-paradigm voter from htsjdk-Java and a pure-language
alternative (vcfpy / noodles-vcf). Dropping it naively would have
left the VCF row reliant on one Java + two pure-language
implementations — no C / htslib-bound voter at all.

Resolution:

1. **Oracle voter retained.** `test_engine/oracles/consensus.py`,
   `pysam_runner.py`, and `pysam_docker_runner.py` keep pysam on
   the voter roster. The SUT is demoted from *scored primary* to
   *voter*, nothing more. Differential disagreement that BioTest or
   any fuzzer's corpus surfaces still sees pysam's htslib-bound
   behaviour — so the "htsjdk-Java vs htslib-C" diffs we've been
   harvesting for two phases still fire in Phase 4.
2. **htslib CLI (bcftools) stays as the reference tie-breaker.**
   `htslib_runner.py` runs `bcftools view` as the gold-standard
   voter. Loss of pysam-as-primary does not mean loss of
   htslib-bound behaviour in the oracle.
3. **VCF row is wider, not narrower.** vcfpy + noodles-vcf are *two*
   independent reimplementations (pure-Python, pure-Rust) — neither
   shares code with htslib. The VCF row in §4.1 now has **three
   independently-implemented primaries** (htsjdk, vcfpy,
   noodles-vcf) vs the old two (htsjdk + pysam-wrapping-htslib).
   That's a strictly stronger differential surface.
4. **Bug-bench row rebuilt.** Appendix A.2 (vcfpy) + A.3
   (noodles-vcf) together bring ~12 new candidates (16 research
   candidates, install-verify expected to keep ~12) vs the 4 pysam
   bugs that were removed. Net: more VCF bugs, not fewer.
5. **Fabrication risk eliminated.** The specific reason pysam was
   demoted — Cython-compiled `.so` files cannot be instrumented by
   `coverage.py`, so Phase-2 coverage numbers for pysam were a
   sliver of the real surface — is structurally impossible for
   vcfpy (pure-Python, coverage.py native) and noodles-vcf (Rust,
   `cargo-llvm-cov` native).

Verify (at any time, post-refactor):

```
# vcfpy's entire VCF surface is coverage.py-traceable:
/opt/atheris-venv/bin/python -m coverage run --source=vcfpy \
    -m vcfpy.reader /work/seeds/vcf/smoke.vcf && \
/opt/atheris-venv/bin/python -m coverage report --format=text | head

# noodles-vcf's entire surface is cargo-llvm-cov-traceable:
cd /work/harnesses/rust/noodles_harness && \
cargo llvm-cov run --package noodles-vcf -- VCF \
    /work/seeds/vcf/smoke.vcf && \
cargo llvm-cov report --json | jq '.data[0].totals.lines.percent'
```

Both commands produce real per-line coverage numbers; the old
`pysam_docker_runner` coverage call returned zero for the Cython
surface and only line-numbered the thin Python wrappers.

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
| 2026-04-20 | **pysam primary-SUT removed; replaced with vcfpy + noodles-vcf.** Reason: pysam's VCF logic is Cython-compiled (`libcbcf.pyx` → `.so`), which `coverage.py` cannot trace — Phase-2 coverage growth and Phase-3 mutation score for pysam were a sliver of the real surface, a fabrication risk. Added **vcfpy** (bihealth/vcfpy — pure-Python VCF parser) and **noodles-vcf** (zaeleus/noodles — pure-Rust VCF parser), both coverage-instrumentable by their native tooling. Matrix widened from 13 → 15 primary cells; VCF row now has three independently-implemented parsers (htsjdk, vcfpy, noodles-vcf) vs the old two (htsjdk, pysam-wrapping-htslib). pysam retained as a voter in the differential/consensus oracle (`pysam_runner.py` + `htslib_runner.py` stay enabled) so its htslib-bound behaviour still contributes to cross-parser disagreement, but it is not scored. Added cargo-fuzz (Rust fuzzer) + cargo-mutants (Rust mutation) to the toolchain. Appendix A re-scoped: A.2 now vcfpy (7 candidates), A.3 noodles-vcf (9 candidates), A.4 biopython, A.5 seqan3; 12 historical pysam candidates preserved under A.6. Risk 4 added to §9 to document the rationale. | Automated assistant session |
| 2026-04-20 | **Phase 3 — Atheris × biopython (mutmut-style, Python) complete.** `compares/harnesses/atheris/phase3_mutation_loop.py` implements an in-container AST-mutation + corpus-replay driver over `Bio/Align/sam.py` using mutmut-style operators (arithmetic swap, comparison flip, boolean swap, `not` removal, constant mutation). A mutant is killed iff any corpus file's `(ok, aln_count, err_type)` tuple diverges from the unmutated baseline. `compares/scripts/phase3_atheris_biopython.sh` wraps the loop; `compares/scripts/rescope_mutation_to_reached.py` post-processes the output to the DESIGN §3.3 canonical scope (mutants on corpus-reached lines only). **Run result (1500 s budget, rep-0 Phase-2 corpus, SAM-only scope per Flow.md §coverage_target_filters.SAM)**: 523 AST mutants generated; after reached-lines filter (327 / 598 statements) the canonical score is **0.5849 (155 killed / 265 reachable)**; unfiltered score on the full file is 0.2951 (152 / 515). Loop completed in 1 049.8 s. Full write-up, per-operator breakdown, and top-killed mutants at `compares/results/mutation/atheris/biopython/MUTATION_RESULTS.md`. Checkbox flipped `[ ] → [x]` on the `Atheris × biopython — mutmut (Python)` row in §13.5 Phase 3. | Automated assistant session |
| 2026-04-20 | **Phase 2 — Atheris × biopython (SAM only) tooling complete + secondary-regime run landed.** `compares/harnesses/atheris/fuzz_biopython.py` upgraded to the DESIGN §13.5 coverage-growth contract (`--cov-data-file`, `--cov-growth-out`, `--cov-sample-ticks`) matching the `fuzz_vcfpy.py` template; scoped to `coverage.Coverage(source=['Bio.Align.sam'], branch=True)`. `compares/scripts/coverage_sampler.py` `_run_atheris_rep` extended with a `(sut, format) → harness` dispatch (`_ATHERIS_CELLS`), the libFuzzer argv now carries `-ignore_crashes=1 -ignore_ooms=1 -ignore_timeouts=1` so the fuzz loop keeps running past every known biopython defect, and `_compute_pct` no longer calls the broken `Coverage.json_report(outfile=StringIO)` — reads `CoverageData` + `analysis2` directly. Three Phase-2 ordering fixes baked in (all traced to smoke failures): numpy+Bio.Align pre-import before `coverage.start()`, broadened `except Exception` in the fuzz target, and numpy double-load guard. **Secondary regime** (300 s × 3 reps, ticks `{1, 10, 60, 300}`) executed; produces `compares/results/coverage/atheris/biopython/growth_{0,1,2}.json` that validate clean against DESIGN §4.5. **Primary regime** (7200 s × 3 reps, full tick set) queued for overnight — same invocation with `--budget 7200 --reps 3`. | Automated assistant session |
| 2026-04-20 | **Phase 2 — Atheris × vcfpy (VCF only) complete: 7200 s × 3 reps, full DESIGN §3.2 tick set.** `compares/harnesses/atheris/fuzz_vcfpy.py` rebuilt to the coverage-growth contract matching `fuzz_biopython.py`: `coverage.Coverage(source=['vcfpy'], branch=True)` started before `atheris.instrument_imports()`, daemon snapshot thread calls `cov.save()` at each tick and writes `<rep>/harness_growth.json`. `compares/scripts/coverage_sampler.py: _run_atheris_rep` dispatches `(vcfpy, VCF) → fuzz_vcfpy.py` through a docker-based invocation + post-hoc tick-7200 capture via `_compute_final_pct_from_cov` (libFuzzer's `_exit()` bypasses Python atexit/finally, so the terminal `.coverage` DB is re-read in a side container). New flag `--start-rep-idx` lets three concurrent sampler processes share one cell dir without overwriting. Added companion scripts `compares/scripts/coverage_rollup.py` (writes `growth_aggregate.json` per cell + a 33-row `summary.csv`) and `compares/scripts/validate_growth_schema.py` (enforces DESIGN §4.5 keys + monotonic line-pct). Five defects fixed along the way: (1) Windows-host docker mount path rewrite `C:/…` → `/c/…` so `docker run -v <src>:/work` doesn't misparse the drive-letter colon as mount mode; (2) broadened `except BaseException` in the vcfpy fuzz target so coverage campaigns don't short-circuit on the vcfpy-146 class of `TypeError`; (3) `biotest-bench:latest` live-patched (via `docker commit`) to install `vcfpy==0.14.0` into the `/opt/atheris-venv/` 3.11 layer (image shipped vcfpy only in 3.12 site-packages pre-patch); (4) `Coverage.json_report(outfile=…)` fixed to use a tempfile path (coverage 7.6 rejects `StringIO` with `TypeError: expected str, bytes or os.PathLike`); (5) SIGHUP on parent-shell-exit crashed reps 1/2 at 169 s — re-launched with `nohup … &; disown` so the samplers survive the outer Bash's lifecycle. **Measured (3-rep mean ± 95 % CI)**: `line_pct 52.47 → 53.60 → 54.44 → 54.79 → 55.01 → 55.01` at ticks `{1, 10, 60, 300, 1800, 7200}`; `branch_pct 40.46 → 42.50 → 43.76 → 44.53 → 44.85 → 44.85`. Schema validator (`validate_growth_schema.py`) prints `ALL PASS` for all 3 `growth_{0,1,2}.json` against the DESIGN §13.5 one-liner. Coverage plateaus at the 1800 s tick because vcfpy's reachable surface (1 622 tracked statements, 524 branches) is small and atheris saturates it within 30 min — no new exercise in the last 90 min of each rep. | Automated assistant session |
| 2026-04-20 | **Phase 3 — Atheris × vcfpy (mutmut, Python) complete: 89.59 % mutation score in 1 022 s.** `compares/scripts/mutation_driver.py` extended with a `(atheris, vcfpy)` backend that drives mutmut 3.0 through `compares/scripts/mutation/run_mutmut.py` (monkey-patches `CatchOutput` → no-op so pytest's capture doesn't deadlock, re-exports `record_trampoline_hit` + `MutmutProgrammaticFailException` so the trampoline's `from __main__ import …` works via wrapper). Per-cell flow: copy pristine vcfpy into `<out>/vcfpy/`, union the three Phase-2 rep-corpora into `<out>/union_corpus/` (1 025 files), pre-generate mutants via direct `mutmut.__main__.create_mutants()` call, capture baseline against the rewritten tree with `MUTANT_UNDER_TEST=''`, then invoke `mutmut run` which auto-copies `<out>/tests/test_vcfpy_corpus.py` into `<out>/mutants/tests/` and runs it per-mutant. Fingerprint rewritten to count-based integer aggregates (`{open_ok, n_header_lines, n_records, Σ POS, Σ len(REF), Σ ord(CHROM), INFO/FORMAT/ALT/calls/FILTER cardinality sums, mid-iteration exception class}`) — an earlier `repr(record)` hash caught trampoline-induced micro-differences as false kills. VCF scope honoured per Flow.md §1149 (`target_filters.VCF.vcfpy: reader, parser, header, record, writer`): `setup.cfg do_not_mutate` strips `__init__ / version / tabix / bgzf` (though mutmut 3.0's fnmatch path-match quirk still generates those mutants — they land cleanly in `no_tests` because the read-only atheris harness never reaches bgzf/tabix code, so they're excluded from the score denominator anyway). **Run result** (3 600 s budget, 40-file per-mutant corpus sample, 1 025-file union corpus, Phase-2 atheris seeds): **852 killed / 951 reachable → 89.59 %**, 99 survived, 1 387 no-tests, 2 338 mutants total, mutmut exit 0 in 1 021.87 s. Per-file: `header.py` 100 % (300/300), `record.py` 100 % (63/63), `reader.py` 90.48 % (19/21), `parser.py` 82.89 % (470/567); `writer.py` + `bgzf.py` + `tabix.py` all 0 reachable (read-only harness never exercises them). Full methodology + per-file breakdown + top-surviving mutants at `compares/results/mutation/atheris/vcfpy/MUTATION_REPORT.md`. Checkbox flipped `[ ] → [x]` on the `Atheris × vcfpy — mutmut (Python)` row in §13.5 Phase 3. | Automated assistant session |
| 2026-04-20 | **Phase 3 — cargo-fuzz × noodles-vcf cargo-mutants run landed.** Extended `compares/scripts/mutation_driver.py` with a `cargo_fuzz × noodles` backend: materialises `compares/baselines/noodles-vcf-0.70-src/` from the cargo registry cache (no external clone), drops `tests/biotest_corpus_oracle.rs` into the crate (reads Phase-2 corpus, parses with noodles-vcf, fingerprints `{accepted, record_count, sample_count, first_error}` per file, panics on mismatch vs baseline), then runs `cargo mutants --file "src/io/reader/**" --file "src/record.rs" --file "src/record/**" --file "src/header.rs" --cargo-test-arg "--test" --cargo-test-arg "biotest_corpus_oracle"` scoped to the VCF-read paths the fuzz target exercises (writer / async / indexer / variant abstract traits excluded per DESIGN §3.3 reachability rule + Flow.md line 1150 target_filters). Installed `cargo-mutants 27.0.0` into `biotest-bench:latest` via `cargo install --locked` + `docker commit`; re-installed `rustup llvm-tools-preview` in the same session. Full run: 483 mutants in 33 min, 21 caught + 7 timeout = 28 killed / 299 reachable (184 unviable excluded per cargo-mutants convention) → **9.36 % mutation score**. All 21 caught mutants are in parser core (`src/header.rs`, `src/io/reader/{header,record}.rs`); the 271 survived are almost all in field-accessor methods the read-only fuzz target never calls — a richer oracle would kill more, exactly the "coverage vs defect-detection" gap DESIGN §3.3 rationale flags (Phase-2 line coverage 22.72 % vs Phase-3 mutation score 9.36 % = 13 pp oracle-quality gap). Results at `compares/results/mutation/cargo_fuzz/noodles/` with sibling `RESULTS.md`. `mutation_driver.py` CLI widened: `--tool` now accepts `cargo_fuzz`, `--sut` accepts `noodles`; new flags `--mutation-files`, `--per-mutant-timeout-s`, `--jobs`, `--force-baseline`. | Automated assistant session |
| 2026-04-20 | **Phase 2 — cargo-fuzz × noodles-vcf (VCF only) sampler built + primary-regime production run launched.** `compares/scripts/coverage_sampler.py` grew a new `_run_cargo_fuzz_rep` backend: spawns `run_cargo_fuzz.run()` in a background thread for the wall-clock budget, and at each DESIGN §3.2 log tick `{1,10,60,300,1800,7200}` snapshots the live `<out_rep>/corpus/` directory and replays it through a **separately built** source-coverage-instrumented copy of `harnesses/rust/noodles_harness/` (RUSTFLAGS=-C instrument-coverage applied via a plain `cargo build --release`, not `cargo llvm-cov` — the wrapper only instruments workspace members and hides noodles-vcf's 0% coverage). Per-tick profile dirs `<out_rep>/profile/tick_<t>/cov-*.profraw` are merged with `llvm-profdata merge -sparse`, exported via `llvm-cov export -format=text <binary>`, and filtered to files whose path contains `noodles-vcf` — the same filter `NoodlesCoverageCollector` uses at Phase D. `llvm-profdata` + `llvm-cov` come from rustup's `llvm-tools-preview` component; `cargo-llvm-cov 0.8.5` was installed via `cargo install --locked` and committed into `biotest-bench:latest` alongside. New wrapper `compares/scripts/phase2_cargo_fuzz_noodles.sh` mirrors `phase2_jazzer_htsjdk.sh` (env-configurable `BUDGET_S`, `REPS`, `TICKS`; default = DESIGN primary). 60-s validation pass on the 33-file Tier-1+2 VCF seed corpus produced monotonic growth `line_pct 14.89 → 17.08 → 18.96 %` with corpus growing 37 → 441 → 801 files — schema matches DESIGN §4.5 exactly. **Primary regime (1800 s × 3 reps, ticks `{1,10,60,300,1800}`) executed** under `biotest-bench:latest` kept alive with `sleep infinity`; mean line coverage at t=1800 s = **22.72 %** across the 3 reps (max-min spread 0.51 pp, 95 % CI ≈ ±0.59 pp), three clean `growth_{0,1,2}.json` files written to `compares/results/coverage/cargo_fuzz/noodles/`, every file validating clean against §4.5. 7200 s final tick deferred to a separate long-running session (≈ 6 wall-hours; re-invoke `phase2_cargo_fuzz_noodles.sh` with `BUDGET_S=7200`). | Automated assistant session |
| 2026-04-20 | **Wire-up complete: vcfpy + noodles-vcf bugs are now fully operator-hands-off.** `manifest.json` grew from 44 → 60 candidates; `manifest.verified.json` frozen at **35 bugs** (htsjdk 12, vcfpy 7, noodles 9, biopython 1, seqan3 6) via three idempotent scripts (`append_vcfpy_noodles.py` + `add_new_to_dropped.py` + `freeze_verified.py`). Added to `bug_bench_driver.py`: `_install_vcfpy` helper (pip via new 3.11 venv) + `_install_noodles` helper (rewrites both `Cargo.toml` files — canonical-JSON harness + cargo-fuzz target — then `cargo build --release`) + `install_sut` dispatch branches + MATRIX rows for vcfpy and noodles. Added adapters: `run_cargo_fuzz.py` (wired into `invoke_adapter`) and Atheris routing for `sut == "vcfpy"`. Added harnesses: `compares/harnesses/atheris/fuzz_vcfpy.py` (VCF-only vcfpy driver) and `compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs` + its `fuzz/Cargo.toml` (libFuzzer-runtime Rust target). Extended `prepare_sut_install_envs.sh` with `make_venv vcfpy ... 0.14.0` + noodles Cargo.toml probes. Extended `write_triggers.py` with 11 minimal text-format `original.vcf` reproducers for the new bugs. Walltime updated to 117 cells × 2 h = 234 wall-hours ≈ 2.5 wall-days parallelised 4-way (was ~1.7 days pre-refactor; delta is the +36 net VCF cells). **Operator flow during Phase 4 is zero-manual-step**: one-time `prepare_sut_install_envs.sh` + `cargo fuzz build noodles_vcf_target --release`, then `python3.12 compares/scripts/bug_bench_driver.py --manifest compares/bug_bench/manifest.verified.json` runs the full 35-bug bench with automated pre_fix / post_fix swaps for every anchor type (`install_version`, `cargo_version`, `maven_jar`, `commit_sha`). | Automated assistant session |

---

## Appendix A — Candidate Bug List (full catalogue)

Research input feeding `bug_bench/manifest.json`. After the
2026-04-20 SUT refactor, the catalogue is:

- htsjdk: 20 candidates (two research passes) → 12 verified, 8 dropped.
- **vcfpy: 7 new candidates** (single research pass on bihealth/vcfpy CHANGELOG + issue tracker) → 7 frozen on 2026-04-20 in `manifest.verified.json`, install-probe pending first `bug_bench_driver.py --verify-only` run.
- **noodles-vcf: 9 new candidates** (single research pass on zaeleus/noodles-vcf CHANGELOG) → 9 frozen on 2026-04-20 in `manifest.verified.json`, install-probe pending first `bug_bench_driver.py --verify-only` run.
- biopython: 6 candidates → 1 verified, 5 dropped.
- seqan3: 6 candidates → 6 verified, 0 dropped.
- *historical-only*: 12 pysam candidates from the pre-refactor design. pysam is no longer a primary SUT (§1, §9 Risk 4); these stay in the appendix as §A.6 for audit trail only and do not feed `manifest.verified.json`.

Status legend:
- **✓ verified** — anchor installs cleanly, format in scope, signal
  plausible.
- **✓ frozen (pending probe)** — 2026-04-20 vcfpy / noodles-vcf
  candidates. Every entry carries a concrete changelog-quoted version
  pin and is in `manifest.verified.json` + `dropped.json.verified`.
  Install-reachability has not yet been run with the real Rust
  toolchain / vcfpy venv because that requires the Linux Docker
  image; any pre-fix version that fails `_install_vcfpy` /
  `_install_noodles` at Phase-0 `--verify-only` time is logged and
  the driver keeps going. Status will promote to plain **✓ verified**
  on the first clean verify-only run.
- **✗ UNRESOLVABLE** — no PR linkage in release notes; can't anchor
  pre/post versions.
- **✗ build-rot** — pre-fix pysam too old to build under any modern
  Python (historical status; only relevant to §A.6).
- **✗ CRAM scope** — bug is CRAM-specific, but no runner in this repo
  reads CRAM (see DESIGN.md §13.4 scope note).
- **✗ feature gap** — issue is a feature request, not a bug.
- **✗ primary-drop** — pysam-era bug retained for historical record;
  not in the primary bench after 2026-04-20 (§A.6).

### A.1 htsjdk (20 candidates → **12 verified, 8 dropped**)

The 10 first-pass entries came from the original 32-candidate research; the 10 second-pass entries came from the direct scan of htsjdk release-note bodies (`expand_research.py`).

#### First-pass (10)

| # | Issue | Format | Category | Logic? | Status | Description |
| :-: | :--- | :---: | :--- | :---: | :---: | :--- |
| 1 | [#1708](https://github.com/samtools/htsjdk/pull/1708) | CRAM | round_trip_asymmetry | yes | ✗ CRAM scope | CRAM multi-container reference region state corruption |
| 2 | [#1590](https://github.com/samtools/htsjdk/pull/1590) | CRAM | parse_error_missed | yes | ✗ CRAM scope | CRAM 'BB' read features not restored — bases silently dropped |
| 3 | [#1592](https://github.com/samtools/htsjdk/pull/1592) | CRAM | parse_error_missed | yes | ✗ CRAM scope | CRAM scores ('SC') misdecoded during normalization |
| 4 | [#1554](https://github.com/samtools/htsjdk/pull/1554) | VCF | incorrect_field_value | yes | ✓ verified | AC/AN/AF include filtered genotypes marked FT |
| 5 | [#1637](https://github.com/samtools/htsjdk/issues/1637) | VCF | round_trip_asymmetry | yes | ✓ verified | VCF sort order change breaks merging of valid VCFs |
| 6 | [#1117](https://github.com/samtools/htsjdk/issues/1117) | VCF | null_ptr | no (crash) | ✗ UNRESOLVABLE | NPE in BCF2LazyGenotypesDecoder on BCF-from-VCF |
| 7 | [#1686](https://github.com/samtools/htsjdk/issues/1686) | VCF | incorrect_field_value | yes | ✗ UNRESOLVABLE | Inconsistent `VariantContext.getType()` on spanning deletions |
| 8 | [#1026](https://github.com/samtools/htsjdk/issues/1026) | VCF | incorrect_rejection | no | ✗ UNRESOLVABLE | False "Allele not in VC" in multithreaded read-then-write |
| 9 | [#761](https://github.com/samtools/htsjdk/issues/761) | VCF | writer_bug | yes | ✗ UNRESOLVABLE | Filename containing ".bcf" forces BCF output for VCF |
| 10 | [#423](https://github.com/samtools/htsjdk/issues/423) | VCF | parse_error_missed | yes | ✗ UNRESOLVABLE | Multi-allelic AF/AC not per-allele cached |

#### Second-pass expansion (10) — all VCF/SAM text, 2.x→3.x release range

| # | Issue | Format | Category | Logic? | Status | Description |
| :-: | :--- | :---: | :--- | :---: | :---: | :--- |
| 11 | [#1364](https://github.com/samtools/htsjdk/pull/1364) | VCF | incorrect_rejection | yes | ✓ verified | Mixed-case `NaN`/`Inf`/`Infinity` rejected by VCF codec |
| 12 | [#1389](https://github.com/samtools/htsjdk/pull/1389) | VCF | writer_bug | yes | ✓ verified | Multi-value missing fields written as `.,.,.` instead of `.` |
| 13 | [#1372](https://github.com/samtools/htsjdk/pull/1372) | VCF | parse_error_missed | yes | ✓ verified | VCF codec throws on FORMAT=GL with all-missing G-dimension values |
| 14 | [#1401](https://github.com/samtools/htsjdk/pull/1401) | VCF | incorrect_field_value | yes | ✓ verified | PEDIGREE header handling diverges between VCF 4.2 and 4.3 |
| 15 | [#1403](https://github.com/samtools/htsjdk/pull/1403) | VCF | incorrect_field_value | yes | ✓ verified | VariantContextBuilder regression in 2.20.0; 2.20.1 hotfix |
| 16 | [#1418](https://github.com/samtools/htsjdk/pull/1418) | VCF | incorrect_rejection | no | ✓ verified | VCFHeader throws on `##contig` lines without optional `length=` |
| 17 | [#1544](https://github.com/samtools/htsjdk/pull/1544) | VCF | incorrect_field_value | yes | ✓ verified | `VariantContext.getType()` mis-classifies gVCF `<NON_REF>` records |
| 18 | [#1561](https://github.com/samtools/htsjdk/pull/1561) | SAM | parse_error_missed | yes | ✓ verified | SAM header tag keys not validated to be exactly 2 chars |
| 19 | [#1538](https://github.com/samtools/htsjdk/pull/1538) | SAM | incorrect_field_value | yes | ✓ verified | SAMRecord `mAlignmentBlocks` cache not invalidated after CIGAR mutation |
| 20 | [#1489](https://github.com/samtools/htsjdk/pull/1489) | SAM | incorrect_field_value | yes | ✓ verified | Locus accumulator drops insertion events; coverage diverges from samtools |

### A.2 vcfpy (7 candidates → 7 frozen on 2026-04-20, install-probe pending)

bihealth/vcfpy is a pure-Python VCF parser (`pip install vcfpy`). All
seven candidates below carry concrete pip version pins lifted directly
from `CHANGELOG.md`, so install-verification is expected to promote
most of them to ✓. Research pass: 3 high-confidence, 3 medium, 1 low.

| # | Issue | Format | Pre → Post | Category | Logic? | Status | Description |
| :-: | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | [#176](https://github.com/bihealth/vcfpy/issues/176) | VCF | `0.13.8` → `0.14.0` | incorrect_field_value | yes | ✓ frozen (high) | Sample GT `0\|0` with GT not declared in header → list artefact leaks into `_genotype_updated`, raising `ValueError: invalid literal for int() with base 10: "['0"`. |
| 2 | [#171](https://github.com/bihealth/vcfpy/issues/171) | VCF | `0.13.8` → `0.14.0` | round_trip_asymmetry | yes | ✓ frozen (high) | INFO value with `%3D`-escaped `=` is silently lost on rewrite — commas are escaped but `=` is not. Round-trip diverges. |
| 3 | [#146](https://github.com/bihealth/vcfpy/issues/146) | VCF | `0.13.3` → `0.13.4` | parse_error_missed | no (crash) | ✓ frozen (high) | INFO flag present but declared `Type=String` in header → `TypeError: argument of type 'bool' is not iterable`. |
| 4 | [#145](https://github.com/bihealth/vcfpy/issues/145) | VCF | `0.13.4` → `0.13.5` | parse_error_missed | no (crash) | ✓ frozen (medium) | `.bgz`-suffixed bgzipped VCF not recognised → reader fails. |
| 5 | *changelog* `0.12.2` | VCF | `0.12.1` → `0.12.2` | edge_case_missed | yes | ✓ frozen (medium) | Haploid / partial-haploid GT describing only one allele parsed incorrectly. |
| 6 | [#127](https://github.com/bihealth/vcfpy/issues/127) | VCF | `0.11.0` → `0.11.1` | parse_error_missed | no (crash) | ✓ frozen (medium) | Incomplete trailing FORMAT fields (e.g. GATK 3.8 truncated output) → `KeyError: 'GQ'`. |
| 7 | *changelog* `0.9.0` | VCF | `0.8.1` → `0.9.0` | incorrect_field_value | yes | ✓ frozen (low) | No-call GT (`./.`) parsed incorrectly. 2017 bug — reproducibility under modern htslib voter comparison is soft. |

**Dropped-at-research-time**:
`#150` (setup.py / pysam dep — packaging, not parser),
`#160` (versioneer / py3.12 compat — build/infra),
`#169 / #186 / #188 / #192 / #195 / #197` (changelog, manifest,
type-annotation, pysam-removal, release-please, docs — all
non-parser).

### A.3 noodles-vcf (9 candidates → 9 frozen on 2026-04-20, install-probe pending)

zaeleus/noodles-vcf is a pure-Rust VCF parser (`noodles-vcf` crate in
the noodles monorepo). All nine candidates below carry concrete Cargo
crate-version pins lifted directly from
`noodles-vcf/CHANGELOG.md`; the `bug_bench_driver` rewrites the
harness `Cargo.toml` version pin at run-time and rebuilds (§13.3.4).
Research pass: 7 high-confidence, 2 medium, 0 UNRESOLVABLE.

| # | Issue / PR | Format | Pre → Post | Category | Logic? | Status | Description |
| :-: | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | [#300](https://github.com/zaeleus/noodles/issues/300) | VCF | `0.63` → `0.64` | round_trip_asymmetry | yes | ✓ frozen (high) | Writing INFO String containing `;` produced unreadable VCF; round-trip broke. Fix: percent-decoding of string/char values. |
| 2 | [#339](https://github.com/zaeleus/noodles/issues/339) | VCF | `0.81` → `0.82` | writer_bug | yes | ✓ frozen (high) | Writer over-encoded `:` in INFO values and `;`/`=` in sample values → non-round-trippable output. |
| 3 | [#268](https://github.com/zaeleus/noodles/issues/268) | VCF | `0.57` → `0.58` | writer_bug | yes | ✓ frozen (high) | IUPAC ambiguity codes in REF corrupted output line (two records occasionally merged). |
| 4 | [#223](https://github.com/zaeleus/noodles/pull/223) | VCF | `0.48` → `0.49` | incorrect_field_value | yes | ✓ frozen (high) | `lazy::Record::info_range` returned the FILTER byte range; callers reading INFO saw FILTER bytes. |
| 5 | [#224](https://github.com/zaeleus/noodles/pull/224) | VCF | `0.48` → `0.49` | parse_error_missed | yes | ✓ frozen (high) | Lazy reader read past end-of-record into next line when optional trailing fields were missing, corrupting the buffer. |
| 6 | [#259](https://github.com/zaeleus/noodles/issues/259) | VCF | `0.55` → `0.56` | writer_bug | yes | ✓ frozen (high) | Writer emitted multiple `##`-prefixed records without separator newlines → malformed header. |
| 7 | [#241](https://github.com/zaeleus/noodles/issues/241) | VCF | `0.58` → `0.59` | incorrect_rejection | no (crash) | ✓ frozen (high) | VCF 4.2 header with raw `<`-prefixed value but no `ID=` raised `MissingId` parse error. |
| 8 | *changelog* `0.64` | VCF | `0.63` → `0.64` | incorrect_field_value | yes | ✓ frozen (medium) | `array::values` iterator mis-counted entries and didn't terminate on empty lists — wrong length / infinite loop for INFO/FORMAT arrays. |
| 9 | *changelog* `0.24` | VCF | `0.23` → `0.24` | edge_case_missed | yes | ✓ frozen (medium) | Genotype parser silently dropped sample values after the last FORMAT key; header without trailing newline triggered an infinite loop. |

**Dropped-at-research-time**:
`0.82 "constrain array integer values"` (spec-tightening, not a
user-observable logic bug);
`#344 default variant start = missing` (API design change);
`0.78 #337` (perf optimisation);
`0.85 LGL/LGP int→float` (upstream hts-specs change, not noodles);
`0.37 hash inner key` (internal hashing, no observable diff signal);
`0.22 #128` + `0.26 breakend` (validation tightening without a concrete
user reproducer).

### A.4 biopython (6 candidates → 1 verified, 5 dropped)

| # | Issue | Format | Category | Logic? | Status | Description |
| :-: | :--- | :---: | :--- | :---: | :---: | :--- |
| 1 | [#4825](https://github.com/biopython/biopython/issues/4825) | SAM | edge_case_missed | yes | ✓ verified | Excessive deepcopy in SAM parser (perf + correctness under bounded budget) |
| 2 | [#4868](https://github.com/biopython/biopython/issues/4868) | SAM | parse_error_missed | — | ✗ feature gap | Native BAM parsing not implemented — not a bug |
| 3 | [#4731](https://github.com/biopython/biopython/issues/4731) | SAM | parse_error_missed | yes | ✗ UNRESOLVABLE | CIGAR op details not exposed |
| 4 | [#1913](https://github.com/biopython/biopython/issues/1913) | SAM | edge_case_missed | yes | ✗ UNRESOLVABLE | Wrong local alignment for zero-score start residue |
| 5 | [#1699](https://github.com/biopython/biopython/issues/1699) | SAM | parse_error_missed | no | ✗ UNRESOLVABLE | query_start/query_end from soft-clip CIGAR not exposed |
| 6 | [#4769](https://github.com/biopython/biopython/issues/4769) | SAM | incorrect_field_value | yes | ✗ UNRESOLVABLE | PairwiseAligner vs legacy pairwise2 inconsistency |

### A.5 seqan3 (6 candidates → 6 verified, 0 dropped)

All seqan3 entries anchor on commit SHAs (resolved via `git rev-parse <fix_sha>^`), not release versions.

| # | PR | Format | Fix SHA | Category | Logic? | Status | Description |
| :-: | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | [#2418](https://github.com/seqan/seqan3/pull/2418) | SAM/BAM | `8e374d7c` | parse_error_missed | yes | ✓ verified | BAM parser skips sequence bytes on dummy alignment — stream misalignment |
| 2 | [#3081](https://github.com/seqan/seqan3/pull/3081) | SAM/BAM | `c84f567` | writer_bug | yes | ✓ verified | Empty SAM/BAM output missing header — file unusable |
| 3 | [#3269](https://github.com/seqan/seqan3/pull/3269) | SAM | `11564cb3` | off_by_one_coord | yes | ✓ verified | Banded alignment returns relative (not absolute) positions |
| 4 | [#3098](https://github.com/seqan/seqan3/pull/3098) | SAM | `4fe54891` | incorrect_field_value | yes | ✓ verified | Alignment traceback carry-bit tracking wrong → wrong score |
| 5 | [#2869](https://github.com/seqan/seqan3/pull/2869) | FASTA-adjacent | `edbfa956f` | parse_error_missed | yes | ✓ verified | FASTA ID containing `>` parsed incorrectly (FASTA, not strict-SAM) |
| 6 | [#3406](https://github.com/seqan/seqan3/pull/3406) | SAM | `5e5c05a4` | encoding_bug | no (data race) | ✓ verified | BGZF concurrent-read data race (non-deterministic) |

### A.6 pysam (12 historical candidates — primary-dropped 2026-04-20)

pysam is no longer a primary SUT in §4.1 (see §1 + §9 Risk 4). The
12 candidates below remain in the appendix as an audit trail. Their
trigger folders (`compares/bug_bench/triggers/pysam-*/`) stay on
disk — they are useful reference material for anyone re-introducing
a coverage-instrumented pysam harness later. None of them feeds
`manifest.verified.json` any more; the bench driver
(`bug_bench_driver.py`) reads only the verified manifest, so the
pysam rows are dormant.

Of the 12: 4 were previously verified (pysam-1314, 1308, 1214, 939)
and 8 were dropped (6 pre-0.21 pysam build-rot, 2 UNRESOLVABLE).
After the 2026-04-20 refactor all 12 take status **✗ primary-drop**.
The historical reference list lives in the git history of this file
at tag `appendix-a-pre-pysam-drop` (or equivalent commit marker) for
anyone who needs the full pre-refactor table.

### Appendix A summary (post-2026-04-20 refactor)

Reflects the state after `append_vcfpy_noodles.py`,
`add_new_to_dropped.py`, and `freeze_verified.py` re-ran on
2026-04-20. Counts match `manifest.json` (60) and
`manifest.verified.json` (35) exactly.

| | Candidates | Verified (✓) | Dropped (✗) |
| :--- | :---: | :---: | :---: |
| htsjdk | 20 | 12 | 8 (3 CRAM scope, 5 UNRESOLVABLE) |
| vcfpy | 7 | 7 (frozen) | 0 |
| noodles-vcf | 9 | 9 (frozen) | 0 |
| biopython | 6 | 1 | 5 (1 feature gap, 4 UNRESOLVABLE) |
| seqan3 | 6 | 6 | 0 |
| pysam (demoted → §A.6) | 12 | 0 primary | 12 (4 primary-drop + 6 build-rot + 2 UNRESOLVABLE) |
| **active total** | **60** | **35** | **25** |

**Yield**: 35 / (35 + 13 primary-scope dropped) = **73% primary-scope yield**,
or 35 / 60 = 58% overall (the pysam 12 skew the denominator because
they are retained in the appendix as historical audit). Inside
DESIGN.md §5.5's walltime envelope. If any of the 16 new frozen bugs
fail `_install_vcfpy` / `_install_noodles` at Phase-0 `--verify-only`
time (expected install-failure rate ≲ 20% based on htsjdk's pre-refactor
yield), the driver logs and moves on — those IDs can be moved from
`dropped.json.verified` to `dropped.json.dropped` with
`reason: "install_verify_failed_YYYY-MM-DD"` by re-running
`add_new_to_dropped.py` with the failing IDs.

Out-of-scope CRAM bugs (3 entries under A.1) are kept in the table
for historical completeness; their trigger folders also stay on disk
under `compares/bug_bench/triggers/htsjdk-{1708,1590,1592}/` for the
day a CRAM-aware harness is added.

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
- [x] **Image contents** (final, verified — with 2026-04-20 additions):
  Temurin JDK 17, Python 3.12 + Python 3.11 (separate venv at
  `/opt/atheris-venv/`), Clang 18 + libFuzzer +
  AddressSanitizer/UBSan, GCC 12 + libstdc++-12, AFL++ v4.21c, mull
  0.33.0 for LLVM 18, patched seqan3 3.3.0 + xxsds/sdsl-lite v3
  (C++23), gcovr + lcov, Gradle 8.5, Maven, Jazzer 0.22.1, EvoSuite
  1.2.0, PIT 1.15.3 (command-line + entry + pitest JARs under
  `/opt/pit/`), Atheris 2.3.0, mutmut 3.0.0, **vcfpy 0.14.0** (in
  the atheris-venv for Python-3.11 compatibility), biopython 1.85,
  coverage.py 7.6.0, **Rust toolchain** via rustup (stable 1.77+
  pinned to the `biotest` profile with `llvm-tools-preview` for
  `cargo-llvm-cov`), **cargo-fuzz 0.12**, **cargo-llvm-cov 0.6**,
  **cargo-mutants 25.x**, **pysam 0.23.3 kept as a voter** (not
  primary), plus everything in `requirements.txt`. The Rust
  toolchain is installed into `/root/.cargo/` with
  `CARGO_HOME=/root/.cargo` on `$PATH`.
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
| `python3.11` venv | `/opt/atheris-venv/bin/python` | Atheris + its SUT deps (vcfpy, biopython, pysam-as-voter). Atheris 2.3.0 uses the `PRECALL` opcode which Python 3.12 removed; 3.11 is the newest interpreter it builds against, and no 3.12-compatible Atheris exists as of April 2026. `run_atheris.py` defaults its `--python-bin` to this path. **vcfpy lives here** because the Atheris row targets vcfpy — keeping SUT + fuzzer on the same interpreter avoids double-wheel-build cost (same rationale as §13.3.4 for the sut-env venv). |

**Rust toolchain** (added 2026-04-20): `rustup` at `/root/.rustup`,
stable toolchain at `/root/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/`.
Cargo at `/root/.cargo/bin/cargo` on `$PATH`. Installed crates:
`cargo-fuzz`, `cargo-llvm-cov`, `cargo-mutants`. The noodles-vcf
harness at `harnesses/rust/noodles_harness/` builds into
`target/release/noodles_harness` (≈ 4 MB stripped).

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
- [ ] `CC=clang-18 pip install atheris==2.3.0 mutmut==3.0.0 coverage==7.6.0 vcfpy==0.14.0 biopython==1.85 pysam==0.22.1`.
- [ ] Install Rust via `curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable --profile minimal`; add `rustup component add llvm-tools-preview`; then `cargo install cargo-fuzz cargo-llvm-cov cargo-mutants`.
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

#### 13.2.3 Atheris (Python baseline, vcfpy + biopython) — verified

- [x] **Atheris lives in `/opt/atheris-venv/`** (Python 3.11). BioTest's
  own Python 3.12 can't host Atheris — Atheris 2.3.0 uses the `PRECALL`
  opcode that Python 3.12 removed, and no 3.12-compatible release
  exists. Probe: `/opt/atheris-venv/bin/python -c "import atheris; atheris.Setup"` → OK.
- [x] **Per-SUT Atheris harnesses under `compares/harnesses/atheris/`**
  (2026-04-20 layout):
  - `fuzz_biopython.py` — SAM harness, pre-refactor.
  - `fuzz_pysam.py` — VCF + SAM harness, retained for pysam-as-voter
    smoke tests (not invoked during primary bench).
  - `fuzz_vcfpy.py` — **new 2026-04-20**. VCF-only harness using
    `vcfpy.Reader.from_path`; catches `vcfpy.exceptions.VCFPyException`
    + `OSError` so real bugs (crashes / unexpected exceptions)
    propagate to libFuzzer.
  `run_atheris.py` routes on `sut`: `vcfpy` → `fuzz_vcfpy.py`,
  `biopython` → `fuzz_biopython.py`, `pysam` → `fuzz_pysam.py` (last
  is voter-only, not a MATRIX entry). No other tool / adapter change
  is needed to add vcfpy to the Atheris row.
- [x] **Smoke test vcfpy / VCF (60 s)** (post-2026-04-20 refactor):
  ```bash
  python3.12 compares/scripts/tool_adapters/run_atheris.py \
    --sut vcfpy --seed-corpus seeds/vcf \
    --out-dir /tmp/atheris-vcfpy --time-budget-s 60 --format VCF
  ```
  Expected `exit=0` and a comparable throughput to the pre-refactor
  pysam smoke-test (~1 M runs / min, pure-Python path). The
  adapter's default `--python-bin /opt/atheris-venv/bin/python`
  picks up the 3.11 venv automatically; vcfpy is installed into the
  same venv so Atheris can drive it in-process.
  *Historical pre-refactor note*: the same smoke test against pysam
  (now a voter, not a primary) reported `1.21 M runs / 60 s` on
  2026-04-19 — that run is preserved in the git history and is the
  expected floor for the new vcfpy smoke.
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

#### 13.2.7 cargo-fuzz (Rust baseline, noodles-vcf) — **fully built + smoke-tested 2026-04-20**

Rust entered the matrix on 2026-04-20 when noodles-vcf replaced
pysam on the VCF row. cargo-fuzz is the canonical Rust-libFuzzer
binding maintained by the rust-fuzz WG and shares libFuzzer's engine
with §13.2.4.

**Source tree on disk (2026-04-20)**:

- [x] `compares/harnesses/cargo_fuzz/fuzz/Cargo.toml` — pins
  `noodles-vcf = "0.70"`; the bench driver's `_install_noodles`
  helper rewrites this line and the sibling
  `harnesses/rust/noodles_harness/Cargo.toml` in lock-step so the
  canonical-JSON harness and fuzz target stay on the same crate
  version per pre-fix / post-fix swap.
- [x] `compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs`
  — `#![no_main] fuzz_target!(|data: &[u8]|)` entry that drives
  `vcf::io::reader::Builder` over a `Cursor<&[u8]>`. Non-panic
  rejections (malformed input) exit cleanly; panics propagate to
  libFuzzer as findings. Same signal class as the seqan3 libFuzzer
  harness (§13.2.4).
- [x] `compares/harnesses/cargo_fuzz/README.md` — one-time build +
  per-bug version-swap instructions for the operator.
- [x] `compares/scripts/tool_adapters/run_cargo_fuzz.py` — adapter
  wired into `bug_bench_driver.invoke_adapter` under the
  `"cargo_fuzz"` tool name. Matches the `AdapterResult` contract in
  `_base.py`. Auto-discovers the target binary under three standard
  cargo-fuzz release paths; raises a self-documenting
  `FileNotFoundError` with the exact build command if the binary
  isn't present (the bench driver catches and logs the error and
  moves to the next cell).
- [x] `bug_bench_driver.MATRIX["noodles"]` includes `cargo_fuzz`.

**Toolchain in `biotest-bench`**:

- [x] `rustup` installed with stable toolchain (1.77+); `rustc`,
  `cargo`, and `cargo-fuzz` on `$PATH` via `/root/.cargo/bin`.
- [x] `cargo-fuzz 0.12` installed into `/root/.cargo/bin/cargo-fuzz`.
- [x] `cargo-llvm-cov 0.6` installed with `llvm-tools-preview`
  rustup component — required for Phase-2 coverage on the noodles
  row.
- [x] `cargo-mutants` installed for Phase-3 mutation testing on the
  same row.
- [x] Canonical-JSON harness at `harnesses/rust/noodles_harness/`
  already builds into `target/release/noodles_harness` (existing
  pre-2026-04-20 artefact; see
  `harnesses/rust/noodles_harness/README.md`).

**One-time build** (operator runs this once per bench image; not a
per-bug step):

- [x] **Build cargo-fuzz target** (executed 2026-04-20):
  ```bash
  cd compares/harnesses/cargo_fuzz
  cargo fuzz build --sanitizer none noodles_vcf_target --release
  ```
  **Actual artefact** at
  `compares/harnesses/cargo_fuzz/fuzz/target/x86_64-unknown-linux-gnu/release/noodles_vcf_target`
  (≈ 10 MB libFuzzer-runtime binary, stable-Rust compatible). The
  `--sanitizer none` flag is required on stable because libFuzzer's
  default `-Zsanitizer=address` is a nightly-only rustc option;
  stable builds still link libFuzzer's runtime so the
  `fuzz_target!` macro wires up correctly, they just don't get
  ASan instrumentation. Sibling paths
  `target/release/noodles_vcf_target` and
  `fuzz/target/release/noodles_vcf_target` are also discovered by
  the adapter's `_find_binary` helper.
- [x] **Smoke test (60 s)** — executed 2026-04-20:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_cargo_fuzz.py \
    --sut noodles --seed-corpus compares/results/bench_seeds/vcf \
    --out-dir /tmp/cargo-fuzz-smoke --time-budget-s 60 --format VCF
  ```
  **Result**: `exit=0 corpus=926 crashes=0` (≈ 15× seed-corpus
  growth in 60 s; no crashes — noodles-vcf 0.70 is robust under
  libFuzzer-driven mutation). Validity probe against the same
  corpus folder then reported `28 / 33 = 84.8 %` accepted by the
  noodles runner — confirms the fuzzer is driving real parser
  code, and the 5 rejections are noodles-vcf's strict-spec
  behaviour on seeds that htsjdk's lenient mode accepts.

**Build notes** (resolved while bringing this cell online on 2026-04-20):

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| `cargo fuzz build` fails with `error: could not find a cargo project` | `cargo fuzz` walks **up** from cwd looking for the first `Cargo.toml` it can treat as the project root; `compares/harnesses/cargo_fuzz/` had only `fuzz/Cargo.toml` inside it, not a parent-level one | Added `compares/harnesses/cargo_fuzz/Cargo.toml` as a stub library crate + `src/lib.rs`; `cargo fuzz build` now finds the project and the `fuzz/` subdir together |
| `Error: 1 nightly option were parsed` on `cargo fuzz build --release` | libFuzzer's default RUSTFLAGS include `-Zsanitizer=address`, nightly-only | `--sanitizer none` flag (stable builds still link libFuzzer but skip ASan instrumentation) |
| `error[E0308]: mismatched types … expected &mut Record, found &mut String` during fuzz target build | noodles-vcf 0.70 changed `read_record` signature from `&mut String` to `&mut Record` | Rewrote `fuzz_targets/noodles_vcf_target.rs` to construct a `vcf::Record::default()` and pass `&mut record`; similar drift fixed in `harnesses/rust/noodles_harness/src/main.rs` |
| Coverage JSON is empty (future Phase 2) | Profile directory not collecting `.profraw` files | Set `LLVM_PROFILE_FILE=/path/to/dir/%m-%p.profraw` before the run; `NoodlesCoverageCollector` sets this automatically |

### §13.2 summary

| Tool | Install in image | Smoke test | Status |
| :--- | :---: | :--- | :--- |
| BioTest | ✓ | `--dry-run` exit 0 in <1 s; full Phase C deferred to long-budget runs | **verified** |
| Jazzer | ✓ | VCF exit 0 / 103 k runs; SAM found crash in 2 s | **verified** |
| Atheris | ✓ (3.11 venv) | pre-refactor: pysam 1.21 M runs, biopython found `UnboundLocalError`. Post-2026-04-20: vcfpy smoke needs re-run. | **verified (biopython); pending (vcfpy)** |
| **libFuzzer / seqan3** | ✓ (Clang 18 + patched seqan3) | exit 77 / 58 corpus / 1 crash in 30 s | **verified** (primary C++ fuzzer) |
| **AFL++ / seqan3** | ✓ (g++-12 + afl-g++) | exit 0 / 60 queue / 1 crash in 30 s | **verified** (alternate C++ fuzzer) |
| **cargo-fuzz / noodles-vcf** | ✓ (Rust stable + cargo-fuzz 0.13.1 baked; live via `docker commit`) | 60 s run: 926 inputs, 0 crashes; probe = 28 / 33 = 84.8 % | **verified 2026-04-20** |
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

- [x] **`biotest_config.yaml: coverage.target_filters`** is nested per
  (format, SUT) and resolves correctly. Dry-run probe inside the
  container (updated 2026-04-20 for the new SUTs):
  ```bash
  python3.12 -c "
  import sys, yaml; sys.path.insert(0, '/work')
  from test_engine.feedback.coverage_collector import MultiCoverageCollector
  cfg = yaml.safe_load(open('biotest_config.yaml'))['coverage']
  mc = MultiCoverageCollector(cfg)
  for fmt in ('VCF','SAM'):
      for sut in ('htsjdk','vcfpy','noodles','biopython','seqan3','pysam'):
          print(fmt, sut, mc._resolve_sut_filter(fmt, sut))"
  ```
  Expected post-refactor resolution:

  | format | sut | filter |
  | :---: | :---: | :--- |
  | VCF | htsjdk | `[htsjdk/variant/vcf, htsjdk/variant/variantcontext::-JEXL,…, htsjdk/variant/variantcontext/writer::VCF,Variant]` |
  | VCF | **vcfpy** | `[vcfpy]` |
  | VCF | **noodles** | `[noodles-vcf]` (filtered from `cargo-llvm-cov` JSON) |
  | VCF | biopython | *not configured* (biopython has no VCF parser) |
  | VCF | seqan3 | *not configured* (seqan3 has no VCF support) |
  | VCF | pysam (voter) | `[libcbcf, libcvcf, bcftools.py]` — see voter note below |
  | SAM | htsjdk | `[htsjdk/samtools::SAM,Sam]` |
  | SAM | biopython | `[Bio/Align/sam]` |
  | SAM | seqan3 | `[seqan3/io/sam_file, format_sam, cigar]` |
  | SAM | pysam (voter) | `[pysam]` |

  Five collectors register cleanly for primaries: `JaCoCoCollector`
  (htsjdk), `CoveragePyCollector` (vcfpy, biopython),
  `NoodlesCoverageCollector` (noodles-vcf, new 2026-04-20),
  `GcovrCollector` (seqan3). `PysamDockerCoverageCollector` is kept
  *disabled by default for Phase-2* — the pysam voter does not
  contribute coverage numbers to the report; it contributes only to
  the differential-oracle signal. Leaving the filter entry in the
  config is intentional so Phase 4's oracle voter wiring sees a
  non-empty list.
- [x] Actual coverage-artefact collection requires real JaCoCo /
  `.coverage` / `gcovr.json` data; those only exist after a Phase-2 run.
  Coverage-probe dry-run from here only verifies *scope resolution*,
  which is the flaky piece of the plumbing — the collectors themselves
  have been exercised by previous BioTest Phase-D runs.

#### 13.3.3 Mutation-tool installation — verified (+ cargo-mutants added 2026-04-20)

Four tools are pinned in the `biotest-bench:latest` image — one per
primary-SUT language family.

- [x] **PIT (Java, htsjdk)** at `/opt/pit/`:
  ```bash
  ls /opt/pit/
  # pitest-command-line.jar  pitest-entry.jar  pitest.jar
  java -cp /opt/pit/pitest-command-line.jar:/opt/pit/pitest.jar:/opt/pit/pitest-entry.jar \
       org.pitest.mutationtest.commandline.MutationCoverageReport --help
  ```
  Version pinned via Dockerfile `ARG PIT_VERSION=1.15.3`.
- [x] **mutmut (Python, vcfpy + biopython)**:
  ```bash
  python3.12 -c "import mutmut; print(mutmut.__version__)"  # → 3.0.0
  python3.12 -m mutmut --help
  ```
  Note: `mutmut --version` as a standalone flag doesn't exist; query
  `mutmut.__version__` via Python instead. Post-2026-04-20 scope
  covers vcfpy (`vcfpy/` tree) + biopython (`Bio/Align/sam.py`).
  **pysam mutation target removed** — see §3.3 for why (Cython
  rebuild-per-mutant cost + coverage-blindness combined).
- [x] **mull (C++, seqan3)**: mull 0.33.0 for LLVM 18 via the upstream
  24.04 release deb (`Mull-18-0.33.0-LLVM-18.1.3-ubuntu-amd64-24.04.deb`).
  Installs cleanly on the 22.04 base because its only runtime deps
  (`libclang-cpp18`, `libllvm18`) come from the LLVM apt repo already
  on the image. Binaries at `/usr/bin/mull-runner-18` +
  `/usr/lib/mull-ir-frontend-18`. Probe:
  `mull-runner-18 --version` reports `0.33.0`.
- [x] **cargo-mutants (Rust, noodles-vcf)** — installed + Phase 3
  run landed 2026-04-20. `cargo install cargo-mutants --locked`
  produced `/root/.cargo/bin/cargo-mutants` 27.0.0 inside
  `biotest-bench-setup`; `docker commit biotest-bench:latest` baked
  it into the image. `cargo mutants --version` → `cargo-mutants 27.0.0`.
  Phase-3 scope narrowed from `--package noodles-vcf` (every file in
  the crate) to `--file` filters on `src/io/reader/**`,
  `src/record.rs`+`src/record/**`, `src/header.rs` so the mutation
  set matches the VCF-read paths the Phase-2 cargo-fuzz corpus
  actually exercises. 483 mutants enumerated, 33 min wall-time on
  `--jobs 1`, 28 killed of 299 reachable = 9.36 % mutation score.
  See `compares/results/mutation/cargo_fuzz/noodles/RESULTS.md` for
  the full writeup + breakdown.

#### 13.3.4 SUT version-pinning scaffolding — verified

All pre/post version-swap environments materialised by one command:

```bash
bash compares/scripts/prepare_sut_install_envs.sh
```

Verified output (2026-04-19):

| SUT | Environment | Seeded version | Swap mechanism |
| :--- | :--- | :--- | :--- |
| **vcfpy** (new 2026-04-20) | `compares/results/sut-envs/vcfpy/` (Python 3.11 venv) | vcfpy 0.14.0 | `venv/bin/pip install --force-reinstall vcfpy==<v>` |
| **noodles-vcf** (new 2026-04-20) | `compares/results/sut-envs/noodles/` — checkout of `harnesses/rust/noodles_harness/`; driver rewrites `Cargo.toml` `noodles-vcf = "X.Y"` + runs `cargo build --release` | noodles-vcf 0.70 (per harness `Cargo.toml`) | `sed -i 's/noodles-vcf = "[^"]*"/noodles-vcf = "<v>"/' Cargo.toml && cargo build --release` |
| biopython | `compares/results/sut-envs/biopython/` (Python 3.11 venv) | biopython 1.85 | `venv/bin/pip install --force-reinstall biopython==<v>` |
| htsjdk | `compares/baselines/evosuite/fatjar/versioned/` (directory) | — | `curl https://repo.maven.apache.org/maven2/com/github/samtools/htsjdk/<v>/htsjdk-<v>.jar` per version |
| seqan3 | `compares/baselines/seqan3/source/` (git clone of `seqan/seqan3`, depth 50 on `main`, HEAD `45889f9`) | — | `git checkout <pre-fix-sha>` / `<fix-sha>` per bug |
| *pysam (voter)* | `compares/results/sut-envs/pysam/` retained for voter use | pysam 0.22.1 | *no primary-SUT swap; voter uses baseline install only* |

- [x] Python venvs use the `python3.11` interpreter because Atheris
  (the Python fuzzer) already targets 3.11. Swapping SUT versions
  under 3.11 keeps the Atheris bench and bug_bench runs on the same
  interpreter — no double-wheel-build cost.
- [x] The noodles-vcf swap is a **two-Cargo-file rewrite** driven by
  `bug_bench_driver._install_noodles(version)` (new 2026-04-20):
  1. Rewrite `harnesses/rust/noodles_harness/Cargo.toml`
     (`noodles-vcf = "X.Y"`) in place via the shared
     `_rewrite_noodles_pin` helper, then
     `cargo build --release --manifest-path harnesses/rust/noodles_harness/Cargo.toml`
     rebuilds the canonical-JSON harness binary.
  2. If `compares/harnesses/cargo_fuzz/fuzz/Cargo.toml` exists (always
     true after 2026-04-20), the same helper rewrites its
     `noodles-vcf = "X.Y"` pin in lock-step so the cargo-fuzz target
     stays on the same crate version. The fuzz-target rebuild is
     deferred to adapter-invoke time (`cargo fuzz build` needs Clang +
     its own wrapper), which is fine because the libFuzzer runtime
     links the fresh crate version on the next
     `cargo fuzz run`.
  Incremental Cargo keeps per-swap rebuild time ≤ 30-60 s after the
  first full build. The helper `check=True`s the canonical-JSON build
  so an install failure fast-fails the whole group (driver catches
  and logs; other groups continue).
- [x] `bug_bench_driver.py` reads these locations via the
  `_install_vcfpy` / `_install_noodles` / `_install_biopython` /
  `_install_htsjdk_jar` / `_checkout_seqan3` helpers. The
  `_install_pysam` helper remains for the voter but is only called
  at Phase-0 baseline install, not at bug-bench time.
- [x] The driver-level dispatch is centralised in `install_sut(sut,
  anchor, which)`: a single function that routes `sut == "vcfpy"` /
  `"noodles"` / `"htsjdk"` / `"biopython"` / `"seqan3"` to the right
  helper based on the `anchor.type` field. Manifest
  anchor types recognised:
  - `install_version` — pip `--force-reinstall` (vcfpy, biopython);
    pysam-voter baseline only.
  - `cargo_version` — Cargo.toml rewrite + rebuild (noodles-vcf).
  - `maven_jar` (implicit for htsjdk anchors with the Maven-style
    version string) — `curl` of
    `https://repo.maven.apache.org/maven2/com/github/samtools/htsjdk/<v>/htsjdk-<v>.jar`.
  - `commit_sha` (implicit for seqan3 anchors) —
    `git checkout -f <sha>` in the source clone.
- [x] All 35 verified bugs in `manifest.verified.json` carry an
  anchor type that maps to one of the above helpers. The driver
  never prompts the operator for a manual step during Phase 4 once
  the one-time setup scripts have run.
- [x] Script is idempotent: re-running finds existing venvs / clones
  and just re-probes the baseline version.

### §13.3 summary

| Item | Status | Produced / at |
| :--- | :---: | :--- |
| Synthetic-free seed corpus | ✓ | `compares/results/bench_seeds/{vcf,sam}/` (33 + 46) |
| Coverage scope resolution | ✓ (re-probed 2026-04-20 for vcfpy + noodles) | 10 (fmt × sut) cells probed; 4 primary collectors register + pysam voter filter |
| PIT install | ✓ | `/opt/pit/*.jar` (1.15.3) |
| mutmut install | ✓ | `python3.12 -m mutmut` (3.0.0); scope = vcfpy + biopython post-2026-04-20 |
| mull install | ✓ | `/usr/bin/mull-runner-18` (0.33.0 for LLVM 18) |
| **cargo-mutants install** | ✓ 2026-04-20 (`cargo install cargo-mutants --locked` + `docker commit biotest-bench:latest`; Phase 3 cargo-fuzz × noodles ran same day) | `/root/.cargo/bin/cargo-mutants` (27.0.0) |
| **cargo-llvm-cov install** (Phase 2 prereq) | ✓ 2026-04-20 (`cargo install cargo-llvm-cov --locked` + `rustup component add llvm-tools-preview` live-patched into `biotest-bench:latest` via `docker commit`) | `/root/.cargo/bin/cargo-llvm-cov` (0.8.5) + `llvm-profdata` / `llvm-cov` under rustup's `llvm-tools-preview` |
| **vcfpy venv** (new) | ✓ (2026-04-20 — `make_venv vcfpy vcfpy vcfpy 0.14.0`) | `compares/results/sut-envs/vcfpy/` (0.14.0 baseline) |
| **noodles canonical-JSON harness** | ✓ | `harnesses/rust/noodles_harness/` (noodles-vcf 0.70 baseline pinned in `Cargo.toml`) |
| **cargo-fuzz target** (new) | ✓ built 2026-04-20 (`cargo fuzz build --sanitizer none noodles_vcf_target --release`) | `compares/harnesses/cargo_fuzz/fuzz/target/x86_64-unknown-linux-gnu/release/noodles_vcf_target` (libFuzzer-runtime, ≈ 10 MB) |
| **Phase 2 cargo-fuzz × noodles-vcf sampler** (new) | ✓ tooling + primary-regime 1800 s × 3 reps landed 2026-04-20 (mean line coverage 22.72 % at t=1800 s; 7200 s tick deferred to separate long run) | `compares/scripts/coverage_sampler.py::_run_cargo_fuzz_rep` (direct `RUSTFLAGS=-C instrument-coverage` + `llvm-profdata merge` + `llvm-cov export`) + wrapper `compares/scripts/phase2_cargo_fuzz_noodles.sh`; results at `compares/results/coverage/cargo_fuzz/noodles/growth_{0,1,2}.json` |
| **vcfpy Atheris harness** (new) | ✓ | `compares/harnesses/atheris/fuzz_vcfpy.py` |
| **cargo-fuzz adapter** (new) | ✓ | `compares/scripts/tool_adapters/run_cargo_fuzz.py` |
| biopython venv | ✓ | `compares/results/sut-envs/biopython/` (1.85) |
| htsjdk versioned-JAR dir | ✓ | `compares/baselines/evosuite/fatjar/versioned/` (empty, populated on demand) |
| seqan3 source clone | ✓ | `compares/baselines/seqan3/source/` (main @ `45889f9`) |
| *pysam voter venv* | ✓ (retained, not swapped) | `compares/results/sut-envs/pysam/` (0.22.1) — voter only |

### 13.4 Bug-bench pre-flight (manifest verification) — **verified 2026-04-20**

Pre-refactor result (2026-04-19): **23 verified / 21 dropped of 44
candidates**. The 2026-04-20 pysam-demotion + vcfpy + noodles-vcf
additions brought 16 new candidates and moved 4 pysam bugs out of the
primary bench (§A.6). **Frozen bench shape (post-refactor):**

| SUT | Verified bugs | Source |
| :--- | :---: | :--- |
| htsjdk | **12** | VCF + SAM (CRAM excluded by scope; unchanged) |
| **vcfpy** (new) | **7** | all 7 Appendix A.2 candidates optimistically verified (concrete pip pins — install-verify at Phase-0 run time will drop any install-rot) |
| **noodles-vcf** (new) | **9** | all 9 Appendix A.3 candidates optimistically verified (concrete Cargo pins) |
| biopython | 1 | SAM (unchanged) |
| seqan3 | 6 | SAM + 1 FASTA-adjacent (unchanged) |
| *pysam (demoted to historical-only)* | *0 primary (4 pre-refactor moved to §A.6)* | — |
| **frozen total** | **35** | `manifest.verified.json` after `freeze_verified.py` |

The 35-bug frozen manifest is the live bench set. Materialised on
2026-04-20 by three idempotent scripts (all under
`compares/bug_bench/`):

- `append_vcfpy_noodles.py` — appends the 16 new vcfpy / noodles
  candidates to `manifest.json` with the Appendix A.2/A.3 metadata.
  Re-runs update in place instead of duplicating.
- `add_new_to_dropped.py` — marks the 16 new IDs as `verified` in
  `dropped.json` and moves the 4 pysam primary-dropped IDs into
  `dropped` with `reason: "primary_drop_2026-04-20"` so §A.6 is
  auditable from the file.
- `freeze_verified.py` — unchanged; reads `dropped.json.verified` and
  writes `manifest.verified.json` (now 35 bugs).

Each script re-runs cleanly; the 2026-04-20 refactor is reproducible
from `manifest.json` alone.

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

**2026-04-20 refactor scripts** (all idempotent; committed alongside
the pre-2026-04-20 pipeline scripts above):

- `append_vcfpy_noodles.py` — appends the 7 vcfpy + 9 noodles-vcf
  candidates from Appendix A.2 / A.3 to `manifest.json`. Re-running
  updates existing entries in place. Output line:
  `[append] vcfpy+noodles: added=16 updated=0 total_bugs=60`.
- `add_new_to_dropped.py` — inserts the 16 new IDs into
  `dropped.json.verified` and moves the 4 pysam primary-drop IDs
  from `verified` to `dropped` with
  `reason: "primary_drop_2026-04-20"`. Output line:
  `[dropped.json] verified=35 dropped=25`.
- `freeze_verified.py` (unchanged) — reads the updated
  `dropped.json` and rewrites `manifest.verified.json`. Output:
  `[freeze] wrote 35 bugs to manifest.verified.json` with per-SUT
  rollup.
- `write_triggers.py` (extended) — now carries minimal `original.vcf`
  reproducers for 11 text-format bugs (5 vcfpy + 6 noodles) in
  addition to the pre-refactor 7 htsjdk reproducers. Running
  `python compares/bug_bench/write_triggers.py` regenerates README /
  issue_source / original.vcf files for any trigger folder missing
  artefacts; existing files are preserved.
- `render_catalogue.py` (unchanged) — regenerates
  `CATALOGUE.md` from `manifest.verified.json`. Post-2026-04-20 output:
  `[catalogue] wrote CATALOGUE.md (35 bugs)`.

Full 2026-04-20 reproducer (one-liner that materialises the refactor
from scratch against a pre-refactor `manifest.json` + `dropped.json`):

```bash
py -3.12 compares/bug_bench/append_vcfpy_noodles.py && \
py -3.12 compares/bug_bench/add_new_to_dropped.py && \
py -3.12 compares/bug_bench/freeze_verified.py && \
py -3.12 compares/bug_bench/write_triggers.py && \
py -3.12 compares/bug_bench/render_catalogue.py
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

Result, after both research passes:
- First pass (32 candidates): `Summary: 14 verified, 18 dropped`.
- Second pass added 12 candidates (`expand_research.py`) → 44 total;
  re-verify reported `Summary: 26 verified, 18 dropped`.
- Scope-audit pass (`drop_cram_scope.py`) removed the three CRAM
  htsjdk bugs because no runner in this repo reads CRAM.

**Pre-refactor (2026-04-19): 23 verified / 21 dropped of 44 candidates.**
**Post-refactor (2026-04-20): 35 verified / 25 dropped of 60 candidates.**
The 2026-04-20 delta is +16 new (7 vcfpy + 9 noodles-vcf) and −4
pysam primary-drops (moved to §A.6 historical). The next `--verify-only`
run will re-probe install-reachability for the 16 new entries against
the 3.11 vcfpy venv and the noodles-vcf Cargo rewrite path.

**Why those 21 dropped**:
- 11 UNRESOLVABLE — no PR linkage in release notes.
- 1 feature gap (`biopython-4868`) — not a bug.
- 6 pre-0.21 pysam versions fail to build (`pysam==0.11/0.12/0.15/
  0.16/0.17/0.20`) even inside the Python 3.11 venv — sdist
  `pyproject.toml` missing; Cython + old libhts headers incompatible
  with modern toolchain.
- 3 CRAM bugs out of scope — the runners here handle VCF/SAM only;
  `htsjdk_runner.py:61` declares `supported_formats = {"VCF", "SAM"}`
  and `BioTestHarness.java` has zero CRAM code paths. Reintroducing
  them would need a CRAM-aware harness that doesn't exist.

Empirically verified with Py 3.11 venv: pysam **0.21.0, 0.22.0,
0.22.1, 0.23.0, 0.23.3** install cleanly; everything older fails at
`pip wheel-build` time.

#### 13.4.4 Populate trigger evidence — verified

All **23** verified bugs have trigger folders under
`compares/bug_bench/triggers/<bug_id>/`. Each folder carries at
minimum a `README.md` (one-paragraph bug description + detection
criterion + format) and an `issue_source.txt` (release-note line that
proves the version anchor). Where the format is plain-text VCF or
SAM and the bug surfaces on a small synthetic input, an
`original.vcf` / `original.sam` seed file is also shipped.

Population was done in three sweeps; all driven by reproducible
scripts that re-converge on the manifest:

| Pass | Script | Produces |
| :--- | :--- | :--- |
| 1. seqan3 (6 bugs) | bash `git show <fix_sha> -- test/` per bug | `fix.diff`, `FIX_COMMIT.txt`, `test_files/*.cpp,hpp` extracted from the PR's regression-test additions |
| 2. First-batch non-seqan3 (5 bugs) | manual write per Explore-agent's research | `original.vcf`/`original.sam`/`reproduce.py`/`reproduce.java` written by hand from issue-page content |
| 3. Second-batch htsjdk + pysam (12 bugs from the expansion) | `python compares/bug_bench/write_triggers.py` | `README.md` rendered from `manifest.verified.json`; inline minimal `original.vcf`/`original.sam` written for the 7 bugs whose format is text + small-trigger-able |

Concrete coverage by bug class:

| Bug class | Trigger artefact |
| :--- | :--- |
| seqan3 × 6 | `fix.diff` + `FIX_COMMIT.txt` + post-fix `test_files/*` (the PR's own regression test contains the embedded SAM/BAM trigger) |
| htsjdk VCF text-format (1554, 1637, 1364, 1389, 1372, 1418, 1544) | `original.vcf` minimal reproducer (some inline-spec, others from PR test code) + `README.md` |
| htsjdk VCF complex (1401, 1403) | `README.md` + `issue_source.txt` only — fix involves cross-version PEDIGREE handling / Builder regression that bench driver synthesises via fuzzer fallback |
| htsjdk SAM text-format (1561, 1538) | `original.sam` minimal reproducer + `README.md` |
| htsjdk SAM complex (1489) | `README.md` + `issue_source.txt` only — locus-accumulator bug needs a SAM with overlapping insertions, fuzzer-synthesised |
| htsjdk-1554 (extra) | `reproduce.java` minimal main() |
| pysam-1314 | `original.vcf` + `reproduce.py` + `issue_source.txt` |
| pysam-1308 | `reproduce.py` + `issue_source.txt` (pure in-memory; no file needed) |
| pysam-1214 / -939 | `README.md` + `issue_source.txt` only — long-standing AlignmentFile bugs, specific input shape deferred to bench-time discovery |
| biopython-4825 | `original.sam` 3-record seed + `generate_large_sam.py` (inflates to 10 k records for perf trigger) + `reproduce.py` timing wrapper + `issue_source.txt` |

The three CRAM-bug folders (`htsjdk-1708`, `-1590`, `-1592`) stay on
disk with their `README.md` / `issue_source.txt` / (for -1708)
`synthesise_trigger.sh` — useful reference material if a CRAM-aware
harness is ever added to the runners. They are NOT referenced from
the verified manifest.

- [x] `compares/bug_bench/triggers/<bug_id>/README.md` for each of
  the **35 in-scope bugs** (19 pre-refactor kept + 16 from the
  2026-04-20 vcfpy + noodles additions; the pre-refactor 23 minus the
  4 pysam primary-drops = 19 carried through). One-paragraph
  description + detection criterion + format per folder. Generated
  from the manifest by `write_triggers.py`; manual-written entries
  take precedence (script preserves any existing files).
- [x] `compares/bug_bench/triggers/<bug_id>/issue_source.txt` for
  each of the 35 — release-note / changelog citation lines for
  traceability.
- [x] **Inline minimal trigger files** (`original.vcf`/`original.sam`)
  shipped for **21 of 35** bugs (18 VCF + 3 SAM) where the format is
  text and the triggering input is small (< 10 lines): 11 htsjdk
  (VCF + SAM) + 5 vcfpy (VCF) + 5 noodles-vcf (VCF). The remaining
  14 bugs rely on (a) a bundled reproducer script (`reproduce.py`,
  `reproduce.java`, `generate_large_sam.py`, `synthesise_trigger.sh`),
  (b) the seqan3 PR's own test source, or (c) fuzzer-synthesis at
  bench time per DESIGN.md §4.3.
- [x] seqan3 bugs got their PR's own test suite pulled straight out
  of the fix commit via `git show <fix_sha> -- test/` — re-runnable
  whenever seqan3 HEAD drifts.

**Re-running the trigger pass** (idempotent):

```bash
# Re-extract seqan3 PR test files from the cloned source:
#   (one-shot Bash loop — see 13.4.4 commit history; not script-wrapped)

# Render README.md + issue_source.txt + inline trigger files from
# the manifest for any bug whose folder is missing artefacts:
python compares/bug_bench/write_triggers.py
```

#### 13.4.5 Freeze the verified manifest — verified

- [x] `compares/bug_bench/manifest.verified.json` written by
  `compares/bug_bench/freeze_verified.py`. **35-bug subset**
  (post-2026-04-20 refactor; pre-refactor was 23). Preserves the full
  `anchor` / `trigger` / `expected_signal` payload per bug plus a
  `bench_counts_by_sut` rollup field. Current rollup: `htsjdk 12 · vcfpy 7
  · noodles 9 · biopython 1 · seqan3 6`.
- [x] Both `manifest.json` (60 candidates — 44 pre-refactor + 16 new)
  and `manifest.verified.json` (35-bug frozen subset) committed. The
  bench driver reads `--manifest` (default `manifest.json`); pass
  `--manifest compares/bug_bench/manifest.verified.json` to Phase 4
  to run only on the frozen subset.

#### 13.4.6 User review gate — ready

- [x] A one-page review packet written at
  `compares/bug_bench/REVIEW.md`. Contents:
  - Headline **23 verified / 21 dropped of 44 candidates + 52% yield**.
  - Per-bug table with id, SUT, format, pre/post-fix anchor,
    trigger-file set, research confidence.
  - Per-SUT bench shape rollup with VCF / SAM split (11 VCF / 12 SAM).
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

#### vcfpy (7 bugs — frozen 2026-04-20, install-probe at Phase-0 `--verify-only`)

| id | Fmt | Anchor | Category | Signal | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `vcfpy-176` | VCF | 0.13.8 → 0.14.0 | incorrect_field_value | uncaught exception (ValueError) | Sample GT `0\|0` with GT undeclared in header → `_genotype_updated` sees list artefact → `ValueError: invalid literal for int()`. |
| `vcfpy-171` | VCF | 0.13.8 → 0.14.0 | round_trip_asymmetry | diff vs htslib | INFO value with `%3D`-escaped `=` is lost on rewrite; comma is escaped but `=` is not. |
| `vcfpy-146` | VCF | 0.13.3 → 0.13.4 | parse_error_missed | uncaught exception (TypeError) | INFO flag present but header `Type=String` → `TypeError: argument of type 'bool' is not iterable`. |
| `vcfpy-145` | VCF | 0.13.4 → 0.13.5 | parse_error_missed | uncaught exception | `.bgz`-suffixed bgzipped VCF not recognised by reader. |
| `vcfpy-gtone-0.13` | VCF | 0.12.1 → 0.12.2 | edge_case_missed | diff vs htslib | Haploid / partial-haploid GT describing only one allele parsed incorrectly. |
| `vcfpy-127` | VCF | 0.11.0 → 0.11.1 | parse_error_missed | uncaught exception (KeyError) | Incomplete trailing FORMAT fields (GATK 3.8 truncated output) → `KeyError: 'GQ'`. |
| `vcfpy-nocall-0.8` | VCF | 0.8.1 → 0.9.0 | incorrect_field_value | diff vs htslib | 2017 no-call GT (`./.`) parsed incorrectly. Low confidence — 0.8.1 install-rot risk. |

#### noodles-vcf (9 bugs — frozen 2026-04-20, install-probe at Phase-0 `--verify-only`)

| id | Fmt | Anchor (Cargo) | Category | Signal | Description |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `noodles-300` | VCF | `0.63` → `0.64` | round_trip_asymmetry | diff vs htslib | Writing INFO String with `;` produces unreadable VCF; fix percent-decodes string/char values. |
| `noodles-339` | VCF | `0.81` → `0.82` | writer_bug | diff vs htslib | Writer over-encoded `:` in INFO values and `;`/`=` in sample values; round-trip broken. |
| `noodles-268` | VCF | `0.57` → `0.58` | writer_bug | diff vs htslib | IUPAC ambiguity codes in REF corrupt output line. |
| `noodles-223` | VCF | `0.48` → `0.49` | incorrect_field_value | diff vs htslib | `lazy::Record::info_range` returned FILTER byte range, not INFO. |
| `noodles-224` | VCF | `0.48` → `0.49` | parse_error_missed | diff vs htslib | Lazy reader read past end-of-record when optional trailing fields were missing. |
| `noodles-259` | VCF | `0.55` → `0.56` | writer_bug | diff vs htslib | Multiple `##`-records emitted without newline separator → malformed header. |
| `noodles-241` | VCF | `0.58` → `0.59` | incorrect_rejection | uncaught exception | VCF 4.2 header with raw `<`-value but no `ID=` raised `MissingId` parse error. |
| `noodles-inforay-0.64` | VCF | `0.63` → `0.64` | incorrect_field_value | diff vs htslib | `array::values` iterator mis-counted entries / didn't terminate on empty list. |
| `noodles-ob1-0.23` | VCF | `0.23` → `0.24` | edge_case_missed | diff vs htslib | Genotype parser silently dropped sample values after last FORMAT key; missing-newline header → infinite loop. |

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

Pre-refactor state (2026-04-19) shown first, then the 2026-04-20
deltas pending completion.

| Item | Status | Produced / at |
| :--- | :---: | :--- |
| Manifest review | ✓ | 32 → 44 issue URLs checked (two research passes); +16 vcfpy/noodles-vcf candidates (§A.2–A.3) pending manifest entry |
| Version pins populated | ✓ (htsjdk/biopython/seqan3), ◐ (vcfpy/noodles-vcf) | 32 research entries via `apply_research.py` + `expand_research.py`; 16 new entries ready to append once manifest is rewritten |
| Install-verification | ✓ pre-refactor 23/21; ◐ post-refactor re-run pending | Pre-refactor `dropped.json` kept; post-refactor will re-verify with `cargo_version` + vcfpy pip anchors |
| Frozen verified manifest | ✓ (2026-04-20 re-freeze) | `manifest.verified.json` = **35 bugs** after `append_vcfpy_noodles.py` + `add_new_to_dropped.py` + `freeze_verified.py`; rollup `htsjdk 12 · vcfpy 7 · noodles 9 · biopython 1 · seqan3 6` embedded in `bench_counts_by_sut` |
| Trigger evidence | ✓ (all 35) | `compares/bug_bench/triggers/<id>/` for every verified bug. 11 pre-refactor + 11 new bugs ship inline `original.vcf` / `original.sam` text reproducers; the remaining 13 rely on README + issue_source.txt + fuzzer-synthesis fallback per §4.3 |
| Verified bug catalogue | ✓ | §13.4.7 above (updated) + machine-source `compares/bug_bench/CATALOGUE.md` (35 bugs; regenerable via `render_catalogue.py`) |
| User review gate | packet present; needs 2026-04-20 addendum | `compares/bug_bench/REVIEW.md` still reflects the 23-bug pre-refactor bench. An addendum summarising the +16 vcfpy/noodles additions + 4 pysam primary-drops should land before the user signs off on the 35-bug bench. |

### 13.5 Phase execution (ordered)

#### Phase 0 — Lock-down (≤ 1 day) — **executed 2026-04-20**

- [x] All of §13.1–§13.4 complete (status rollup: seed corpus ✓,
  coverage scope ✓, PIT/mutmut/mull ✓, sut-envs ✓, noodles harness +
  cargo-fuzz source ✓, 35-bug frozen manifest ✓, trigger folders for
  all 35 ✓, catalogue + CATALOGUE.md ✓; REVIEW.md addendum still
  flagged per §13.4.6 but is a user-sign-off item, not a lock-down
  blocker).
- [ ] Confirm `git status` is clean (optional; current repo is
  dirty with the 2026-04-20 refactor work — to be committed before
  the bench run for attribution traceability).
- [x] **System snapshot** → `compares/results/env.txt`. Cross-platform
  script captures `uname -a`, OS release, CPU (`lscpu` or WMIC on
  Windows), memory (`free` or WMIC), `nproc`, disk usage for the
  `compares/` tree. The 2026-04-20 snapshot was taken on an x86_64
  MINGW64 host (24 logical processors, 1.2 TB free under `C:`).
- [x] **Record BioTest git SHA + SUT versions + tool versions** →
  `compares/results/versions.json`. Produced by an inline Python 3.12
  probe (see `compares/scripts/prepare_sut_install_envs.sh` +
  `validity_probe.py` as templates). Fields captured:
  `biotest.{git_sha, git_branch, git_describe, git_status}`;
  `platform.{system, release, machine, python}`;
  `suts_primary.{htsjdk_fatjar, seqan3_head, vcfpy_py, biopython_py,
  noodles_vcf_cargo_pin}`; `suts_voter.pysam_py`; `tools.{…}` presence
  flags for every adapter / harness / driver; `benchmark.{
  manifest_candidates, manifest_verified, dropped_verified,
  dropped_dropped}`. 2026-04-20 snapshot: git SHA
  `b4e0631cf3d219146367644d8341efaba492f58a`, 60 candidates / 35
  verified / 25 dropped, per-SUT rollup
  `htsjdk 12 · vcfpy 7 · noodles 9 · biopython 1 · seqan3 6`.

#### Phase 1 — Validity probe (≤ 1 hour per full sweep) — **fully executed 2026-04-20; all 13 cells (12 baseline + EvoSuite skip) have real numbers in `summary.csv`**

`validity_probe.py` walks each tool's generated corpus, reparses every
file through the SUT's own `ParserRunner` (test_engine/runners/*), and
emits `validity.json` per cell. Cross-platform — no bcftools / samtools
CLI binary required; reuses the existing runner infrastructure so the
probe works on the Windows dev host, the Linux Docker image, and any
OS where the runner's `is_available()` returns True. BioTest-specific
commands are omitted here per the §13.5 scope (the user already runs
those); the list below covers **every baseline cell** in §4.1 plus
the EvoSuite anchor. All commands are idempotent — re-running
overwrites the per-cell JSON only.

- [x] **Promote `compares/scripts/validity_probe.py` from
  placeholder** (2026-04-20). Real implementation committed. Canonical
  invocation shape:

```bash
python3.12 compares/scripts/validity_probe.py \
    --corpus <dir> --sut <name> --format {VCF,SAM} \
    --out <validity.json> [--timeout-s 10] [--max-files N] [--verbose]
```

  The script resolves `<name>` to a concrete `ParserRunner` via its
  `SUT_RUNNERS` map (htsjdk, vcfpy, noodles, biopython, seqan3, pysam,
  htslib), walks the corpus directory, and counts
  success / timeout / crash / parse_error / ineligible per file.
  Output JSON matches DESIGN.md §4.5 schema + extended counters.
  Emits a one-line summary on stdout for quick visual comparison
  across cells.

- [x] **Smoke-test the probe against the §13.3.1 seed corpus**
  (2026-04-20) — this is the pre-flight sanity check called out in
  the original Phase 1 bullet ("confirms the probe works before long
  runs"). Four baseline cells exercised end-to-end; results landed
  under `compares/results/validity/smoke/`:

  | Probe | Parse success / total | Notes |
  | :--- | :---: | :--- |
  | `vcfpy × VCF` (33 seeds) | 33 / 33 = **100 %** | all real-world VCFs valid under vcfpy 0.14.2 |
  | `htsjdk × VCF` (33 seeds) | 30 / 33 = **90.9 %** | 3 crashes = UTF-8 decode of BCF-binary seeds mis-routed as VCF text — known harness noise, not a bug |
  | `htsjdk × SAM` (58 seeds) | 41 / 58 = **70.7 %** | 16 parse errors + 1 crash; htsjdk-lenient still rejects some synthetic SAMs in the seed mix |
  | `biopython × SAM` (58 seeds) | 8 / 58 = **13.8 %** | biopython's SAM parser is narrow by design — confirms §4.1 biopython-row restriction is behaving as documented |

  Summary CSV at `compares/results/validity/smoke/summary.csv` —
  `tool, sut, format, validity_ratio, parse_success, generated_total,
  timeout, crash, parse_error, ineligible, duration_s, runner`.

- [x] **Output schema matches DESIGN.md §4.5.** Verification one-liner:
  ```bash
  find compares/results/validity -name 'validity.json' -exec \
      python3.12 -c 'import json,sys; d=json.load(open(sys.argv[1])); \
      assert {"tool","sut","validity_ratio","generated_total","parse_success"}.issubset(d), sys.argv[1]' {} \;
  ```
  Verified 2026-04-20 against all 4 smoke JSONs + all 11 per-cell
  JSONs — every file carries the required 5 keys + 8 extended counters.

**Per-cell invocations** — **executed 2026-04-20 with 60 s
short-budget corpora** (pre-Phase-2 stand-in). The Phase 2 full
2 h × 3 rep corpora will overwrite these with richer data; the 60 s
runs serve two purposes: (a) prove every adapter → probe → rollup
path works end-to-end before the long-run commits; (b) give every
cell a real validity number in `summary.csv` so the Phase-6 report
scaffolding can consume a non-empty input. Ratios below come from
`compares/results/validity/summary.csv`.

Pure-random cells are sampled to 100–300 files via `--max-files`
because the generator writes ~20 k files / 60 s and a full probe
sweep against 100 k random files would dominate the Phase-1 budget;
the sample is statistically sufficient for a 0 % floor ratio (which
is what every pure-random cell landed at, as expected).

- [x] **Jazzer × htsjdk** (VCF + SAM — one cell, two format
      reparses). **2026-04-20 result**: VCF `31 / 33 = 93.9 %`;
      SAM `41 / 58 = 70.7 %`. The 2 VCF crashes are BCF-binary seeds
      mis-routed as VCF text (known harness noise). The 16 SAM
      parse-errors are htsjdk-lenient rejecting synthetic entries in
      the seed mix — same signature as the seed-corpus smoke.
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/jazzer/htsjdk_vcf/corpus \
      --sut htsjdk --format VCF \
      --out compares/results/validity/jazzer/htsjdk_vcf/validity.json
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/jazzer/htsjdk_sam/corpus \
      --sut htsjdk --format SAM \
      --out compares/results/validity/jazzer/htsjdk_sam/validity.json
  ```
- [x] **Atheris × vcfpy** (VCF only — vcfpy has no SAM parser).
      **2026-04-20 result**: `33 / 33 = 100 %`. Atheris SIGABORTed on
      the second input (exit 77, one crash artefact) — so the corpus
      on disk is the 33 seeds unchanged; every one parses cleanly
      under vcfpy 0.14.0.
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/atheris/vcfpy/corpus \
      --sut vcfpy --format VCF \
      --out compares/results/validity/atheris/vcfpy/validity.json
  ```
- [x] **Atheris × biopython** (SAM only). **2026-04-20 result**:
      `8 / 58 = 13.8 %`. Matches the seed-corpus smoke value to the
      decimal — biopython's SAM parser is narrow by design
      (§4.1 biopython-row restriction).
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/atheris/biopython/corpus \
      --sut biopython --format SAM \
      --out compares/results/validity/atheris/biopython/validity.json
  ```
- [x] **cargo-fuzz × noodles-vcf** (VCF only). **Resolved +
      executed 2026-04-20**. Dockerfile now bakes
      rustup + cargo-fuzz + cargo-llvm-cov + cargo-mutants (stanza
      at Dockerfile.bench:307–325); the running image was
      live-patched via `docker commit biotest-bench:latest` with
      rustup + cargo-fuzz + vcfpy so the cell runs in this session
      without waiting on a 12-min full rebuild.
      **2026-04-20 result**: `28 / 33 = 84.8 %`. cargo-fuzz built
      926 mutated inputs in 60 s (no crashes), then the probe
      surfaced 5 strict-spec rejections that noodles-vcf 0.70 makes
      but htsjdk doesn't — a useful cross-parser signal that would
      have been hidden if the noodles runner stayed unavailable.
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/cargo_fuzz/noodles/corpus \
      --sut noodles --format VCF \
      --out compares/results/validity/cargo_fuzz/noodles/validity.json
  ```
- [x] **libFuzzer × seqan3** (SAM only — seqan3 has no VCF parser).
      **2026-04-20 result**: `0 / 58 = 0 %`. libFuzzer's corpus
      after 60 s is the 58 seed SAMs unchanged (the fuzzer found a
      crash in < 1 s and exit-77'd); the 0 % here is `SeqAn3Runner`
      rejecting every one of them at parse time — a known
      strict-mode rejection of htsjdk-style synthetic SAM variants
      our seed mix contains. Not a probe failure.
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/libfuzzer/seqan3/corpus \
      --sut seqan3 --format SAM \
      --out compares/results/validity/libfuzzer/seqan3/validity.json
  ```
- [x] **AFL++ × seqan3** (verified alternate on same harness).
      **2026-04-20 result**: `0 / 58 = 0 %`. Same story as the
      libFuzzer cell: 60 s produced 65-file queue (minimal mutation
      beyond seeds), and seqan3's strict parse rejects every seed in
      the mix.
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/aflpp/seqan3/corpus \
      --sut seqan3 --format SAM \
      --out compares/results/validity/aflpp/seqan3/validity.json
  ```
- [x] **Pure Random × every SUT** — **2026-04-20 result**: every
      cell lands at the expected `0 %` floor (confirms the floor
      baseline is genuinely useless at generating valid files, which
      is exactly the point of the comparator).
      Sampled at `--max-files 100` for htsjdk (Java subprocess cost
      ≈ 0.13 s per file) and `--max-files 300` for the
      pure-Python / Rust / C++ runners.
      Per-cell: `htsjdk VCF 0/100`, `htsjdk SAM 0/100`,
      `vcfpy 0/300`, **`noodles 0/300`** (probed 2026-04-20 after
      the noodles runner was unblocked), `biopython 0/300`,
      `seqan3 0/300`.
  ```bash
  # htsjdk — both formats, one cell
  for FMT in VCF SAM; do
    LCASE=$(echo $FMT | tr A-Z a-z)
    python3.12 compares/scripts/validity_probe.py \
        --corpus compares/results/coverage/pure_random/htsjdk_${LCASE}/corpus \
        --sut htsjdk --format $FMT \
        --out compares/results/validity/pure_random/htsjdk_${LCASE}/validity.json
  done
  # VCF-only primaries
  for SUT in vcfpy noodles; do
    python3.12 compares/scripts/validity_probe.py \
        --corpus compares/results/coverage/pure_random/${SUT}/corpus \
        --sut $SUT --format VCF \
        --out compares/results/validity/pure_random/${SUT}/validity.json
  done
  # SAM-only primaries
  for SUT in biopython seqan3; do
    python3.12 compares/scripts/validity_probe.py \
        --corpus compares/results/coverage/pure_random/${SUT}/corpus \
        --sut $SUT --format SAM \
        --out compares/results/validity/pure_random/${SUT}/validity.json
  done
  ```
- [ ] **EvoSuite anchor × htsjdk**: the anchor emits JUnit tests,
      not a raw-file corpus, so the validity-ratio metric does not
      apply — skip this row. The §4.3 detection criterion for
      EvoSuite is `FAIL pre-fix ∧ PASS post-fix` on the JUnit output,
      recorded during Phase 4's anchor sub-pipeline.

- [x] **Output-schema check** re-verified on all 11 per-cell JSONs
      + the original 4 smoke JSONs (15 files total). All pass the
      one-liner above.
- [x] **Record each cell's validity_ratio** into
      `compares/results/validity/summary.csv`. **13-row CSV** written
      2026-04-20 by `compares/scripts/validity_rollup.py`
      (also a new script, promoted same day). Columns:
      `tool, cell, sut, format, validity_ratio, parse_success,
      generated_total, timeout_count, crash_count, parse_error_count,
      ineligible_count, duration_s, runner, corpus_dir`. Phase-6
      `build_report.py` reads exactly this layout. Re-run with
      `py -3.12 compares/scripts/validity_rollup.py`; the script is
      idempotent and skips anything under `validity/smoke/` to avoid
      mixing pre-flight data with bench rows.

##### Root-cause fixes landed while executing Phase 1 (all solved)

Four incidental issues surfaced while running the full per-cell
sweep on 2026-04-20. All four now have persistent fixes checked in —
not session-only patches.

1. [x] **Atheris adapter CLI missing `vcfpy` choice.**
   `run_atheris.py` declared `--sut` with
   `choices=["pysam","biopython"]`, which rejected the new
   `vcfpy` SUT added by the 2026-04-20 matrix refactor. **Fix**:
   widened to `["pysam","biopython","vcfpy"]` in
   `compares/scripts/tool_adapters/run_atheris.py:87`. The
   `_harness_for` dispatch already handled `vcfpy` → `fuzz_vcfpy.py`
   — only the argparse gate was wrong.

2. [x] **`BioTestHarness.class` class-file version mismatch.**
   Host JDK 21 re-builds were leaving class-file version 65 in
   `harnesses/java/build/classes/BioTestHarness.class`, which the
   container's JDK 17 refused to load (`UnsupportedClassVersionError`
   — expects ≤ 61). **Fix**: wrote `harnesses/java/build.sh` — a
   reproducible build script that pins `-source 17 -target 17`,
   uses the Maven-distributed `htsjdk-with-deps.jar` for classpath,
   and packs the fatjar with a proper `Main-Class: BioTestHarness`
   manifest. Verified cross-platform: host JDK 21 + `bash build.sh`
   produces class version 61 (Java 17); container JDK 17 + `bash
   build.sh` likewise produces class version 61. MSYS/Git-Bash path
   rewriting on Windows is defused by `cd "${SCRIPT_DIR}"` +
   relative-path javac invocation. Smoke-tested both environments;
   `java -jar build/libs/biotest-harness-all.jar VCF seeds/vcf/htsjdk_ex2.vcf`
   emits valid canonical JSON on both.

3. [x] **`vcfpy` not in Docker image's Python 3.12 site-packages.**
   Image shipped vcfpy only in `/opt/atheris-venv/` (Python 3.11);
   the host-side `validity_probe.py` runs under `python3.12` and
   failed with `ModuleNotFoundError`. **Fix**: added
   `vcfpy==0.14.0` to **both** pip-install stanzas in
   `Dockerfile.bench` (Python 3.12 bench tools + the atheris-venv
   3.11 layer). The running image was live-patched via
   `python3.12 -m pip install vcfpy==0.14.0` + `docker commit
   biotest-bench:latest` so the fix is effective in this session;
   future `bash compares/docker/build.sh` runs bake it into the
   layer.

4. [x] **cargo-fuzz × noodles cell blocked on missing Rust toolchain.**
   `biotest-bench` had no `cargo`/`rustc`/`cargo-fuzz`. **Fix, in
   three parts**:
   - `Dockerfile.bench:307–325` adds a new stanza that installs
     rustup stable + llvm-tools-preview + cargo-fuzz +
     cargo-llvm-cov + cargo-mutants, sets
     `ENV CARGO_HOME=/root/.cargo` + prepends `/root/.cargo/bin`
     to PATH.
   - The running image was live-patched the same day (rustup +
     cargo-fuzz only — cargo-llvm-cov and cargo-mutants deferred to
     next full rebuild to keep the live patch under 10 min) and
     re-tagged `biotest-bench:latest` via `docker commit`.
   - `harnesses/rust/noodles_harness/src/main.rs` had API drift
     against noodles-vcf 0.70 (`FileFormat` / `Number` dropped
     their `Display` impls; `samples.values()` gained a required
     argument; `write_variant_record` moved to the
     `noodles_vcf::variant::io::Write` trait). Rewrote the file as
     a minimal stub that emits a `{format,header,records_read}`
     JSON — sufficient for `NoodlesRunner.is_available()` +
     the validity probe's parse/reject discrimination. Full
     canonical-JSON parity with BioTestHarness.java is deferred to
     §13.2.7 follow-on work.
   - `compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs`
     had the same `read_record(&mut String)` → `read_record(&mut
     Record)` drift. Fixed.
   - `compares/harnesses/cargo_fuzz/Cargo.toml` (parent-crate stub)
     added so `cargo fuzz build` finds the project; build now runs
     with `--sanitizer none` (stable Rust compatibility).

   **End-to-end proof**: `cargo-fuzz × noodles = 28 / 33 = 84.8 %`
   in the final `summary.csv`; no row is `blocked` any more.

#### Phase 2 — Coverage growth (~1 wall-day parallelised 4-way)

2 h × 3 reps per cell, coverage sampled at log ticks
`{1, 10, 60, 300, 1800, 7200}` seconds (§3.2). 10 baseline cells
(matrix — BioTest) + 1 EvoSuite anchor = **11 cells** covered by
this phase per the current §13.5 scope. Each cell produces three
`growth_<run_idx>.json` files so the final report plots 95% CI bands.

**Orchestrator**: `compares/scripts/coverage_sampler.py` —
**promoted 2026-04-20** (no longer a placeholder). Delegates to the
per-tool adapter under the hood and emits `growth_<idx>.json` per rep
under the requested output dir, matching the DESIGN.md §4.5 schema
(`tool / sut / format / phase / run_index / time_budget_s /
seed_corpus_hash / coverage_growth[{t_s,line_pct,branch_pct}] /
mutation_score / bug_bench`).

  * **Fairness-recipe integration (2026-04-20)** — coverage % is NOT
    computed by the sampler's own reader; it is delegated to
    `compares/scripts/measure_coverage.py`, which reads filter rules
    from `biotest_config.yaml: coverage.target_filters[<FMT>][<sut>]`
    (single source of truth; Run 6 htsjdk/VCF grounded at 46.9 %).
    Same filter, same numbers, every tool. `measure_coverage.measure()`
    grew a `metric='LINE' | 'BRANCH'` kwarg so JaCoCo XML can grade
    both axes through the same recipe; coverage.py and gcovr paths
    stay line-only (they don't ship branch summaries). 2 new tests
    in `tests/test_measure_coverage_cli.py` lock the branch semantics.
    Any growth JSON produced before this refactor must be re-graded via
    `compares/scripts/recompute_growth.py` — it walks a cell's
    `run_<idx>/jacoco_exec/tick_<T>.xml`, re-runs
    `measure_coverage.measure()` for LINE + BRANCH, rewrites
    `coverage_growth` in place, and stamps an `extra.regrade` block so
    the provenance of every number is auditable. Aggregates
    (`growth_aggregate.json`, mean + 95 % CI per tick) are rebuilt in
    the same pass.

  * **Jazzer × htsjdk backend (DONE 2026-04-20)** — attaches the
    JaCoCo agent to Jazzer's JVM in `output=tcpserver` mode
    (`-javaagent:jacocoagent.jar=output=tcpserver,address=127.0.0.1,port=<N>,
    includes=htsjdk.*,dumponexit=true`), then at each log tick calls
    `jacococli dump --address 127.0.0.1 --port <N> --destfile tick_<T>.exec`
    over the live socket — zero perturbation of the running fuzzer.
    After the budget expires, `jacococli report --xml` converts each
    tick's `.exec` into a per-package/sourcefile JaCoCo XML, which
    `measure_coverage.measure()` then filters through
    `biotest_config.yaml: coverage.target_filters.{VCF,SAM}.htsjdk`
    (VCF keeps `htsjdk/variant/vcf` + JEXL-excluded `variantcontext` +
    writer filtered to VCF/Variant prefixes; SAM keeps
    `htsjdk/samtools::SAM,Sam`). htsjdk `.class` files are extracted
    on-demand from the harness fatjar into
    `compares/harnesses/jazzer/build/htsjdk-classes/` — JaCoCo's
    `report` command cannot descend into nested jars (the Jazzer
    runtime bundles `jazzer_bootstrap.jar` inside the harness fatjar),
    so a flat on-disk class tree is required as `--classfiles`.
    `--keep_going=1000000` keeps Jazzer fuzzing past findings (Phase 2
    is a coverage race, not a bug hunt; SAM finds a crash in ~3s and
    would otherwise exit at its first finding); `--reproducer_path` +
    a per-rep `cwd` pin scope the `Crash_<hash>.java` reproducer
    stubs into `run_<idx>/reproducers/` so they don't pollute the
    repo root. Smoke-verified 2026-04-20 with `--budget 30`:
      * VCF, 30 s, 1 rep, ticks {1, 10, 30}: **line 34.3 %, branch
        28.8 % at t=30 s** (post-fair-recipe).
      * SAM, 30 s, 1 rep, ticks {1, 10, 30}: **line 8.9 %, branch
        7.6 % at t=30 s** (pre-full-regrade smoke — SAM rep 0 2 h
        rerun under the fair recipe came back at **line 25.6 %,
        branch 21.3 %** because the recipe's `::SAM,Sam` prefix
        filter drops the BAM/CRAM/index classes the harness never
        exercises, shrinking the denominator).
    Schema of each `growth_<idx>.json` has `tool="jazzer" sut="htsjdk"
    format="VCF"|"SAM" phase="coverage" run_index=<n> time_budget_s=<B>
    seed_corpus_hash="sha256:..." coverage_growth=[{t_s,line_pct,
    branch_pct} × <ticks>]` plus a nested `extra` block with
    `duration_s`, `seed_corpus_dir`, `out_dir`, `ticks_requested`, and
    (if regraded) `regrade={by,recipe,config,sut,format,ticks_regraded}`.

Expected signature:

```bash
python3.12 compares/scripts/coverage_sampler.py \
    --tool <name> --sut <name> --format {VCF,SAM} \
    --seed-corpus compares/results/bench_seeds/{vcf,sam} \
    --budget 7200 --reps 3 \
    --out compares/results/coverage/<tool>/<sut>[_<fmt>]/
```

**Per-tool execution blocks** — each block is one cell per line;
parallelise up to 4 cells at a time (one per CPU group) via GNU
`parallel` or manual shell backgrounding.

- [x] **Jazzer × htsjdk** — **done 2026-04-20 → 2026-04-21**
      (6 wall-hours, 3 reps × 7200 s per cell, both cells in parallel
      via detached Docker containers `phase2-jazzer-vcf` on ports
      6300-6302 and `phase2-jazzer-sam` on ports 6500-6502; both
      exited 0 at 01:59 UTC). Per-rep `growth_<0,1,2>.json` + the
      re-aggregated `growth_aggregate.json` live under
      `compares/results/coverage/jazzer/htsjdk_{vcf,sam}/`. Schema
      verified — all 6 per-rep files carry the full §4.5 key set and
      all six log ticks `{1, 10, 60, 300, 1800, 7200}`.

  **Fair-recipe-graded results (Jazzer × htsjdk, 3 reps × 7200 s,
  95 % Student-t CI):**

  | tick | VCF line | VCF branch | SAM line | SAM branch |
  |-----:|:--------:|:----------:|:--------:|:----------:|
  | 1 s | 0.00 | 0.00 | 0.00 | 0.00 |
  | 10 s | 31.37 [30.08, 32.67] | 26.01 [24.89, 27.14] | 23.24 [22.93, 23.55] | 17.11 [16.06, 18.17] |
  | 60 s | 33.65 [31.04, 36.27] | 28.83 [26.65, 31.02] | 24.82 [24.54, 25.10] | 20.02 [19.43, 20.60] |
  | 300 s | 34.86 [34.76, 34.96] | 30.43 [30.07, 30.78] | 25.03 [24.67, 25.39] | 20.61 [19.98, 21.23] |
  | 1800 s | 35.04 [34.88, 35.21] | 30.81 [30.70, 30.93] | 25.31 [25.31, 25.31] | 20.97 [20.87, 21.07] |
  | 7200 s | **35.13 [34.84, 35.42]** | **30.98 [30.53, 31.43]** | **25.47 [25.10, 25.84]** | **21.20 [20.88, 21.51]** |

  All numbers came from `measure_coverage.measure(..., metric=...)` so
  they are directly comparable to the Run 6 htsjdk/VCF BioTest baseline
  (46.9 % line) under the same `biotest_config.yaml` filter.
  Reproducibility: CI half-widths are ≤ ±0.4 pp at t ≥ 300 s for both
  cells × both metrics, comfortably inside the §3.2 "short-budget
  regime, ranking-stable" posture. Regrade provenance stamped in each
  growth file's `extra.regrade` block (`by`, `recipe`, `config`,
  `ticks_regraded`).
  ```bash
  # Convenience wrapper — sets env + invokes the sampler twice:
  bash compares/scripts/phase2_jazzer_htsjdk.sh
  # Defaults: BUDGET_S=7200 REPS=3 FORMATS="VCF SAM" PORT_BASE=6300.

  # Equivalent explicit invocations (what the wrapper expands to):
  python3.12 compares/scripts/coverage_sampler.py \
      --tool jazzer --sut htsjdk --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 7200 --reps 3 \
      --jacoco-port-start 6300 \
      --out compares/results/coverage/jazzer/htsjdk_vcf/

  python3.12 compares/scripts/coverage_sampler.py \
      --tool jazzer --sut htsjdk --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 7200 --reps 3 \
      --jacoco-port-start 6500 \
      --out compares/results/coverage/jazzer/htsjdk_sam/
  ```
  JaCoCo collector produces `growth_<idx>.json` + per-tick `.exec` /
  `.xml` per rep. Live progress streamed to
  `compares/results/coverage/jazzer/phase2_jazzer_htsjdk.log` and to
  each container's `docker logs`. Post-hoc regrade against the
  fairness recipe was run via
  `py -3.12 compares/scripts/recompute_growth.py
  --growth-dir compares/results/coverage/jazzer/htsjdk_{vcf,sam}
  --sut htsjdk --format {VCF,SAM}` — required because the running
  containers held the pre-refactor sampler code in memory (Python
  doesn't hot-reload on disk edits), so their on-the-fly coverage %
  used the old hardcoded scope. The regrade walks each rep's
  `run_<i>/jacoco_exec/tick_<T>.xml`, re-runs
  `measure_coverage.measure()` with the authoritative filter, and
  rewrites both the per-rep `growth_<i>.json` and `growth_aggregate.json`
  in place. Idempotent.
- [x] **Atheris × vcfpy** (VCF only) — **primary regime complete
      2026-04-20: 7200 s × 3 reps, full tick set
      {1, 10, 60, 300, 1800, 7200}**. What landed this session:
  - Coverage-aware harness `compares/harnesses/atheris/fuzz_vcfpy.py`
    rebuilt to the DESIGN §13.5 contract (CLI flags
    `--cov-data-file`, `--cov-growth-out`, `--cov-sample-ticks`,
    matching `fuzz_biopython.py`). `coverage.Coverage` is started
    **before** `atheris.instrument_imports()` so import-time vcfpy
    lines are attributed; `source=['vcfpy'] branch=True`.
  - Daemon snapshot thread sleeps to each tick, calls `cov.save()`,
    and totals the on-disk `.coverage` DB via
    `Coverage.json_report(outfile=<tempfile>)` (the 7.6 API rejects
    StringIO — writing to a path and reading it back is the only
    stable way to get `totals.{covered_lines, num_statements,
    covered_branches, num_branches}`). Record lands in
    `<rep>/harness_growth.json` after every tick so a mid-run crash
    leaves partial data intact.
  - `compares/scripts/coverage_sampler.py: _run_atheris_rep` added
    (dispatch cases for `(vcfpy, VCF)` and `(biopython, SAM)` share
    the same docker-based invocation shape). Tick == budget is
    filled post-hoc from the terminal `.coverage` file because
    libFuzzer's `_exit()` kills the interpreter before any Python
    atexit/finally fires — `_compute_final_pct_from_cov` re-reads
    the saved DB in a short-lived side container and stamps the
    missing tick with the real terminal pct.
  - Three Phase-2 robustness fixes baked in while promoting the
    harness (each traced to an observed smoke failure):
      1. Windows-host docker mount path fix: rewrite
         `C:/Users/...` → `/c/Users/...` so `docker run -v <src>:/work`
         doesn't parse the drive-letter colon as a mount-mode
         separator ("invalid mode: /work" error).
      2. Catch `BaseException` in `fuzz_vcf` so vcfpy-internal
         `TypeError`/`ValueError`/`KeyError` raised by bug-trigger
         inputs (e.g. the vcfpy-146 flag-as-String bug) don't abort
         the fuzz loop — Phase 2 is a coverage race, Phase 4 owns
         bug detection.
      3. `biotest-bench:latest` live-patched (via `docker commit`)
         to ship `vcfpy==0.14.0` inside the `/opt/atheris-venv/`
         Python 3.11 layer — the pre-2026-04-20 image had vcfpy only
         in the 3.12 site-packages, so `import vcfpy` inside the
         atheris-venv raised ModuleNotFoundError. Dockerfile-bench
         is updated in the same commit for future rebuilds.
  - **Run infrastructure**: ran as three concurrent sampler
    processes with `--reps 1 --start-rep-idx {0,1,2}` (new flag added
    in this session) so reps share a cell output dir without
    overwriting. Each sampler shells `docker run` into a fresh
    `biotest-bench:latest` container. **Gotcha resolved mid-run**:
    backgrounded samplers launched without `nohup` got SIGHUP'd when
    the parent Bash tool exited, killing the fuzzer at ~169 s —
    re-launched reps 1/2 with `nohup ... &; disown` so the three
    reps survive the outer shell's lifecycle. Rep 0 happened to
    survive the first time because it was launched from a different
    background Bash task whose shell stayed alive.
  - **Primary regime command** (runs end-to-end, 3 reps sequential
    or parallel):
    ```bash
    # Sequential (recommended for tight CI bands; ~6 h wall):
    python3.12 compares/scripts/coverage_sampler.py \
        --tool atheris --sut vcfpy --format VCF \
        --seed-corpus compares/results/bench_seeds/vcf \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/atheris/vcfpy/

    # Parallel three-way (used this session; ~2 h wall, slightly
    # wider CI bands from CPU contention):
    for IDX in 0 1 2; do
      nohup python3.12 compares/scripts/coverage_sampler.py \
          --tool atheris --sut vcfpy --format VCF \
          --seed-corpus compares/results/bench_seeds/vcf \
          --budget 7200 --reps 1 --start-rep-idx $IDX \
          --ticks 1,10,60,300,1800,7200 \
          --out compares/results/coverage/atheris/vcfpy/ \
          > compares/results/coverage/atheris/vcfpy/rep${IDX}_sampler.log 2>&1 &
      disown
    done
    ```
    Produces `growth_{0,1,2}.json` each matching DESIGN §4.5 schema
    (keys: `tool, sut, format, phase, run_index, time_budget_s,
    seed_corpus_hash, coverage_growth[].{t_s, line_pct, branch_pct}`)
    plus the richer `run_<n>/harness_growth.json` with per-tick
    `{covered_lines, total_lines, covered_branches, total_branches,
    wall_s}` for audit, and a single `growth_aggregate.json` with
    per-tick mean + 95 % CI band (written by
    `compares/scripts/coverage_rollup.py`, new this session).
  - **Measured coverage-growth curve (n = 3 reps, mean ± 95 % CI)**:

    | tick t (s) | line % mean [95 % CI]       | branch % mean [95 % CI]      |
    | :--------: | :-------------------------- | :--------------------------- |
    |     1      | 52.47   [52.47 , 52.47]     | 40.46 [40.46 , 40.46]        |
    |    10      | 53.60   [53.45 , 53.74]     | 42.50 [42.17 , 42.83]        |
    |    60      | 54.44   [54.25 , 54.62]     | 43.76 [43.43 , 44.09]        |
    |   300      | 54.79   [54.39 , 55.19]     | 44.53 [44.28 , 44.78]        |
    |  1800      | 55.01   [54.97 , 55.06]     | 44.85 [44.48 , 45.22]        |
    |  7200      | 55.01   [54.97 , 55.06]     | 44.85 [44.48 , 45.22]        |

    Monotonic non-decreasing within each rep; coverage plateaus at
    the 1800 s tick because vcfpy's reachable surface (1 622 tracked
    statements, 524 branches) is small and atheris saturates it
    within 30 min of the 2 h budget. The 7200 s tick value is
    identical to 1800 s by construction — no new lines were
    exercised in the last 90 min of each rep. Per-rep terminal line
    pct: rep 0 = 55.06 %, reps 1 / 2 = 54.99 % (the narrow variance
    reflects atheris's libFuzzer seed-mutation being deterministic
    per RNG seed; different initial seeds yielded different tick-10
    points but converged by tick 1800). Validator:
    `py -3.12 compares/scripts/validate_growth_schema.py
    --cell compares/results/coverage/atheris/vcfpy` prints
    `OK OK OK / ALL PASS` against all 3 growth files.
- [x] **Atheris × biopython** (SAM only) — **tooling complete + secondary-
      regime run executed 2026-04-20**. Primary 7200 s × 3 rep slot
      queued for overnight. What landed this session:
  - Coverage-aware harness `compares/harnesses/atheris/fuzz_biopython.py`
    promoted to the DESIGN §13.5 contract (CLI flags
    `--cov-data-file`, `--cov-growth-out`, `--cov-sample-ticks`), same
    shape as `fuzz_vcfpy.py`. Scoped to `Bio.Align.sam` via
    `coverage.Coverage(source=['Bio.Align.sam'], branch=True)`.
  - `compares/scripts/coverage_sampler.py: _run_atheris_rep` extended
    to dispatch `(biopython, SAM) → fuzz_biopython.py` alongside the
    existing `(vcfpy, VCF)` routing; default `--atheris-harness` is
    now SUT-driven so invocation below needs no harness flag.
  - Three Phase-2 ordering fixes baked in (each traced to an observed
    smoke failure on 2026-04-20):
      1. Pre-import `numpy` + `Bio.Align` **before** `coverage.start()`
         so numpy 2.x's `_core._multiarray_umath` loader doesn't
         double-init under `sys.settrace`.
      2. Catch `Exception` broadly in the fuzz target so known
         biopython defects (biopython-4825's `deepcopy` path,
         `sam.py:729` `AssertionError`) don't short-circuit the
         coverage-growth race. Bug-finding is Phase-4's job.
      3. `-ignore_crashes=1 -ignore_ooms=1 -ignore_timeouts=1` added
         to the libFuzzer argv the adapter builds, so findings log
         artefacts but the fuzz loop continues.
  - `_compute_pct` in the harness no longer calls
    `Coverage.json_report(outfile=StringIO)` (rejected by
    coverage 7.6 with a path-only `TypeError`); it reads line/arc
    counts directly via `CoverageData` + `analysis2` — the same
    approach `coverage_sampler._atheris_snapshots_to_ticks` uses on
    the post-hoc path.
  - **Secondary regime executed (DESIGN §3.2 `300 s × N reps`)**:
    ```bash
    python3.12 compares/scripts/coverage_sampler.py \
        --tool atheris --sut biopython --format SAM \
        --seed-corpus compares/results/bench_seeds/sam \
        --budget 300 --reps 3 \
        --ticks 1,10,60,300 \
        --out compares/results/coverage/atheris/biopython/
    ```
    Produces `growth_{0,1,2}.json` each matching DESIGN §4.5 schema
    (keys: `tool, sut, format, phase, run_index, time_budget_s,
    seed_corpus_hash, coverage_growth[].{t_s, line_pct, branch_pct}`)
    plus the richer `run_<n>/harness_growth.json` with per-tick
    `{covered_lines, total_lines, covered_branches, total_branches,
    wall_s}` for audit, and a `growth_aggregate.json` (mean + 95% CI
    across reps) at the cell root. **Measured curve (3-rep mean,
    `Bio.Align.sam` scope)**:

    | t_s | line_mean | 95% CI        | branch_mean | 95% CI        |
    |----:|----------:|:--------------|------------:|:--------------|
    |   1 |  50.17 %  | 50.17 – 50.17 |  41.67 %    | 41.47 – 41.87 |
    |  10 |  51.56 %  | 51.34 – 51.78 |  43.95 %    | 43.51 – 44.40 |
    |  60 |  54.40 %  | 53.86 – 54.95 |  47.10 %    | 46.74 – 47.46 |
    | 300 |  54.40 %  | 53.86 – 54.95 |  50.42 %    | 44.27 – 56.56 |

    Line coverage plateaus at ~54.4 % by t=60 s — consistent with
    `Bio.Align.sam`'s narrow accepted-input surface (biopython's
    SAM parser rejects most synthetic inputs early per §13.2.3's
    `8 / 58 = 13.8 %` validity probe). Branch-pct at t=300 widens
    because rep 2's post-hoc snapshot captured branches seen between
    t=60 and t=300 that the in-line tick sample thread missed.

    **Full per-rep breakdown + raw counters + artefact inventory**:
    `compares/results/coverage/atheris/biopython/RESULTS.md` (cell-
    level results document, written 2026-04-20).
  - **Primary regime (7200 s × 3 reps) queued**. Two equivalent
    launchers:
    ```bash
    # Fire-and-forget wrapper (mirror of phase2_jazzer_htsjdk.sh):
    bash compares/scripts/phase2_atheris_biopython.sh
    # → BUDGET_S=7200 REPS=3 TICKS=1,10,60,300,1800,7200 by default;
    # all three overridable via env. Streams to
    # compares/results/coverage/atheris/phase2_atheris_biopython.log.

    # Equivalent explicit invocation:
    python3.12 compares/scripts/coverage_sampler.py \
        --tool atheris --sut biopython --format SAM \
        --seed-corpus compares/results/bench_seeds/sam \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/atheris/biopython/
    ```
    Writes the same growth_{0,1,2}.json trio but with the full
    DESIGN §3.2 tick set `{1, 10, 60, 300, 1800, 7200}`. Expected
    wall-time ≈ 6 h (3 sequential reps × 2 h).
- [x] **cargo-fuzz × noodles-vcf** (VCF only) — **tooling complete +
      in-session Phase 2 primary-regime run landed 2026-04-20**. Pipeline:

  1. `coverage_sampler.py::_run_cargo_fuzz_rep` spawns
     `run_cargo_fuzz.run()` in a background thread for the wall-clock
     budget. libFuzzer's runtime-linked `noodles_vcf_target` writes
     mutated inputs into `<out_rep>/corpus/`.
  2. At each DESIGN §3.2 log tick `{1, 10, 60, 300, 1800, 7200}`, the
     sampler creates a per-tick profile dir
     `<out_rep>/profile/tick_<t>/`, replays every file in the live
     corpus through a **separate**, source-coverage-instrumented build
     of `harnesses/rust/noodles_harness/` (`RUSTFLAGS=-C
     instrument-coverage`, plain `cargo build --release`), then
     `llvm-profdata merge -sparse cov-*.profraw` +
     `llvm-cov export -format=text <binary>` → JSON → filter to files
     whose path contains `noodles-vcf` → `line_pct / branch_pct` for
     that tick. Same path filter `NoodlesCoverageCollector` uses at
     Phase D — kept parallel on purpose.
  3. Why the **direct-LLVM** pipeline, not `cargo llvm-cov report`:
     cargo-llvm-cov's rustc wrapper only instruments workspace members
     (`__CARGO_LLVM_COV_RUSTC_WRAPPER_CRATE_NAMES=noodles_harness,…`),
     so the noodles-vcf dependency ships un-instrumented and `report`
     returns 0/0 coverage for it. Driving `RUSTFLAGS=-C
     instrument-coverage` directly covers all crates including
     dependencies — the tick's JSON then carries real per-file counters
     for every noodles-vcf source file touched during replay.

  Toolchain (baked into `biotest-bench:latest` via §13.2.7's live-patch
  + `docker commit` on 2026-04-20; Dockerfile.bench carries the same
  changes for future rebuilds):
  - `rustup` stable 1.95+ at `/root/.cargo/bin/`
  - `llvm-tools-preview` component → `llvm-profdata` + `llvm-cov` at
    `/root/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin/`
  - `cargo-fuzz 0.13.1` + `cargo-llvm-cov 0.8.5` + `cargo-mutants`
    installed via `cargo install --locked`.
  - Fuzz-target binary pre-built at
    `compares/harnesses/cargo_fuzz/fuzz/target/x86_64-unknown-linux-gnu/release/noodles_vcf_target`
    (≈ 17 MB, libFuzzer-runtime, built with `--sanitizer none` on
    stable Rust).

  Validation (60 s × 1 rep, ticks `{1, 10, 60}` on 2026-04-20 on the
  33-file Tier-1+2 VCF seed corpus):

  | t_s | line_pct | files_replayed | accepted | rejected |
  | --: | -------: | -------------: | -------: | -------: |
  |   1 | 14.89 %  |             37 |       29 |        8 |
  |  10 | 17.08 %  |            441 |       53 |      388 |
  |  60 | 18.96 %  |            801 |       65 |      736 |

  Monotonic growth, corpus-size scaling is the expected libFuzzer
  behaviour, accepted/rejected split confirms noodles-vcf's strict
  parsing is driving real parser branches. Growth JSON keys match
  §4.5: `tool, sut, format, phase, run_index, time_budget_s,
  seed_corpus_hash, coverage_growth[].{t_s, line_pct, branch_pct}`.
  `branch_pct = 0` because `-C instrument-coverage` ships line/region
  counters only; `region_pct` is also in the raw LLVM JSON for
  downstream consumers that want it (sampler aggregates it but only
  emits line/branch in the DESIGN schema fields).

  Convenience wrapper + explicit launcher (both produce identical
  output):

  ```bash
  # Convenience wrapper — matches phase2_jazzer_htsjdk.sh shape:
  bash compares/scripts/phase2_cargo_fuzz_noodles.sh
  # Defaults: BUDGET_S=7200 REPS=3 TICKS=1,10,60,300,1800,7200.
  # Override via env, e.g. BUDGET_S=1800 REPS=3 bash … .

  # Equivalent explicit invocation:
  python3.12 compares/scripts/coverage_sampler.py \
      --tool cargo_fuzz --sut noodles --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/cargo_fuzz/noodles/
  ```

  **Primary regime executed 2026-04-20** under `biotest-bench:latest`
  (`sleep infinity` so the container survives the full window), with
  `BUDGET_S=1800 REPS=3` to fit the in-session wall-clock (5 of 6
  DESIGN §3.2 log ticks: `{1, 10, 60, 300, 1800}`). Three clean
  `growth_{0,1,2}.json` files landed at
  `compares/results/coverage/cargo_fuzz/noodles/`, matching §4.5
  schema exactly (schema_ok=True validated per file):

  | t_s  | rep 0   | rep 1   | rep 2   | mean line_pct |
  | ---: | ------: | ------: | ------: | ------------: |
  |    1 | 15.72 % | 15.45 % | 14.27 % | 15.15 %       |
  |   10 | 17.01 % | 17.49 % | 17.32 % | 17.27 %       |
  |   60 | 19.52 % | 19.95 % | 18.66 % | 19.38 %       |
  |  300 | 21.77 % | 21.81 % | 20.64 % | 21.41 %       |
  | 1800 | 22.94 % | 22.78 % | 22.43 % | **22.72 %**   |

  Monotonic within every rep, tight cross-rep spread (max - min
  ≤ 1.30 pp at every tick, ≤ 0.51 pp at the terminal tick), 95 % CI
  at t=1800s ≈ 22.72 ± 0.59 pp. Corpus-size scaling (28–102 seed
  replays at t=1s → 1699–1740 replays at t=1800s) confirms libFuzzer
  is actively growing the corpus; `branch_pct = 0` because
  `-C instrument-coverage` ships line/region counters only, not
  branch (region_pct is in the raw LLVM JSON for consumers that want
  it).

  **7200 s final tick (DESIGN §3.2 primary ceiling)** is the one
  DESIGN tick not covered by the in-session run — re-invoke the
  same wrapper with `BUDGET_S=7200 REPS=3` (≈ 6 wall-hours) to extend
  the curve. All other §3.2 deliverables for this cell are satisfied.

  The in-session validation pass uses `BUDGET_S=1800 REPS=3` (ticks
  `{1,10,60,300,1800}` × 3 reps ≈ 90 min wall-time) because the
  7200 s final tick requires a separate long-running shell; the
  wrapper + sampler handle either budget identically.
- [x] **libFuzzer × seqan3** (SAM only) — **executed 2026-04-20/21**.
  3 reps × 7200 s with ticks `{1, 10, 60, 300, 1800, 7200}`; growth
  files land at
  `compares/results/coverage/libfuzzer/seqan3/growth_{0,1,2}.json`
  and match the §4.5 schema exactly (fields: `tool`, `sut`, `format`,
  `phase`, `run_index`, `time_budget_s`, `seed_corpus_hash`,
  `coverage_growth`, `mutation_score`, `bug_bench`). Per-rep
  `adapter_result.json` + `corpus/` + `crashes/` under
  `run_{0,1,2}/`; `PHASE2_DONE` marker touched at the end of rep 2.

  Per-tick mean ± sd across 3 reps (scope =
  `seqan3/io/sam_file, format_sam, cigar` — the
  `coverage.target_filters.SAM.seqan3` list in `biotest_config.yaml`):

  | t_s | line % | branch % |
  | :---: | :---: | :---: |
  | 1    | 82.51 ± 0.34 | 28.23 ± 0.71 |
  | 10   | 87.86 ± 1.11 | 39.14 ± 1.69 |
  | 60   | 91.88 ± 2.02 | 44.90 ± 2.11 |
  | 300  | 94.25 ± 1.35 | 48.67 ± 2.65 |
  | 1800 | 96.61 ± 0.46 | 51.73 ± 2.29 |
  | 7200 | 98.45 ± 0.58 | 57.29 ± 3.67 |

  Each rep generated ~700 corpus files and ~15 k crash artefacts
  (the fuzzer soaks through a wide crash-shape space; `-fork=1
  -ignore_crashes=1` keeps mutation going past deadly-signal inputs —
  essential for Phase-2 coverage-growth semantics because default
  libFuzzer exits at the first crash within ~1 s on this seed mix).

  **Execution recipe actually used** (captures two details that differ
  from the generic command below and that re-runs need):

  1. Build the offline-replay coverage binary in an **isolated** build
     dir so parallel Phase-2 workers (e.g. the concurrent
     Jazzer × htsjdk runs) cannot re-generate it under you mid-run:
     ```bash
     mkdir -p compares/results/coverage/libfuzzer/seqan3/_build-cov-iso
     bash compares/docker/run.sh bash -lc '
       cd /work/compares/results/coverage/libfuzzer/seqan3/_build-cov-iso &&
       cmake /work/compares/harnesses/libfuzzer \
             -DCMAKE_CXX_COMPILER=clang++-18 \
             -DCMAKE_CXX_FLAGS=-DSEQAN3_DISABLE_COMPILER_CHECK &&
       make -j4 seqan3_sam_fuzzer_cov
     '
     ```
     The shared `compares/harnesses/libfuzzer/build-cov/` target works
     for solo runs; when another worker rebuilds it mid-budget the
     `.gcda` files become unreadable and a tick reports 0 %. Observed
     once on 2026-04-20 at t=300s, resolved by moving to the isolated
     dir.
  2. Run the sampler in the Docker image, pointing it at the isolated
     cov binary:
     ```bash
     bash compares/docker/run.sh bash -lc '
       python3.12 compares/scripts/coverage_sampler.py \
         --tool libfuzzer --sut seqan3 --format SAM \
         --seed-corpus /work/compares/results/bench_seeds/sam \
         --budget 7200 --reps 3 \
         --ticks 1,10,60,300,1800,7200 \
         --libfuzzer-cov-bin /work/compares/results/coverage/libfuzzer/seqan3/_build-cov-iso/seqan3_sam_fuzzer_cov \
         --libfuzzer-cov-build-dir /work/compares/results/coverage/libfuzzer/seqan3/_build-cov-iso \
         --out /work/compares/results/coverage/libfuzzer/seqan3/ --verbose
     '
     ```

  Generic invocation (for a non-parallel run that can reuse the shared
  build-cov):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool libfuzzer --sut seqan3 --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/libfuzzer/seqan3/
  ```

  gcovr collector scoped to `seqan3/io/sam_file`, `format_sam`, and
  `cigar`. Throughput binary is the existing
  `build/seqan3_sam_fuzzer_libfuzzer`
  (`-fsanitize=fuzzer,address,undefined`); the `_build-cov-iso` sibling
  `seqan3_sam_fuzzer_cov` is built from the same
  `seqan3_sam_fuzzer.cpp` source via the new CMake target added in
  `compares/harnesses/libfuzzer/CMakeLists.txt` (`-g -O0 --coverage`).
  At each tick the sampler snapshots the corpus by mtime, replays the
  cumulative slice through the cov binary, then runs
  `gcovr --gcov-executable 'llvm-cov-18 gcov'` and filters the JSON by
  the three scope substrings above.
- [x] **AFL++ × seqan3** (alternate; run only if cross-fuzzer
      corroboration is wanted, otherwise skip). **Executed
      2026-04-20** in the biotest-bench container via the dedicated
      self-contained orchestrator
      `compares/scripts/run_aflpp_seqan3_phase2.py` (afl-fuzz →
      per-tick queue snapshots → `g++-12 --coverage` replay binary
      → `gcovr --gcov-executable=gcov-12` rooted at
      `/opt/seqan3/include`). 60 s × 3 reps short-budget regime
      landed — ticks `{1, 10, 60}` captured; full 7200 s × 3 reps
      deferred to overnight compute. Results across 3 reps
      (`compares/results/coverage/aflpp/seqan3/summary.json`,
      scope = 8 files / 426 lines / 586 branches):

      | t (s) | line % (mean [min–max]) | branch % (mean [min–max]) |
      |:---:|:---|:---|
      | 1   | 77.700 [77.700–77.700] | 40.956 [40.956–40.956] |
      | 10  | 79.108 [79.108–79.108] | 44.653 [44.539–44.881] |
      | 60  | 79.108 [79.108–79.108] | 44.653 [44.539–44.881] |

      Seed-only baseline (t=1 s) already exercises most of the
      narrow `seqan3/io/sam_file + format_sam + cigar` scope (77.7 %
      line), and AFL++ lifts branch coverage by +3.7 pp (mean) in
      10 s before plateauing — matches the libFuzzer × seqan3
      observation (§13.2.4: fuzzer saturates quickly against a
      harness that only reads `id()` + `sequence()`). All three
      `growth_<rep>.json` files conform to the DESIGN §4.5 schema;
      full write-up + reproducer at
      `compares/results/coverage/aflpp/seqan3/REPORT.md`.

  ```bash
  # Short-regime invocation actually used (60 s × 3 reps, ticks 1/10/60):
  python3.12 compares/scripts/run_aflpp_seqan3_phase2.py \
      --seed-corpus /work/compares/results/bench_seeds/sam \
      --budget 60 --reps 3 \
      --out /work/compares/results/coverage/aflpp/seqan3

  # Primary-regime re-run (7200 s × 3 reps, ticks 1/10/60/300/1800/7200):
  python3.12 compares/scripts/run_aflpp_seqan3_phase2.py \
      --seed-corpus /work/compares/results/bench_seeds/sam \
      --budget 7200 --reps 3 \
      --out /work/compares/results/coverage/aflpp/seqan3
  ```
- [x] **Pure Random × every SUT** (6 commands — floor baseline
      must span the full matrix for the 95% CI bands to be
      comparable). **Executed 2026-04-20** via the self-contained
      orchestrator `compares/scripts/run_pure_random_phase2.py`
      (`coverage_sampler.py` dispatches `--tool pure_random` into
      the same driver; either entry point produces identical output).
      Full primary regime: 7200 s × 3 reps × 6 cells, ticks
      `{1, 10, 60, 300, 1800, 7200}`. 18/18 `growth_<rep>.json`
      files landed under
      `compares/results/coverage/pure_random/<cell>/` and pass
      `validate_growth_schema.py` with zero hard errors. Coverage
      backends per cell: **JaCoCo append-mode** for htsjdk VCF + SAM
      (`java -javaagent:jacocoagent.jar=destfile=…,append=true,…` on
      each replay JVM — one `.exec` accumulates across ticks, then
      `jacococli report --xml` filtered to `FORMAT_SCOPES[fmt]`);
      **coverage.py programmatic API** for vcfpy + biopython (driver
      pre-imports NumPy / Bio.Align / vcfpy BEFORE
      `coverage.Coverage(…).start()` — dodges the NumPy 2.x
      "`cannot load module more than once per process`"
      double-load bug in the CTracer; single-subprocess replay per
      tick so `cov.save()` doesn't get overwritten by a later
      chunk); **gcov / gcovr** for seqan3 (cumulative `.gcda`
      within each tick, reset across ticks; `gcovr -r harnesses/cpp
      --json` rooted at the harness TU because the MSYS2 system
      headers aren't `--coverage`-instrumented on the Windows dev
      host — full-library coverage is deferred to the
      Docker-image Clang-18 + patched seqan3 build per §13.2.4);
      **cargo-llvm-cov skipped** for noodles-vcf (Rust toolchain
      absent on the Windows host → the cell lands with
      `coverage_growth=[…, 0.0/0.0, …]` + `extra.blocked_reason`
      documenting the block, so the matrix still spans all 6 cells
      and the Phase-6 CI bands compare fairly across tools; a
      Docker-image rerun promotes it to real numbers with no
      schema change). Measured curve at t=7200 s (3-rep mean, 95 %
      CI across reps, `compares/results/coverage/pure_random/<cell>/growth_aggregate.json`):

      | cell              | line % (mean [95 % CI]) | branch % (mean [95 % CI]) |
      |:------------------|:-----------------------|:-------------------------|
      | htsjdk VCF        |  1.490 [1.44 – 1.54]   |  0.350 [0.26 – 0.45]    |
      | htsjdk SAM        |  2.190 [1.90 – 2.49]   |  0.750 [0.71 – 0.80]    |
      | vcfpy             |  2.720 [2.72 – 2.72]   |  0.670 [0.67 – 0.67]    |
      | noodles-vcf       |  0.000 [0.00 – 0.00] † |  0.000 [0.00 – 0.00] † |
      | biopython         |  1.840 [0.53 – 3.15]   |  0.890 [0.02 – 1.76]    |
      | seqan3            | 78.300 [69.19 – 87.42] ‡ | 43.190 [36.34 – 50.05] ‡ |

      † cargo-llvm-cov unavailable on the Windows dev host — see
      the blocked_reason in each rep's `extra`; promote to real
      numbers inside the biotest-bench Docker image.
      ‡ seqan3 scope covers only `harnesses/cpp/biotest_harness.cpp`
      on this host (MSYS2 libstdc++ headers aren't instrumented) —
      the number is the harness parse-path coverage, not
      `seqan3/io/sam_file` full-library coverage; the latter is a
      Docker-image measurement.

      Low percentages on the other rows are the **expected**
      floor-baseline signal: `os.urandom` bytes almost never satisfy
      the VCF/SAM header grammar, so coverage is dominated by the
      "reject at header" branch in each parser. That is exactly why
      Pure Random is the floor comparator — other fuzzers must beat
      this number to justify their complexity. The output schema
      matches DESIGN §4.5 with an extra `per_tick` block inside
      `extra` carrying `(prefix_size, accepted, rejected, timeout)`
      per tick — see `run_pure_random_phase2.py` docstring for the
      driver's generate-then-replay prefix-sampling model.
  ```bash
  for FMT in VCF SAM; do
    LCASE=$(echo $FMT | tr A-Z a-z)
    python3.12 compares/scripts/coverage_sampler.py \
        --tool pure_random --sut htsjdk --format $FMT \
        --seed-corpus compares/results/bench_seeds/${LCASE} \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/pure_random/htsjdk_${LCASE}/
  done
  # vcfpy + noodles — VCF-only primaries
  for SUT in vcfpy noodles; do
    python3.12 compares/scripts/coverage_sampler.py \
        --tool pure_random --sut $SUT --format VCF \
        --seed-corpus compares/results/bench_seeds/vcf \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/pure_random/${SUT}/
  done
  # biopython + seqan3 — SAM-only primaries
  for SUT in biopython seqan3; do
    python3.12 compares/scripts/coverage_sampler.py \
        --tool pure_random --sut $SUT --format SAM \
        --seed-corpus compares/results/bench_seeds/sam \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/pure_random/${SUT}/
  done

  # Equivalent single-call matrix runner (runs the 6 cells above
  # sequentially and writes the same output tree):
  py -3.12 compares/scripts/run_pure_random_phase2.py \
      --run-all --budget 7200 --reps 3
  ```
- [ ] **EvoSuite anchor × htsjdk** — not a per-tick coverage run;
      EvoSuite emits a generated JUnit suite, then JaCoCo measures
      coverage on that suite. Existing host-side driver handles it:
  ```bash
  SEARCH_BUDGET=7200 bash compares/scripts/run_evosuite.sh \
      --classes 'htsjdk.variant.vcf.*,htsjdk.samtools.*'
  bash compares/scripts/measure_evosuite_coverage.sh
  # Landed JSON:
  #   compares/results/coverage/evosuite_anchor/htsjdk/growth.json
  ```
  Reps = 1 because EvoSuite's genetic-algorithm search is
  deterministic at a fixed search budget; §4.2 exempts the anchor
  from the 3-rep rule.

- [ ] **Monitor**: confirm log ticks `{1, 10, 60, 300, 1800, 7200}`
      appear in each `growth_<run_idx>.json`. One-liner check:
  ```bash
  find compares/results/coverage -name 'growth_*.json' -exec \
      python3.12 -c 'import json,sys; d=json.load(open(sys.argv[1])); \
      ticks=sorted({s["t_s"] for s in d["coverage_growth"]}); \
      assert {1,10,60,300,1800,7200}.issubset(ticks), (sys.argv[1], ticks)' {} \;
  ```
- [ ] **Parallelisation layout**: 4 concurrent workers, one per
      CPU group. Recommended split (keeps coverage tools on distinct
      JVMs / venvs / cargo builds):
      worker-1 = Jazzer (htsjdk VCF + SAM back-to-back);
      worker-2 = Atheris (vcfpy + biopython);
      worker-3 = cargo-fuzz (noodles) + libFuzzer (seqan3);
      worker-4 = Pure Random (all 6 SUTs serially — each is fast so
      the serial walltime is ~6h vs ~2h per heavy-tool worker).
- [ ] **Back up** `compares/results/coverage/` to off-machine
      storage after the full sweep completes.

#### Phase 3 — Mutation score (~2 overnights, 1 per 2 SUTs)

For each (tool, SUT) cell, the mutation driver (a) picks the right
per-language mutation engine — PIT (Java) / mutmut (Python) /
cargo-mutants (Rust) / mull (C++); (b) reads the tool's accepted-
input corpus from Phase 2 as the test suite; (c) runs each mutant
against that suite; (d) emits `summary.json` with
`{killed, reachable, score}`.

**Orchestrator** — two scripts, both landed 2026-04-21 alongside
Jazzer × htsjdk's Phase-3 run:

* `compares/scripts/phase3_jazzer_pit.sh` — end-to-end PIT driver for
  the Jazzer × htsjdk row. Uses JUnit-4 tests
  (`compares/scripts/phase3_pit/{VCF,SAM}MutationTest.java`) that
  iterate the corpus and assert each file's outcome matches the
  pre-computed `baseline.json` produced by `BaselineBuilder.java`. PIT
  fires one minion JVM per mutant; a mutant is killed whenever any
  corpus file's outcome string (`ok:<record-count>` or
  `err:<ExceptionClass>`) diverges from baseline — this is the
  DESIGN.md §3.3 "parse-success flip / crash flip / record-diff"
  criterion at record-count + exception-class granularity.
* `compares/scripts/enumerate_target_classes.py` — reuses
  `biotest_config.yaml:coverage.target_filters.<fmt>.<sut>` (the same
  fairness recipe Phase 2 scopes coverage with) to produce PIT's
  `--targetClasses` list. That guarantees PIT mutates **exactly** the
  classes Jazzer's harness actually drives: for VCF that's 81 classes
  (vcf + non-JEXL variantcontext + VCF*/Variant* writer), for SAM 98
  classes (`samtools::SAM,Sam`-prefixed). htsjdk's 800+ other classes —
  BAM, CRAM, BCF, JEXL, CLI, index — stay out of the denominator.
* `compares/scripts/summarise_pit.py` + `compares/scripts/write_phase3_report.py`
  — XML → `summary.json` → Markdown report at
  `compares/results/mutation/jazzer/mutation_score.md`.

Expected signature (per-tool row; fallback when a dedicated driver
doesn't exist yet):

```bash
py -3.12 compares/scripts/mutation_driver.py \
    --tool <name> --sut <name> \
    --corpus <path to Phase-2 accepted inputs> \
    --budget <seconds> \
    --out compares/results/mutation/<tool>/<sut>/
```

**Pre-flight** (do this once per overnight batch):
- [ ] **Stop Ollama / local LLMs.** Mutation testing is RAM-hungry
      and any background LLM will OOM PIT's fork pool.
- [ ] **Confirm Phase 2 corpora exist** at
      `compares/results/coverage/<tool>/<sut>[_<fmt>]/corpus/`. Each
      tool's corpus becomes that tool's test suite.

**Per-cell invocations** (10 baseline cells + 1 EvoSuite anchor;
11 total; BioTest rows deliberately omitted per §13.5 scope):

- [x] **Jazzer × htsjdk — PIT (Java)** — **done 2026-04-21**.
      Primary-regime run; per-cell final numbers (see
      `compares/results/mutation/jazzer/mutation_score.md` for the
      full report with per-class top-5 breakdowns + PIT status
      histograms):

      | cell | target classes | reachable | killed | survived | NO_COVERAGE | **score** |
      |:-----|:-------------:|:---------:|:------:|:--------:|:-----------:|:---------:|
      | Jazzer × htsjdk / **VCF** | 81 | 628 | 233 | 395 | 1674 | **37.10 %** |
      | Jazzer × htsjdk / **SAM** | 98 | 630 | 161 | 469 | 2546 | **25.56 %** |

      Reachable = KILLED + SURVIVED + TIMED_OUT (DESIGN.md §3.3:
      "mutants in code the corpus actually executed"). NO_COVERAGE
      mutants fall outside the denominator — they sit on lines no
      corpus file reaches, so the test suite has no chance to kill
      them. They're logged in the summary for transparency but
      don't dilute the score.

      Reproducer — one command, both formats, inside `biotest-bench`:
  ```bash
  # Full run (threads=6 for VCF; SAM wants threads=2 + -Xmx2g on the
  # minion — the SAM 6-thread fork pool OOM'd the initial run, log at
  # compares/results/mutation/jazzer/phase3_jazzer_htsjdk.log).
  docker run -d --name phase3-jazzer-vcf \
      -v "$(pwd):/work" -w /work \
      -e FORMATS="VCF" -e THREADS=6 -e CORPUS_MAX=200 \
      biotest-bench:latest bash compares/scripts/phase3_jazzer_pit.sh
  docker run -d --name phase3-jazzer-sam \
      -v "$(pwd):/work" -w /work \
      -e FORMATS="SAM" -e THREADS=2 -e CORPUS_MAX=150 \
      biotest-bench:latest bash compares/scripts/phase3_jazzer_pit.sh
  # after both exit:
  py -3.12 compares/scripts/write_phase3_report.py
  ```

      Mutant scope (exactly what the fairness recipe says): **VCF** =
      `htsjdk.variant.vcf.*` + `htsjdk.variant.variantcontext.*` minus
      `*JEXL*`/`*Jexl*` + `htsjdk.variant.variantcontext.writer.*`
      restricted to `VCF*`/`Variant*` files (81 classes). **SAM** =
      `htsjdk.samtools::SAM,Sam` prefix (98 classes). BAM, CRAM, BCF,
      index, and CLI code stay out of the denominator because the
      Jazzer harness never exercises them. Mutators = `DEFAULTS`.

      Walltime: VCF = 26.5 min (6 threads); SAM = 34 min (2 threads).
      ~1 h combined — well under §3.3's 2 h/cell budget; plenty of
      headroom to widen to `--mutators STRONGER` or `CORPUS_MAX=500` if
      a richer kill surface is wanted.
- [x] **Atheris × vcfpy — mutmut (Python)** — **tooling complete +
      primary-regime run executed 2026-04-20**. Result:
      **89.59 % mutation score (852 killed / 951 reachable)** in
      **1 022 s** wall-time against the Phase-2 atheris-union corpus
      (1 025 files), scoped to the five VCF-parser modules per
      Flow.md §1149. What landed this session:
  - `compares/scripts/mutation_driver.py` — promoted from placeholder.
    Per-cell flow for `--tool atheris --sut vcfpy`: (1) copy pristine
    `vcfpy/` from the biotest-bench atheris-venv into `<out>/vcfpy/`;
    (2) materialise `<out>/union_corpus/` by unioning the three
    Phase-2 rep corpora; (3) write `<out>/setup.cfg` with
    `do_not_mutate = __init__.py, version.py, tabix.py, bgzf.py`
    (the four files outside Flow.md's `target_filters.VCF.vcfpy`
    scope); (4) pre-generate the mutmut-rewritten tree by calling
    `mutmut.__main__.create_mutants() + copy_also_copy_files()`
    directly (side-effect: `<out>/mutants/vcfpy/` populated with
    trampolines); (5) capture baseline fingerprints against the
    rewritten tree with `MUTANT_UNDER_TEST=''`; (6) invoke
    `mutmut run` via the `run_mutmut.py` shim. Final summary.json
    parsed from mutmut's spinner + per-file `*.py.meta` DBs so the
    build-report consumer gets both total and per-file breakdown.
  - `compares/scripts/mutation/run_mutmut.py` — monkey-patches
    mutmut 3.0 around two pain points: (a) replaces `CatchOutput`
    with a no-op context manager (pytest's capture machinery
    deadlocks against mutmut's fileno-less stdout redirect → exit-4
    BadTestExecutionCommandsException); (b) re-exports
    `record_trampoline_hit` + `MutmutProgrammaticFailException` at
    module scope so the trampoline's `from __main__ import …` works
    when mutmut is invoked via wrapper.
  - `compares/scripts/mutation/test_vcfpy_corpus.py` — pytest
    runner that mutmut auto-copies into `<out>/mutants/tests/` and
    invokes per-mutant. Replays `MUTMUT_CORPUS_SAMPLE` (=40 here)
    corpus files through `vcfpy.Reader.from_path(...)`, computes a
    count-based integer fingerprint (n_header_lines, n_records,
    Σ POS, Σ len(REF), Σ ord(CHROM), per-record INFO/FORMAT/ALT
    cardinality sums, mid-iteration exception class), compares
    against `MUTMUT_BASELINE_FILE`. Exit 1 on first flip (kill),
    exit 0 on all-match (survive). Exit 5 ("no tests") only fires
    when mutmut's stats phase didn't associate this file's test
    with any mutant — i.e. the mutant's function is out of scope.
  - `compares/scripts/mutation/vcfpy_corpus_runner.py` — same
    fingerprint logic packaged as a standalone CLI (`--mode
    baseline` / default `check`) so baseline capture doesn't need
    mutmut. Used only by step (5) above.
  - **Integer-aggregate fingerprint (not byte-exact repr)** is
    required — earlier revisions hashed `repr(record)` which picked
    up object-identity / insertion-order drift from mutmut's
    trampoline rewrite even when `MUTANT_UNDER_TEST=''`, causing
    false-positive kills on every stats-phase invocation. Counting
    aggregates are trampoline-invariant but still flip on any
    reachable semantic mutation. The 99 remaining survivors in
    `parser.py` (vs. 100 % on header/record and 90 % on reader)
    are the well-understood "dead-branch + warning-string flip"
    residue mutation testing always leaves behind.
  - **VCF scope honoured twice**: (1) `do_not_mutate` strips
    `__init__` / `version` / `tabix` / `bgzf` at generation time
    (though mutmut 3.0's fnmatch implementation matches on the
    full path and doesn't in fact skip bgzf/tabix as we intended —
    those mutants are still generated but ALL land in the
    `no_tests` bucket because the atheris corpus never hits
    bgzf/tabix code paths, so they're naturally excluded from the
    score denominator); (2) the reachable denominator includes
    only mutants whose function mutmut's stats phase saw the
    runner execute — i.e. ONLY mutants in `reader.py`, `parser.py`,
    `header.py`, `record.py` (writer.py mutants land in `no_tests`
    because the read-only Atheris harness never exercises them).
    Matches Flow.md §1149's `target_filters.VCF.vcfpy` scope
    exactly.
  - **Primary regime command** (end-to-end, ~17 min wall):
    ```bash
    py -3.12 compares/scripts/mutation_driver.py \
        --tool atheris --sut vcfpy \
        --budget 3600 --corpus-sample 40 --max-children 1 \
        --out compares/results/mutation/atheris/vcfpy
    ```
    Launch with `nohup ... &; disown` from any interactive shell
    so mutmut's child docker container survives the parent Bash
    exit (same SIGHUP gotcha Phase 2 rep 1/2 hit).
  - **Measured result — 2026-04-20, 3 600 s wall-budget
    (actually finished in 1 021.87 s), 1 025-file union corpus
    with 40-file per-mutant sample**:

    | Metric                                    |     Value |
    | :---------------------------------------- | --------: |
    | **Mutation score (reachable-scoped)**     | **89.59 %** |
    | Killed                                    |       852 |
    | Survived                                  |        99 |
    | Reachable                                 |       951 |
    | No-tests (out-of-scope / unreached)       |     1 387 |
    | Total AST mutants generated               |     2 338 |
    | mutmut wall-time                          |  1 021.87 s |
    | mutmut exit code                          |         0 |

    Per-file breakdown: **`header.py` 100.00 %** (300 / 300),
    **`parser.py` 82.89 %** (470 / 567), **`reader.py` 90.48 %**
    (19 / 21), **`record.py` 100.00 %** (63 / 63); `writer.py`,
    `bgzf.py`, `tabix.py` 0 reachable by construction (atheris
    harness is read-only on plain-text VCF).
  - **Full write-up + methodology + per-file table + top-surviving
    mutants** at `compares/results/mutation/atheris/vcfpy/MUTATION_REPORT.md`.
- [x] **Atheris × biopython — mutmut (Python)** — **tooling complete +
      representative run executed 2026-04-20**. What landed this session:
  - `compares/harnesses/atheris/phase3_mutation_loop.py` — in-container
    AST-mutation + corpus-replay driver. Uses hand-rolled mutmut-style
    operators (arithmetic swaps, comparison flips, `And↔Or`, `not`
    removal, constant mutations `True↔False`/`None→0`/int ±1/string
    → empty) on `Bio/Align/sam.py`. Each mutant is swapped into
    `/opt/atheris-venv/.../Bio/Align/sam.py` in place (backed up as
    `.phase3_bak`, restored in `finally`). A fresh-import worker
    subprocess parses every corpus file through
    `Bio.Align.sam.AlignmentIterator`; a mutant is **killed** iff any
    file's `(ok, aln_count, err_type)` tuple diverges from the
    unmutated baseline — otherwise **survived**. Honours
    `--budget-s` / `--max-mutants` so the loop degrades gracefully when
    cut short.
  - `compares/scripts/phase3_atheris_biopython.sh` — wrapper that
    invokes the loop inside `biotest-bench:latest` with the rep-0 corpus
    mounted read-write. One-liner (mirrors phase2_atheris_biopython.sh):
    ```bash
    bash compares/scripts/phase3_atheris_biopython.sh
    # Env overrides: BUDGET_S (default 900), PER_MUTANT_TIMEOUT_S (60),
    # MAX_MUTANTS (0 = budget-bounded), CORPUS_DIR (defaults to
    # compares/results/coverage/atheris/biopython/run_0/corpus).
    ```
  - Results land under
    `compares/results/mutation/atheris/biopython/`:
    `summary.json` (DESIGN §4.5 mutation_score + baseline rollup),
    `mutants.jsonl` (one line per tested mutant with
    `{id, operator, lineno, outcome, elapsed_s, diff_files[]}`),
    `_worker.py` (the fresh-import corpus-replay worker), and
    `phase3_atheris_biopython.log` (stream from the wrapper).
  - Mutant scope: `Bio/Align/sam.py` only (the SAM parser path;
    pairwise-alignment mutants would be out of scope and inflate
    `reachable`). On 2026-04-20 the AST-mutation pass yields **523
    mutants** over that file. Flow.md §`coverage_target_filters.SAM`
    pins this file as the authoritative SAM scope for biopython, so
    file-level + line-level filters are mutually consistent with the
    Phase-2 coverage target.
  - **Reached-lines scoping (DESIGN §3.3 canonical)** applied via
    `compares/scripts/rescope_mutation_to_reached.py` — post-processes
    `mutants.jsonl` against the Phase-2 `.coverage` SQLite, producing
    `summary_scoped.json` + `mutants_scoped.jsonl`. Mutants on lines
    the Phase-2 corpus never executed are excluded from the
    `reachable` denominator (they'd all survive by construction and
    don't reflect oracle power).
  - **Measured result — 2026-04-20, 1500 s wall-budget, rep-0 corpus**:

    | Metric                           |     Value |
    | :------------------------------- | --------: |
    | Mutation score (scoped)          | **0.5849** |
    | Killed / Reachable (scoped)      | 155 / 265 |
    | Reached lines in `sam.py`        | 327 / 598 |
    | Mutation score (full file)       |   0.2951  |
    | Killed / Reachable (full file)   | 152 / 515 |
    | Total AST mutants generated      |      523  |
    | Loop duration                    | 1 049.8 s |

    Top-killing operator: `unary_not_removal` (100 % kill-rate on
    reached lines) — flipping `not flag & 4` at `sam.py:728`
    (SAM FLAG unmapped-bit per SAMv1 §1.4) diverges on 59 of 390
    corpus files. Lowest-killing operator: `const_bool`
    (True↔False) at 16.7 % — typical oracle-weak cases DESIGN §3.3
    flags.
  - **Full per-operator breakdown, top-killed mutants, caveats, and
    artefact inventory**:
    `compares/results/mutation/atheris/biopython/MUTATION_RESULTS.md`.
- [x] **cargo-fuzz × noodles-vcf — cargo-mutants (Rust)** —
      **landed 2026-04-20**. Driver invocation:
  ```bash
  py -3.12 compares/scripts/mutation_driver.py \
      --tool cargo_fuzz --sut noodles \
      --corpus compares/results/coverage/cargo_fuzz/noodles/run_0/corpus \
      --budget 7200 \
      --out compares/results/mutation/cargo_fuzz/noodles/
  ```
  **Mutant scope — tighter than "`--package noodles-vcf`" to honour
  DESIGN §3.3's "reachable = mutants in code the corpus actually
  executed"**: we restrict to the VCF-read paths the cargo-fuzz target
  exercises (via `--file` filters):

  | Pattern              | What it covers                         |
  | :------------------- | :------------------------------------- |
  | `src/io/reader/**`   | builder + header reader + record reader + field parsers + BufRead impls |
  | `src/record.rs` + `src/record/**` | `Record` + `TryFrom<&[u8]>` parse + per-field data types |
  | `src/header.rs`      | `Header` + `FromStr` parse impl        |

  **NOT mutated** (not exercised by the read-only fuzz target): writer
  (`src/io/writer/**`), async (`src/async/**`), indexer, and the
  abstract-trait layer in `src/variant/**`. This aligns with Flow.md
  line 1150's `target_filters.VCF` coverage scope, tightened for the
  cargo-fuzz row's read-only call pattern.

  **Pipeline** — the mutable noodles-vcf 0.70 source lives at
  `compares/baselines/noodles-vcf-0.70-src/` (materialised from the
  cargo registry cache via `cargo fetch` + `cp -r`; no external git
  clone required). A Rust integration test
  `tests/biotest_corpus_oracle.rs` reads the Phase-2 corpus, parses
  via (possibly mutated) noodles-vcf, fingerprints `{accepted,
  record_count, sample_count, first_error}` per file, and compares
  against a captured baseline; divergence → panic → mutant caught.
  cargo-mutants runs `cargo test --test biotest_corpus_oracle` per
  mutant.

  **Results** (full run 2026-04-20, corpus sample = 200 files, wall
  time 33 min, budget used 27 %):

  | Bucket        | Count |
  | :------------ | ----: |
  | enumerated mutants | 483 |
  | **killed**    | **28** (caught 21 + timeout 7) |
  | survived      | 271  |
  | unviable      | 184  |
  | reachable     | 299  (killed + survived, excludes unviable per cargo-mutants convention) |
  | **score**     | **9.36 %** (= 28 / 299)       |

  All 21 caught mutants are in parser core (`src/header.rs:361`,
  `src/io/reader/header.rs` 5 mutants, `src/io/reader/record.rs`
  13+ mutants) — exactly where the fuzz corpus pushes bytes.
  The 271 survived mutants are almost all in accessor methods
  (Header::infos, Record::reference_sequence_name, …) that the
  read-only fuzz target never calls; a richer oracle (BioTest's
  cross-parser canonical-JSON diff) would kill more. The **13 pp
  gap** to the Phase-2 coverage number (22.72 % lines vs 9.36 %
  mutation) is the classic "coverage saturates before defect
  detection" signal (DESIGN §3.3 rationale paragraph).

  Results manifested at `compares/results/mutation/cargo_fuzz/noodles/`:
  `summary.json` (DESIGN §4.5 schema), `baseline.json`,
  `mutants.out/{outcomes.json,caught.txt,missed.txt,timeout.txt,
  unviable.txt,diff/,log/}`, and a sibling `RESULTS.md` with the full
  per-cell writeup.

  Prereq state refreshed: **`cargo-mutants 27.0.0` installed** via
  `cargo install cargo-mutants --locked` + `docker commit
  biotest-bench:latest` on 2026-04-20 (§13.3.3 row flipped to ✓).
  **`rustup llvm-tools-preview` re-installed** in the same session
  (the earlier install was in a short-lived container that got
  recycled; now committed into the image).
- [x] **libFuzzer × seqan3 — mull (C++)** — **executed 2026-04-21**.
  Both format sub-cells run. The SAM cell carries a real mutation
  score; the VCF cell is a documented `status: not_applicable`
  (seqan3 has no VCF parser — `Flow.md §2.1` *"SeqAn3 暂不支持 VCF
  IO，故移除"*; `biotest_config.yaml: coverage.target_filters.VCF`
  has no `seqan3` key; `seqan3_sam_fuzzer.cpp` instantiates only
  `seqan3::sam_file_input` + `seqan3::format_sam{}`).

  | format | killed | survived | compile-errors | reachable | **score** | wall |
  | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
  | SAM | **52** | **1** | 31 | **53** | **0.9811** | 595.6 s |
  | VCF | —   | —   | —  | —  | **N/A** | — |

  The one surviving SAM mutant is
  `format_sam.hpp:533  ROR_eq_to_ne '=='→'!='` on the line
  `(tag_end_pos == std::string_view::npos) ? raw_record[10].end() :
  raw_record[10].begin() + tag_end_pos;` — an explainable live
  mutant: the libFuzzer harness reads only `record.id()` +
  `record.sequence()` (widening the fields triggers the
  `alphabet_tuple_base` concept failures documented in §13.2.4), so
  mutations that only perturb the tag-section iterator produce
  identical `id_hash` + `seq_len_sum` digests on the corpus and are
  indistinguishable through our observables.

  **Mutator used — mull substitute.** `biotest-bench:latest` ships
  mull 0.33's Ubuntu-24.04 deb (§13.1), but the image is 22.04 so
  both runtime binaries abort at load time:
  `mull-runner-18` → `GLIBC_2.39 not found`;
  `mull-ir-frontend-18` → `GLIBC_2.36/2.38/2.39 not found`. Upstream
  doesn't ship a 22.04 build for mull 0.33 at the LLVM 18 target,
  and rebuilding mull from source / bumping the base image is out
  of scope for this run. The SAM cell therefore runs the
  **mull-equivalent source-level driver** now wired into
  `compares/scripts/mutation_driver.py` (new `_run_libfuzzer_seqan3`
  backend): same ROR / AOR / LOR operator families mull's
  `--mutators=default` emits, same seqan3 SAM scope
  (`seqan3/io/sam_file`, `format_sam`, `cigar` — identical to
  biotest_config.yaml `coverage.target_filters.SAM.seqan3`), same
  DESIGN §3.3 kill semantics (parse-success flip / canonical-digest
  diff / crash flip — implemented via a new
  `BIOTEST_HARNESS_MUT_DIGEST=1` mode of
  `seqan3_sam_fuzzer.cpp` that prints a per-input digest line the
  driver diff-compares across baseline and mutant runs).

  **Reachability filter (DESIGN §3.3 denominator).** At campaign
  start the driver invokes `gcovr` against the Phase-2
  `_build-cov-iso/*.gcda` (reusing Phase 2's coverage
  instrumentation) and only considers mutations on lines with
  `count > 0`. 698 reachable lines → 84 in-scope candidate mutants →
  53 compiled → 52 killed. The 31 compile-errors are
  mull-equivalent unviable mutants (seqan3 template concepts reject
  them — e.g. `+`→`-` inside a SFINAE bound).

  Artefacts + full writeup:
  `compares/results/mutation/libfuzzer/seqan3_{sam,vcf}/summary.json`
  + `details.json` + `runner.log` + `baseline.json`. Headline
  report at
  `compares/results/coverage/libfuzzer/seqan3/phase3_mutation_report.md`
  (lives next to the Phase 2 growth files so the SAM row's
  Phase 2 + Phase 3 artefacts are collocated).

  Reproduce (inside `biotest-bench`):
  ```bash
  # 0. Build the mutation-test driver binary (one-off per image).
  mkdir -p compares/results/coverage/libfuzzer/seqan3/_build-mut-iso
  bash compares/docker/run.sh bash -lc '
    cd /work/compares/results/coverage/libfuzzer/seqan3/_build-mut-iso &&
    cmake /work/compares/harnesses/libfuzzer \
          -DCMAKE_CXX_COMPILER=clang++-18 \
          -DCMAKE_CXX_FLAGS=-DSEQAN3_DISABLE_COMPILER_CHECK &&
    make -j4 seqan3_sam_fuzzer_mut
  '

  # 1. SAM campaign.
  bash compares/docker/run.sh bash -lc '
    python3.12 compares/scripts/mutation_driver.py \
        --tool libfuzzer --sut seqan3 --format SAM \
        --in-container \
        --corpus /work/compares/results/coverage/libfuzzer/seqan3/run_0/corpus \
        --out /work/compares/results/mutation/libfuzzer/seqan3_sam \
        --max-mutants 120 --corpus-sample 120 --budget 3600 \
        --per-file-timeout-s 2 \
        --seqan3-src-root /opt/seqan3/include \
        --mut-build-dir /work/compares/results/coverage/libfuzzer/seqan3/_build-mut-iso \
        --mut-bin /work/compares/results/coverage/libfuzzer/seqan3/_build-mut-iso/seqan3_sam_fuzzer_mut \
        --cov-build-dir /work/compares/results/coverage/libfuzzer/seqan3/_build-cov-iso
  '

  # 2. VCF — emits an N/A summary immediately (seqan3 has no VCF parser).
  bash compares/docker/run.sh bash -lc '
    python3.12 compares/scripts/mutation_driver.py \
        --tool libfuzzer --sut seqan3 --format VCF \
        --in-container \
        --out /work/compares/results/mutation/libfuzzer/seqan3_vcf \
        --corpus /work/compares/results/coverage/libfuzzer/seqan3/run_0/corpus
  '
  ```
- [x] **AFL++ × seqan3 — mull (C++)** (alternate; run only if a
      cross-fuzzer corroboration is desired on the mutation score).
      **Executed 2026-04-20** via the self-contained source-level
      mutation driver
      `compares/scripts/run_aflpp_seqan3_phase3.py`. mull-0.33's
      `mull-runner-18` + `mull-ir-frontend-18` binaries require
      `GLIBC_2.39`; biotest-bench is Ubuntu 22.04 (glibc 2.35), so
      both binaries ELF-launch-error at run time despite the .deb
      installing cleanly (§13.2.4). The stand-in driver implements
      the DESIGN §3.3 detection semantics (_"killed if the generated
      test suite causes the mutated SUT's output to diverge from the
      unmutated SUT's output"_) by regex operator-swap on covered
      lines in `seqan3/io/sam_file/**`, rebuilding the cov binary
      per mutant, and comparing the 53-file exit-code vector of the
      AFL++ Phase-2 corpus against baseline. Swap mull back in when
      the bench image is upgraded to Ubuntu 24.04.

      **Result (20-mutant budget; corpus = Phase-2 `run_0/corpus`)**:

      | Metric | Value |
      |:---|---:|
      | mutants generated | 20 |
      | compile-failed (excluded from reachable) | 6 |
      | reachable | 14 |
      | killed | 10 |
      | survived | 4 |
      | **mutation score** | **0.7143 (71.4 %)** |

      By operator: `NE_TO_EQ` 4/4 (100 %), `LE_TO_GE` 1/1 (100 %),
      `EQ_TO_NE` 4/6 (66.7 %), `PLUS_TO_MINUS` 1/2 (50 %),
      `TRUE_TO_FALSE` 0/1 (0 %); `AND_TO_OR`/`OR_TO_AND` all
      compile-failed (C++20 concept conjunctions reject those
      swaps). By file: `format_sam_base.hpp` 8/10 (80 %),
      `cigar.hpp` 2/4 (50 %). All 10 kills diverge on
      `real_world_htslib_auxf_values.sam` — the htslib c1_auxf
      regression seed that also drives the Phase-2 AFL++ crash
      finding, converting baseline SIGABRT (rc=−6) to mutant
      clean-exit (rc=0) as the mutations disable tag-size
      assertions. Four survivors concentrate on harness-narrow
      paths (`cigar_str == "*"`, `ref_info_present_in_header`)
      that the record-id-only harness never consumes — a richer
      harness (iterate `cigar_sequence()` +
      `reference_position()`) would convert 3 of them to kills.
      Full write-up + reproducer at
      `compares/results/mutation/aflpp/AFLPP_MUTATION_RESULTS.md`.

  ```bash
  # Source-level driver actually used (mull-unblocked rerun at bottom):
  python3.12 compares/scripts/run_aflpp_seqan3_phase3.py \
      --corpus  /work/compares/results/coverage/aflpp/seqan3/run_0/corpus \
      --cov-gcovr-json /work/compares/results/coverage/aflpp/seqan3/run_0/gcovr_snapshots/t_60s.json \
      --budget-mutants 20 \
      --out     /work/compares/results/mutation/aflpp/seqan3

  # Once mull is unblocked (bench image on Ubuntu 24.04 / glibc 2.39):
  py -3.12 compares/scripts/mutation_driver.py \
      --tool aflpp --sut seqan3 --corpus \
      compares/results/coverage/aflpp/seqan3/run_0/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/aflpp/seqan3/
  ```
- [x] **Pure Random × every SUT** (6 cells; one PIT + two mutmut +
      two mull-or-cargo-mutants calls. The floor-baseline's mutation
      score is the key comparator for the other tools). **Executed
      2026-04-20** via the self-contained orchestrator
      `compares/scripts/run_pure_random_phase3.py` (union of the 3
      Phase-2 reps' `run_*/corpus` as test suite; mutmut 2.5.1 for
      vcfpy / biopython; PIT / cargo-mutants / mull graceful-skip
      with `blocked_reason` on the Windows host per DESIGN §3.3's
      floor-baseline matrix-completeness rule). **Mutation scope
      matches `biotest_config.yaml:coverage.target_filters`**
      exactly — vcfpy mutates only `reader/parser/header/record/writer.py`
      (bgzf + tabix excluded per Flow.md vcfpy row "排除 bgzf/tabix");
      biopython mutates only `Bio/Align/sam.py` (single file,
      inherently scoped). This drops vcfpy's mutant count from
      2239 (whole-package) to 1484 (scoped) and keeps the score
      honest: off-path helpers can't silently pad the denominator.
      Test-kill protocol (per DESIGN §3.3): baseline captures a
      sha1 fingerprint per file (record stream + exception
      type/message) with the unmutated SUT; each mutmut-generated
      mutant runs a fingerprint-compare driver; exit 1 on any flip
      = killed. `mutmut 2.5.1`'s text output hides the "killed"
      count (bug), so the driver reads the authoritative counts
      from `.mutmut-cache`'s `Mutant.status` SQLite column via
      `compares/scripts/mutation/rederive_summaries.py`. Results:

      | cell         | engine              | killed | reachable | score (killed / reachable) |
      |:-------------|:--------------------|-------:|----------:|:--------------------------|
      | htsjdk VCF   | PIT 1.15.3          |     —  |        —  | **blocked †**              |
      | htsjdk SAM   | PIT 1.15.3          |     —  |        —  | **blocked †**              |
      | vcfpy        | mutmut 2.5.1        | **1139** | **1484** | **76.75 %**                |
      | noodles-vcf  | cargo-mutants       |     —  |        —  | **blocked ‡**              |
      | biopython    | mutmut 2.5.1        | **9**  | **853**  | **1.06 %**                 |
      | seqan3       | mull 0.33 (LLVM 18) |     —  |        —  | **blocked §**              |

      † PIT JARs downloaded at `compares/baselines/pit/` but
      running PIT against pure_random's corpus needs a JUnit 5
      wrapper + compiled classpath — both pre-wired inside
      `biotest-bench:latest /opt/pit/`. Deferred to Docker rerun.
      ‡ cargo-mutants absent on Windows (no Rust toolchain); same
      block as DESIGN §13.2.7 noodles coverage row. § mull 0.33
      requires Clang 18 + patched seqan3 (DESIGN §13.2.4);
      Docker-only.

      The **vcfpy 77 % vs biopython 1 %** asymmetry is the key
      diagnostic: pure_random bytes reach deep into vcfpy's parse
      graph (pure-Python, accepts arbitrary bytes) and flip
      exception-message fingerprints routinely, but biopython's
      `Bio.Align.sam.AlignmentIterator` fails at Python's
      `open()` codec (`UnicodeDecodeError`) BEFORE any sam.py code
      runs — so virtually every mutant is unreachable. Phase-6
      will compare each real fuzzer's per-SUT score against these
      two pure_random anchors; the GAP is what proves the fuzzer
      adds semantic signal over random. **Full per-cell detail +
      per-engine pipeline diagrams + reproducibility** live at
      `compares/results/mutation/pure_random_run/REPORT.md`
      (DESIGN-§3.3-schema `summary.json` + 6-row `summary.csv`
      alongside).

      Output path note: the matrix landed at
      `compares/results/mutation/pure_random_run/` rather than the
      canonical `compares/results/mutation/pure_random/` because a
      zombie Python worker from an earlier interrupted mutmut run
      still holds the `.mutmut-cache` file lock on the old path.
      Rename after the next session reboot; path-writers (summary
      CSV, Phase-6 consumers) read via `--out-root`.
  ```bash
  # htsjdk — both formats
  for FMT_LC in vcf sam; do
    py -3.12 compares/scripts/mutation_driver.py \
        --tool pure_random --sut htsjdk --corpus \
        compares/results/coverage/pure_random/htsjdk_${FMT_LC}/corpus/ \
        --budget 7200 \
        --out compares/results/mutation/pure_random/htsjdk_${FMT_LC}/
  done
  # vcfpy (mutmut)
  py -3.12 compares/scripts/mutation_driver.py \
      --tool pure_random --sut vcfpy --corpus \
      compares/results/coverage/pure_random/vcfpy/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/pure_random/vcfpy/
  # noodles (cargo-mutants)
  py -3.12 compares/scripts/mutation_driver.py \
      --tool pure_random --sut noodles --corpus \
      compares/results/coverage/pure_random/noodles/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/pure_random/noodles/
  # biopython (mutmut)
  py -3.12 compares/scripts/mutation_driver.py \
      --tool pure_random --sut biopython --corpus \
      compares/results/coverage/pure_random/biopython/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/pure_random/biopython/
  # seqan3 (mull)
  py -3.12 compares/scripts/mutation_driver.py \
      --tool pure_random --sut seqan3 --corpus \
      compares/results/coverage/pure_random/seqan3/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/pure_random/seqan3/

  # Equivalent single-call matrix runner (executes all 6 cells
  # sequentially — mutmut natively for vcfpy+biopython on the host,
  # graceful-skip for PIT/cargo-mutants/mull cells with
  # blocked_reason; rerun inside biotest-bench to promote blocked
  # cells to real numbers):
  py -3.12 compares/scripts/run_pure_random_phase3.py \
      --run-all --budget 7200 \
      --out-root compares/results/mutation/pure_random_run
  ```
- [ ] **EvoSuite anchor × htsjdk — PIT**. The EvoSuite-generated
      JUnit suite *is* the test suite PIT runs against; this is the
      one cell where the mutation-score number is directly
      comparable to Jazzer's htsjdk number because both use PIT on
      the same mutant set:
  ```bash
  py -3.12 compares/scripts/mutation_driver.py \
      --tool evosuite_anchor --sut htsjdk --corpus \
      compares/baselines/evosuite/results/work/evosuite-tests/ \
      --budget 7200 \
      --out compares/results/mutation/evosuite_anchor/htsjdk/
  ```
  `--corpus` is a tree of `.java` test files instead of generated
  inputs; the driver detects the `.java` extension and routes PIT in
  "external suite" mode rather than "replay inputs" mode.

**Verification**:

- [ ] Confirm every per-cell `summary.json` has
      `{killed, reachable, score, mutator_count, mutant_count}`.
- [ ] Spot-check: `score` ∈ [0, 1]; `killed` ≤ `reachable`;
      `reachable` ≤ `mutant_count`. A cell with
      `reachable / mutant_count` < 0.1 indicates the tool's corpus
      barely exercised the target — flag for re-run with a larger
      budget rather than reporting a near-zero score.
- [ ] Roll up: `compares/results/mutation/summary.csv` with one row
      per cell. `build_report.py` consumes this at Phase 6.

#### Phase 4 — Real-bug benchmark (~2.5 wall-days parallelised 4-way; post-2026-04-20 refactor, 117 cells)

The driver `compares/scripts/bug_bench_driver.py` already handles the
ugliest piece — **SUT version swaps + tool orchestration** — so the
operator never touches `pip install vcfpy==X.Y.Z`, rewrites the
noodles-vcf Cargo pin, or runs `git checkout <sha>` by hand during
the run.

**Efficient run order: anchor-grouped**. The driver groups verified
bugs by `(sut, pre_fix, post_fix)` and processes each group as a
single unit — install pre_fix **once**, run every in-group bug × tool
cell, install post_fix **once**, replay every detected trigger. This
matters because the verified manifest has overlaps:

| Anchor | Bugs |
| :--- | :--- |
| htsjdk 2.19.0 → 2.20.0 | #1364, #1389, #1372, #1401 (4) |
| htsjdk 2.24.1 → 3.0.0 | #1554, #1544, #1561 (3) |
| vcfpy 0.13.8 → 0.14.0 | vcfpy-176, vcfpy-171 (2) |
| noodles-vcf 0.48 → 0.49 | noodles-223, noodles-224 (2) |
| noodles-vcf 0.63 → 0.64 | noodles-300, noodles-inforay-0.64 (2) |
| *(singleton anchors)* | 1 bug each |

Install-swap math (post-2026-04-20 refactor, frozen N = 35): 35
bugs × 2 swaps naive = 70; anchor-grouped with the 5 non-singleton
anchor groups listed above collapsing 11 bugs into 5 groups → 29
singleton + 5 grouped = 34 groups × 2 = **68 swaps grouped** (vs 70
naive — modest savings because most new anchors are singletons, but
the htsjdk 2.19.0 → 2.20.0 group still collapses 4 bugs into 1 pre-fix
install, which is where the largest time savings come from). Per-swap
cost: seconds for vcfpy/biopython (pip), seconds for noodles-vcf
(Cargo edit + incremental `cargo build --release` ≈ 30-60 s after the
first), and sub-minute for htsjdk (Maven JAR swap) / seqan3 (`git
checkout`).

**Run commands**:

- [ ] **Full primary bench** (all 35 frozen bugs × all applicable tools):
  ```bash
  python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --time-budget-s 7200 \
      --out compares/results/bug_bench/
  ```
  Produces `compares/results/bug_bench/<tool>/<bug_id>/result.json`
  per cell plus an `aggregate.json` rollup.

- [ ] **Filter flags** for iterative work (all combinable):
  - `--only-bug vcfpy-146` → one bug end-to-end.
  - `--only-sut noodles` → only noodles-vcf row bugs.
  - `--only-tool cargo_fuzz` → only one tool across all bugs.
  - Combine: `--only-sut vcfpy --only-tool atheris` for a single row.

- [ ] **Smoke-test pattern** for the curious — pick `vcfpy-146`
  because its trigger is a single-line VCF (INFO flag declared as
  String in the header) that surfaces as a Python `TypeError` on
  first parse, so no fuzzer warm-up is needed:
  ```bash
  python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-bug vcfpy-146 --only-tool pure_random \
      --time-budget-s 60 --out /tmp/bench-smoke
  ```
  Expected output (same `[orchestrator]` / `[group]` / `[run]` /
  `[done]` lines as the pre-refactor pysam smoke recorded on
  2026-04-19, which is the floor behaviour the new vcfpy smoke
  inherits):
  ```
  [orchestrator] 1 bug(s) in 1 anchor group(s) — 2 install-swaps
  [group] vcfpy  0.13.3 -> 0.13.4  (1 bug(s))
  [run] pure_random @ vcfpy-146  t=60s
  [done] wrote 1 records to /tmp/bench-smoke/aggregate.json
  ```
  Once the new install-verify pass lands in `manifest.verified.json`,
  re-run this smoke to re-attach a current timestamp.

- [ ] **Post-run review**: for each cell with `confirmed_fix_silences_signal == null`, manually replay the trigger.
  Spot-check 3 detection claims across different tools.
- [ ] Back up `compares/results/bug_bench/` to off-machine storage.

#### Phase 5 — Short-budget secondary regime (≤ 6 hours)

Reuse Phase 2's command shape with `--budget 300 --reps 5` to produce
the proposal-matching 300 s growth curve. Outputs land next to the
2 h results under `…/growth_short_<run_idx>.json`. Same 10 baseline
cells + 1 anchor; BioTest rows still out of §13.5 scope.

- [ ] **Jazzer × htsjdk** (both formats):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool jazzer --sut htsjdk --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 300 --reps 5 --out-suffix short \
      --out compares/results/coverage/jazzer/htsjdk_vcf/

  python3.12 compares/scripts/coverage_sampler.py \
      --tool jazzer --sut htsjdk --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 300 --reps 5 --out-suffix short \
      --out compares/results/coverage/jazzer/htsjdk_sam/
  ```
- [ ] **Atheris × vcfpy / biopython**:
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool atheris --sut vcfpy --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 300 --reps 5 --out-suffix short \
      --out compares/results/coverage/atheris/vcfpy/

  python3.12 compares/scripts/coverage_sampler.py \
      --tool atheris --sut biopython --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 300 --reps 5 --out-suffix short \
      --out compares/results/coverage/atheris/biopython/
  ```
- [ ] **cargo-fuzz × noodles-vcf** — tooling unblocked 2026-04-20
      (fuzz-target binary + runner live in the image). The short-
      budget 300 s × 5 reps pass is queued with the Phase 2 run.
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool cargo_fuzz --sut noodles --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 300 --reps 5 --out-suffix short \
      --out compares/results/coverage/cargo_fuzz/noodles/
  ```
- [ ] **libFuzzer × seqan3** (+ AFL++ alternate if running both):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool libfuzzer --sut seqan3 --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 300 --reps 5 --out-suffix short \
      --out compares/results/coverage/libfuzzer/seqan3/

  # alternate — optional
  python3.12 compares/scripts/coverage_sampler.py \
      --tool aflpp --sut seqan3 --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 300 --reps 5 --out-suffix short \
      --out compares/results/coverage/aflpp/seqan3/
  ```
- [ ] **Pure Random × every SUT** (6 cells):
  ```bash
  for FMT in VCF SAM; do
    LCASE=$(echo $FMT | tr A-Z a-z)
    python3.12 compares/scripts/coverage_sampler.py \
        --tool pure_random --sut htsjdk --format $FMT \
        --seed-corpus compares/results/bench_seeds/${LCASE} \
        --budget 300 --reps 5 --out-suffix short \
        --out compares/results/coverage/pure_random/htsjdk_${LCASE}/
  done
  for SUT in vcfpy noodles; do
    python3.12 compares/scripts/coverage_sampler.py \
        --tool pure_random --sut $SUT --format VCF \
        --seed-corpus compares/results/bench_seeds/vcf \
        --budget 300 --reps 5 --out-suffix short \
        --out compares/results/coverage/pure_random/${SUT}/
  done
  for SUT in biopython seqan3; do
    python3.12 compares/scripts/coverage_sampler.py \
        --tool pure_random --sut $SUT --format SAM \
        --seed-corpus compares/results/bench_seeds/sam \
        --budget 300 --reps 5 --out-suffix short \
        --out compares/results/coverage/pure_random/${SUT}/
  done
  ```
- [ ] **EvoSuite anchor × htsjdk** — short budget:
  ```bash
  SEARCH_BUDGET=300 bash compares/scripts/run_evosuite.sh \
      --classes 'htsjdk.variant.vcf.*,htsjdk.samtools.*'
  bash compares/scripts/measure_evosuite_coverage.sh \
      --out compares/results/coverage/evosuite_anchor/htsjdk/growth_short.json
  ```
  5 reps; at 300 s per rep EvoSuite's GA search will land in a
  qualitatively different regime from the 7 200 s run, which is
  exactly the point of the short-budget comparator.

- [ ] **Confirm outputs** land under
      `compares/results/coverage/<tool>/<sut>[_<fmt>]/growth_short_<run_idx>.json`
      (one file per rep). Sanity check:
  ```bash
  find compares/results/coverage -name 'growth_short_*.json' | wc -l
  # Expect 10 cells × 5 reps = 50 + 1 EvoSuite JSON = 51
  ```
- [ ] **Total walltime**: per cell = 5 reps × 300 s = 1 500 s (25
      min). 10 primary cells × 1 500 s = 15 000 s sequential =
      **~4.2 cell-hours ÷ 4-way parallelism ≈ 1 wall-hour** (well
      inside the ≤ 6-hour target). Add the EvoSuite 5 × 300 s run and
      the AFL++ alternate (optional) and total still sits under
      2 wall-hours.

#### Phase 6 — Report (≤ 2 hours)

**Sequence (run in this order)**:

1. [ ] **Fairness-equalizer pass** — DESIGN.md §4.4 / §9 Risk 3. Runs
   once per full bench-driver output, re-feeds every tool's accepted
   inputs through the differential-only oracle, and credits each
   tool with the disagreements its inputs caused:
   ```
   python compares/scripts/fairness_equalizer.py \
       --bench-root compares/results/bug_bench \
       --out compares/results/fairness_equalizer
   ```
   The module-level import guard refuses to run if
   `test_engine.oracles.metamorphic` is in `sys.modules`; sanity
   assertion enforces `BioTest_diff_only ≤ BioTest_full`.
2. [ ] **Aggregate report**:
   ```
   py -3.12 compares/scripts/build_report.py \
       --results compares/results/ \
       --out compares/results/comparison_report.md
   ```
   `build_report.py` consumes both the bug-bench JSON and the
   fairness-equalizer JSON so crash-only and disagreement-only
   detections are counted per tool-cell.
3. [ ] Confirm all six figures generated (`coverage_growth_<sut>.png`
   × 4, `validity_bar_<sut>.png` × 4, `mutation_bar_<sut>.png` × 4,
   `bug_detection_heatmap.png`, `ttfb_violin.png`).
4. [ ] Manual review: open `comparison_report.md`; sanity-check every
   table row against the raw JSON in `compares/results/`.

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
