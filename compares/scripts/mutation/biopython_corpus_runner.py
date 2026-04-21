"""Biopython Bio.Align.sam corpus-runner for mutmut (Phase-3 driver).

mutmut contract (``[tool.mutmut] runner = "<cmd>"``):
  * exit 0 → SURVIVED; exit 1 → KILLED; exit 33 → no tests.

This script plays the `pytest` role: replays a pure_random corpus
through the mutated `Bio.Align.sam.AlignmentIterator` and compares
fingerprints to a pre-mutation baseline.

Envs (set by mutation_driver):
  * MUTMUT_RUNNER_MODE        "baseline" or "check" (default "check")
  * MUTMUT_BIOPYTHON_SRC      path to mutable Bio/Align/sam.py
  * MUTMUT_CORPUS_DIR         directory of corpus files
  * MUTMUT_BASELINE_FILE      JSON {filename: fingerprint}
  * MUTMUT_CORPUS_SAMPLE      optional N (default 200)
  * MUTMUT_CORPUS_TIMEOUT_S   optional per-file timeout (default 2.0s)
"""

from __future__ import annotations

import hashlib
import json
import os
import signal
import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    src = os.environ.get("MUTMUT_BIOPYTHON_SRC")
    if not src:
        return
    pkg_file = Path(src).resolve()
    # If mutmut mutates Bio/Align/sam.py in place we need its parent
    # three levels up on sys.path so `from Bio.Align import sam` loads
    # our mutable copy. But dragging the whole Bio tree into the copy
    # is wasteful — instead, we replace the LIVE module's bytecode by
    # importing from the mutable file directly.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "Bio.Align.sam", str(pkg_file),
    )
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    # Pre-import heavy deps so numpy's C ext loads before our swap.
    import numpy  # noqa: F401
    from Bio import Align  # noqa: F401 — parent package
    spec.loader.exec_module(module)
    sys.modules["Bio.Align.sam"] = module


class _TimeoutError(Exception):
    pass


def _alarm_handler(_signum, _frame):
    raise _TimeoutError("per-file parse exceeded MUTMUT_CORPUS_TIMEOUT_S")


def _sample_corpus_files(corpus_dir: Path, max_n: int) -> list[Path]:
    return sorted(p for p in corpus_dir.iterdir() if p.is_file())[:max_n]


def _fingerprint_for_file(path: Path, timeout_s: float) -> str:
    from Bio.Align import sam as _sam

    h = hashlib.sha1()
    if os.name == "posix":
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_s)
    try:
        try:
            with open(path) as fh:
                it = _sam.AlignmentIterator(fh)
                count = 0
                for rec in it:
                    count += 1
                    if count >= 200:
                        h.update(b"|cap")
                        break
                    try:
                        row = (
                            getattr(rec, "target", None),
                            getattr(rec, "query", None),
                            type(rec).__name__,
                        )
                        h.update(b"|r")
                        h.update(repr(row).encode(errors="replace"))
                    except BaseException as exc:
                        h.update(b"|r-fail:")
                        h.update(type(exc).__name__.encode())
                h.update(f"|n={count}".encode())
        except BaseException as exc:
            # Include a short exception-message fragment so header-reject
            # mutations that change the error text (same exception class,
            # different message) still flip the fingerprint. Without
            # this, pure-random's single-bucket corpus can't distinguish
            # most deep-parser mutations.
            msg = str(exc).replace("\n", " ")[:96]
            h.update(
                f"open-or-parse-fail:{type(exc).__name__}:{msg}".encode(
                    errors="replace",
                )
            )
    except _TimeoutError:
        return hashlib.sha1(b"timeout").hexdigest()
    finally:
        if os.name == "posix":
            signal.setitimer(signal.ITIMER_REAL, 0)
    return h.hexdigest()


def _run_baseline(corpus: Path, baseline: Path, n: int, to: float) -> int:
    _ensure_src_on_path()
    out = {p.name: _fingerprint_for_file(p, to)
           for p in _sample_corpus_files(corpus, n)}
    baseline.parent.mkdir(parents=True, exist_ok=True)
    baseline.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[baseline] wrote {len(out)} entries to {baseline}")
    return 0


def _run_check(corpus: Path, baseline: Path, n: int, to: float) -> int:
    if not baseline.exists():
        print(f"[check] baseline missing: {baseline}", file=sys.stderr)
        return 33
    ref = json.loads(baseline.read_text(encoding="utf-8"))
    _ensure_src_on_path()
    for p in _sample_corpus_files(corpus, n):
        if p.name not in ref:
            continue
        fp = _fingerprint_for_file(p, to)
        if fp != ref[p.name]:
            print(f"[check] KILL {p.name}: base={ref[p.name][:12]} "
                  f"mut={fp[:12]}", file=sys.stderr)
            return 1
    return 0


def main() -> int:
    mode = os.environ.get("MUTMUT_RUNNER_MODE", "check").lower()
    corpus = Path(os.environ.get("MUTMUT_CORPUS_DIR", "")).resolve()
    baseline = Path(os.environ.get("MUTMUT_BASELINE_FILE", "")).resolve()
    n = int(os.environ.get("MUTMUT_CORPUS_SAMPLE", "200"))
    to = float(os.environ.get("MUTMUT_CORPUS_TIMEOUT_S", "2.0"))
    if not corpus.exists() or not corpus.is_dir():
        print(f"[runner] MUTMUT_CORPUS_DIR invalid: {corpus}", file=sys.stderr)
        return 2
    if mode == "baseline":
        return _run_baseline(corpus, baseline, n, to)
    return _run_check(corpus, baseline, n, to)


if __name__ == "__main__":
    raise SystemExit(main())
