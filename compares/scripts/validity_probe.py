"""Phase-1 validity probe.

Reads a corpus directory of candidate VCF / SAM files, reparses each
one through a target SUT's ParserRunner, and writes a JSON file
summarising how many the SUT accepted.

Per DESIGN.md §3.1 the validity ratio is `parse_success /
generated_total` — fraction of the tool's generated inputs that the
SUT's parser accepts as syntactically / structurally valid. Runs on
any platform because it reuses `test_engine/runners/` (no bcftools or
samtools CLI binary required).

Output schema (DESIGN.md §4.5):

    {
      "tool":             "<derived from corpus path>",
      "sut":              "<arg>",
      "format":           "VCF" | "SAM",
      "validity_ratio":   0.xx,
      "parse_success":    int,
      "generated_total":  int,
      "ineligible_count": int,          # outside SUT's supported_formats
      "timeout_count":    int,
      "crash_count":      int,
      "parse_error_count": int,
      "duration_s":       float,
      "runner":           "<runner class name>",
      "corpus_dir":       "<absolute path>",
    }

Usage:

    python3.12 compares/scripts/validity_probe.py \\
        --corpus compares/results/coverage/jazzer/htsjdk_vcf/corpus \\
        --sut htsjdk --format VCF \\
        --out compares/results/validity/jazzer/htsjdk_vcf/validity.json

    # Smoke-test mode (probe works, without a Phase-2 corpus):
    python3.12 compares/scripts/validity_probe.py \\
        --corpus compares/results/bench_seeds/vcf \\
        --sut vcfpy --format VCF --out /tmp/smoke.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from test_engine.runners.base import ParserRunner  # noqa: E402

logger = logging.getLogger("validity_probe")


# SUT → ParserRunner class, resolved lazily so missing deps on one
# runner don't break the whole script.
SUT_RUNNERS: dict[str, str] = {
    "htsjdk":    "test_engine.runners.htsjdk_runner:HTSJDKRunner",
    "vcfpy":     "test_engine.runners.vcfpy_runner:VcfpyRunner",
    "noodles":   "test_engine.runners.noodles_runner:NoodlesRunner",
    "biopython": "test_engine.runners.biopython_runner:BiopythonRunner",
    "seqan3":    "test_engine.runners.seqan3_runner:SeqAn3Runner",
    "pysam":     "test_engine.runners.pysam_runner:PysamRunner",
    "htslib":    "test_engine.runners.htslib_runner:HTSLibRunner",
}


def _load_runner(sut: str) -> ParserRunner:
    """Import + instantiate the ParserRunner for the given SUT name."""
    if sut not in SUT_RUNNERS:
        raise ValueError(
            f"unknown SUT {sut!r}; known: {sorted(SUT_RUNNERS.keys())}")
    mod_path, cls_name = SUT_RUNNERS[sut].split(":")
    try:
        mod = __import__(mod_path, fromlist=[cls_name])
    except ImportError as e:
        raise RuntimeError(
            f"cannot import runner for {sut}: {e}") from e
    cls = getattr(mod, cls_name)
    return cls()


def _iter_corpus_files(corpus_dir: Path, fmt: str) -> list[Path]:
    """Files in `corpus_dir` that look like the requested format."""
    if not corpus_dir.exists():
        return []
    exts_vcf = (".vcf", ".vcf.gz", ".bcf")
    exts_sam = (".sam", ".bam", ".cram")
    fmt = fmt.upper()
    want = exts_vcf if fmt == "VCF" else exts_sam
    files: list[Path] = []
    for p in sorted(corpus_dir.iterdir()):
        if not p.is_file():
            continue
        name = p.name.lower()
        if any(name.endswith(e) for e in want):
            files.append(p)
    # If nothing matches the extension, fall back to every regular file
    # (adapters often name outputs `rand_0000.vcf` etc. which matches,
    # but some fuzzers emit extension-less `crashes/artefact-<hash>`).
    if not files:
        files = [p for p in sorted(corpus_dir.iterdir()) if p.is_file()]
    return files


def _infer_tool(corpus_dir: Path) -> str:
    """Best-effort: derive the tool name from the adapter path layout
    compares/results/<phase>/<tool>/<sut>[_<fmt>]/corpus/."""
    parts = corpus_dir.resolve().parts
    for i, p in enumerate(parts):
        if p == "coverage" and i + 1 < len(parts):
            return parts[i + 1]
    return corpus_dir.parent.name  # fallback: parent dir name


def probe(
    corpus_dir: Path,
    sut: str,
    fmt: str,
    timeout_s: float = 10.0,
    max_files: int | None = None,
) -> dict[str, Any]:
    """Run the SUT's parser over every file in `corpus_dir`, counting
    successes and error classes."""
    runner = _load_runner(sut)
    if not runner.is_available():
        raise RuntimeError(
            f"runner for {sut!r} is not available on this machine "
            f"(runner.is_available() returned False)")

    files = _iter_corpus_files(corpus_dir, fmt)
    if max_files is not None:
        files = files[:max_files]

    t0 = time.time()
    success = 0
    timeout_n = 0
    crash_n = 0
    parse_error_n = 0
    ineligible_n = 0

    for fp in files:
        try:
            result = runner.run(fp, format_type=fmt, timeout_s=timeout_s)
        except Exception as exc:
            logger.warning("runner exception on %s: %s", fp, exc)
            crash_n += 1
            continue
        if result.success:
            success += 1
        else:
            etype = result.error_type or "parse_error"
            if etype == "timeout":
                timeout_n += 1
            elif etype == "crash":
                crash_n += 1
            elif etype == "ineligible":
                ineligible_n += 1
            else:
                parse_error_n += 1

    total = len(files)
    # Valid denominator excludes "ineligible" — those never should have
    # been routed to this runner in the first place (format mismatch).
    valid_denom = max(total - ineligible_n, 1)
    ratio = success / valid_denom if total else 0.0

    return {
        "tool":              _infer_tool(corpus_dir),
        "sut":               sut,
        "format":            fmt.upper(),
        "validity_ratio":    round(ratio, 6),
        "parse_success":     success,
        "generated_total":   total,
        "ineligible_count":  ineligible_n,
        "timeout_count":     timeout_n,
        "crash_count":       crash_n,
        "parse_error_count": parse_error_n,
        "duration_s":        round(time.time() - t0, 3),
        "runner":            type(runner).__name__,
        "corpus_dir":        str(corpus_dir.resolve()),
    }


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", type=Path, required=True,
                   help="directory of candidate files to reparse")
    p.add_argument("--sut", required=True, choices=sorted(SUT_RUNNERS.keys()))
    p.add_argument("--format", default="VCF", choices=["VCF", "SAM"])
    p.add_argument("--out", type=Path, required=True,
                   help="output validity.json path; parent dir auto-created")
    p.add_argument("--timeout-s", type=float, default=10.0,
                   help="per-file parse timeout in seconds")
    p.add_argument("--max-files", type=int, default=None,
                   help="cap corpus walk to first N files (smoke-test use)")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s %(message)s",
    )

    try:
        result = probe(
            corpus_dir=args.corpus,
            sut=args.sut,
            fmt=args.format,
            timeout_s=args.timeout_s,
            max_files=args.max_files,
        )
    except Exception as exc:
        logger.error("probe failed: %s", exc)
        return 2

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"[validity] {result['tool']:>14} × {result['sut']:<10} "
          f"{result['format']}: "
          f"{result['parse_success']}/{result['generated_total']} "
          f"= {result['validity_ratio']:.1%}  "
          f"(timeout={result['timeout_count']} crash={result['crash_count']} "
          f"parse_error={result['parse_error_count']} "
          f"ineligible={result['ineligible_count']})  "
          f"in {result['duration_s']:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
