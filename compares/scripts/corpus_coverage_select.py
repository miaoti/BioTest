"""Coverage-guided corpus selection — greedy set-cover on per-file line coverage.

Motivation (run-6 post-mortem, 2026-04-23):

BioTest's multi-Rank corpus generators produce 200–1000 files per cell, but
many are coverage-redundant from the SUT parser's view. Jazzer/atheris/
cargo-fuzz keep ~200 files because their internal coverage-feedback loop
drops anything that doesn't cover new lines. BioTest has no such feedback
loop at generation time — this script adds it at SELECTION time.

For each candidate corpus file this script runs the SUT's parser (same
entry points Phase 2 measurement and the Phase-3 mutation harness use)
with language-native coverage instrumentation, records the set of lines
the file hits, and greedy-picks the files that collectively cover the
most distinct lines up to a target count.

Zero per-SUT user effort: the instrumentation (`coverage.py`, JaCoCo,
grcov, gcov) already exists in `biotest-bench:latest` for Phase 2 — this
script just invokes it per-file in a loop and does set-cover offline.

Output replaces the `corpus/` directory with a trimmed `corpus_selected/`.
Mutation-score staging in `phase3_*.sh` drivers looks for `corpus_selected/`
first and falls back to `corpus/` if missing.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import logging
import sys
import tempfile
from pathlib import Path
from typing import Callable, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

logger = logging.getLogger("corpus_coverage_select")


# ---------------------------------------------------------------------------
# Per-file line-coverage collectors (one per language)
# ---------------------------------------------------------------------------

def _coverage_vcfpy(file_path: Path) -> set[tuple[str, int]]:
    """Run vcfpy.Reader over file_path, return set of (module, line) hit.

    Pre-import vcfpy (same pattern as _coverage_biopython's numpy/
    Bio.Align) so coverage.py instruments its module correctly on
    repeated probes — coverage cannot retrofit instrumentation on
    modules already in sys.modules when cov.start() is called.
    """
    import vcfpy  # type: ignore  # noqa: F401
    import coverage
    import io
    cov = coverage.Coverage(source=["vcfpy"], data_file=None)
    cov.start()
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        try:
            rdr = vcfpy.Reader.from_stream(io.StringIO(text))
            for _ in rdr:
                pass
            rdr.close()
        except Exception:
            pass
    finally:
        cov.stop()
    hit: set[tuple[str, int]] = set()
    data = cov.get_data()
    for fn in data.measured_files():
        for ln in (data.lines(fn) or []):
            hit.add((fn, ln))
    return hit


def _coverage_biopython(file_path: Path) -> set[tuple[str, int]]:
    """Run Bio.Align.sam.AlignmentIterator over file_path.

    Bio.Align requires numpy to be importable. We pre-import numpy and
    Bio.Align *before* starting coverage so module-init lines don't bias
    the per-file coverage maps — we want only the parse-path lines.
    """
    import numpy  # noqa: F401 — required by Bio.Align at import time
    from Bio.Align import sam as bio_sam  # type: ignore  # noqa: F401
    import coverage
    import io
    cov = coverage.Coverage(source=["Bio.Align.sam"], data_file=None)
    cov.start()
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        try:
            it = bio_sam.AlignmentIterator(io.StringIO(text))
            for _ in it:
                pass
        except Exception:
            pass
    finally:
        cov.stop()
    hit: set[tuple[str, int]] = set()
    data = cov.get_data()
    for fn in data.measured_files():
        for ln in (data.lines(fn) or []):
            hit.add((fn, ln))
    return hit


_COVERAGE_COLLECTORS: dict[tuple[str, str], Callable[[Path], set]] = {
    ("vcfpy",     "VCF"): _coverage_vcfpy,
    ("biopython", "SAM"): _coverage_biopython,
}


def _collector_from_prebuilt_json(json_path: Path):
    """Read a pre-computed per-file coverage JSON produced by an
    external probe (e.g. PerFileCoverageProbe.java for Java SUTs, or
    a grcov post-processor for Rust). Format:

        {"<filename>": ["<symbol>:<line>", ...], ...}

    Each entry becomes the file's coverage-set for greedy set-cover.
    This keeps the Python selection logic identical across languages —
    language-specific probes just produce this JSON shape.
    """
    import json as _json
    data = _json.loads(json_path.read_text(encoding="utf-8"))

    def _probe(file_path: Path) -> set:
        return set(data.get(file_path.name, []))
    return _probe

# NOTE: an outcome-fingerprint fallback (using baseline.json) was
# evaluated for SUTs without a native coverage collector (htsjdk / noodles
# / seqan3). It measured WORSE than full-corpus pass-through on
# htsjdk_vcf (178 kills selected vs 192 unselected, 2026-04-23) because
# ~20 distinct outcomes makes greedy set-cover degrade to near-random.
# Coverage selection is therefore restricted to Python cells where
# coverage.py gives genuine line-level signal.


# ---------------------------------------------------------------------------
# Greedy set-cover
# ---------------------------------------------------------------------------

def greedy_select(
    file_coverage: dict[Path, set],
    target: int,
    prioritise: Optional[list[Path]] = None,
) -> list[Path]:
    """Greedy set-cover: pick files that maximise incremental coverage."""
    covered: set = set()
    picked: list[Path] = []
    pool = dict(file_coverage)

    # Optionally seed with a priority set (e.g. curated primary seeds) —
    # preserves user-curated inputs even if a fuzzed file has strictly
    # larger coverage.
    for p in (prioritise or []):
        if p in pool:
            picked.append(p)
            covered |= pool.pop(p)
        if len(picked) >= target:
            return picked

    while len(picked) < target and pool:
        best = None
        best_gain = 0
        best_lines = None
        for f, lines in pool.items():
            gain = len(lines - covered)
            if gain > best_gain:
                best = f
                best_gain = gain
                best_lines = lines
        if best is None or best_gain == 0:
            # No more file contributes new lines; pool is saturated.
            # Fill to target with arbitrary order for robustness.
            for f in list(pool):
                if len(picked) >= target:
                    break
                picked.append(f)
                pool.pop(f)
            break
        picked.append(best)
        covered |= best_lines
        pool.pop(best)

    return picked


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def select_directory(
    input_dir: Path, output_dir: Path, sut: str, fmt: str,
    target: int = 200, prioritise_prefix: Optional[str] = None,
    prebuilt_coverage_json: Optional[Path] = None,
) -> dict:
    """Walk input_dir, measure per-file coverage, write coverage-maximal
    subset of size `target` to output_dir.

    If `prebuilt_coverage_json` points to a valid JSON file produced by
    a language-specific external probe (e.g. PerFileCoverageProbe.java
    for Java SUTs), we use that directly. Otherwise we look up a
    registered in-process coverage collector (coverage.py for Python
    SUTs).
    """
    fmt_u = fmt.upper()
    if prebuilt_coverage_json is not None and prebuilt_coverage_json.exists():
        collect = _collector_from_prebuilt_json(prebuilt_coverage_json)
    else:
        key = (sut.lower(), fmt_u)
        if key not in _COVERAGE_COLLECTORS:
            raise SystemExit(
                f"corpus_coverage_select: no per-file coverage collector "
                f"for SUT={sut!r}, FMT={fmt_u!r}, and no --prebuilt-json "
                f"supplied. Registered collectors: "
                f"{list(_COVERAGE_COLLECTORS.keys())}"
            )
        collect = _COVERAGE_COLLECTORS[key]
    ext = fmt_u.lower()

    files = sorted(p for p in input_dir.iterdir()
                   if p.is_file() and p.suffix.lower() == f".{ext}")
    if not files:
        raise SystemExit(f"no {ext} files in {input_dir}")

    # Priority = curated primary seeds (non-rank-prefixed filenames).
    priority: list[Path] = []
    _rank_prefixes = ("kept_", "diverse_", "bytefuzz_", "bv_",
                       "struct_", "rawfuzz_")
    if prioritise_prefix is None:
        priority = [f for f in files if not f.name.startswith(_rank_prefixes)]
    else:
        priority = [f for f in files if f.name.startswith(prioritise_prefix)]

    logger.info(
        "selecting from %d files → target=%d, priority=%d",
        len(files), target, len(priority),
    )

    # Per-file coverage
    file_cov: dict[Path, set] = {}
    for i, f in enumerate(files, 1):
        try:
            hit = collect(f)
        except Exception as e:
            logger.warning("coverage probe failed on %s: %s", f.name, e)
            hit = set()
        file_cov[f] = hit
        if i % 25 == 0:
            logger.info("  probed %d/%d (latest cov=%d lines)",
                        i, len(files), len(hit))

    picked = greedy_select(file_cov, target=target, prioritise=priority)
    total_cov = set()
    for f in picked:
        total_cov |= file_cov[f]

    # Materialise output
    output_dir.mkdir(parents=True, exist_ok=True)
    # Clear only same-ext files (don't nuke sibling dirs or baselines).
    for existing in output_dir.glob(f"*.{ext}"):
        existing.unlink()
    for f in picked:
        (output_dir / f.name).write_bytes(f.read_bytes())

    result = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "sut": sut,
        "format": fmt_u,
        "input_count": len(files),
        "target": target,
        "selected_count": len(picked),
        "priority_count": len(priority),
        "total_lines_covered": len(total_cov),
    }
    logger.info("result: %s", result)
    return result


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--sut", required=True)
    p.add_argument("--format", required=True, choices=["VCF", "SAM"])
    p.add_argument("--target", type=int, default=200,
                   help="Target corpus size")
    p.add_argument("--prebuilt-json", type=Path, default=None,
                   help="Pre-computed per-file coverage JSON from an "
                        "external probe (e.g. PerFileCoverageProbe.java "
                        "for Java SUTs).")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    r = select_directory(
        input_dir=args.input.resolve(),
        output_dir=args.output.resolve(),
        sut=args.sut,
        fmt=args.format,
        target=args.target,
        prebuilt_coverage_json=(args.prebuilt_json.resolve()
                                if args.prebuilt_json else None),
    )
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
