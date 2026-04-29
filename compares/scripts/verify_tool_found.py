"""Post-process: verify whether each cell's BioTest harvested triggers
satisfy §5.3.1 independently of the manifest PoV.

For each (bug_id) under the rerun output dir, walks
`biotest/<bug>/crashes/T_*.{vcf,sam}` and runs the silence-on-fix
predicate on each file in BOTH directions (forward + reverse). A cell
scores tool_found = True iff some T_* trigger satisfies one of:
  - signal(T_*, V_pre) = True  AND signal(T_*, V_post) = False  (forward)
  - signal(T_*, V_pre) = False AND signal(T_*, V_post) = True   (reverse)

Outputs:
  - per-cell summary printed to stdout
  - aggregate JSON at <out_root>/tool_found_audit.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "compares" / "scripts"))

# Reuse the bench's silence predicate so behaviour matches the deployed
# bench exactly. We DO need to install pre_fix and post_fix versions
# between calls — caller orchestrates that.
from bug_bench_driver import _replay_trigger_silenced, install_sut


def _load_manifest():
    return json.loads(
        (REPO / "compares" / "bug_bench" / "manifest.verified.json").read_text()
    )["bugs"]


def _bug_record(manifest, bug_id):
    for b in manifest:
        if b["id"] == bug_id:
            return b
    raise KeyError(bug_id)


def _harvested_triggers(rerun_root: Path, bug_id: str) -> list[Path]:
    crashes = rerun_root / "biotest" / bug_id / "crashes"
    if not crashes.exists():
        return []
    return sorted(p for p in crashes.iterdir() if p.is_file())


def audit_cell(rerun_root: Path, bug_id: str, max_triggers: int = 30) -> dict:
    manifest = _load_manifest()
    bug = _bug_record(manifest, bug_id)
    sut = bug["sut"]
    fmt = bug.get("format", "VCF")

    triggers = _harvested_triggers(rerun_root, bug_id)
    if not triggers:
        return {
            "bug_id": bug_id, "sut": sut, "fmt": fmt,
            "n_triggers": 0,
            "tool_found": False,
            "reason": "no harvested triggers in crashes/",
        }

    # Step 1: install pre_fix, get pre-fix verdict for each trigger
    print(f"[{bug_id}] install pre_fix={bug['anchor']['pre_fix']}", flush=True)
    install_sut(sut, bug["anchor"], "pre_fix")
    pre_results: dict[str, bool | None] = {}
    for trig in triggers[:max_triggers]:
        try:
            v = _replay_trigger_silenced(sut, trig, fmt)
        except Exception as e:
            print(f"  pre_fix replay {trig.name}: ERROR {type(e).__name__}", flush=True)
            v = None
        pre_results[trig.name] = v

    # Step 2: install post_fix, get post-fix verdict for each trigger
    print(f"[{bug_id}] install post_fix={bug['anchor']['post_fix']}", flush=True)
    install_sut(sut, bug["anchor"], "post_fix")
    post_results: dict[str, bool | None] = {}
    for trig in triggers[:max_triggers]:
        try:
            v = _replay_trigger_silenced(sut, trig, fmt)
        except Exception as e:
            print(f"  post_fix replay {trig.name}: ERROR {type(e).__name__}", flush=True)
            v = None
        post_results[trig.name] = v

    # Step 3: classify
    forward_hits = []   # pre fail, post pass = forward §5.3.1
    reverse_hits = []   # pre pass, post fail = reverse §5.3.1
    for name in pre_results:
        pre = pre_results[name]
        post = post_results[name]
        if pre is False and post is True:
            forward_hits.append(name)
        elif pre is True and post is False:
            reverse_hits.append(name)

    tool_found = bool(forward_hits or reverse_hits)
    return {
        "bug_id": bug_id, "sut": sut, "fmt": fmt,
        "n_triggers": len(triggers),
        "n_tested": min(len(triggers), max_triggers),
        "tool_found": tool_found,
        "forward_hits": forward_hits[:5],   # cap log size
        "reverse_hits": reverse_hits[:5],
        "reason": (
            f"forward §5.3.1 on {len(forward_hits)} triggers" if forward_hits else
            f"reverse §5.3.1 on {len(reverse_hits)} triggers" if reverse_hits else
            "no harvested trigger satisfied §5.3.1 in either direction"
        ),
    }


def main():
    if len(sys.argv) < 2:
        print("usage: verify_tool_found.py <rerun_root> [bug_id1 bug_id2 ...]")
        sys.exit(2)

    rerun_root = Path(sys.argv[1]).resolve()
    if not rerun_root.exists():
        print(f"rerun_root does not exist: {rerun_root}", file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) > 2:
        bug_ids = sys.argv[2:]
    else:
        # Auto-discover from biotest/<bug>/ subdirs
        bt = rerun_root / "biotest"
        bug_ids = sorted(p.name for p in bt.iterdir() if p.is_dir()) if bt.exists() else []

    if not bug_ids:
        print("no bug_ids to audit", file=sys.stderr)
        sys.exit(1)

    results = []
    print(f"auditing {len(bug_ids)} cells in {rerun_root}\n")
    for bug_id in bug_ids:
        try:
            r = audit_cell(rerun_root, bug_id)
        except Exception as e:
            print(f"[{bug_id}] AUDIT ERROR: {type(e).__name__}: {e}")
            r = {"bug_id": bug_id, "tool_found": False, "error": str(e)}
        results.append(r)
        print(f"[{r['bug_id']}] tool_found={r.get('tool_found')} "
              f"n_triggers={r.get('n_triggers')} reason={r.get('reason', '')}\n",
              flush=True)

    # Aggregate
    out = rerun_root / "tool_found_audit.json"
    out.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    n_found = sum(1 for r in results if r.get("tool_found"))
    print(f"\n=== Summary ===")
    print(f"  tool_found = {n_found} / {len(results)}")
    print(f"  audit JSON: {out}")


if __name__ == "__main__":
    main()
