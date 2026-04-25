#!/usr/bin/env python3
"""Print SAM bugs in the (now 9-bug) sam_only manifest."""
import json
from pathlib import Path

p = Path("/work/compares/bug_bench/manifest.sam_only.json")
m = json.loads(p.read_text(encoding="utf-8"))
bugs = m.get("bugs", m)
print(f"manifest: {len(bugs)} SAM bugs")
for b in bugs:
    bid = b.get("id")
    sut = b.get("sut")
    fmt = b.get("format")
    sig = b.get("expected_signal", {}).get("type")
    print(f"  {bid:25} sut={sut:10} fmt={fmt:5} signal={sig}")
