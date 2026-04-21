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
    """Canonical fingerprint: `hash(ok?|records[POS|REF|ALT|INFO keys]...)`.

    Why not hash the full canonical JSON? Two reasons:
      1. vcfpy's exception paths and field defaults are noisy — we
         only care about signal flips, not exact byte equality.
      2. Hashing a trimmed record stream is cheaper and still flips
         reliably on any semantically-meaningful mutation
         (wrong POS, wrong ALT count, wrong INFO keyset, raised
         exception class).
    """
    import vcfpy  # noqa: E402 — imports after _ensure_vcfpy_on_path

    h = hashlib.sha1()
    if os.name == "posix":
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_s)
    try:
        try:
            reader = vcfpy.Reader.from_path(str(path))
        except BaseException as exc:  # parser refused the file
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
                if i >= 200:  # cap per-file work
                    h.update(b"|cap")
                    break
        finally:
            try:
                reader.close()
            except Exception:
                pass
    except _TimeoutError:
        return hashlib.sha1(b"timeout").hexdigest()
    finally:
        if os.name == "posix":
            signal.setitimer(signal.ITIMER_REAL, 0)
    return h.hexdigest()


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
