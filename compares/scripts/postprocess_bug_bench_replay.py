#!/usr/bin/env python3
"""Re-run the silence-on-fix replay step for bug_bench cells that were
written with ``confirmed_fix_silences_signal`` set to ``None`` or
``False`` due to driver bugs that have since been patched:

  * ``UnboundLocalError: local 'subprocess'`` on the vcfpy branch —
    fixed by removing a shadowing local ``import subprocess`` inside
    the noodles branch (see bug_bench_driver.py:_replay_trigger_silenced).
  * noodles binary was invoked as ``noodles_harness <trig_path>`` instead
    of ``noodles_harness <FMT> <trig_path>`` — harness always errored out
    and every replay looked like "post-fix still crashes". Fixed.

Usage (inside biotest-bench:latest, with Rust toolchain on PATH)::

    python3.12 compares/scripts/postprocess_bug_bench_replay.py \\
        --manifest compares/bug_bench/manifest.vcf_only.json \\
        --results-dir compares/results/bug_bench/biotest \\
        --only-sut vcfpy noodles

For each cell where ``detected`` is true but ``confirmed_fix_silences_signal``
is not ``True``, install the post-fix SUT once per anchor group and
replay the first trigger file under ``crashes/``. Rewrites
``result.json`` in place. The original result is preserved under
``result.json.pre_postprocess`` for audit.
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


def _load_cells(results_dir: Path) -> list[tuple[str, Path, dict]]:
    out = []
    for cell_dir in sorted(results_dir.iterdir()):
        r = cell_dir / "result.json"
        if not r.exists():
            continue
        rec = json.loads(r.read_text(encoding="utf-8"))
        out.append((cell_dir.name, cell_dir, rec))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--results-dir", type=Path, required=True)
    ap.add_argument("--only-sut", nargs="+", default=None)
    args = ap.parse_args()

    manifest = _load_manifest(args.manifest)
    cells = _load_cells(args.results_dir)

    # Pick the cells that need re-replay.
    needs_replay: list[tuple[str, Path, dict, dict]] = []
    for bug_id, cell_dir, rec in cells:
        if args.only_sut and rec.get("sut") not in args.only_sut:
            continue
        if not rec.get("detected"):
            continue
        if rec.get("confirmed_fix_silences_signal") is True:
            continue  # already confirmed-correctly, skip
        bug = manifest.get(bug_id)
        if bug is None:
            print(f"[skip] {bug_id}: not in manifest")
            continue
        needs_replay.append((bug_id, cell_dir, rec, bug))

    if not needs_replay:
        print("Nothing to re-replay.")
        return 0

    # Group by (sut, post_fix) so we install each post_fix once.
    groups: dict[tuple[str, str], list] = defaultdict(list)
    for bug_id, cell_dir, rec, bug in needs_replay:
        k = (bug["sut"], bug["anchor"]["post_fix"])
        groups[k].append((bug_id, cell_dir, rec, bug))

    print(f"[replay] {len(needs_replay)} cell(s) in {len(groups)} group(s)")

    for (sut, post_fix), members in groups.items():
        print(f"\n[group] {sut}  post_fix={post_fix}  ({len(members)} cell(s))")
        try:
            install_sut(sut, members[0][3]["anchor"], "post_fix")
        except Exception as e:
            print(f"  install failed: {type(e).__name__}: {str(e)[:200]}")
            # Leave these cells with their existing confirmed=None/False.
            continue

        for bug_id, cell_dir, rec, bug in members:
            # First trigger file under crashes/ — the adapter harvests
            # transformed seeds here as parseable VCF/SAM.
            crashes_dir = cell_dir / "crashes"
            triggers = sorted(p for p in crashes_dir.iterdir() if p.is_file())
            if not triggers:
                print(f"  [skip] {bug_id}: no trigger file under crashes/")
                continue
            trig = triggers[0]
            fmt = bug.get("format", "VCF")
            try:
                silenced = _replay_trigger_silenced(sut, trig, fmt)
            except Exception as e:
                print(f"  [error] {bug_id}: {type(e).__name__}: "
                      f"{str(e)[:200]}")
                silenced = None

            # Preserve the pre-postprocess record once.
            backup = cell_dir / "result.json.pre_postprocess"
            if not backup.exists():
                backup.write_text(json.dumps(rec, indent=2), encoding="utf-8")

            rec["confirmed_fix_silences_signal"] = silenced
            rec.setdefault("notes", "")
            note = f" [postprocess: re-replayed silence; result={silenced}]"
            if note not in rec["notes"]:
                rec["notes"] += note
            (cell_dir / "result.json").write_text(
                json.dumps(rec, indent=2), encoding="utf-8"
            )
            print(f"  {bug_id}: confirmed={silenced}  trig={trig.name}")

    print("\n[done] postprocess complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
