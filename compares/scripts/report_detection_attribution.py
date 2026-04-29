"""Print a per-cell detection-attribution report (tool-output vs PoV-verified)."""
from __future__ import annotations

import io
import json
import pathlib
import sys
from contextlib import redirect_stdout

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[2]


def src_of(trig: str | None) -> str:
    if not trig:
        return "-"
    norm = trig.replace("\\", "/")
    if "compares/bug_bench/triggers/" in norm:
        return "PoV"
    if "/crashes/" in norm:
        return "tool-output"
    return "?"


def main(out_text: io.StringIO | None = None) -> None:
    m_vcf = json.loads(
        (ROOT / "compares" / "bug_bench" / "manifest.vcf_only.json").read_text(
            encoding="utf-8"
        )
    )
    m_sam = json.loads(
        (ROOT / "compares" / "bug_bench" / "manifest.sam_only.json").read_text(
            encoding="utf-8"
        )
    )
    target = sys.stdout if out_text is None else out_text
    with redirect_stdout(target):
        tot = {"detected": 0, "tool": 0, "pov": 0}
        vcf = {"detected": 0, "tool": 0, "pov": 0, "n": len(m_vcf["bugs"])}
        sam = {"detected": 0, "tool": 0, "pov": 0, "n": len(m_sam["bugs"])}
        print(f"{'bug':22s} | fmt | via_tool | via_pov | source")
        print("-" * 80)
        for label, m, bucket in [("VCF", m_vcf, vcf), ("SAM", m_sam, sam)]:
            for b in m["bugs"]:
                p = (
                    ROOT / "compares" / "results" / "bug_bench" / "biotest"
                    / b["id"] / "result.json"
                )
                if not p.exists():
                    continue
                r = json.loads(p.read_text(encoding="utf-8"))
                if not r.get("detected"):
                    continue
                t = bool(r.get("detected_via_tool_output"))
                v = bool(r.get("detected_via_pov_verification"))
                bucket["detected"] += 1
                tot["detected"] += 1
                if t:
                    bucket["tool"] += 1
                    tot["tool"] += 1
                if v:
                    bucket["pov"] += 1
                    tot["pov"] += 1
                print(
                    f"{b['id']:22s} | {label} | {str(t):8s} | {str(v):7s} | "
                    f"{src_of(r.get('trigger_input'))}"
                )
        print()
        print(
            f"VCF: {vcf['detected']}/{vcf['n']} confirmed "
            f"(tool-found: {vcf['tool']}, PoV-verified: {vcf['pov']})"
        )
        print(
            f"SAM: {sam['detected']}/{sam['n']} confirmed "
            f"(tool-found: {sam['tool']}, PoV-verified: {sam['pov']})"
        )
        print(
            f"Total: {tot['detected']}/{vcf['n']+sam['n']} "
            f"(tool-found: {tot['tool']}, PoV-verified: {tot['pov']})"
        )


if __name__ == "__main__":
    main()
