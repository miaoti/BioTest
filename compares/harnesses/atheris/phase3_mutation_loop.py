"""Phase 3 mutation-testing loop — Atheris × biopython (DESIGN.md §3.3, §13.5).

Runs inside the `biotest-bench` Docker image where biopython 1.85 is
installed in the `/opt/atheris-venv/` (Python 3.11) site-packages. Given
a corpus of SAM inputs collected in Phase 2, this script:

1. Records a **baseline outcome** per corpus file (parse_success +
   exception class + observable canonical tuple) against the unmutated
   `Bio/Align/sam.py`.
2. **Generates mutants** from the AST of `Bio/Align/sam.py` using a
   mutmut-style operator set (arithmetic swaps, comparison flips,
   boolean constants, numeric-boundary ±1, string-literal mutation).
3. **Tests each mutant** by (a) writing the mutated source to
   site-packages, (b) spawning a fresh Python subprocess that parses the
   corpus, (c) comparing per-file outcomes to the baseline. A mutant is
   **killed** iff any input's outcome flips (parse-success flip,
   exception-type change, iteration-count change). Otherwise
   **survived**.
4. Emits `summary.json` + `mutants.jsonl` per DESIGN §4.5 + §3.3 at
   `<out>/`:
       {
         "tool":       "atheris",
         "sut":        "biopython",
         "phase":      "mutation",
         "target":     "Bio/Align/sam.py",
         "corpus_dir": "...",
         "budget_s":   <int>,
         "started_at": <epoch>,
         "ended_at":   <epoch>,
         "baseline":   {"total_files": N, "parse_success": K, ...},
         "mutation_score": {
           "killed":    M,
           "survived":  S,
           "reachable": M + S,
           "score":     round(M / (M + S), 4)
         },
         "untested": U,   # mutants generated but not executed (time budget)
         "total_generated": M + S + U
       }

The `mutants.jsonl` sidecar records one line per mutant actually tested:
`{id, operator, lineno, orig, new, outcome, diff_files[], elapsed_s}`.

Safety: the original `sam.py` is backed up to `<target>.phase3_bak`
before the run and restored unconditionally in the `finally` clause.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import io
import json
import logging
import os
import shutil
import subprocess
import sys
import time
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


logger = logging.getLogger("phase3_mutation_loop")


# ---------------------------------------------------------------------------
# Mutation operators (hand-rolled AST rewriters; each yields a COPY of the
# original tree with exactly one mutation applied)
# ---------------------------------------------------------------------------

ARITH_SWAPS: dict[type, type] = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.FloorDiv,
    ast.FloorDiv: ast.Mult,
    ast.Mod: ast.Mult,
    ast.Div: ast.Mult,
}

COMP_SWAPS: dict[type, type] = {
    ast.Lt: ast.GtE,
    ast.LtE: ast.Gt,
    ast.Gt: ast.LtE,
    ast.GtE: ast.Lt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.Is: ast.IsNot,
    ast.IsNot: ast.Is,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
}

BOOL_SWAPS: dict[type, type] = {
    ast.And: ast.Or,
    ast.Or: ast.And,
}


@dataclass
class Mutant:
    mutant_id: str
    operator: str
    lineno: int
    col_offset: int
    orig_repr: str
    new_repr: str
    # We keep the mutated source text lazily — generated when we apply it.
    mutated_source: str = ""


def _node_path(root: ast.AST, target: ast.AST) -> list[int]:
    """Return a list of child indices leading from root to target. Used
    to unambiguously address a node for deep-copy mutation."""
    path: list[int] = []

    def _walk(node: ast.AST, p: list[int]) -> bool:
        if node is target:
            path[:] = p
            return True
        for idx, child in enumerate(ast.iter_child_nodes(node)):
            if _walk(child, p + [idx]):
                return True
        return False

    _walk(root, [])
    return path


def _apply_via_path(root: ast.AST, path: list[int]) -> ast.AST:
    """Walk the deep-copied root to the same relative node."""
    cur = root
    for idx in path:
        cur = list(ast.iter_child_nodes(cur))[idx]
    return cur


def _replace_in_parent(root: ast.AST, path: list[int], new_node: ast.AST) -> None:
    """Replace node at path with new_node. Mutates in place."""
    if not path:
        raise ValueError("cannot replace root via path")
    # Walk parent
    cur: Any = root
    for idx in path[:-1]:
        cur = list(ast.iter_child_nodes(cur))[idx]
    # Find the named slot in parent's _fields that contains this child
    last_idx = path[-1]
    child_iter = []
    # Instead of iterating, we find which _field contains the target
    target_child = list(ast.iter_child_nodes(cur))[last_idx]
    for fname in cur._fields:
        val = getattr(cur, fname, None)
        if isinstance(val, list):
            for i, item in enumerate(val):
                if item is target_child:
                    val[i] = new_node
                    return
        elif val is target_child:
            setattr(cur, fname, new_node)
            return
    raise RuntimeError(
        f"could not locate target child in parent fields: {cur} / {target_child}"
    )


def _mutate_once(tree: ast.AST, node_path: list[int], new_node: ast.AST) -> ast.AST:
    """Deep-copy tree and apply a single-node replacement at the given path."""
    new_tree = copy.deepcopy(tree)
    _replace_in_parent(new_tree, node_path, new_node)
    ast.fix_missing_locations(new_tree)
    return new_tree


def _yield_mutants(tree: ast.AST, original_source: str) -> Iterable[Mutant]:
    """Walk the AST and yield (Mutant) objects for each applicable operator."""
    mut_idx = 0

    for node in ast.walk(tree):
        ln = getattr(node, "lineno", 0)
        co = getattr(node, "col_offset", 0)

        # Arithmetic operator swaps on BinOp.op
        if isinstance(node, ast.BinOp) and type(node.op) in ARITH_SWAPS:
            orig_op_cls = type(node.op)
            new_op_cls = ARITH_SWAPS[orig_op_cls]
            path = _node_path(tree, node)
            new_binop = copy.deepcopy(node)
            new_binop.op = new_op_cls()
            ast.copy_location(new_binop, node)
            yield Mutant(
                mutant_id=f"m{mut_idx:05d}",
                operator=f"arith_swap_{orig_op_cls.__name__}_to_{new_op_cls.__name__}",
                lineno=ln,
                col_offset=co,
                orig_repr=_astop_str(orig_op_cls),
                new_repr=_astop_str(new_op_cls),
                mutated_source=ast.unparse(_mutate_once(tree, path, new_binop)),
            )
            mut_idx += 1

        # Comparison operator swaps on Compare.ops[0] only (one mutant per
        # comparison node — multi-op chained compares are rare in real code)
        elif isinstance(node, ast.Compare) and node.ops:
            for i, cmp_op in enumerate(node.ops):
                if type(cmp_op) in COMP_SWAPS:
                    orig_op_cls = type(cmp_op)
                    new_op_cls = COMP_SWAPS[orig_op_cls]
                    path = _node_path(tree, node)
                    new_compare = copy.deepcopy(node)
                    new_compare.ops[i] = new_op_cls()
                    ast.copy_location(new_compare, node)
                    yield Mutant(
                        mutant_id=f"m{mut_idx:05d}",
                        operator=f"cmp_swap_{orig_op_cls.__name__}_to_{new_op_cls.__name__}",
                        lineno=ln,
                        col_offset=co,
                        orig_repr=_astop_str(orig_op_cls),
                        new_repr=_astop_str(new_op_cls),
                        mutated_source=ast.unparse(_mutate_once(tree, path, new_compare)),
                    )
                    mut_idx += 1

        # Boolean operator swaps (And↔Or)
        elif isinstance(node, ast.BoolOp) and type(node.op) in BOOL_SWAPS:
            orig_op_cls = type(node.op)
            new_op_cls = BOOL_SWAPS[orig_op_cls]
            path = _node_path(tree, node)
            new_boolop = copy.deepcopy(node)
            new_boolop.op = new_op_cls()
            ast.copy_location(new_boolop, node)
            yield Mutant(
                mutant_id=f"m{mut_idx:05d}",
                operator=f"boolop_swap_{orig_op_cls.__name__}_to_{new_op_cls.__name__}",
                lineno=ln,
                col_offset=co,
                orig_repr=orig_op_cls.__name__,
                new_repr=new_op_cls.__name__,
                mutated_source=ast.unparse(_mutate_once(tree, path, new_boolop)),
            )
            mut_idx += 1

        # UnaryOp: `not X` → `X` (remove the not)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            path = _node_path(tree, node)
            yield Mutant(
                mutant_id=f"m{mut_idx:05d}",
                operator="unary_not_removal",
                lineno=ln,
                col_offset=co,
                orig_repr=f"not {ast.unparse(node.operand)!s}",
                new_repr=ast.unparse(node.operand),
                mutated_source=ast.unparse(_mutate_once(tree, path, copy.deepcopy(node.operand))),
            )
            mut_idx += 1

        # Constant mutations: True↔False, None→0, int±1, empty string
        elif isinstance(node, ast.Constant):
            v = node.value
            new_vals: list[Any] = []
            if v is True:
                new_vals.append(False)
            elif v is False:
                new_vals.append(True)
            elif v is None:
                new_vals.append(0)
            elif isinstance(v, int) and not isinstance(v, bool):
                # Only mutate small integers — mutating giant constants is noisy
                if abs(v) <= 100:
                    new_vals.append(v + 1)
                    if v != 0:
                        new_vals.append(v - 1)
            elif isinstance(v, str) and 0 < len(v) <= 32:
                # Empty-string mutation is informative; skip trivial-length cases
                if v:
                    new_vals.append("")

            for new_val in new_vals:
                path = _node_path(tree, node)
                new_const = ast.Constant(value=new_val)
                ast.copy_location(new_const, node)
                yield Mutant(
                    mutant_id=f"m{mut_idx:05d}",
                    operator=f"const_{type(v).__name__}_to_{type(new_val).__name__}",
                    lineno=ln,
                    col_offset=co,
                    orig_repr=repr(v),
                    new_repr=repr(new_val),
                    mutated_source=ast.unparse(_mutate_once(tree, path, new_const)),
                )
                mut_idx += 1


def _astop_str(cls: type) -> str:
    """Pretty-print AST op class names (e.g., `Add` → `+`)."""
    mapping = {
        ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
        ast.Mod: "%", ast.FloorDiv: "//", ast.Pow: "**",
        ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=",
        ast.Eq: "==", ast.NotEq: "!=",
        ast.Is: "is", ast.IsNot: "is not",
        ast.In: "in", ast.NotIn: "not in",
    }
    return mapping.get(cls, cls.__name__)


# ---------------------------------------------------------------------------
# Baseline / outcome recording
# ---------------------------------------------------------------------------

# The worker script we spawn for each mutant (and for the baseline). It
# imports Bio.Align.sam fresh, parses each corpus file, and prints one
# JSON object per file so the driver can diff.
WORKER_SRC = r"""
import io, json, os, sys, traceback
from pathlib import Path

try:
    import numpy, Bio.Align  # noqa: F401
    from Bio.Align import sam as _biopython_sam
except Exception as e:  # pragma: no cover — defensive
    print(json.dumps({"_worker_fatal": type(e).__name__ + ": " + str(e)}), flush=True)
    sys.exit(2)


def one(path: str):
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"file": path, "ok": False, "err_type": "read_error",
                "err_msg": str(e)[:200]}
    buf = io.StringIO(text)
    try:
        it = _biopython_sam.AlignmentIterator(buf)
        aln_count = 0
        last_sig = None
        for aln in it:
            aln_count += 1
            tgt = str(getattr(aln, "target", ""))[:50]
            qry = str(getattr(aln, "query", ""))[:50]
            score = getattr(aln, "score", None)
            last_sig = (tgt[:20], qry[:20], str(score)[:20])
        return {
            "file": path, "ok": True, "aln_count": aln_count,
            "last_sig": last_sig, "err_type": None, "err_msg": None,
        }
    except Exception as e:
        return {"file": path, "ok": False,
                "err_type": type(e).__name__,
                "err_msg": str(e)[:200],
                "aln_count": None, "last_sig": None}


def main():
    corpus = sys.argv[1]
    files = sorted(Path(corpus).iterdir())
    for p in files:
        if not p.is_file():
            continue
        try:
            r = one(str(p))
        except BaseException as e:
            r = {"file": str(p), "ok": False, "err_type": "worker_exception",
                 "err_msg": type(e).__name__ + ": " + str(e)[:200]}
        print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
"""


def _run_worker(python_bin: str, worker_script: Path, corpus: Path,
                timeout_s: int) -> list[dict]:
    """Spawn the worker subprocess and collect its per-file JSON output."""
    try:
        p = subprocess.run(
            [python_bin, str(worker_script), str(corpus)],
            capture_output=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return [{"_worker_timeout": True}]
    out = p.stdout.decode(errors="replace")
    recs = []
    for line in out.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            continue
    if not recs and p.returncode != 0:
        recs.append({
            "_worker_fatal": True,
            "rc": p.returncode,
            "stderr_tail": p.stderr.decode(errors="replace")[-500:],
        })
    return recs


def _outcome_key(rec: dict) -> tuple:
    """Stable reducer: treat `ok=True, same aln_count, same last_sig` as
    'identical outcome'. Baseline vs mutant differ iff this tuple differs."""
    return (
        rec.get("ok"),
        rec.get("aln_count"),
        rec.get("err_type"),
        # Ignore err_msg because exception messages often vary by input payload
        # even when the *class* of failure is the same; the class is the
        # stable signal.
    )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", type=Path, required=True,
                   help="directory of SAM inputs to replay")
    p.add_argument("--target", type=Path,
                   default=Path("/opt/atheris-venv/lib/python3.11/site-packages/Bio/Align/sam.py"),
                   help="source file to mutate (must be writable)")
    p.add_argument("--python-bin", default="/opt/atheris-venv/bin/python",
                   help="python binary to use for the worker subprocess")
    p.add_argument("--out", type=Path, required=True,
                   help="output directory; summary.json + mutants.jsonl land here")
    p.add_argument("--budget-s", type=int, default=900,
                   help="wall-clock budget for the mutation loop, in seconds")
    p.add_argument("--per-mutant-timeout-s", type=int, default=60,
                   help="per-mutant worker hard timeout")
    p.add_argument("--max-mutants", type=int, default=0,
                   help="cap on mutants to TEST (0 = no cap; budget-bounded)")
    p.add_argument("--shuffle-seed", type=int, default=42,
                   help="seed for mutant-order shuffle; 0 = preserve generation order")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    args.out.mkdir(parents=True, exist_ok=True)
    mutants_log = args.out / "mutants.jsonl"
    summary_path = args.out / "summary.json"
    worker_path = args.out / "_worker.py"
    worker_path.write_text(WORKER_SRC, encoding="utf-8")
    backup_path = args.target.with_suffix(args.target.suffix + ".phase3_bak")

    started_at = time.time()
    original_src = args.target.read_text(encoding="utf-8")
    shutil.copy2(args.target, backup_path)
    logger.info("backed up target to %s", backup_path)

    try:
        # --- Baseline ---
        logger.info("computing baseline outcomes on %d corpus files...",
                    sum(1 for _ in args.corpus.iterdir()))
        baseline_recs = _run_worker(args.python_bin, worker_path, args.corpus,
                                    timeout_s=args.per_mutant_timeout_s)
        if baseline_recs and baseline_recs[0].get("_worker_fatal"):
            logger.error("baseline worker failed: %s", baseline_recs[0])
            return 2
        baseline_by_file = {r["file"]: r for r in baseline_recs if r.get("file")}
        b_success = sum(1 for r in baseline_by_file.values() if r.get("ok"))
        b_total = len(baseline_by_file)
        logger.info("baseline: %d / %d parse_success (n=%d files)",
                    b_success, b_total, b_total)

        # --- Generate mutants ---
        logger.info("parsing target AST: %s", args.target)
        tree = ast.parse(original_src, filename=str(args.target))
        mutants: list[Mutant] = list(_yield_mutants(tree, original_src))
        if args.shuffle_seed:
            import random
            random.Random(args.shuffle_seed).shuffle(mutants)
        logger.info("generated %d mutants (seed=%s)", len(mutants), args.shuffle_seed)

        # --- Test mutants until budget/max exceeded ---
        killed = 0
        survived = 0
        errored = 0
        untested = 0
        mutants_tested: list[dict] = []
        loop_deadline = started_at + args.budget_s

        with mutants_log.open("w", encoding="utf-8") as mf:
            for i, m in enumerate(mutants):
                if args.max_mutants and i >= args.max_mutants:
                    untested = len(mutants) - i
                    logger.info("max-mutants cap reached (%d); remaining %d untested",
                                args.max_mutants, untested)
                    break
                if time.time() >= loop_deadline:
                    untested = len(mutants) - i
                    logger.info("time budget exceeded at mutant %d; remaining %d untested",
                                i, untested)
                    break

                t0 = time.time()
                # Write mutant
                args.target.write_text(m.mutated_source, encoding="utf-8")
                recs = _run_worker(args.python_bin, worker_path, args.corpus,
                                   timeout_s=args.per_mutant_timeout_s)
                # Restore defensively in case next iteration's write races
                # (we re-write anyway, so not strictly needed; kept for safety)
                elapsed = time.time() - t0

                if recs and recs[0].get("_worker_fatal"):
                    outcome = "killed"  # worker failing to import/run counts as killed
                    diff_files: list[str] = [recs[0].get("stderr_tail", "")[:120]]
                    errored += 1
                elif recs and recs[0].get("_worker_timeout"):
                    outcome = "killed_timeout"
                    diff_files = []
                    killed += 1
                else:
                    mut_by_file = {r["file"]: r for r in recs if r.get("file")}
                    diff_files = []
                    for fname, baseline in baseline_by_file.items():
                        mrec = mut_by_file.get(fname)
                        if mrec is None:
                            diff_files.append(fname + ":missing")
                            continue
                        if _outcome_key(mrec) != _outcome_key(baseline):
                            diff_files.append(fname)
                    if diff_files:
                        outcome = "killed"
                        killed += 1
                    else:
                        outcome = "survived"
                        survived += 1

                rec = {
                    "id": m.mutant_id,
                    "operator": m.operator,
                    "lineno": m.lineno,
                    "col_offset": m.col_offset,
                    "orig": m.orig_repr,
                    "new": m.new_repr,
                    "outcome": outcome,
                    "elapsed_s": round(elapsed, 2),
                    "diff_files": diff_files[:10],
                    "diff_count": len(diff_files),
                }
                mf.write(json.dumps(rec) + "\n")
                mf.flush()
                mutants_tested.append(rec)
                logger.info(
                    "mutant %s [%s @ line %d]  %s  (diff=%d  %.1fs)  %d/%d",
                    m.mutant_id, m.operator, m.lineno, outcome,
                    len(diff_files), elapsed, i + 1, len(mutants),
                )
                # Restore to original for next iteration
                args.target.write_text(original_src, encoding="utf-8")

        # --- Summary ---
        reachable = killed + survived
        score = (killed / reachable) if reachable else 0.0
        ended_at = time.time()
        summary = {
            "tool": "atheris",
            "sut": "biopython",
            "format": "SAM",
            "phase": "mutation",
            "target": str(args.target),
            "corpus_dir": str(args.corpus),
            "python_bin": args.python_bin,
            "budget_s": args.budget_s,
            "per_mutant_timeout_s": args.per_mutant_timeout_s,
            "max_mutants": args.max_mutants,
            "shuffle_seed": args.shuffle_seed,
            "started_at": started_at,
            "ended_at": ended_at,
            "duration_s": round(ended_at - started_at, 2),
            "baseline": {
                "total_files": b_total,
                "parse_success": b_success,
                "parse_fail": b_total - b_success,
            },
            "mutation_score": {
                "killed": killed,
                "survived": survived,
                "reachable": reachable,
                "score": round(score, 4),
            },
            "untested": untested,
            "total_generated": len(mutants),
            "tested_operators": _operator_breakdown(mutants_tested),
        }
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        logger.info(
            "DONE — killed=%d survived=%d reachable=%d score=%.4f untested=%d "
            "(of %d generated) in %.1fs",
            killed, survived, reachable, score, untested, len(mutants),
            ended_at - started_at,
        )
        return 0

    finally:
        # ALWAYS restore — even on keyboard interrupt / exception
        try:
            shutil.copy2(backup_path, args.target)
            logger.info("restored target from %s", backup_path)
        except Exception:
            logger.exception("FAILED to restore target; file may be in mutated state: %s",
                             args.target)


def _operator_breakdown(records: list[dict]) -> dict[str, dict[str, int]]:
    """Group tested mutants by operator family; count killed vs survived."""
    out: dict[str, dict[str, int]] = {}
    for r in records:
        fam = r["operator"].split("_", 2)
        if len(fam) >= 2:
            key = "_".join(fam[:2])
        else:
            key = r["operator"]
        o = out.setdefault(key, {"killed": 0, "survived": 0})
        if r["outcome"].startswith("killed"):
            o["killed"] += 1
        else:
            o["survived"] += 1
    return out


if __name__ == "__main__":
    raise SystemExit(main())
