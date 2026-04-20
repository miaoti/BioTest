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

Different tool classes emit different native signals. We translate each into a uniform "bug detected" predicate so scores are comparable.

| Tool class | Native signal | How it becomes a "detection" |
| :--- | :--- | :--- |
| BioTest | Metamorphic violation OR consensus disagreement | Existing `test_engine/oracles/differential.py` + `metamorphic.py` |
| Jazzer / Atheris / libFuzzer / cargo-fuzz | Crash, sanitizer abort, uncaught exception | Each fuzzer's native `crashes/` / `artifacts/` output directory |
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

A tool "detects" a bug iff (a) at least one input it generated triggers the detection criterion on the pre-fix SUT AND (b) the same input does not trigger on the post-fix SUT. Condition (b) is essential — without it, any non-deterministic disagreement would score as a detection.

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

#### 13.2.7 cargo-fuzz (Rust baseline, noodles-vcf) — **wired 2026-04-20; one-time build pending**

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

- [ ] **Build cargo-fuzz target**:
  ```bash
  cd compares/harnesses/cargo_fuzz
  cargo fuzz build noodles_vcf_target --release
  ```
  Expected artefact at
  `compares/harnesses/cargo_fuzz/fuzz/target/x86_64-unknown-linux-gnu/release/noodles_vcf_target`
  (~3-5 MB, libFuzzer-instrumented). Sibling paths
  `target/release/noodles_vcf_target` and
  `fuzz/target/release/noodles_vcf_target` are also discovered by
  the adapter's `_find_binary` helper.
- [ ] **Smoke test (60 s)**:
  ```bash
  python3.12 compares/scripts/tool_adapters/run_cargo_fuzz.py \
    --sut noodles --seed-corpus compares/results/bench_seeds/vcf \
    --out-dir /tmp/cargo-fuzz-smoke --time-budget-s 60 --format VCF
  ```
  Acceptance: `exit=0` (no crashes) or `exit=77` (libFuzzer signal
  raised → bug candidate surfaced). Either outcome means the fuzzer
  is driving noodles-vcf correctly.

Until the one-time build runs, the adapter returns a clean
`FileNotFoundError` per (tool, bug) cell and the rest of the bench
(htsjdk + vcfpy + biopython + seqan3 rows) continues. Nothing in the
bench is blocked on this step; operators can run htsjdk / vcfpy
today and bring noodles online at any point without re-running the
earlier rows.

**Known build notes** (to populate as `run_cargo_fuzz.py` is
smoke-tested):

| Symptom | Expected cause | Expected fix |
| :--- | :--- | :--- |
| `cargo fuzz build` can't find target | Harness crate missing `[[bin]]` entry for fuzz target | Already authored at `fuzz/fuzz_targets/noodles_vcf_target.rs`; confirm `fuzz/Cargo.toml` has `[[bin]] name = "noodles_vcf_target"` |
| Coverage build fails with "cannot link libFuzzer" | LLVM runtime not installed for target toolchain | `rustup component add llvm-tools-preview` |
| Coverage JSON is empty | Profile directory not collecting `.profraw` files | Set `LLVM_PROFILE_FILE=/path/to/dir/%m-%p.profraw` before the run |

### §13.2 summary

| Tool | Install in image | Smoke test | Status |
| :--- | :---: | :--- | :--- |
| BioTest | ✓ | `--dry-run` exit 0 in <1 s; full Phase C deferred to long-budget runs | **verified** |
| Jazzer | ✓ | VCF exit 0 / 103 k runs; SAM found crash in 2 s | **verified** |
| Atheris | ✓ (3.11 venv) | pre-refactor: pysam 1.21 M runs, biopython found `UnboundLocalError`. Post-2026-04-20: vcfpy smoke needs re-run. | **verified (biopython); pending (vcfpy)** |
| **libFuzzer / seqan3** | ✓ (Clang 18 + patched seqan3) | exit 77 / 58 corpus / 1 crash in 30 s | **verified** (primary C++ fuzzer) |
| **AFL++ / seqan3** | ✓ (g++-12 + afl-g++) | exit 0 / 60 queue / 1 crash in 30 s | **verified** (alternate C++ fuzzer) |
| **cargo-fuzz / noodles-vcf** | ✓ (Rust stable + cargo-fuzz 0.12) | fuzz-target + smoke-test pending (§13.2.7) | **scaffolded 2026-04-20** |
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
- [ ] **cargo-mutants (Rust, noodles-vcf)** — scheduled 2026-04-20.
  Install via `cargo install cargo-mutants --locked`; runs as
  `cargo mutants --package noodles-vcf` against the harness crate
  (which pulls noodles-vcf transitively) or directly against a
  checkout of the noodles monorepo. Probe:
  ```bash
  /root/.cargo/bin/cargo mutants --version  # expect 25.x
  ```
  Scope: `cargo mutants --in-place --package noodles-vcf` restricts
  mutants to the `noodles-vcf` crate source (not the harness or
  other noodles subcrates). Expected runtime per-mutant is similar
  to mull (Rust builds a full crate per mutant but incremental
  caching keeps this ≤ 10s/mutant on modern hardware).

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
| **cargo-mutants install** | ◐ (scheduled; one `cargo install cargo-mutants --locked` at next Dockerfile refresh) | `/root/.cargo/bin/cargo-mutants` (25.x) |
| **vcfpy venv** (new) | ✓ (2026-04-20 — `make_venv vcfpy vcfpy vcfpy 0.14.0`) | `compares/results/sut-envs/vcfpy/` (0.14.0 baseline) |
| **noodles canonical-JSON harness** | ✓ | `harnesses/rust/noodles_harness/` (noodles-vcf 0.70 baseline pinned in `Cargo.toml`) |
| **cargo-fuzz target** (new) | ✓ source on disk; one-time `cargo fuzz build` pending | `compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs` + `fuzz/Cargo.toml` |
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

#### Phase 1 — Validity probe (≤ 1 hour per full sweep) — **probe promoted + smoke-tested 2026-04-20; per-cell runs deferred to post-Phase-2**

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
  Verified 2026-04-20 against all four smoke-test JSONs — every file
  carries the required 5 keys + 8 extended counters.

**Per-cell invocations** — **deferred until Phase 2 has produced
tool-generated corpora**. These commands point the promoted probe at
each tool's `coverage/<tool>/<sut>/corpus/` directory, which does not
exist until the 2 h × 3 rep coverage runs complete (Phase 2 below).
Each checkbox below stays `[ ]` until its Phase 2 corpus lands, at
which point the probe runs in seconds. The §13.2 smoke-test
directories under `/tmp/` are transient, so the ground-truth pre-flight
equivalent already ran on 2026-04-20 against
`compares/results/bench_seeds/` (see the smoke table above); that
confirms the probe itself works end-to-end.

- [ ] **Jazzer × htsjdk** (VCF + SAM — one cell, two format
      reparses):
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
- [ ] **Atheris × vcfpy** (VCF only — vcfpy has no SAM parser):
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/atheris/vcfpy/corpus \
      --sut vcfpy --format VCF \
      --out compares/results/validity/atheris/vcfpy/validity.json
  ```
- [ ] **Atheris × biopython** (SAM only):
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/atheris/biopython/corpus \
      --sut biopython --format SAM \
      --out compares/results/validity/atheris/biopython/validity.json
  ```
- [ ] **cargo-fuzz × noodles-vcf** (VCF only):
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/cargo_fuzz/noodles/corpus \
      --sut noodles --format VCF \
      --out compares/results/validity/cargo_fuzz/noodles/validity.json
  ```
- [ ] **libFuzzer × seqan3** (SAM only — seqan3 has no VCF parser):
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/libfuzzer/seqan3/corpus \
      --sut seqan3 --format SAM \
      --out compares/results/validity/libfuzzer/seqan3/validity.json
  ```
- [ ] **AFL++ × seqan3** (verified alternate on same harness; run
      only if libFuzzer regresses or a cross-fuzzer sanity check is
      wanted):
  ```bash
  python3.12 compares/scripts/validity_probe.py \
      --corpus compares/results/coverage/aflpp/seqan3/corpus \
      --sut seqan3 --format SAM \
      --out compares/results/validity/aflpp/seqan3/validity.json
  ```
- [ ] **Pure Random × every SUT** (6 probes; the floor baseline
      must land on the same grid as every real tool):
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

- [x] **Output-schema check** already verified on the four smoke-test
      JSONs (see the bulleted item above). Re-run the same one-liner
      after each per-cell invocation lands; no cell's JSON is ever
      accepted if it's missing one of the five required keys.
- [ ] **Record each cell's validity_ratio** into
      `compares/results/validity/summary.csv` for the final report.
      The smoke-test rollup at
      `compares/results/validity/smoke/summary.csv` is the template
      shape; the Phase-6 report consumer expects the same column
      layout.

#### Phase 2 — Coverage growth (~1 wall-day parallelised 4-way)

2 h × 3 reps per cell, coverage sampled at log ticks
`{1, 10, 60, 300, 1800, 7200}` seconds (§3.2). 10 baseline cells
(matrix — BioTest) + 1 EvoSuite anchor = **11 cells** covered by
this phase per the current §13.5 scope. Each cell produces three
`growth_<run_idx>.json` files so the final report plots 95% CI bands.

**Orchestrator**: `compares/scripts/coverage_sampler.py` (placeholder
to promote per §6 Phase 0). Expected signature — delegates to the
per-tool adapter under the hood:

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

- [ ] **Jazzer × htsjdk** (2 formats, run as separate cells so
      coverage attribution stays clean):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool jazzer --sut htsjdk --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/jazzer/htsjdk_vcf/

  python3.12 compares/scripts/coverage_sampler.py \
      --tool jazzer --sut htsjdk --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/jazzer/htsjdk_sam/
  ```
  JaCoCo collector produces `growth_<idx>.json` + `.exec` per rep.
- [ ] **Atheris × vcfpy** (VCF only):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool atheris --sut vcfpy --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/atheris/vcfpy/
  ```
  coverage.py collector traces the `vcfpy/` package tree. Atheris
  runs under `/opt/atheris-venv/bin/python` automatically.
- [ ] **Atheris × biopython** (SAM only):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool atheris --sut biopython --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/atheris/biopython/
  ```
  coverage.py collector scoped to `Bio/Align/sam.py`.
- [ ] **cargo-fuzz × noodles-vcf** (VCF only):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool cargo_fuzz --sut noodles --format VCF \
      --seed-corpus compares/results/bench_seeds/vcf \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/cargo_fuzz/noodles/
  ```
  `NoodlesCoverageCollector` runs `cargo llvm-cov report --json`
  against `/tmp/llvm-profile-*` collected during the fuzz run (set
  `LLVM_PROFILE_FILE` in the adapter env). **Pre-requisite**: one-time
  `cargo fuzz build noodles_vcf_target --release` (§13.2.7).
- [ ] **libFuzzer × seqan3** (SAM only):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool libfuzzer --sut seqan3 --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/libfuzzer/seqan3/
  ```
  gcovr collector scoped to `include/seqan3/io/sam_file/**`. The
  harness must be built with `--coverage` (primary libFuzzer path in
  the bench image already does this; see §13.2.4).
- [ ] **AFL++ × seqan3** (alternate; run only if cross-fuzzer
      corroboration is wanted, otherwise skip):
  ```bash
  python3.12 compares/scripts/coverage_sampler.py \
      --tool aflpp --sut seqan3 --format SAM \
      --seed-corpus compares/results/bench_seeds/sam \
      --budget 7200 --reps 3 \
      --out compares/results/coverage/aflpp/seqan3/
  ```
- [ ] **Pure Random × every SUT** (6 commands — floor baseline
      must span the full matrix for the 95% CI bands to be
      comparable):
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

**Orchestrator**: `compares/scripts/mutation_driver.py` (placeholder
to promote per §6 Phase 0). Expected signature:

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

- [ ] **Jazzer × htsjdk — PIT (Java)**:
  ```bash
  # VCF corpus
  py -3.12 compares/scripts/mutation_driver.py \
      --tool jazzer --sut htsjdk --corpus \
      compares/results/coverage/jazzer/htsjdk_vcf/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/jazzer/htsjdk_vcf/
  # SAM corpus
  py -3.12 compares/scripts/mutation_driver.py \
      --tool jazzer --sut htsjdk --corpus \
      compares/results/coverage/jazzer/htsjdk_sam/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/jazzer/htsjdk_sam/
  ```
  Mutant scope: `src/main/java/htsjdk/variant/vcf/**` +
  `src/main/java/htsjdk/samtools/**`. PIT under the hood; mutators =
  DEFAULT_GROUP (§3.3).
- [ ] **Atheris × vcfpy — mutmut (Python)**:
  ```bash
  py -3.12 compares/scripts/mutation_driver.py \
      --tool atheris --sut vcfpy --corpus \
      compares/results/coverage/atheris/vcfpy/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/atheris/vcfpy/
  ```
  Mutant scope: the `vcfpy/` package tree inside
  `compares/results/sut-envs/vcfpy/lib/python3.11/site-packages/`.
  The driver copies vcfpy to a temp dir, runs mutmut against it, and
  replays each tool corpus file.
- [ ] **Atheris × biopython — mutmut (Python)**:
  ```bash
  py -3.12 compares/scripts/mutation_driver.py \
      --tool atheris --sut biopython --corpus \
      compares/results/coverage/atheris/biopython/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/atheris/biopython/
  ```
  Mutant scope: `Bio/Align/sam.py` only (the SAM parser path;
  pairwise alignment mutants would be out of scope and inflate
  `reachable`).
- [ ] **cargo-fuzz × noodles-vcf — cargo-mutants (Rust)**:
  ```bash
  py -3.12 compares/scripts/mutation_driver.py \
      --tool cargo_fuzz --sut noodles --corpus \
      compares/results/coverage/cargo_fuzz/noodles/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/cargo_fuzz/noodles/
  ```
  Mutant scope: `cargo mutants --package noodles-vcf` restricts to
  the `noodles-vcf` crate. The driver invokes
  `/root/.cargo/bin/cargo-mutants` in a scratch checkout of the
  noodles monorepo; per-mutant rebuild is incremental (~10 s).
- [ ] **libFuzzer × seqan3 — mull (C++)**:
  ```bash
  py -3.12 compares/scripts/mutation_driver.py \
      --tool libfuzzer --sut seqan3 --corpus \
      compares/results/coverage/libfuzzer/seqan3/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/libfuzzer/seqan3/
  ```
  Mutant scope: `include/seqan3/io/sam_file/**`. Requires the
  Clang-18 + patched seqan3 IR build (§13.2.4); `mull-runner-18`
  operates on the IR emitted during that build.
- [ ] **AFL++ × seqan3 — mull (C++)** (alternate; run only if a
      cross-fuzzer corroboration is desired on the mutation score):
  ```bash
  py -3.12 compares/scripts/mutation_driver.py \
      --tool aflpp --sut seqan3 --corpus \
      compares/results/coverage/aflpp/seqan3/corpus/ \
      --budget 7200 \
      --out compares/results/mutation/aflpp/seqan3/
  ```
- [ ] **Pure Random × every SUT** (6 cells; one PIT + two mutmut +
      two mull-or-cargo-mutants calls. The floor-baseline's mutation
      score is the key comparator for the other tools):
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
- [ ] **cargo-fuzz × noodles-vcf**:
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
