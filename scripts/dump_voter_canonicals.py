#!/usr/bin/env python3
"""Dump each VCF voter's canonical-JSON output for a single seed and
diff them pairwise. Follow-on to validate_oracle_on_correct_vcfs.py —
that script shows the oracle can't form a consensus; this one shows
*why* (which fields disagree across voters).

Usage::
    py -3.12 scripts/dump_voter_canonicals.py seeds/vcf/spec_example.vcf
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from test_engine.runners.htsjdk_runner import HTSJDKRunner  # noqa: E402
from test_engine.runners.vcfpy_runner import VcfpyRunner  # noqa: E402
from test_engine.runners.pysam_runner import PysamRunner  # noqa: E402
from test_engine.runners.noodles_runner import NoodlesRunner  # noqa: E402
from test_engine.runners.reference_runner import ReferenceRunner  # noqa: E402
from test_engine.canonical.post_normalize import post_normalize  # noqa: E402


def _collect_diffs(a: dict, b: dict, path: str = "") -> list[str]:
    """Return short human-readable diff lines between two JSON trees."""
    diffs = []
    if type(a) != type(b):
        return [f"{path}: type {type(a).__name__} vs {type(b).__name__}"]
    if isinstance(a, dict):
        all_keys = set(a) | set(b)
        for k in sorted(all_keys):
            if k not in a:
                diffs.append(f"{path}.{k}: MISSING in left")
            elif k not in b:
                diffs.append(f"{path}.{k}: MISSING in right")
            else:
                diffs.extend(_collect_diffs(a[k], b[k], f"{path}.{k}"))
    elif isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"{path}: len {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            diffs.extend(_collect_diffs(x, y, f"{path}[{i}]"))
    else:
        if a != b:
            s = f"{path}: {repr(a)[:40]} vs {repr(b)[:40]}"
            diffs.append(s)
    return diffs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", type=Path)
    ap.add_argument("--out-dir", type=Path, default=_REPO_ROOT / "compares"
                    / "results" / "voter_canonicals")
    args = ap.parse_args()

    voters = {
        "htsjdk": HTSJDKRunner(),
        "vcfpy": VcfpyRunner(),
        "pysam": PysamRunner(),
        "noodles": NoodlesRunner(),
        "reference": ReferenceRunner(),
    }
    voters = {n: r for n, r in voters.items() if r.is_available()}

    outputs = {}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for name, runner in voters.items():
        r = runner.run(args.seed, "VCF")
        if r.success and r.canonical_json is not None:
            normalized = post_normalize(r.canonical_json, "VCF")
            if isinstance(normalized, dict) and "_unusable" in normalized:
                print(f"[{name}] UNUSABLE after post-normalize: "
                      f"{normalized['_unusable']}")
                continue
            outputs[name] = normalized
            out = args.out_dir / f"{args.seed.stem}__{name}.json"
            out.write_text(
                json.dumps(normalized, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            print(f"[{name}] OK  -> {out.name} (post-normalized)")
        else:
            print(f"[{name}] FAILED  error_type={r.error_type}  "
                  f"stderr={(r.stderr or '')[:60]}")

    # Pairwise diffs.
    names = sorted(outputs.keys())
    print()
    print(f"=== Pairwise diffs for {args.seed.name} ({len(names)} voters) ===")
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            diffs = _collect_diffs(outputs[a], outputs[b])
            print(f"\n--- {a}  vs  {b}  ({len(diffs)} diffs) ---")
            for d in diffs[:20]:
                print(f"  {d}")
            if len(diffs) > 20:
                print(f"  ... (+{len(diffs)-20} more)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
