# Phase 4 — Baseline-tool fix plan (biotest excluded)

**Audience**: operator running Phase 4 baselines while BioTest itself
is still under development.
**Scope**: every action you need to take per chat, per baseline tool,
to make the comparator arm of Phase 4 produce meaningful numbers.
**Out of scope**: biotest — leave it alone until the BioTest pipeline
is ready. Nothing here runs `--only-tool biotest`.

**Authored**: 2026-04-21. Supersedes the Phase-4 tool guidance in
`PHASE4_EXECUTION_PLAN.md §"Chat N — …Commands"` blocks wherever the
two disagree. Root-cause analysis for *why* these changes are needed:
`compares/PHASE4_DIAGNOSIS.md` + `compares/DESIGN.md §9 Risk 5`.

---

## 0. Global fixes to land before any chat re-runs

These are orthogonal to any specific chat — land them once, then
every re-run inherits the fix. Skip to §1 if you want to go chat-by-
chat first.

### 0.1 Seed sanitization (removes the Chat-2 "chr1,chr3" class of budget waste)

Current problem: `seeds/sam/real_world_htslib_colons.bam` crashes
htsjdk SAM parser on the first read with `MS: 0 ; base unit: 0000…`
(zero mutations performed). libFuzzer/jazzer/atheris all halt on
first crash → 100 % of a 300 s budget spent on one poison seed
(Chat 2 report deep-dive). A 7200 s budget halves this to 4 % but
doesn't eliminate it.

**Action**: write + run `compares/scripts/sanitize_seeds.py`:

```python
#!/usr/bin/env python3
"""Drop seeds that already throw in BOTH pre-fix and post-fix of every
in-scope SUT. Such seeds are validation-rejected, not target bugs — they
just burn fuzzer budget."""
import json, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SUTS = {
    "VCF": ["htsjdk", "vcfpy", "noodles"],
    "SAM": ["htsjdk", "biopython", "seqan3"],
}

def parses(sut: str, path: Path, fmt: str) -> bool:
    # Use the repo's ParserRunner (test_engine/runners/<sut>_runner.py)
    # with a 10 s timeout; return True if no exception.
    cmd = ["python3.12", "-c", (
        f"from test_engine.runners.{sut}_runner import {sut.title()}Runner as R; "
        f"r = R().run('{path}', '{fmt}'); "
        f"print(bool(r.success))"
    )]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=15, cwd=str(REPO))
        return p.returncode == 0 and b"True" in p.stdout
    except Exception:
        return False

def main():
    dropped = []
    for fmt, suts in SUTS.items():
        for seed in (REPO/"seeds"/fmt.lower()).iterdir():
            if not seed.is_file():
                continue
            # Drop iff EVERY SUT throws — that makes it a validation-rejected
            # seed, not a bug-triggering one.
            if all(not parses(s, seed, fmt) for s in suts):
                dropped.append(str(seed))
                seed.unlink()
    (REPO/"seeds"/"dropped_during_sanitization.json").write_text(
        json.dumps(dropped, indent=2))
    print(f"dropped {len(dropped)} poison seeds")

if __name__ == "__main__":
    main()
```

Run once: `python compares/scripts/sanitize_seeds.py`. Commit the
resulting `seeds/dropped_during_sanitization.json` as evidence.

### 0.2 libFuzzer "keep-going" mode (turns 1 crash into N)

Current problem: libFuzzer / jazzer / atheris / cargo_fuzz default
behaviour is **halt on first crash** (exit 77). Once they find the
first parser defect in 1 minute, the remaining 299 s of the budget
does nothing. We want them to keep exploring past crashes so they
can find the *target* bug, not just the first unrelated crash.

**Action**: pass `-fork=1 -ignore_crashes=1` to the adapters that
drive libFuzzer directly, and `--keep_going=N` where N is a large
limit for Jazzer.

Edit each adapter:

- `compares/scripts/tool_adapters/run_libfuzzer.py` — append
  `"-fork=1", "-ignore_crashes=1"` to the cmd list that invokes the
  harness binary.
- `compares/scripts/tool_adapters/run_cargo_fuzz.py` — same.
- `compares/scripts/tool_adapters/run_atheris.py` — same (atheris
  wraps libFuzzer identically).
- `compares/scripts/tool_adapters/run_jazzer.py` — append
  `"--keep_going=1000"` to the jazzer CLI invocation. Jazzer's
  keep-going flag is documented here:
  https://github.com/CodeIntelligenceTesting/jazzer#keep-going.

Note: `-fork=1` also helps with OOM robustness — each crash runs in
a subprocess so a malloc blow-up in one input doesn't kill the whole
trial.

### 0.3 Budget bump from 300 s to 7200 s

Magma's short-regime floor is 7200 s per trial (Hazimeh et al.
SIGMETRICS'20). 300 s is a debugging budget, not a benchmark budget.
See `compares/DESIGN.md §9 Risk 5 §2` for the Magma/FuzzBench scaling
argument.

**Action**: every re-run uses `BUDGET_S=7200`. The chat commands in
`PHASE4_EXECUTION_PLAN.md` already parameterize this — just set the
env var.

**Caveat**: 7200 s × ~60 cells (all remaining baselines across chats
1-5) ≈ **120 compute-hours sequential, ~30 h @ 4-way parallel.**
Budget your machine-time accordingly. If 30 h is infeasible, 3600 s
is an acceptable half-way compromise (Klees CCS'18 argues 24 h is
minimum but shorter is OK if you document it).

### 0.4 PoV seed injection per cell (Magma-standard practice)

Each bug in `compares/bug_bench/triggers/<bug_id>/original.{vcf,sam}`
is a **Proof-of-Vulnerability** — a known-good input that triggers
the bug on pre-fix. Starting the fuzzer from the PoV dramatically
shortens time-to-first-bug and is the standard setup Magma/FuzzBench
use when measuring detection attribution (vs measuring discovery
ability from scratch).

**Action**: pre-seed every cell's `corpus/` with the bug's PoV plus
the sanitized general corpus.

Edit `compares/scripts/bug_bench_driver.py::invoke_adapter` (just
before `_run` is called) to copy
`compares/bug_bench/triggers/<bug_id>/original.*` into the adapter's
corpus dir alongside the general seeds:

```python
pov_dir = REPO_ROOT / "compares" / "bug_bench" / "triggers" / bug["id"]
if pov_dir.exists():
    for pov in pov_dir.glob(f"original.{bug.get('format','VCF').lower()}"):
        # Merge into the corpus the adapter will be called with; adapters
        # that copy seeds into their own corpus dir will pick this up.
        shutil.copy2(pov, seed_corpus / f"pov_{bug['id']}_{pov.name}")
```

Alternative (cleaner): have the driver pass a per-bug seed-corpus
override to the adapter when a PoV exists. Either works.

### 0.5 vcfpy install-failure fixes (Chat 3)

Chat 3's `skip_reasons.json` records two non-trivial install errors:

- `vcfpy-127` pre_fix **0.11.0** — `install pre_fix failed (sdist
  build: no pip in build env)`. Root cause: 0.11.0 is an sdist-only
  release; pip's isolated build env in the dedicated vcfpy sut-env
  venv is missing setuptools/wheel.
  **Action**: `pip install --no-build-isolation vcfpy==0.11.0` into
  the vcfpy sut-env (`compares/results/sut-envs/vcfpy/bin/pip`).
  Better: add `--no-build-isolation` to the `_install_vcfpy` helper
  in `bug_bench_driver.py` for every vcfpy install so all
  sdist-only versions work.

- `vcfpy-nocall-0.8` pre_fix **0.8.1** — `install pre_fix failed
  (version not on PyPI)`. 0.8.1 is a git-only release never
  published to PyPI.
  **Action**: patch `_install_vcfpy` to fall back to GitHub tarball
  when PyPI install errors with "No matching distribution found":
  `pip install "git+https://github.com/bihealth/vcfpy@v0.8.1"`.
  If GitHub tag `v0.8.1` doesn't exist, use commit SHA from the
  CHANGELOG.

### 0.6 Noodles harness per-version compile (Chat 4)

The canonical-JSON harness `harnesses/rust/noodles_harness/src/main.rs`
uses 0.70 API and won't compile against 0.23 / 0.48. Chat 4's 3
skips are all on those anchors.

**Option A (fastest — accept the skips)**: leave as-is and document
that noodles-223 / noodles-224 / noodles-ob1-0.23 are structurally
unmeasurable under the current single-harness design. Already noted
in `PHASE4_EXECUTION_PLAN.md §"Chat 4 expected tooling skips"`.

**Option B (1-2 d engineering)**: maintain a per-version
`main_0_23.rs` / `main_0_48.rs` / `main_0_70.rs` with the API each
version expects, and have `_install_noodles` swap `src/main.rs`
alongside the Cargo.toml pin. Moderate engineering; medium lift on
the 3 skipped cells.

Pick A unless the paper draft needs those 3 cells specifically.

### 0.7 EvoSuite minimum-viable budget

EvoSuite's genetic-algorithm search needs **at least 60 s** to
initialize + 1-2 × that for any meaningful search. At 300 s it
barely starts. Fraser & Arcuri FSE'11 used 120 s × 30 trials; the
EvoSuite doc recommends ≥ 600 s for non-trivial classes.

**Action**: bump EvoSuite cells to `BUDGET_S=3600` (1 h) minimum
when you re-run them. At 7200 s (2 h) you're in the range EvoSuite
papers actually measure at.

---

## 1. Chat 1 — htsjdk VCF

**Already ran**: Chat 1 produced 27 cells at `BUDGET_S=300` across
{jazzer, evosuite_anchor, pure_random}. Artefacts in
`compares/results/bug_bench_chat1_draft/`. Findings summary:
jazzer 7 false+ (2 unique crash signatures in
`AbstractVCFCodec.oneAllele:582` — unrelated latent bug, not any of
our 35 targets), 2 miss; evosuite 9 miss; pure_random 9 miss.

### 1.1 `evosuite_anchor` (0 FOUND, 9 miss)

- **Why 0**: 300 s is below EvoSuite's GA warm-up; the search barely
  starts before the budget elapses. No crashes surfaced → no
  `failing-tests/` → `detected=false` on every cell.
- **Actions**:
  1. Re-run at **`BUDGET_S=7200`** (2 h per cell). 9 × 7200 s = 18 h
     sequential. Single-chat time.
  2. Verify `compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar`
     exists and has the 9 pre-fix versions loaded. If not, run
     `bash compares/scripts/prepare_sut_install_envs.sh` first — its
     htsjdk JAR block populates the versioned directory from Maven
     Central.
  3. Confirm `compares/scripts/run_evosuite.sh` is writing
     `failing-tests/` (not `failing_tests/` — both conventions exist
     across EvoSuite versions). The driver's
     `_invoke_evosuite_anchor` only scans `failing-tests/`.
  4. No seed-pool fix needed — EvoSuite generates JUnit cases, not
     bytes; it ignores the seed corpus.

### 1.2 `jazzer` (0 FOUND, 7 false+, 2 miss)

- **Why 0 FOUND**: the 7 crashes are real but all trace to the
  `oneAllele:582` IOOBE — a different, latent htsjdk bug that
  survives from 2.19.0 through 3.0.4. Predicate correctly flagged
  them as `false+` (Klees CCS'18 behaviour). Two misses
  (htsjdk-1372 and htsjdk-1418) reflect jazzer halting on the
  oneAllele crash before finding the target-bug input.
- **Actions**:
  1. Land **§0.2 keep-going flag** (`--keep_going=1000`). After the
     oneAllele crash, jazzer will keep mutating and may surface the
     target bug.
  2. Land **§0.3 budget 7200 s**.
  3. Land **§0.4 PoV seed injection** — most important for jazzer.
     Pre-seeding the corpus with
     `compares/bug_bench/triggers/htsjdk-1418/original.vcf` (and the
     other 6 known-triggering VCFs) lets jazzer start FROM the bug.
     Without this jazzer has to rediscover the bug from scratch,
     which at 7200 s vs Magma's 86400 s budget is ≥ 10× below the
     rediscovery floor.
  4. **Optional**: file an upstream bug report for `oneAllele:582`
     to htsjdk — it's a genuine latent defect your benchmark
     surfaced as a by-product.

### 1.3 `pure_random` (0 FOUND, 9 miss)

- **Why 0**: `run_pure_random.py` intrinsically reports
  `crash_count = 0` — it just emits random bytes, no SUT invocation.
  Chat 6's post-hoc `ParserRunner` replay is where pure_random
  actually scores.
- **Actions**:
  1. No adapter-level fix needed.
  2. Ensure Chat 6 executes the pure_random post-hoc replay (§6
     below). Without it, every pure_random cell reads `miss`
     forever.
  3. Re-running pure_random at 7200 s is valuable only to produce
     a larger `corpus/` for Chat 6 to replay. At 60 s the corpus
     has ~180 k files; at 7200 s it's ~22 M files. If filesystem
     inode caps are a concern (Chat 1's report noted 67 M inode
     exhaustion), either cap corpus writes in `run_pure_random.py`
     or drop the budget to 1800 s for pure_random specifically.

---

## 2. Chat 2 — htsjdk SAM

**Already ran**: 9 cells at `BUDGET_S=300` across {jazzer,
evosuite_anchor, pure_random}. Artefacts:
`compares/results/bug_bench_chat2_draft/`. Findings: jazzer 3
false+ (ALL same poison seed `real_world_htslib_colons.bam` →
`SAMSequenceRecord.validateSequenceName` regex); evosuite 3 miss;
pure_random 3 miss.

### 2.1 `evosuite_anchor` (0 FOUND, 3 miss)

- Same as 1.1.
- Actions: 1.1 actions apply verbatim.

### 2.2 `jazzer` (0 FOUND, 3 false+)

- **Why 0 FOUND**: single poison seed in the SAM corpus causes
  all three cells to produce the *byte-identical* trigger file
  (md5 `9e3faa…`). `MS: 0 ; base unit: 0000…` means zero mutations
  — jazzer hit the seed crash and halted.
- **Actions**:
  1. **Run §0.1 seed sanitization first.** This should drop
     `real_world_htslib_colons.bam` (htsjdk, seqan3, biopython will
     all reject its `@SQ chr1,chr3` header). After sanitization
     confirm via:
     ```bash
     grep -l 'chr1,chr3' seeds/sam/*.{sam,bam} 2>/dev/null
     # expect: no output
     ```
  2. Land §0.2 keep-going, §0.3 budget 7200 s, §0.4 PoV seed
     injection (load
     `compares/bug_bench/triggers/htsjdk-{1489,1538,1561}/original.sam`).
  3. Re-run — likely outcome is still 0 FOUND because all 3 target
     bugs are `differential_disagreement` (no crash expected); but
     with the poison seed gone, jazzer's corpus now has a real
     chance of discovering crashes in the un-flagged 3 bugs that
     survive the post-fix replay.

### 2.3 `pure_random` (0 FOUND, 3 miss)

- Same as 1.3. Chat 6 post-hoc replay is the scoring path.

---

## 3. Chat 3 — vcfpy VCF

**Already ran**: 14 cells at `BUDGET_S=300` across {atheris,
pure_random}. Artefacts:
`compares/results/bug_bench_chat3_artefacts/`. Findings: atheris
0 FOUND / 5 miss / 2 skip (vcfpy-127, vcfpy-nocall-0.8 — install
failures); pure_random mirrors the same pattern.

### 3.1 `atheris` (0 FOUND, 5 miss, 2 skip)

- **Why 0 FOUND** for the 5 miss cells: 4 of 7 target bugs are
  `uncaught_exception` (vcfpy-176, -146, -145, -127) which atheris
  CAN theoretically catch. But at 300 s without PoV seeding and
  without grammar awareness, atheris's byte-level mutation of
  random VCF bytes almost never produces the very specific malformed
  inputs those bugs need (e.g. vcfpy-146's trigger is "INFO flag
  declared as String in the header" — a 3-line edit away from a
  valid VCF that atheris won't random-walk to in 300 s).
- **Why 2 skip**: install failures, §0.5 above.
- **Actions**:
  1. Land **§0.5 vcfpy install fix** first (`--no-build-isolation`
     + GitHub-tarball fallback). Then the 2 skips convert to cells.
  2. Land §0.2 keep-going (atheris wraps libFuzzer so the same
     `-ignore_crashes=1` applies), §0.3 budget 7200 s, §0.4 PoV
     seed injection (critical for semantic-bug-adjacent
     `uncaught_exception`).
  3. Expected outcome after fixes: 3-4 of 4 `uncaught_exception`
     bugs detected; 0-1 of 3 `differential_disagreement` bugs
     (atheris has no differential oracle, so these are floors).
  4. Verify `fuzz_vcfpy.py` harness catches
     `vcfpy.exceptions.VCFPyException` AND `OSError` (it already
     does per Chat 3 artefacts — good).

### 3.2 `pure_random` (0 FOUND, 5 miss, 2 skip)

- Same install-failure skips; §0.5 resolves them.
- Scoring path is Chat 6 post-hoc replay.
- The pure_random corpus for vcfpy cells at 300 s is tiny; at
  7200 s it becomes usefully large.

---

## 4. Chat 4 — noodles VCF

**Already ran**: 12 cells at `BUDGET_S=300` across {cargo_fuzz,
pure_random}. Artefacts:
`compares/results/bug_bench_chat4_draft/`. Findings: cargo_fuzz
0 FOUND / 6 miss / 3 skip (harness-skew on 0.23/0.48 anchors);
pure_random mirrors.

### 4.1 `cargo_fuzz` (0 FOUND, 6 miss, 3 skip)

- **Why 0 FOUND** for the 6 miss cells: 8 of 9 target bugs are
  `differential_disagreement` — crash-finder can't see these.
  noodles-241 is the sole `uncaught_exception` and is the best
  candidate for cargo_fuzz to find at a longer budget. At 300 s
  without PoV seeding it's ~10× below the rediscovery floor for
  that bug's specific panic path.
- **Why 3 skip**: §0.6 harness version skew.
- **Actions**:
  1. Decide §0.6 Option A (accept skips, document) or B (per-
     version harness). For now — **Option A**.
  2. Land §0.2 keep-going, §0.3 budget 7200 s, §0.4 PoV seed
     injection. `compares/bug_bench/triggers/noodles-241/original.vcf`
     is the critical one for the `uncaught_exception` cell.
  3. Rebuild the fuzz target after the Cargo.toml pin swap — the
     driver's `_install_noodles` handles the canonical-JSON
     harness, but the cargo-fuzz target needs a separate
     `cargo fuzz build noodles_vcf_target --release --sanitizer none`
     per version. Add this to `_install_noodles` or make the
     cargo_fuzz adapter rebuild on first invocation per cell.
  4. Expected after fixes: 0-1 of 9 cells FOUND (noodles-241 at
     the 10-50 % rate, the 8 differential bugs stay at 0).

### 4.2 `pure_random` (0 FOUND, 6 miss, 3 skip)

- Same §0.6 harness-skew skips.
- Chat 6 post-hoc replay scores the remaining 6.

---

## 5. Chat 5 — biopython + seqan3 SAM (NOT YET RUN)

**Not yet executed.** When you run it, this chat covers 21 cells:
1 biopython bug × 3 tools + 6 seqan3 bugs × 3 tools.

Plan says {biotest, atheris/libfuzzer, pure_random}. **Drop
biotest**. Run {atheris (biopython), libfuzzer (seqan3),
pure_random (both)}. That's 14 cells:

- biopython × atheris: 1 cell
- biopython × pure_random: 1 cell
- seqan3 × libfuzzer: 6 cells
- seqan3 × pure_random: 6 cells

### 5.1 `atheris` (biopython, 1 cell)

- **Target bug**: biopython-4825 (1.85 → 1.86),
  `timeout_or_differential_disagreement`.
- **Actions**:
  1. Land §0.2 keep-going, §0.3 budget 7200 s, §0.4 PoV seed
     injection (`compares/bug_bench/triggers/biopython-4825/`).
  2. **Add timeout flag**: atheris supports `-timeout=N` (libFuzzer
     semantics). Since the signal type is
     `timeout_or_differential_disagreement`, set
     `-timeout=30` so per-input timeouts get logged as crashes
     (they're the signal).
  3. Verify the atheris venv has biopython installed:
     `/opt/atheris-venv/bin/python -c "import atheris, Bio"`. If
     not, pip-install biopython into the atheris venv then
     `docker commit` the container.
  4. Expected: 1/1 cell FOUND (timeout-type bugs are straightforward
     for atheris when `-timeout` is set).

### 5.2 `libfuzzer` (seqan3, 6 cells)

- **Target bugs**: all 6 are `differential_disagreement` (except
  -3406 = `intermittent_differential_disagreement`).
- **Why expected 0 FOUND**: crash-finder fundamentally cannot see
  differential bugs (literature argument — DESIGN §9 Risk 5 ¶2.4).
  Still worth running for the baseline comparison data.
- **Actions**:
  1. **Preflight**: seqan3 shallow clone must contain all 10 commit
     SHAs. Check via:
     ```bash
     cd compares/baselines/seqan3/source
     for sha in df9fd5ff 8e374d7c fa221c13 c84f5671 ca4d6683 \
                11564cb3 4961904f 4fe54891 edbfa956f 745c645f 5e5c05a4; do
       git cat-file -e ${sha}^{commit} 2>/dev/null \
         || echo "MISSING: ${sha}"
     done
     ```
     If any missing: `git fetch --unshallow`.
  2. The seqan3 **libfuzzer harness must be rebuilt per pre-fix
     commit** because seqan3 is header-only — different commits
     produce binary-incompatible harnesses. Either:
     - Add a per-commit rebuild step to
       `bug_bench_driver.py::_checkout_seqan3` (currently it only
       does `git checkout -f <sha>`; it doesn't rebuild the
       harness).
     - Or run `bash compares/scripts/build_harnesses.sh --only-seqan3`
       after each checkout. Slow but correct.
  3. Land §0.2 keep-going, §0.3 budget 7200 s, §0.4 PoV seed
     injection.
  4. Expected: 0-1 of 6 cells FOUND (the one
     `intermittent_differential_disagreement` bug might surface as
     a crash).

### 5.3 `pure_random` (biopython + seqan3, 7 cells)

- Same pattern as 1.3 / 2.3 / 3.2 / 4.2. Chat 6 scores.

### 5.4 Run command (baseline-only)

```bash
docker exec -d biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  rm -rf /tmp/bug_bench_chat5
  mkdir -p /tmp/bug_bench_chat5
  BUDGET_S=${BUDGET_S:-7200}
  export BUDGET_S
  echo "[chat5] budget=${BUDGET_S}s start=$(date -u +%FT%TZ)" \
       >> /tmp/phase4-chat5.log

  # biopython × atheris, pure_random (drop biotest)
  for TOOL in atheris pure_random; do
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut biopython --only-tool ${TOOL} \
      --time-budget-s ${BUDGET_S} \
      --out /tmp/bug_bench_chat5 \
      >> /tmp/phase4-chat5.log 2>&1
  done

  # seqan3 × libfuzzer, pure_random (drop biotest)
  for TOOL in libfuzzer pure_random; do
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut seqan3 --only-tool ${TOOL} \
      --time-budget-s ${BUDGET_S} \
      --out /tmp/bug_bench_chat5 \
      >> /tmp/phase4-chat5.log 2>&1
  done

  echo "[chat5] end=$(date -u +%FT%TZ)" >> /tmp/phase4-chat5.log
  python3.12 compares/scripts/rollup_bug_bench.py \
    --bench-root /tmp/bug_bench_chat5 \
    --out /tmp/bug_bench_chat5/aggregate.json
'
```

---

## 6. Chat 6 — post-processing (NOT YET RUN)

**Not yet executed.** This is the chat that **converts every
pure_random `miss` into a real score** via post-hoc replay. Without
it, every pure_random cell across Chats 1-5 reads `miss` forever.

### 6.1 Write the post-hoc replay script

`compares/scripts/pure_random_replay.py` — walks
`compares/results/bug_bench/pure_random/<bug_id>/corpus/*.{vcf,sam}`
and runs each input through the bug's SUT `ParserRunner` with a
short per-input timeout, both pre-fix and post-fix. Apply the
§5.3.1 three-condition predicate:

- A corpus file `F` counts as a DETECT for pure_random @ bug B iff
  `signal(F, V_pre) = true AND signal(F, V_post) = false`.
- `signal` = "ParserRunner raised an exception" (Miller CACM'90
  schema per DESIGN §4.3).

Output: update each pure_random cell's `result.json` to
`detected=true, trigger_input=<path>, confirmed_fix_silences_signal=true`
if any corpus file qualifies. Write a per-cell
`post_hoc_replay_summary.json` with counts.

### 6.2 Write the rollup

`compares/scripts/rollup_bug_bench.py` — see the spec in
`PHASE4_EXECUTION_PLAN.md §"Chat 6"`. Simple glob + JSON concat.

### 6.3 Run the Fairness Equalizer

`compares/scripts/fairness_equalizer.py` already exists (per DESIGN
§4.4). Runs in ~10 min per tool. **This is the other big scoring
lift** — it re-feeds every tool's accepted corpus through BioTest's
differential-only oracle, crediting each tool with the disagreements
its inputs caused. Without biotest running as a generator, the
equalizer still produces meaningful scores for jazzer/atheris/
libfuzzer/cargo_fuzz/pure_random because it's the **oracle** that's
shared, not the generator.

### 6.4 Merge everything into the canonical tree

```bash
docker exec biotest-bench-setup bash -c '
  DST=/work/compares/results/bug_bench
  mkdir -p ${DST}
  # Merge all chat outputs
  for SRC in /work/compares/results/bug_bench_chat1_draft \
             /work/compares/results/bug_bench_chat2_draft \
             /work/compares/results/bug_bench_chat3_artefacts \
             /work/compares/results/bug_bench_chat4_draft \
             /tmp/bug_bench_chat5; do
    test -d ${SRC} && rsync -a ${SRC}/ ${DST}/
  done

  # Post-hoc replay (converts pure_random miss → scored cell)
  python3.12 /work/compares/scripts/pure_random_replay.py \
    --bench-root ${DST}

  # Rollup
  python3.12 /work/compares/scripts/rollup_bug_bench.py \
    --bench-root ${DST} --out ${DST}/aggregate.json

  # Fairness equalizer
  python3.12 /work/compares/scripts/fairness_equalizer.py \
    --bench-root ${DST} --out ${DST}/fairness_equalizer

  # Review
  python3.12 /work/compares/scripts/post_run_review.py \
    --bench-root ${DST} --spot-check 5
'

bash compares/scripts/backup_bug_bench.sh
```

### 6.5 Deferred: DESIGN.md §13.5 Phase 4 checkboxes

Don't flip them yet. Reason: biotest is still in development per
operator. When biotest lands and you re-run Phase 4 with the full
matrix, that's the moment to mark boxes. For now, add a note under
the Phase 4 header:

```
> **Baseline-only status 2026-04-21**: Chats 1-4 ran at BUDGET_S=300
> across jazzer/atheris/cargo_fuzz/evosuite_anchor/pure_random.
> Zero FOUND cells — diagnosis in compares/PHASE4_DIAGNOSIS.md + §9
> Risk 5. biotest deferred until main BioTest pipeline matures.
> Chat 5 (biopython + seqan3 baselines) + Chat 6 (post-hoc replay +
> equalizer) pending. Full Phase 4 completion blocked on biotest.
```

---

## 7. Priority order if time is limited

If you can only do 2-3 things, do these in order:

1. **§0.1 seed sanitization** (20 min) — eliminates the Chat-2 class
   of poison-seed budget waste for every chat.
2. **§0.4 PoV seed injection** (1 h engineering) — largest leverage
   on crash-finder detection rate; transforms Chat 1/2/3/4/5 from
   "rediscover bug from scratch" to "mutate around a known
   trigger".
3. **§0.3 budget bump to 7200 s + rerun Chat 5** — completes the
   baseline coverage; gives you real numbers for the paper draft.

Everything else (§0.2 keep-going, §0.5 vcfpy install, §0.6 noodles
per-version, §0.7 EvoSuite budget) is secondary polish.

**Non-priority but valuable side outputs**:
- The `oneAllele:582` IOOBE in htsjdk is an undisclosed latent bug
  surfaced by jazzer during Chat 1. Filing an upstream PR is free
  lifting for the paper draft ("our benchmark methodology found an
  unrelated real bug").
