"""mutmut runner for Atheris × vcfpy Phase-3 mutation testing.

mutmut's contract for a runner (``[tool.mutmut] runner = "<cmd>"``):

  * exit 0  → mutant SURVIVED (test suite passed, bad)
  * exit 1  → mutant KILLED   (at least one test failed, good)
  * exit 33 → "no tests"      (ignored by mutmut)

This script plays the `pytest` role. Instead of running unit tests it
replays a fuzzer-grown corpus through ``vcfpy.Reader`` and compares
the output fingerprint to a baseline captured before mutation.

A single run is cheap: ~50 corpus files × ~5 ms = <0.5 s, plus ~0.5 s
Python+vcfpy import. Fits comfortably inside mutmut's per-mutant slot
so the full campaign stays within the DESIGN.md §13.5 Phase 3 2 h
budget.

Modes
-----

1. ``MUTMUT_RUNNER_MODE=baseline``
   Walk the corpus, compute output fingerprints with the *unmutated*
   vcfpy, and write them to ``$MUTMUT_BASELINE_FILE``.

2. default (any other value or unset)
   Load the baseline, replay the sampled corpus, and exit 1 on the
   first observed divergence.

Environment variables used (set by ``mutation_driver.py``):

  * ``MUTMUT_RUNNER_MODE``      — "baseline" or "check" (default).
  * ``MUTMUT_VCFPY_SRC``        — path to the mutable vcfpy package
                                  (prepended to sys.path so ``import
                                  vcfpy`` resolves to the mutant
                                  source, NOT the venv's pristine copy).
  * ``MUTMUT_CORPUS_DIR``       — directory of corpus .vcf files.
  * ``MUTMUT_BASELINE_FILE``    — JSON dict ``{filename: fingerprint}``.
  * ``MUTMUT_CORPUS_SAMPLE``    — optional; max number of corpus files
                                  to replay per mutant (default 200 —
                                  deterministic first-N slice).
  * ``MUTMUT_CORPUS_TIMEOUT_S`` — optional; per-file parse timeout
                                  (default 2.0s, implemented via
                                  signal.alarm on POSIX).

A file's fingerprint is a short hash computed from a deterministic
serialisation of the parsed record stream — enough for flipping to
diff-compare in O(n) time but small enough to keep the baseline JSON
tractable even for 1000-file corpora.
"""

from __future__ import annotations

import hashlib
import json
import os
import signal
import sys
from pathlib import Path


def _ensure_vcfpy_on_path() -> None:
    """Prepend the mutable vcfpy parent dir to sys.path so `import vcfpy`
    picks up the mutmut-modified source rather than the venv copy."""
    src = os.environ.get("MUTMUT_VCFPY_SRC")
    if not src:
        return
    # vcfpy lives as a package directory — its parent is what sys.path needs.
    pkg = Path(src).resolve()
    parent = str(pkg.parent)
    if parent in sys.path:
        return
    sys.path.insert(0, parent)
    # Drop any already-imported vcfpy from sys.modules so re-imports use
    # the mutable source.
    for name in list(sys.modules):
        if name == "vcfpy" or name.startswith("vcfpy."):
            del sys.modules[name]


class _TimeoutError(Exception):
    pass


def _alarm_handler(_signum, _frame):  # pragma: no cover — POSIX only
    raise _TimeoutError("per-file parse exceeded MUTMUT_CORPUS_TIMEOUT_S")


def _sample_corpus_files(corpus_dir: Path, max_n: int) -> list[Path]:
    """Return a deterministic first-N slice of the corpus sorted by name.
    Deterministic so the baseline captured at time T0 matches whatever
    mutmut sees later even if new files are added."""
    files = sorted(p for p in corpus_dir.iterdir() if p.is_file())
    return files[:max_n]


def _fingerprint_for_file(path: Path, timeout_s: float) -> str:
    """Coarse, counting-only fingerprint matching
    ``test_vcfpy_corpus.py::_fingerprint_for_file`` byte-for-byte.

    Earlier revisions hashed ``repr(record)`` which made the
    fingerprint sensitive to insertion-order / method-binding drift
    from mutmut's trampoline rewrite even when MUTANT_UNDER_TEST was
    empty. We instead count integer aggregates across the parsed
    stream — each is invariant under mutmut's always-call-orig path
    (so the baseline matches stats-phase exactly) but flips on any
    mutation that changes record count / INFO-keyset cardinality /
    POS math / exception class — which is the signal we want.
    """
    import vcfpy  # noqa: E402 — imports after _ensure_vcfpy_on_path

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
        except BaseException as exc:  # parser refused the file
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
                    # Atheris corpora commonly slip past .from_path
                    # but trip vcfpy asserts mid-iteration (malformed
                    # GT, overflow in POS, bogus types). The exception
                    # class itself is the signal — a mutation that
                    # changes rejection semantics (e.g. AssertionError
                    # → ValueError) flips the fingerprint here.
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
            except Exception:
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


def _run_baseline(corpus_dir: Path, baseline_file: Path, sample_n: int,
                  timeout_s: float) -> int:
    """Write `{filename: fingerprint}` JSON of the unmutated vcfpy."""
    _ensure_vcfpy_on_path()
    out: dict[str, str] = {}
    for f in _sample_corpus_files(corpus_dir, sample_n):
        out[f.name] = _fingerprint_for_file(f, timeout_s)
    baseline_file.parent.mkdir(parents=True, exist_ok=True)
    baseline_file.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[baseline] wrote {len(out)} entries to {baseline_file}")
    return 0


def _run_check(corpus_dir: Path, baseline_file: Path, sample_n: int,
               timeout_s: float) -> int:
    """Compare mutated vcfpy output vs. baseline. Exit 1 on first flip."""
    if not baseline_file.exists():
        # mutmut's "no tests" exit code — baseline missing means the
        # driver hasn't prepared this cell yet.
        print(f"[check] baseline missing: {baseline_file}", file=sys.stderr)
        return 33
    baseline = json.loads(baseline_file.read_text(encoding="utf-8"))
    _ensure_vcfpy_on_path()
    for f in _sample_corpus_files(corpus_dir, sample_n):
        if f.name not in baseline:
            continue
        fp = _fingerprint_for_file(f, timeout_s)
        if fp != baseline[f.name]:
            # Killed! Print once so mutmut's log shows which file flipped.
            print(f"[check] KILL {f.name}: baseline={baseline[f.name][:12]} "
                  f"mutant={fp[:12]}", file=sys.stderr)
            return 1
    return 0


def main() -> int:
    mode = os.environ.get("MUTMUT_RUNNER_MODE", "check").lower()
    corpus = Path(os.environ.get("MUTMUT_CORPUS_DIR", "")).resolve()
    baseline = Path(os.environ.get("MUTMUT_BASELINE_FILE", "")).resolve()
    sample_n = int(os.environ.get("MUTMUT_CORPUS_SAMPLE", "200"))
    timeout_s = float(os.environ.get("MUTMUT_CORPUS_TIMEOUT_S", "2.0"))

    if not corpus.exists() or not corpus.is_dir():
        print(f"[runner] MUTMUT_CORPUS_DIR invalid: {corpus}", file=sys.stderr)
        return 2

    if mode == "baseline":
        return _run_baseline(corpus, baseline, sample_n, timeout_s)
    return _run_check(corpus, baseline, sample_n, timeout_s)


if __name__ == "__main__":
    raise SystemExit(main())
