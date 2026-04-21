"""Re-derive Phase-3 summary.json files from mutmut's SQLite cache.

Used as a post-hoc fix when the mutmut `mutmut results` text output
missed the killed count (mutmut 2.5.1 hides it) but the
`mutmut_cache_backup.sqlite` has the authoritative status.

Usage:

    py -3.12 compares/scripts/mutation/rederive_summaries.py \\
        compares/results/mutation/pure_random_run

Walks each `<cell>/mutmut_cache_backup.sqlite` and rewrites that
cell's `summary.json` with the cache-truth values.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


def _read_sqlite(path: Path) -> dict[str, int]:
    con = sqlite3.connect(str(path))
    rows = con.execute(
        "SELECT status, COUNT(*) FROM Mutant GROUP BY status"
    ).fetchall()
    con.close()
    return {s: int(n) for s, n in rows}


def _derive(raw: dict[str, int]) -> dict:
    killed = raw.get("ok_killed", 0)
    survived = raw.get("bad_survived", 0)
    timeout = raw.get("bad_timeout", 0)
    suspicious = raw.get("ok_suspicious", 0)
    skipped = raw.get("skipped", 0)
    not_checked = raw.get("unknown", 0) + raw.get("not_checked", 0)
    reachable = killed + survived + timeout + suspicious
    total = reachable + skipped + not_checked
    score = (killed / reachable) if reachable else 0.0
    return {
        "killed": killed,
        "survived": survived,
        "timeout": timeout,
        "suspicious": suspicious,
        "skipped": skipped,
        "no_tests": 0,
        "not_checked": not_checked,
        "reachable": reachable,
        "mutant_count": total,
        "score": round(score, 4),
        "score_display": (
            f"{score * 100:.2f}%" if reachable else "n/a (reachable=0)"
        ),
        "raw_status_counts": raw,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: rederive_summaries.py <matrix_dir>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    rewrote = 0
    for cache in sorted(root.rglob("mutmut_cache_backup.sqlite")):
        cell_dir = cache.parent
        summary = cell_dir / "summary.json"
        if not summary.exists():
            continue
        raw = _read_sqlite(cache)
        if not raw:
            continue
        base = json.loads(summary.read_text(encoding="utf-8"))
        base.update(_derive(raw))
        summary.write_text(json.dumps(base, indent=2), encoding="utf-8")
        rewrote += 1
        print(f"rewrote {summary}  killed={base['killed']}  "
              f"reachable={base['reachable']}  score={base['score_display']}")
    print(f"\n{rewrote} summary.json file(s) rederived.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
