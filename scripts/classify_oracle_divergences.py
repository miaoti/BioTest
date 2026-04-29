#!/usr/bin/env python3
"""Enumerate every category of voter disagreement on correct inputs.

Runs each VCF seed (or SAM, per ``--format``) through every available
voter; applies post-normalize + strip_to_strict; and for every seed
where consensus fails, records the *specific* pairwise diff paths.
Output is a frequency table: how often does each diff-path key show
up across the corpus, sorted descending. That tells us which rules
to add to the post-normalizer next.

Usage::
    py -3.12 scripts/classify_oracle_divergences.py --format VCF --strict
    py -3.12 scripts/classify_oracle_divergences.py --format SAM --strict
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from test_engine.canonical.post_normalize import post_normalize  # noqa: E402
from test_engine.oracles.tolerance import strip_to_strict  # noqa: E402


def _vcf_voters():
    from test_engine.runners.htsjdk_runner import HTSJDKRunner
    from test_engine.runners.vcfpy_runner import VcfpyRunner
    from test_engine.runners.pysam_runner import PysamRunner
    from test_engine.runners.reference_runner import ReferenceRunner
    voters = {
        "htsjdk": HTSJDKRunner(),
        "vcfpy": VcfpyRunner(),
        "pysam": PysamRunner(),
        "reference": ReferenceRunner(),
    }
    return {n: r for n, r in voters.items() if r.is_available()}


def _sam_voters():
    from test_engine.runners.htsjdk_runner import HTSJDKRunner
    from test_engine.runners.biopython_runner import BiopythonRunner
    from test_engine.runners.seqan3_runner import SeqAn3Runner
    from test_engine.runners.pysam_runner import PysamRunner
    from test_engine.runners.htslib_runner import HTSlibRunner
    from test_engine.runners.reference_runner import ReferenceRunner
    voters = {
        "htsjdk": HTSJDKRunner(),
        "biopython": BiopythonRunner(),
        "seqan3": SeqAn3Runner(),
        "pysam": PysamRunner(),
        "htslib": HTSlibRunner(),
        "reference": ReferenceRunner(),
    }
    return {n: r for n, r in voters.items() if r.is_available()}


def _normalize_path_for_bucket(path: str) -> str:
    """Collapse record / sample indices so similar diffs cluster.
    e.g. ``.records[37].INFO.DP`` → ``.records[*].INFO.DP``.
    """
    import re
    path = re.sub(r"\[\d+\]", "[*]", path)
    return path


def _collect_diff_paths(a, b, path: str = "", out: list | None = None) -> list:
    """Return a list of diff-path strings (not values), clustered by
    ``_normalize_path_for_bucket``.
    """
    if out is None:
        out = []
    if type(a).__name__ != type(b).__name__ and not (
        isinstance(a, (int, float)) and isinstance(b, (int, float))
    ):
        out.append(_normalize_path_for_bucket(path) + " :type-mismatch")
        return out
    if isinstance(a, dict):
        keys = set(a) | set(b)
        for k in sorted(keys):
            if k not in a:
                out.append(_normalize_path_for_bucket(f"{path}.{k}") + " :missing-left")
            elif k not in b:
                out.append(_normalize_path_for_bucket(f"{path}.{k}") + " :missing-right")
            else:
                _collect_diff_paths(a[k], b[k], f"{path}.{k}", out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append(_normalize_path_for_bucket(path) + " :len-mismatch")
            return out
        for i, (x, y) in enumerate(zip(a, b)):
            _collect_diff_paths(x, y, f"{path}[{i}]", out)
    else:
        if a != b:
            out.append(_normalize_path_for_bucket(path) + " :value-mismatch")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["VCF", "SAM"], required=True)
    ap.add_argument("--seeds", type=Path, default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--max-seeds", type=int, default=0)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    fmt = args.format
    seed_dir = args.seeds or (_REPO_ROOT / "seeds" / fmt.lower())
    seeds = sorted(seed_dir.glob(f"*.{fmt.lower()}"))
    if args.max_seeds:
        seeds = seeds[: args.max_seeds]

    voters = _vcf_voters() if fmt == "VCF" else _sam_voters()
    print(f"[voters] {sorted(voters.keys())}  [seeds] {len(seeds)}")

    # For each seed: post-normalize all voters, run pairwise diffs,
    # record paths. Cluster by (voter_a, voter_b, normalized_path).
    path_counts: Counter[tuple[str, str, str]] = Counter()
    path_examples: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    per_seed_stats = []

    for seed in seeds:
        outs = {}
        for n, r in voters.items():
            try:
                res = r.run(seed, fmt)
            except Exception:
                continue
            if not res.success:
                continue
            norm = post_normalize(res.canonical_json, fmt)
            if isinstance(norm, dict) and "_unusable" in norm:
                continue
            if args.strict:
                norm = strip_to_strict(norm, fmt)
            outs[n] = norm

        names = sorted(outs.keys())
        stat = {"seed": seed.name, "voters": names, "diffs_by_pair": {}}
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                diffs = _collect_diff_paths(outs[a], outs[b])
                stat["diffs_by_pair"][f"{a}|{b}"] = len(diffs)
                for d in diffs:
                    k = (a, b, d)
                    path_counts[k] += 1
                    if len(path_examples[k]) < 3:
                        path_examples[k].append(seed.name)
        per_seed_stats.append(stat)

    # Aggregate by path (across voter pairs)
    per_path: Counter[str] = Counter()
    for (a, b, d), n in path_counts.items():
        per_path[d] += n

    print()
    print(f"=== Top diff-path keys across all voter pairs (total pairs=0..~{len(voters)*(len(voters)-1)//2} × {len(seeds)} seeds) ===")
    for d, n in per_path.most_common(40):
        print(f"  {n:>5d}  {d}")

    print()
    print("=== Top per-voter-pair diff keys ===")
    pair_totals: Counter[tuple[str, str]] = Counter()
    for (a, b, d), n in path_counts.items():
        pair_totals[(a, b)] += n
    for (a, b), total in pair_totals.most_common():
        print(f"\n[{a} vs {b}]  total diff count = {total}")
        items = sorted(
            ((d, path_counts[(a, b, d)]) for (aa, bb, d) in path_counts
             if aa == a and bb == b),
            key=lambda x: -x[1],
        )
        for d, n in items[:15]:
            examples = ", ".join(path_examples[(a, b, d)][:2])
            print(f"    {n:>4d}  {d}   <e.g. {examples}>")

    out_path = args.out or (_REPO_ROOT / "compares" / "results"
                            / f"oracle_divergences_{fmt.lower()}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({
            "format": fmt,
            "voters": sorted(voters.keys()),
            "seeds_count": len(seeds),
            "strict": args.strict,
            "top_paths": [(d, n) for d, n in per_path.most_common(60)],
            "pair_totals": {f"{a}|{b}": n for (a, b), n in pair_totals.items()},
            "per_seed": per_seed_stats,
        }, indent=2),
        encoding="utf-8",
    )
    print(f"\n[wrote] {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
