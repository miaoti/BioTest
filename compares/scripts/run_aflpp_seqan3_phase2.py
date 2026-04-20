"""Phase-2 coverage-growth run for the AFL++ × seqan3 cell (DESIGN §13.5).

Self-contained orchestrator so the bench can produce the canonical
`growth_<rep>.json` output for the DESIGN §4.5 schema without touching
the contested shared `coverage_sampler.py`. Designed to be run INSIDE
the `biotest-bench:latest` container where `afl-fuzz`, `gcov-12`, and
`gcovr` are on PATH.

Usage (from inside the container via bash compares/docker/run.sh):

    python3.12 compares/scripts/run_aflpp_seqan3_phase2.py \\
        --seed-corpus compares/results/bench_seeds/sam \\
        --budget 300 --reps 3 \\
        --out compares/results/coverage/aflpp/seqan3/

Coverage pipeline:
  1. afl-fuzz drives `build-aflpp/seqan3_sam_fuzzer_aflpp` for --budget
     seconds with `-V` (self-terminates at budget).
  2. At each log tick in {1,10,60,300,1800,7200} ≤ budget the live
     `afl-state/default/queue/` is snapshotted (cheap copy; race-safe
     since AFL++ queue files are effectively write-once).
  3. After afl-fuzz exits, each snapshot is replayed through
     `build-cov/seqan3_sam_fuzzer_cov` (built with
     `g++-12 --coverage`). `.gcda` files accumulate, are captured per
     tick, and fed to `gcovr --gcov-executable=gcov-12 --json`.
  4. The gcovr JSON is filtered to the three
     `biotest_config.yaml:coverage.target_filters.SAM.seqan3`
     substrings (`seqan3/io/sam_file`, `format_sam`, `cigar`), then
     aggregated into {line_pct, branch_pct} per tick.

Output contract (one file per rep):
  <out>/growth_<rep_idx>.json — DESIGN §4.5 schema
  <out>/summary.json          — per-tick mean + 95% CI style min/max
  <out>/summary.csv           — flat CSV for Phase-6 build_report.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_TICKS: tuple[int, ...] = (1, 10, 60, 300, 1800, 7200)

AFLPP_BIN = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
             / "build-aflpp" / "seqan3_sam_fuzzer_aflpp")
COV_BUILD_DIR = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
                 / "build-cov")
COV_BIN = COV_BUILD_DIR / "seqan3_sam_fuzzer_cov"
GCOV_EXE = "gcov-12"

# Matches biotest_config.yaml:coverage.target_filters.SAM.seqan3.
SCOPE = ("seqan3/io/sam_file", "format_sam", "cigar")


def _sha256_dir(path: Path) -> str:
    h = hashlib.sha256()
    if not path.exists():
        return "sha256:empty"
    for p in sorted(path.rglob("*")):
        if p.is_file():
            h.update(p.name.encode()); h.update(b"\0")
            h.update(p.read_bytes()); h.update(b"\0")
    return "sha256:" + h.hexdigest()


def _ticks_in_budget(budget_s: int) -> list[int]:
    ts = [t for t in DEFAULT_TICKS if t <= budget_s]
    if not ts or ts[-1] != budget_s:
        ts.append(budget_s)
    return sorted(set(ts))


def _seed_copy(src: Path, dst: Path) -> int:
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in src.iterdir() if src.exists() else []:
        if p.is_file():
            shutil.copy2(p, dst / p.name); n += 1
    return n


def _prune_gcda(build: Path) -> None:
    for g in build.glob("*.gcda"):
        try: g.unlink()
        except FileNotFoundError: pass


def _snapshot_queue(src: Path, dst: Path) -> int:
    dst.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        return 0
    n = 0
    for p in sorted(src.iterdir()):
        if p.is_file() and p.name != ".state":
            try:
                shutil.copy2(p, dst / p.name); n += 1
            except (FileNotFoundError, PermissionError):
                continue
    return n


def _replay(cov_bin: Path, snap: Path, log: Path, timeout_s: int = 10) -> dict:
    stats = {"total": 0, "accepted": 0, "rejected": 0, "timeout": 0}
    if not snap.exists():
        return stats
    with log.open("ab") as lf:
        lf.write(f"\n=== replay {snap} ===\n".encode())
        for f in sorted(snap.iterdir()):
            if not f.is_file():
                continue
            stats["total"] += 1
            try:
                with f.open("rb") as src:
                    r = subprocess.run(
                        [str(cov_bin)], stdin=src, stdout=lf, stderr=lf,
                        timeout=timeout_s, check=False, cwd=str(cov_bin.parent),
                    )
                if r.returncode == 0:
                    stats["accepted"] += 1
                else:
                    stats["rejected"] += 1
            except subprocess.TimeoutExpired:
                stats["timeout"] += 1
            except OSError:
                stats["rejected"] += 1
    return stats


GCOVR_ROOT = "/opt/seqan3/include"


def _run_gcovr(build: Path, out_json: Path) -> bool:
    """gcovr 5.0 excludes files not under `--root`; the seqan3 sources
    all live under /opt/seqan3/include so we root gcovr there (this
    also trims /usr/include/c++ and AFL++ harness chaff automatically).
    We deliberately do NOT pass `-f` filters here: gcovr 5.0's filter
    regex is anchored differently across patch versions, and our Python
    aggregator already scopes by the three substrings listed in SCOPE.
    Filtering once, in one place, keeps behaviour deterministic."""
    out_json.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["gcovr", f"--gcov-executable={GCOV_EXE}", "-r", GCOVR_ROOT,
           "--json", str(out_json), str(build)]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=300, check=False)
    except subprocess.TimeoutExpired:
        return False
    if r.returncode != 0:
        sys.stderr.write(
            f"[gcovr] rc={r.returncode} {r.stderr.decode(errors='replace')[:300]}\n")
    return out_json.exists() and out_json.stat().st_size > 0


def _aggregate(gcovr_json: Path) -> dict[str, int]:
    if not gcovr_json.exists():
        return {"line_covered": 0, "line_total": 0,
                "branch_covered": 0, "branch_total": 0, "files": 0}
    try:
        data = json.loads(gcovr_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"line_covered": 0, "line_total": 0,
                "branch_covered": 0, "branch_total": 0, "files": 0}
    lc = lt = bc = bt = files = 0
    for f in data.get("files", []):
        name = (f.get("file") or f.get("filename") or "").replace("\\", "/")
        if not any(s in name for s in SCOPE):
            continue
        files += 1
        for ln in f.get("lines", []):
            if ln.get("gcovr/noncode"):
                continue
            lt += 1
            if int(ln.get("count", 0) or 0) > 0:
                lc += 1
            for br in ln.get("branches", []) or []:
                bt += 1
                if int(br.get("count", 0) or 0) > 0:
                    bc += 1
    return {"line_covered": lc, "line_total": lt,
            "branch_covered": bc, "branch_total": bt, "files": files}


def _one_rep(
    rep_idx: int, seed_corpus: Path, out_dir: Path, budget_s: int,
    ticks: list[int], seed_hash: str,
) -> dict[str, Any]:
    rep_dir = out_dir / f"run_{rep_idx}"
    corpus_dir = rep_dir / "corpus"
    crashes_dir = rep_dir / "crashes"
    afl_input = rep_dir / "afl-input"
    afl_out = rep_dir / "afl-state"
    snapshots = rep_dir / "snapshots"
    gcda_snapshots = rep_dir / "gcda_snapshots"
    gcovr_snapshots = rep_dir / "gcovr_snapshots"
    for d in (corpus_dir, crashes_dir, afl_input, afl_out, snapshots,
              gcda_snapshots, gcovr_snapshots):
        d.mkdir(parents=True, exist_ok=True)
    log_file = rep_dir / "tool.log"; log_file.touch(exist_ok=True)
    replay_log = rep_dir / "replay.log"; replay_log.touch(exist_ok=True)

    seeded = _seed_copy(seed_corpus, afl_input)
    if seeded == 0:
        (afl_input / "stub").write_bytes(b"\n")

    queue_live = afl_out / "default" / "queue"
    crashes_src = afl_out / "default" / "crashes"

    _prune_gcda(COV_BUILD_DIR)

    env = os.environ.copy()
    env.setdefault("AFL_SKIP_CPUFREQ", "1")
    env.setdefault("AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES", "1")
    env.setdefault("AFL_BENCH_UNTIL_CRASH", "0")
    env.setdefault("AFL_NO_UI", "1")

    cmd = ["afl-fuzz", "-i", str(afl_input), "-o", str(afl_out),
           "-V", str(budget_s), "--", str(AFLPP_BIN)]

    print(f"[rep {rep_idx}] starting afl-fuzz budget={budget_s}s ticks={ticks}")
    t0 = time.time()
    logfh = log_file.open("ab")
    proc = subprocess.Popen(
        cmd, stdout=logfh, stderr=subprocess.STDOUT, env=env,
        preexec_fn=os.setsid if os.name != "nt" else None,
    )

    snap_dirs: dict[int, Path] = {}
    try:
        for t in ticks:
            target = t0 + t
            while time.time() < target:
                if proc.poll() is not None:
                    break
                time.sleep(min(0.5, max(0.05, target - time.time())))
            snap = snapshots / f"t_{t}s"
            n = _snapshot_queue(queue_live, snap)
            snap_dirs[t] = snap
            print(f"[rep {rep_idx}] tick t={t}s snapshot={n} queue-files")
            if proc.poll() is not None:
                for rem in (tt for tt in ticks if tt > t):
                    snap_dirs[rem] = snap
                break
    finally:
        try:
            proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            try:
                if os.name == "nt":
                    proc.terminate()
                else:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                proc.wait(timeout=15)
            except Exception:
                try:
                    if os.name == "nt":
                        proc.kill()
                    else:
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try: proc.wait(timeout=5)
                except subprocess.TimeoutExpired: pass
        finally:
            try: logfh.close()
            except Exception: pass

    # Normalize AFL++ output layout.
    if crashes_src.exists():
        for p in crashes_src.iterdir():
            if p.is_file() and p.name != "README.txt":
                try: shutil.copy2(p, crashes_dir / p.name)
                except OSError: continue
    if queue_live.exists():
        for p in queue_live.iterdir():
            if p.is_file() and p.name != ".state":
                try: shutil.copy2(p, corpus_dir / p.name)
                except OSError: continue

    growth: list[dict[str, Any]] = []
    for t in sorted(snap_dirs):
        _prune_gcda(COV_BUILD_DIR)
        replay_stats = _replay(COV_BIN, snap_dirs[t], replay_log)
        tick_gcda = gcda_snapshots / f"t_{t}s"
        tick_gcda.mkdir(parents=True, exist_ok=True)
        for g in COV_BUILD_DIR.glob("*.gcda"):
            shutil.copy2(g, tick_gcda / g.name)
        gcovr_json = gcovr_snapshots / f"t_{t}s.json"
        _run_gcovr(COV_BUILD_DIR, gcovr_json)
        agg = _aggregate(gcovr_json)
        line_pct = (100.0 * agg["line_covered"] / agg["line_total"]
                    if agg["line_total"] else 0.0)
        branch_pct = (100.0 * agg["branch_covered"] / agg["branch_total"]
                      if agg["branch_total"] else 0.0)
        print(f"[rep {rep_idx}] t={t}s line={line_pct:.2f}% "
              f"branch={branch_pct:.2f}% replayed={replay_stats['total']} "
              f"files_in_scope={agg['files']}")
        growth.append({
            "t_s": t,
            "line_pct": round(line_pct, 3),
            "branch_pct": round(branch_pct, 3),
            "line_covered": agg["line_covered"],
            "line_total": agg["line_total"],
            "branch_covered": agg["branch_covered"],
            "branch_total": agg["branch_total"],
            "files_in_scope": agg["files"],
            "queue_files": sum(1 for _ in snap_dirs[t].iterdir())
                           if snap_dirs[t].exists() else 0,
            "replayed": replay_stats["total"],
            "accepted": replay_stats["accepted"],
            "rejected": replay_stats["rejected"],
            "timeout": replay_stats["timeout"],
        })

    queue_final = (sum(1 for p in queue_live.iterdir() if p.is_file())
                   if queue_live.exists() else 0)
    crash_final = (sum(1 for p in crashes_src.iterdir()
                       if p.is_file() and p.name != "README.txt")
                   if crashes_src.exists() else 0)

    record = {
        "tool": "aflpp",
        "sut": "seqan3",
        "format": "SAM",
        "phase": "coverage",
        "run_index": rep_idx,
        "time_budget_s": budget_s,
        "seed_corpus_hash": seed_hash,
        "coverage_growth": [
            {"t_s": g["t_s"],
             "line_pct": g["line_pct"],
             "branch_pct": g["branch_pct"]}
            for g in growth
        ],
        "mutation_score": None,
        "bug_bench": None,
        "extra": {
            "started_at": t0,
            "ended_at": time.time(),
            "duration_s": round(time.time() - t0, 2),
            "ticks_requested": ticks,
            "ticks_sampled": sorted(snap_dirs),
            "coverage_scope": list(SCOPE),
            "aflpp_binary": str(AFLPP_BIN),
            "cov_replay_binary": str(COV_BIN),
            "gcov_executable": GCOV_EXE,
            "queue_size_final": queue_final,
            "crash_count_final": crash_final,
            "per_tick_detail": growth,
            "seed_corpus_dir": str(seed_corpus.resolve()),
            "out_dir": str(rep_dir.resolve()),
        },
    }
    (out_dir / f"growth_{rep_idx}.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8")

    # Adapter-style manifest (matches Phase-1's adapter_result.json shape).
    (rep_dir / "adapter_result.json").write_text(json.dumps({
        "tool": "aflpp",
        "sut": "seqan3",
        "time_budget_s": budget_s,
        "started_at": t0,
        "ended_at": time.time(),
        "corpus_dir": str(corpus_dir),
        "crashes_dir": str(crashes_dir),
        "log_file": str(log_file),
        "generated_count": queue_final,
        "crash_count": crash_final,
        "exit_code": proc.returncode if proc.returncode is not None else -1,
        "extra": {
            "aflpp_binary": str(AFLPP_BIN),
            "cov_replay_binary": str(COV_BIN),
            "gcov_executable": GCOV_EXE,
            "coverage_scope": list(SCOPE),
            "ticks_requested": ticks,
            "ticks_sampled": sorted(snap_dirs),
            "afl_state_dir": str(afl_out),
        },
    }, indent=2), encoding="utf-8")

    return record


def _write_summary(out_dir: Path, records: list[dict[str, Any]], budget_s: int,
                   ticks: list[int]) -> Path:
    # per-tick: mean + min + max across reps (DESIGN §3.2 "95% CI band"
    # approximation — with reps=3 min/max already gives the outer
    # envelope, which is the band the Phase-6 plot wants).
    tick_to_lines: dict[int, list[float]] = {}
    tick_to_branches: dict[int, list[float]] = {}
    for r in records:
        for g in r["coverage_growth"]:
            tick_to_lines.setdefault(g["t_s"], []).append(g["line_pct"])
            tick_to_branches.setdefault(g["t_s"], []).append(g["branch_pct"])

    agg = []
    for t in sorted(tick_to_lines):
        lp = tick_to_lines[t]; bp = tick_to_branches[t]
        agg.append({
            "t_s": t,
            "reps": len(lp),
            "line_pct_mean": round(sum(lp) / len(lp), 3),
            "line_pct_min": round(min(lp), 3),
            "line_pct_max": round(max(lp), 3),
            "branch_pct_mean": round(sum(bp) / len(bp), 3),
            "branch_pct_min": round(min(bp), 3),
            "branch_pct_max": round(max(bp), 3),
        })

    summary = {
        "tool": "aflpp",
        "sut": "seqan3",
        "format": "SAM",
        "phase": "coverage",
        "reps": len(records),
        "time_budget_s": budget_s,
        "ticks_requested": ticks,
        "coverage_scope": list(SCOPE),
        "coverage_growth_aggregate": agg,
        "rep_files": [f"growth_{i}.json" for i in range(len(records))],
        "produced_at": time.time(),
    }
    out_json = out_dir / "summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Flat CSV for Phase-6 scaffolding.
    csv_path = out_dir / "summary.csv"
    header = ("tool,sut,format,rep,t_s,line_pct,branch_pct,"
              "line_covered,line_total,branch_covered,branch_total,"
              "files_in_scope,queue_files,replayed,accepted,rejected,timeout\n")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write(header)
        for r in records:
            idx = r["run_index"]
            for g in r["extra"]["per_tick_detail"]:
                f.write(
                    f"aflpp,seqan3,SAM,{idx},{g['t_s']},"
                    f"{g['line_pct']},{g['branch_pct']},"
                    f"{g['line_covered']},{g['line_total']},"
                    f"{g['branch_covered']},{g['branch_total']},"
                    f"{g['files_in_scope']},{g['queue_files']},"
                    f"{g['replayed']},{g['accepted']},"
                    f"{g['rejected']},{g['timeout']}\n"
                )
    return out_json


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--budget", type=int, default=7200)
    p.add_argument("--reps", type=int, default=3)
    args = p.parse_args(argv)

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    if not AFLPP_BIN.exists():
        sys.stderr.write(
            f"[fatal] AFL++ binary missing: {AFLPP_BIN}. Build: "
            f"bash compares/scripts/build_harnesses.sh aflpp\n")
        return 2
    if not COV_BIN.exists():
        sys.stderr.write(
            f"[fatal] Coverage binary missing: {COV_BIN}. Build via: "
            f"cd compares/harnesses/libfuzzer && mkdir -p build-cov && "
            f"cd build-cov && g++-12 -std=c++23 -O0 -g --coverage "
            f"-I/opt/seqan3/include -I/opt/sdsl-lite/include "
            f"../seqan3_sam_fuzzer.cpp -o seqan3_sam_fuzzer_cov\n")
        return 2
    if shutil.which("afl-fuzz") is None:
        sys.stderr.write("[fatal] afl-fuzz not on PATH — run inside biotest-bench\n")
        return 2
    if shutil.which("gcovr") is None:
        sys.stderr.write("[fatal] gcovr not on PATH\n")
        return 2
    if shutil.which(GCOV_EXE) is None:
        sys.stderr.write(f"[fatal] {GCOV_EXE} not on PATH\n")
        return 2

    ticks = _ticks_in_budget(args.budget)
    seed_hash = _sha256_dir(args.seed_corpus)
    print(f"[setup] budget={args.budget}s reps={args.reps} ticks={ticks}")
    print(f"[setup] seed_corpus={args.seed_corpus} seed_hash={seed_hash[:20]}…")

    records: list[dict[str, Any]] = []
    for i in range(args.reps):
        rec = _one_rep(i, args.seed_corpus.resolve(), out_dir,
                       args.budget, ticks, seed_hash)
        records.append(rec)
        final = rec["coverage_growth"][-1] if rec["coverage_growth"] else {}
        print(f"[rep {i}] done: final line={final.get('line_pct', 0)}% "
              f"branch={final.get('branch_pct', 0)}%")

    summary_path = _write_summary(out_dir, records, args.budget, ticks)
    print(f"[summary] {summary_path}")
    print(f"[growth]  wrote {args.reps} growth_*.json under {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
