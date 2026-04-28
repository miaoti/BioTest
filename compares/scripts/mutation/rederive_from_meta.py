"""Rederive a mutmut cell's summary.json from the .meta `exit_code_by_key` files.

`_summarise_mutmut_output` in mutation_driver.py parses mutmut's text
report which (in v3.x) lists only `no tests` entries — killed/survived
counts are missing. The authoritative truth lives in each mutated
module's `<module>.py.meta` under
`mutants/<package>/<module>.py.meta`'s `exit_code_by_key` dict:

    exit 0  = pytest passed           = mutant SURVIVED  (baseline test still green)
    exit 1  = pytest failed (assert)  = mutant KILLED    (corpus flipped a fingerprint)
    exit 33 = pytest collection error = mutant had NO TESTS (unreachable)

Cross-checked against the atheris/vcfpy summary.json which was
pre-produced with correct counts (killed=852, survived=99, no_tests=1387)
— exit-code tallies match exactly.

Usage:

    py -3.12 compares/scripts/mutation/rederive_from_meta.py \\
        compares/results/mutation/biotest/vcfpy \\
        --package vcfpy
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path


def _tally(cell_dir: Path, package: str) -> Counter:
    base = cell_dir / "mutants" / package
    codes: Counter = Counter()
    for mf in base.glob("*.py.meta"):
        try:
            d = json.loads(mf.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for _k, c in d.get("exit_code_by_key", {}).items():
            codes[c] += 1
    return codes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cell_dir", type=Path)
    ap.add_argument("--package", default="vcfpy")
    args = ap.parse_args()

    cell = args.cell_dir.resolve()
    summary_path = cell / "summary.json"
    if not summary_path.exists():
        print(f"[rederive] missing {summary_path}", flush=True)
        return 2

    codes = _tally(cell, args.package)
    killed = codes.get(1, 0)          # test failed = killed
    survived = codes.get(0, 0)        # test passed = survived (mutant indistinguishable)
    no_tests = codes.get(33, 0)       # collection error = no_tests
    # Non-standard exit codes: treat as suspicious/other.
    other = {int(k): v for k, v in codes.items() if k not in (0, 1, 33)}
    reachable = killed + survived
    score = (killed / reachable) if reachable else 0.0
    total = reachable + no_tests + sum(other.values())

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary.update({
        "killed": killed,
        "survived": survived,
        "timeout": other.get(124, 0),
        "suspicious": 0,
        "skipped": 0,
        "no_tests": no_tests,
        "not_checked": 0,
        "reachable": reachable,
        "mutant_count": total,
        "score": round(score, 4),
        "score_display": f"{score * 100:.2f}%" if reachable else "n/a",
        "raw_status_counts": {str(k): v for k, v in codes.items()},
        "rederive_source": "mutants/{pkg}/*.py.meta exit_code_by_key".format(pkg=args.package),
    })
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[rederive] {summary_path}  killed={killed}/{reachable}  "
          f"score={summary['score_display']}  no_tests={no_tests}  total={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
