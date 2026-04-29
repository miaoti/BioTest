#!/usr/bin/env python3
"""
Copy a diverse subset of the Jazzer-generated SAM / VCF corpus into
BioTest's seed directory.

Why
---
Jazzer is a coverage-guided JVM fuzzer (libFuzzer front-end for Java).
During Phase-2 benchmarking (see
``compares/results/coverage/jazzer/coverage_growth.md``) Jazzer
synthesises byte-level corpora that hit ~25 % line coverage on
htsjdk/SAM in 2 hours — 3.5 pp ahead of BioTest Run 10's 21.9 % / 6.7 h.

Analysis of the per-class coverage gap showed Jazzer's advantage sits
in parser error-reporting and validation paths
(``SAMValidationError*``, ``SAMUtils``, ``SAMRecord`` validation
branches) that file-level metamorphic testing reaches only by
accident. Ingesting a SMALL, STRATIFIED SAMPLE of Jazzer's kept
corpus as BioTest seeds lifts most of that advantage without blowing
up Phase C's O(seeds × MRs × voters × Hypothesis iters) runtime.

Why not ingest all 3 062 files
-------------------------------
BioTest's Phase C runs each seed through every MR and every voter.
Dumping 3 062 seeds in would scale a typical ~5 000-test iteration to
~350 000 tests — days of wall time, most of it redundant because
byte-level mutants tend to cluster near a handful of distinct
structural shapes. A stratified sample of ~30 (the current SAM corpus
size) preserves Jazzer's diversity win while keeping Phase C
tractable. ``measure_coverage.py`` will flag whether the sample was
enough when the next Phase D run lands.

Zero user input
---------------
The Jazzer corpus is already a repo artefact under
``compares/results/coverage/jazzer/htsjdk_sam/run_<N>/corpus/`` (from
the Phase-2 benchmark run recorded in coverage_notes/). This script
does not launch Jazzer, does not need Docker, and does not rely on
any external download. Safe to re-run deterministically — the
sampling uses stable-sorted hash filenames + fixed stratum cuts.

Strategy
--------
1. Enumerate every Jazzer corpus file across the three reps.
2. Dedup by filename (Jazzer names files by their content hash, so
   cross-rep duplicates collapse for free).
3. Bucket by size:
      small   < 500 B   — minimal / single-record files
      medium  500-5000 B — typical records with tags
      large   >= 5000 B  — many-record or unusual-tag files
   Then take ``per_stratum`` files from each bucket, stable-ordered
   by filename so repeated runs always pick the same sample.
4. Write each pick to ``seeds/sam/jazzer_<stratum>_<hash8>.sam``
   so downstream tooling can tell synthetic-seed sources apart.

Usage
-----
    py -3.12 seeds/fetch_jazzer_corpus.py                    # default
    py -3.12 seeds/fetch_jazzer_corpus.py --per-stratum 15   # pick 15 per
    py -3.12 seeds/fetch_jazzer_corpus.py --dry-run          # list only
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_JAZZER_ROOT = (
    _REPO_ROOT / "compares" / "results" / "coverage" / "jazzer" / "htsjdk_sam"
)
_TARGET_DIR = _REPO_ROOT / "seeds" / "sam"


# Stratum cut-offs (bytes). Tweak if Jazzer's size distribution shifts.
_STRATA: tuple[tuple[str, int, int], ...] = (
    ("small", 0, 500),
    ("medium", 500, 5_000),
    ("large", 5_000, 10**9),
)


def _enumerate_corpus() -> list[Path]:
    """Walk every ``run_<N>/corpus/`` directory and return all files."""
    paths: list[Path] = []
    for rep_dir in sorted(_JAZZER_ROOT.glob("run_*/corpus")):
        paths.extend(sorted(rep_dir.iterdir()))
    return paths


def _dedup_by_name(paths: list[Path]) -> list[Path]:
    """Jazzer file names are content-hashes; same-hash across reps = same
    file. Keep the first occurrence, preserving sort order.
    """
    seen: set[str] = set()
    out: list[Path] = []
    for p in paths:
        if p.name in seen:
            continue
        seen.add(p.name)
        out.append(p)
    return out


def _bucket_by_size(paths: list[Path]) -> dict[str, list[Path]]:
    buckets: dict[str, list[Path]] = {name: [] for name, _, _ in _STRATA}
    for p in paths:
        try:
            sz = p.stat().st_size
        except OSError:
            continue
        for name, low, high in _STRATA:
            if low <= sz < high:
                buckets[name].append(p)
                break
    return buckets


def _looks_like_sam(path: Path) -> bool:
    """Sanity check — the first non-blank line starts with ``@`` OR
    the line has ≥ 11 tab-separated columns, AND the ENTIRE file is
    valid UTF-8.

    Rejects:
      - empty files
      - files with embedded NUL bytes
      - files that fail UTF-8 decode (SAM is ASCII, so any UTF-8-
        invalid byte signals Jazzer slipped in a binary / non-text
        mutant that BioTest's Python seed loader will crash on)
    Accepts:
      - Jazzer's *intentional* malformations that still decode as UTF-8
        (the whole point — they exercise parser error paths)
    """
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if not data:
        return False
    if b"\x00" in data:
        return False
    # Full-file UTF-8 check — the SeedCorpus loader reads with encoding="utf-8"
    # and raises on invalid bytes, so anything that fails here would crash
    # Phase C on first encounter. Run 11 hit exactly this (0xff at position 7).
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    first_line = text.split("\n", 1)[0].rstrip("\r")
    if not first_line:
        return False
    if first_line.startswith("@"):
        return True
    return first_line.count("\t") >= 10


def pick_seeds(per_stratum: int) -> list[tuple[str, Path]]:
    """Return a deterministic list of ``(stratum, source_path)`` pairs
    sampled uniformly across the three size strata.
    """
    enumerated = _enumerate_corpus()
    deduped = _dedup_by_name(enumerated)
    buckets = _bucket_by_size(deduped)
    chosen: list[tuple[str, Path]] = []
    for name, _, _ in _STRATA:
        valid = [p for p in buckets[name] if _looks_like_sam(p)]
        chosen.extend((name, p) for p in valid[:per_stratum])
    return chosen


def copy_seeds(
    per_stratum: int = 10,
    dry_run: bool = False,
) -> list[Path]:
    """Sample + copy Jazzer seeds into ``seeds/sam/``.

    Returns the list of destination paths actually written (or
    reported, if ``dry_run``).
    """
    if not _JAZZER_ROOT.exists():
        logger.warning(
            "Jazzer corpus not found at %s — skipping (run the Phase-2 "
            "Jazzer benchmark first or provide a --corpus-root flag).",
            _JAZZER_ROOT,
        )
        return []

    picks = pick_seeds(per_stratum)
    if not picks:
        logger.warning("No usable Jazzer seeds found under %s", _JAZZER_ROOT)
        return []

    written: list[Path] = []
    for stratum, src in picks:
        short_hash = src.name[:8]
        dst = _TARGET_DIR / f"jazzer_{stratum}_{short_hash}.sam"
        if dry_run:
            print(f"[dry-run] {src}  ->  {dst}")
            written.append(dst)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(src, dst)
        written.append(dst)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--per-stratum", type=int, default=10,
        help="Number of seeds to pick from each size stratum (default 10 → "
             "~30 total seeds across small/medium/large).",
    )
    ap.add_argument(
        "--dry-run", action="store_true",
        help="List which files would be copied without writing anything.",
    )
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    written = copy_seeds(per_stratum=args.per_stratum, dry_run=args.dry_run)
    logger.info(
        "%s %d Jazzer seeds under %s",
        "Would copy" if args.dry_run else "Copied", len(written), _TARGET_DIR,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
