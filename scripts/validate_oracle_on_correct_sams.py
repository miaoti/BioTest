#!/usr/bin/env python3
"""Oracle sanity check — SAM version.

Mirrors ``validate_oracle_on_correct_vcfs.py`` for the SAM voter pool
(htsjdk, biopython, seqan3, pysam, htslib, reference).

Usage::
    py -3.12 scripts/validate_oracle_on_correct_sams.py [--strict]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from test_engine.runners.htsjdk_runner import HTSJDKRunner  # noqa: E402
from test_engine.runners.biopython_runner import BiopythonRunner  # noqa: E402
from test_engine.runners.seqan3_runner import SeqAn3Runner  # noqa: E402
from test_engine.runners.pysam_runner import PysamRunner  # noqa: E402
from test_engine.runners.htslib_runner import HTSlibRunner  # noqa: E402
from test_engine.runners.reference_runner import ReferenceRunner  # noqa: E402
from test_engine.canonical.post_normalize import post_normalize  # noqa: E402
from test_engine.oracles.tolerance import strip_to_strict  # noqa: E402


def _canon_hash(payload) -> str:
    if payload is None:
        return "NULL"
    s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def _run_one(runner, path, strict=False):
    try:
        r = runner.run(path, "SAM")
    except Exception as e:
        return f"RAISE:{type(e).__name__}", str(e)[:80], False
    if not r.success:
        return f"ERR:{r.error_type or 'unknown'}", (r.stderr or "")[:80], False
    norm = post_normalize(r.canonical_json, "SAM")
    if isinstance(norm, dict) and "_unusable" in norm:
        return f"UNUSABLE:{norm['_unusable']}", "", False
    if strict:
        norm = strip_to_strict(norm, "SAM")
    return _canon_hash(norm), "", True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=Path, default=_REPO_ROOT / "seeds" / "sam")
    ap.add_argument("--primary", default="htsjdk")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", type=Path,
                    default=_REPO_ROOT / "compares" / "results"
                    / "oracle_validation_sam.json")
    args = ap.parse_args()

    voters = {
        "htsjdk": HTSJDKRunner(),
        "biopython": BiopythonRunner(),
        "seqan3": SeqAn3Runner(),
        "pysam": PysamRunner(),
        "htslib": HTSlibRunner(),
        "reference": ReferenceRunner(),
    }
    voters = {n: r for n, r in voters.items() if r.is_available()}
    print(f"[voters available] {sorted(voters.keys())}")

    seeds = sorted(args.seeds.glob("*.sam"))
    if args.limit > 0:
        seeds = seeds[: args.limit]
    print(f"[seeds] {len(seeds)} files")

    rows = []
    for seed in seeds:
        per_voter = {n: _run_one(r, seed, strict=args.strict)
                     for n, r in voters.items()}
        buckets: dict[str, list[str]] = {}
        for name, (bid, _, ok) in per_voter.items():
            if ok:
                buckets.setdefault(bid, []).append(name)
        primary_bucket = per_voter.get(args.primary, ("MISSING", "", False))[0]
        match_primary = (
            [n for n, (bid, _, ok) in per_voter.items()
             if ok and bid == primary_bucket and n != args.primary]
            if per_voter.get(args.primary, (None, "", False))[2]
            else []
        )
        biggest = max(buckets.values(), key=len, default=[])
        rows.append({
            "seed": seed.name,
            "voters_total": len(voters),
            "voters_ok": sum(1 for _, (_, _, ok) in per_voter.items() if ok),
            "ok_buckets": len(buckets),
            "consensus_size": len(biggest),
            "voters_matching_primary": sorted(match_primary),
        })
        print(f"  {seed.name:<45s} ok={rows[-1]['voters_ok']}/{len(voters)}  "
              f"buckets={rows[-1]['ok_buckets']}  consensus={rows[-1]['consensus_size']}  "
              f"match_primary={','.join(match_primary) or '(none)'}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"primary": args.primary, "seeds": rows}, indent=2),
                        encoding="utf-8")
    n = len(rows)
    with_consensus = sum(1 for r in rows if r["consensus_size"] >= 2)
    all_disagree = sum(1 for r in rows if r["voters_ok"] >= 2
                       and r["ok_buckets"] >= r["voters_ok"])
    with_primary = sum(1 for r in rows if r["voters_matching_primary"])
    print()
    print(f"=== SAM oracle summary ({n} seeds) ===")
    print(f"  {with_consensus}/{n} with consensus of ≥2 voters")
    print(f"  {all_disagree}/{n} with every voter in its own bucket")
    print(f"  {with_primary}/{n} with at least 1 voter matching primary")
    return 0


if __name__ == "__main__":
    sys.exit(main())
