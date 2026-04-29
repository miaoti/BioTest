#!/usr/bin/env python3
"""Oracle sanity check — feed every known-correct VCF seed through
every VCF voter and bucket by canonical-JSON equality.

Hypothesis under test: the differential / consensus oracle can only
flag a "bug" when some voter disagrees with a consensus majority. If
on known-correct input EVERY voter lands in a separate canonical-JSON
bucket (no consensus possible), then Phase-4's detection signal is
dominated by voter-variance-on-valid-input, not real SUT bugs.

For each seed we report:
  - total voters that produced canonical JSON
  - number of distinct canonical-JSON buckets
  - bucket membership
  - how many voters match the primary (config: noodles)

Run inside biotest-bench:latest so every voter is available.

Usage::
    py -3.12 scripts/validate_oracle_on_correct_vcfs.py [--seeds DIR]
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
from test_engine.runners.vcfpy_runner import VcfpyRunner  # noqa: E402
from test_engine.runners.pysam_runner import PysamRunner  # noqa: E402
from test_engine.runners.noodles_runner import NoodlesRunner  # noqa: E402
from test_engine.runners.htslib_runner import HTSlibRunner  # noqa: E402
from test_engine.runners.reference_runner import ReferenceRunner  # noqa: E402
from test_engine.canonical.post_normalize import post_normalize  # noqa: E402
from test_engine.oracles.tolerance import strip_to_strict  # noqa: E402


def _canon_hash(payload) -> str:
    """Stable hash of canonical JSON, ignoring Python dict ordering."""
    if payload is None:
        return "NULL"
    s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def _run_one(
    runner, path: Path, fmt: str = "VCF", strict: bool = False,
) -> tuple[str, str, bool]:
    """Returns (bucket_id, error_summary, success).
    bucket_id = canonical-JSON hash of the *post-normalized* output if
    parsed OK, else 'ERR:<etype>' / 'UNUSABLE:<reason>'.

    When ``strict=True``, additionally strip each record to the
    variant-identity fields (CHROM+POS+REF+ALT) before hashing — this
    is the bucketing key the oracle uses with field_tolerance=True.
    """
    try:
        r = runner.run(path, fmt)
    except Exception as e:
        return f"RAISE:{type(e).__name__}", str(e)[:80], False
    if not r.success:
        return f"ERR:{r.error_type or 'unknown'}", (r.stderr or "")[:80], False
    norm = post_normalize(r.canonical_json, fmt)
    if isinstance(norm, dict) and "_unusable" in norm:
        return f"UNUSABLE:{norm['_unusable']}", "", False
    if strict:
        norm = strip_to_strict(norm, fmt)
    return _canon_hash(norm), "", True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=Path, default=_REPO_ROOT / "seeds" / "vcf")
    ap.add_argument("--primary", default="noodles")
    ap.add_argument("--limit", type=int, default=0,
                    help="Max seeds to process (0 = all)")
    ap.add_argument("--strict", action="store_true",
                    help="Bucket on variant-identity fields only "
                         "(CHROM+POS+REF+ALT). Matches the oracle's "
                         "field_tolerance=True path.")
    ap.add_argument("--out", type=Path,
                    default=_REPO_ROOT / "compares" / "results"
                    / "oracle_validation_vcf.json")
    args = ap.parse_args()

    voters = {
        "htsjdk": HTSJDKRunner(),
        "vcfpy": VcfpyRunner(),
        "pysam": PysamRunner(),
        "noodles": NoodlesRunner(),
        "htslib": HTSlibRunner(),
        "reference": ReferenceRunner(),
    }

    # Prune voters that aren't available in this env.
    voters = {n: r for n, r in voters.items() if r.is_available()}
    print(f"[voters available] {sorted(voters.keys())}")
    if args.primary not in voters:
        print(f"[warn] primary {args.primary!r} not in available voters")

    seeds = sorted(args.seeds.glob("*.vcf"))
    if args.limit > 0:
        seeds = seeds[: args.limit]
    print(f"[seeds] processing {len(seeds)} file(s) under {args.seeds}")

    rows = []
    for seed in seeds:
        per_voter: dict[str, tuple[str, str, bool]] = {}
        for name, runner in voters.items():
            per_voter[name] = _run_one(runner, seed, strict=args.strict)

        # Bucket by canonical-JSON hash (only successful parses group).
        buckets: dict[str, list[str]] = {}
        for name, (bid, _, ok) in per_voter.items():
            if ok:
                buckets.setdefault(bid, []).append(name)
        # Non-success voters go in their own per-error bucket
        err_counter: dict[str, list[str]] = {}
        for name, (bid, _, ok) in per_voter.items():
            if not ok:
                err_counter.setdefault(bid, []).append(name)

        primary_bucket = per_voter.get(args.primary, ("MISSING", "", False))[0]
        match_primary = (
            [n for n, (bid, _, ok) in per_voter.items()
             if ok and bid == primary_bucket and n != args.primary]
            if per_voter.get(args.primary, (None, "", False))[2]
            else []
        )
        biggest_bucket = max(buckets.values(), key=len, default=[])
        rows.append({
            "seed": seed.name,
            "voters_total": len(voters),
            "voters_ok": sum(1 for _, (_, _, ok) in per_voter.items() if ok),
            "ok_buckets": len(buckets),
            "err_buckets": len(err_counter),
            "consensus_size": len(biggest_bucket),
            "consensus_members": sorted(biggest_bucket),
            "primary_bucket": primary_bucket,
            "voters_matching_primary": sorted(match_primary),
            "per_voter": {n: {"bucket": bid, "ok": ok, "err": err}
                          for n, (bid, err, ok) in per_voter.items()},
        })

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"primary": args.primary, "seeds": rows}, indent=2),
        encoding="utf-8",
    )
    print(f"[wrote] {args.out}")

    # Summary table.
    print()
    print(f"{'seed':<50s} {'ok':>3s}/{'tot':<3s}  {'buckets':>8s}  "
          f"{'consensus':>9s}  match_primary")
    for r in rows:
        print(f"  {r['seed']:<48s} {r['voters_ok']:>3d}/{r['voters_total']:<3d}  "
              f"{r['ok_buckets']:>8d}  {r['consensus_size']:>9d}  "
              f"{','.join(r['voters_matching_primary']) or '(none)'}")

    # Aggregate
    print()
    print("=== aggregate ===")
    total = len(rows)
    n_consensus_2plus = sum(1 for r in rows if r["consensus_size"] >= 2)
    n_all_disagree = sum(1 for r in rows
                         if r["ok_buckets"] >= r["voters_ok"]
                         and r["voters_ok"] >= 2)
    primary_has_ally = sum(1 for r in rows
                           if r["voters_matching_primary"])
    print(f"  {total} seeds processed")
    print(f"  {n_consensus_2plus}/{total} have a consensus of >=2 voters")
    print(f"  {n_all_disagree}/{total} have every voter in its own bucket (ORACLE CANNOT FIND CONSENSUS)")
    print(f"  {primary_has_ally}/{total} have at least 1 voter matching primary")
    ok_dist = Counter(r["voters_ok"] for r in rows)
    print(f"  ok-voter distribution: {dict(sorted(ok_dist.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
