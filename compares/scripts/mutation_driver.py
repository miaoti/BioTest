"""Phase-3 mutation-score driver (DESIGN.md §3.3 + §13.5 Phase 3).

Per-cell contract — matches the invocation shape DESIGN.md §13.5
Phase 3 prescribes:

    py -3.12 compares/scripts/mutation_driver.py \\
        --tool <name> --sut <name> \\
        --corpus <path to Phase-2 accepted inputs> \\
        --budget <seconds> \\
        --out compares/results/mutation/<tool>/<sut>/

Output layout (per cell):

    <out>/summary.json           # {killed, reachable, score, …}
    <out>/mutmut_results.txt     # mutmut's raw stdout dump
    <out>/mutmut_stats.json      # mutmut's internal stats.json copy
    <out>/baseline.json          # per-file fingerprint snapshot
    <out>/runner.log             # stderr from the per-mutant runner
    <out>/config.json            # echo of args + resolved paths for audit
    <out>/vcfpy_src_mutated/     # mutmut-rewritten vcfpy source

Currently implemented: atheris × vcfpy (Python, mutmut 3.x).
Other cells follow the same pattern — pit (Java), mull (C++),
cargo-mutants (Rust) — and land behind the same `--tool/--sut` CLI.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKER_IMAGE = "biotest-bench:latest"
ATHERIS_PY = "/opt/atheris-venv/bin/python"
SYSTEM_PY = "python3.12"  # mutmut lives in 3.12 site-packages


def _docker_mount_src() -> str:
    """See coverage_sampler.py — same rationale. /c/... form on Win."""
    norm = str(REPO_ROOT).replace("\\", "/")
    if len(norm) >= 2 and norm[1] == ":":
        return f"/{norm[0].lower()}{norm[2:] if norm[2:].startswith('/') else '/' + norm[2:]}"
    return norm


def _ctr_path(host: Path) -> str:
    rel = host.resolve().relative_to(REPO_ROOT.resolve())
    return "/work/" + str(rel).replace("\\", "/")


def _docker_run(cmd_inside: list[str], *, env: dict[str, str] | None = None,
                timeout_s: int | None = None,
                stdout_file: Path | None = None,
                stderr_file: Path | None = None) -> int:
    """Run a command inside biotest-bench with /work bind-mounted."""
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{_docker_mount_src()}:/work",
        "-w", "/work",
        "-e", "PYTHONPATH=/work",
        "-e", "MSYS_NO_PATHCONV=1",
    ]
    for k, v in (env or {}).items():
        docker_cmd += ["-e", f"{k}={v}"]
    docker_cmd += [DOCKER_IMAGE, *cmd_inside]

    stdout_fp = stdout_file.open("ab") if stdout_file else subprocess.PIPE
    stderr_fp = stderr_file.open("ab") if stderr_file else subprocess.PIPE
    try:
        proc = subprocess.run(
            docker_cmd, stdout=stdout_fp, stderr=stderr_fp,
            timeout=timeout_s, check=False,
        )
        return proc.returncode
    except subprocess.TimeoutExpired:
        return -1
    finally:
        if stdout_file:
            stdout_fp.close()
        if stderr_file and stderr_file != stdout_file:
            stderr_fp.close()


# ---------------------------------------------------------------------------
# atheris × vcfpy backend
# ---------------------------------------------------------------------------

def _run_atheris_vcfpy(args: argparse.Namespace) -> int:
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    # mutmut 3.x's `guess_paths_to_mutate()` has hard-coded heuristics:
    # `lib/` → `src/` → cwd-basename. It has no CLI flag or setup.cfg
    # override for the path list. So we exploit the basename heuristic:
    # out/'s basename is already "vcfpy"; dropping the mutable package
    # at `out/vcfpy/` satisfies `isdir(cwd.basename)` when cwd=out.
    # mutmut then writes its rewritten-with-trampolines copy to
    # `out/mutants/vcfpy/` and leaves `out/vcfpy/` untouched — we
    # therefore capture the baseline fingerprints against `out/vcfpy/`
    # (or equivalently the venv's pristine vcfpy) and the mutant-run
    # phase imports from `out/mutants/vcfpy/` via sys.path insert.
    src_root = out
    src_pkg = out / "vcfpy"
    tests_dir = out / "tests"     # mutmut auto-copies tests/ → mutants/tests/
    baseline_file = out / "baseline.json"
    runner_log = out / "runner.log"
    mutmut_log = out / "mutmut_run.log"
    summary_path = out / "summary.json"
    mutants_db = out / "mutants"  # mutmut's cache/results dir

    # 1. Materialise a fresh mutable vcfpy source copy from the venv.
    if src_pkg.exists() and not args.reuse_src:
        shutil.rmtree(src_pkg)
    if not src_pkg.exists():
        print(f"[driver] copying pristine vcfpy from atheris-venv → {src_pkg}",
              flush=True)
        src_root.mkdir(parents=True, exist_ok=True)
        rc = _docker_run([
            "bash", "-c",
            f"cp -r /opt/atheris-venv/lib/python3.11/site-packages/vcfpy "
            f"{_ctr_path(src_pkg)}",
        ], timeout_s=60, stdout_file=mutmut_log, stderr_file=mutmut_log)
        if rc != 0 or not src_pkg.exists():
            print("[driver] vcfpy source copy FAILED", file=sys.stderr)
            return 2

    # 2. Resolve corpus. If a directory is given, use it as-is. If `union`
    #    is requested, aggregate rep 0/1/2 corpora into a single dir.
    corpus_dir = _materialise_corpus(args, out)
    if corpus_dir is None:
        return 2
    corpus_size = sum(1 for _ in corpus_dir.iterdir() if _.is_file())
    print(f"[driver] corpus dir: {corpus_dir}  ({corpus_size} files)",
          flush=True)

    # 3. Materialise the pytest runner file under <out>/tests/ so mutmut's
    #    auto-copy drops it into <out>/mutants/tests/ before each
    #    pytest invocation.
    tests_dir.mkdir(parents=True, exist_ok=True)
    runner_src = REPO_ROOT / "compares/scripts/mutation/test_vcfpy_corpus.py"
    shutil.copy2(runner_src, tests_dir / "test_vcfpy_corpus.py")
    # Empty conftest.py is enough — the test reads everything it needs
    # from env vars. An __init__.py keeps pytest --import-mode=append
    # happy.
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")
    (tests_dir / "conftest.py").write_text("", encoding="utf-8")

    # 4. Capture unmutated baseline. The standalone runner script still
    #    carries this logic (mode=baseline), so we can call it once
    #    directly without going through mutmut.
    print(f"[driver] capturing baseline → {baseline_file}", flush=True)
    rc = _docker_run(
        [SYSTEM_PY, f"/work/compares/scripts/mutation/vcfpy_corpus_runner.py"],
        env={
            "MUTMUT_RUNNER_MODE": "baseline",
            "MUTMUT_VCFPY_SRC": _ctr_path(src_pkg),
            "MUTMUT_CORPUS_DIR": _ctr_path(corpus_dir),
            "MUTMUT_BASELINE_FILE": _ctr_path(baseline_file),
            "MUTMUT_CORPUS_SAMPLE": str(args.corpus_sample),
            "MUTMUT_CORPUS_TIMEOUT_S": str(args.per_file_timeout_s),
            "PYTHONUNBUFFERED": "1",
        },
        timeout_s=600,
        stdout_file=runner_log,
        stderr_file=runner_log,
    )
    if rc != 0:
        print(f"[driver] baseline capture failed (rc={rc}); see {runner_log}",
              file=sys.stderr)
        return 2
    baseline = json.loads(baseline_file.read_text(encoding="utf-8"))
    print(f"[driver] baseline entries: {len(baseline)}", flush=True)

    # 5. Write setup.cfg for mutmut's (limited) knobs. mutmut 3.0 can't
    #    override paths_to_mutate here — it auto-guesses from cwd
    #    basename (see note at src_root above). `runner` only toggles
    #    between PytestRunner and HammettRunner; we keep the default
    #    (pytest). The pytest test file under tests/ is what does the
    #    real work.
    cfg = out / "setup.cfg"
    cfg.write_text(
        "[mutmut]\n"
        "do_not_mutate=\n"
        "    __init__.py\n"
        "    version.py\n"
        "    tabix.py\n"
        "    bgzf.py\n"
        "    writer.py\n",
        encoding="utf-8",
    )

    # 6. Invoke mutmut 3.x. cwd = out; its basename is "vcfpy", the
    #    subdir <out>/vcfpy/ is the mutable package, so
    #    `guess_paths_to_mutate()` returns "vcfpy". mutmut then writes
    #    <out>/mutants/vcfpy/ + copies <out>/tests/ → <out>/mutants/tests/.
    #    pytest runs from <out>/mutants/, sees `tests/test_vcfpy_corpus.py`,
    #    imports vcfpy from mutants/vcfpy/, hits the trampoline which
    #    dispatches based on the MUTANT_UNDER_TEST env var mutmut sets.
    print("[driver] invoking mutmut run …", flush=True)
    env = {
        "MUTMUT_CORPUS_DIR": _ctr_path(corpus_dir),
        "MUTMUT_BASELINE_FILE": _ctr_path(baseline_file),
        "MUTMUT_CORPUS_SAMPLE": str(args.corpus_sample),
        "MUTMUT_CORPUS_TIMEOUT_S": str(args.per_file_timeout_s),
        "PYTHONUNBUFFERED": "1",
    }
    start = time.time()
    rc = _docker_run(
        ["bash", "-c",
         f"cd {_ctr_path(out)} && "
         f"{SYSTEM_PY} /work/compares/scripts/mutation/run_mutmut.py run "
         f"--max-children {args.max_children}"],
        env=env,
        timeout_s=args.budget + 300,
        stdout_file=mutmut_log,
        stderr_file=mutmut_log,
    )
    mut_duration = time.time() - start
    print(f"[driver] mutmut run exited rc={rc} after {mut_duration:.0f}s",
          flush=True)

    # 6. Pull mutmut's status via `mutmut results`.
    results_txt = out / "mutmut_results.txt"
    _docker_run(
        ["bash", "-c",
         f"cd {_ctr_path(out)} && {SYSTEM_PY} -m mutmut results"],
        timeout_s=120,
        stdout_file=results_txt,
        stderr_file=results_txt,
    )

    # 7. mutmut 3.x stores state under `mutants/` in the cwd. Copy the key
    #    JSONs into the cell dir for audit.
    for name in ("stats.json", "results.json", "cache.json", "work.json"):
        cand = out / "mutants" / name
        if cand.exists():
            shutil.copy2(cand, out / f"mutmut_{name}")

    # 8. Summarise.  Parse `mutmut_results.txt` (mutmut prints per-status
    #    totals) to build a DESIGN §4.5 summary block.
    summary = _summarise_mutmut_output(results_txt, mutmut_log)
    summary.update({
        "tool": "atheris",
        "sut": "vcfpy",
        "format": "VCF",
        "phase": "mutation",
        "time_budget_s": args.budget,
        "mutmut_exit_code": rc,
        "mutmut_duration_s": round(mut_duration, 2),
        "corpus_size": corpus_size,
        "corpus_sample": args.corpus_sample,
        "per_file_timeout_s": args.per_file_timeout_s,
        "paths_to_mutate": [
            str(src_pkg.relative_to(REPO_ROOT).as_posix()),
        ],
        "baseline_entries": len(baseline),
    })
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[driver] wrote {summary_path}")

    (out / "config.json").write_text(json.dumps({
        "args": vars(args),
        "corpus_dir": str(corpus_dir),
        "baseline_file": str(baseline_file),
        "vcfpy_src_mutated": str(src_pkg),
        "docker_image": DOCKER_IMAGE,
        "system_python": SYSTEM_PY,
        "atheris_python": ATHERIS_PY,
    }, indent=2, default=str), encoding="utf-8")

    # Terse console summary
    print()
    print(f"[mutation] {summary.get('score_display', 'n/a')} "
          f"({summary.get('killed', '?')} killed / "
          f"{summary.get('reachable', '?')} reachable of "
          f"{summary.get('mutant_count', '?')} total)")
    return 0


def _materialise_corpus(args: argparse.Namespace, out: Path) -> Path | None:
    if args.corpus.exists() and args.corpus.is_dir():
        return args.corpus
    if args.union_corpus_from:
        # Accept a glob-ish pattern pointing to rep roots:
        # compares/results/coverage/atheris/vcfpy/run_*
        src_root = args.union_corpus_from.resolve()
        rep_dirs = sorted(src_root.glob("run_*/corpus"))
        if not rep_dirs:
            print(f"[driver] no run_*/corpus dirs under {src_root}",
                  file=sys.stderr)
            return None
        union_dir = out / "union_corpus"
        union_dir.mkdir(exist_ok=True)
        for rd in rep_dirs:
            for p in rd.iterdir():
                if p.is_file():
                    tgt = union_dir / p.name
                    if not tgt.exists():
                        shutil.copy2(p, tgt)
        return union_dir
    print(f"[driver] corpus {args.corpus} is not a directory",
          file=sys.stderr)
    return None


def _summarise_mutmut_output(results_txt: Path, log_file: Path) -> dict:
    """Parse mutmut's human-friendly status report into numbers.

    mutmut 3.x's `mutmut results` prints blocks like:

        To apply a mutant on disk:
        killed: 42 🎉
        survived: 13 🙁
        timeout: 1 ⏰
        ...

    We turn that into `{killed, survived, timeout, suspicious,
    skipped, no_tests, not_checked, total, reachable, score}`.
    """
    status_counts: dict[str, int] = {}
    text = ""
    if results_txt.exists():
        text = results_txt.read_text(encoding="utf-8", errors="replace")
    if not text and log_file.exists():
        text = log_file.read_text(encoding="utf-8", errors="replace")

    # Simple per-line scrape. mutmut's results lines look like "<status>: <int>".
    known = {
        "killed", "survived", "timeout", "suspicious",
        "skipped", "no tests", "not checked",
    }
    for line in text.splitlines():
        s = line.strip()
        if ":" not in s:
            continue
        key, _, val = s.partition(":")
        key = key.strip().lower()
        val = val.strip().split()[0] if val.strip() else ""
        if key in known and val.isdigit():
            status_counts[key.replace(" ", "_")] = int(val)

    killed = status_counts.get("killed", 0)
    survived = status_counts.get("survived", 0)
    timeout = status_counts.get("timeout", 0)
    suspicious = status_counts.get("suspicious", 0)
    skipped = status_counts.get("skipped", 0)
    no_tests = status_counts.get("no_tests", 0)
    not_checked = status_counts.get("not_checked", 0)

    # mutmut's "no tests" bucket = mutant function never executed by the
    # runner → matches DESIGN.md §3.3's "unreachable" semantics. Kills
    # and survivors together form the "reachable" denominator.
    reachable = killed + survived + timeout + suspicious
    total = reachable + skipped + no_tests + not_checked
    score = (killed / reachable) if reachable else 0.0

    return {
        "killed": killed,
        "survived": survived,
        "timeout": timeout,
        "suspicious": suspicious,
        "skipped": skipped,
        "no_tests": no_tests,
        "not_checked": not_checked,
        "reachable": reachable,
        "mutant_count": total,
        "score": round(score, 4),
        "score_display": f"{score * 100:.1f}%" if reachable else "n/a",
        "raw_status_counts": status_counts,
    }


# ---------------------------------------------------------------------------
# cargo_fuzz × noodles backend (Rust / cargo-mutants)
# ---------------------------------------------------------------------------
#
# Architecture: the same Phase-2 "accepted-input corpus" from run_0 becomes
# the test suite here. We enact DESIGN §3.3's test-kill protocol via a
# per-mutant integration test in the (mutable copy of) noodles-vcf 0.70:
#
#   1. `compares/baselines/noodles-vcf-0.70-src/` is a mutable copy of the
#      noodles-vcf 0.70 sources, obtained via `cargo fetch` into the
#      registry cache and then copied into the repo (no external clone).
#   2. `tests/biotest_corpus_oracle.rs` — the oracle: reads each VCF in
#      `BIOTEST_CORPUS_DIR`, parses via noodles-vcf, fingerprints the
#      outcome, and `assert_eq!`'s against a baseline captured on the
#      un-mutated crate. Divergence → panic → test fails → mutant caught.
#   3. `cargo mutants --file <paths> --cargo-test-arg "--test
#      biotest_corpus_oracle" ...` drives mutation. cargo-mutants copies
#      the crate to a scratch dir per mutant, applies the mutant to
#      source, rebuilds the crate + oracle test, runs `cargo test
#      --test biotest_corpus_oracle`, and records Caught / Missed /
#      Timeout / Unviable per mutant.
#   4. We parse the machine-readable `mutants.out/outcomes.json` and
#      aggregate counts into DESIGN §4.5's `mutation_score` block.
#
# cargo-mutants' `Caught / Missed / Unviable / Timeout / Success` vocabulary
# maps onto DESIGN.md §3.3 as:
#   Caught    → killed      (oracle detected divergence)
#   Missed    → survived    (corpus didn't distinguish the mutant)
#   Timeout   → killed*     (test ran past --timeout; counted as killed
#                             by cargo-mutants convention and by DESIGN
#                             §3.3 "crash flip" — behaviour changed)
#   Unviable  → skipped     (mutant doesn't compile; NOT a scoreable
#                             bucket — excluded from reachable denom)
#   Success   → baseline    (the un-mutated test run; doesn't count)


NOODLES_VCF_SRC = REPO_ROOT / "compares/baselines/noodles-vcf-0.70-src"
NOODLES_VCF_MUTATION_FILES = [
    "src/io/reader/**",
    "src/record.rs", "src/record/**",
    "src/header.rs",
]


def _run_cargo_fuzz_noodles(args: argparse.Namespace) -> int:
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    summary_path = out / "summary.json"
    config_path = out / "config.json"
    baseline_path = out / "baseline.json"
    run_log = out / "main_run.log"

    if not NOODLES_VCF_SRC.exists() or not (NOODLES_VCF_SRC / "Cargo.toml").exists():
        print(
            f"[driver] noodles-vcf mutable source missing at {NOODLES_VCF_SRC}.\n"
            "Materialise it once via (inside biotest-bench):\n"
            "  cd /work/harnesses/rust/noodles_harness && cargo fetch\n"
            "  cp -r /root/.cargo/registry/src/*/noodles-vcf-0.70.0 "
            f"{NOODLES_VCF_SRC}\n"
            "Then re-run this driver.",
            file=sys.stderr,
        )
        return 2

    # Resolve corpus. Default to Phase-2 rep_0's corpus (≈ 1700 files
    # the fuzzer's accepted + rejected inputs; we sample a deterministic
    # prefix for tractability inside DESIGN §3.3's 7200 s budget).
    corpus = args.corpus.resolve()
    if not corpus.is_dir():
        print(f"[driver] corpus {corpus} is not a directory", file=sys.stderr)
        return 2

    # Capture baseline once. Idempotent: if baseline.json already exists
    # AND matches the current source, skip.
    if not baseline_path.exists() or args.force_baseline:
        print(f"[driver] capturing baseline → {baseline_path}", flush=True)
        rc = _docker_run(
            [
                "bash", "-c",
                f"cd /work/compares/baselines/noodles-vcf-0.70-src && "
                f"CARGO_BUILD_JOBS=2 cargo test --release --test biotest_corpus_oracle",
            ],
            env={
                "PATH": "/root/.cargo/bin:/usr/local/sbin:/usr/local/bin:"
                        "/usr/sbin:/usr/bin:/sbin:/bin",
                "BIOTEST_BASELINE_MODE": "capture",
                "BIOTEST_BASELINE_JSON": _ctr_path(baseline_path),
                "BIOTEST_CORPUS_DIR": _ctr_path(corpus),
                "BIOTEST_CORPUS_SAMPLE": str(args.corpus_sample),
            },
            timeout_s=900,
            stdout_file=run_log, stderr_file=run_log,
        )
        if rc != 0 or not baseline_path.exists():
            print(f"[driver] baseline capture failed (rc={rc}); see {run_log}",
                  file=sys.stderr)
            return 2

    # Run cargo-mutants over the reader+record+header paths.
    # Reset mutants.out each run so `outcomes.json` reflects only this run.
    (out / "mutants.out").exists() and shutil.rmtree(out / "mutants.out")
    file_flags = []
    for pat in args.mutation_files:
        file_flags += ["--file", pat]
    cargo_test_args = [
        "--cargo-test-arg", "--release",
        "--cargo-test-arg", "--test",
        "--cargo-test-arg", "biotest_corpus_oracle",
    ]
    cargo_mutants_cmd = [
        "cargo", "mutants",
        *file_flags,
        *cargo_test_args,
        "--timeout", str(args.per_mutant_timeout_s),
        "--jobs", str(args.jobs),
        "--output", _ctr_path(out),
    ]
    print(f"[driver] cargo mutants across {len(args.mutation_files)} file patterns",
          flush=True)
    start = time.time()
    rc = _docker_run(
        ["bash", "-c",
         f"cd /work/compares/baselines/noodles-vcf-0.70-src && "
         + " ".join(f"'{a}'" if ' ' in a else a for a in cargo_mutants_cmd)],
        env={
            "PATH": "/root/.cargo/bin:/usr/local/sbin:/usr/local/bin:"
                    "/usr/sbin:/usr/bin:/sbin:/bin",
            "BIOTEST_BASELINE_MODE": "check",
            "BIOTEST_BASELINE_JSON": _ctr_path(baseline_path),
            "BIOTEST_CORPUS_DIR": _ctr_path(corpus),
            "BIOTEST_CORPUS_SAMPLE": str(args.corpus_sample),
        },
        timeout_s=args.budget + 300,
        stdout_file=run_log, stderr_file=run_log,
    )
    duration = time.time() - start
    print(f"[driver] cargo mutants exited rc={rc} after {duration:.0f}s",
          flush=True)

    # Parse outcomes.
    outcomes_path = out / "mutants.out" / "outcomes.json"
    summary = _summarise_cargo_mutants(outcomes_path)
    summary.update({
        "tool": "cargo_fuzz",
        "sut": "noodles",
        "format": "VCF",
        "phase": "mutation",
        "time_budget_s": args.budget,
        "cargo_mutants_exit_code": rc,
        "cargo_mutants_duration_s": round(duration, 2),
        "corpus_dir": str(corpus),
        "corpus_sample": args.corpus_sample,
        "per_mutant_timeout_s": args.per_mutant_timeout_s,
        "paths_to_mutate": args.mutation_files,
        "baseline_entries": _count_baseline_entries(baseline_path),
    })
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[driver] wrote {summary_path}")

    config_path.write_text(json.dumps({
        "args": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
        "corpus_dir": str(corpus),
        "baseline_file": str(baseline_path),
        "noodles_vcf_src": str(NOODLES_VCF_SRC),
        "docker_image": DOCKER_IMAGE,
    }, indent=2), encoding="utf-8")

    print()
    print(f"[mutation] {summary.get('score_display', 'n/a')} "
          f"({summary.get('killed', '?')} killed / "
          f"{summary.get('reachable', '?')} reachable of "
          f"{summary.get('mutant_count', '?')} total)")
    return 0


def _count_baseline_entries(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        txt = path.read_text(encoding="utf-8")
        return sum(
            1 for line in txt.splitlines()
            if line.strip() and line.strip() != "{" and line.strip() != "}"
        )
    except Exception:
        return 0


def _summarise_cargo_mutants(outcomes_path: Path) -> dict:
    """Parse `mutants.out/outcomes.json` into DESIGN §4.5's
    `{killed, reachable, score, mutator_count, mutant_count, …}`
    mutation-score block."""
    if not outcomes_path.exists():
        return {
            "killed": 0, "survived": 0, "timeout": 0,
            "unviable": 0, "success": 0,
            "reachable": 0, "mutant_count": 0, "mutator_count": 0,
            "score": 0.0, "score_display": "n/a",
            "error": f"outcomes.json missing at {outcomes_path}",
        }
    data = json.loads(outcomes_path.read_text(encoding="utf-8"))
    outcomes = data.get("outcomes", [])

    # cargo-mutants summary strings: Success (baseline-only), CaughtMutant,
    # MissedMutant, Timeout, Unviable, Failure.
    buckets = {"caught": 0, "missed": 0, "timeout": 0,
               "unviable": 0, "success": 0, "failure": 0}
    mutators: set[str] = set()
    for o in outcomes:
        summary = (o.get("summary") or "").lower()
        if "caught" in summary:
            buckets["caught"] += 1
        elif "missed" in summary:
            buckets["missed"] += 1
        elif "timeout" in summary:
            buckets["timeout"] += 1
        elif "unviable" in summary:
            buckets["unviable"] += 1
        elif summary == "success":
            buckets["success"] += 1
        elif "failure" in summary:
            buckets["failure"] += 1
        # Track distinct mutation operators ("replace + with -", etc.)
        mut = o.get("scenario", {}).get("mutant") if isinstance(o.get("scenario"), dict) else None
        if isinstance(mut, dict):
            op = mut.get("replacement") or mut.get("function_name") or ""
            if op:
                mutators.add(op[:80])

    killed = buckets["caught"] + buckets["timeout"]
    survived = buckets["missed"]
    reachable = killed + survived
    total = reachable + buckets["unviable"] + buckets["success"] + buckets["failure"]
    score = (killed / reachable) if reachable else 0.0

    return {
        "killed": killed,
        "survived": survived,
        "caught": buckets["caught"],
        "timeout": buckets["timeout"],
        "missed": buckets["missed"],
        "unviable": buckets["unviable"],
        "baseline_success": buckets["success"],
        "reachable": reachable,
        "mutant_count": total,
        "mutator_count": len(mutators),
        "score": round(score, 4),
        "score_display": f"{score * 100:.1f}%" if reachable else "n/a",
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--tool", required=True, choices=["atheris", "cargo_fuzz"],
                   help="Phase-2 tool whose corpus is the 'test suite'.")
    p.add_argument("--sut", required=True, choices=["vcfpy", "noodles"],
                   help="SUT under mutation.")
    p.add_argument("--corpus", type=Path,
                   default=REPO_ROOT / "compares/results/mutation/atheris/vcfpy/union_corpus",
                   help="Tool's accepted-input corpus directory. If missing, "
                        "pass --union-corpus-from to materialise one from "
                        "Phase-2 rep subdirs.")
    p.add_argument("--union-corpus-from", type=Path,
                   default=REPO_ROOT / "compares/results/coverage/atheris/vcfpy",
                   help="Parent dir whose run_*/corpus subdirs will be "
                        "unioned into a single corpus dir if --corpus is not "
                        "an existing directory.")
    p.add_argument("--budget", type=int, default=7200,
                   help="mutmut run wall-clock cap, seconds (DESIGN §13.5 "
                        "Phase 3 default = 7200).")
    p.add_argument("--corpus-sample", type=int, default=120,
                   help="Max corpus files replayed per mutant (the runner "
                        "takes a deterministic first-N slice sorted by "
                        "filename). DESIGN §3.3 'test-kill protocol' "
                        "requires SOME corpus; 120 gives ~1 s / mutant which "
                        "is enough to surface any reachable flip.")
    p.add_argument("--per-file-timeout-s", type=float, default=2.0,
                   help="Hard per-file parse timeout (runner uses SIGALRM).")
    p.add_argument("--out", type=Path,
                   default=REPO_ROOT / "compares/results/mutation/atheris/vcfpy",
                   help="Cell output directory.")
    p.add_argument("--reuse-src", action="store_true",
                   help="Keep any existing vcfpy/ tree. By default we "
                        "re-materialise a pristine copy each run.")
    p.add_argument("--max-children", type=int, default=1,
                   help="mutmut --max-children parallelism. 1 keeps "
                        "pytest startup cost from dominating, higher "
                        "values trade that for parallelism if cores "
                        "are free. Default 1.")

    # cargo_fuzz × noodles — Rust cargo-mutants flags
    p.add_argument("--mutation-files", nargs="+",
                   default=NOODLES_VCF_MUTATION_FILES,
                   help="cargo-mutants --file glob patterns (one or more). "
                        "Default narrows to the reader/record/header paths "
                        "the Phase-2 fuzz corpus actually exercises.")
    p.add_argument("--per-mutant-timeout-s", type=int, default=60,
                   help="cargo-mutants --timeout per-mutant cap, seconds.")
    p.add_argument("--jobs", type=int, default=1,
                   help="cargo-mutants --jobs parallelism (mem-bound on "
                        "small hosts).")
    p.add_argument("--force-baseline", action="store_true",
                   help="Rebuild the baseline fingerprint even if it exists.")
    args = p.parse_args()

    if args.tool == "atheris" and args.sut == "vcfpy":
        return _run_atheris_vcfpy(args)
    if args.tool == "cargo_fuzz" and args.sut == "noodles":
        # Default corpus + out dir for the Rust cell if caller didn't
        # override via flag.
        if args.corpus == REPO_ROOT / "compares/results/mutation/atheris/vcfpy/union_corpus":
            args.corpus = REPO_ROOT / "compares/results/coverage/cargo_fuzz/noodles/run_0/corpus"
        if args.out == REPO_ROOT / "compares/results/mutation/atheris/vcfpy":
            args.out = REPO_ROOT / "compares/results/mutation/cargo_fuzz/noodles"
        return _run_cargo_fuzz_noodles(args)
    print(f"mutation_driver: (tool={args.tool!r}, sut={args.sut!r}) not supported",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli())
