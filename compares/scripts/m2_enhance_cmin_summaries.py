"""Backfill the per-(cell, rep, strategy) cmin summaries with the
selector-specific stats (buckets / kept_kill_count) parsed from the
corpus_minimize.py log output."""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def parse_log(log_path: Path) -> dict:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    out: dict = {}
    # The log captures the script's tail (15 lines), which includes the
    # final JSON summary line by line.
    for key in ("buckets", "kept_max_kill_count", "kept_mean_kill_count",
                "files_with_zero_kills", "kept", "dropped"):
        m = re.search(rf'"{key}":\s*([0-9.]+)', text)
        if m:
            try:
                out[key] = float(m.group(1)) if "." in m.group(1) else int(m.group(1))
            except ValueError:
                pass
    return out


def main() -> int:
    pat = REPO / "compares/results/m2_cmin"
    for sj in sorted(pat.rglob("*_summary.json")):
        log_path = sj.with_suffix(".json.log")
        if not log_path.exists():
            continue
        data = json.loads(sj.read_text(encoding="utf-8"))
        extras = parse_log(log_path)
        data.update(extras)
        sj.write_text(json.dumps(data), encoding="utf-8")
        print(f"  enhanced {sj.relative_to(REPO)}: {extras}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
