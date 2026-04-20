"""Atheris harness for vcfpy VCF parsing.

vcfpy is the pure-Python bihealth/vcfpy parser. Unlike pysam, its
entire VCF surface is implemented in Python, so coverage.py traces it
cleanly and Atheris can drive it in-process without libFuzzer hooking
into Cython.

Coverage-growth mode (added 2026-04-20 for DESIGN §13.5 Phase 2).
When the orchestrator passes `--cov-growth-out=<path>` the harness:

  1. Starts `coverage.Coverage(source=['vcfpy'], branch=True)` before
     atheris.Setup() so every parser line / branch vcfpy executes is
     attributed.
  2. Spawns a daemon thread that sleeps until each tick boundary in
     `--cov-sample-ticks`, calls `cov.save()`, computes line/branch
     pct against the on-disk .coverage file, and appends a record
     to growth_<idx>.json (written after every tick so a crash
     still leaves a partial report).
  3. Atheris.Fuzz() runs for the libFuzzer `-max_total_time=` budget.
     On exit (normal or exit-77 crash), a finalizer writes any
     remaining ticks with `null` line/branch_pct (so the JSON schema
     always has the full tick list, as DESIGN §4.5 expects).

Smoke-test (60s, no coverage output — same shape as DESIGN §13.2.3):

    /opt/atheris-venv/bin/python compares/harnesses/atheris/fuzz_vcfpy.py \\
        -max_total_time=60 \\
        -artifact_prefix=/tmp/vcfpy/ \\
        /path/to/seeds/

Phase 2 (coverage growth, 7200s budget, full tick schedule):

    /opt/atheris-venv/bin/python compares/harnesses/atheris/fuzz_vcfpy.py \\
        --format=VCF \\
        --cov-data-file=/tmp/phase2/.coverage \\
        --cov-growth-out=/tmp/phase2/growth_0.json \\
        --cov-sample-ticks=1,10,60,300,1800,7200 \\
        -max_total_time=7200 \\
        -artifact_prefix=/tmp/phase2/crashes/ \\
        /path/to/seeds/
"""

from __future__ import annotations

import atexit
import io
import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path


# coverage.py must be imported + started BEFORE atheris.instrument_imports
# so the vcfpy module's import-time lines show up in the trace. The
# instrumenter adds bytecode hooks but coverage.py's line hook still fires
# underneath.
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
        source=["vcfpy"],
        branch=True,
        config_file=False,
    )
    cov.start()
    _COV_INSTANCE = cov


def _compute_pct(data_file: str) -> tuple[float | None, float | None,
                                          int, int, int, int]:
    """Return (line_pct, branch_pct, covered_lines, total_lines,
                covered_branches, total_branches).

    Values are computed by loading the freshly-saved .coverage db and
    calling coverage.Coverage.json_report() filtered to vcfpy.
    """
    import tempfile as _tempfile
    import coverage as _coverage_mod
    cov_reader = _coverage_mod.Coverage(
        data_file=data_file,
        source=["vcfpy"],
        branch=True,
        config_file=False,
    )
    try:
        cov_reader.load()
    except Exception:
        return None, None, 0, 0, 0, 0
    # coverage.json_report() wants a path, not a StringIO — write to a
    # throwaway temp file and immediately read it back.
    fd, tmp_path = _tempfile.mkstemp(prefix="atheris-vcfpy-cov-", suffix=".json")
    os.close(fd)
    try:
        try:
            cov_reader.json_report(outfile=tmp_path)
        except Exception:
            return None, None, 0, 0, 0, 0
        try:
            report = json.loads(Path(tmp_path).read_text(encoding="utf-8"))
        except Exception:
            return None, None, 0, 0, 0, 0
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
    totals = report.get("totals", {})
    covered_lines = int(totals.get("covered_lines", 0))
    missing_lines = int(totals.get("missing_lines", 0))
    total_lines = covered_lines + missing_lines
    line_pct = (covered_lines / total_lines * 100.0) if total_lines else None

    covered_branches = int(totals.get("covered_branches", 0))
    total_branches = int(totals.get("num_branches", 0))
    branch_pct = (covered_branches / total_branches * 100.0
                  if total_branches else None)
    return (line_pct, branch_pct,
            covered_lines, total_lines,
            covered_branches, total_branches)


def _write_growth() -> None:
    if not _COV_GROWTH_OUT:
        return
    # Emit each record already collected, plus a `pending: True` flag
    # for ticks that haven't been reached yet. Keeps the JSON's ticks
    # list stable across crashes.
    out = {
        "coverage_growth": list(_GROWTH_RECORDS),
        "tool": "atheris",
        "sut": "vcfpy",
        "format": "VCF",
    }
    with _GROWTH_LOCK:
        Path(_COV_GROWTH_OUT).parent.mkdir(parents=True, exist_ok=True)
        Path(_COV_GROWTH_OUT).write_text(json.dumps(out, indent=2),
                                         encoding="utf-8")


def _sample_once(t_s: int, wall_now: float) -> None:
    if _COV_INSTANCE is None or _COV_DATA_FILE is None:
        return
    # Flush in-memory counters to disk without stopping collection.
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


_ATEXIT_RAN = False


def _atexit_flush() -> None:
    """Idempotent coverage-shutdown hook. Runs on both libFuzzer's
    exit() path (via `atexit.register`) and the Python finally path."""
    global _ATEXIT_RAN
    if _ATEXIT_RAN:
        return
    _ATEXIT_RAN = True
    if _COV_INSTANCE is not None:
        try:
            _COV_INSTANCE.stop()
        except Exception:
            pass
        try:
            _COV_INSTANCE.save()
        except Exception:
            pass
    if _ARGS_COVERAGE_MODE:
        _finalize()


def _finalize() -> None:
    """Ensure every tick requested has a record before the process exits.

    If a tick fell exactly at or after atheris's max_total_time, the
    snapshot thread was still sleeping when libFuzzer returned and the
    record was never written. For Phase-2 coverage-growth we DO want a
    real value at every tick ≤ budget — the final coverage state is
    already saved to disk by main()'s finally clause, so we compute
    the pct from the terminal .coverage file and stamp it on every
    missing tick. Ticks > budget (shouldn't happen because the sampler
    passes ticks ≤ budget, but defensive) are stamped null with a
    `skipped_reason` so the schema is stable across runs.
    """
    recorded = {r["t_s"] for r in _GROWTH_RECORDS}
    wall_end = time.monotonic() - _T_START
    final_pct: tuple[float | None, float | None,
                     int, int, int, int] | None = None
    for tick in _COV_TICKS:
        if tick in recorded:
            continue
        if _COV_DATA_FILE and Path(_COV_DATA_FILE).exists():
            if final_pct is None:
                final_pct = _compute_pct(_COV_DATA_FILE)
            (line_pct, branch_pct,
             cov_lines, tot_lines,
             cov_branches, tot_branches) = final_pct
            rec = {
                "t_s": tick,
                "wall_s": wall_end,
                "line_pct": round(line_pct, 2) if line_pct is not None else None,
                "branch_pct": round(branch_pct, 2) if branch_pct is not None else None,
                "covered_lines": cov_lines,
                "total_lines": tot_lines,
                "covered_branches": cov_branches,
                "total_branches": tot_branches,
                "source": "finalize_snapshot",
            }
        else:
            rec = {
                "t_s": tick,
                "wall_s": wall_end,
                "line_pct": None,
                "branch_pct": None,
                "skipped_reason": "atheris_exited_before_tick",
            }
        with _GROWTH_LOCK:
            _GROWTH_RECORDS.append(rec)
    _write_growth()


# Start coverage BEFORE atheris instruments the imports.
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
    # Remove stale coverage data so the per-rep measurement starts clean.
    try:
        os.remove(_COV_DATA_FILE)
    except OSError:
        pass
    _start_coverage(_COV_DATA_FILE)

import atheris

with atheris.instrument_imports():
    import vcfpy


FORMAT = "VCF"


def _with_temp_input(data: bytes, suffix: str) -> Path:
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, prefix="atheris-vcfpy-"
    )
    try:
        tmp.write(data)
        tmp.flush()
        return Path(tmp.name)
    finally:
        tmp.close()


def fuzz_vcf(data: bytes) -> None:
    if not data:
        return
    path = _with_temp_input(data, ".vcf")
    try:
        reader = vcfpy.Reader.from_path(str(path))
        try:
            _ = reader.header
            for rec in reader:
                _ = rec.CHROM, rec.POS, rec.ID, rec.REF, rec.ALT
                _ = rec.QUAL, rec.FILTER
                _ = dict(rec.INFO)
                for call in rec.calls:
                    _ = call.sample, dict(call.data)
        finally:
            try:
                reader.close()
            except Exception:
                pass
    except BaseException:
        # Phase-2 coverage campaigns want the fuzz loop to keep going past
        # every reachable crash path — vcfpy raises VCFPyException /
        # OSError on expected malformed input, but we also want
        # TypeError / ValueError / IndexError (the "real" bug signals)
        # counted as coverage, not fatal. Bug detection for these bugs
        # lives in Phase 4 (bug_bench), not here. Catch BaseException so
        # libFuzzer never SIGABRTs out of the fuzz loop on a Python-level
        # exception.
        pass
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def fuzz_sam(_data: bytes) -> None:
    raise RuntimeError(
        "vcfpy is VCF-only; run the biopython or pysam harness for SAM."
    )


def _dispatch(data: bytes) -> None:
    if FORMAT == "SAM":
        fuzz_sam(data)
    else:
        fuzz_vcf(data)


def main() -> None:
    global FORMAT, _T_START
    argv = list(sys.argv)
    cleaned = []
    for tok in argv:
        if tok.startswith("--format="):
            FORMAT = tok.split("=", 1)[1].upper()
        elif tok.startswith("--cov-"):
            # consumed above at module load time; hide from atheris
            pass
        else:
            cleaned.append(tok)

    _T_START = time.monotonic()

    if _ARGS_COVERAGE_MODE and _COV_TICKS:
        t = threading.Thread(target=_snapshot_loop, daemon=True)
        t.start()

    # libFuzzer calls exit() when -max_total_time elapses, which bypasses
    # main()'s finally clause but still fires atexit handlers. Register
    # the coverage flush + finalize there so the growth JSON always has
    # a record per tick.
    atexit.register(_atexit_flush)

    try:
        atheris.Setup(cleaned, _dispatch)
        atheris.Fuzz()
    finally:
        _atexit_flush()


if __name__ == "__main__":
    main()
