#!/usr/bin/env python3
"""Audit Phase-4 confirmed detections: for each cell where
``confirmed_fix_silences_signal=True``, re-run the *pre-fix* SUT
against the actual trigger file. If the pre-fix SUT *succeeds*,
then silence-on-fix was vacuously satisfied — the detection is a
false positive (both versions parse the trigger cleanly; the
"differential" was pure cross-voter canonicalization variance,
not a real SUT bug).

DESIGN.md §5.3.1 actually requires:
  detects(T, B) := ∃ I : signal_T(I, V_pre) = true
                        AND signal_T(I, V_post) = false

Our driver only checks V_post silence. Without the V_pre = true
check, every cross-voter canonical-JSON disagreement on *correct*
input scores as a detection. This script fills in the missing half
of the predicate.

Output: JSON report + per-cell classification:
  real_detection     V_pre fails AND V_post succeeds (bug silenced)
  false_positive     V_pre succeeds (no signal to silence)
  still_failing      both V_pre and V_post fail (truly unrelated)
  unknown            replay infra unavailable

Runs inside biotest-bench:latest.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _run_sut(sut: str, trig_path: Path, fmt: str) -> tuple[bool, str]:
    """Returns (success, error_type_or_empty)."""
    fmt = fmt.upper()
    if sut == "htsjdk":
        from test_engine.runners.htsjdk_runner import HTSJDKRunner
        r = HTSJDKRunner().run(trig_path, fmt)
        return r.success, r.error_type or ""
    if sut == "biopython":
        from test_engine.runners.biopython_runner import BiopythonRunner
        r = BiopythonRunner().run(trig_path, fmt)
        return r.success, r.error_type or ""
    if sut == "vcfpy":
        py = "/opt/atheris-venv/bin/python"
        proc = subprocess.run(
            [py, "-c",
             "import sys, vcfpy\n"
             "try:\n"
             "    with vcfpy.Reader.from_path(sys.argv[1]) as r:\n"
             "        [_ for _ in r]\n"
             "except Exception as e:\n"
             "    print(type(e).__name__)\n"
             "    sys.exit(1)\n",
             str(trig_path)],
            capture_output=True, text=True, timeout=30,
        )
        return proc.returncode == 0, (proc.stdout.strip() if proc.returncode else "")
    if sut == "noodles":
        binary = (_REPO_ROOT / "harnesses" / "rust" / "noodles_harness"
                  / "target" / "release" / "noodles_harness")
        if not binary.exists():
            return False, "binary_missing"
        proc = subprocess.run(
            [str(binary), fmt, str(trig_path)],
            capture_output=True, timeout=30,
        )
        return proc.returncode == 0, "" if proc.returncode == 0 else f"rc={proc.returncode}"
    if sut == "seqan3":
        from test_engine.runners.seqan3_runner import SeqAn3Runner
        runner = SeqAn3Runner()
        if not runner.is_available():
            return False, "binary_missing"
        r = runner.run(trig_path, fmt)
        return r.success, r.error_type or ""
    return False, f"unknown_sut:{sut}"


def _install_sut(sut: str, anchor: dict, which: str) -> None:
    from compares.scripts.bug_bench_driver import install_sut
    install_sut(sut, anchor, which)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path,
                    default=_REPO_ROOT / "compares" / "bug_bench"
                    / "manifest.verified.json")
    ap.add_argument("--results-dir", type=Path,
                    default=_REPO_ROOT / "compares" / "results"
                    / "bug_bench" / "biotest")
    ap.add_argument("--out", type=Path,
                    default=_REPO_ROOT / "compares" / "results"
                    / "phase4_audit.json")
    args = ap.parse_args()

    manifest = {b["id"]: b
                for b in json.loads(args.manifest.read_text(encoding="utf-8"))
                                    ["bugs"]}

    # Load confirmed cells.
    cells = []
    for cdir in sorted(args.results_dir.iterdir()):
        r = cdir / "result.json"
        if not r.exists():
            continue
        rec = json.loads(r.read_text(encoding="utf-8"))
        if rec.get("confirmed_fix_silences_signal") is not True:
            continue  # we only audit confirmed detections
        bug = manifest.get(rec["bug_id"])
        if bug is None:
            continue
        cells.append((cdir, rec, bug))

    print(f"[audit] {len(cells)} confirmed cells to re-check")

    # Group by (sut, pre_fix) so we install pre_fix once per group.
    groups = defaultdict(list)
    for cdir, rec, bug in cells:
        k = (bug["sut"], bug["anchor"]["pre_fix"])
        groups[k].append((cdir, rec, bug))

    audit_results = []

    for (sut, pre_fix), members in groups.items():
        print(f"\n[group] {sut}  pre_fix={pre_fix}  ({len(members)} cell(s))")
        try:
            _install_sut(sut, members[0][2]["anchor"], "pre_fix")
        except Exception as e:
            print(f"  install failed: {type(e).__name__}: {str(e)[:100]}")
            for cdir, rec, bug in members:
                audit_results.append({
                    "bug_id": rec["bug_id"],
                    "sut": sut,
                    "classification": "unknown",
                    "reason": f"install pre_fix failed: {e!r}"[:200],
                })
            continue

        for cdir, rec, bug in members:
            # First trigger file (same pick as the driver).
            crashes = cdir / "crashes"
            triggers = sorted(p for p in crashes.iterdir() if p.is_file())
            if not triggers:
                audit_results.append({
                    "bug_id": rec["bug_id"], "sut": sut,
                    "classification": "unknown",
                    "reason": "no trigger file in crashes/",
                })
                continue
            trig = triggers[0]
            fmt = bug.get("format", "VCF")
            try:
                pre_ok, pre_err = _run_sut(sut, trig, fmt)
            except Exception as e:
                audit_results.append({
                    "bug_id": rec["bug_id"], "sut": sut,
                    "classification": "unknown",
                    "reason": f"pre_fix run raised: {type(e).__name__}",
                })
                continue

            if pre_ok:
                cls = "false_positive"
                reason = (f"pre_fix SUT parses trigger cleanly — silence-on-fix "
                          f"was vacuously satisfied")
            else:
                cls = "real_detection"
                reason = f"pre_fix failed with {pre_err!r}"
            audit_results.append({
                "bug_id": rec["bug_id"],
                "sut": sut,
                "classification": cls,
                "pre_fix_succeeds": pre_ok,
                "pre_fix_error": pre_err,
                "trigger": trig.name,
                "reason": reason,
            })
            print(f"  {rec['bug_id']:<25s} pre_fix_ok={pre_ok}  -> {cls}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(audit_results, indent=2), encoding="utf-8")
    print(f"\n[wrote] {args.out}")

    # Summary
    counter = Counter(r["classification"] for r in audit_results)
    print()
    print("=== Audit summary ===")
    print(f"  confirmed cells audited: {len(audit_results)}")
    for k, v in sorted(counter.items()):
        print(f"    {k:<20s} {v}")
    fps = sum(1 for r in audit_results if r["classification"] == "false_positive")
    if len(audit_results):
        print(f"\n  FALSE POSITIVE rate (of confirmed cells): "
              f"{fps}/{len(audit_results)} = "
              f"{100*fps/len(audit_results):.0f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
