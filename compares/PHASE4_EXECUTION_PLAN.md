# Phase 4 Execution Plan — 6-chat production split

**Authored**: 2026-04-20.
**Scope**: `compares/DESIGN.md §13.5 Phase 4` — real-bug benchmark
over the 35-bug frozen manifest, 117 cells, multi-day run.
**System of record for completion**: the `[ ]` → `[x]` checkboxes in
`compares/DESIGN.md §13.5 Phase 4`. This document is the runbook; the
DESIGN.md boxes are the final deliverable.

---

## Top-level split

| chat | SUT × format               | bugs | tools                                  | cells | ~walltime B=300s | ~walltime B=7200s |
| :--- | :------------------------- | :--: | :------------------------------------- | :---: | ---------------: | ----------------: |
| 1    | htsjdk VCF                 |  9   | biotest, jazzer, pure_random, evosuite |  36   | 3.5 h            | ~72 h  (≈3 d)     |
| 2    | htsjdk SAM                 |  3   | biotest, jazzer, pure_random, evosuite |  12   | 1.2 h            | ~24 h  (≈1 d)     |
| 3    | vcfpy VCF                  |  7   | biotest, atheris, pure_random          |  21   | 2.0 h            | ~42 h             |
| 4    | noodles VCF                |  9   | biotest, cargo_fuzz, pure_random       |  27   | 2.5 h            | ~54 h             |
| 5    | biopython SAM + seqan3 SAM |  7   | biotest, atheris/libfuzzer, pure_random|  21   | 2.0 h            | ~42 h             |
| 6    | (post-processing)          |  —   | rollup + review + backup + DESIGN.md   |   —   | 0.25 h           | 0.25 h            |

**Budget knob** (all chats): set `$BUDGET_S` before running. Three
supported regimes — `60` (smoke, single-chat compatible), `300`
(reduced proof-of-execution), `7200` (DESIGN.md production target).

**Parallelism model**: Chats 1-5 are independent — run them in any
order, on any machine, even simultaneously if the operator has the
cores. Chat 6 is a strict barrier: it depends on Chats 1-5 having
written their results into the canonical `compares/results/bug_bench/`
tree on the shared `/work` volume.

---

## Global context (all chats start here)

### What Phase 4 does

For every bug in `compares/bug_bench/manifest.verified.json`, for every
fuzzer/harness eligible for that bug's SUT row in the `MATRIX` dict,
the driver `compares/scripts/bug_bench_driver.py`:

1. Installs the pre-fix SUT version (pip / Maven / Cargo / git checkout).
2. Runs the tool against the pre-fix SUT for `--time-budget-s` seconds.
3. Records whether any crash / disagreement / exception fired and
   (if so) what the minimal triggering input was.
4. Installs the post-fix SUT version.
5. Replays the triggering input; confirms the signal silences.
6. Writes per-cell `result.json` + `aggregate.json` rollup.

The manifest has been **frozen at 35 bugs** (2026-04-20 pysam-demotion
refactor): htsjdk 12, vcfpy 7, noodles 9, biopython 1, seqan3 6.

### What's already done (do NOT redo)

- Docker image `biotest-bench:latest` with JDK 17, Python 3.11 + 3.12,
  Clang 18 + libFuzzer, AFL++, Rust stable + cargo-fuzz + cargo-llvm-cov
  + cargo-mutants, mull, EvoSuite baked in.
- `compares/results/sut-envs/{pysam,biopython,vcfpy}/` — 3.11 venvs.
- `compares/bug_bench/manifest.verified.json` frozen, 35 bugs.
- `compares/results/bench_seeds/{vcf,sam}/` — 33 + 46 seed inputs.
- Harnesses: `compares/harnesses/atheris/fuzz_{pysam,biopython,vcfpy}.py`,
  `compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs`,
  `compares/harnesses/libfuzzer/seqan3_sam_fuzzer.cpp`,
  `harnesses/java/BioTestHarness.java` (JDK-17 class file v61).
- Driver fixes landed 2026-04-20:
  - `_rewrite_noodles_pin` is idempotent (`re.subn` match-count check).
  - `_install_noodles` injects `/root/.cargo/bin` into subprocess PATH.
  - `verify_bug(install=False)` by default (no redundant pre-install).
  - `run_biotest.py` snapshots `bug_reports/` before the run and
    harvests only new entries (52k-dir I/O storm fixed).
  - `run_biotest.py` symlinks seeds rather than copying.
- Tool adapters present under `compares/scripts/tool_adapters/`:
  `run_{biotest,jazzer,atheris,libfuzzer,aflpp,cargo_fuzz,pure_random}.py`.
- Post-processing scripts: `compares/scripts/post_run_review.py`,
  `compares/scripts/backup_bug_bench.sh`.

### Global detection semantics

See `compares/DESIGN.md §5.3.1 "Formal detection predicate"` for the
full formalisation and citations. Short version:

> `detects(T, B) := ∃ input I produced by T during its budget-bounded
>                  run on V_pre such that
>                  signal_T(I, V_pre) = true AND
>                  signal_T(I, V_post) = false.`

`signal_T` varies per tool class; see `DESIGN.md §4.3` for the
per-tool row. The predicate is grounded in:

- **Magma** (Hazimeh, Herrera, Payer — SIGMETRICS'20) — canonical
  ground-truth fuzzing benchmark; source of the pre-fix / post-fix
  anchor + silence-on-fix protocol.
- **FuzzBench** (Metzman et al. — OOPSLA'21) — industry-standard
  comparator benchmark; uses the same predicate.
- **LAVA** (Dolan-Gavitt et al. — S&P'16) — motivates the silence-on-
  fix confirmation via ground-truth bug inoculation.
- **Klees et al.** (CCS'18 §3.1-§3.2) — "raw crash counts over-count
  unique bugs" — motivates requiring both clauses of the predicate
  rather than `crash_count > 0` alone.
- **Böhme et al.** (ICSE'22 §5) — attribution to a specific target
  bug requires differential pre/post-fix confirmation.

Operationally, the driver records three orthogonal booleans per cell:

1. `result.json.detected == true` — `signal_T(I, V_pre) = true` for
   at least one artifact in the pre-fix run (libFuzzer-family: files
   under `crashes/`; BioTest: new entries under `bug_reports/`;
   Pure Random: Chat 6 post-hoc `ParserRunner` replay).
2. `result.json.trigger_input != null` — the driver picked a
   canonical representative `I` (first file in the relevant artifact
   dir).
3. `result.json.confirmed_fix_silences_signal == true` —
   `signal_T(I, V_post) = false`. The driver installs `V_post` and
   replays `I` through the language-specific `ParserRunner`.

A cell is scored as `tool T found bug B` iff **all three** booleans
are true.

`confirmed_fix_silences_signal == null` → replay was impossible
(missing trigger file, post-fix install failed, no runner for this
SUT, harness-version-skew on Rust). Listed under `null_silences` in
the Chat 6 post-run review for manual triage. Prior Magma / FuzzBench
runs report 5-15 % of raw-crash cells falling into this residual
category.

`confirmed_fix_silences_signal == false` → post-fix SUT *still*
crashes on the trigger. Either the fix didn't land where we expect,
or the crash is attributable to a different bug. Not counted as a
detection for the target bug.

### Per-tool detection implementations

| tool            | how `crash_count` is populated |
| :-------------- | :----------------------------- |
| biotest         | count of NEW entries in `bug_reports/` during the run (snapshot-diff, post-2026-04-20 fix) |
| jazzer          | libFuzzer artifacts in `crashes/`: `crash-*`, `timeout-*`, `slow-unit-*` |
| atheris         | libFuzzer artifacts (atheris wraps libFuzzer) |
| libfuzzer       | libFuzzer artifacts |
| cargo_fuzz      | libFuzzer artifacts (cargo-fuzz wraps libFuzzer) |
| aflpp           | `crashes/*` inside AFL++'s sync dir |
| pure_random     | always 0 intrinsically — **Chat 6** replays its corpus through `ParserRunner` post-hoc |
| evosuite_anchor | `failing-tests/` dir contents (EvoSuite's GA selects test inputs that still fail post-fix) |

### Expected signals (bug manifest field `expected_signal.type`)

- `differential_disagreement` — oracle voter disagreement. BioTest's
  native signal. Crash-finders pick it up only if the disagreement
  *also* raises an exception (often true for parser bugs, not always).
- `uncaught_exception` — SUT throws a parse-time exception that
  propagates past its try/catch barrier. Direct hit for crash-finders.
- `timeout_or_differential_disagreement` — either is acceptable.
- `intermittent_differential_disagreement` — flaky; single negative
  doesn't invalidate.

### Canonical result layout

After all six chats complete, `compares/results/bug_bench/` contains:

```
compares/results/bug_bench/
├── aggregate.json              # unified rollup (Chat 6 writes)
├── run_manifest.json           # Chat 6: git SHA + image ID + timestamps
├── post_run_review.json        # Chat 6: per-cell counts + spot-checks
├── post_run_review.md          # human-readable version
├── biotest/<bug_id>/           # per cell
│   ├── result.json             # BugResult schema
│   ├── corpus/                 # seeds + tool-generated inputs
│   ├── crashes/                # crashing inputs
│   └── tool.log                # tool stderr/stdout
├── jazzer/<bug_id>/...
├── atheris/<bug_id>/...
├── libfuzzer/<bug_id>/...
├── cargo_fuzz/<bug_id>/...
├── pure_random/<bug_id>/...
└── evosuite_anchor/<bug_id>/...
```

Each chat writes its slice into a `/tmp/bug_bench_chat<N>/` dir inside
the container, then rsyncs into the canonical `/work/compares/results/
bug_bench/` at the end. The rsync is additive — chats never overwrite
each other's cells because cell paths are keyed by `<tool>/<bug_id>/`.

---

## Chat 1 — htsjdk VCF × 4 tools (36 cells)

### Scope
- SUT: **htsjdk**
- Format: **VCF**
- Bugs: 9 htsjdk-* VCF bugs listed below
- Tools: `biotest`, `jazzer`, `pure_random`, `evosuite_anchor`
- Cells: 9 × 4 = **36**
- Walltime: B=60s ≈ 45 min, B=300s ≈ 3.5 h, B=7200s ≈ 72 h
- Depends on: none
- Produces: per-cell artifacts under `/tmp/bug_bench_chat1/`, rsynced to
  `/work/compares/results/bug_bench/` at the end.

### Preflight (run first)

```bash
docker ps --format '{{.Names}}' | grep -q biotest-bench-setup \
  || { echo 'biotest-bench-setup container must be up'; exit 1; }

docker exec biotest-bench-setup bash -c '
  set -e
  test -x /work/compares/results/sut-envs/vcfpy/bin/python || { \
    echo "missing vcfpy venv"; exit 1; }
  test -f /work/compares/bug_bench/manifest.verified.json
  test -d /work/compares/results/bench_seeds/vcf
  test -x /root/.cargo/bin/cargo
  test -x /opt/atheris-venv/bin/python
  test -f /work/compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar
'
```

### Bugs in this chat

| bug_id      | format | pre_fix   | post_fix  | anchor_type       | expected_signal            |
| :---------- | :----: | :-------- | :-------- | :---------------- | :------------------------- |
| htsjdk-1554 |  VCF   | 2.24.1    | 3.0.0     | install_version   | differential_disagreement  |
| htsjdk-1637 |  VCF   | 3.0.3     | 3.0.4     | install_version   | differential_disagreement  |
| htsjdk-1364 |  VCF   | 2.19.0    | 2.20.0    | install_version   | differential_disagreement  |
| htsjdk-1389 |  VCF   | 2.19.0    | 2.20.0    | install_version   | differential_disagreement  |
| htsjdk-1372 |  VCF   | 2.19.0    | 2.20.0    | install_version   | differential_disagreement  |
| htsjdk-1401 |  VCF   | 2.19.0    | 2.20.0    | install_version   | differential_disagreement  |
| htsjdk-1403 |  VCF   | 2.20.0    | 2.20.1    | install_version   | differential_disagreement  |
| htsjdk-1418 |  VCF   | 2.20.1    | 2.21.0    | install_version   | **uncaught_exception**     |
| htsjdk-1544 |  VCF   | 2.24.1    | 3.0.0     | install_version   | differential_disagreement  |

### Detection rules in this chat

- **biotest**: bug_reports snapshot-diff → `crash_count` = count of
  NEW `bug_reports/BUG-*` directories. `trigger_input` = canonical
  `original.{vcf,sam}` under each new bug report. Post-fix replay uses
  `test_engine.runners.htsjdk_runner.HTSJDKRunner`.
- **jazzer**: libFuzzer artifacts in `crashes/` (`crash-*`,
  `timeout-*`). Each file = 1 crash. Post-fix replay same as above.
- **pure_random**: no intrinsic detection; `crash_count` always 0.
  Post-hoc detection via Chat 6 — replays `corpus/rand_*.vcf` through
  `HTSJDKRunner`, scores as detected if any input raises `ParseError`
  on pre-fix AND is accepted on post-fix.
- **evosuite_anchor**: `failing-tests/` dir contents post-GA. Detection
  = "post-fix htsjdk passes the EvoSuite-generated JUnit cases that
  pre-fix failed". Written by `run_evosuite.sh` into each cell's
  `detection_metadata.json`.

### Commands

```bash
# Executes in background; writes progress to the per-chat log.
docker exec -d biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  rm -rf /tmp/bug_bench_chat1
  mkdir -p /tmp/bug_bench_chat1

  BUDGET_S=${BUDGET_S:-300}
  export BUDGET_S
  echo "[chat1] budget=${BUDGET_S}s start=$(date -u +%FT%TZ)" \
       >> /tmp/phase4-chat1.log

  for TOOL in biotest jazzer pure_random evosuite_anchor; do
    echo "[chat1] tool=${TOOL} $(date -u +%FT%TZ)" >> /tmp/phase4-chat1.log
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut htsjdk --only-tool ${TOOL} \
      --time-budget-s ${BUDGET_S} \
      --out /tmp/bug_bench_chat1 \
      >> /tmp/phase4-chat1.log 2>&1
  done

  # Keep only VCF-format bugs: manifest orders htsjdk bugs into 9 VCF
  # + 3 SAM; --only-sut htsjdk picks up all 12. Prune the SAM cells so
  # Chat 2 owns them cleanly.
  for TOOL in biotest jazzer pure_random evosuite_anchor; do
    for SAM_BUG in htsjdk-1561 htsjdk-1538 htsjdk-1489; do
      rm -rf /tmp/bug_bench_chat1/${TOOL}/${SAM_BUG}
    done
  done

  echo "[chat1] end=$(date -u +%FT%TZ)" >> /tmp/phase4-chat1.log
  # Per-chat aggregate snapshot
  python3.12 compares/scripts/rollup_bug_bench.py \
    --bench-root /tmp/bug_bench_chat1 \
    --out /tmp/bug_bench_chat1/aggregate.json
  # Chat-local run manifest
  python3.12 - <<PY > /tmp/bug_bench_chat1/run_manifest.json
import json, subprocess, os, time
print(json.dumps({
    "chat": 1,
    "scope": "htsjdk VCF × {biotest, jazzer, pure_random, evosuite_anchor}",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "git_sha": subprocess.check_output(
        ["git","-C","/work","rev-parse","HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME",""),
}, indent=2))
PY
'
```

Monitor:
```bash
docker exec biotest-bench-setup bash -c \
  "grep -E '^\[(chat1|orchestrator|group|run|done|skip)\]' /tmp/phase4-chat1.log | tail -20"
```

### Handoff to Chat 6

When `/tmp/bug_bench_chat1/aggregate.json` exists and
`run_manifest.json` exists alongside it, this chat is done. Chat 6
rsyncs `/tmp/bug_bench_chat1/` into `/work/compares/results/bug_bench/`.

### Paste-ready prompt for Chat 1

Paste the following into a fresh Claude Code session running in
`C:\Users\miaot\Github\BioTest`:

> **Task**: Execute Chat 1 of the Phase 4 real-bug benchmark per
> `compares/PHASE4_EXECUTION_PLAN.md` §"Chat 1 — htsjdk VCF × 4 tools".
>
> Scope: 36 cells (9 htsjdk VCF bugs × {biotest, jazzer, pure_random,
> evosuite_anchor}).
>
> Before running: verify the `biotest-bench-setup` Docker container is
> up, the vcfpy sut-env + /root/.cargo/bin/cargo + /opt/atheris-venv +
> htsjdk-with-deps.jar all exist inside the container. If any are
> missing, invoke
> `bash compares/scripts/prepare_sut_install_envs.sh` inside the
> container first.
>
> Run the bench in background via `docker exec -d` using the command
> block under "Commands" in the plan. Default `BUDGET_S=300`; operator
> may override. Monitor `/tmp/phase4-chat1.log` until all four tool
> loops have exited.
>
> Success criteria:
> - `/tmp/bug_bench_chat1/aggregate.json` exists with 36 records.
> - `/tmp/bug_bench_chat1/run_manifest.json` exists with the chat's
>   git SHA and the per-chat budget.
> - No tool loop's log shows unexpected `adapter_raise` exit codes.
>
> On success, report a one-line summary: `"Chat 1 done — 36 cells, <N>
> detected, log at /tmp/phase4-chat1.log"`. Do NOT merge into
> `compares/results/bug_bench/` — that's Chat 6's job.
>
> Do not mark DESIGN.md `§13.5 Phase 4` boxes yet — also Chat 6's job.

---

## Chat 2 — htsjdk SAM × 4 tools (12 cells)

### Scope
- SUT: **htsjdk**
- Format: **SAM**
- Bugs: 3 htsjdk-* SAM bugs below
- Tools: `biotest`, `jazzer`, `pure_random`, `evosuite_anchor`
- Cells: 3 × 4 = **12**
- Walltime: B=60s ≈ 15 min, B=300s ≈ 1.2 h, B=7200s ≈ 24 h
- Depends on: none
- Produces: per-cell artifacts under `/tmp/bug_bench_chat2/`.

### Preflight (identical to Chat 1)
```bash
docker exec biotest-bench-setup bash -c '
  set -e
  test -f /work/compares/bug_bench/manifest.verified.json
  test -d /work/compares/results/bench_seeds/sam
  test -f /work/compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar
'
```

### Bugs in this chat

| bug_id      | format | pre_fix | post_fix | anchor_type     | expected_signal           |
| :---------- | :----: | :------ | :------- | :-------------- | :------------------------ |
| htsjdk-1561 |  SAM   | 2.24.1  | 3.0.0    | install_version | differential_disagreement |
| htsjdk-1538 |  SAM   | 2.24.0  | 2.24.1   | install_version | differential_disagreement |
| htsjdk-1489 |  SAM   | 2.22.0  | 2.23.0   | install_version | differential_disagreement |

### Detection rules in this chat

Same as Chat 1 for each tool, with `HTSJDKRunner` for post-fix replay.

### Commands

```bash
docker exec -d biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  rm -rf /tmp/bug_bench_chat2
  mkdir -p /tmp/bug_bench_chat2

  BUDGET_S=${BUDGET_S:-300}
  export BUDGET_S
  echo "[chat2] budget=${BUDGET_S}s start=$(date -u +%FT%TZ)" \
       >> /tmp/phase4-chat2.log

  # Run --only-sut htsjdk then filter to SAM bugs after.
  for TOOL in biotest jazzer pure_random evosuite_anchor; do
    for BUG in htsjdk-1561 htsjdk-1538 htsjdk-1489; do
      echo "[chat2] tool=${TOOL} bug=${BUG} $(date -u +%FT%TZ)" \
           >> /tmp/phase4-chat2.log
      python3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.verified.json \
        --only-bug ${BUG} --only-tool ${TOOL} \
        --time-budget-s ${BUDGET_S} \
        --out /tmp/bug_bench_chat2 \
        >> /tmp/phase4-chat2.log 2>&1
    done
  done

  echo "[chat2] end=$(date -u +%FT%TZ)" >> /tmp/phase4-chat2.log
  python3.12 compares/scripts/rollup_bug_bench.py \
    --bench-root /tmp/bug_bench_chat2 \
    --out /tmp/bug_bench_chat2/aggregate.json
  python3.12 - <<PY > /tmp/bug_bench_chat2/run_manifest.json
import json, subprocess, os, time
print(json.dumps({
    "chat": 2,
    "scope": "htsjdk SAM × {biotest, jazzer, pure_random, evosuite_anchor}",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "git_sha": subprocess.check_output(
        ["git","-C","/work","rev-parse","HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME",""),
}, indent=2))
PY
'
```

### Paste-ready prompt for Chat 2

> **Task**: Execute Chat 2 of Phase 4 per
> `compares/PHASE4_EXECUTION_PLAN.md §"Chat 2 — htsjdk SAM × 4 tools"`.
>
> Scope: 12 cells (3 htsjdk SAM bugs × 4 tools). Uses `--only-bug` to
> hit the three SAM bugs specifically (the manifest's `--only-sut
> htsjdk` filter would also pick up the 9 VCF bugs handled by Chat 1).
>
> Run the bench in background per the plan's "Commands" block. Default
> `BUDGET_S=300`. Monitor `/tmp/phase4-chat2.log`.
>
> Success criteria:
> - `/tmp/bug_bench_chat2/aggregate.json` exists with 12 records.
> - `/tmp/bug_bench_chat2/run_manifest.json` present.
>
> On success, one-line summary: `"Chat 2 done — 12 cells, <N>
> detected, log at /tmp/phase4-chat2.log"`. Do not merge or mark
> DESIGN.md — Chat 6's job.

---

## Chat 3 — vcfpy VCF × 3 tools (21 cells)

### Scope
- SUT: **vcfpy**
- Format: **VCF**
- Bugs: 7 vcfpy-* bugs below
- Tools: `biotest`, `atheris`, `pure_random`
- Cells: 7 × 3 = **21**
- Walltime: B=60s ≈ 25 min, B=300s ≈ 2.0 h, B=7200s ≈ 42 h
- Depends on: none
- Produces: `/tmp/bug_bench_chat3/`.

### Preflight

```bash
docker exec biotest-bench-setup bash -c '
  set -e
  test -x /work/compares/results/sut-envs/vcfpy/bin/python || { \
    bash /work/compares/scripts/prepare_sut_install_envs.sh; }
  test -x /opt/atheris-venv/bin/python
  /opt/atheris-venv/bin/python -c "import atheris, vcfpy" || { \
    /opt/atheris-venv/bin/pip install vcfpy==0.14.0; }
  test -f /work/compares/harnesses/atheris/fuzz_vcfpy.py
'
```

### Bugs in this chat

| bug_id            | format | pre_fix | post_fix | anchor_type     | expected_signal            |
| :---------------- | :----: | :------ | :------- | :-------------- | :------------------------- |
| vcfpy-176         |  VCF   | 0.13.8  | 0.14.0   | install_version | **uncaught_exception**     |
| vcfpy-171         |  VCF   | 0.13.8  | 0.14.0   | install_version | differential_disagreement  |
| vcfpy-146         |  VCF   | 0.13.3  | 0.13.4   | install_version | **uncaught_exception**     |
| vcfpy-145         |  VCF   | 0.13.4  | 0.13.5   | install_version | **uncaught_exception**     |
| vcfpy-gtone-0.13  |  VCF   | 0.12.1  | 0.12.2   | install_version | differential_disagreement  |
| vcfpy-127         |  VCF   | 0.11.0  | 0.11.1   | install_version | **uncaught_exception**     |
| vcfpy-nocall-0.8  |  VCF   | 0.8.1   | 0.9.0    | install_version | differential_disagreement  |

### Detection rules in this chat

- **biotest**: `bug_reports/` snapshot-diff.
- **atheris**: libFuzzer artifacts under `crashes/`. The fuzzer drives
  `fuzz_vcfpy.py` which calls `vcfpy.Reader.from_path`; any
  `vcfpy.exceptions.VCFPyException` / `OSError` → libFuzzer artifact.
- **pure_random**: intrinsic `crash_count = 0`. Chat 6 post-hoc replays
  `corpus/rand_*.vcf` through the vcfpy runner (once the runner exists
  — see "Chat 3 pre-work" below).

### Chat 3 pre-work (must land BEFORE the bench runs)

`bug_bench_driver.py::_replay_trigger_silenced` has no vcfpy branch —
as a result, every `confirmed_fix_silences_signal` for a vcfpy cell
returns `False`. Add a vcfpy branch before running:

```python
# In _replay_trigger_silenced, add after the biopython branch:
elif sut == "vcfpy":
    # vcfpy has no ParserRunner in test_engine.runners; invoke directly.
    import vcfpy  # type: ignore
    try:
        with vcfpy.Reader.from_path(str(trig_path)) as reader:
            for _ in reader:
                pass
        return True  # post-fix parsed the trigger cleanly
    except Exception:
        return False
```

This branch must be added inside the `biotest-bench-setup` container's
copy of the driver, **and** committed to the host repo so future runs
inherit it.

### Commands

```bash
docker exec -d biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  rm -rf /tmp/bug_bench_chat3
  mkdir -p /tmp/bug_bench_chat3

  BUDGET_S=${BUDGET_S:-300}
  export BUDGET_S
  echo "[chat3] budget=${BUDGET_S}s start=$(date -u +%FT%TZ)" \
       >> /tmp/phase4-chat3.log

  for TOOL in biotest atheris pure_random; do
    echo "[chat3] tool=${TOOL} $(date -u +%FT%TZ)" >> /tmp/phase4-chat3.log
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut vcfpy --only-tool ${TOOL} \
      --time-budget-s ${BUDGET_S} \
      --out /tmp/bug_bench_chat3 \
      >> /tmp/phase4-chat3.log 2>&1
  done

  echo "[chat3] end=$(date -u +%FT%TZ)" >> /tmp/phase4-chat3.log
  python3.12 compares/scripts/rollup_bug_bench.py \
    --bench-root /tmp/bug_bench_chat3 \
    --out /tmp/bug_bench_chat3/aggregate.json
  python3.12 - <<PY > /tmp/bug_bench_chat3/run_manifest.json
import json, subprocess, os, time
print(json.dumps({
    "chat": 3,
    "scope": "vcfpy VCF × {biotest, atheris, pure_random}",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "git_sha": subprocess.check_output(
        ["git","-C","/work","rev-parse","HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME",""),
}, indent=2))
PY
'
```

### Paste-ready prompt for Chat 3

> **Task**: Execute Chat 3 of Phase 4 per
> `compares/PHASE4_EXECUTION_PLAN.md §"Chat 3 — vcfpy VCF × 3 tools"`.
>
> Scope: 21 cells (7 vcfpy VCF bugs × {biotest, atheris, pure_random}).
>
> Pre-work **required before running**: the driver has no vcfpy
> branch in `_replay_trigger_silenced` — add it per the plan's "Chat 3
> pre-work" section. This is a short Edit to
> `compares/scripts/bug_bench_driver.py` and must be committed before
> the bench kicks off.
>
> Preflight: verify `/opt/atheris-venv` has both `atheris` and
> `vcfpy==0.14.0`; if not, pip-install vcfpy into the atheris venv
> and `docker commit` to persist.
>
> Run the bench in background per the plan's "Commands" block.
> Default `BUDGET_S=300`. Monitor `/tmp/phase4-chat3.log`.
>
> Success: 21 records in `/tmp/bug_bench_chat3/aggregate.json`,
> `run_manifest.json` present, 4 `uncaught_exception` bugs detected by
> atheris (expected floor behaviour).
>
> Do not merge or mark DESIGN.md.

---

## Chat 4 — noodles VCF × 3 tools (27 cells)

### Scope
- SUT: **noodles-vcf**
- Format: **VCF**
- Bugs: 9 noodles-* bugs below
- Tools: `biotest`, `cargo_fuzz`, `pure_random`
- Cells: 9 × 3 = **27**
- Walltime: B=60s ≈ 40 min, B=300s ≈ 2.5 h, B=7200s ≈ 54 h
- Depends on: none
- Produces: `/tmp/bug_bench_chat4/`.

### Preflight

```bash
docker exec biotest-bench-setup bash -c '
  set -e
  export PATH=/root/.cargo/bin:$PATH
  test -x /root/.cargo/bin/cargo
  test -x /root/.cargo/bin/cargo-fuzz
  test -f /work/harnesses/rust/noodles_harness/Cargo.toml
  test -f /work/compares/harnesses/cargo_fuzz/fuzz/Cargo.toml
  test -f /work/compares/harnesses/cargo_fuzz/fuzz/fuzz_targets/noodles_vcf_target.rs

  # Build the cargo-fuzz target once so the adapter can find the binary.
  cd /work/compares/harnesses/cargo_fuzz
  cargo fuzz build noodles_vcf_target --release --sanitizer none \
    --manifest-path fuzz/Cargo.toml
'
```

### Bugs in this chat

| bug_id                | format | pre_fix | post_fix | anchor_type   | expected_signal           | harness-skew risk |
| :-------------------- | :----: | :------ | :------- | :------------ | :------------------------ | :---------------- |
| noodles-300           |  VCF   | 0.63    | 0.64     | cargo_version | differential_disagreement | low               |
| noodles-339           |  VCF   | 0.81    | 0.82     | cargo_version | differential_disagreement | low               |
| noodles-268           |  VCF   | 0.57    | 0.58     | cargo_version | differential_disagreement | **medium**        |
| noodles-223           |  VCF   | 0.48    | 0.49     | cargo_version | differential_disagreement | **high**          |
| noodles-224           |  VCF   | 0.48    | 0.49     | cargo_version | differential_disagreement | **high**          |
| noodles-259           |  VCF   | 0.55    | 0.56     | cargo_version | differential_disagreement | **medium**        |
| noodles-241           |  VCF   | 0.58    | 0.59     | cargo_version | **uncaught_exception**    | **medium**        |
| noodles-inforay-0.64  |  VCF   | 0.63    | 0.64     | cargo_version | differential_disagreement | low               |
| noodles-ob1-0.23      |  VCF   | 0.23    | 0.24     | cargo_version | differential_disagreement | **high**          |

**harness-skew risk**: the canonical-JSON harness `main.rs` and the
cargo-fuzz target `noodles_vcf_target.rs` were written against
noodles-vcf 0.70 API. Older versions may have incompatible trait
bounds or method signatures. A failed cargo build during install-swap
is a tooling-level skip — record and move on.

### Detection rules in this chat

- **biotest**: `bug_reports/` snapshot-diff.
- **cargo_fuzz**: libFuzzer artifacts in `crashes/`. The fuzzer binary
  is `compares/harnesses/cargo_fuzz/fuzz/target/x86_64-unknown-linux-gnu/release/noodles_vcf_target`.
- **pure_random**: intrinsic 0; Chat 6 replays `corpus/rand_*.vcf`
  through the noodles post-fix harness (see "Chat 4 pre-work").

### Chat 4 pre-work (must land BEFORE the bench runs)

Similar to Chat 3: `_replay_trigger_silenced` has no noodles branch.
Add one that invokes the canonical-JSON harness binary:

```python
# In _replay_trigger_silenced, add after the seqan3 branch:
elif sut == "noodles":
    import subprocess
    binary = REPO_ROOT / "harnesses" / "rust" / "noodles_harness" \
             / "target" / "release" / "noodles_harness"
    if not binary.exists():
        return None
    proc = subprocess.run(
        [str(binary), str(trig_path)],
        capture_output=True, timeout=30,
    )
    return proc.returncode == 0
```

### Commands

```bash
docker exec -d biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  rm -rf /tmp/bug_bench_chat4
  mkdir -p /tmp/bug_bench_chat4

  BUDGET_S=${BUDGET_S:-300}
  export BUDGET_S
  echo "[chat4] budget=${BUDGET_S}s start=$(date -u +%FT%TZ)" \
       >> /tmp/phase4-chat4.log

  for TOOL in biotest cargo_fuzz pure_random; do
    echo "[chat4] tool=${TOOL} $(date -u +%FT%TZ)" >> /tmp/phase4-chat4.log
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut noodles --only-tool ${TOOL} \
      --time-budget-s ${BUDGET_S} \
      --out /tmp/bug_bench_chat4 \
      >> /tmp/phase4-chat4.log 2>&1
  done

  echo "[chat4] end=$(date -u +%FT%TZ)" >> /tmp/phase4-chat4.log
  python3.12 compares/scripts/rollup_bug_bench.py \
    --bench-root /tmp/bug_bench_chat4 \
    --out /tmp/bug_bench_chat4/aggregate.json
  python3.12 - <<PY > /tmp/bug_bench_chat4/run_manifest.json
import json, subprocess, os, time
print(json.dumps({
    "chat": 4,
    "scope": "noodles VCF × {biotest, cargo_fuzz, pure_random}",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "git_sha": subprocess.check_output(
        ["git","-C","/work","rev-parse","HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME",""),
}, indent=2))
PY
'
```

### Paste-ready prompt for Chat 4

> **Task**: Execute Chat 4 of Phase 4 per
> `compares/PHASE4_EXECUTION_PLAN.md §"Chat 4 — noodles VCF × 3 tools"`.
>
> Scope: 27 cells (9 noodles VCF bugs × {biotest, cargo_fuzz,
> pure_random}).
>
> Pre-work **required before running**: (a) add a noodles branch to
> `_replay_trigger_silenced` per the plan; (b) confirm
> `cargo fuzz build noodles_vcf_target --release --sanitizer none`
> succeeds (the preflight block does this automatically).
>
> **Expected tooling skips**: noodles-223, -224, -ob1-0.23, and
> possibly -259/-268/-241 may fail the cargo build step on their
> pre-fix anchor because the main.rs / fuzz target uses 0.70 API not
> compatible with 0.23/0.48/0.55/0.57/0.58. The driver records these
> as install failures and moves on — do not attempt to patch main.rs
> per-version unless explicitly instructed.
>
> Run the bench in background per the plan's "Commands" block. Default
> `BUDGET_S=300`. Monitor `/tmp/phase4-chat4.log`.
>
> Success: 27 records in `/tmp/bug_bench_chat4/aggregate.json`
> (counting skipped cells). `run_manifest.json` present.
>
> Do not merge or mark DESIGN.md.

---

## Chat 5 — biopython + seqan3 SAM × 3 tools (21 cells)

### Scope
- SUTs: **biopython** (SAM) + **seqan3** (SAM)
- Format: **SAM**
- Bugs: 1 biopython-* + 6 seqan3-* below
- Tools: `biotest`, `atheris` (biopython) / `libfuzzer` (seqan3), `pure_random`
- Cells: (1 × 3) + (6 × 3) = **21**
- Walltime: B=60s ≈ 25 min, B=300s ≈ 2.0 h, B=7200s ≈ 42 h
- Depends on: none
- Produces: `/tmp/bug_bench_chat5/`.

### Preflight

```bash
docker exec biotest-bench-setup bash -c '
  set -e
  test -x /work/compares/results/sut-envs/biopython/bin/python
  test -x /opt/atheris-venv/bin/python
  /opt/atheris-venv/bin/python -c "import atheris, Bio"
  test -f /work/compares/harnesses/atheris/fuzz_biopython.py

  # seqan3 libFuzzer harness — built once, reused across anchors.
  test -f /work/compares/harnesses/libfuzzer/CMakeLists.txt
  test -x /work/compares/harnesses/libfuzzer/build/seqan3_sam_fuzzer \
    || bash /work/compares/scripts/build_harnesses.sh --only-seqan3

  # seqan3 shallow clone must contain all 12 commit SHAs below.
  SEQAN3_SRC=/work/compares/baselines/seqan3/source
  test -d ${SEQAN3_SRC}/.git
  for SHA in df9fd5ff64f59fdb124c4a564a4141d1f9cff22b \
             8e374d7ce7a1ce4de0077bc3698d5ae2c8e79600 \
             fa221c1302cfe515211ea70de375a1802826d3d9 \
             c84f5671665478ec1b71535201cbffbe1fdd8c82 \
             ca4d668390e35b4045ccd02d070927f8178ed2ce \
             11564cb3bcea39666d6d3979080bc5d8fdbe1d7e \
             4961904fbc3b254f7a611b5b467c2e33ae5b1042 \
             4fe548913e96d3f908dd524bd3dc13b48f87bfa4 \
             745c645fe26272791464cd67180775d28c00bf28 \
             5e5c05a471269703d7afc38bdc4348cef60be63b; do
    git -C ${SEQAN3_SRC} cat-file -e ${SHA}^{commit} 2>/dev/null \
      || { git -C ${SEQAN3_SRC} fetch --unshallow origin || \
           git -C ${SEQAN3_SRC} fetch origin +refs/heads/*:refs/remotes/origin/*; \
           break; }
  done
'
```

### Bugs in this chat

| bug_id        | sut       | format | pre_fix                                   | post_fix                                 | anchor_type     | expected_signal                           |
| :------------ | :-------- | :----: | :---------------------------------------- | :--------------------------------------- | :-------------- | :---------------------------------------- |
| biopython-4825| biopython |  SAM   | 1.85                                      | 1.86                                     | install_version | timeout_or_differential_disagreement      |
| seqan3-2418   | seqan3    |  SAM   | `df9fd5ff64f59fdb124c4a564a4141d1f9cff22b`| `8e374d7ce7a1ce4de0077bc3698d5ae2c8e79600`| commit_sha      | differential_disagreement                 |
| seqan3-3081   | seqan3    |  SAM   | `fa221c1302cfe515211ea70de375a1802826d3d9`| `c84f5671665478ec1b71535201cbffbe1fdd8c82`| commit_sha      | differential_disagreement                 |
| seqan3-3269   | seqan3    |  SAM   | `ca4d668390e35b4045ccd02d070927f8178ed2ce`| `11564cb3bcea39666d6d3979080bc5d8fdbe1d7e`| commit_sha      | differential_disagreement                 |
| seqan3-3098   | seqan3    |  SAM   | `4961904fbc3b254f7a611b5b467c2e33ae5b1042`| `4fe548913e96d3f908dd524bd3dc13b48f87bfa4`| commit_sha      | differential_disagreement                 |
| seqan3-2869   | seqan3    |  SAM   | `edbfa956f^` (parent)                     | `edbfa956f`                              | commit_sha      | differential_disagreement                 |
| seqan3-3406   | seqan3    |  SAM   | `745c645fe26272791464cd67180775d28c00bf28`| `5e5c05a471269703d7afc38bdc4348cef60be63b`| commit_sha      | intermittent_differential_disagreement    |

### Detection rules in this chat

- **biotest**: `bug_reports/` snapshot-diff.
- **atheris (biopython)**: libFuzzer artifacts; post-fix replay via
  `test_engine.runners.biopython_runner.BiopythonRunner`.
- **libfuzzer (seqan3)**: libFuzzer artifacts from
  `compares/harnesses/libfuzzer/build/seqan3_sam_fuzzer`; post-fix
  replay via `test_engine.runners.seqan3_runner.SeqAn3Runner` (which
  shells out to the rebuilt harness binary).
- **pure_random**: intrinsic 0; Chat 6 post-hoc replay.

### Commands

```bash
docker exec -d biotest-bench-setup bash -c '
  export PATH=/root/.cargo/bin:$PATH
  cd /work
  rm -rf /tmp/bug_bench_chat5
  mkdir -p /tmp/bug_bench_chat5

  BUDGET_S=${BUDGET_S:-300}
  export BUDGET_S
  echo "[chat5] budget=${BUDGET_S}s start=$(date -u +%FT%TZ)" \
       >> /tmp/phase4-chat5.log

  # biopython × 3 tools
  for TOOL in biotest atheris pure_random; do
    echo "[chat5] biopython tool=${TOOL} $(date -u +%FT%TZ)" \
         >> /tmp/phase4-chat5.log
    python3.12 compares/scripts/bug_bench_driver.py \
      --manifest compares/bug_bench/manifest.verified.json \
      --only-sut biopython --only-tool ${TOOL} \
      --time-budget-s ${BUDGET_S} \
      --out /tmp/bug_bench_chat5 \
      >> /tmp/phase4-chat5.log 2>&1
  done

  # seqan3 × 3 tools
  for TOOL in biotest libfuzzer pure_random; do
    echo "[chat5] seqan3 tool=${TOOL} $(date -u +%FT%TZ)" \
         >> /tmp/phase4-chat5.log
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
  python3.12 - <<PY > /tmp/bug_bench_chat5/run_manifest.json
import json, subprocess, os, time
print(json.dumps({
    "chat": 5,
    "scope": "biopython+seqan3 SAM × 3 tools",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "git_sha": subprocess.check_output(
        ["git","-C","/work","rev-parse","HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME",""),
}, indent=2))
PY
'
```

### Paste-ready prompt for Chat 5

> **Task**: Execute Chat 5 of Phase 4 per
> `compares/PHASE4_EXECUTION_PLAN.md §"Chat 5 — biopython + seqan3
> SAM × 3 tools"`.
>
> Scope: 21 cells (1 biopython bug + 6 seqan3 bugs × 3 tools).
>
> Preflight: verify the seqan3 shallow clone contains all 10 commit
> SHAs listed in the bug table; if any is missing, deepen via
> `git fetch --unshallow`. Verify the libFuzzer seqan3 harness binary
> exists; rebuild via `bash compares/scripts/build_harnesses.sh
> --only-seqan3` if missing.
>
> Run the bench in background per the plan's "Commands" block. Default
> `BUDGET_S=300`. Monitor `/tmp/phase4-chat5.log`.
>
> **Expected tooling quirks**: seqan3 needs a `libseqan3` rebuild per
> commit; the driver's `_checkout_seqan3` handles the git checkout but
> the seqan3 harness rebuild happens only if the operator has pre-built
> binaries per commit. If seqan3 cells show install failures, consult
> `compares/baselines/seqan3/build.sh` and rebuild the harness per
> pre-fix commit.
>
> Success: 21 records in `/tmp/bug_bench_chat5/aggregate.json`.
> `run_manifest.json` present.
>
> Do not merge or mark DESIGN.md.

---

## Chat 6 — Post-processing, rollup, review, backup, DESIGN.md update

### Scope
- No fuzzing; pure consolidation + review + commit.
- Depends on: Chats 1-5 have all written their `/tmp/bug_bench_chatN/`
  dirs and `run_manifest.json` files.
- Walltime: ~15 min regardless of production budget.
- Produces: canonical `compares/results/bug_bench/` tree, the
  DESIGN.md §13.5 Phase 4 checkmarks, and the off-machine backup
  archive.

### Pre-requisites — fail fast if missing

```bash
docker exec biotest-bench-setup bash -c '
  for N in 1 2 3 4 5; do
    test -f /tmp/bug_bench_chat${N}/aggregate.json \
      || { echo "chat${N} aggregate.json missing — abort"; exit 1; }
    test -f /tmp/bug_bench_chat${N}/run_manifest.json \
      || { echo "chat${N} run_manifest.json missing — abort"; exit 1; }
  done
'
```

### Script that does not yet exist — must be created

`compares/scripts/rollup_bug_bench.py` — Chat 6's first implementation
task. Walks `<bench_root>/<tool>/<bug_id>/result.json`, concatenates
the records into `<bench_root>/aggregate.json`. Minimal:

```python
#!/usr/bin/env python3
"""Walk a bug-bench results tree and emit a unified aggregate.json.

Used both by per-chat partial rollups (under /tmp/bug_bench_chatN/)
and by Chat 6's canonical rollup (under compares/results/bug_bench/).
"""
import argparse, json
from pathlib import Path

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    records = []
    for result in args.bench_root.rglob("result.json"):
        if result.parent.parent.name == args.bench_root.name:
            continue  # the top-level aggregate itself
        try:
            records.append(json.loads(result.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"[rollup] skip {result}: {e}")
    args.out.write_text(
        json.dumps({"results": records}, indent=2), encoding="utf-8",
    )
    print(f"[rollup] {len(records)} records -> {args.out}")

if __name__ == "__main__":
    main()
```

### Commands

```bash
# 1. Merge chat dirs into canonical location.
docker exec biotest-bench-setup bash -c '
  set -e
  DST=/work/compares/results/bug_bench
  mkdir -p ${DST}
  for N in 1 2 3 4 5; do
    rsync -a /tmp/bug_bench_chat${N}/ ${DST}/
  done

  # 2. Rebuild unified aggregate.json from the merged tree.
  cd /work
  python3.12 compares/scripts/rollup_bug_bench.py \
    --bench-root compares/results/bug_bench \
    --out compares/results/bug_bench/aggregate.json

  # 3. Top-level run manifest — merge all five chat manifests.
  python3.12 - <<PY > compares/results/bug_bench/run_manifest.json
import json
from pathlib import Path
chats = []
for n in range(1, 6):
    src = Path(f"/tmp/bug_bench_chat{n}/run_manifest.json")
    if src.exists():
        chats.append(json.loads(src.read_text()))
out = {"phase": 4, "chats": chats}
print(json.dumps(out, indent=2))
PY

  # 4. Post-run review — detection counts + spot-check replays.
  python3.12 compares/scripts/post_run_review.py \
    --bench-root compares/results/bug_bench --spot-check 3
'

# 5. Backup the canonical tree off-machine.
bash compares/scripts/backup_bug_bench.sh

# 6. Mark DESIGN.md §13.5 Phase 4 boxes [x] with per-chat budget +
#    timestamp + aggregate numbers. This is a hand Edit — see the
#    template block further down.

# 7. Commit.
git add compares/results/bug_bench/aggregate.json \
        compares/results/bug_bench/run_manifest.json \
        compares/results/bug_bench/post_run_review.{json,md} \
        compares/DESIGN.md
git commit -m "phase4: land 117-cell real-bug bench (budget=${BUDGET_S}s)"
```

### DESIGN.md §13.5 Phase 4 checkbox update template

Edit `compares/DESIGN.md` around the "Phase 4 — Real-bug benchmark"
section (≈line 3507). Replace each `- [ ]` bullet with a `- [x]`
followed by a single timestamp + summary sentence. Template:

```
- [x] **Full primary bench** (all 35 frozen bugs × all applicable
      tools). **Executed 2026-MM-DD** at `--time-budget-s ${BUDGET_S}`
      across Chats 1-5; 117 cells → `<DETECTED>` detected,
      `<NULL_SILENCES>` null-silences, `<INSTALL_FAILS>` install-skipped.
      Aggregate at `compares/results/bug_bench/aggregate.json`.
```

Repeat for the smoke-test, filter-flag, post-run review, and backup
bullets (all of which are satisfied by the Chat 1-5 + Chat 6
artifacts).

### Paste-ready prompt for Chat 6

> **Task**: Execute Chat 6 of Phase 4 per
> `compares/PHASE4_EXECUTION_PLAN.md §"Chat 6 — Post-processing"`.
>
> **Pre-requisites (fail fast if missing)**: for `N` in 1..5 the path
> `/tmp/bug_bench_chat${N}/aggregate.json` and `run_manifest.json` must
> exist. If any is missing, stop and tell the operator which chat
> didn't complete.
>
> Steps:
> 1. Write `compares/scripts/rollup_bug_bench.py` per the plan (does
>    not yet exist).
> 2. Merge `/tmp/bug_bench_chat1..5/` into
>    `compares/results/bug_bench/` via rsync (additive — chats don't
>    overlap cell paths).
> 3. Rebuild the canonical `aggregate.json` from the merged tree.
> 4. Merge chat-local `run_manifest.json` into a top-level
>    `run_manifest.json` keyed by `chat`.
> 5. Run `compares/scripts/post_run_review.py --bench-root compares/
>    results/bug_bench --spot-check 3`.
> 6. Run `bash compares/scripts/backup_bug_bench.sh` to produce the
>    `.tar.zst` backup.
> 7. Update `compares/DESIGN.md §13.5 Phase 4` — flip all `- [ ]` to
>    `- [x]` with timestamp + aggregate numbers per the plan's
>    template.
> 8. Commit with message `phase4: land 117-cell real-bug bench
>    (budget=${BUDGET_S}s)`.
>
> Do not push to remote — the operator will push after reviewing the
> commit.
>
> Report: one-liner per chat + the aggregate detection count + the
> backup archive path.

---

## Appendix — common failure modes and fixes

| symptom | root cause | fix |
| :------ | :--------- | :-- |
| `[skip] noodles-XXX: install failed: ... cargo: not found` | PATH missing `/root/.cargo/bin` | `export PATH=/root/.cargo/bin:$PATH` before invoking the driver (already in every chat's Commands block). |
| `[skip] noodles-XXX: install failed: could not find noodles-vcf version pin` | non-idempotent rewriter (pre-2026-04-20) | ensure the driver has the `re.subn` patch. |
| bench hangs on `[run] biotest @ ...` with 0% CPU | 9p-mount I/O storm from historical `bug_reports/` harvest | ensure `run_biotest.py` has the snapshot-before-harvest patch (landed 2026-04-20). |
| bench hangs on `[run] biotest @ ...` with non-zero CPU | Phase C boot is normal at `B≥300s`; takes 2-5 min before first MR executes | wait |
| `[skip] seqan3-XXX: install failed: ... commit not in shallow clone` | shallow clone depth too small | `git -C compares/baselines/seqan3/source fetch --unshallow`. |
| `adapter_raise: FileNotFoundError: cargo-fuzz binary` | fuzz target not built for current noodles pin | `cargo fuzz build noodles_vcf_target --release --sanitizer none --manifest-path compares/harnesses/cargo_fuzz/fuzz/Cargo.toml`. |
| all atheris cells score 0 detections | atheris venv lacks vcfpy or biopython | `/opt/atheris-venv/bin/pip install vcfpy==0.14.0 biopython==1.86`, then `docker commit biotest-bench-setup biotest-bench:latest` to persist. |
| cell shows `confirmed_fix_silences_signal: null` for vcfpy | `_replay_trigger_silenced` has no vcfpy branch | add the branch per Chat 3 pre-work. |
| cell shows `confirmed_fix_silences_signal: null` for noodles | `_replay_trigger_silenced` has no noodles branch | add the branch per Chat 4 pre-work. |
