#!/usr/bin/env python3
"""
Aggregate Phase D outputs into a consolidated metrics report.

Gathers data from:
  - data/feedback_state.json      (iteration state, SCC history)
  - data/det_report.json          (test events, DET rate)
  - data/scc_report.json          (final SCC, blind spots)
  - data/mr_registry.json         (MR counts, transform distribution)
  - coverage_artifacts/           (JaCoCo, coverage.py, pysam Docker)
  - bug_reports/BUG-*/summary.json (bug classification)

Writes: data/phase_d_report.md
Prints: compact console summary

Usage:
    py -3.12 scripts/generate_report.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  WARN: could not parse {path}: {e}", file=sys.stderr)
        return None


def gather_feedback_state() -> dict:
    state = _read_json(ROOT / "data" / "feedback_state.json") or {}
    return {
        "iterations": state.get("iteration", 0),
        "scc_history": state.get("scc_history", []),
        "enforced_history": state.get("enforced_history", []),
        "demoted_history": state.get("demoted_history", []),
    }


def gather_det() -> dict:
    det = _read_json(ROOT / "data" / "det_report.json") or {}
    return {
        "total_tests": det.get("total_tests", 0),
        "disagreements": det.get("disagreements", 0),
        "det_rate": det.get("det_rate", 0.0),
        "by_mr": det.get("by_mr", {}),
        "by_type": det.get("by_type", {}),
    }


def gather_scc() -> dict:
    scc = _read_json(ROOT / "data" / "scc_report.json") or {}
    return {
        "total_rules": scc.get("total_rules", 0),
        "covered_count": scc.get("covered_count", 0),
        "scc_percent": scc.get("scc_percent", 0.0),
        "blind_spot_count": scc.get("blind_spot_count", 0),
        "top_blind_spots": scc.get("blind_spot_details", [])[:10],
    }


def gather_registry() -> dict:
    reg = _read_json(ROOT / "data" / "mr_registry.json") or {"enforced": [], "quarantine": []}
    enforced = reg.get("enforced", [])
    quarantine = reg.get("quarantine", [])

    # Distribution of transform steps
    transform_counter = Counter()
    for mr in enforced:
        for step in mr.get("transform_steps", []):
            transform_counter[step] += 1

    return {
        "enforced_count": len(enforced),
        "quarantine_count": len(quarantine),
        "enforced_mrs": [(mr.get("mr_id", ""), mr.get("mr_name", "")) for mr in enforced],
        "transform_distribution": dict(transform_counter.most_common(10)),
    }


def gather_coverage() -> dict:
    result = {
        "jacoco_htsjdk": None,
        "coveragepy_biopython": None,
        "pysam_docker": None,
        "gcovr_seqan3": None,
    }

    # JaCoCo (htsjdk) — applies the same VCF/SAM-scoped target_filters the
    # runtime collector uses, so the post-run report matches Phase D's feedback
    # signal rather than showing a diluted all-classes number.
    jacoco_xml = ROOT / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    jacoco_exec = ROOT / "coverage_artifacts" / "jacoco" / "jacoco.exec"
    if jacoco_xml.exists():
        try:
            import xml.etree.ElementTree as ET
            import yaml

            # Read target_filters from config for a single source of truth.
            cfg_path = ROOT / "biotest_config.yaml"
            with cfg_path.open("r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            target_filters = (cfg.get("coverage") or {}).get("target_filters") or {}
            # Use only the format(s) actually exercised in this run. If
            # phase_c.format_filter is set, scope the denominator to that
            # format; otherwise union all formats.
            run_fmt = ((cfg.get("phase_c") or {}).get("format_filter") or "").upper()
            if run_fmt and run_fmt in target_filters:
                raw_entries = list(target_filters[run_fmt])
                result.setdefault("jacoco_htsjdk_meta", {})["format_scope"] = run_fmt
            else:
                raw_entries = list(target_filters.get("VCF", [])) + list(target_filters.get("SAM", []))
                result.setdefault("jacoco_htsjdk_meta", {})["format_scope"] = "VCF+SAM"

            # Parse "pkg::PFX1,PFX2" entries into (package, prefixes) rules.
            rules: list[tuple[str, tuple[str, ...]]] = []
            for entry in raw_entries:
                if "::" in entry:
                    pkg, pfxs = entry.split("::", 1)
                    rules.append((pkg.strip(), tuple(p.strip() for p in pfxs.split(",") if p.strip())))
                else:
                    rules.append((entry.strip(), ()))

            def match_pkg(name: str):
                for rp, pfx in rules:
                    if name == rp:
                        return pfx
                return None

            tree = ET.parse(jacoco_xml)
            root = tree.getroot()
            covered = missed = 0
            for pkg in root.findall(".//package"):
                name = pkg.get("name", "")
                prefixes = match_pkg(name)
                if prefixes is None:
                    continue
                for src in pkg.findall("sourcefile"):
                    src_name = src.get("name", "")
                    if prefixes and not any(src_name.startswith(p) for p in prefixes):
                        continue
                    # Per-sourcefile LINE counter (not recursive — avoids
                    # double counting method-level counters).
                    for counter in src.findall("counter"):
                        if counter.get("type") == "LINE":
                            covered += int(counter.get("covered", 0))
                            missed += int(counter.get("missed", 0))
            total = covered + missed
            pct = (covered / total * 100) if total > 0 else 0.0
            result["jacoco_htsjdk"] = {"covered": covered, "total": total, "pct": pct}
        except Exception as e:
            result["jacoco_htsjdk"] = {"error": str(e)}
    elif jacoco_exec.exists():
        size_kb = jacoco_exec.stat().st_size / 1024
        result["jacoco_htsjdk"] = {"exec_size_kb": size_kb, "note": "XML not yet generated"}

    # coverage.py (biopython).
    # NOTE: cov.analysis2 returns (filename, statements, excluded, missing,
    # formatted_missing). `statements` is the full set of tracked
    # executable lines (not executed ones). Executed = statements - missing.
    # Prior versions here used len(analysis[1]) as "covered" which always
    # produced a 50% nonsense when nothing ran (covered = missed = all stmts).
    cov_file = ROOT / "coverage_artifacts" / ".coverage"
    if cov_file.exists():
        try:
            import coverage
            cov = coverage.Coverage(data_file=str(cov_file))
            cov.load()
            covered = missed = 0
            for fp in cov.get_data().measured_files():
                if "Bio" not in fp:
                    continue
                _, statements, _excluded, missing, *_ = cov.analysis2(fp)
                stmt_count = len(statements)
                miss_count = len(missing)
                covered += stmt_count - miss_count
                missed += miss_count
            total = covered + missed
            pct = (covered / total * 100) if total > 0 else 0.0
            result["coveragepy_biopython"] = {"covered": covered, "total": total, "pct": pct}
        except Exception as e:
            result["coveragepy_biopython"] = {"error": str(e)}

    # pysam Docker
    pysam_dir = ROOT / "coverage_artifacts" / "pysam"
    summaries = list(pysam_dir.glob("summary.*.json")) if pysam_dir.exists() else []
    if summaries:
        covered = total = 0
        by_file = {}
        for sp in summaries:
            try:
                data = json.loads(sp.read_text(encoding="utf-8"))
                for fname, stats in data.items():
                    executed = stats.get("executed", 0)
                    file_total = stats.get("total", 0)
                    covered += executed
                    total += file_total
                    by_file[fname] = {"covered": executed, "total": file_total}
            except Exception:
                pass
        pct = (covered / total * 100) if total > 0 else 0.0
        result["pysam_docker"] = {"covered": covered, "total": total, "pct": pct, "files": by_file}

    return result


def gather_bug_reports() -> dict:
    bug_dir = ROOT / "bug_reports"
    if not bug_dir.exists():
        return {"total": 0, "by_class": {}, "by_mr": {}}

    bugs = [p for p in bug_dir.iterdir() if p.is_dir() and p.name.startswith("BUG-")]

    by_class = Counter()
    by_mr = Counter()
    by_parser = Counter()
    by_severity = Counter()

    for b in bugs:
        summary_path = b / "summary.json"
        if not summary_path.exists():
            continue
        try:
            s = json.loads(summary_path.read_text(encoding="utf-8"))
            by_class[s.get("failure_type", "?")] += 1
            by_mr[s.get("mr_name", "?")] += 1
            by_parser[s.get("parser_name", "?")] += 1
            by_severity[s.get("severity", "?")] += 1
        except Exception:
            pass

    return {
        "total": len(bugs),
        "by_class": dict(by_class),
        "by_mr": dict(by_mr.most_common(5)),
        "by_parser": dict(by_parser),
        "by_severity": dict(by_severity),
    }


def build_report() -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    state = gather_feedback_state()
    det = gather_det()
    scc = gather_scc()
    registry = gather_registry()
    coverage = gather_coverage()
    bugs = gather_bug_reports()

    lines = []
    lines.append(f"# Phase D End-to-End Run Report — {ts}")
    lines.append("")

    # --- Executive Summary ---
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- Iterations completed: **{state['iterations']}**")
    lines.append(f"- Total MRs enforced: **{registry['enforced_count']}** "
                 f"(quarantined: {registry['quarantine_count']})")
    lines.append(f"- Total tests: **{det['total_tests']}** (DET rate: **{det['det_rate']*100:.1f}%**)")
    lines.append(f"- Bug reports: **{bugs['total']}**")
    lines.append(f"- SCC: **{scc['scc_percent']:.2f}%** "
                 f"({scc['covered_count']}/{scc['total_rules']} rules)")
    lines.append("")

    # --- SCC Progression ---
    lines.append("## SCC Progression Across Iterations")
    lines.append("")
    history = state["scc_history"]
    enforced_hist = state["enforced_history"]
    demoted_hist = state["demoted_history"]
    if history:
        lines.append("| Iteration | SCC % | Enforced MRs | Demoted |")
        lines.append("|-----------|-------|--------------|---------|")
        for i, (s, e, d) in enumerate(zip(history,
                                           enforced_hist or [0] * len(history),
                                           demoted_hist or [0] * len(history)), 1):
            lines.append(f"| {i} | {s:.2f}% | {e} | {d} |")
    else:
        lines.append("_No iteration history available._")
    lines.append("")

    # --- MR Registry ---
    lines.append("## MR Registry")
    lines.append("")
    lines.append(f"- Enforced: **{registry['enforced_count']}**")
    lines.append(f"- Quarantined: **{registry['quarantine_count']}**")
    lines.append("")
    if registry["transform_distribution"]:
        lines.append("**Transform Step Distribution (top 10):**")
        lines.append("")
        lines.append("| Transform | Count |")
        lines.append("|-----------|-------|")
        for t, n in registry["transform_distribution"].items():
            lines.append(f"| `{t}` | {n} |")
    lines.append("")

    if registry["enforced_mrs"]:
        lines.append("**Enforced MRs:**")
        lines.append("")
        lines.append("| mr_id | mr_name |")
        lines.append("|-------|---------|")
        for mr_id, mr_name in registry["enforced_mrs"][:20]:
            lines.append(f"| `{mr_id}` | {mr_name} |")
    lines.append("")

    # --- Test Execution ---
    lines.append("## Phase C Test Execution")
    lines.append("")
    lines.append(f"- Total tests: **{det['total_tests']}**")
    lines.append(f"- Disagreements: **{det['disagreements']}**")
    lines.append(f"- DET rate: **{det['det_rate']*100:.1f}%**")
    lines.append("")
    if det["by_type"]:
        lines.append("**By Test Type:**")
        lines.append("")
        lines.append("| Type | Total | Failures | DET % |")
        lines.append("|------|-------|----------|-------|")
        for t, stats in det["by_type"].items():
            total = stats.get("total", 0)
            fails = stats.get("failures", 0)
            rate = stats.get("det_rate", 0.0) * 100
            lines.append(f"| {t} | {total} | {fails} | {rate:.1f}% |")
    lines.append("")

    # --- Code Coverage (primary SUT only, per Flow.md Phase D §1.3) ---
    # Read primary_target from config so the report reflects the actual
    # SUT that drove this run's feedback loop.
    try:
        import yaml as _yaml
        _cfg = _yaml.safe_load((ROOT / "biotest_config.yaml").read_text(encoding="utf-8")) or {}
        primary_target = ((_cfg.get("feedback_control") or {}).get("primary_target") or "").lower()
        run_fmt = ((_cfg.get("phase_c") or {}).get("format_filter") or "").upper()
    except Exception:
        primary_target = ""
        run_fmt = ""

    sut_key_map = {
        "htsjdk": ("htsjdk (Java)", "jacoco_htsjdk"),
        "biopython": ("biopython (Python)", "coveragepy_biopython"),
        "pysam": ("pysam (Docker)", "pysam_docker"),
        "seqan3": ("seqan3 (C++)", "gcovr_seqan3"),
    }

    header_suffix = ""
    if primary_target:
        header_suffix = f" — Primary Target: {primary_target}"
        if run_fmt:
            header_suffix += f" (format scope: {run_fmt})"
    lines.append(f"## Code Coverage{header_suffix}")
    lines.append("")
    if primary_target:
        lines.append(
            f"_Per Flow.md Phase D §1.3, feedback-driven runs measure coverage "
            f"for the **primary target only** (`{primary_target}`). Other SUTs "
            f"participate as differential oracles and are intentionally not "
            f"instrumented for coverage._"
        )
        lines.append("")

    active_rows: list[tuple[str, str, str, str]] = []
    if primary_target and primary_target in sut_key_map:
        sut, key = sut_key_map[primary_target]
        data = coverage.get(key)
        if data is None:
            active_rows.append((sut, "not collected", "--", "primary target had no data"))
        elif "error" in data:
            active_rows.append((sut, f"error: {data['error'][:50]}", "--", "--"))
        elif "covered" in data:
            active_rows.append((sut, f"{data['pct']:.1f}%",
                               f"{data['covered']}/{data['total']}", "OK"))
        elif "exec_size_kb" in data:
            active_rows.append((sut, "exec-only", f"{data['exec_size_kb']:.1f} KB", "no XML"))
        else:
            active_rows.append((sut, "?", "?", "?"))
    else:
        # No primary_target configured — fall back to all-SUTs view.
        for sut, key in sut_key_map.values():
            data = coverage.get(key)
            if data is None:
                active_rows.append((sut, "not collected", "--", "--"))
            elif "error" in data:
                active_rows.append((sut, f"error: {data['error'][:50]}", "--", "--"))
            elif "covered" in data:
                active_rows.append((sut, f"{data['pct']:.1f}%",
                                   f"{data['covered']}/{data['total']}", "OK"))
            elif "exec_size_kb" in data:
                active_rows.append((sut, "exec-only", f"{data['exec_size_kb']:.1f} KB", "no XML"))
            else:
                active_rows.append((sut, "?", "?", "?"))

    lines.append("| SUT | Coverage | Lines | Status |")
    lines.append("|-----|----------|-------|--------|")
    for row in active_rows:
        lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
    lines.append("")

    # --- SCC Blind Spots ---
    lines.append("## Top 10 SCC Blind Spots (Uncovered Spec Rules)")
    lines.append("")
    if scc["top_blind_spots"]:
        for i, bs in enumerate(scc["top_blind_spots"][:10], 1):
            severity = bs.get("severity", "?")
            section = bs.get("section_id", "?")
            text = bs.get("text_snippet", "")[:120].replace("\n", " ")
            lines.append(f"{i}. **[{severity}]** {section}")
            lines.append(f"   > {text}...")
    else:
        lines.append("_No blind spots recorded._")
    lines.append("")

    # --- Bug Reports ---
    lines.append("## Bug Reports")
    lines.append("")
    lines.append(f"- Total: **{bugs['total']}**")
    lines.append("")
    if bugs["by_class"]:
        lines.append("**By Classification:**")
        for cls, n in bugs["by_class"].items():
            lines.append(f"- `{cls}`: {n}")
        lines.append("")
    if bugs["by_parser"]:
        lines.append("**By Parser:**")
        for p, n in bugs["by_parser"].items():
            lines.append(f"- `{p}`: {n}")
        lines.append("")
    if bugs["by_severity"]:
        lines.append("**By Severity:**")
        for s, n in bugs["by_severity"].items():
            lines.append(f"- `{s}`: {n}")
        lines.append("")
    if bugs["by_mr"]:
        lines.append("**Top 5 MRs by Failure Count:**")
        for mr, n in bugs["by_mr"].items():
            lines.append(f"- {mr}: {n}")
        lines.append("")

    return "\n".join(lines)


def main():
    print("Generating Phase D report...\n")
    report_md = build_report()

    out_path = ROOT / "data" / "phase_d_report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_md, encoding="utf-8")
    print(f"Report written to: {out_path}")
    print()
    print("=" * 60)
    print(report_md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
