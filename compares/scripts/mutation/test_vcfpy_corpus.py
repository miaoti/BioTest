"""pytest test that acts as the mutmut runner for Atheris × vcfpy.

mutmut 3.x is pytest-coupled (see ``PytestRunner`` in
``mutmut/__main__.py``): the `runner` setup.cfg knob only switches to
the alternative HammettRunner, not to a custom shell script. To drive
mutmut with a fuzzer corpus we therefore package the corpus-replay
logic as a pytest test and let mutmut auto-copy this file into
``mutants/tests/`` before each run.

The test is one function (``test_vcfpy_corpus_vs_baseline``) so every
mutant either kills it or doesn't — mutmut can't split credit across
multiple tests, but the fuzzer corpus is the evidence either way.

Execution path inside mutmut:

  1. mutmut rewrites every ``vcfpy/**.py`` to insert mutant functions +
     a trampoline guarded by ``os.environ['MUTANT_UNDER_TEST']``.
  2. mutmut copies the rewritten tree into ``<cell>/mutants/``, then
     copies ``<cell>/tests/`` alongside to ``<cell>/mutants/tests/``.
  3. For each mutant:
       a. mutmut sets ``MUTANT_UNDER_TEST=<mangled_name>`` (or "stats"
          for the stats phase).
       b. mutmut calls ``pytest -x -q --import-mode=append <test-ids>``
          inside ``<cell>/mutants/``.
       c. pytest collects this file, imports ``vcfpy`` (which resolves
          to ``<cell>/mutants/vcfpy/`` — the mutated copy — because
          mutmut prepends ``mutants`` to sys.path), runs the test.
       d. Test replays the Phase-2 atheris corpus, compares
          fingerprints against the pre-captured baseline, passes or
          fails.

Environment variables (set by ``mutation_driver.py``; the test reads
them at collection time from ``mutants/tests/conftest.py``):

  * ``MUTMUT_CORPUS_DIR``       — absolute path to corpus .vcf files.
  * ``MUTMUT_BASELINE_FILE``    — absolute path to baseline fingerprint JSON.
  * ``MUTMUT_CORPUS_SAMPLE``    — max corpus files to replay (first-N,
                                  sorted by filename).
  * ``MUTMUT_CORPUS_TIMEOUT_S`` — per-file parse timeout (SIGALRM).

Exit-code semantics (pytest → mutmut):

  * exit 0 (all pass) → mutant SURVIVED.
  * exit 1 (≥1 fail) → mutant KILLED.
  * exit 5 (no tests collected) → mutmut records "no tests" (meaning
    the mutant's function was never reached by the runner — treated
    as unreachable).

Notes on robustness:

  * We catch ``BaseException`` inside ``_fingerprint_for_file`` — a
    mutation might throw ``SystemExit``, ``KeyboardInterrupt``, or any
    Python exception from deep inside vcfpy, and a kill on *any* of
    those signals is still a kill.
  * Timeouts are handled via ``signal.setitimer`` on POSIX. The test
    is skipped on Windows (mutmut is Linux-only in practice).
"""

from __future__ import annotations

import hashlib
import json
import os
import signal
from pathlib import Path

import pytest


class _TimeoutError(Exception):
    pass


def _alarm_handler(_signum, _frame):
    raise _TimeoutError("per-file parse exceeded MUTMUT_CORPUS_TIMEOUT_S")


def _fingerprint_for_file(path, timeout_s):
    """Coarse, counting-only fingerprint.

    Earlier revisions hashed repr(record) which made the fingerprint
    sensitive to insertion-order / method-binding drift introduced by
    mutmut's trampoline rewrite even when MUTANT_UNDER_TEST was empty
    — that produced false "kill" signals on the baseline vs. stats
    phase. We instead compute ONLY integer counts over the parsed
    stream (which are invariant under mutmut's always-call-orig path)
    AND exception-class labels on failure paths (which DO flip on
    mutations that change error semantics — exactly what we want to
    catch). This is the same "count-based semantic fingerprint"
    pattern Phase-4's bug-bench differential oracle uses.
    """
    import vcfpy

    open_tag = "ok"
    n_header_lines = 0
    header_key_total = 0
    n_records = 0
    n_iter_fail = ""
    n_alt_total = 0
    n_info_key_total = 0
    n_format_key_total = 0
    n_call_total = 0
    n_filter_total = 0
    pos_sum = 0
    ref_len_sum = 0
    chrom_charsum = 0

    if os.name == "posix":
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_s)
    try:
        try:
            reader = vcfpy.Reader.from_path(str(path))
        except BaseException as exc:
            return "open-fail:" + type(exc).__name__
        try:
            try:
                lines = list(reader.header.lines)
                n_header_lines = len(lines)
                for ln in lines:
                    header_key_total += len(str(getattr(ln, "key", "")))
            except BaseException as exc:
                n_header_lines = -1
                header_key_total = -1 * len(type(exc).__name__)

            while True:
                try:
                    rec = next(reader)
                except StopIteration:
                    break
                except BaseException as exc:
                    n_iter_fail = type(exc).__name__
                    break
                try:
                    n_records += 1
                    n_alt_total += len(rec.ALT or [])
                    n_info_key_total += len(rec.INFO or {})
                    n_format_key_total += len(rec.FORMAT or [])
                    n_call_total += len(rec.calls)
                    n_filter_total += len(rec.FILTER or [])
                    try:
                        pos_sum += int(rec.POS or 0)
                    except Exception:
                        pass
                    ref_len_sum += len(str(rec.REF or ""))
                    chrom_charsum += sum(
                        ord(c) for c in str(rec.CHROM or "")
                    )
                except BaseException as exc:
                    n_iter_fail = "rec-fail:" + type(exc).__name__
                    break
                if n_records >= 200:
                    break
        finally:
            try:
                reader.close()
            except BaseException:
                pass
    except _TimeoutError:
        return "timeout"
    finally:
        if os.name == "posix":
            signal.setitimer(signal.ITIMER_REAL, 0)

    parts = [
        open_tag,
        f"hdr={n_header_lines}",
        f"hkt={header_key_total}",
        f"rec={n_records}",
        f"ifail={n_iter_fail}",
        f"alt={n_alt_total}",
        f"info={n_info_key_total}",
        f"fmt={n_format_key_total}",
        f"calls={n_call_total}",
        f"filt={n_filter_total}",
        f"pos={pos_sum}",
        f"ref={ref_len_sum}",
        f"chr={chrom_charsum}",
    ]
    return hashlib.sha1("|".join(parts).encode()).hexdigest()


def _sample_corpus(corpus_dir, max_n):
    files = sorted(p for p in corpus_dir.iterdir() if p.is_file())
    return files[:max_n]


@pytest.fixture(scope="session")
def _corpus_context():
    corpus_dir = Path(os.environ["MUTMUT_CORPUS_DIR"]).resolve()
    baseline_file = Path(os.environ["MUTMUT_BASELINE_FILE"]).resolve()
    sample_n = int(os.environ.get("MUTMUT_CORPUS_SAMPLE", "120"))
    timeout_s = float(os.environ.get("MUTMUT_CORPUS_TIMEOUT_S", "2.0"))
    assert corpus_dir.is_dir(), f"corpus dir missing: {corpus_dir}"
    assert baseline_file.exists(), f"baseline missing: {baseline_file}"
    baseline = json.loads(baseline_file.read_text(encoding="utf-8"))
    return {
        "corpus_dir": corpus_dir,
        "baseline_file": baseline_file,
        "baseline": baseline,
        "sample_n": sample_n,
        "timeout_s": timeout_s,
    }


def test_vcfpy_corpus_vs_baseline(_corpus_context):
    """Pass if every corpus file's mutated output matches its baseline
    fingerprint; fail on first divergence (which kills the mutant)."""
    ctx = _corpus_context
    for f in _sample_corpus(ctx["corpus_dir"], ctx["sample_n"]):
        if f.name not in ctx["baseline"]:
            continue
        fp = _fingerprint_for_file(f, ctx["timeout_s"])
        assert fp == ctx["baseline"][f.name], (
            f"fingerprint flip on {f.name}: "
            f"baseline={ctx['baseline'][f.name][:12]} "
            f"mutant={fp[:12]}"
        )
