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
    import vcfpy

    h = hashlib.sha1()
    if os.name == "posix":
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_s)
    try:
        try:
            reader = vcfpy.Reader.from_path(str(path))
        except BaseException as exc:
            h.update(f"open-fail:{type(exc).__name__}".encode())
            return h.hexdigest()
        try:
            try:
                header_hash = str(sorted(
                    (ln.key, str(getattr(ln, "mapping", "")))
                    for ln in reader.header.lines
                ))
                h.update(b"hdr|")
                h.update(header_hash.encode())
            except BaseException as exc:
                h.update(f"hdr-fail:{type(exc).__name__}".encode())

            for i, rec in enumerate(reader):
                try:
                    alt_tag = tuple(
                        type(a).__name__ + ":" + str(getattr(a, "value", a))
                        for a in (rec.ALT or [])
                    )
                    info_keys = tuple(sorted((rec.INFO or {}).keys()))
                    fmt_keys = tuple(rec.FORMAT or [])
                    sample_hash = len(rec.calls)
                    rec_fp = (
                        rec.CHROM, rec.POS, rec.ID, rec.REF,
                        alt_tag, rec.QUAL, tuple(rec.FILTER or []),
                        info_keys, fmt_keys, sample_hash,
                    )
                    h.update(b"|r")
                    h.update(repr(rec_fp).encode())
                except BaseException as exc:
                    h.update(b"|r-fail:")
                    h.update(f"{type(exc).__name__}".encode())
                if i >= 200:
                    h.update(b"|cap")
                    break
        finally:
            try:
                reader.close()
            except BaseException:
                pass
    except _TimeoutError:
        return hashlib.sha1(b"timeout").hexdigest()
    finally:
        if os.name == "posix":
            signal.setitimer(signal.ITIMER_REAL, 0)
    return h.hexdigest()


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
