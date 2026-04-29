#!/usr/bin/env python3
"""Per-cell audit of the 10 null_silence cells.

For each cell where v6 reported ``detected=True, confirmed_fix_silences_signal=False``:
  1. Install the pre-fix SUT.
  2. Run the canonical PoV through the per-SUT subprocess predicate.
  3. Install the post-fix SUT.
  4. Re-run the PoV.
  5. Record exact exit codes / stderr signatures on both sides.

Output: a table that tells us whether each null_silence is:
  - manifest-anchor-wrong (post-fix release doesn't actually contain the fix)
  - wrapper-blocks-the-bug (our subprocess predicate dispatches around it)
  - genuinely unfixed on the tested version (the fix is in a later release)
  - a real second bug surfacing (worth filing separately)

Run inside biotest-bench:latest.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


UNCONFIRMED = None  # use --all to audit every bug


def _run_pov(sut: str, pov: Path, fmt: str) -> tuple[bool, str]:
    """(success_bool, error_signature). success=True means parser accepted input."""
    if sut == "vcfpy":
        proc = subprocess.run(
            ["/opt/atheris-venv/bin/python", "-c",
             "import sys, vcfpy\n"
             "try:\n"
             "    with vcfpy.Reader.from_path(sys.argv[1]) as r:\n"
             "        [_ for _ in r]\n"
             "except Exception as e:\n"
             "    print(type(e).__name__, ':', str(e)[:160])\n"
             "    sys.exit(1)\n",
             str(pov)],
            capture_output=True, text=True, timeout=30,
        )
        return proc.returncode == 0, (proc.stdout + proc.stderr).strip()[:180]
    if sut == "htsjdk":
        sys.path.insert(0, str(_REPO_ROOT))
        from test_engine.runners.htsjdk_runner import HTSJDKRunner
        r = HTSJDKRunner().run(pov, fmt)
        sig = f"{r.error_type or ''}: {(r.stderr or '')[:160]}"
        return r.success, sig
    if sut == "biopython":
        sys.path.insert(0, str(_REPO_ROOT))
        from test_engine.runners.biopython_runner import BiopythonRunner
        r = BiopythonRunner().run(pov, fmt)
        return r.success, f"{r.error_type or ''}: {(r.stderr or '')[:160]}"
    if sut == "seqan3":
        sys.path.insert(0, str(_REPO_ROOT))
        from test_engine.runners.seqan3_runner import SeqAn3Runner
        runner = SeqAn3Runner()
        if not runner.is_available():
            return False, "binary_missing"
        r = runner.run(pov, fmt)
        return r.success, f"{r.error_type or ''}: {(r.stderr or '')[:160]}"
    if sut == "noodles":
        binary = (_REPO_ROOT / "harnesses" / "rust" / "noodles_harness"
                  / "target" / "release" / "noodles_harness")
        if not binary.exists():
            return False, "binary_missing"
        proc = subprocess.run(
            [str(binary), fmt.upper(), str(pov)],
            capture_output=True, timeout=30,
        )
        return proc.returncode == 0, (proc.stderr.decode(errors="replace") or "")[:180]
    return False, f"unknown_sut:{sut}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path,
                    default=_REPO_ROOT / "compares" / "bug_bench"
                    / "manifest.verified.json")
    ap.add_argument("--out", type=Path,
                    default=_REPO_ROOT / "compares" / "results"
                    / "null_silence_audit.json")
    ap.add_argument("--all", action="store_true",
                    help="Audit every bug in the manifest, not just the 10 unconfirmed")
    ap.add_argument("--ids", nargs="*", default=None)
    args = ap.parse_args()

    from compares.scripts.bug_bench_driver import install_sut

    manifest = {b["id"]: b
                for b in json.loads(args.manifest.read_text(encoding="utf-8"))
                                   ["bugs"]}

    if args.all:
        target_ids = sorted(manifest.keys())
    elif args.ids:
        target_ids = args.ids
    else:
        target_ids = [
            "htsjdk-1418",
            "noodles-241", "noodles-259", "noodles-268", "noodles-300",
            "noodles-339", "noodles-inforay-0.64",
            "vcfpy-127", "vcfpy-145", "vcfpy-gtone-0.13",
        ]

    rows = []
    for bug_id in target_ids:
        if bug_id not in manifest:
            continue
        bug = manifest[bug_id]
        sut = bug["sut"]
        fmt = bug.get("format", "VCF")
        pov = _REPO_ROOT / "compares" / "bug_bench" / "triggers" / bug_id / f"original.{fmt.lower()}"
        if not pov.exists():
            pov = _REPO_ROOT / "compares" / "bug_bench" / "triggers" / bug_id / "original.vcf"
        if not pov.exists():
            rows.append({"bug_id": bug_id, "skip": "no PoV file"})
            continue

        # Install pre-fix
        try:
            install_sut(sut, bug["anchor"], "pre_fix")
        except Exception as e:
            rows.append({"bug_id": bug_id, "skip": f"pre-fix install failed: {e}"})
            continue
        pre_ok, pre_sig = _run_pov(sut, pov, fmt)

        # Install post-fix
        try:
            install_sut(sut, bug["anchor"], "post_fix")
        except Exception as e:
            rows.append({
                "bug_id": bug_id,
                "pre_ok": pre_ok, "pre_sig": pre_sig,
                "skip_post": f"post-fix install failed: {e}",
            })
            continue
        post_ok, post_sig = _run_pov(sut, pov, fmt)

        classification = None
        if pre_ok and post_ok:
            classification = "no_signal_either_side"
        elif pre_ok and not post_ok:
            classification = "regression_introduced"
        elif not pre_ok and post_ok:
            classification = "real_detection_would_confirm"
        elif not pre_ok and not post_ok:
            if pre_sig != post_sig:
                classification = "different_error_still_present_LIKELY_real_bug_in_both"
            else:
                classification = "identical_error_both_sides_LIKELY_anchor_wrong"

        rows.append({
            "bug_id": bug_id, "sut": sut,
            "pre_fix": bug["anchor"].get("pre_fix"),
            "post_fix": bug["anchor"].get("post_fix"),
            "pre_ok": pre_ok, "pre_sig": pre_sig,
            "post_ok": post_ok, "post_sig": post_sig,
            "classification": classification,
        })
        print(f"{bug_id:<22}  pre={pre_ok!s:<5}  post={post_ok!s:<5}  → {classification}")
        print(f"      pre_sig:  {pre_sig[:100]}")
        print(f"      post_sig: {post_sig[:100]}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    print()
    print("=== SUMMARY ===")
    from collections import Counter
    cls = Counter(r.get("classification") or r.get("skip") or "?"
                   for r in rows)
    for k, v in cls.most_common():
        print(f"  {v:>2d}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
