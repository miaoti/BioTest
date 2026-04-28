"""Re-parse a mutmut campaign's summary.json from authoritative
artefacts.

mutation_driver.py's inline summariser reads `mutmut results` output,
but on the atheris × vcfpy cell mutmut only prints per-mutant
`name: status` lines for the `no_tests` bucket — killed/survived
counts come out of the spinner line in mutmut_run.log + the per-file
`*.py.meta` DBs. This tool post-processes those authoritative sources
and rewrites the cell's summary.json with the real numbers plus a
per-file breakdown.

Usage:
    py -3.12 compares/scripts/finalize_mutation_summary.py <cell-dir>
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

STATUS_CODE = {
    1: "killed",
    0: "survived",
    5: "no_tests",
    33: "no_tests",
    34: "skipped",
    35: "suspicious",
    36: "timeout",
}

# mutmut's spinner line: "N/TOTAL  🎉 killed 🫥 no_tests  ⏰ timeout
# 🤔 suspicious  🙁 survived". Optional trailing " 🔇 skipped".
_SPINNER_RE = re.compile(
    r"([0-9]+)/([0-9]+)\s+\U0001F389\s+([0-9]+)\s+\U0001FAE5\s+([0-9]+)\s+"
    r"⏰\s+([0-9]+)\s+\U0001F914\s+([0-9]+)\s+\U0001F641\s+([0-9]+)"
    r"(?:\s+\U0001F507\s+([0-9]+))?"
)


def _parse_spinner(log_text: str) -> dict | None:
    hits = _SPINNER_RE.findall(log_text)
    if not hits:
        return None
    done, total, killed, no_tests, timeout, suspicious, survived, skipped = hits[-1]
    return {
        "done": int(done),
        "total": int(total),
        "killed": int(killed),
        "no_tests": int(no_tests),
        "timeout": int(timeout),
        "suspicious": int(suspicious),
        "survived": int(survived),
        "skipped": int(skipped) if skipped else 0,
    }


def _per_file(cell_dir: pathlib.Path) -> tuple[dict, dict]:
    # mutmut 3.x writes mutants under a vcfpy/ subdir of the cwd.
    # The driver's nested-workdir layout puts it at either
    # cell_dir/mutants/vcfpy/ (when cell basename == "vcfpy") or
    # cell_dir/vcfpy/mutants/vcfpy/ (nested workdir).
    cand_roots = [
        cell_dir / "mutants" / "vcfpy",
        cell_dir / "vcfpy" / "mutants" / "vcfpy",
    ]
    root = next((p for p in cand_roots if p.exists()), None)
    if root is None:
        return {}, {}
    per_file: dict[str, dict] = {}
    mutant_count_by_file: dict[str, int] = {}
    for meta in root.glob("*.py.meta"):
        fn = meta.stem.removesuffix(".py")
        d = json.loads(meta.read_text(encoding="utf-8"))
        tally = {k: 0 for k in
                 ("total", "killed", "survived", "no_tests",
                  "timeout", "suspicious", "skipped")}
        for _, code in (d.get("exit_code_by_key") or {}).items():
            tally["total"] += 1
            tally[STATUS_CODE.get(code, "no_tests")] += 1
        reach = tally["killed"] + tally["survived"] + tally["timeout"] + tally["suspicious"]
        tally["reachable"] = reach
        tally["score"] = round(tally["killed"] / reach, 4) if reach else None
        per_file[fn] = tally
        mutant_count_by_file[fn] = tally["total"]
    return dict(sorted(per_file.items())), dict(sorted(mutant_count_by_file.items()))


def finalize(cell_dir: pathlib.Path) -> dict:
    log = cell_dir / "mutmut_run.log"
    summary_path = cell_dir / "summary.json"
    if not log.exists():
        raise SystemExit(f"mutmut_run.log missing under {cell_dir}")
    spinner = _parse_spinner(log.read_text(encoding="utf-8", errors="replace"))
    if spinner is None:
        raise SystemExit(f"no spinner line matched under {log}")

    summary = {}
    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception:
            summary = {}

    reachable = spinner["killed"] + spinner["survived"] + spinner["timeout"] + spinner["suspicious"]
    score = spinner["killed"] / reachable if reachable else 0.0
    per_file, count_by_file = _per_file(cell_dir)

    summary.update({
        "killed": spinner["killed"],
        "survived": spinner["survived"],
        "timeout": spinner["timeout"],
        "suspicious": spinner["suspicious"],
        "no_tests": spinner["no_tests"],
        "skipped": spinner["skipped"],
        "not_checked": spinner["total"] - spinner["done"],
        "reachable": reachable,
        "mutant_count": spinner["total"],
        "done_count": spinner["done"],
        "score": round(score, 4),
        "score_display": f"{score*100:.2f}%" if reachable else "n/a",
        "per_file": per_file,
        "mutant_count_by_file": count_by_file,
    })
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    for arg in sys.argv[1:]:
        cell = pathlib.Path(arg).resolve()
        s = finalize(cell)
        print(f"[finalize] {cell}: score={s['score_display']} "
              f"killed={s['killed']} reach={s['reachable']} "
              f"mut={s['mutant_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
