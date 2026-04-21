"""Phase-3 mutation-score run for the AFL++ × seqan3 cell (DESIGN §13.5).

Self-contained source-level mutation driver — stands in for mull on
biotest-bench images where mull-0.33's binary is broken by a glibc
mismatch (mull was built against glibc 2.39; bench image is glibc
2.35). Produces the DESIGN §3.3 `summary.json` contract
(`{killed, reachable, score}`) using the standard mutation-testing
protocol:

  1. pick mutation sites from lines already executed by the tool's
     Phase-2 accepted-input corpus (DESIGN §3.3 "reachable = mutants
     in code the corpus actually executed");
  2. materialise each mutant by copy-on-write overlay of the target
     scope header (`-I <overlay>` shadows `-I /opt/seqan3/include`
     in the compile command) with a single regex operator swap;
  3. rebuild the replay binary (`g++-12 -std=c++23 -O0 -g
     --coverage`);
  4. replay the full Phase-2 corpus through baseline + mutant, hash
     (exit-code, per-file-exit-code vector) → kill iff any file's
     exit code differs from baseline.

Operators (regex-based, `re.sub(count=1)` on the one chosen line):
  `==` ↔ `!=`, `<=` ↔ `>=`, `<` ↔ `>`,
  `&&` ↔ `||`, ` + ` ↔ ` - `, `true` ↔ `false`.
Templates use `<` / `>` heavily so the `<`/`>` swap is only picked
when the line also contains a comparison-like token (`==`, `!=`,
`< 0`, etc.) — the classifier in `_pick_mutants()` skips ambiguous
template-heavy lines automatically.

Usage (inside biotest-bench via bash compares/docker/run.sh):

    python3.12 compares/scripts/run_aflpp_seqan3_phase3.py \\
        --corpus compares/results/coverage/aflpp/seqan3/run_0/corpus \\
        --cov-gcovr-json compares/results/coverage/aflpp/seqan3/run_0/gcovr_snapshots/t_60s.json \\
        --budget-mutants 20 \\
        --out compares/results/mutation/aflpp/seqan3/

Output:
  <out>/summary.json            DESIGN §3.3 schema (killed / reachable / score)
  <out>/mutants/                per-mutant dirs with patched header +
                                baseline/mutant exit-code vectors +
                                kill decision
  <out>/MUTATION_RESULTS.md     human-readable report (written by the
                                caller after inspection; the driver
                                only writes JSON)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]

SEQAN3_INCLUDE = Path("/opt/seqan3/include")
SDSL_INCLUDE = Path("/opt/sdsl-lite/include")

HARNESS_CPP = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
               / "seqan3_sam_fuzzer.cpp")
COV_BUILD_DIR = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
                 / "build-cov")

# Scope — mirrors DESIGN §3.3 mutant target
# (`include/seqan3/io/sam_file/**`) + keeps the 3 substrings from
# biotest_config.yaml:coverage.target_filters.SAM.seqan3.
SCOPE_SUBSTRINGS = ("seqan3/io/sam_file", "format_sam", "cigar")

# Regex operator swaps. Each rule is (label, pattern, replacement).
# Compiled once, applied with re.sub(count=1) on the chosen line so
# only the first match flips per mutant.
OPERATORS: tuple[tuple[str, str, str], ...] = (
    ("EQ_TO_NE", r"==", "!="),
    ("NE_TO_EQ", r"!=", "=="),
    ("LE_TO_GE", r"<=", ">="),
    ("GE_TO_LE", r">=", "<="),
    ("AND_TO_OR", r"&&", "||"),
    ("OR_TO_AND", r"\|\|", "&&"),
    ("TRUE_TO_FALSE", r"\btrue\b", "false"),
    ("FALSE_TO_TRUE", r"\bfalse\b", "true"),
    ("PLUS_TO_MINUS", r"(?<= )\+(?= )", "-"),
    ("MINUS_TO_PLUS", r"(?<= )-(?= )", "+"),
)

# Lines in templates often carry `<` or `>` unrelated to comparisons;
# we only apply `<`/`>` operators where the line also contains an
# unambiguous comparison token. This keeps the mutation set
# compilable more reliably.
COMPARISON_GUARD = re.compile(r"[!=]=|<=|>=|\b(size|length|empty|bool)\s*\(")


def _sha256_files(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(p.name.encode()); h.update(b"\0")
        try:
            h.update(p.read_bytes())
        except OSError:
            h.update(b"<READERR>")
        h.update(b"\0")
    return h.hexdigest()


def _covered_lines(gcovr_json: Path) -> dict[str, set[int]]:
    """file -> set of line numbers with count>0 (i.e. executed by
    the Phase-2 corpus). Only scope files are kept."""
    out: dict[str, set[int]] = {}
    data = json.loads(gcovr_json.read_text(encoding="utf-8"))
    for f in data.get("files", []):
        name = (f.get("file") or "").replace("\\", "/")
        if not any(s in name for s in SCOPE_SUBSTRINGS):
            continue
        covered = set()
        for ln in f.get("lines", []):
            if ln.get("gcovr/noncode"):
                continue
            if int(ln.get("count", 0) or 0) > 0:
                covered.add(int(ln.get("line_number", 0)))
        if covered:
            out[name] = covered
    return out


def _pick_mutants(
    covered: dict[str, set[int]], budget: int,
) -> list[dict[str, Any]]:
    """Scan covered lines in scope files, emit up to `budget` mutants.

    Each mutant dict carries: `{id, file_rel, abs_path, line, operator,
    original_line, mutated_line}`. Picks deterministic (file order,
    line order, operator order) so a rerun produces the same set."""
    mutants: list[dict[str, Any]] = []
    for file_rel in sorted(covered):
        abs_path = SEQAN3_INCLUDE / file_rel
        if not abs_path.exists():
            continue
        src_lines = abs_path.read_text(encoding="utf-8", errors="replace").splitlines()
        for lineno in sorted(covered[file_rel]):
            if lineno <= 0 or lineno > len(src_lines):
                continue
            line = src_lines[lineno - 1]
            stripped = line.strip()
            # Skip preprocessor, pure-comment, empty, and include lines.
            if not stripped or stripped.startswith(("#", "//", "/*", "*")):
                continue
            if "seqan3" not in line and "::" not in line and not COMPARISON_GUARD.search(line):
                # Conservative filter — picks lines that look like they
                # execute seqan3 logic, not boilerplate.
                pass  # don't skip solely on this; fall through to per-op check
            for op_name, pat, rep in OPERATORS:
                if not re.search(pat, line):
                    continue
                # Skip patterns that clash with C++ templates/generics —
                # only accept lines that have a comparison guard token.
                if op_name in ("LE_TO_GE", "GE_TO_LE") and not COMPARISON_GUARD.search(line):
                    continue
                mutated = re.sub(pat, rep, line, count=1)
                if mutated == line:
                    continue
                mutants.append({
                    "id": f"m{len(mutants):03d}",
                    "file_rel": file_rel,
                    "abs_path": str(abs_path),
                    "line": lineno,
                    "operator": op_name,
                    "original_line": line,
                    "mutated_line": mutated,
                })
                if len(mutants) >= budget:
                    return mutants
                break  # one mutant per line (avoid over-sampling same site)
    return mutants


def _build_binary(overlay_dir: Path | None, out_bin: Path, build_log: Path) -> bool:
    """Build `seqan3_sam_fuzzer_cov` into `out_bin`. Overlay dir (if
    given) is `-I`-first so it shadows /opt/seqan3/include/…"""
    build_log.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["g++-12", "-std=c++23", "-O0", "-g", "--coverage"]
    if overlay_dir is not None:
        cmd.extend(["-I", str(overlay_dir)])
    cmd.extend([
        "-I", str(SEQAN3_INCLUDE),
        "-I", str(SDSL_INCLUDE),
        str(HARNESS_CPP),
        "-o", str(out_bin),
    ])
    with build_log.open("ab") as lf:
        lf.write(b"\n=== build ===\n")
        lf.write((" ".join(cmd) + "\n").encode())
        try:
            r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, timeout=180)
        except subprocess.TimeoutExpired:
            lf.write(b"\n<BUILD TIMEOUT>\n")
            return False
    return r.returncode == 0 and out_bin.exists()


def _replay(binary: Path, corpus: Path, timeout_s: int = 5) -> dict[str, Any]:
    """Feed each corpus file into binary on stdin. Record per-file
    (exit, signal) tuple + aggregate digest."""
    results: list[tuple[str, int]] = []
    total = accepted = rejected = timed_out = 0
    if not corpus.exists():
        return {"total": 0, "accepted": 0, "rejected": 0, "timeout": 0,
                "digest": "EMPTY", "per_file": []}
    for f in sorted(corpus.iterdir()):
        if not f.is_file():
            continue
        total += 1
        try:
            with f.open("rb") as stdin_src:
                r = subprocess.run(
                    [str(binary)], stdin=stdin_src,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    timeout=timeout_s, check=False,
                )
            rc = r.returncode
            if rc == 0:
                accepted += 1
            else:
                rejected += 1
        except subprocess.TimeoutExpired:
            rc = -999
            timed_out += 1
        except OSError:
            rc = -888
            rejected += 1
        results.append((f.name, rc))
    digest = hashlib.sha256(
        "\n".join(f"{n}:{c}" for n, c in results).encode()
    ).hexdigest()
    return {"total": total, "accepted": accepted, "rejected": rejected,
            "timeout": timed_out, "digest": digest, "per_file": results}


def _apply_mutant(mutant: dict[str, Any], overlay_dir: Path) -> Path:
    """Copy the scope file into overlay_dir, apply the regex swap at
    the chosen line, return the overlaid path."""
    rel = mutant["file_rel"]
    dst = overlay_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    src_lines = Path(mutant["abs_path"]).read_text(
        encoding="utf-8", errors="replace").splitlines(keepends=True)
    line_idx = mutant["line"] - 1
    original = src_lines[line_idx]
    # Preserve trailing newline style.
    trailing = ""
    if original.endswith("\n"):
        trailing = "\n"
        core = original[:-1]
    else:
        core = original
    for op_name, pat, rep in OPERATORS:
        if op_name == mutant["operator"]:
            core = re.sub(pat, rep, core, count=1)
            break
    src_lines[line_idx] = core + trailing
    dst.write_text("".join(src_lines), encoding="utf-8")
    return dst


def _run_one_mutant(
    mutant: dict[str, Any], baseline_digest: str, baseline_per_file: list,
    corpus: Path, mutant_root: Path, replay_timeout: int,
) -> dict[str, Any]:
    """Build + replay one mutant; return a decision record."""
    md = mutant_root / mutant["id"]
    md.mkdir(parents=True, exist_ok=True)
    overlay = md / "overlay"
    overlay.mkdir(exist_ok=True)
    _apply_mutant(mutant, overlay)
    bin_out = md / "seqan3_sam_fuzzer_cov"
    log = md / "build.log"
    t0 = time.time()
    build_ok = _build_binary(overlay, bin_out, log)
    build_s = time.time() - t0
    if not build_ok:
        return {**mutant, "status": "compile_failed",
                "build_ok": False, "build_s": round(build_s, 2),
                "killed": False, "reachable": False,
                "digest_mutant": None, "digest_baseline": baseline_digest,
                "first_divergence": None}
    t1 = time.time()
    rep = _replay(bin_out, corpus, timeout_s=replay_timeout)
    replay_s = time.time() - t1
    # Per-file comparison for diagnostic first-divergence.
    first_div = None
    base_map = dict(baseline_per_file)
    for name, rc in rep["per_file"]:
        if base_map.get(name) != rc:
            first_div = {"file": name, "baseline_rc": base_map.get(name),
                         "mutant_rc": rc}
            break
    killed = rep["digest"] != baseline_digest
    (md / "replay.json").write_text(json.dumps({
        "mutant": mutant,
        "baseline_digest": baseline_digest,
        "mutant_digest": rep["digest"],
        "total": rep["total"],
        "accepted": rep["accepted"],
        "rejected": rep["rejected"],
        "timeout": rep["timeout"],
        "first_divergence": first_div,
        "build_s": round(build_s, 2),
        "replay_s": round(replay_s, 2),
        "killed": killed,
    }, indent=2), encoding="utf-8")
    # Drop the per-mutant binary / overlay copies — they're big. Keep
    # the patched source overlay for audit (small).
    try:
        bin_out.unlink()
    except FileNotFoundError:
        pass
    # Clean .gcda left in build-cov to avoid polluting the next mutant.
    for g in COV_BUILD_DIR.glob("*.gcda"):
        try: g.unlink()
        except FileNotFoundError: pass
    return {**mutant, "status": "executed" if killed else "survived",
            "build_ok": True, "build_s": round(build_s, 2),
            "replay_s": round(replay_s, 2),
            "killed": killed, "reachable": True,
            "digest_mutant": rep["digest"], "digest_baseline": baseline_digest,
            "first_divergence": first_div,
            "replay_total": rep["total"], "replay_accepted": rep["accepted"],
            "replay_rejected": rep["rejected"], "replay_timeout": rep["timeout"]}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", type=Path, required=True,
                   help="Phase-2 AFL++ final corpus directory")
    p.add_argument("--cov-gcovr-json", type=Path, required=True,
                   help="Phase-2 gcovr JSON snapshot (final tick) for "
                        "selecting covered mutation sites")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--budget-mutants", type=int, default=20,
                   help="maximum number of mutants to generate + execute")
    p.add_argument("--replay-timeout", type=int, default=5,
                   help="per-file replay timeout (s)")
    args = p.parse_args(argv)

    if not HARNESS_CPP.exists():
        sys.stderr.write(f"[fatal] harness missing: {HARNESS_CPP}\n"); return 2
    if not args.corpus.exists():
        sys.stderr.write(f"[fatal] corpus missing: {args.corpus}\n"); return 2
    if not args.cov_gcovr_json.exists():
        sys.stderr.write(f"[fatal] gcovr JSON missing: {args.cov_gcovr_json}\n"); return 2
    if shutil.which("g++-12") is None:
        sys.stderr.write("[fatal] g++-12 not on PATH — run inside biotest-bench\n"); return 2

    args.out.mkdir(parents=True, exist_ok=True)
    mutant_root = args.out / "mutants"
    mutant_root.mkdir(exist_ok=True)

    print(f"[setup] corpus={args.corpus} ({sum(1 for _ in args.corpus.iterdir())} files)")
    print(f"[setup] gcovr source = {args.cov_gcovr_json}")

    # 1. Baseline build + replay.
    baseline_bin = args.out / "baseline" / "seqan3_sam_fuzzer_cov"
    baseline_bin.parent.mkdir(exist_ok=True)
    baseline_log = args.out / "baseline" / "build.log"
    print("[baseline] building…")
    if not _build_binary(None, baseline_bin, baseline_log):
        sys.stderr.write("[fatal] baseline build failed; see baseline/build.log\n")
        return 3
    print("[baseline] replaying corpus…")
    baseline_replay = _replay(baseline_bin, args.corpus, timeout_s=args.replay_timeout)
    (args.out / "baseline" / "replay.json").write_text(
        json.dumps(baseline_replay, indent=2), encoding="utf-8")
    print(f"[baseline] digest={baseline_replay['digest'][:16]}…  "
          f"files={baseline_replay['total']}  "
          f"acc={baseline_replay['accepted']}  "
          f"rej={baseline_replay['rejected']}  "
          f"to={baseline_replay['timeout']}")

    # 2. Pick mutants from covered lines.
    covered = _covered_lines(args.cov_gcovr_json)
    scope_total_lines = sum(len(v) for v in covered.values())
    print(f"[sites] scope files with covered lines: {len(covered)}; "
          f"total covered lines: {scope_total_lines}")
    mutants = _pick_mutants(covered, args.budget_mutants)
    print(f"[sites] picked {len(mutants)} mutants for execution")

    # 3. Execute each mutant.
    records: list[dict[str, Any]] = []
    for i, m in enumerate(mutants, start=1):
        print(f"[mutant {i}/{len(mutants)}] {m['id']} {m['operator']} "
              f"{m['file_rel']}:{m['line']}")
        rec = _run_one_mutant(
            m, baseline_replay["digest"], baseline_replay["per_file"],
            args.corpus, mutant_root, args.replay_timeout,
        )
        records.append(rec)
        status = "KILL" if rec["killed"] else ("SKIP(compile)"
                                               if rec["status"] == "compile_failed"
                                               else "LIVE")
        print(f"                {status}  build={rec.get('build_s', 0)}s")

    # 4. Aggregate.
    reachable = [r for r in records if r["reachable"]]
    killed = [r for r in reachable if r["killed"]]
    survived = [r for r in reachable if not r["killed"]]
    compile_failed = [r for r in records if r["status"] == "compile_failed"]
    score = (len(killed) / len(reachable)) if reachable else 0.0

    summary = {
        "tool": "aflpp",
        "sut": "seqan3",
        "format": "SAM",
        "phase": "mutation",
        "engine": "source_level_overlay (mull-alternative; DESIGN §3.3 semantics)",
        "mull_status": "blocked: mull-0.33 binary requires glibc 2.39; "
                       "biotest-bench ships glibc 2.35",
        "corpus_dir": str(args.corpus.resolve()),
        "corpus_size": baseline_replay["total"],
        "gcovr_source": str(args.cov_gcovr_json.resolve()),
        "scope_substrings": list(SCOPE_SUBSTRINGS),
        "budget_mutants": args.budget_mutants,
        "mutants_generated": len(records),
        "compile_failed": len(compile_failed),
        "reachable": len(reachable),
        "killed": len(killed),
        "survived": len(survived),
        "score": round(score, 4),
        "baseline_digest": baseline_replay["digest"],
        "operator_breakdown": {
            op: {
                "generated": sum(1 for r in records if r["operator"] == op),
                "reachable": sum(1 for r in reachable if r["operator"] == op),
                "killed": sum(1 for r in killed if r["operator"] == op),
            }
            for op in sorted({r["operator"] for r in records})
        },
        "per_file_breakdown": {
            fn: {
                "generated": sum(1 for r in records if r["file_rel"] == fn),
                "reachable": sum(1 for r in reachable if r["file_rel"] == fn),
                "killed": sum(1 for r in killed if r["file_rel"] == fn),
            }
            for fn in sorted({r["file_rel"] for r in records})
        },
        "mutants": records,
        "produced_at": time.time(),
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2),
                                          encoding="utf-8")
    print("\n==== Phase-3 mutation summary (AFL++ × seqan3) ====")
    print(f"  mutants generated : {len(records)}")
    print(f"  compile-failed    : {len(compile_failed)}")
    print(f"  reachable         : {len(reachable)}")
    print(f"  killed            : {len(killed)}")
    print(f"  survived          : {len(survived)}")
    print(f"  score             : {score:.4f}  "
          f"({len(killed)} / {len(reachable)})")
    print(f"  summary.json      : {args.out / 'summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
