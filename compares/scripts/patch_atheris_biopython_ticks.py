"""Post-process patch for atheris × biopython rep directories whose
final tick was dropped to the libFuzzer-shutdown race (pre-fix to
`fuzz_biopython.py._finalize`).

Reads each `run_<N>/.coverage` SQLite snapshot, computes the missing
tick's `line_pct` / `branch_pct` against `Bio.Align.sam` using the
same logic the harness's `_compute_pct` now carries, then back-patches
`run_<N>/harness_growth.json` and `growth_<N>.json` in place.

Idempotent — skipping reps whose tick set is already complete.

Usage:

    python3.12 compares/scripts/patch_atheris_biopython_ticks.py \\
        --out compares/results/coverage/atheris/biopython/ \\
        --ticks 1,10,60,300
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

logger = logging.getLogger("patch_atheris_biopython_ticks")


def _pct_in_docker(coverage_file: Path, image: str) -> tuple[float | None, float | None,
                                                             int, int, int, int]:
    """Compute coverage stats for Bio.Align.sam using the atheris-venv's
    coverage.py. Shells out to docker because the repo-host Python 3.12
    can't read a .coverage file created by Python 3.11 (the file format
    is version-pinned)."""
    rel = coverage_file.resolve().relative_to(REPO_ROOT.resolve())
    in_ctr = "/work/" + rel.as_posix()
    code = (
        "import io, json, coverage\n"
        f"c = coverage.Coverage(data_file='{in_ctr}', source=['Bio.Align.sam'], branch=True, config_file=False)\n"
        "try:\n"
        "    c.load()\n"
        "except Exception:\n"
        "    print(json.dumps({'ok': False, 'error': 'load_failed'}))\n"
        "    raise SystemExit(0)\n"
        "d = c.get_data()\n"
        "covered_lines = missing_lines = 0\n"
        "covered_branches = total_branches = 0\n"
        "for fname in d.measured_files():\n"
        "    norm = fname.replace('\\\\', '/')\n"
        "    if 'Bio/Align/sam' not in norm:\n"
        "        continue\n"
        "    _, statements, _excluded, missing, *_ = c.analysis2(fname)\n"
        "    covered_lines += len(statements) - len(missing)\n"
        "    missing_lines += len(missing)\n"
        "    if d.has_arcs():\n"
        "        arcs = d.arcs(fname) or []\n"
        "        covered_branches += len(arcs)\n"
        "        total_branches += max(len(arcs), 2 * len(statements))\n"
        "total_lines = covered_lines + missing_lines\n"
        "line_pct = (covered_lines / total_lines * 100.0) if total_lines else None\n"
        "branch_pct = (covered_branches / total_branches * 100.0) if total_branches else None\n"
        "print(json.dumps({'ok': True, 'line_pct': line_pct, 'branch_pct': branch_pct, "
        "'covered_lines': covered_lines, 'total_lines': total_lines, "
        "'covered_branches': covered_branches, 'total_branches': total_branches}))\n"
    )

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{REPO_ROOT}:/work",
        "-w", "/work",
        image,
        "/opt/atheris-venv/bin/python", "-c", code,
    ]
    env = {"MSYS_NO_PATHCONV": "1"}
    r = subprocess.run(cmd, capture_output=True, text=True, env={**__import__("os").environ, **env})
    if r.returncode != 0:
        logger.warning("docker compute failed rc=%s stderr=%s",
                       r.returncode, r.stderr[:300])
        return None, None, 0, 0, 0, 0
    try:
        out = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as exc:
        logger.warning("couldn't parse docker output: %s / %r", exc, r.stdout[:300])
        return None, None, 0, 0, 0, 0
    if not out.get("ok"):
        return None, None, 0, 0, 0, 0
    return (out["line_pct"], out["branch_pct"],
            out["covered_lines"], out["total_lines"],
            out["covered_branches"], out["total_branches"])


def patch_rep(rep_dir: Path, ticks: list[int], docker_image: str) -> int:
    """Back-patch tick(s) in harness_growth.json + growth_<n>.json from
    the saved .coverage file. Returns number of ticks added."""
    hg = rep_dir / "harness_growth.json"
    cov = rep_dir / ".coverage"
    if not hg.exists() or not cov.exists():
        logger.info("rep %s: missing %s or .coverage — skipping",
                    rep_dir.name,
                    "harness_growth.json" if not hg.exists() else ".coverage")
        return 0

    payload = json.loads(hg.read_text(encoding="utf-8"))
    recorded = {int(r["t_s"]): r for r in payload.get("coverage_growth", [])
                if r.get("line_pct") is not None}
    to_fill = [t for t in ticks if t not in recorded]
    if not to_fill:
        logger.info("rep %s: all %d tick(s) already recorded",
                    rep_dir.name, len(ticks))
        return 0

    (line_pct, branch_pct,
     cov_lines, tot_lines,
     cov_branches, tot_branches) = _pct_in_docker(cov, docker_image)
    if line_pct is None:
        logger.warning("rep %s: no coverage data; leaving tick(s) %s empty",
                       rep_dir.name, to_fill)
        return 0

    # Wall time for the missing tick: the budget is the harness's
    # original `time_budget_s`, which we can't easily recover from the
    # harness JSON. Use the largest tick as a proxy (accurate for the
    # tick-at-end-of-budget race we actually see).
    for t in to_fill:
        rec = {
            "t_s": t,
            "wall_s": float(t),  # nominal — we don't have the real wall time
            "line_pct": round(line_pct, 2),
            "branch_pct": round(branch_pct, 2),
            "covered_lines": cov_lines,
            "total_lines": tot_lines,
            "covered_branches": cov_branches,
            "total_branches": tot_branches,
            "recovered_from": "post_run_coverage_snapshot",
        }
        # drop any stale null record for this tick
        payload["coverage_growth"] = [
            r for r in payload["coverage_growth"] if int(r["t_s"]) != t
        ]
        payload["coverage_growth"].append(rec)
    # Sort by t_s for determinism
    payload["coverage_growth"].sort(key=lambda r: int(r["t_s"]))
    hg.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("rep %s: back-patched ticks %s (line_pct=%.2f)",
                rep_dir.name, to_fill, line_pct)
    return len(to_fill)


def patch_growth_json(rep_dir: Path, ticks: list[int]) -> int:
    """Re-emit `growth_<idx>.json` (the sampler-level artefact sibling of
    run_<idx>/) using the freshly back-patched harness_growth.json. The
    sampler filters null-pct ticks out; after our patch every requested
    tick has a real pct so the sampler-level JSON can be rebuilt from
    the harness JSON alone."""
    # rep_dir = <out>/run_<n> → growth_<n>.json = <out>/growth_<n>.json
    name = rep_dir.name  # "run_0"
    try:
        idx = int(name.rsplit("_", 1)[1])
    except (IndexError, ValueError):
        logger.warning("rep %s: unrecognised rep-dir name, skipping growth_*.json",
                       rep_dir.name)
        return 0
    growth_file = rep_dir.parent / f"growth_{idx}.json"
    if not growth_file.exists():
        logger.info("no growth_%d.json alongside %s — skipping", idx, rep_dir)
        return 0

    hg = rep_dir / "harness_growth.json"
    hg_payload = json.loads(hg.read_text(encoding="utf-8"))
    g_payload = json.loads(growth_file.read_text(encoding="utf-8"))

    rebuilt = []
    for rec in hg_payload["coverage_growth"]:
        t = int(rec["t_s"])
        lp = rec.get("line_pct")
        bp = rec.get("branch_pct")
        if lp is None:
            continue
        rebuilt.append({
            "t_s": t,
            "line_pct": float(lp),
            "branch_pct": float(bp) if bp is not None else 0.0,
        })
    rebuilt.sort(key=lambda r: r["t_s"])

    g_payload["coverage_growth"] = rebuilt
    growth_file.write_text(json.dumps(g_payload, indent=2), encoding="utf-8")
    logger.info("rewrote %s with %d ticks", growth_file.name, len(rebuilt))
    return len(rebuilt)


def _cli() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True,
                   help="cell output dir (contains run_0/, run_1/, ..., growth_*.json)")
    p.add_argument("--ticks", default="1,10,60,300,1800,7200")
    p.add_argument("--docker-image", default="biotest-bench:latest")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    ticks = sorted({int(x) for x in args.ticks.split(",") if x.strip()})

    total_added = 0
    for rep_dir in sorted(args.out.glob("run_*")):
        if not rep_dir.is_dir():
            continue
        total_added += patch_rep(rep_dir, ticks, args.docker_image)
        patch_growth_json(rep_dir, ticks)

    print(f"[patch] back-filled {total_added} tick record(s) across "
          f"{len(list(args.out.glob('run_*')))} rep(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
