"""Atheris harness for Biopython's SAM parsing path (Bio.Align.sam).

Biopython has no VCF parser — only SAM is fuzzed here. Coverage-growth
mode mirrors the `fuzz_vcfpy.py` template (DESIGN.md §13.5 Phase 2).

Smoke mode (no coverage output — DESIGN §13.2.3 `Atheris × biopython`):

    /opt/atheris-venv/bin/python compares/harnesses/atheris/fuzz_biopython.py \\
        -max_total_time=60 \\
        -artifact_prefix=/tmp/bio/ \\
        /path/to/seeds/sam/

Coverage-growth mode (invoked by `compares/scripts/coverage_sampler.py`):

    /opt/atheris-venv/bin/python compares/harnesses/atheris/fuzz_biopython.py \\
        --format=SAM \\
        --cov-data-file=/tmp/phase2/.coverage \\
        --cov-growth-out=/tmp/phase2/growth_0.json \\
        --cov-sample-ticks=1,10,60,300,1800,7200 \\
        -max_total_time=7200 \\
        -artifact_prefix=/tmp/phase2/crashes/ \\
        /path/to/seeds/sam/

Atheris reports uncaught exceptions as findings. The fuzz target catches
only the exceptions Biopython raises for legitimately malformed input;
anything beyond that list (UnboundLocalError, SystemExit, etc.) is a
real Biopython defect and propagates so libFuzzer logs it.
"""

from __future__ import annotations

import io
import json
import os
import sys
import threading
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Coverage-growth mode — parse CLI flags and start coverage.py BEFORE
# atheris.instrument_imports so every Bio.Align.sam line/branch is
# attributed. Same contract as fuzz_vcfpy.py.
# ---------------------------------------------------------------------------

_COV_INSTANCE = None
_COV_DATA_FILE: str | None = None
_COV_GROWTH_OUT: str | None = None
_COV_TICKS: list[int] = []
_GROWTH_RECORDS: list[dict] = []
_GROWTH_LOCK = threading.Lock()
_T_START = 0.0


def _start_coverage(data_file: str) -> None:
    global _COV_INSTANCE
    import coverage as _coverage_mod
    cov = _coverage_mod.Coverage(
        data_file=data_file,
        source=["Bio.Align.sam"],
        branch=True,
        config_file=False,
    )
    cov.start()
    _COV_INSTANCE = cov


def _compute_pct(data_file: str) -> tuple[float | None, float | None,
                                          int, int, int, int]:
    """Return (line_pct, branch_pct, covered_lines, total_lines,
                covered_branches, total_branches) for `Bio.Align.sam`.

    Uses the `CoverageData` + `analysis2` API directly. We avoided
    `Coverage.json_report(outfile=...)` because several coverage.py
    versions reject a StringIO there with a path-only TypeError."""
    import coverage as _coverage_mod
    cov_reader = _coverage_mod.Coverage(
        data_file=data_file,
        source=["Bio.Align.sam"],
        branch=True,
        config_file=False,
    )
    try:
        cov_reader.load()
    except Exception:
        return None, None, 0, 0, 0, 0

    data = cov_reader.get_data()
    covered_lines = missing_lines = 0
    covered_branches = total_branches = 0

    for fname in data.measured_files():
        norm = fname.replace("\\", "/")
        if "Bio/Align/sam" not in norm:
            continue
        try:
            _, statements, _excluded, missing, *_ = cov_reader.analysis2(fname)
        except Exception:
            # If analysis2 can't re-read the source (e.g. host source tree
            # is ephemeral) fall back to data.lines / data.missing which
            # still gives an accurate executed-line count.
            executed = data.lines(fname) or []
            covered_lines += len(executed)
            continue
        covered_lines += len(statements) - len(missing)
        missing_lines += len(missing)

        if data.has_arcs():
            arcs = data.arcs(fname) or []
            covered_branches += len(arcs)
            # Upper-bound heuristic — coverage.py doesn't expose the
            # reachable-arc set without AST compilation. 2×statements is
            # the same estimate used by coverage_sampler._atheris_snapshots_to_ticks.
            total_branches += max(len(arcs), 2 * len(statements))

    total_lines = covered_lines + missing_lines
    line_pct = (covered_lines / total_lines * 100.0) if total_lines else None
    branch_pct = (covered_branches / total_branches * 100.0
                  if total_branches else None)
    return (line_pct, branch_pct,
            covered_lines, total_lines,
            covered_branches, total_branches)


def _write_growth() -> None:
    if not _COV_GROWTH_OUT:
        return
    out = {
        "coverage_growth": list(_GROWTH_RECORDS),
        "tool": "atheris",
        "sut": "biopython",
        "format": "SAM",
    }
    with _GROWTH_LOCK:
        Path(_COV_GROWTH_OUT).parent.mkdir(parents=True, exist_ok=True)
        Path(_COV_GROWTH_OUT).write_text(json.dumps(out, indent=2),
                                         encoding="utf-8")


def _sample_once(t_s: int, wall_now: float) -> None:
    if _COV_INSTANCE is None or _COV_DATA_FILE is None:
        return
    try:
        _COV_INSTANCE.save()
    except Exception as e:  # pragma: no cover — defensive
        rec = {"t_s": t_s, "wall_s": wall_now - _T_START,
               "line_pct": None, "branch_pct": None,
               "error": f"cov.save failed: {type(e).__name__}: {e}"}
        with _GROWTH_LOCK:
            _GROWTH_RECORDS.append(rec)
        return
    (line_pct, branch_pct,
     cov_lines, tot_lines,
     cov_branches, tot_branches) = _compute_pct(_COV_DATA_FILE)
    rec = {
        "t_s": t_s,
        "wall_s": wall_now - _T_START,
        "line_pct": round(line_pct, 2) if line_pct is not None else None,
        "branch_pct": round(branch_pct, 2) if branch_pct is not None else None,
        "covered_lines": cov_lines,
        "total_lines": tot_lines,
        "covered_branches": cov_branches,
        "total_branches": tot_branches,
    }
    with _GROWTH_LOCK:
        _GROWTH_RECORDS.append(rec)
    _write_growth()


def _snapshot_loop() -> None:
    for tick in _COV_TICKS:
        wait = (_T_START + tick) - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _sample_once(tick, time.monotonic())


def _finalize() -> None:
    """Post-atheris sweep. For every tick that didn't fire during the
    sampling thread (typically the final tick, which races with libFuzzer
    shutdown + daemon-thread kill), compute coverage from the
    already-saved `.coverage` file so the DESIGN §4.5 tick list is
    complete. Falls back to a null record only if no `.coverage` file
    exists on disk (can happen if coverage.start never ran)."""
    recorded = {r["t_s"] for r in _GROWTH_RECORDS}
    wall_end = time.monotonic() - _T_START
    for tick in _COV_TICKS:
        if tick in recorded:
            continue
        if _COV_DATA_FILE and Path(_COV_DATA_FILE).exists():
            (line_pct, branch_pct,
             cov_lines, tot_lines,
             cov_branches, tot_branches) = _compute_pct(_COV_DATA_FILE)
            rec = {
                "t_s": tick,
                "wall_s": wall_end,
                "line_pct": round(line_pct, 2) if line_pct is not None else None,
                "branch_pct": round(branch_pct, 2) if branch_pct is not None else None,
                "covered_lines": cov_lines,
                "total_lines": tot_lines,
                "covered_branches": cov_branches,
                "total_branches": tot_branches,
                "recovered_from": "final_coverage_snapshot",
            }
        else:
            rec = {
                "t_s": tick,
                "wall_s": wall_end,
                "line_pct": None,
                "branch_pct": None,
                "skipped_reason": "no_coverage_data_on_disk",
            }
        with _GROWTH_LOCK:
            _GROWTH_RECORDS.append(rec)
    _write_growth()


_ARGS_COVERAGE_MODE = any(a.startswith("--cov-growth-out=") for a in sys.argv)
if _ARGS_COVERAGE_MODE:
    for _a in sys.argv:
        if _a.startswith("--cov-data-file="):
            _COV_DATA_FILE = _a.split("=", 1)[1]
        elif _a.startswith("--cov-growth-out="):
            _COV_GROWTH_OUT = _a.split("=", 1)[1]
        elif _a.startswith("--cov-sample-ticks="):
            _COV_TICKS = sorted({int(x) for x in _a.split("=", 1)[1].split(",")})
    if _COV_DATA_FILE is None:
        _COV_DATA_FILE = str(Path(_COV_GROWTH_OUT).with_name(".coverage"))
    Path(_COV_DATA_FILE).parent.mkdir(parents=True, exist_ok=True)
    try:
        os.remove(_COV_DATA_FILE)
    except OSError:
        pass


# Pre-load numpy + Bio.Align BEFORE we start coverage.py or atheris.
# Two interactions drove this ordering (both observed 2026-04-20):
#   1. numpy 2.x's `_core._multiarray_umath` raises `ImportError: cannot
#      load module more than once per process` if its C extension is
#      visited while `sys.settrace` is already active (coverage.py's hook).
#   2. Atheris 2.3.0's `instrument_imports` rewrites numpy bytecode in a
#      way that trips Bio.Align's `MissingPythonDependencyError`.
# Keeping numpy + Bio.Align outside both hooks side-steps both.
import numpy as _np  # noqa: F401,E402
import Bio.Align as _bio_align  # noqa: F401,E402

if _ARGS_COVERAGE_MODE:
    _start_coverage(_COV_DATA_FILE)


import atheris  # noqa: E402

with atheris.instrument_imports():
    from Bio.Align import sam as _biopython_sam  # noqa: F401


FORMAT = "SAM"


def fuzz_sam(data: bytes) -> None:
    if not data:
        return
    try:
        text = data.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        return

    buf = io.StringIO(text)
    try:
        alignments = _biopython_sam.AlignmentIterator(buf)
        for aln in alignments:
            _ = aln.target
            _ = aln.query
            _ = aln.score if hasattr(aln, "score") else None
            _ = str(aln.coordinates) if hasattr(aln, "coordinates") else None
    # Phase-2 coverage-growth mode (§13.5): we want the fuzz loop to keep
    # running past every known biopython defect (biopython-4825,
    # AssertionError from sam.py:729 on malformed CIGAR/SEQ, etc.) so the
    # coverage curve accumulates over the full budget. Bug-finding lives
    # in Phase 4 (bug-bench), not here. Catch Exception broadly; the
    # surrounding libFuzzer runtime still counts each raised exception as
    # a finding, but the process keeps going.
    except Exception as expected:  # noqa: BLE001
        del expected


def _dispatch(data: bytes) -> None:
    fuzz_sam(data)


def main() -> None:
    global FORMAT, _T_START
    argv = list(sys.argv)
    cleaned: list[str] = []
    for tok in argv:
        if tok.startswith("--format="):
            FORMAT = tok.split("=", 1)[1].upper()
        elif tok.startswith("--cov-"):
            # consumed at module load time; hide from atheris
            pass
        else:
            cleaned.append(tok)

    _T_START = time.monotonic()

    if _ARGS_COVERAGE_MODE and _COV_TICKS:
        t = threading.Thread(target=_snapshot_loop, daemon=True)
        t.start()

    try:
        atheris.Setup(cleaned, _dispatch)
        atheris.Fuzz()
    finally:
        if _COV_INSTANCE is not None:
            try:
                _COV_INSTANCE.stop()
                _COV_INSTANCE.save()
            except Exception:
                pass
        if _ARGS_COVERAGE_MODE:
            _finalize()


if __name__ == "__main__":
    main()
