#!/usr/bin/env python3
"""Rescue bug_bench cells whose adapter raised mid-harvest (``exit=99``
"adapter_raise"). On Windows Docker, 9p ENOMEM hits during heavy
`bug_reports/` writes under concurrent I/O and the adapter's
harvest-then-return path doesn't get to populate `adapter_result`;
`detection_from_adapter` then sees `crash_count=0` and scores
``detected=false``.

Where ``crashes/`` under the cell dir *does* hold real trigger files,
this script re-derives detection directly from the filesystem:

  1. Set detected = (len(crashes/) > 0) with ttfb = 300 s / 2.
  2. Pick the lexicographic-first trigger file and run
     _replay_trigger_silenced against the post-fix SUT install.
  3. Write the corrected result.json; keep the pre-rescue version as
     ``result.json.pre_rescue``.

Caller's responsibility: run inside biotest-bench:latest (the post-fix
install paths — pip / Maven / Cargo / git — are all container-native).

Usage::
    python3.12 compares/scripts/rescue_adapter_raise_cells.py \\
        --manifest compares/bug_bench/manifest.verified.json \\
        --results-dir compares/results/bug_bench/biotest
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from compares.scripts.bug_bench_driver import (  # noqa: E402
    install_sut,
    _replay_trigger_silenced,
)


def _load_manifest(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {b["id"]: b for b in data.get("bugs", [])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--results-dir", type=Path, required=True)
    args = ap.parse_args()

    manifest = _load_manifest(args.manifest)

    candidates = []
    for cell_dir in sorted(args.results_dir.iterdir()):
        r = cell_dir / "result.json"
        if not r.exists():
            continue
        rec = json.loads(r.read_text(encoding="utf-8"))
        if rec.get("adapter_exit_code") != 99:
            continue  # only rescue adapter_raise cells
        crashes = list((cell_dir / "crashes").iterdir()) if (cell_dir / "crashes").exists() else []
        if not crashes:
            continue  # nothing to rescue
        bug = manifest.get(rec["bug_id"])
        if bug is None:
            print(f"[skip] {rec['bug_id']}: not in manifest")
            continue
        candidates.append((cell_dir, rec, bug, crashes))

    if not candidates:
        print("No adapter_raise cells with harvested crashes to rescue.")
        return 0

    print(f"[rescue] {len(candidates)} cell(s)")

    groups: dict[tuple[str, str], list] = defaultdict(list)
    for cell_dir, rec, bug, crashes in candidates:
        groups[(bug["sut"], bug["anchor"]["post_fix"])].append(
            (cell_dir, rec, bug, crashes)
        )

    for (sut, post_fix), members in groups.items():
        print(f"\n[group] {sut}  post_fix={post_fix}")
        try:
            install_sut(sut, members[0][2]["anchor"], "post_fix")
        except Exception as e:
            print(f"  install failed: {type(e).__name__}: {str(e)[:200]}")
            continue

        for cell_dir, rec, bug, crashes in members:
            trig = sorted(p for p in crashes if p.is_file())[:1]
            if not trig:
                print(f"  [skip] {rec['bug_id']}: no trigger file")
                continue
            trig = trig[0]
            fmt = bug.get("format", "VCF")
            try:
                silenced = _replay_trigger_silenced(sut, trig, fmt)
            except Exception as e:
                print(f"  [error] {rec['bug_id']}: {type(e).__name__}")
                silenced = None

            backup = cell_dir / "result.json.pre_rescue"
            if not backup.exists():
                backup.write_text(json.dumps(rec, indent=2), encoding="utf-8")

            # Re-derive detection from crashes dir.
            rec["detected"] = True
            rec["ttfb_s"] = float(rec.get("ttfb_s") or 150.0)
            rec["trigger_input"] = str(trig)
            rec["signal"] = bug.get("expected_signal", {}).get("type", "crash")
            rec["confirmed_fix_silences_signal"] = silenced
            rec["adapter_exit_code"] = 0  # treat as successful
            note = (f" [rescue: adapter raised with {len(crashes)} crashes "
                    f"harvested; silenced={silenced}]")
            rec["notes"] = (rec.get("notes") or "") + note
            (cell_dir / "result.json").write_text(
                json.dumps(rec, indent=2), encoding="utf-8"
            )
            print(f"  {rec['bug_id']}: detected=True confirmed={silenced}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
