<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Java-21-orange?logo=openjdk&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-29.1-blue?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-544%20passing-brightgreen?logo=pytest" />
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
java -version           # Java 21 (any recent LTS works)
docker --version        # Docker (pysam runs in Docker on Windows)
rustc --version         # Optional — only if you want the noodles-vcf SUT
g++ --version           # Optional — only if you want the seqan3 SAM SUT

# 2. Install Python deps + build the per-language harnesses
py -3.12 -m pip install -r requirements.txt
bash harnesses/java/build.sh                                         # htsjdk JAR (required for the htsjdk SUT)
py -3.12 harnesses/pysam/build_docker.py                              # pysam Docker image (required for the pysam SUT)
cargo build --release \
    --manifest-path harnesses/rust/noodles_harness/Cargo.toml         # noodles VCF SUT (optional)
g++ -std=c++20 -O2 harnesses/cpp/biotest_harness.cpp \
    -o harnesses/cpp/build/biotest_harness.exe                        # seqan3 SAM SUT (optional)

# 3. Configure the LLM — pick ONE provider, set 2 vars in .env.
#    Full provider matrix in "Switching the LLM provider" below.
cat > .env <<'EOF'
LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=sk-...
EOF

# 4. Populate Tier-2 seeds (optional, ~30 curated real-world files)
py -3.12 seeds/fetch_real_world.py

# 5. Run the pipeline
py -3.12 biotest.py --phase D             # Recommended: full pipeline + feedback loop
py -3.12 biotest.py                       # A → B → C only (no feedback loop)
py -3.12 biotest.py --phase C             # Re-execute Phase C (re-use existing MR registry)
py -3.12 biotest.py --dry-run             # Validate config and exit
```

Tests:
```bash
py -3.12 -m pytest tests/ --ignore=tests/test_golden_retrieval.py
```

After a run, results land here:

| Path                               | Contents                                                      |
|:-----------------------------------|:--------------------------------------------------------------|
| `bug_reports/`                     | One JSON per disagreement, with parser outputs + spec evidence |
| `data/det_report.json`             | DET rate per MR and per parser pair                            |
| `data/scc_report.json`             | Spec coverage trajectory per Phase D iteration                |
| `data/feedback_state.json`         | Phase D loop state (current iteration, plateau detection)      |
| `coverage_artifacts/`              | Per-language coverage data (jacoco / coverage.py / gcovr / llvm-cov) |

---

## Configuring Your Run

Two files steer the pipeline: `.env` (secrets + LLM choice) and
`biotest_config.yaml` (everything else). These are the knobs you'll
touch most often.

### Switching the LLM provider

The LLM is configured via two `.env` variables. Pick one row from the
matrix and you're done — no code changes:

| Provider        | `LLM_MODEL=`                                | API key var          | Notes                                              |
|:----------------|:--------------------------------------------|:---------------------|:---------------------------------------------------|
| DeepSeek        | `deepseek-chat`, `deepseek-reasoner`        | `DEEPSEEK_API_KEY`   | Cheap; chat = V3 (fast), reasoner = R1 (stronger)  |
| OpenAI          | `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, …       | `OPENAI_API_KEY`     |                                                    |
| Anthropic       | `claude-3-5-sonnet-20241022`, `claude-opus-4-...`, … | `ANTHROPIC_API_KEY` |                                              |
| Google          | `gemini-2.5-flash`, `gemini-1.5-pro`, …     | `GOOGLE_API_KEY`     |                                                    |
| Groq            | `llama-3.3-70b-versatile`, `qwen2.5-72b-instruct`, … | `GROQ_API_KEY` | Recognized by model-name keyword, no prefix needed |
| Ollama (local)  | `ollama/qwen2.5-coder:32b`, `ollama/llama3.3:70b`, … | (none)        | Set `OLLAMA_BASE_URL` (default `http://localhost:11434/v1`) |
| vLLM (local)    | `vllm/<served-model-name>`                  | (optional)           | Set `VLLM_BASE_URL` (e.g. `http://localhost:8000/v1`) |

Optional resilience: a comma-separated `LLM_FALLBACK_MODELS` retries the
request on the next model in the chain when the primary errors. Mix
providers freely.

```bash
# .env
LLM_MODEL=deepseek-chat
LLM_FALLBACK_MODELS=deepseek-reasoner,gpt-4o-mini
DEEPSEEK_API_KEY=sk-...
OPENAI_API_KEY=sk-...
```

### Choose which phases to run

`biotest.py --phase` accepts any comma-separated subset of `A,B,C,D`:

| Invocation         | What runs                                       | When to use                                      |
|:-------------------|:------------------------------------------------|:-------------------------------------------------|
| `--phase D`        | A (cached) → B → C → coverage feedback loop     | **Recommended for typical use**                  |
| (no flag)          | A → B → C                                       | Want everything except the feedback loop         |
| `--phase C`        | C only (reuses existing MR registry + ChromaDB) | Iterating on transforms or seed corpus           |
| `--phase B`        | B only (reuses existing ChromaDB)               | Iterating on prompts or themes                   |
| `--phase A`        | Just rebuild the spec vector store              | Specs changed                                    |
| `--phase A,B,C,D`  | Force everything from scratch                   | Hard reset                                       |
| `--dry-run`        | Validate config and exit                        | Sanity check before a long run                   |

### Change the primary target (coverage measurement focus)

Phase D's feedback loop drives off coverage on **one** SUT — the
"primary target". Switch which SUT is measured by editing one key:

```yaml
# biotest_config.yaml
feedback_control:
  primary_target: vcfpy        # was: htsjdk. Any SUT in phase_c.suts works.
```

Valid primaries are SUTs whose runner reports coverage: **VCF** →
`htsjdk` / `vcfpy` / `noodles`; **SAM** → `htsjdk` / `biopython` /
`seqan3`. `pysam` ships its parser as compiled Cython, so coverage.py
can't trace it; pysam is fine as a voter but is **not** a valid primary.

### Switch format (VCF ↔ SAM)

```yaml
# biotest_config.yaml
phase_c:
  format_filter: SAM           # was: VCF
```

Phase B auto-derives the format-to-mine from this single key, so you
don't need to edit `phase_b.formats` or seed paths separately.

### Enable / disable individual SUTs

Each SUT can be turned off without removing it from the file:

```yaml
# biotest_config.yaml
phase_c:
  suts:
    - name: htsjdk
      enabled: true
    - name: noodles
      enabled: false           # skip noodles for this run
    - name: seqan3
      enabled: false           # skip seqan3 if you didn't build the C++ harness
    # …
```

Disabled SUTs don't run and don't need to be installed. Useful when you
don't have a Rust or C++ toolchain on your machine.

### Adjust the feedback loop budget

```yaml
# biotest_config.yaml
feedback_control:
  max_iterations: 4            # how many B+C+coverage rounds at most
  timeout_minutes: 180         # graceful self-stop when wall time exceeds this
  target_scc_percent: 95.0     # stop early when spec coverage hits this
```

---

## Adding a New Parser (SUT)

Parsers speak different languages and expose different APIs, so each one
needs a thin **Harness** that exposes a uniform contract:

> **parse contract.** Given a file path and a format (`VCF` or `SAM`),
> return a JSON object matching `test_engine/canonical/schema.py`. Exit 0 on
> success, non-zero on error.

### Step 1 — write the Harness

| SUT language  | What to write                                      | Example                                       |
|:-------------:|----------------------------------------------------|-----------------------------------------------|
| Java          | `.java` → fat JAR                                  | `harnesses/java/BioTestHarness.java`          |
| Python (pip)  | `ParserRunner` subclass (in-process)               | `test_engine/runners/biopython_runner.py`, `test_engine/runners/vcfpy_runner.py` |
| Python (Docker) | CLI script + Dockerfile                          | `harnesses/pysam/`                            |
| C / C++       | Binary that reads a file, prints canonical JSON    | `harnesses/cpp/biotest_harness.cpp`           |
| Rust          | Cargo binary crate, JSON on stdout                 | `harnesses/rust/noodles_harness/`             |
| Go / …        | Same contract: binary, stdin→canonical JSON→stdout | (follow the C++ / Rust patterns)              |

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
| **vcfpy**   | `vcfpy.Writer.from_path`                                       | `test_engine/runners/vcfpy_runner.py`          |
| **noodles** | `noodles_vcf::io::writer::Writer`                              | `harnesses/rust/noodles_harness/src/main.rs` (`write_roundtrip`) |
| **htslib**  | `bcftools view` / `samtools view` (already a round-trip)       | `test_engine/runners/htslib_runner.py`         |

### Opt-out is silent

If your SUT has no writer, leave `supports_write_roundtrip = False` (the
default). The framework's runtime-capability filter hides
`sut_write_roundtrip` from the Phase B menu when no primary SUT supports it,
so no MR will ever target your read-only runner for write testing.

### Optional: richer LLM catalogs via reflection

Two sibling opt-in flags let the framework surface your SUT's live API
surface to the LLM that mines metamorphic relations:

| Flag                                  | What it enables                                                  |
|:--------------------------------------|:-----------------------------------------------------------------|
| `supports_query_methods: bool`        | Scalar getter catalog for API-query MRs (Rank 5)                 |
| `supports_mutator_methods: bool`      | Mutator-method catalog — prompt-only signal for Rank 6 MR synth  |

Both default to `False`. Opt in by implementing the matching
`discover_query_methods(fmt)` / `discover_mutator_methods(fmt)` — each is a
thin wrapper over your language's native reflection (Python:
`test_engine/runners/introspection.py` helpers; Java: your harness's
`--mode discover_methods` CLI; C/C++/Rust: `harnesses/_reflect/` scaffolding).
See `documents/Flow.md` §5.5 for the runner-contract details.

---

## The 44 Atomic Transforms

Each transform either preserves biological semantics (1–20, 26–32, 36–43)
or deliberately violates a specific spec rule to exercise rejection paths
(21–25, 33–35). All are grounded in published literature — see
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

### SAM coverage plan — Phase 2 & 3 additions (8 new, 2026-04-19)

Phase 2 adds 5 header-subtag-reorder transforms (the SAMv1 §1.3
"TAG:VALUE pairs within a record line have no ordering" invariant) and
3 new malformed mutators. Phase 3 adds 2 binary-codec round-trips via
the `samtools` CLI. All are SUT-agnostic and pass through the existing
dispatch / strategy plumbing — no runner code changes. See
`documents/Flow.md` "SAM Coverage Plan" for the full design.

| #  | Transform                              | Fmt | Scope  | Purpose                                                         |
|:--:|:---------------------------------------|:---:|:------:|:----------------------------------------------------------------|
| 26 | `shuffle_hd_subtags`                   | SAM | Header | Permute TAG:VALUE inside `@HD` (subtags have no spec order)     |
| 27 | `shuffle_sq_record_subtags`            | SAM | Header | Permute TAG:VALUE inside each `@SQ` record                      |
| 28 | `shuffle_rg_record_subtags`            | SAM | Header | Permute TAG:VALUE inside each `@RG` record                      |
| 29 | `shuffle_pg_record_subtags`            | SAM | Header | Permute TAG:VALUE inside each `@PG` record                      |
| 30 | `shuffle_co_comments`                  | SAM | Header | Shuffle `@CO` comment lines (canonical normalizer sorts them)   |
| 31 | `sam_bam_round_trip`                   | SAM | File   | SAM → BAM → SAM via `samtools view -b`; exercises BAM codec     |
| 32 | `sam_cram_round_trip`                  | SAM | File   | SAM → CRAM → SAM via `samtools view -C -T ref`; needs toy ref   |

New Rank-3 malformed mutators (all SAM):

| #  | Transform                              | Fmt | Spec rule broken                                                   |
|:--:|:---------------------------------------|:---:|:-------------------------------------------------------------------|
| 33 | `violate_tlen_sign_consistency`        | SAM | Paired reads must have opposite-signed TLEN (SAMv1 §1.4)           |
| 34 | `violate_optional_tag_type_character`  | SAM | Tag type char restricted to `AifZHB` (SAMtags §2.1)                |
| 35 | `violate_flag_bit_exclusivity`         | SAM | FLAG 0x4 unmapped ⇔ RNAME=`*` / POS=0 (SAMv1 §1.4.1)               |

### SAM Round 1 — record-level transforms (5 new, 2026-04-26)

Five record-level SAM transforms targeting Phase-4 of the SAM coverage
plan. Selected from a research dossier of SAMv1 §1.4 / §1.5 / SAMtags
specs; each spec-cited and unit-tested. All-SUT applicable (text-only
record mutations).

| #  | Transform                              | Scope  | SAMv1.tex citation | Purpose                                                       |
|:--:|:---------------------------------------|:------:|:-------------------|:--------------------------------------------------------------|
| 36 | `normalize_unmapped_record_fields`     | Record | §1.4.1 (FLAG 0x4)  | When FLAG&0x4 set: force RNAME=`*`, POS=0, MAPQ=0, CIGAR=`*`, RNEXT=`*`, PNEXT=0, TLEN=0 |
| 37 | `strip_mate_flags_if_unpaired`         | Record | §1.4.2 (FLAG 0x40/0x80) | When FLAG&0x1 unset, clear paired-end-only flag bits      |
| 38 | `normalize_seq_case`                   | Record | §1.4.10 (SEQ chars)| Force SEQ to uppercase ACGTN (when not `*`)                   |
| 39 | `cigar_zero_length_op_removal`         | Record | §1.4.6             | Remove `0M`, `0I`, `0D`, `0N`, `0S`, `0H`, `0P`, `0=`, `0X` ops |
| 40 | `canonicalize_cigar_match_operators`   | Record | §1.4.6 + SAMtags MD| Rewrite each `M` op as a sequence of `=`/`X` ops driven by the MD tag; recompute NM |

Round-1 4-rep cascade result (relative to pre-Round-1 baseline):
**htsjdk_sam +2.85pp, biopython_sam +1.10pp, seqan3_sam +1.00pp.**

### SAM Round 2 — three more spec-cited transforms (3 new, 2026-04-29)

Three additional transforms, each pre-cascade code-reviewed against the
SAMv1.tex spec.

| #  | Transform                              | Scope  | SAMv1.tex citation | Purpose                                                                 |
|:--:|:---------------------------------------|:------:|:-------------------|:------------------------------------------------------------------------|
| 41 | `pos_shift_with_sq_ln_bound_check`     | File   | line 739–743 + LN range | Shift all alignment POS by +N + widen `@SQ LN` by +N (Recommended Practice path) |
| 42 | `canonicalize_rnext_equals_alias`      | Record | line 571           | Toggle RNEXT between `=` alias and explicit value when RNEXT==RNAME      |
| 43 | `bump_hd_vn_minor`                     | Header | 1.5↔1.6 deltas     | Toggle `@HD VN` between 1.5 and 1.6 (semantics-preserving for the corpus shape) |

Round-2 4-rep cascade was approximately neutral
(htsjdk −1.08pp, biopython +0.70pp, seqan3 −0.45pp; all within std
bands). Diagnosis in `documents/Flow.md` "SAM coverage refine —
Round 2": the 18-transform menu hit saturation under the fixed 5400s
wall budget — more transforms cost more Phase-B mining than they
gained in Phase-C coverage at the published budget.

### SAM Refine experiment (4 new + harness mode + 7 literal seeds, 2026-04-30 → 05-01)

Diff-driven gap closure: per-cell coverage diffs (`compares/results/coverage/SAMrefine/`)
identified three patterns that explained ≥86% of the SOTA-favoring
gap. Targeted interventions:

| Lever | What it adds | Cells | Δ from L1+L2+L4+L5 |
|:-----:|:-------------|:------|:-------------------|
| **L1** (4 transforms below) | Rare format tokens biotest's emitter never emitted | all 3 | ~+2.0pp combined |
| **L2** (`--mode parse_validate` in `harnesses/java/BioTestHarness.java`) | Post-parse `SAMRecord.isValid()` (113-line body) + `getAlignmentBlocks()` + `validateCigar()` per record, env-var-gated for htsjdk only | htsjdk_sam | +2.7-3.5pp |
| **L4** (cascade orchestrator config tune) | `seed_synthesis.max_seeds_per_iteration: 5→3` (saturation mitigation) | all 3 | small, compounding |
| **L5** (cell-partitioned literal seeds) | 7 hand-crafted `seeds/sam/literals_*.sam` files seeding magic constants per cell | all 3 | small, multiplicative with L1 |

#### L1 — four new emitter-dialect transforms

| #  | Transform                              | Scope  | SAMv1.tex citation | Purpose                                                                 |
|:--:|:---------------------------------------|:------:|:-------------------|:------------------------------------------------------------------------|
| 44 | `add_sq_rare_tags`                     | Header | §1.3 `@SQ`         | Append AH/AN/AS/DS/TP to each `@SQ` line (when missing); reaches biopython `_read_header` arms + htsjdk `SAMSequenceDictionary.addSequenceAlias` |
| 45 | `add_pg_rare_tags`                     | Header | §1.3 `@PG`         | Append CL/DS/VN to each `@PG` line; reaches seqan3 `format_sam_base.hpp:538-549, 558-568` |
| 46 | `add_hd_group_order_tag`               | Header | §1.3 `@HD GO`      | Add `GO:none` to `@HD` if absent; reaches seqan3 `format_sam_base.hpp:374, 379-380` |
| 47 | `emit_h_hex_optional_tag`              | Record | §1.5 H-type        | Convert one `B:c/C/s/S/i/I` tag to a lossy single-byte `H:hex` projection; reaches seqan3 `read_sam_byte_vector` body |

Each ships with 8–12 unit tests (31 total) in `tests/test_transforms.py`.

#### Refine cascade result (4-rep mean, n=4)

| Cell | Round 2 | **Refine** | Δ vs Round 2 | SOTA | **Δ vs SOTA** |
|---|---:|---:|---:|---:|---:|
| **htsjdk_sam** | 20.90% ± 2.33% | **25.77% ± 2.51%** | **+4.88pp ↑** | jazzer 25.47% | **+0.30pp ⭐** |
| biopython_sam | 51.45% ± 0.78% | 53.98% ± 0.52% | +2.52pp ↑ | atheris 54.40% | −0.42pp (within std) |
| seqan3_sam | 91.75% ± 0.10% | 94.18% ± 0.67% | +2.43pp ↑ | libfuzzer 98.45% | −4.27pp (harness-bound) |

**Headline: htsjdk_sam beat jazzer by +0.30pp** — the first SAM cell
where biotest's metamorphic-relation pipeline exceeds a coverage-guided
fuzzer SOTA on a fair wall-time / filter-scope comparison. Reps 0+1
individually hit 28.0% / 27.9% before kept_* corpus saturation pulled
reps 2+3 down to 23.6%.

seqan3_sam stayed −4.27pp below libfuzzer because the residual gap is
**483 missed branches in `if constexpr` template arms** driven by the
C++ harness's `record_type` parameterisation — orthogonal to any
input-domain lever; out of scope for this experiment.

Full writeup: `compares/results/coverage/biotest_4rep_cascade_sam_refine_20260430/SUMMARY.md`.
Evidence + plan + reviewer passes: `compares/results/coverage/SAMrefine/`
(`root_cause.md`, `sota_mechanisms.md`, per-cell diffs, `refine.md` v2,
`refine_review.md`, `refine_implementation_review.md`).

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
| **MR synthesis** (Rank 6) — **opt-in** | Each Phase D iteration asks the LLM for NEW metamorphic relations (not new files) that target uncovered classes / modules. Measured +0.7–1.1 pp at ~1.5–2× wall time on htsjdk/VCF (Runs 7/8); off by default. Flip `feedback_control.mr_synthesis.enabled: true` to enable. | Fuzz4All ICSE'24; PromptFuzz CCS'24; ChatAFL NDSS'24 | `mr_engine/agent/mr_synthesizer.py` |
| **Per-class blindspot + mutator catalog** (Tier 2) — **opt-in** | Blindspot ticket surfaces the Top uncovered classes / modules + a reflection-discovered mutator catalog (prompt-only). Same measurement window as Rank 6; off by default. Flip `feedback_control.prompt_enrichment.per_class_blindspot` / `.mutator_catalog` to enable. | (internal) | `test_engine/feedback/blindspot_builder.py`, `test_engine/runners/introspection.py::get_mutator_methods` |
| **Coverage-growth corpus keeper** (Rank 8) | Every transformed file (`T_*`) that at least one parser runner accepts is content-hashed and saved to `seeds/<fmt>/kept_<sha8>.{vcf,sam}` before the tempfile is unlinked. Refinement A (2026-04-22): AST-hash dedup so semantics-preserving transforms (e.g. `shuffle_meta_lines`) that produce canonical-JSON-identical output as their source are rejected — keeps only genuinely parser-path-diverse material. Next `SeedCorpus` picks them up via the existing glob. On by default; FIFO-capped per format. | Zest ISSTA'19 (Padhye et al., arXiv:1812.00078); Fuzz4All ICSE'24; libFuzzer ATC'16 | `test_engine/feedback/corpus_keeper.py`, `test_engine/orchestrator.py::_run_single_test` |
| **Value-diversifier** (Rank 9) | **Non-metamorphic** side-lever that populates `seeds/<fmt>_diverse/` with N byte-distinct variants per source seed by perturbing numerical fields (POS / QUAL / MAPQ / AF / DP / TLEN) within spec-valid ranges, gated by canonical-normalizer validity + optional SUT-parser probe (Refinement C, 2026-04-22). Directly attacks the `Math` / `VoidMethodCall` / `RemoveConditional_ORDER_ELSE` kill gaps identified in `WHY_BIOTEST_UNDERPERFORMS.md` — those mutators require numerically-varied inputs that pure semantic metamorphic transforms can never produce. Files live in a sibling dir so Phase C's MR loop doesn't glob them; mutation-score staging explicitly unions them. SUT-agnostic (all field positions are from VCF/SAM spec). | Offutt & Untch *Mutation 2000* 2001; Zest ISSTA'19 | `mr_engine/transforms/value_diversifier.py` |
| **Byte-level fuzzer** (Rank 10) | Unstructured byte-level mutation (bit-flip / byte-sub / byte-insert / byte-delete, weighted toward `sub_random_digit` for high valid-yield) on each source seed, producing `seeds/<fmt>_bytefuzz/`. Header lines preserved verbatim; non-header byte positions mutated at random. Same validity gate as Rank 9 (canonical normalizer + optional SUT parser). Targets the `RemoveConditional_EQUAL_ELSE` / `VoidMethodCall` kills that require tokenizer-edge diversity (which Rank 9's per-field structured perturbation can't produce). Zero new dependency — uses `random` stdlib + existing normalizer. **Not** a libFuzzer integration; no coverage feedback at the fuzzer level — Phase-3 mutation score is the downstream fitness signal. Keeps BioTest's SUT-agnostic and oracle-separability properties intact. | Zest ISSTA'19 (Padhye et al.); libFuzzer ATC'16 (operator library); Miller CACM'90 (random-bytes-with-validity-gate) | `mr_engine/transforms/byte_fuzzer.py` |
| **Boundary-value diversifier** (Rank 11) | Classic Boundary Value Analysis (Myers 1979) applied to VCF/SAM numerical fields: for each seed, emits variants with spec-extreme values (POS=1, POS=INT_MAX, QUAL=0, MAPQ=255, AF=0.0, AF=1.0, TLEN=INT_MIN, etc.). Deterministic hits of the comparison-mutant boundaries that Rank 9's random perturbation only hits by luck. Output to `seeds/<fmt>_diverse/bv_<sha8>.{vcf,sam}`. Same validity gate as Rank 9/10. | Myers 1979 *The Art of Software Testing* ch.4 (original BVA); Just et al. FSE'14 (BVA kills ~30% of relational-operator mutants random misses) | `mr_engine/transforms/boundary_values.py` |
| **Per-cell adaptive corpus composition** (Refinement D) | Each mutation cell's corpus is staged with a per-SUT composition: tolerant parsers (htsjdk / vcfpy / seqan3) get primary + Rank 9/11 diverse + Rank 10 bytefuzz (~1050 files); strict parsers (biopython / noodles) get primary + diverse-only (~450 files, skip bytefuzz that their parsers would reject at 80%+ rate). Automated mapping by SUT name; new SUTs pick their tolerance via a baseline parse-rate probe (>50% reject → strict). | (internal — run-4 post-mortem finding) | `compares/scripts/` staging logic |
| **Structural variant generator** (Rank 12) | Deterministically enumerates **branch-diverse** inputs from a spec-derived catalogue: SAM CIGAR shape mixes (H/S/I/D/=/X/P/M/N combinations), tag-type permutations (Z/H/B/A/i), flag-bit combinations (12 SAM flags), multi-record files; VCF multi-sample records (1-10 samples with varied genotype patterns including `./.`, phased `0\|1`, polyploid `0/1/2`), symbolic ALT (`<DEL>`/`<DUP>`/`<INS>`/`<CNV>`), multi-contig, varied FILTER/INFO/FORMAT combinations. Run-6 diagnostic: closed htsjdk_sam gap from -6.28pp to -2.88pp (+20 kills) by hitting `RemoveConditional_EQUAL_ELSE` and `VoidMethodCall` mutants that value-level perturbation (Ranks 9/11) can't reach — those mutants need files that traverse different branch paths through the same classes. Same validity gate as Rank 9/10/11; SUT-agnostic. | Andrews-Briand-Labiche ICSE'05 (structural test data variety beats value variety for mutation); Just et al. FSE'14 (relational mutants need branch-diverse inputs) | `mr_engine/transforms/structural_diversifier.py` |
| **Lenient byte fuzzer** (Rank 13) | Byte-level mutator with a WEAK gate: emits any file with ≥1 line, skipping the canonical normalizer gate Ranks 9/10/11 use. PIT/cargo-mutants/mull oracles compare unmutated-vs-mutated parse outcome — they don't need metamorphic-valid inputs, only deterministic ones. Rank 13 produces files that htsjdk's `LENIENT` parser accepts (yielding `err:IOException`, `err:IllegalArgumentException`, etc.) but the normalizer rejects, hitting error-path branches where byte-corrupted-but-recognizable input flips exception types under mutation. Used only by Phase-3 mutation staging for cells with non-strict oracles; not used by Phase-C MR loop (which requires metamorphic-valid inputs). | Miller-Fredriksen-So CACM'90 (random-bytes-with-weak-gate); Padhye et al. ISSTA'19 (Zest: branch-gate, not validity-gate) | `mr_engine/transforms/lenient_byte_fuzzer.py` |

Configured under `feedback_control.seed_synthesis`,
`feedback_control.mr_synthesis`, `feedback_control.prompt_enrichment`,
and `phase_b.themes` in `biotest_config.yaml`.

Measured ceiling on htsjdk/VCF with Ranks 1-5 + Rank 7 active:
**~47% line coverage** (Run 6 = 46.9% in 170 min). Turning on Rank 6 +
Tier 2 has bought at most +1.1 pp at ~2× wall time (Runs 7/8),
a per-minute return roughly 40× less efficient than the baseline rate —
so the project's honest posture is "baseline is the sweet spot; the
extra levers ship as opt-in." Above ~48% in this paradigm requires
per-SUT harness code (Liyanage & Böhme ICSE'23 published ceiling ~60%).
See `documents/Flow.md` for the full writeup and `coverage_notes/` for
per-run measurements.

### SAM coverage plan (2026-04-19) — 6 additional levers + 3 refine rounds

A companion, SUT-agnostic lever stack specifically for closing the SAM
coverage gap. All 6 live entirely in framework code + data; nothing
per-SUT changes.

| Phase | Lever                                         | Where                                                                               |
|:-----:|:----------------------------------------------|:------------------------------------------------------------------------------------|
| 1     | Expanded SAM Tier-2 corpus (+30 htslib files) | `seeds/fetch_real_world.py`                                                         |
| 2     | 5 header-subtag shuffles + 3 malformed        | `mr_engine/transforms/sam.py`, `mr_engine/transforms/malformed.py`                  |
| 3     | SAM↔BAM / SAM↔CRAM round-trip via samtools    | `mr_engine/transforms/sam.py` (`sam_bam_round_trip`, `sam_cram_round_trip`)         |
| 4     | Rule-reachability filter + query-methods gate | `test_engine/feedback/blindspot_builder.py`, `phase_a.rule_capability_tags` config  |
| 5     | SeedMind generator-mode synthesis             | `mr_engine/agent/seed_synthesizer.py::synthesize_seeds_via_generator`               |
| 6     | Tier-2 cross-parser corpus minimization       | `seeds/minimize_corpus.py`                                                          |

Expected cumulative lift on biopython/SAM (Run 1 baseline 44.0 %):
**55–62 %**, ceiling-bounded by the published ~60 % automated-MR limit.

**Three refine rounds extended this plan in 2026-04-26 → 05-01** (full
detail in `documents/Flow.md` "SAM coverage refine" section):

| Round | What it added | Cascade result vs SOTA |
|---|---|---|
| Round 1 (2026-04-26) | 5 record-level SAM transforms (#36–40 above) | htsjdk +2.85, biopython +1.10, seqan3 +1.00 pp vs prior baseline |
| Round 2 (2026-04-29) | 3 spec-cited SAM transforms (#41–43 above) | Approximately neutral (saturation under fixed wall budget) |
| Refine experiment (2026-04-30 → 05-01) | 4 emitter-dialect transforms (#44–47), `--mode parse_validate` Java harness mode, 7 cell-partitioned literal seeds, blindspot-driven cascade tuning | **htsjdk_sam beats jazzer by +0.30pp**; biopython −0.42pp from atheris (within std); seqan3 −4.27pp from libfuzzer (harness-bound branch gap) |

The Refine experiment was diff-driven — per-cell coverage diffs against
the published SOTA fuzzers identified three patterns explaining ≥86%
of the gap, and L1/L2/L4/L5 levers above were each tied to a specific
pattern's evidence. Plan + reviewer passes documented under
`compares/results/coverage/SAMrefine/`. Final cascade SUMMARY at
`compares/results/coverage/biotest_4rep_cascade_sam_refine_20260430/SUMMARY.md`.

---

## Seed Corpus

Two tiers:

- **Tier-1 (committed, ~6 files)**: hand-crafted minimal examples under
  `seeds/vcf/` and `seeds/sam/` — enough for smoke tests.
- **Tier-2 (gitignored, ~60 files)**: curated real-world seeds from htsjdk,
  bcftools, hts-specs, GATK, htslib. Pull with `py -3.12 seeds/fetch_real_world.py`.
  Full provenance + diversity axes in `seeds/SOURCES.md`. Per-file cap 500 KB.
- **CRAM toy reference (committed, ≤10 KB)**: `seeds/ref/toy.fa` — required by
  `sam_cram_round_trip`; seed `@SQ` names must subset the reference's FASTA
  entries or the transform no-ops.

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
    - { name: pysam,     coverage_dir: coverage_artifacts/pysam }    # voter only (see caveat below)
    - { name: vcfpy }                                                  # pure-Python VCF voter
    - { name: noodles,   adapter: harnesses/rust/noodles_harness/target/release/noodles_harness.exe }
    - { name: htslib }    # gold-standard tie-breaker

feedback_control:
  enabled: true
  max_iterations: 4
  timeout_minutes: 180
  target_scc_percent: 95.0
  primary_target: htsjdk
  max_rules_per_iteration: 5      # Top-K blindspot window
  seed_synthesis:
    enabled: true                 # LLM-driven VCF/SAM seed synthesis (Rank 1)
    max_seeds_per_iteration: 5
  mr_synthesis:
    enabled: false                # LLM-driven NEW MRs (Rank 6). Off by default
                                  # after Runs 7/8 showed +0.7-1.1 pp at 1.5-2x
                                  # wall time - flip true per-run if willing to
                                  # pay the cost.
    max_mrs_per_iteration: 5
  prompt_enrichment:              # Tier 2, both off by default (same reason)
    per_class_blindspot: false
    mutator_catalog: false
  min_coverage_delta_pp: 0.3      # coverage-delta early-stop safety rail
  coverage_plateau_patience: 2

coverage:
  enabled: true
  target_filters:
    VCF:
      # Scope follows the "measure what we exercise" rule: each SUT's
      # list names ONLY the modules the three ops (parse / write_roundtrip /
      # query_methods) touch — nothing else.
      htsjdk:  [htsjdk/variant/vcf, htsjdk/variant/variantcontext/writer]
      pysam:   [libcbcf, libcvcf, bcftools.py]   # narrow — see pysam caveat below
      vcfpy:   [vcfpy/reader, vcfpy/parser, vcfpy/header, vcfpy/record, vcfpy/writer]
      noodles: [noodles-vcf/src/io/reader, noodles-vcf/src/io/writer,
                noodles-vcf/src/header, noodles-vcf/src/record,
                noodles-vcf/src/variant, noodles-vcf/src/lib.rs]
    SAM:
      htsjdk:    [htsjdk/samtools]
      biopython: [Bio/Align/sam]
      seqan3:    [seqan3/io/sam_file]
      pysam:     [libcsam, libcalignedsegment, libcalignmentfile, samtools.py, Pileup.py]
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

| SUT           | Language | VCF | SAM | parse | write_roundtrip | query_methods | Coverage                | Independent impl? | Role                                   |
|:--------------|:---------|:---:|:---:|:-----:|:---------------:|:-------------:|:------------------------|:-----------------:|:---------------------------------------|
| **htsjdk**    | Java     | ✓   | ✓   | ✓     | ✓               | ✓             | JaCoCo                  | ✓                 | Regular voter                          |
| **pysam**     | Python   | ✓   | ✓   | ✓     | ✓               | ✓             | coverage.py *(limited)* | ✗ (wraps htslib)  | Regular voter                          |
| **biopython** | Python   | —   | ✓   | ✓     | —               | ✓             | coverage.py             | ✓                 | Regular voter (SAM)                    |
| **seqan3**    | C++      | —   | ✓   | ✓     | —               | —             | gcovr/gcov              | ✓                 | Regular voter (SAM)                    |
| **vcfpy**     | Python   | ✓   | —   | ✓     | ✓               | ✓             | coverage.py             | ✓                 | Regular voter (VCF)                    |
| **noodles**   | Rust     | ✓   | —   | ✓     | ✓               | —†            | cargo-llvm-cov          | ✓                 | Regular voter (VCF)                    |
| **htslib**    | CLI      | ✓   | ✓   | ✓     | ✓ (CLI)         | —             | —                       | (reference)       | **Tie-breaker (gold standard)**        |
| reference     | Python   | ✓   | ✓   | ✓     | —               | —             | —                       | —                 | Independent canonical impl.            |

> **†** noodles deliberately skips `query_methods` because Rust has no
> runtime reflection (same choice as seqan3). The framework's
> runtime-capability resolver hides `query_method_roundtrip` from the
> LLM menu when no primary SUT opts in, so the gap is harmless.

> **pysam coverage caveat.** `pysam`'s VCF/SAM logic lives in Cython-
> compiled `libcbcf.pyx` / `libcsam*.pyx` → native `.so`. `coverage.py`
> only traces Python bytecode, so of pysam's shipped `.py` files only
> the CLI wrappers (`bcftools.py`, `samtools.py`) are measurable — and
> neither sits on the `pysam.VariantFile` / `pysam.AlignmentFile` parse
> path. pysam is kept as a **voter** but is **not a valid
> `primary_target`** for coverage-driven Phase D feedback. Use
> **htsjdk**, **vcfpy**, or **noodles** as the coverage primary.

Coordinate normalization (all handled inside harnesses):

| Parser      | SAM POS | VCF POS | Harness action       |
|:------------|:-------:|:-------:|:---------------------|
| htsjdk      | 1-based | 1-based | —                    |
| pysam       | 0-based | 0-based | **+1** for both      |
| Biopython   | 0-based | n/a     | **+1**               |
| SeqAn3      | 0-based | n/a     | **+1**               |
| vcfpy       | n/a     | 1-based | —                    |
| noodles     | n/a     | 1-based | —                    |

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
