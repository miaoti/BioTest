#!/usr/bin/env python3
"""Quick floor-baseline: run pure random against every bug's pre-fix SUT
with the same §5.3.1 detection predicate BioTest's driver now uses.

For each bug:
  1. Install pre-fix SUT.
  2. Generate N random VCF/SAM byte strings via os.urandom.
  3. Run each through the SUT's subprocess predicate.
  4. Collect files that fail on pre-fix.
  5. Install post-fix SUT.
  6. Re-run the failing files; count those that now succeed.
  7. That's the pure-random confirmed-detection count for this bug.

Compare against BioTest's 3/35 to establish an apples-to-apples floor.

Budget: 200 random files × 35 bugs = 7000 parser calls. ~20 min with
subprocess overhead.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _run_pov(sut: str, trig: Path, fmt: str) -> tuple[bool, str]:
    if sut == "vcfpy":
        proc = subprocess.run(
            ["/opt/atheris-venv/bin/python", "-c",
             "import sys, vcfpy\n"
             "try:\n"
             "    with vcfpy.Reader.from_path(sys.argv[1]) as r:\n"
             "        [_ for _ in r]\n"
             "except Exception:\n"
             "    sys.exit(1)\n",
             str(trig)],
            capture_output=True, text=True, timeout=10,
        )
        return proc.returncode == 0, ""
    if sut == "htsjdk":
        from test_engine.runners.htsjdk_runner import HTSJDKRunner
        r = HTSJDKRunner().run(trig, fmt)
        return r.success, r.error_type or ""
    if sut == "biopython":
        from test_engine.runners.biopython_runner import BiopythonRunner
        r = BiopythonRunner().run(trig, fmt)
        return r.success, r.error_type or ""
    if sut == "noodles":
        binary = (_REPO_ROOT / "harnesses" / "rust" / "noodles_harness"
                  / "target" / "release" / "noodles_harness")
        if not binary.exists():
            return False, "binary_missing"
        proc = subprocess.run(
            [str(binary), fmt.upper(), str(trig)],
            capture_output=True, timeout=10,
        )
        return proc.returncode == 0, ""
    if sut == "seqan3":
        from test_engine.runners.seqan3_runner import SeqAn3Runner
        runner = SeqAn3Runner()
        if not runner.is_available():
            return False, "unavailable"
        r = runner.run(trig, fmt)
        return r.success, r.error_type or ""
    return False, "unknown_sut"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path,
                    default=_REPO_ROOT / "compares" / "bug_bench"
                    / "manifest.verified.json")
    ap.add_argument("--n-random", type=int, default=100)
    ap.add_argument("--out", type=Path,
                    default=_REPO_ROOT / "compares" / "results"
                    / "pure_random_baseline.json")
    args = ap.parse_args()

    from compares.scripts.bug_bench_driver import install_sut

    manifest = {b["id"]: b
                for b in json.loads(args.manifest.read_text(encoding="utf-8"))
                                   ["bugs"]}

    rng = random.Random(0xB10)

    # Generate N random VCF/SAM-extension files once; reuse for every bug.
    tmp_dir = _REPO_ROOT / "compares" / "results" / "_random_seeds"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for p in tmp_dir.iterdir():
        p.unlink(missing_ok=True)
    random_seeds_vcf = []
    random_seeds_sam = []
    for i in range(args.n_random):
        size = rng.randint(16, 4096)
        blob = os.urandom(size)
        f = tmp_dir / f"rand_{i:04d}.vcf"
        f.write_bytes(blob)
        random_seeds_vcf.append(f)
        f2 = tmp_dir / f"rand_{i:04d}.sam"
        f2.write_bytes(blob)
        random_seeds_sam.append(f2)

    rows = []
    for bug_id, bug in manifest.items():
        sut = bug["sut"]
        fmt = bug.get("format", "VCF")
        random_seeds = random_seeds_vcf if fmt.upper() == "VCF" else random_seeds_sam

        try:
            install_sut(sut, bug["anchor"], "pre_fix")
        except Exception as e:
            rows.append({"bug_id": bug_id, "skip": f"pre_fix install failed"})
            continue

        # Find random seeds the pre-fix SUT rejects.
        pre_fail = []
        for rs in random_seeds:
            ok, _ = _run_pov(sut, rs, fmt)
            if not ok:
                pre_fail.append(rs)

        if not pre_fail:
            rows.append({"bug_id": bug_id, "pre_fail_count": 0, "confirmed": 0})
            print(f"{bug_id:<25} sut={sut:<10} pre_fail=0  confirmed=0")
            continue

        # Install post_fix, re-run pre_fail to see which silence.
        try:
            install_sut(sut, bug["anchor"], "post_fix")
        except Exception as e:
            rows.append({"bug_id": bug_id,
                         "pre_fail_count": len(pre_fail),
                         "skip_post": "install failed"})
            continue
        silenced_count = 0
        for rs in pre_fail:
            ok, _ = _run_pov(sut, rs, fmt)
            if ok:
                silenced_count += 1
        rows.append({"bug_id": bug_id,
                     "pre_fail_count": len(pre_fail),
                     "confirmed": silenced_count})
        print(f"{bug_id:<25} sut={sut:<10} pre_fail={len(pre_fail):<3d} "
              f"confirmed={silenced_count}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    total_confirmed = sum(1 for r in rows if r.get("confirmed", 0) > 0)
    print()
    print(f"=== pure_random baseline ===")
    print(f"  bugs with at least 1 confirmed trigger: {total_confirmed}/{len(rows)} "
          f"({100*total_confirmed/max(1,len(rows)):.0f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
