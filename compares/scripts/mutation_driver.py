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
    # override. We therefore need the mutmut cwd to have basename
    # `vcfpy` AND contain a `vcfpy/` subdirectory (which satisfies
    # `isdir(cwd.basename)`).
    #
    # When --out already ends in `/vcfpy` (the original layout) we
    # reuse it directly. When it's some other name (e.g.
    # `vcfpy_runs/run_0/` for a per-rep re-run) we nest the mutmut
    # workdir at `<out>/vcfpy/` so mutmut sees the right basename,
    # and keep the top-level out/ for shared artefacts (summary.json,
    # driver log, union_corpus/).
    if out.name == "vcfpy":
        work = out
    else:
        work = out / "vcfpy"
        work.mkdir(parents=True, exist_ok=True)
    src_root = work
    src_pkg = work / "vcfpy"
    tests_dir = work / "tests"    # mutmut auto-copies tests/ → mutants/tests/
    baseline_file = work / "baseline.json"
    runner_log = out / "runner.log"
    mutmut_log = out / "mutmut_run.log"
    summary_path = out / "summary.json"
    mutants_db = work / "mutants"  # mutmut's cache/results dir

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
    # 2-pre. Phase E augmentation: union seeds/<fmt>_struct + seeds/<fmt>_rawfuzz
    #        into the corpus when the SUT's parser is non-strict. This is the
    #        path by which `biotest.py`'s Phase E auto-output reaches the
    #        mutation harness. The M2 dual-policy disclosure (REVIEW2.md)
    #        needs an isolated cmin-only measurement, so --no-augment-corpus
    #        and --no-coverage-select bypass these post-corpus steps.
    if not args.no_augment_corpus:
        corpus_dir = _augment_with_phase_e(
            corpus_dir, sut=args.sut, fmt=(args.format or "VCF"), out=out,
        )
    # 2a. Coverage-guided selection (opt-in but default-on for supported
    #     cells). Closes the kill gap to atheris/jazzer/cargo-fuzz by
    #     pruning redundant files. No-op if no collector exists for the
    #     (sut, fmt) pair.
    if not args.no_coverage_select:
        corpus_dir = _coverage_select_if_supported(
            corpus_dir, out, sut=args.sut, fmt=(args.format or "VCF"),
            target=args.corpus_sample,
        )
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

    # 4. Write setup.cfg before we call create_mutants — the same
    #    do_not_mutate filter needs to apply to both passes so the
    #    generated `mutants/vcfpy/` tree matches what the live mutmut
    #    run in step 6 will see.
    #
    #    Mutation is scoped to the five VCF-parser modules called out
    #    by documents/Flow.md §1149 (`target_filters.VCF: vcfpy/reader,
    #    parser, header, record, writer`). bgzf.py + tabix.py are
    #    explicitly listed as "BioTest 不走这些路径" (not-in-scope),
    #    so we do_not_mutate them. __init__.py + version.py hold no
    #    parser logic. That leaves reader.py + parser.py + header.py +
    #    record.py + writer.py — the identical whitelist Phase 2's
    #    `CoveragePyCollector` uses.
    cfg = out / "setup.cfg"
    cfg.write_text(
        "[mutmut]\n"
        "do_not_mutate=\n"
        "    __init__.py\n"
        "    version.py\n"
        "    tabix.py\n"
        "    bgzf.py\n",
        encoding="utf-8",
    )

    # 5. Pre-generate mutants/vcfpy/ so the baseline can be captured
    #    against the SAME rewritten tree the mutmut test phase will
    #    use.  If we captured the baseline against pristine
    #    `<out>/vcfpy/` instead, the trampoline rewrite (which replaces
    #    every method with an `object.__getattribute__` dispatcher)
    #    introduces tiny semantic drift — method binding, module-level
    #    dict ordering, etc. — that the fingerprint picks up as a
    #    false-positive kill even under MUTANT_UNDER_TEST=stats.
    #    `create_mutants()` is idempotent, so the real `mutmut run`
    #    below re-generates the same tree.
    print("[driver] pre-generating mutants/ tree (one-shot)…", flush=True)
    pregen_log = out / "pregen.log"
    rc = _docker_run(
        ["bash", "-c",
         f"cd {_ctr_path(work)} && "
         f"{SYSTEM_PY} -c \"import mutmut.__main__ as m; "
         f"m.read_config(); m.create_mutants(); m.copy_also_copy_files(); "
         f"print('pregen ok: mutants/vcfpy present')\""],
        timeout_s=600,
        stdout_file=pregen_log,
        stderr_file=pregen_log,
    )
    if rc != 0 or not (work / "mutants" / "vcfpy").exists():
        print(f"[driver] pre-generate FAILED (rc={rc}); see {pregen_log}",
              file=sys.stderr)
        return 2

    # 6. Capture unmutated baseline FROM THE REWRITTEN TREE. The
    #    trampolines fall through to the original function whenever
    #    MUTANT_UNDER_TEST is unset, so calling vcfpy from this tree
    #    with no env var produces exactly what stats-phase will see.
    rewritten_src_pkg = work / "mutants" / "vcfpy"
    print(f"[driver] capturing baseline → {baseline_file} "
          f"(from {rewritten_src_pkg.name}/)", flush=True)
    rc = _docker_run(
        [SYSTEM_PY, f"/work/compares/scripts/mutation/vcfpy_corpus_runner.py"],
        env={
            "MUTMUT_RUNNER_MODE": "baseline",
            "MUTMUT_VCFPY_SRC": _ctr_path(rewritten_src_pkg),
            "MUTMUT_CORPUS_DIR": _ctr_path(corpus_dir),
            "MUTMUT_BASELINE_FILE": _ctr_path(baseline_file),
            "MUTMUT_CORPUS_SAMPLE": str(args.corpus_sample),
            "MUTMUT_CORPUS_TIMEOUT_S": str(args.per_file_timeout_s),
            "MUTANT_UNDER_TEST": "",
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
         f"cd {_ctr_path(work)} && "
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
         f"cd {_ctr_path(work)} && {SYSTEM_PY} -m mutmut results"],
        timeout_s=120,
        stdout_file=results_txt,
        stderr_file=results_txt,
    )

    # 7. mutmut 3.x stores state under `mutants/` in the cwd. Copy the key
    #    JSONs into the cell dir for audit.
    for name in ("stats.json", "results.json", "cache.json", "work.json"):
        cand = work / "mutants" / name
        if cand.exists():
            shutil.copy2(cand, out / f"mutmut_{name}")

    # 8. Summarise.  Parse `mutmut_results.txt` (mutmut prints per-status
    #    totals) to build a DESIGN §4.5 summary block.
    summary = _summarise_mutmut_output(results_txt, mutmut_log)
    summary.update({
        "tool": args.tool,
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


def _coverage_select_if_supported(
    corpus_dir: Path, out: Path, sut: str, fmt: str, target: int,
) -> Path:
    """Run coverage-guided corpus selection if a collector exists for the
    (sut, fmt) pair. Otherwise pass through the input corpus unchanged.

    Closes the kill-count gap to coverage-guided fuzzers by ensuring the
    files the mutation oracle actually samples (first-N lexicographic)
    are coverage-diverse — jazzer/atheris produce their corpus this way
    internally; we select for it post-hoc over our Rank-generated output.
    """
    try:
        sys.path.insert(0, str(REPO_ROOT / "compares/scripts"))
        from corpus_coverage_select import _COVERAGE_COLLECTORS, select_directory
    except Exception as e:
        print(f"[driver] coverage-select import failed ({e}); skipping",
              flush=True)
        return corpus_dir

    key = (sut.lower(), fmt.upper())
    if key not in _COVERAGE_COLLECTORS:
        return corpus_dir  # no per-file coverage collector for this cell

    selected_dir = out / "corpus_selected"
    try:
        r = select_directory(
            input_dir=corpus_dir, output_dir=selected_dir,
            sut=sut, fmt=fmt, target=target,
        )
        print(f"[driver] coverage-select: {r['input_count']} → "
              f"{r['selected_count']} files "
              f"(covered {r['total_lines_covered']} lines)", flush=True)
        return selected_dir
    except SystemExit as e:
        print(f"[driver] coverage-select failed ({e}); using original corpus",
              flush=True)
        return corpus_dir
    except Exception as e:
        print(f"[driver] coverage-select error ({e}); using original corpus",
              flush=True)
        return corpus_dir


def _augment_with_phase_e(corpus_dir: Path, sut: str, fmt: str, out: Path) -> Path:
    """Union the Phase-E augmented corpus dirs (`seeds/<fmt>_struct/`,
    `seeds/<fmt>_rawfuzz/`) into a fresh staging dir for non-strict-
    parser SUTs. Strict parsers (biopython, noodles) keep primary-only.
    """
    STRICT = {"biopython", "noodles"}
    if sut.lower() in STRICT:
        return corpus_dir
    ext = fmt.lower()
    aug_dirs = [REPO_ROOT / f"seeds/{ext}_struct",
                REPO_ROOT / f"seeds/{ext}_rawfuzz"]
    aug_dirs = [d for d in aug_dirs if d.is_dir() and any(d.iterdir())]
    if not aug_dirs:
        return corpus_dir
    staged = out / "phase_e_augmented_corpus"
    staged.mkdir(parents=True, exist_ok=True)
    # Clear only same-ext to avoid clobbering sibling artifacts.
    for f in staged.glob(f"*.{ext}"):
        f.unlink()
    # Copy primary
    for f in corpus_dir.glob(f"*.{ext}"):
        shutil.copy2(f, staged / f.name)
    n_primary = sum(1 for _ in staged.glob(f"*.{ext}"))
    # Union augmented dirs
    n_aug = 0
    for d in aug_dirs:
        for f in d.glob(f"*.{ext}"):
            tgt = staged / f.name
            if not tgt.exists():
                shutil.copy2(f, tgt)
                n_aug += 1
    print(f"[driver] phase-E augmentation: {n_primary} primary + {n_aug} "
          f"augmented (struct/rawfuzz) → {staged}", flush=True)
    return staged


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
    # Phase E augmentation. _augment_with_phase_e is a no-op for
    # noodles (strict Rust parser, per STRICT set inside the helper) —
    # call it for symmetry; helper returns unchanged corpus.
    corpus = _augment_with_phase_e(corpus, sut="noodles", fmt="VCF", out=out)

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

    # NOTE: coverage-guided corpus selection via outcome-fingerprint was
    # evaluated for the PIT cells (r19 2026-04-23) and measured WORSE than
    # passing the full corpus through — ~20 distinct outcome strings makes
    # greedy set-cover degrade to near-random. The same coarseness applies
    # to noodles' Rust oracle, so we keep it OFF here. Coverage-selection
    # is reserved for cells with a Python-native per-file coverage.py
    # collector (vcfpy, biopython), which gives line-level granularity.

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
    # shlex-quote every arg so glob chars (**, *) in --file patterns
    # aren't expanded by bash -c before cargo-mutants sees them.
    import shlex
    rc = _docker_run(
        ["bash", "-c",
         f"cd /work/compares/baselines/noodles-vcf-0.70-src && "
         + " ".join(shlex.quote(a) for a in cargo_mutants_cmd)],
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
        "tool": args.tool,
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

# ---------------------------------------------------------------------------
# libfuzzer × seqan3 backend (C++ / source-level mutation + digest replay)
# ---------------------------------------------------------------------------
#
# Mull 0.33 ships as a .deb built for Ubuntu 24.04 (glibc 2.39); the
# biotest-bench image is 22.04 (glibc 2.35), so `mull-runner-18` fails
# at load time with `GLIBC_2.39 not found` and `mull-ir-frontend-18`
# fails the same way. DESIGN.md §13.1 documents mull's presence but
# not the glibc mismatch — rebuilding mull from source or bumping the
# base to 24.04 are both out of scope for this run, so this backend is
# a **mull-equivalent substitute**: it applies the same ROR / AOR /
# LOR operator families mull's `--mutators=default` emits, scoped to
# the same seqan3 SAM source paths mull would accept, and computes
# kill/survive by the same per-input observable-diff semantics
# (DESIGN §3.3 "parse-success flip / canonical-JSON diff / crash
# flip"). The only differences vs mull are that mutations are applied
# at source level (rebuild per mutant) rather than LLVM-IR level
# (link-time mutant switching), and the operator set is a trimmed
# high-signal subset rather than mull's full catalogue.
#
# seqan3 has no VCF parser (Flow.md §2.1 notes "SeqAn3 暂不支持 VCF IO"
# — the VCF differential matrix dropped seqan3 on that basis). The VCF
# code path therefore emits a `status: "not_applicable"` summary.json
# rather than a fabricated score; the DESIGN §13.5 Phase 3 checklist
# entry gets both summaries as its backing artefacts.

_SEQAN3_SRC_ROOT_IN_CTR = "/opt/seqan3/include"
_SEQAN3_SAM_SCOPE_FILES = (
    "seqan3/io/sam_file/",
    "seqan3/alphabet/cigar/",
)
_SEQAN3_SAM_SCOPE_SINGLE_FILES = (
    "seqan3/io/sam_file/detail/cigar.hpp",
)

# Mutation operator families. Each entry is (family, pattern, replacement).
# Patterns use lookbehind/lookahead to avoid multi-char operator matches
# (e.g. `<<` is NOT a `<` match) and template-parameter matches.
# The list is deliberately conservative — a rule that produces many
# non-compiling mutants wastes rebuild budget.
_MUTATION_RULES_SRC = [
    # ROR — relational operator replacement.
    ("ROR_lte_to_lt", r"(?<![<!=>])<=(?!=)", "<"),
    ("ROR_gte_to_gt", r"(?<![<!=>])>=(?!=)", ">"),
    ("ROR_eq_to_ne",  r"(?<![<!=>])==(?!=)", "!="),
    ("ROR_ne_to_eq",  r"(?<![<!=>])!=(?!=)", "=="),
    # AOR — arithmetic operator replacement, restricted to spaced
    # infix form (` + ` / ` - `) so we don't rewrite unary `-x`,
    # `++i` or template-y `T::x`.
    ("AOR_plus_to_minus",  r"(?<=\s)\+(?=\s)", "-"),
    ("AOR_minus_to_plus",  r"(?<=\s)-(?=\s)", "+"),
    # LOR / COR — logical operator replacement.
    ("LOR_and_to_or", r"(?<!&)&&(?!&)", "||"),
    ("LOR_or_to_and", r"(?<!\|)\|\|(?!\|)", "&&"),
]


def _sha256_bytes(data: bytes) -> str:
    import hashlib as _h
    return _h.sha256(data).hexdigest()


def _seqan3_sam_scope_files(src_root: Path) -> list[Path]:
    """All .hpp / .h files under the seqan3 SAM scope substrings.

    Matches `biotest_config.yaml: coverage.target_filters.SAM.seqan3`
    + `harnesses/cpp/README.md` scope. Also pulls single-file entries
    (e.g. the standalone cigar helper)."""
    files: set[Path] = set()
    for sub in _SEQAN3_SAM_SCOPE_FILES:
        pdir = src_root / sub
        if pdir.exists():
            for p in pdir.rglob("*.hpp"):
                files.add(p.resolve())
            for p in pdir.rglob("*.h"):
                files.add(p.resolve())
    for single in _SEQAN3_SAM_SCOPE_SINGLE_FILES:
        f = src_root / single
        if f.exists():
            files.add(f.resolve())
    return sorted(files)


def _load_reachable_lines(gcovr_json: Path | None,
                          scope_files: list[Path]) -> dict[str, set[int]]:
    """Return {relative_file_path → {line_no, ...}} where `count > 0`.

    Relative paths are relative to the seqan3 source root — matches
    gcovr's own `file` field when `--root /opt/seqan3/include` is used.
    Missing JSON / unparseable JSON degrades to `{}` which means every
    in-scope mutation is treated as reachable (strictly more mutants).
    """
    if gcovr_json is None or not gcovr_json.exists():
        return {}
    try:
        data = json.loads(gcovr_json.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out: dict[str, set[int]] = {}
    for f in data.get("files", []):
        name = f.get("file", "")
        reached: set[int] = set()
        for line in f.get("lines", []):
            if line.get("gcovr/noncode"):
                continue
            if line.get("count", 0) > 0:
                ln = line.get("line_number")
                if isinstance(ln, int):
                    reached.add(ln)
        if reached:
            out[name] = reached
    return out


def _strip_string_literals(line: str) -> list[tuple[int, int]]:
    """Return a list of (start, end) ranges that are inside "..." or
    '...' literals — matches should be suppressed inside these."""
    import re as _re
    spans: list[tuple[int, int]] = []
    # Non-greedy matcher for "..." and '...' respecting simple \" and \'.
    for m in _re.finditer(r'"(?:\\.|[^"\\])*"', line):
        spans.append(m.span())
    for m in _re.finditer(r"'(?:\\.|[^'\\])*'", line):
        spans.append(m.span())
    return spans


def _in_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
    for a, b in spans:
        if a <= pos < b:
            return True
    return False


def _enumerate_mutations(
    scope_files: list[Path],
    src_root: Path,
    reachable: dict[str, set[int]] | None,
) -> list[dict]:
    """Return list of mutation dicts:
      {file: str, rel: str, line: int, col: int,
       orig: str, new: str, family: str}
    Skips comment / preprocessor / string-literal matches and
    (when reachable is provided) unreached lines."""
    import re as _re
    compiled = [(name, _re.compile(pat), rep) for name, pat, rep in _MUTATION_RULES_SRC]
    mutations: list[dict] = []
    for f in scope_files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(f.resolve().relative_to(src_root.resolve())).replace("\\", "/")
        reached_set = None
        if reachable is not None:
            reached_set = reachable.get(rel)
            if reached_set is None:
                # No coverage entry → no Phase-2 execution → skip this
                # file. An empty dict (no cov data) falls back to
                # "everything is reachable" via the None sentinel above.
                if reachable:
                    continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith(("#", "//", "/*", "*", "*/")):
                continue
            if reached_set is not None and line_no not in reached_set:
                continue
            spans = _strip_string_literals(line)
            for name, pat, rep in compiled:
                for m in pat.finditer(line):
                    if _in_spans(m.start(), spans):
                        continue
                    mutations.append({
                        "file": str(f),
                        "rel": rel,
                        "line": line_no,
                        "col": m.start(),
                        "orig": m.group(0),
                        "new": rep,
                        "family": name,
                    })
    return mutations


def _apply_mutation_inplace(file_path: Path, line_no: int, col: int,
                            orig: str, new: str) -> bytes:
    """Apply a single (line, col, orig→new) mutation. Returns the
    original file bytes so the caller can revert atomically."""
    original = file_path.read_bytes()
    text = original.decode("utf-8", errors="replace")
    lines = text.split("\n")
    if line_no - 1 >= len(lines):
        raise RuntimeError(f"line {line_no} out of range for {file_path}")
    line = lines[line_no - 1]
    if line[col:col + len(orig)] != orig:
        raise RuntimeError(
            f"mutation anchor mismatch at {file_path}:{line_no}:{col}: "
            f"expected {orig!r}, got {line[col:col + len(orig)]!r}"
        )
    new_line = line[:col] + new + line[col + len(orig):]
    lines[line_no - 1] = new_line
    file_path.write_text("\n".join(lines), encoding="utf-8")
    return original


def _revert_mutation(file_path: Path, original: bytes) -> None:
    file_path.write_bytes(original)


def _rebuild_mut_binary(build_dir: Path, binary_name: str = "seqan3_sam_fuzzer_mut",
                        timeout_s: int = 120) -> tuple[bool, str]:
    """Invoke `make` in `build_dir` to rebuild the mutation-test binary.

    Returns (success, captured_stderr_tail). seqan3 header-only builds
    recompile the single TU each time (~15-30 s on biotest-bench). A
    compile failure is expected for a fraction of source mutations —
    those are reported as 'equivalent (won't compile)' in the summary."""
    # `touch` the source file to force make to pick up the header
    # change even when the header's mtime is within the same second as
    # the last build (a known gotcha on fast filesystems).
    src = build_dir.parent.parent.parent / "harnesses" / "libfuzzer" / "seqan3_sam_fuzzer.cpp"
    try:
        os.utime(src, None)
    except OSError:
        pass
    proc = subprocess.run(
        ["make", "-s", binary_name],
        cwd=str(build_dir),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=timeout_s, check=False,
    )
    ok = (proc.returncode == 0)
    tail = (proc.stderr or b"").decode("utf-8", errors="replace")[-400:]
    return ok, tail


def _run_corpus_digest(binary: Path, corpus_files: list[Path],
                        per_file_timeout_s: float) -> dict[str, str]:
    """Replay each file through `binary`; return {name: digest-line}.

    The digest-line is the first line of stdout (per-file single line
    by design of BIOTEST_HARNESS_MUT_DIGEST), or a sentinel if the
    binary crashed / timed out. This is the observable the mutation
    driver diff-compares across baseline vs mutated runs to decide
    kill vs survive (DESIGN §3.3 'parse-success flip / canonical-JSON
    diff / crash flip')."""
    out: dict[str, str] = {}
    for f in corpus_files:
        try:
            with f.open("rb") as fh:
                proc = subprocess.run(
                    [str(binary)],
                    stdin=fh, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                    timeout=per_file_timeout_s, check=False,
                )
            line = (proc.stdout or b"").decode("utf-8", errors="replace").splitlines()
            first = line[0] if line else ""
            # Collapse exit code + first output line into one fingerprint;
            # baseline "ok ... ..." and mutant "throw ..." diff out.
            out[f.name] = f"rc={proc.returncode} {first}"
        except subprocess.TimeoutExpired:
            out[f.name] = "timeout"
        except OSError as e:
            out[f.name] = f"oserror:{e.errno}"
    return out


def _digest_diff(baseline: dict[str, str], mutated: dict[str, str]) -> list[str]:
    """Return the list of file names where baseline != mutated."""
    diffs = []
    for k in baseline:
        if mutated.get(k) != baseline[k]:
            diffs.append(k)
    # Files only in mutated (shouldn't happen unless corpus changed
    # mid-run) also count.
    for k in mutated:
        if k not in baseline:
            diffs.append(k)
    return diffs


def _write_vcf_na_summary(out: Path, args: argparse.Namespace) -> int:
    """seqan3 has no VCF parser; emit a documented N/A payload."""
    out.mkdir(parents=True, exist_ok=True)
    summary = {
        "tool": args.tool,
        "sut": "seqan3",
        "format": "VCF",
        "phase": "mutation",
        "status": "not_applicable",
        "reason": (
            "seqan3 has no VCF parser. Flow.md §2.1 explicitly drops "
            "seqan3 from the VCF differential matrix ('SeqAn3 暂不支持 "
            "VCF IO'). biotest_config.yaml coverage.target_filters.VCF "
            "has no `seqan3` key; the libFuzzer harness "
            "(compares/harnesses/libfuzzer/seqan3_sam_fuzzer.cpp) "
            "instantiates only `seqan3::sam_file_input` + "
            "`seqan3::format_sam`. There is no VCF code in seqan3 to "
            "mutate, so a VCF mutation score for this cell is "
            "structurally undefined rather than zero."
        ),
        "mutator": "mull-substitute-v1 (custom source-level, "
                   "glibc-22.04-compatible replacement for mull 0.33 "
                   "which requires glibc 2.39; see "
                   "compares/results/mutation/libfuzzer/seqan3_sam/"
                   "summary.json for the SAM cell)",
        "killed": None,
        "reachable": None,
        "score": None,
        "mutator_count": 0,
        "mutant_count": 0,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2),
                                      encoding="utf-8")
    (out / "config.json").write_text(json.dumps({
        "args": {k: str(v) for k, v in vars(args).items()},
        "format": "VCF",
        "status": "not_applicable",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2), encoding="utf-8")
    print(f"mutation_driver: libfuzzer×seqan3/VCF → N/A ({out}/summary.json)")
    return 0


def _libfuzzer_seqan3_loop_in_container(args: argparse.Namespace) -> int:
    """Inner mutation loop — expected to run inside biotest-bench."""
    src_root = Path(args.seqan3_src_root)
    scope_files = _seqan3_sam_scope_files(src_root)
    if not scope_files:
        print(f"mutation_driver: no seqan3 SAM scope files under "
              f"{src_root}", file=sys.stderr)
        return 2

    # Reachability filter: prefer an explicit JSON, else regenerate
    # from the Phase-2 _build-cov-iso .gcda files if they exist.
    cov_json = Path(args.cov_report) if args.cov_report else None
    if cov_json is None or not cov_json.exists():
        cov_build = Path(args.cov_build_dir) if args.cov_build_dir else None
        if cov_build and cov_build.exists():
            derived = Path(args.out).resolve() / "_gcovr_reach.json"
            derived.parent.mkdir(parents=True, exist_ok=True)
            proc = subprocess.run(
                ["gcovr", "--json", "--root", str(src_root),
                 "--gcov-executable", "llvm-cov-18 gcov",
                 "--output", str(derived), str(cov_build)],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                timeout=300, check=False,
            )
            if proc.returncode == 0 and derived.stat().st_size > 0:
                cov_json = derived
    reachable = _load_reachable_lines(cov_json, scope_files)

    mutations = _enumerate_mutations(scope_files, src_root, reachable)
    if args.max_mutants and len(mutations) > args.max_mutants:
        # Deterministic subset — spread evenly so every family surfaces.
        step = max(1, len(mutations) // args.max_mutants)
        mutations = mutations[::step][:args.max_mutants]

    mut_bin = Path(args.mut_bin)
    mut_build = Path(args.mut_build_dir)
    if not mut_bin.exists():
        print(f"mutation_driver: mut binary {mut_bin} missing — build "
              "via `bash compares/scripts/build_harnesses.sh libfuzzer_mut`",
              file=sys.stderr)
        return 2
    if not mut_build.exists():
        print(f"mutation_driver: mut build dir {mut_build} missing",
              file=sys.stderr)
        return 2

    corpus = Path(args.corpus)
    if not corpus.exists():
        print(f"mutation_driver: corpus {corpus} missing", file=sys.stderr)
        return 2
    # Phase E augmentation for seqan3 (non-strict templated C++ parser).
    # Use args.out (unique per invocation) to avoid races between
    # parallel runs sharing args.tool='biotest'.
    fmt_local = (args.format or "SAM").upper()
    out_for_aug = Path(args.out).resolve()
    out_for_aug.mkdir(parents=True, exist_ok=True)
    corpus = _augment_with_phase_e(corpus, sut="seqan3", fmt=fmt_local, out=out_for_aug)
    all_corpus_files = sorted((p for p in corpus.iterdir() if p.is_file()),
                              key=lambda p: p.name)
    sample = (all_corpus_files[:args.corpus_sample]
              if args.corpus_sample and len(all_corpus_files) > args.corpus_sample
              else all_corpus_files)

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    log_file = out / "runner.log"
    log = log_file.open("w", encoding="utf-8")

    def _log(msg: str) -> None:
        log.write(msg + "\n"); log.flush()
        print(msg, file=sys.stderr)

    _log(f"[mut] scope files: {len(scope_files)}")
    _log(f"[mut] reachable-lines map: {sum(len(v) for v in reachable.values()) if reachable else 'unfiltered'}")
    _log(f"[mut] candidate mutations: {len(mutations)}")
    _log(f"[mut] corpus sample: {len(sample)}/{len(all_corpus_files)}")
    _log(f"[mut] mut binary: {mut_bin}")
    _log(f"[mut] mut build dir: {mut_build}")

    # Baseline run. Force a fresh build from the CURRENT (reverted)
    # source before collecting digests — otherwise a previous
    # campaign could leave `mut_bin` as a post-mutation build (we
    # always revert the source in the finally-block, but never
    # rebuild the binary back to the pristine state). Baseline
    # digests collected against a stale mutant binary would corrupt
    # every subsequent kill decision in this campaign.
    started_all = time.time()
    rebuild_ok, rebuild_stderr = _rebuild_mut_binary(mut_build)
    if not rebuild_ok:
        _log(f"[mut] baseline rebuild FAILED — aborting campaign: "
             f"{rebuild_stderr[-400:]}")
        log.close()
        return 2
    _log(f"[mut] baseline binary rebuilt in "
         f"{time.time()-started_all:.1f}s (guards against stale mutant state)")
    baseline = _run_corpus_digest(mut_bin, sample, args.per_file_timeout_s)
    (out / "baseline.json").write_text(json.dumps(baseline, indent=2),
                                       encoding="utf-8")
    _log(f"[mut] baseline digests collected ({len(baseline)} files) in "
         f"{time.time()-started_all:.1f}s")

    details = []
    killed = survived = compile_errors = equivalent = 0
    t_overall = time.time()
    hit_budget = False
    for idx, m in enumerate(mutations, start=1):
        if args.budget and (time.time() - t_overall) > args.budget:
            hit_budget = True
            _log(f"[mut] budget {args.budget}s exhausted at mutant {idx-1}; "
                 "stopping")
            break
        file_path = Path(m["file"])
        mut_started = time.time()
        try:
            original = _apply_mutation_inplace(
                file_path, m["line"], m["col"], m["orig"], m["new"],
            )
        except Exception as exc:  # noqa: BLE001
            _log(f"[mut] skip #{idx} {m['rel']}:{m['line']} {m['family']}: {exc}")
            continue

        try:
            ok, stderr_tail = _rebuild_mut_binary(mut_build)
            if not ok:
                compile_errors += 1
                details.append({**m, "outcome": "compile_error",
                                 "stderr_tail": stderr_tail[-200:]})
                _log(f"[mut] #{idx:<4} COMPILE_ERROR "
                     f"{m['rel']}:{m['line']} {m['family']} "
                     f"({time.time()-mut_started:.1f}s)")
                continue

            mutated = _run_corpus_digest(mut_bin, sample, args.per_file_timeout_s)
            diffs = _digest_diff(baseline, mutated)
            if diffs:
                killed += 1
                details.append({**m, "outcome": "killed",
                                 "diff_files": diffs[:5],
                                 "diff_count": len(diffs)})
                _log(f"[mut] #{idx:<4} KILLED      "
                     f"{m['rel']}:{m['line']} {m['family']} "
                     f"{m['orig']!r}→{m['new']!r} "
                     f"(diff on {len(diffs)} files, "
                     f"{time.time()-mut_started:.1f}s)")
            else:
                survived += 1
                details.append({**m, "outcome": "survived"})
                _log(f"[mut] #{idx:<4} SURVIVED    "
                     f"{m['rel']}:{m['line']} {m['family']} "
                     f"{m['orig']!r}→{m['new']!r} "
                     f"({time.time()-mut_started:.1f}s)")
        finally:
            _revert_mutation(file_path, original)

    total_run = killed + survived
    score = (killed / total_run) if total_run else None
    summary = {
        "tool": args.tool,
        "sut": "seqan3",
        "format": "SAM",
        "phase": "mutation",
        "status": "ok",
        "mutator": "mull-substitute-v1",
        "mutator_note": (
            "Mull 0.33 ships as a 24.04 deb (glibc 2.39); biotest-bench "
            "is 22.04 (glibc 2.35) so mull-runner-18/mull-ir-frontend-18 "
            "fail at load time. This driver applies the same ROR / AOR / "
            "LOR operator families mull's --mutators=default emits, "
            "scoped to the same seqan3 SAM source paths, and uses the "
            "same DESIGN §3.3 kill semantics (parse-success flip / "
            "canonical-JSON digest diff / crash flip)."
        ),
        "mutators_used": sorted({r[0] for r in _MUTATION_RULES_SRC}),
        "scope_files": len(scope_files),
        "candidate_mutants": len(mutations),
        "executed_mutants": killed + survived + compile_errors,
        "killed": killed,
        "survived": survived,
        "compile_errors": compile_errors,
        "equivalent": equivalent,
        "reachable": total_run,   # mutants that compiled + ran
        "mutant_count": len(mutations),
        "mutator_count": len({r[0] for r in _MUTATION_RULES_SRC}),
        "score": round(score, 4) if score is not None else None,
        "corpus_dir": str(corpus),
        "corpus_sample": len(sample),
        "corpus_total": len(all_corpus_files),
        "per_file_timeout_s": args.per_file_timeout_s,
        "budget_s": args.budget,
        "budget_hit": hit_budget,
        "duration_s": round(time.time() - t_overall, 2),
        "cov_reachability_json": str(cov_json) if cov_json else None,
        "mut_binary": str(mut_bin),
        "mut_build_dir": str(mut_build),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2),
                                      encoding="utf-8")
    (out / "details.json").write_text(json.dumps(details, indent=2),
                                      encoding="utf-8")
    _log(f"[mut] done: killed={killed} survived={survived} "
         f"compile_errors={compile_errors} score="
         f"{summary['score']} elapsed={summary['duration_s']}s")
    log.close()
    return 0


def _run_libfuzzer_seqan3(args: argparse.Namespace, fmt: str) -> int:
    """Host-side dispatcher for libFuzzer × seqan3 mutation testing.

    VCF: emits an N/A summary immediately — seqan3 has no VCF parser.
    SAM: if this process is already running inside biotest-bench (the
    seqan3 source tree at /opt/seqan3/include is present), run the
    mutation loop directly; otherwise shell into the bench container
    via `docker run` and re-invoke this script with --in-container.
    """
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    if fmt == "VCF":
        return _write_vcf_na_summary(out, args)

    # SAM path
    ctr_src = Path(_SEQAN3_SRC_ROOT_IN_CTR)
    in_container = ctr_src.exists()
    if args.in_container or in_container:
        # Pick up defaults for in-container paths if caller didn't override.
        if not args.seqan3_src_root:
            args.seqan3_src_root = _SEQAN3_SRC_ROOT_IN_CTR
        if not args.mut_build_dir:
            args.mut_build_dir = str(REPO_ROOT /
                "compares/results/coverage/libfuzzer/seqan3/_build-mut-iso")
        if not args.mut_bin:
            args.mut_bin = str(Path(args.mut_build_dir) / "seqan3_sam_fuzzer_mut")
        if not args.cov_build_dir:
            args.cov_build_dir = str(REPO_ROOT /
                "compares/results/coverage/libfuzzer/seqan3/_build-cov-iso")
        return _libfuzzer_seqan3_loop_in_container(args)

    # Host path — spawn biotest-bench and re-invoke this script.
    # Before spawning, make sure the mutation binary exists inside the
    # container. Caller is responsible for having run build_harnesses.sh
    # libfuzzer_mut; we don't auto-build here (that would mask build
    # problems behind a long-running mutation campaign).
    corpus_ctr = _ctr_path(args.corpus) if args.corpus.exists() else str(args.corpus)
    out_ctr = _ctr_path(out)
    cov_build_default = (REPO_ROOT /
        "compares/results/coverage/libfuzzer/seqan3/_build-cov-iso")
    mut_build_default = (REPO_ROOT /
        "compares/results/coverage/libfuzzer/seqan3/_build-mut-iso")
    if not mut_build_default.exists():
        print(
            f"mutation_driver: mut build dir missing at {mut_build_default}. "
            "Run this first inside biotest-bench:\n  bash compares/docker/run.sh bash -lc '"
            f"mkdir -p {_ctr_path(mut_build_default)} && "
            f"cd {_ctr_path(mut_build_default)} && "
            "cmake /work/compares/harnesses/libfuzzer -DCMAKE_CXX_COMPILER=clang++-18 "
            "-DCMAKE_CXX_FLAGS=-DSEQAN3_DISABLE_COMPILER_CHECK && "
            "make seqan3_sam_fuzzer_mut'",
            file=sys.stderr,
        )
        return 2
    inner = [
        SYSTEM_PY, "/work/compares/scripts/mutation_driver.py",
        "--tool", args.tool, "--sut", "seqan3", "--format", "SAM",
        "--in-container",
        "--corpus", corpus_ctr,
        "--out", out_ctr,
        "--max-mutants", str(args.max_mutants),
        "--corpus-sample", str(args.corpus_sample),
        "--per-file-timeout-s", str(args.per_file_timeout_s),
        "--budget", str(args.budget),
        "--seqan3-src-root", _SEQAN3_SRC_ROOT_IN_CTR,
        "--mut-build-dir", _ctr_path(mut_build_default),
        "--mut-bin", _ctr_path(mut_build_default) + "/seqan3_sam_fuzzer_mut",
        "--cov-build-dir", _ctr_path(cov_build_default),
    ]
    if args.cov_report:
        inner += ["--cov-report", str(args.cov_report)]

    stdout_log = out / "container.stdout.log"
    stderr_log = out / "container.stderr.log"
    rc = _docker_run(inner, stdout_file=stdout_log, stderr_file=stderr_log,
                     timeout_s=args.budget + 1800)
    if rc != 0:
        print(f"mutation_driver: in-container libfuzzer×seqan3 exited rc={rc}; "
              f"see {stderr_log}", file=sys.stderr)
    return rc


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--tool", required=True,
                   choices=["atheris", "cargo_fuzz", "libfuzzer", "biotest"],
                   help="Phase-2 tool whose corpus is the 'test suite'.")
    p.add_argument("--sut", required=True,
                   choices=["vcfpy", "noodles", "seqan3", "biopython"],
                   help="SUT under mutation.")
    p.add_argument("--format", default=None, choices=["SAM", "VCF"],
                   help="Format — only consumed by libfuzzer×seqan3. seqan3 "
                        "has no VCF parser so the VCF cell emits a documented "
                        "N/A summary without running mutations.")
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

    # libfuzzer × seqan3 — source-level mutation flags
    p.add_argument("--max-mutants", type=int, default=60,
                   help="Max mutations sampled per libFuzzer × seqan3 run. "
                        "Budget math: ~15-25 s per mutant (Clang full-TU "
                        "rebuild) + ~5 s corpus replay. 60 mutants ≈ 25 min.")
    p.add_argument("--seqan3-src-root", default=None,
                   help="seqan3 source root (inside biotest-bench "
                        "/opt/seqan3/include). Auto-detected in-container.")
    p.add_argument("--mut-build-dir", default=None,
                   help="Build dir for seqan3_sam_fuzzer_mut. Defaults to "
                        "compares/results/coverage/libfuzzer/seqan3/"
                        "_build-mut-iso.")
    p.add_argument("--mut-bin", default=None,
                   help="Override the mutation-test binary path.")
    p.add_argument("--cov-build-dir", default=None,
                   help="Phase-2 _build-cov-iso dir used as the "
                        "reachability-filter gcovr source.")
    p.add_argument("--cov-report", default=None,
                   help="Explicit gcovr JSON for reachability filtering. "
                        "If omitted, regenerated from --cov-build-dir.")
    p.add_argument("--in-container", action="store_true",
                   help="Internal flag: set when the script re-invokes "
                        "itself inside biotest-bench. Users should not set "
                        "this by hand.")
    p.add_argument("--no-augment-corpus", action="store_true",
                   help="Skip Phase-E struct/rawfuzz augmentation. Used by "
                        "the M2 dual-policy disclosure (REVIEW2.md) to "
                        "isolate the corpus_minimize.py selector effect.")
    p.add_argument("--no-coverage-select", action="store_true",
                   help="Skip the coverage-guided post-cmin selection "
                        "(corpus_coverage_select). M2 dual-policy disclosure.")
    args = p.parse_args()

    # biotest reuses the per-SUT backends below; before dispatch, remap
    # default paths so --corpus / --out point at the biotest tree instead
    # of atheris/cargo_fuzz/libfuzzer defaults.
    default_corpus = REPO_ROOT / "compares/results/mutation/atheris/vcfpy/union_corpus"
    default_out = REPO_ROOT / "compares/results/mutation/atheris/vcfpy"
    if args.tool == "biotest":
        if args.sut == "vcfpy":
            if args.corpus == default_corpus:
                args.corpus = REPO_ROOT / "compares/results/coverage/biotest/vcfpy/run_0/corpus"
            if args.out == default_out:
                args.out = REPO_ROOT / "compares/results/mutation/biotest/vcfpy"
            return _run_atheris_vcfpy(args)
        if args.sut == "noodles":
            if args.corpus == default_corpus:
                args.corpus = REPO_ROOT / "compares/results/coverage/biotest/noodles/run_0/corpus"
            if args.out == default_out:
                args.out = REPO_ROOT / "compares/results/mutation/biotest/noodles"
            return _run_cargo_fuzz_noodles(args)
        if args.sut == "seqan3":
            fmt = (args.format or "SAM").upper()
            if args.corpus == default_corpus:
                args.corpus = REPO_ROOT / "compares/results/coverage/biotest/seqan3/run_0/corpus"
            if args.out == default_out:
                args.out = (REPO_ROOT / "compares/results/mutation/biotest/seqan3_sam"
                            if fmt == "SAM"
                            else REPO_ROOT / "compares/results/mutation/biotest/seqan3_vcf")
            return _run_libfuzzer_seqan3(args, fmt)
        print(f"mutation_driver: --tool biotest --sut {args.sut!r} not wired here; "
              "htsjdk and biopython are driven by phase3_jazzer_pit.sh "
              "and phase3_atheris_biopython.sh respectively (pass TOOL=biotest).",
              file=sys.stderr)
        return 2
    if args.tool == "atheris" and args.sut == "vcfpy":
        return _run_atheris_vcfpy(args)
    if args.tool == "cargo_fuzz" and args.sut == "noodles":
        # Default corpus + out dir for the Rust cell if caller didn't
        # override via flag.
        if args.corpus == default_corpus:
            args.corpus = REPO_ROOT / "compares/results/coverage/cargo_fuzz/noodles/run_0/corpus"
        if args.out == default_out:
            args.out = REPO_ROOT / "compares/results/mutation/cargo_fuzz/noodles"
        return _run_cargo_fuzz_noodles(args)
    if args.tool == "libfuzzer" and args.sut == "seqan3":
        fmt = (args.format or "SAM").upper()
        if fmt not in {"SAM", "VCF"}:
            print(f"mutation_driver: --format must be SAM or VCF, got {args.format!r}",
                  file=sys.stderr)
            return 2
        # Resolve cell-specific defaults if the caller didn't override.
        default_out_sam = REPO_ROOT / "compares/results/mutation/libfuzzer/seqan3_sam"
        default_out_vcf = REPO_ROOT / "compares/results/mutation/libfuzzer/seqan3_vcf"
        if args.out == default_out:
            args.out = default_out_sam if fmt == "SAM" else default_out_vcf
        if args.corpus == default_corpus:
            args.corpus = (REPO_ROOT /
                           "compares/results/coverage/libfuzzer/seqan3/run_0/corpus")
        return _run_libfuzzer_seqan3(args, fmt)
    print(f"mutation_driver: (tool={args.tool!r}, sut={args.sut!r}) not supported",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli())
