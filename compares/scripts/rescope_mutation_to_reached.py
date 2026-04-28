"""Post-process Phase-3 mutation results to apply DESIGN §3.3's
`reachable = mutants in code the corpus actually executed` scoping.

Reads:
- `<mut_out>/mutants.jsonl`           — per-mutant outcomes (incl. lineno)
- `<cov_dir>/run_0/.coverage`         — the Phase-2 SQLite coverage db
- `<target>`                          — source file that was mutated
                                       (default: Bio/Align/sam.py inside
                                       the atheris-venv)

Writes:
- `<mut_out>/summary_scoped.json`     — refined mutation score using
                                       the executed-line filter
- `<mut_out>/mutants_scoped.jsonl`    — mutants.jsonl with an extra
                                       `on_reached_line` boolean

The refined score follows DESIGN §3.3 literally: `score = killed /
(killed + survived)` where both sets include **only** mutants on lines
the Phase-2 corpus actually executed. Mutants on unreached lines — which
are guaranteed to survive by construction — are excluded from the
denominator so the score reflects oracle power over *tested* code, not
corpus breadth.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
logger = logging.getLogger("rescope_mutation")


def _executed_lines_via_docker(
    coverage_file: Path, module_substr: str, image: str
) -> set[int]:
    """Extract executed line numbers for a given module (substring match) via
    the atheris-venv's coverage.py. Runs inside Docker because the host
    Python 3.12 can't read a Python-3.11-produced .coverage file."""
    rel = coverage_file.resolve().relative_to(REPO_ROOT.resolve())
    code = (
        "import json, sys, coverage\n"
        f"c = coverage.Coverage(data_file='/work/{rel.as_posix()}', source=['Bio.Align.sam'], branch=True, config_file=False)\n"
        "c.load()\n"
        "d = c.get_data()\n"
        "lines = set()\n"
        "for fname in d.measured_files():\n"
        f"    if '{module_substr}' not in fname.replace(chr(92),'/'): continue\n"
        "    _, statements, _exc, missing, *_ = c.analysis2(fname)\n"
        "    lines = set(statements) - set(missing)\n"
        "print(json.dumps(sorted(lines)))\n"
    )
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{REPO_ROOT}:/work",
        "-w", "/work",
        image,
        "/opt/atheris-venv/bin/python", "-c", code,
    ]
    import os
    env = {**os.environ, "MSYS_NO_PATHCONV": "1"}
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
    lines = r.stdout.strip().splitlines()[-1]
    return set(json.loads(lines))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mut-out", type=Path, required=True,
                   help="mutation cell output dir (contains mutants.jsonl + summary.json)")
    p.add_argument("--cov-dir", type=Path, required=True,
                   help="Phase-2 cell dir (contains run_<N>/.coverage)")
    p.add_argument("--cov-rep", type=int, default=0,
                   help="which Phase-2 rep's .coverage to use (default 0)")
    p.add_argument("--module-substr", default="Bio/Align/sam",
                   help="source-file substring filter for line extraction")
    p.add_argument("--docker-image", default="biotest-bench:latest")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    cov_file = args.cov_dir / f"run_{args.cov_rep}" / ".coverage"
    if not cov_file.exists():
        logger.error("coverage file missing: %s", cov_file)
        return 2

    logger.info("extracting executed line set from %s (module=%s)",
                cov_file, args.module_substr)
    reached_lines = _executed_lines_via_docker(
        cov_file, args.module_substr, args.docker_image,
    )
    logger.info("reached %d lines of the SUT module", len(reached_lines))

    jsonl = args.mut_out / "mutants.jsonl"
    if not jsonl.exists():
        logger.error("missing mutants.jsonl: %s", jsonl)
        return 2

    mutants = []
    with jsonl.open(encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln:
                continue
            rec = json.loads(ln)
            rec["on_reached_line"] = rec["lineno"] in reached_lines
            mutants.append(rec)

    killed_all = sum(1 for m in mutants if m["outcome"].startswith("killed"))
    survived_all = sum(1 for m in mutants if m["outcome"] == "survived")
    killed_reached = sum(
        1 for m in mutants
        if m["outcome"].startswith("killed") and m["on_reached_line"]
    )
    survived_reached = sum(
        1 for m in mutants
        if m["outcome"] == "survived" and m["on_reached_line"]
    )
    killed_unreached = killed_all - killed_reached
    survived_unreached = survived_all - survived_reached

    reachable_strict = killed_reached + survived_reached
    score_strict = (killed_reached / reachable_strict) if reachable_strict else 0.0

    # Per-operator breakdown on reached-only
    by_op: dict[str, dict[str, int]] = {}
    for m in mutants:
        if not m["on_reached_line"]:
            continue
        fam_parts = m["operator"].split("_", 2)
        fam = "_".join(fam_parts[:2]) if len(fam_parts) >= 2 else m["operator"]
        bucket = by_op.setdefault(fam, {"killed": 0, "survived": 0})
        if m["outcome"].startswith("killed"):
            bucket["killed"] += 1
        else:
            bucket["survived"] += 1

    summary_path = args.mut_out / "summary_scoped.json"
    prior_summary = json.loads((args.mut_out / "summary.json").read_text(encoding="utf-8"))

    refined = {
        **prior_summary,
        "phase": "mutation_scoped",
        "scope": {
            "mode": "reached-lines-only (DESIGN §3.3)",
            "module_substr": args.module_substr,
            "coverage_file": str(cov_file),
            "total_statements": prior_summary.get("total_generated"),
            "reached_lines": len(reached_lines),
        },
        "mutation_score": {
            "killed": killed_reached,
            "survived": survived_reached,
            "reachable": reachable_strict,
            "score": round(score_strict, 4),
        },
        "mutation_score_unfiltered": prior_summary["mutation_score"],
        "counts_by_scope": {
            "on_reached_line": {
                "killed": killed_reached, "survived": survived_reached,
                "total": reachable_strict,
            },
            "on_unreached_line": {
                "killed": killed_unreached, "survived": survived_unreached,
                "total": killed_unreached + survived_unreached,
            },
        },
        "tested_operators_reached": by_op,
    }
    summary_path.write_text(json.dumps(refined, indent=2), encoding="utf-8")

    jsonl_out = args.mut_out / "mutants_scoped.jsonl"
    with jsonl_out.open("w", encoding="utf-8") as fh:
        for m in mutants:
            fh.write(json.dumps(m) + "\n")

    print(f"[rescope] reached-lines filter: {len(reached_lines)} lines executed")
    print(f"[rescope] mutants on reached lines:   killed={killed_reached} "
          f"survived={survived_reached} reachable={reachable_strict} "
          f"score={score_strict:.4f}")
    print(f"[rescope] mutants on unreached lines: killed={killed_unreached} "
          f"survived={survived_unreached} total={killed_unreached+survived_unreached}")
    print(f"[rescope] wrote {summary_path.name} + {jsonl_out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
