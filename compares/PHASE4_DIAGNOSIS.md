# Phase 4 diagnosis — "zero detections" is not method failure

**Authored**: 2026-04-21.
**Trigger**: User observation that Chats 1-4 produced 0 `FOUND` cells
and expressed concern that the method "could not make sense".
**Scope of this document**: (a) exactly what the four chats produced,
(b) why the result is methodologically consistent with the ground-truth
fuzzing literature, (c) the actual gaps, (d) concrete fixes.

---

## 1. What the four chats actually produced

| chat | SUT × format | tools run                                   | FOUND | false+ | miss | skip |
| :--- | :----------- | :------------------------------------------ | ----: | -----: | ---: | ---: |
| 1    | htsjdk VCF   | evosuite_anchor, jazzer, pure_random        |     0 |   7(J) |   20 |    0 |
| 2    | htsjdk SAM   | evosuite_anchor, jazzer, pure_random        |     0 |   3(J) |    6 |    0 |
| 3    | vcfpy  VCF   | atheris, pure_random                        |     0 |      0 |   10 |    4 |
| 4    | noodles VCF  | cargo_fuzz, pure_random                     |     0 |      0 |   12 |    6 |

**(J) = jazzer-attributed.** Chat 1's report
(`compares/results/bug_bench_chat1_draft/report.md`) and Chat 2's
(`…chat2_draft/report.md`) both contain thorough manual triage of
every `false+` cell. Chat 3's (`…chat3_artefacts/report.md`) and
Chat 4's (`…chat4_draft/report.md`) document skips and misses.

**Crucial fact not visible in the aggregate:** `biotest` — the primary
tool under evaluation — was **excluded by operator request in all four
chats**. Every chat's `run_manifest.json` says so. See §2.1 below.

## 2. Why "0 FOUND" is literature-consistent

### 2.1 biotest was never run

`compares/results/bug_bench_chat{1,2,3,4}_draft/run_manifest.json`:
> `"biotest excluded by operator request"`

Phase 4's whole point is to compare fuzzers against **BioTest's
differential + metamorphic oracle**. Running only the comparators
and declaring "the method failed" is equivalent to measuring a
stopwatch against a wall: of course the wall didn't finish first —
we never started the stopwatch.

### 2.2 Budget is 288× below Magma's standard

Our 300 s primary budget vs the canonical benchmarks:

| benchmark  | per-trial budget | trials | total CPU-hours |
| :--------- | ---------------: | -----: | --------------: |
| Magma SIGMETRICS'20     | 24 h  | 10 | ≈ 26 000 (per 118-bug panel) |
| FuzzBench OOPSLA'21     | 23 h  | 20 | ≈ 110 000 (per 20-subject panel) |
| **Our Chats 1-4 (actual)** | **300 s** | **1** | **~40** |

At 300 s we are a factor of **288× below the Magma design floor**.
Even Magma — running the best mutation-based fuzzers at full 24 h
trials — reports that **no single fuzzer triggered more than 68 % of
the verified bugs**, and only **79 % were triggered by any fuzzer
across all trials** (Hazimeh et al. SIGMETRICS'20). The industry-
standard floor (FuzzBench) is 23 h × 20 trials.

Linearly scaling Magma's 68 % best-case rate to our 1/288 budget,
the **expected detection rate is ~0.24 %** → **~0.08 bugs out of
our 35** → **zero is the modal outcome**. (Linear scaling is overly
optimistic; sub-linear is more realistic for structure-aware bugs,
making the expected rate even lower.)

### 2.3 The false+ cells are textbook-correct

Jazzer's 11 crash cells across Chats 1 and 2 are **the correct
Klees et al. CCS'18 §3.1–§3.2 outcome**:

- Klees et al. showed that naive crash counts over-count unique
  bugs by ~500× on average; stack-hashing reduces this to ~46× but
  still with ~16 % false negatives. The detection predicate we use
  (§5.3.1 — "pre-fix crashes AND post-fix does not") is precisely
  the corrective Klees, Magma, and FuzzBench all recommend.
- Chat 1 `report.md §"False+ deep-dive"` shows all 7 htsjdk VCF
  jazzer cells landed on **two stack signatures** (libFuzzer's own
  DEDUP_TOKEN), both in
  `htsjdk.variant.vcf.AbstractVCFCodec.oneAllele:582` —
  `IndexOutOfBoundsException` on malformed genotype strings. This
  bug exists in htsjdk from 2.19.0 through 3.0.4 and is **not** any
  of our 35 manifest bugs. Post-fix replay correctly identifies it
  as surviving the version bump → `false+`.
- Chat 2 `report.md §"False-positive triage"` shows all 3 htsjdk
  SAM jazzer cells produce **byte-identical** trigger files from a
  single poisoned seed (`real_world_htslib_colons.bam`). The seed
  contains a `@SQ` header with sequence name `chr1,chr3`, which
  htsjdk's SAM validator has rejected regex-wise from 2.22.0
  through 3.0.0 — a stable, intentional validation, not a bug.

**Both outcomes are the detection predicate working exactly as
specified.** The reports contain the manual triage confirming this
(Chats 1 and 2 already did the post-run-review work that §5.3.1
prescribes).

### 2.4 The bug *type distribution* limits crash-based fuzzers

Our 35 bugs by `expected_signal.type`:

| signal type                               | count |
| :---------------------------------------- | ----: |
| differential_disagreement                 |   28  |
| uncaught_exception                        |    6  |
| timeout_or_differential_disagreement      |    1  |
| intermittent_differential_disagreement    |    1  |

**28 of 35 (80 %) are semantic `differential_disagreement` bugs.** By
definition these are inputs that parse *successfully* in both
versions but produce *different* canonical-JSON outputs — i.e. no
crash, no exception, no sanitizer abort. Every crash-finder
(`jazzer`, `atheris`, `libfuzzer`, `cargo_fuzz`) is **provably unable
to detect these** by its own oracle. The literature makes this
explicit:

- TWINFUZZ (NDSS'25) — "sanitizers crash immediately on fault;
  differential oracles observe failure only after the subroutine
  returns" — crash-fuzzers cannot see silent output divergence.
- FuzzJIT (USENIX Security'23) — argues for oracle-enhanced fuzzing
  because stock libFuzzer-family tools miss JIT-compiler logic bugs
  that don't crash.
- DUMPLING (NDSS'25) — same argument for JS engines.
- Semantic Crash Bucketing (van Tonder ASE'18) — "semantic bugs can
  be easily missed by fuzzers using crashes as the only oracle".

So for 28 of our 35 bugs we should expect crash-finders to return
`miss` even at 24 h budgets. **That's the scientific reason BioTest
exists — its differential + metamorphic oracle is supposed to close
exactly this gap.** But we didn't run biotest.

### 2.5 Pure Random post-hoc replay never executed

`pure_random`'s adapter (`run_pure_random.py`) emits random bytes and
intrinsically reports `crash_count = 0`. Chat 6 was specified to
post-hoc replay `pure_random/<bug>/corpus/*.{vcf,sam}` through each
SUT's `ParserRunner` and score uncaught exceptions as crashes (the
Miller et al. CACM'90 schema cited in §4.3). **Chat 6 has not been
run**, so every `pure_random` cell correctly reads `miss` — it is
not a scoring failure, it is an incomplete pipeline.

### 2.6 Seed poisoning and short-budget halt behaviour

libFuzzer (and therefore jazzer, atheris, cargo_fuzz) halts on the
first crash it finds. If a seed in `compares/results/bench_seeds/`
immediately trips *any* validation in the SUT, libFuzzer attributes
the entire trial's budget to that seed and halts — it never gets to
mutate-and-explore. Chat 2 documented exactly this:
`real_world_htslib_colons.bam` crashes htsjdk SAM on the very first
read with `MS: 0 ; base unit: 0000...0000` (zero mutations performed).

This is the single biggest budget-amplifier for our zero-FOUND
result. At 300 s, one poison seed = 100 % of the budget wasted.

### 2.7 Noodles harness-skew removed 3-6 cells by construction

Chat 4's `skip_reasons.json` + report document that noodles-vcf
pre-fix versions 0.23 / 0.48 do not compile against the harness
`main.rs` (written for 0.70 API). `noodles-223`, `noodles-224`,
`noodles-ob1-0.23` were skipped for this reason in Chat 4, as the
plan predicted.

## 3. Is the method "making sense"?

Re-reading Chats 1-2's `report.md` alongside the aggregate:

1. **Detection predicate (§5.3.1) behaves exactly as specified.**
   Jazzer produced crashes → predicate checked post-fix silence →
   unrelated-bug crashes correctly flagged `false+`. This is the
   Klees-Magma-Böhme prescribed behaviour.
2. **Jazzer actually surfaced a real, undisclosed htsjdk bug** (the
   `oneAllele:582` IOOBE) as a by-product. That's a useful finding —
   should be reported upstream.
3. **Every zero-FOUND row is explained by one or more of**:
   (a) biotest not run, (b) short budget, (c) semantic-bug type
   incompatible with crash oracle, (d) pure_random post-hoc replay
   not run, (e) poison seed, (f) harness-version skew.

**The method makes sense.** What we have is not a scientific flaw in
the predicate but **an execution-level data gap**. The fix is to
execute the missing pieces, not to change the predicate.

## 4. Concrete fixes, ordered by leverage

| # | fix | cost | expected lift on FOUND rate |
| :-- | :-- | :-- | :-- |
| 1 | **Run biotest across all 35 bugs.** | 35 × 7200 s = ~70 h one-way; ~18 h at 4-way parallel | Large. biotest's differential+MR oracle is designed for the 28 `differential_disagreement` bugs. Expected ≥ 10 of 28 at 2 h budget based on BioTest's Phase-A-D coverage numbers. |
| 2 | **Raise the budget from 300 s to 7200 s (Magma short-regime) for crash-finders.** | 24× longer; ~7 h per chat | Modest. Crash-finders still miss ≥80 % of bugs by signal-type argument (§2.4), but uncaught_exception bugs (6 of 35) may start to surface. |
| 3 | **Execute Chat 6's `pure_random` post-hoc replay.** | ~30 min | Modest. Scores pure_random against Miller CACM'90 schema. Typical outcome: picks up the 4-6 uncaught_exception bugs if the corpus is large enough. |
| 4 | **Sanitize the seed corpus.** Drop any seed whose first-pass parse against *all* in-scope SUTs throws. Measure via a one-shot ParserRunner sweep; prune poisons. | ~20 min | Medium. Removes the fixed-cost budget-killer that Chat 2 flagged. |
| 5 | **Add a grammar-aware mutator layer** (Nautilus / Gramatron / FormatFuzzer) for VCF + SAM. | 1-2 days eng. | Large for crash-finders on structured formats. Mathis et al. PLDI'19 reported pFuzzer 52 % keyword coverage vs AFL 5 %. |
| 6 | **Add a semantic post-hoc oracle for `differential_disagreement` bugs.** Run every tool's corpus through the BioTest consensus oracle as a cross-tool fairness pass; credit each tool for the disagreements its inputs caused. | Already specified in §4.4 ("Fairness equalizer"), not yet run | Large. Lets crash-finders score on semantic bugs their native oracle can't see. |
| 7 | **Report the latent `oneAllele:582` IOOBE as a by-product finding.** | 1 h (draft upstream bug report) | Paper-level finding; not a Phase 4 metric. |

## 5. What to change in DESIGN.md

1. Add **Risk 5 — "Budget vs literature floor"** under §9 (done —
   see §9 Risk 5 in `compares/DESIGN.md`).
2. Expand §5.3.1's "Expected detection rate" paragraph with the
   Magma 68 % / 79 % numbers to set reader expectations (done —
   see §5.3.1).
3. Cross-reference the Chat 1/2/3/4 reports from §13.5 Phase 4 so
   the paper draft can lift the false+ deep-dive verbatim.

## 6. Citations used in this diagnosis

- **Magma** — Hazimeh, Herrera, Payer, *SIGMETRICS'20*, "Magma: A
  Ground-Truth Fuzzing Benchmark". 62 %/79 % reach/trigger rates and
  68 % best-fuzzer rate at 24 h × 10 trials.
- **FuzzBench** — Metzman et al., *OOPSLA'21*, "FuzzBench: An Open
  Fuzzer Benchmarking Platform and Service". 23 h × 20 trials as
  the default configuration.
- **Klees et al.** — Klees, Ruef, Cooper, Wei, Hicks, *CCS'18*,
  "Evaluating Fuzz Testing". Crash counts over-count bugs by
  ~500× (coverage-unique) / ~46× (stack-hashed); 16 % false
  negatives from stack-hash dedup.
- **Böhme et al.** — Böhme, Liyanage, Wüstholz, *ICSE'22*, "On the
  Reliability of Coverage-Based Fuzzer Benchmarking". Ground-truth
  bug benchmarks preferable to coverage proxies for attributing
  detection to specific bugs.
- **TWINFUZZ** — *NDSS'25* differential-testing-for-video-hardware.
  Crash oracles fire on fault; differential oracles fire on
  observable output divergence — different signal classes.
- **FuzzJIT** — Wang et al., *USENIX Security'23*. Oracle-enhanced
  fuzzing motivated by libFuzzer's miss rate on JIT logic bugs.
- **DUMPLING** — *NDSS'25* fine-grained differential JS engine
  fuzzing. Same argument for JS engines.
- **Semantic Crash Bucketing** — van Tonder, *ASE'18*. Explicit
  statement that semantic bugs are silent to crash-only oracles.
- **Miller, Fredriksen, So** — *CACM'90*, "An Empirical Study of
  the Reliability of UNIX Utilities". Origin of the "random input
  → observe crash" schema `pure_random` uses.
- **Mathis et al.** — *PLDI'19*, "Parser-Directed Fuzzing". pFuzzer
  reached 52 % keyword coverage vs AFL's 5 % on parser targets —
  motivates the grammar-aware-mutator suggestion in §4-fix-5.
- **Chen et al.** — *CSUR'18*, "Metamorphic Testing: A Review of
  Challenges and Opportunities". Metamorphic relations as oracle —
  BioTest's primary detection path.
