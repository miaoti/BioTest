# Phase 4 Execution Plan — 117 cells, multi-chat split

**Status**: Authored 2026-04-20. Supersedes inline Phase-4 instructions
in `compares/DESIGN.md §13.5` for the question "how do I actually run
this across multiple sessions". The DESIGN.md checkboxes remain the
system of record for completion.

## 1. Time estimates

Pure walltime excluding operator break time. All estimates assume the
post-2026-04-20 driver fixes are in place (idempotent noodles pin
rewriter, `PATH=/root/.cargo/bin:$PATH` env injection, `bug_reports/`
snapshot-before-harvest, `verify_bug(install=False)` default, seed
symlink instead of copy).

### Per-cell base timings

| tool            | startup | fuzz budget | per-cell total (B=60) | per-cell total (B=300) | per-cell total (B=7200) |
| :-------------- | ------: | ----------: | --------------------: | ---------------------: | ----------------------: |
| biotest         |      5s | budget-bound at ≥300s, `--dry-run` <300s | ~6s | ~320s (boot + Phase C) | ~7210s |
| pure_random     |      1s | budget-bound | ~61s | ~301s | ~7201s |
| atheris         |     15s | budget-bound | ~76s | ~316s | ~7216s |
| jazzer          |     25s | budget-bound | ~86s | ~326s | ~7226s |
| libfuzzer       |      8s | budget-bound | ~69s | ~309s | ~7209s |
| cargo_fuzz      |      8s | budget-bound | ~69s | ~309s | ~7209s |
| evosuite_anchor |     60s | budget-bound | ~120s (short regime) | ~360s | ~7260s |

### Per-swap install timings (anchor-grouped)

| SUT       | swap cost | # swaps | subtotal |
| :-------- | --------: | ------: | -------: |
| htsjdk    |      ~4s  |   16×2  |   2 min  |
| vcfpy     |     ~12s  |    6×2  |   2 min  |
| biopython |     ~12s  |    1×2  |  24s     |
| noodles   |     ~45s  |    8×2  |  12 min  |
| seqan3    |      ~2s  |    6×2  |  24s     |
| **Total (27 anchor groups)** | | | **~17 min** |

Swap count is "install pre_fix once per anchor group + install post_fix
once per anchor group". noodles-223 + noodles-224 share the 0.48→0.49
anchor → counted once. Similar for the 2 noodles 0.63→0.64 pair and
the 4-bug + 3-bug htsjdk groups.

### Aggregate walltime per budget

| budget  | per-cell avg | 117 cells + swaps | 4-way parallel | chats needed |
| :------ | -----------: | ----------------: | -------------: | -----------: |
| **60s  smoke**        | ~70s   | ~2.3h  | ~45 min | **1 chat, tight** |
| **300s reduced**      | ~315s  | ~10.2h | ~2.6h   | **2 chats** |
| **1800s half-hour**   | ~1815s | ~60h   | ~15h    | **4 chats** |
| **7200s production**  | ~7215s | ~237h  | ~60h    | **6+ chats** |

The "60s smoke" regime is what got 90% of the way through in the
2026-04-20 first attempt before I/O issues killed it; with the
`bug_reports/` harvest fix it now completes in ~2 hours end-to-end.

## 2. How detection is defined per tool

All adapters share the `AdapterResult` schema (see
`compares/scripts/tool_adapters/_base.py`). The driver's universal
detection predicate is

```
detected  =  adapter_json["crash_count"] > 0
```

which keys off files in `<cell>/crashes/`. Every crash-finding adapter
(jazzer, atheris, libfuzzer, cargo_fuzz) writes crash inputs there;
evosuite_anchor writes `failing-tests/` which its harness maps into
`crashes/`. `pure_random` and `biotest` need per-tool rules.

### Per-tool detection rules

| tool            | detection trigger inside the adapter |
| :-------------- | :----------------------------------- |
| **biotest**     | counts NEW entries in `bug_reports/` produced during the run (snapshot diff; fixed 2026-04-20). Additionally, `data/det_report.json` entries with non-null signal. Either signals `crash_count ≥ 1`. |
| **jazzer**      | libFuzzer-style artifact files under `-artifact_prefix=<crashes_dir>/`. Each `crash-*` file counts as 1. |
| **atheris**     | libFuzzer-style artifact files (Atheris wraps libFuzzer). Each `crash-*` / `timeout-*` / `leak-*` file counts. |
| **libfuzzer**   | libFuzzer-style artifact files. |
| **cargo_fuzz**  | libFuzzer-style artifact files (cargo-fuzz wraps libFuzzer with a Rust target binary). |
| **pure_random** | no intrinsic detection — post-hoc replay of `corpus/` through the SUT's `ParserRunner`. `post_run_review.py --spot-check` handles this. |
| **evosuite_anchor** | `failing-tests/` directory non-empty after the GA search. |

### Tool-found-the-bug definition (full pipeline)

A (tool, bug) cell is scored as **"tool found the bug in SUT"** iff
**all three** conditions hold:

1. `adapter_json.crash_count > 0` after the pre-fix run.
2. `result.trigger_input` is a file on disk (the driver picks the first
   file in `crashes/` as the canonical sample).
3. `result.confirmed_fix_silences_signal == True` — the post-fix SUT
   parses/handles the trigger input cleanly via `ParserRunner.run()`.

`confirmed_fix_silences_signal == None` means we detected a crash but
could not replay against post-fix (missing trigger file, post-fix
install failed, no runner for this SUT). These cells need manual
spot-check — `post_run_review.py` lists them under `null_silences`.

`confirmed_fix_silences_signal == False` means the post-fix version
STILL crashes on the trigger — either the fix didn't land where we
expect, or the crash is unrelated to the target bug. These cells are
ambiguous and need manual triage.

### Expected signals per bug

Every bug in the manifest carries `expected_signal.type`:

- `differential_disagreement` — oracle voter disagreement between the
  SUT under test and the other voter (pysam / htslib). BioTest's
  primary signal path. Crash-finding fuzzers surface it indirectly via
  an uncaught exception or a runner-side timeout.
- `uncaught_exception` — SUT throws a parse-time exception that
  propagates past its try/catch barrier. Direct for fuzzers.
- `timeout_or_differential_disagreement` — either is acceptable.
- `intermittent_differential_disagreement` — flaky; the driver records
  the finding but a single negative doesn't invalidate the cell.

The crash-finding tools all fire on `uncaught_exception`. For
`differential_disagreement` bugs only `biotest` has a native signal;
other tools will register the bug only if the disagreement *also*
produces a crash in one of the voters (common for parser bugs, not
universal).

## 3. Multi-chat split

Each chat should be self-contained: the Docker image + manifest +
adapters + harnesses are already baked, the driver's CLI lets a chat
run exactly one `--only-sut` / `--only-tool` slice and produce
per-cell JSON records.

The split below assumes B=300s (reduced proof-of-execution budget).
For B=7200s production, double or triple each chat's walltime and
consider splitting the larger slices further.

### Chat 1 — htsjdk VCF/SAM × {biotest, jazzer, pure_random}
- Cells: 12 bugs × 3 tools = **36 cells**
- Estimated walltime at B=300s: **~3.5 hours**
- Estimated walltime at B=7200s: **~72 hours** (split this chat further for production)

Command:
```bash
docker exec biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  for tool in biotest jazzer pure_random; do
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut htsjdk --only-tool $tool \
      --time-budget-s 300 \
      --out /tmp/bug_bench_chat1_${tool} \
      2>&1 | tee -a /tmp/phase4-chat1.log
  done
'
```

After it finishes, sync results to the host:
```bash
docker exec biotest-bench-setup bash -c \
  'rsync -a /tmp/bug_bench_chat1_* /work/compares/results/bug_bench/'
```

Bugs covered (all htsjdk):

| bug_id      | fmt | pre_fix→post_fix | expected_signal            |
| :---------- | :-- | :--------------- | :------------------------- |
| htsjdk-1364 | VCF | 2.19.0 → 2.20.0  | differential_disagreement  |
| htsjdk-1389 | VCF | 2.19.0 → 2.20.0  | differential_disagreement  |
| htsjdk-1372 | VCF | 2.19.0 → 2.20.0  | differential_disagreement  |
| htsjdk-1401 | VCF | 2.19.0 → 2.20.0  | differential_disagreement  |
| htsjdk-1403 | VCF | 2.20.0 → 2.20.1  | differential_disagreement  |
| htsjdk-1418 | VCF | 2.20.1 → 2.21.0  | **uncaught_exception**     |
| htsjdk-1544 | VCF | 2.24.1 → 3.0.0   | differential_disagreement  |
| htsjdk-1554 | VCF | 2.24.1 → 3.0.0   | differential_disagreement  |
| htsjdk-1637 | VCF | 3.0.3 → 3.0.4    | differential_disagreement  |
| htsjdk-1489 | SAM | 2.22.0 → 2.23.0  | differential_disagreement  |
| htsjdk-1538 | SAM | 2.24.0 → 2.24.1  | differential_disagreement  |
| htsjdk-1561 | SAM | 2.24.1 → 3.0.0   | differential_disagreement  |

Tool-cell detection rules: jazzer/pure_random use `crash_count > 0`
from `crashes/`; biotest uses bug_reports/ snapshot-diff and/or DET
report. Post-fix replay uses `test_engine.runners.htsjdk_runner`.

### Chat 2 — htsjdk × evosuite_anchor (white-box anchor)
- Cells: 12 bugs × 1 tool = **12 cells**
- Estimated walltime at B=300s: **~1.5 hours** (EvoSuite boot is heavier)
- Estimated walltime at B=7200s: **~24 hours**

Kept as its own chat because EvoSuite is the ONE white-box baseline
(DESIGN.md §4.2); its adapter path uses `run_evosuite.sh` rather than
the Python adapter shim and needs its own JAR in
`compares/baselines/evosuite/`.

Command:
```bash
docker exec biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.verified.json \
    --only-sut htsjdk --only-tool evosuite_anchor \
    --time-budget-s 300 \
    --out /tmp/bug_bench_chat2 \
    2>&1 | tee /tmp/phase4-chat2.log
'
```

Bugs: same 12 as Chat 1.

Detection: `failing-tests/` non-empty after the GA run. Detection rule
is "post-fix htsjdk still fails the EvoSuite-generated JUnit cases that
pre-fix failed" — `run_evosuite.sh` handles this internally and
writes `detection_metadata.json`.

### Chat 3 — vcfpy × {biotest, atheris, pure_random}
- Cells: 7 bugs × 3 tools = **21 cells**
- Estimated walltime at B=300s: **~2 hours**
- Estimated walltime at B=7200s: **~42 hours**

Command:
```bash
docker exec biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  for tool in biotest atheris pure_random; do
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut vcfpy --only-tool $tool \
      --time-budget-s 300 \
      --out /tmp/bug_bench_chat3_${tool} \
      2>&1 | tee -a /tmp/phase4-chat3.log
  done
'
```

Bugs:

| bug_id            | fmt | pre_fix→post_fix | expected_signal            |
| :---------------- | :-- | :--------------- | :------------------------- |
| vcfpy-176         | VCF | 0.13.8 → 0.14.0  | **uncaught_exception**     |
| vcfpy-171         | VCF | 0.13.8 → 0.14.0  | differential_disagreement  |
| vcfpy-146         | VCF | 0.13.3 → 0.13.4  | **uncaught_exception**     |
| vcfpy-145         | VCF | 0.13.4 → 0.13.5  | **uncaught_exception**     |
| vcfpy-gtone-0.13  | VCF | 0.12.1 → 0.12.2  | differential_disagreement  |
| vcfpy-127         | VCF | 0.11.0 → 0.11.1  | **uncaught_exception**     |
| vcfpy-nocall-0.8  | VCF | 0.8.1  → 0.9.0   | differential_disagreement  |

Detection: atheris/pure_random use `crash_count > 0`; biotest uses
bug_reports/ snapshot-diff. Post-fix replay uses vcfpy via the vcfpy
runner (note: there's no dedicated `test_engine.runners.vcfpy_runner`
yet — replay falls through the generic ParserRunner contract; see
`_replay_trigger_silenced` in bug_bench_driver.py, which currently
returns `False` for `sut == "vcfpy"` because its `elif` ladder hasn't
added vcfpy yet. **Chat 3 must first add a vcfpy branch to
`_replay_trigger_silenced`** or the `confirmed_fix_silences_signal`
field will always read `False` for vcfpy detections).

Uncaught-exception bugs (vcfpy-146, -145, -127, -176) are the easiest
targets for the fuzzer-style tools — a single malformed VCF line
surfaces the bug. `differential_disagreement` bugs (vcfpy-171, -gtone,
-nocall) will score only for biotest unless the disagreement also
raises a Python exception.

### Chat 4 — noodles × {biotest, cargo_fuzz, pure_random}
- Cells: 9 bugs × 3 tools = **27 cells**
- Estimated walltime at B=300s: **~2.5 hours**
- Estimated walltime at B=7200s: **~55 hours**

Command:
```bash
docker exec biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  for tool in biotest cargo_fuzz pure_random; do
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut noodles --only-tool $tool \
      --time-budget-s 300 \
      --out /tmp/bug_bench_chat4_${tool} \
      2>&1 | tee -a /tmp/phase4-chat4.log
  done
'
```

Bugs:

| bug_id                | fmt | pre_fix→post_fix | expected_signal            | known notes |
| :-------------------- | :-- | :--------------- | :------------------------- | :---------- |
| noodles-300           | VCF | 0.63 → 0.64      | differential_disagreement  |             |
| noodles-339           | VCF | 0.81 → 0.82      | differential_disagreement  |             |
| noodles-268           | VCF | 0.57 → 0.58      | differential_disagreement  |             |
| noodles-223           | VCF | 0.48 → 0.49      | differential_disagreement  | *see harness-skew below* |
| noodles-224           | VCF | 0.48 → 0.49      | differential_disagreement  | *see harness-skew below* |
| noodles-259           | VCF | 0.55 → 0.56      | differential_disagreement  |             |
| noodles-241           | VCF | 0.58 → 0.59      | **uncaught_exception**     |             |
| noodles-inforay-0.64  | VCF | 0.63 → 0.64      | differential_disagreement  |             |
| noodles-ob1-0.23      | VCF | 0.23 → 0.24      | differential_disagreement  | *see harness-skew below* |

**Harness-skew caveat**: the canonical-JSON harness
(`harnesses/rust/noodles_harness/src/main.rs`) and the cargo-fuzz
target (`compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs`)
were written against noodles-vcf 0.70 API and may not compile against
0.23 / 0.48. When `cargo build --release --manifest-path ...` fails
under `_install_noodles`, the anchor-group loop records an install
error for every bug in that group and moves on — these cells will show
up in aggregate.json with a top-level `"error": "install pre_fix ... failed"`.

Detection: cargo_fuzz/pure_random use `crash_count > 0`; biotest uses
bug_reports/. Post-fix replay: `_replay_trigger_silenced` has no
noodles branch yet (same gap as vcfpy). **Chat 4 must add a noodles
branch to `_replay_trigger_silenced`** using a subprocess invocation
of the canonical-JSON Rust harness to validate the trigger on post-fix.

### Chat 5 — biopython + seqan3 × {biotest, atheris/libfuzzer, pure_random}
- Cells: (1 biopython × 3 tools) + (6 seqan3 × 3 tools) = 3 + 18 = **21 cells**
- Estimated walltime at B=300s: **~2 hours**
- Estimated walltime at B=7200s: **~42 hours**

Command:
```bash
docker exec biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  for sut in biopython seqan3; do
    for tool in biotest pure_random; do
      python3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.verified.json \
        --only-sut $sut --only-tool $tool \
        --time-budget-s 300 \
        --out /tmp/bug_bench_chat5_${sut}_${tool} \
        2>&1 | tee -a /tmp/phase4-chat5.log
    done
  done
  python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.verified.json \
    --only-sut biopython --only-tool atheris \
    --time-budget-s 300 \
    --out /tmp/bug_bench_chat5_biopython_atheris \
    2>&1 | tee -a /tmp/phase4-chat5.log
  python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.verified.json \
    --only-sut seqan3 --only-tool libfuzzer \
    --time-budget-s 300 \
    --out /tmp/bug_bench_chat5_seqan3_libfuzzer \
    2>&1 | tee -a /tmp/phase4-chat5.log
'
```

biopython bugs (1):

| bug_id           | fmt | pre_fix→post_fix | expected_signal                     |
| :--------------- | :-- | :--------------- | :---------------------------------- |
| biopython-4825   | SAM | 1.85 → 1.86      | timeout_or_differential_disagreement |

seqan3 bugs (6):

| bug_id        | fmt | pre_fix (commit SHA)                    | post_fix (commit SHA)                   | expected_signal            |
| :------------ | :-- | :-------------------------------------- | :-------------------------------------- | :------------------------- |
| seqan3-2418   | SAM | `df9fd5ff64f59fdb124c4a564a4141d1f9cff22b` | `8e374d7ce7a1ce4de0077bc3698d5ae2c8e79600` | differential_disagreement  |
| seqan3-3081   | SAM | `fa221c1302cfe515211ea70de375a1802826d3d9` | `c84f5671665478ec1b71535201cbffbe1fdd8c82` | differential_disagreement  |
| seqan3-3269   | SAM | `ca4d668390e35b4045ccd02d070927f8178ed2ce` | `11564cb3bcea39666d6d3979080bc5d8fdbe1d7e` | differential_disagreement  |
| seqan3-3098   | SAM | `4961904fbc3b254f7a611b5b467c2e33ae5b1042` | `4fe548913e96d3f908dd524bd3dc13b48f87bfa4` | differential_disagreement  |
| seqan3-2869   | SAM | `edbfa956f^` (parent)                    | `edbfa956f`                              | differential_disagreement  |
| seqan3-3406   | SAM | `745c645fe26272791464cd67180775d28c00bf28` | `5e5c05a471269703d7afc38bdc4348cef60be63b` | intermittent_differential_disagreement |

seqan3 swaps are `git checkout -f <sha>` in the shallow clone under
`compares/baselines/seqan3/source/`. If the shallow clone (depth 50)
doesn't contain a commit, `install_sut` will raise and the driver will
skip that anchor — deepen the clone with `git fetch --unshallow` in
the container if needed.

Detection:
- biopython/seqan3 × atheris|libfuzzer: `crash_count > 0`
- biotest: bug_reports/ snapshot-diff
- Post-fix replay: runners exist (`biopython_runner`, `seqan3_runner`)
  so `confirmed_fix_silences_signal` will be `True`/`False` rather than
  `None`.

### Chat 6 — Post-run review, backup, DESIGN.md update
- No fuzzing; pure post-processing.
- Estimated walltime: **~15 minutes**.

Depends on Chats 1-5 writing results into
`compares/results/bug_bench/`.

Steps:
```bash
# 1. Merge all chat outputs into one canonical results dir
docker exec biotest-bench-setup bash -c '
  rsync -a /tmp/bug_bench_chat*/ /work/compares/results/bug_bench/
  # Rebuild the aggregate.json by walking result.json files
  python3.12 /work/compares/scripts/rollup_bug_bench.py \
      --bench-root /work/compares/results/bug_bench \
      --out /work/compares/results/bug_bench/aggregate.json
'

# 2. Post-run review + spot-check
docker exec biotest-bench-setup bash -c '
  cd /work && python3.12 compares/scripts/post_run_review.py \
      --bench-root compares/results/bug_bench --spot-check 3
'

# 3. Backup off-machine
bash compares/scripts/backup_bug_bench.sh

# 4. Update DESIGN.md §13.5 Phase 4 checkboxes
```

`rollup_bug_bench.py` doesn't exist yet — the last chat creates it
from the same `result.json` schema the driver writes. Simple glob +
json.load + concat into `aggregate.json`.

## 4. Single-chat execution (if the operator chooses)

If all six chats feel heavier than running it all at once:

- **Budget = 60s** (smoke-only): ~2 hours in one chat. Validates the
  pipeline end-to-end and scores `uncaught_exception` bugs. Misses
  most `differential_disagreement` bugs because 60 s isn't enough for
  a fuzzer to explore.
- **Budget = 300s** (reduced): ~10 hours in one chat. Too long.
- **Budget = 7200s** (production): ~60 hours @ 4-way. Don't.

Single-chat, B=60s command:
```bash
docker exec biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.verified.json \
    --time-budget-s 60 \
    --out /tmp/bug_bench_all \
    2>&1 | tee /tmp/phase4-single-chat.log
  rsync -a /tmp/bug_bench_all/ /work/compares/results/bug_bench/
'
```

## 5. Checklist of what is in place vs. what each chat must do first

### Already satisfied (do NOT redo)
- Docker image `biotest-bench:latest` with Rust + cargo-fuzz + vcfpy baked in.
- `compares/results/sut-envs/` has pysam, biopython, vcfpy venvs.
- `compares/bug_bench/manifest.verified.json` frozen at 35 bugs.
- Adapters for all seven tools present under `compares/scripts/tool_adapters/`.
- Harnesses: `compares/harnesses/atheris/fuzz_{pysam,biopython,vcfpy}.py`;
  `compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs`;
  `compares/harnesses/libfuzzer/seqan3_sam_fuzzer.cpp`;
  `harnesses/java/BioTestHarness.java` (JDK-17 class file).
- Seed corpora: `compares/results/bench_seeds/vcf` (33), `...sam` (46).
- Driver fixes landed 2026-04-20:
  - `_rewrite_noodles_pin` is idempotent (no-op if already target version)
  - `_install_noodles` injects `/root/.cargo/bin` into subprocess PATH
  - `verify_bug` defaults to metadata-only (no double-install)
  - `run_biotest.py` snapshots `bug_reports/` before the run and
    harvests only new entries
  - `run_biotest.py` symlinks seeds instead of copying
- `compares/scripts/post_run_review.py` and
  `compares/scripts/backup_bug_bench.sh` present and tested on the
  smoke-test output.

### Each chat must verify
- `docker ps | grep biotest-bench-setup` returns a row (container is up).
- `/work/compares/results/sut-envs/vcfpy/bin/python` exists (if it doesn't,
  run `prepare_sut_install_envs.sh` inside the container).
- `/root/.cargo/bin/cargo-fuzz` exists (if not, re-run the cargo-install
  stanza from `compares/docker/Dockerfile.bench`).
- `/tmp/bug_bench_chat*` does NOT already exist (rm -rf if it does —
  we use fresh dirs per chat to avoid mixing prior runs).

### Each chat's concrete outputs
- Per-cell files: `/tmp/bug_bench_chat<N>_<tool>/<tool>/<bug_id>/result.json`
- Per-cell artifacts: `/tmp/bug_bench_chat<N>_<tool>/<tool>/<bug_id>/{corpus,crashes,tool.log}`
- Per-chat aggregate: `/tmp/bug_bench_chat<N>_<tool>/aggregate.json`
- Per-chat log: `/tmp/phase4-chat<N>.log`

Chat 6 merges everything into `compares/results/bug_bench/` and writes:
- `compares/results/bug_bench/aggregate.json` (unified)
- `compares/results/bug_bench/post_run_review.json` + `.md`
- `compares/results/backups/bug_bench-<timestamp>.tar.zst`

## 6. Common failure modes and how to recognize them

| symptom in log | root cause | fix |
| :------------- | :--------- | :-- |
| `[skip] noodles-XXX: install failed: ... cargo: not found` | PATH missing /root/.cargo/bin | `export PATH=/root/.cargo/bin:$PATH` before `python3.12 ...` (already done in chat commands above) |
| `[skip] noodles-XXX: install failed: could not find noodles-vcf version pin` | non-idempotent rewriter bug (pre-2026-04-20) | ensure the driver has the `re.subn` patch |
| driver hangs on `[run] biotest @ ...` with 0% CPU | 9p-mount I/O storm from bug_reports/ harvest | ensure `run_biotest.py` has the snapshot-before-harvest patch |
| driver hangs on `[run] biotest @ ...` with non-zero CPU | Phase C boot (normal at B≥300s; takes 2-5 min before fuzzing begins) | wait |
| `[skip] seqan3-XXX: install failed: ... commit not in shallow clone` | shallow clone depth too small | `git -C compares/baselines/seqan3/source fetch --unshallow` |
| `adapter_raise: FileNotFoundError: cargo-fuzz binary` | fuzz target not built | `cargo fuzz build noodles_vcf_target --release --sanitizer none --manifest-path compares/harnesses/cargo_fuzz/fuzz/Cargo.toml` |
| all atheris cells score 0 detections | atheris venv path mismatch | verify `/opt/atheris-venv/bin/python` exists and has atheris + vcfpy installed |

## 7. Recommendation

1. **If single session is available for ~2.5 hours continuous**: run the
   single-chat B=60s command from §4 as the proof-of-execution. Mark
   DESIGN.md §13.5 Phase 4 boxes [x] with the 60s-budget caveat.
2. **If full production quality matters**: split into 6 chats (§3) at
   B=7200s, spread over ~3 calendar days with 4-way parallelism across
   machines. Chat 6 consolidates.
3. **Compromise (recommended default)**: 6 chats at B=300s. ~10 hours
   total walltime, but each chat is ~1.5-3 hours — fits comfortably in
   one session each. Results are qualitatively equivalent to B=7200s
   for detection (TTFB in short-regime will differ).

For the current session I recommend option 1 (single-chat B=60s) so
the DESIGN.md boxes get checked today, then a future production run at
B=7200s can re-attach more precise TTFB numbers.
