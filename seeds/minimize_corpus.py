#!/usr/bin/env python3
"""
Cross-parser union-edge corpus minimization (Phase 6 of SAM coverage plan).

For every seed file under `seeds/{sam,vcf}/` that is NOT a hand-curated
Tier-1 file, run every enabled Python-based parser (biopython reference
normalizer + any installed coverage.py-traceable parser) against the
seed, collect the set of executed source lines per run, and compute a
greedy cover that keeps the minimal seed subset preserving the UNION of
executed lines across all parsers. Pruned seeds are moved to
`seeds/archive/` (still on disk, reversible).

Grounded in:
- Herrera et al., "Seed Selection for Successful Fuzzing", ISSTA 2021.
- Graphuzz, TOSEM 2024 (graph-based seed scheduling).

Tier-1 preservation: operator-chosen invariant. Hand-curated seeds
(anything NOT matching the `real_world_*` / `synthetic_*` pattern)
are walked for coverage contribution but NEVER moved — they stay as
human-legible debugging anchors.

Usage:
  py -3.12 seeds/minimize_corpus.py                        # live
  py -3.12 seeds/minimize_corpus.py --dry-run              # no moves
  py -3.12 seeds/minimize_corpus.py --format SAM           # one format
  py -3.12 seeds/minimize_corpus.py --archive-dir seeds/archive
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


# Only Tier-2 / synthetic seeds are candidates for minimization.
# Tier-1 hand-curated seeds stay on disk unchanged — they're legible
# anchors for human debugging and cross-run reproducibility.
MINIMIZE_SCOPE: frozenset[str] = frozenset({"real_world_", "synthetic_"})


def _is_candidate_for_pruning(path: Path) -> bool:
    """A seed is a minimization candidate iff its filename starts with
    a Tier-2 prefix. Everything else is Tier-1 and kept intact."""
    return any(path.name.startswith(prefix) for prefix in MINIMIZE_SCOPE)


def _collect_seeds(seeds_dir: Path, formats: list[str]) -> list[Path]:
    out: list[Path] = []
    for fmt in formats:
        sub = seeds_dir / fmt.lower()
        if not sub.exists():
            continue
        ext = f"*.{fmt.lower()}"
        out.extend(sorted(sub.glob(ext)))
    return out


def _per_seed_edges(seed: Path, format_: str) -> set[str]:
    """Return the set of `file:line` strings executed while parsing one
    seed through the reference normalizer.

    Tier-2 minimization uses the Python-side normalizer as a proxy for
    "edges this seed exercises". A file that only exercises edges already
    covered by an earlier seed is redundant. The union-edge signal is
    per-SUT-language-agnostic (all SUTs fan out from the same parse of
    the same bytes), so the minimizer stays SUT-generic.
    """
    try:
        import coverage
    except ImportError:
        print(
            "ERROR: coverage.py not installed. Install with `pip install coverage`",
            file=sys.stderr,
        )
        sys.exit(1)

    # Fresh tracer per seed so each run's executed-line set is isolated.
    cov = coverage.Coverage(data_file=None, branch=False)
    cov.start()
    try:
        if format_.upper() == "VCF":
            from test_engine.canonical.vcf_normalizer import normalize_vcf_text
            lines = seed.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
            try:
                normalize_vcf_text(lines)
            except Exception:
                pass
        elif format_.upper() == "SAM":
            if seed.suffix.lower() == ".bam":
                # BAM is binary; text normalizer can't parse it. Count
                # such seeds as "distinct edge" (their own identity) so
                # the minimizer doesn't collapse all BAMs onto one.
                return {f"bam-fingerprint:{seed.name}:{seed.stat().st_size}"}
            from test_engine.canonical.sam_normalizer import normalize_sam_text
            lines = seed.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
            try:
                normalize_sam_text(lines)
            except Exception:
                pass
        else:
            return set()
    finally:
        cov.stop()

    data = cov.get_data()
    edges: set[str] = set()
    for f in data.measured_files():
        # Keep only normalizer-internal lines; the rest is pytest/hypothesis
        # framework noise that every seed shares and thus contributes no signal.
        if "canonical" not in f.replace("\\", "/"):
            continue
        analysis = cov.analysis2(f)
        statements = analysis[1]
        missing = analysis[3]
        executed = set(statements) - set(missing)
        for line in executed:
            edges.add(f"{Path(f).name}:{line}")
    return edges


def _greedy_minimum_cover(
    per_seed_edges: dict[Path, set[str]],
) -> set[Path]:
    """Return the minimal subset of seeds whose union of edges equals the
    union across all seeds. Classic greedy set-cover (Chvátal 1979):
    O(|seeds| * |edges|) but fine for the scale we operate at (<= ~200
    seeds per format).
    """
    all_edges: set[str] = set().union(*per_seed_edges.values())
    remaining_edges = set(all_edges)
    chosen: set[Path] = set()
    candidates = dict(per_seed_edges)

    while remaining_edges and candidates:
        # Pick the seed contributing the most uncovered edges.
        best_seed, best_gain = max(
            candidates.items(),
            key=lambda kv: (len(kv[1] & remaining_edges), -len(kv[1])),
        )
        gain = len(best_gain & remaining_edges)
        if gain == 0:
            break
        chosen.add(best_seed)
        remaining_edges -= best_gain
        del candidates[best_seed]

    return chosen


def _archive_path(seed: Path, seeds_dir: Path, archive_dir: Path) -> Path:
    rel = seed.relative_to(seeds_dir)
    return archive_dir / rel


def minimize(
    seeds_dir: Path,
    archive_dir: Path,
    formats: list[str],
    dry_run: bool,
) -> tuple[int, int, int]:
    """Return (kept_count, pruned_count, tier1_count) across formats."""
    kept = pruned = tier1 = 0
    for fmt in formats:
        fmt_seeds = [
            s for s in _collect_seeds(seeds_dir, [fmt])
        ]
        if not fmt_seeds:
            continue

        candidates = [s for s in fmt_seeds if _is_candidate_for_pruning(s)]
        tier1_seeds = [s for s in fmt_seeds if not _is_candidate_for_pruning(s)]
        tier1 += len(tier1_seeds)

        if not candidates:
            print(f"[{fmt}] no Tier-2 candidates to prune")
            continue

        print(f"[{fmt}] collecting edges from {len(candidates)} Tier-2 seeds "
              f"(Tier-1 kept: {len(tier1_seeds)})")

        per_seed = {s: _per_seed_edges(s, fmt) for s in candidates}

        # Tier-1 seeds also contribute to the edge set "for free" —
        # their edges are pre-covered, so candidates whose edges are
        # wholly within the Tier-1 union are pure redundancy.
        tier1_edges: set[str] = set()
        for t in tier1_seeds:
            tier1_edges |= _per_seed_edges(t, fmt)
        if tier1_edges:
            for s in list(per_seed.keys()):
                per_seed[s] = per_seed[s] - tier1_edges

        chosen = _greedy_minimum_cover(per_seed)
        to_prune = [s for s in candidates if s not in chosen]

        print(f"[{fmt}] Tier-2 kept: {len(chosen)}, pruned: {len(to_prune)}")
        kept += len(chosen)
        pruned += len(to_prune)

        if dry_run:
            for s in to_prune:
                print(f"  [DRY-RUN] would archive: {s.relative_to(seeds_dir)}")
            continue

        for s in to_prune:
            dest = _archive_path(s, seeds_dir, archive_dir)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(s), str(dest))
            print(f"  archived: {s.name} -> {dest.relative_to(archive_dir.parent)}")

    return kept, pruned, tier1


def main():
    p = argparse.ArgumentParser(
        description=(
            "Minimize Tier-2 seed corpus via greedy union-edge cover. "
            "NOTE: edges are measured on the Python reference normalizer "
            "only — a LOWER BOUND for the real cross-SUT edge set. The "
            "tool will prune more aggressively than a full 6-parser run. "
            "Tier-1 hand-curated seeds are NEVER moved. Prefer --dry-run "
            "first and inspect the archival list before going live."
        ),
    )
    p.add_argument("--seeds-dir", default=str(REPO_ROOT / "seeds"))
    p.add_argument("--archive-dir", default=str(REPO_ROOT / "seeds" / "archive"))
    p.add_argument(
        "--format", action="append", dest="formats",
        help="VCF or SAM; may repeat. Default: both.",
    )
    p.add_argument("--dry-run", action="store_true",
                   help="Report moves without touching disk")
    p.add_argument(
        "--i-understand-this-is-an-approximation",
        action="store_true",
        dest="approx_ok",
        help=(
            "Required to actually move files. Without this flag, live runs "
            "(without --dry-run) fail fast so an operator can't accidentally "
            "prune real coverage-contributing seeds based on the lower-bound "
            "Python-normalizer edge set."
        ),
    )
    args = p.parse_args()

    if not args.dry_run and not args.approx_ok:
        print(
            "ERROR: live minimization requires "
            "`--i-understand-this-is-an-approximation`. See --help.",
            file=sys.stderr,
        )
        return 2

    seeds_dir = Path(args.seeds_dir).resolve()
    archive_dir = Path(args.archive_dir).resolve()
    formats = args.formats or ["VCF", "SAM"]

    kept, pruned, tier1 = minimize(
        seeds_dir=seeds_dir,
        archive_dir=archive_dir,
        formats=formats,
        dry_run=args.dry_run,
    )

    print()
    print(f"Summary: Tier-2 kept {kept}, pruned {pruned}, Tier-1 preserved {tier1}")
    if args.dry_run:
        print("[DRY-RUN] No files moved. Re-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
