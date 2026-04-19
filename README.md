<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Java-21-orange?logo=openjdk&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-29.1-blue?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-364%20passing-brightgreen?logo=pytest" />
  <img src="https://img.shields.io/badge/SUTs-6%20parsers-purple" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

```
  ____  _       _____         _
 | __ )(_) ___ |_   _|__  ___| |_
 |  _ \| |/ _ \  | |/ _ \/ __| __|
 | |_) | | (_) | | |  __/\__ \ |_
 |____/|_|\___/  |_|\___||___/\__|
```

# BioTest

**Automated Metamorphic & Differential Testing for Bioinformatics File Format Parsers**

BioTest mines test rules from the VCF/SAM specs, applies semantics-preserving
transforms to real files, and cross-executes them on multiple parsers
(HTSJDK, pysam, Biopython, SeqAn3, htslib CLI, reference). Disagreements
become bug reports backed by spec evidence.

---

## Pipeline at a Glance

```
Phase A  Spec Ingest     VCF/SAM .tex  →  ChromaDB vector store of testable rules
Phase B  MR Mining       LLM + RAG     →  Metamorphic Relations (transform + target)
Phase C  Cross-Execution apply(T, x)   →  run every parser, vote, diff, shrink
Phase D  Feedback Loop   coverage      →  Top-K blindspot tickets → next B round
```

| Phase | Module              | What it produces                                                             |
|:-----:|---------------------|------------------------------------------------------------------------------|
| A     | `spec_ingestor/`    | `data/chroma_db/` vector store + `data/parsed/*.json` testable rules         |
| B     | `mr_engine/`        | `data/mr_registry.json` (Enforced + Quarantine tiers)                        |
| C     | `test_engine/`      | Bug reports under `bug_reports/` + `data/det_report.json`                    |
| D     | `test_engine/feedback/` | `data/scc_report.json`, `data/feedback_state.json`, blindspot tickets    |

---

## Quick Start

```bash
# 1. Prerequisites
py -3.12 --version      # Python 3.12
java -version           # Java 21
docker --version        # Docker (needed for pysam on Windows)

# 2. Install
py -3.12 -m pip install -r requirements.txt
py -3.12 harnesses/pysam/build_docker.py      # Build pysam container

# 3. Configure LLM (one of: Groq, OpenAI, Anthropic, Google, DeepSeek, Ollama)
#    Set LLM_MODEL=... and the corresponding *_API_KEY in .env

# 4. Populate Tier-2 seeds (optional, ~30 curated real-world files)
py -3.12 seeds/fetch_real_world.py

# 5. Run
py -3.12 biotest.py                       # Full A → B → C
py -3.12 biotest.py --phase C             # Only Phase C (re-use registry)
py -3.12 biotest.py --phase A,B,C,D       # Include feedback loop
py -3.12 biotest.py --dry-run             # Validate config only
```

Tests:
```bash
py -3.12 -m pytest tests/ --ignore=tests/test_golden_retrieval.py
```

---

## Adding a New Parser (SUT)

Parsers speak different languages and expose different APIs, so each one
needs a thin **Harness** that exposes a uniform contract:

> **parse contract.** Given a file path and a format (`VCF` or `SAM`),
> return a JSON object matching `test_engine/canonical/schema.py`. Exit 0 on
> success, non-zero on error.

### Step 1 — write the Harness

| SUT language  | What to write                                      | Example                                |
|:-------------:|----------------------------------------------------|----------------------------------------|
| Java          | `.java` → fat JAR                                  | `harnesses/java/BioTestHarness.java`   |
| Python (pip)  | `ParserRunner` subclass (in-process)               | `test_engine/runners/biopython_runner.py` |
| Python (Docker) | CLI script + Dockerfile                          | `harnesses/pysam/`                     |
| C / C++       | Binary that reads a file, prints canonical JSON    | `harnesses/cpp/biotest_harness.cpp`    |
| Rust / Go / … | Same as C++: a process contract, JSON on stdout    | (follow the C++ pattern)               |

> **Coordinate trap.** Canonical JSON uses 1-based positions. If your SUT is
> 0-based internally (pysam, SeqAn3, Biopython), **add +1** to POS/PNEXT in
> the harness before printing.

### Step 2 — register it in `biotest_config.yaml`

```yaml
phase_c:
  suts:
    - name: my_parser
      language: Rust
      enabled: true
      adapter: harnesses/rust/my_parser   # path to binary
      timeout_s: 60
```

### Step 3 — add a runner class (if subprocess-based)

Create `test_engine/runners/my_parser_runner.py` by mirroring
`htsjdk_runner.py` (Java) or `seqan3_runner.py` (C++). Python libraries
follow `biopython_runner.py`.

### Step 4 — tell the coverage collector what "in scope" means for *your* SUT

**This step is not optional.** Without it the framework either measures
no coverage for your SUT, or pollutes the denominator with every package
your SUT's library ships (CRAM, BAM index, legacy codecs, JEXL filters,
etc. in the case of htsjdk). A VCF run on a new SUT should measure
coverage on that SUT's VCF code *only*.

Add a per-SUT block under `coverage.target_filters.<FORMAT>.<sut_name>`:

```yaml
coverage:
  target_filters:
    VCF:
      my_parser:               # must match the SUT name from Step 2
        - my_parser/vcf        # Python package / Java pkg / C++ dir substring
        # optional: keep it narrow
        - my_parser/model::VCF,Variant,-*JEXL*
    SAM:
      my_parser:
        - my_parser/sam
```

Pattern syntax (each entry):

| Pattern | Meaning |
|:--------|:--------|
| `pkg/path` | whole package / source directory, all files |
| `pkg/path::VCF,Variant` | package + include-list: only files starting with `VCF` or `Variant` |
| `pkg/path::-JEXL,-Jexl` | package + exclude-list: everything EXCEPT files starting with those prefixes |
| `pkg/path::*SV*,-BCF2*` | wildcards: `*Foo*` = contains "Foo"; `-BCF2*` = exclude files starting with BCF2 |

**Rule of thumb**: include your SUT's parse + data-model + writer
packages. Exclude binary codecs, alternative format backends, or
filter-expression engines you aren't testing. See the existing
`htsjdk` / `pysam` / `biopython` / `seqan3` entries in
`biotest_config.yaml` for working examples.

### Step 5 — run

```bash
py -3.12 biotest.py --phase C
```

The new SUT joins both the metamorphic and differential oracles
automatically, and its coverage is measured against the scope YOU
specified in Step 4.

---

## Adding **Write** Support to a SUT

The framework exposes a single format-agnostic transform — `sut_write_roundtrip`
— that parses a file with the primary SUT, re-serializes it through that same
SUT's public writer, and feeds the rewritten text back into the oracle
pipeline. Per Chen, Kuo, Liu, Tse (2018) §3.2 this is the canonical
`parse(write(parse(x))) == parse(x)` metamorphic relation.

If your SUT exposes a writer (VCF or SAM or both), you opt in by implementing
**two things** on your `ParserRunner` subclass:

```python
# test_engine/runners/my_parser_runner.py
class MyParserRunner(ParserRunner):
    supports_write_roundtrip: bool = True        # ← 1. opt-in flag

    def run_write_roundtrip(                      # ← 2. writer contract
        self,
        input_path: Path,
        format_type: str = "VCF",
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        # Call your parser's public writer.
        # Handle fmt = "VCF" and/or "SAM" — return an "ineligible" RunnerResult
        # for formats your SUT can't write (framework treats that as a no-op).
        rewritten_text: str = ...
        return RunnerResult(
            success=True,
            canonical_json={"rewritten_text": rewritten_text},
            parser_name=self.name,
            format_type=format_type.upper(),
        )
```

That's the entire contract. You do **not** register a new transform, add a
new Hypothesis strategy, or edit the dispatch plumbing — the framework
already handles all of that for any runner whose `supports_write_roundtrip`
is True.

### How the pieces connect

```
Phase B menu  →  sut_write_roundtrip (format: VCF/SAM)
                       │
Phase C run   →  strategy picks seed from the MR's format corpus
                       │
                 orchestrator resolves primary SUT's runner
                       │
                 dispatch  ──►  runner.run_write_roundtrip(path, fmt)
                       │
                 rewritten text  ──►  normal consensus / metamorphic oracle
```

The `format_type` argument tells your runner whether the seed is VCF or SAM;
the orchestrator feeds it from the MR's declared scope. One transform serves
both formats — no per-format duplicates to maintain.

### Reference implementations

| SUT         | Writer API                                                     | Source                                         |
|:------------|:---------------------------------------------------------------|:-----------------------------------------------|
| **htsjdk**  | `VCFWriter` + `SAMFileWriterFactory`                           | `harnesses/java/BioTestHarness.java`           |
| **pysam**   | `pysam.VariantFile("w")` + `pysam.AlignmentFile("wh")`         | `harnesses/pysam/pysam_harness.py`             |
| **htslib**  | `bcftools view` / `samtools view` (already a round-trip)       | `test_engine/runners/htslib_runner.py`         |

### Opt-out is silent

If your SUT has no writer, leave `supports_write_roundtrip = False` (the
default). The framework's runtime-capability filter hides
`sut_write_roundtrip` from the Phase B menu when no primary SUT supports it,
so no MR will ever target your read-only runner for write testing.

---

## The 25 Atomic Transforms

Each transform either preserves biological semantics (transforms 1–20) or
deliberately violates a specific spec rule to exercise rejection paths
(transforms 21–25). All are grounded in published literature — see
`documents/Flow.md` for full citations.

### VCF (15)

| # | Transform                         | Scope     | Purpose                                                       |
|:-:|:----------------------------------|:---------:|:--------------------------------------------------------------|
| 1 | `shuffle_meta_lines`              | Header    | Shuffle `##` lines (keep `##fileformat` first)                |
| 2 | `permute_structured_kv_order`     | Header    | Reorder `key=value` inside `##INFO=<…>`                       |
| 3–6 | `choose_permutation` + `permute_ALT` + `remap_GT` + `permute_Number_A_R_fields` | Record | **Compound**: reorder ALT alleles, update GT and Number=A/R |
| 7 | `permute_sample_columns`          | File      | Shuffle sample columns across header + data                   |
| 8 | `shuffle_info_field_kv`           | Record    | Shuffle INFO `k=v` pairs in each record                       |
| 9 | `inject_equivalent_missing_values`| Record    | Add a declared-but-missing FORMAT field                       |
| 10| `trim_common_affixes`             | Record    | Trim shared REF/ALT prefix/suffix (Tan 2015)                  |
| 11| `left_align_indel`                | Record    | Left-shift indels in homopolymer runs (Tan 2015)              |
| 12| `split_multi_allelic`             | Record    | Split multi-ALT into per-ALT records (bcftools norm)          |
| 13| `vcf_bcf_round_trip`              | File      | VCF → BCF → VCF via pysam                                     |
| 14| `permute_bcf_header_dictionary`   | File      | Shuffle BCF dict order, round-trip                            |
| 15| `permute_csq_annotations`         | Record    | Permute CSQ/ANN record order (VEP/SnpEff)                     |

### SAM (4)

| #  | Transform                           | Scope   | Purpose                                               |
|:--:|:------------------------------------|:-------:|:------------------------------------------------------|
| 16 | `permute_optional_tag_fields`       | Record  | Shuffle optional `TAG:TYPE:VALUE` fields              |
| 17 | `split_or_merge_adjacent_cigar_ops` | Record  | `10M` ↔ `4M6M` (Z3-guarded for CIGAR/SEQ length)      |
| 18 | `reorder_header_records`            | Header  | Shuffle `@SQ`/`@RG` (keep `@HD` first)                |
| 19 | `toggle_cigar_hard_soft_clipping`   | Record  | Convert `H` ↔ `S` with SEQ/QUAL sync                  |

### VCF + SAM (1)

| #  | Transform                | Scope | Purpose                                                                |
|:--:|:-------------------------|:-----:|:-----------------------------------------------------------------------|
| 20 | `sut_write_roundtrip`    | File  | `parse(write(parse(x))) == parse(x)` — runner picks VCF or SAM writer |

### Malformed-input mutators (5) — REJECTION_INVARIANCE

These deliberately break a CRITICAL spec rule. Paired with the
**error-consensus oracle** (accept / silent_skip / reject / crash voting) to
expose parsers that silently tolerate spec violations.

| #  | Transform                              | Fmt  | Spec rule broken                                               |
|:--:|:---------------------------------------|:----:|:---------------------------------------------------------------|
| 21 | `violate_info_number_a_cardinality`    | VCF  | INFO `Number=A` values must equal `len(ALT)`                   |
| 22 | `violate_required_fixed_columns`       | VCF  | First 8 columns are mandatory                                  |
| 23 | `violate_fileformat_first_line`        | VCF  | `##fileformat` must be line 1                                  |
| 24 | `violate_gt_index_bounds`              | VCF  | GT indices must satisfy `0 ≤ idx ≤ len(ALT)`                   |
| 25 | `violate_cigar_seq_length`             | SAM  | `sum(query-consuming CIGAR ops) == len(SEQ)`                   |

---

## How the framework keeps coverage climbing

MR-only testing naturally ceilings at ~25–40% line coverage on file-format
parsers (Liyanage & Böhme, ICSE 2023; Nguyen et al., Fuzzing Workshop 2023;
Chen & Kuo, ACM CSUR 2018). Above that band you have to widen the test
paradigm — the framework does so via five zero-user-cost levers, each
backed by published research:

| Lever | What it does | Cite | Where |
|:-----:|:-------------|:-----|:------|
| **Seed synthesis** (Rank 1) | Each Phase D iteration asks the LLM for raw VCF/SAM files targeting uncovered source lines; validated candidates land as `seeds/vcf/synthetic_iter*_*.vcf` | SeedMind arXiv:2411.18143; SeedAIchemy arXiv:2511.12448; TitanFuzz ISSTA'23; Fuzz4All ICSE'24 | `mr_engine/agent/seed_synthesizer.py` |
| **htslib corpus** (Rank 2) | `seeds/fetch_real_world.py` pulls upstream htslib `test/` files — BCF/CRAM edge cases, Unicode, CIGAR bounds | (data) | `seeds/fetch_real_world.py` |
| **Malformed MRs** (Rank 3) | 5 spec-rule-targeted mutators + `error_consensus` oracle exercise parser rejection branches | Gmutator TOSEM'25 | `mr_engine/transforms/malformed.py`, `test_engine/oracles/error_consensus.py` |
| **`hypothesis.target()`** (Rank 4) | `divergence` + `seed_size` scalar objectives steer Hypothesis toward examples that cause more consensus-disagreements | Hypothesis docs (MacIver, Hatfield-Dodds) | `test_engine/orchestrator.py::_run_mr_with_hypothesis` |
| **API-query MRs** (Rank 5) | `P(parse(x)) == P(parse(T(x)))` — runtime reflection (Java + Python; `libclang` / `rustdoc` for C/C++/Rust templates) discovers the SUT's public scalar query methods; LLM mines MRs against them; `query_consensus` oracle compares scalar results across voters | MR-Scout TOSEM'24 (arXiv:2304.07548); MeMo JSS'21; Chen-Kuo-Liu-Tse 2018 §3.2 | `test_engine/runners/introspection.py`, `test_engine/oracles/query_consensus.py`, `mr_engine/transforms/query.py` |

Configured under `feedback_control.seed_synthesis` and `phase_b.themes`
in `biotest_config.yaml`. Realistic ceiling with all five active:
**~52–58% line coverage on htsjdk/VCF**, at the edge of the ~60% hard
ceiling for automated MR/fuzz testing without per-SUT hand-written
drivers. See `documents/Flow.md` for the full Phase B + C + D writeup
including the API-query oracle (§5.5) and citation chain.

---

## Seed Corpus

Two tiers:

- **Tier-1 (committed, ~6 files)**: hand-crafted minimal examples under
  `seeds/vcf/` and `seeds/sam/` — enough for smoke tests.
- **Tier-2 (gitignored, ~30 files)**: curated real-world seeds from htsjdk,
  bcftools, hts-specs, GATK. Pull with `py -3.12 seeds/fetch_real_world.py`.
  Full provenance + diversity axes in `seeds/SOURCES.md`. Per-file cap 500 KB.

Phase D preflight requires ≥ 15 VCF seeds.

---

## Configuration (`biotest_config.yaml`)

```yaml
phase_a:
  specs:
    - { file: VCFv4.5.tex, format: VCF, version: "4.5" }
    - { file: SAMv1.tex,   format: SAM, version: "1.6" }

phase_b:
  formats: [VCF]
  themes:  [ordering_invariance]
  llm:
    model: deepseek-chat     # also: groq/*, gpt-4o, gemini-*, claude-*, ollama/*

phase_c:
  format_filter: VCF
  suts:
    - { name: htsjdk,    adapter: harnesses/java/build/libs/biotest-harness-all.jar }
    - { name: biopython }
    - { name: seqan3,    adapter: harnesses/cpp/build/biotest_harness.exe }
    - { name: pysam,     coverage_dir: coverage_artifacts/pysam }
    - { name: htslib }    # gold-standard tie-breaker

feedback_control:
  enabled: true
  max_iterations: 5
  target_scc_percent: 95.0
  primary_target: htsjdk
  max_rules_per_iteration: 5      # Top-K blindspot window

coverage:
  enabled: true
  target_filters:
    VCF: [htsjdk/variant/vcf, htsjdk/variant/variantcontext/writer, pysam]
    SAM: [htsjdk/samtools,    Bio/Align/sam, seqan3/io/sam_file, pysam]
```

---

## Dual Oracle System

Two complementary oracles, layered on **majority-voting consensus**:

### Oracle 1 — Metamorphic (per-parser)

```
semantic( parse(x) )  ==  semantic( parse(T(x)) )
```

Each per-parser outcome is tagged with one `failure_cause`:

| `failure_cause`     | Meaning                                                      | Blamed               |
|:--------------------|:-------------------------------------------------------------|:---------------------|
| `against_consensus` | SUT disagreed with majority on BOTH `x` and `T(x)`           | the SUT              |
| `non_conformance`   | SUT matched consensus on one side, diverged on the other     | the SUT (not MR)     |
| `mr_invalid`        | htslib rejected `T(x)` or `consensus(x) ≠ consensus(T(x))`   | the MR → quarantine  |
| `inconclusive`      | No majority, no htslib tie-breaker                           | nobody               |
| `crash` / `timeout` | Parser died                                                  | usually the SUT      |

### Oracle 2 — Differential (consensus)

Group parser outputs by semantic equivalence; the bucket holding a strict
majority wins. On a 2-vs-2 tie, **htslib** (bcftools/samtools, the upstream
hts-specs reference) is the gold-standard tie-breaker. A SUT whose format
eligibility excludes the current file is silent — not a dissenting vote.

### DET Rate

```
DET Rate = tests with disagreement / total tests
```

Exported to `data/det_report.json`, tracked per MR and per parser pair.

---

## SUT Matrix

| SUT         | Language | VCF | SAM | Coverage          | Role                                   |
|:------------|:---------|:---:|:---:|:------------------|:---------------------------------------|
| **htsjdk**  | Java     | ✓   | ✓   | JaCoCo            | Regular voter                          |
| **pysam**   | Python   | ✓   | ✓   | coverage.py       | Regular voter                          |
| **biopython** | Python | —   | ✓   | coverage.py       | Regular voter (SAM)                    |
| **seqan3**  | C++      | —   | ✓   | gcovr/gcov        | Regular voter (SAM)                    |
| **htslib**  | CLI      | ✓   | ✓   | —                 | **Tie-breaker (gold standard)**        |
| reference   | Python   | ✓   | ✓   | —                 | Independent canonical impl.            |

Coordinate normalization (all handled inside harnesses):

| Parser      | SAM POS | VCF POS | Harness action       |
|:------------|:-------:|:-------:|:---------------------|
| htsjdk      | 1-based | 1-based | —                    |
| pysam       | 0-based | 0-based | **+1** for both      |
| Biopython   | 0-based | n/a     | **+1**               |
| SeqAn3      | 0-based | n/a     | **+1**               |

---

## Phase D Essentials

Phase D wraps B and C into an iterative loop driven by code coverage on the
**primary target** SUT.

```
for iteration in range(max_iterations):
    Phase B   mine MRs (with Top-K blindspot ticket from previous round)
    Phase C   execute  →  consensus + metamorphic + differential
              ├─ SCC computed with the 良民证 rule (any parser's endorsement vetoes demotion)
              ├─ coverage collected from the primary target only
              ├─ uncovered source slices extracted per rule
              ├─ rule_attempts tracker updated (failure_count, exponential cooldown)
              └─ quarantine auto-demotion when NO parser endorsed
    check 5 termination conditions: timeout / SCC target / budget / catastrophic demote / plateau
```

### Prioritized Blindspot Queue

Uncovered rules are scored by
`(format_match, failure_count, −complexity, −proximity, severity, chunk_id)`
and only the Top K (default 5) land in the LLM prompt each iteration.
Covered rules are wiped; shown-but-still-uncovered rules enter exponential
cooldown (1 → 2 → 4 → 4 iterations). State at `data/rule_attempts.json`.

Operator log per iteration:
```
Total Blindspots: 312 | Injecting Top 5 into this ticket | 307 remaining (2 cooling down).
```

### Runtime-Gated Transform Menu

The LLM only sees transforms whose preconditions the current runtime can
satisfy. `sut_write_roundtrip` is hidden from the menu unless at least one
enabled SUT declares `supports_write_roundtrip = True`, so the LLM never
picks a writer MR it would have to skip at Phase C.

---

## Project Layout (abridged)

```
biotest.py                         Grand orchestrator + Rich UI
biotest_config.yaml                Pipeline configuration
spec_ingestor/                     Phase A
mr_engine/                         Phase B (agent + transforms + DSL + registry)
  transforms/{vcf,sam}.py          20 atomic transforms + @register_transform
test_engine/                       Phase C (oracles, runners, generators, triage)
  runners/{base,htsjdk,pysam,biopython,seqan3,htslib,reference}_runner.py
  generators/{dispatch,strategy_router,vcf_strategies,sam_strategies}.py
  canonical/{schema,vcf_normalizer,sam_normalizer}.py
  oracles/{metamorphic,differential,deep_equal}.py
  feedback/{scc_tracker,loop_controller,coverage_collector,blindspot_builder}.py
harnesses/java/BioTestHarness.java htsjdk (VCF + SAM, parse + write_roundtrip)
harnesses/pysam/pysam_harness.py   pysam  (VCF + SAM, parse + write_roundtrip)
harnesses/cpp/biotest_harness.cpp  SeqAn3 (SAM parse)
seeds/vcf/, seeds/sam/             Tier-1 committed seeds
tests/                             pytest suite
documents/Flow.md                  full architecture for Phases A/B/C/D
```

---

## License

MIT
