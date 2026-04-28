#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/bug_bench_chat4_7200/cargo_fuzz")
for d in sorted(root.iterdir()):
    if not d.is_dir():
        continue
    r_path = d / "result.json"
    if r_path.exists():
        r = json.loads(r_path.read_text())
        err = r.get("install_error") or ""
        det = r.get("detected")
        conf = r.get("confirmed_fix_silences_signal")
        print(f"  {d.name:25s}  det={det} conf={conf} err={err[:60]!r}")
    else:
        tool_log = d / "tool.log"
        if tool_log.exists():
            tail = tool_log.read_text().strip().split("\n")[-1]
            time_match = ""
            for part in tail.split():
                if part.startswith("time:"):
                    time_match = f"time={tail.split('time:')[1].split()[0]}s"
                    break
            print(f"  {d.name:25s}  (fuzzing) {time_match}")
        else:
            print(f"  {d.name:25s}  (no log)")
