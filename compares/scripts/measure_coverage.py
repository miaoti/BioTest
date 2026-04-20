#!/usr/bin/env python3
"""
Tool-agnostic coverage measurement against BioTest's filter rules.

Given a coverage report (JaCoCo XML for Java tools, coverage.py JSON for
Python tools, gcovr JSON for C/C++ tools) and a ``(SUT, format)`` pair,
computes the same filtered line coverage BioTest's feedback loop uses
at runtime. The filter rules are read FROM ``biotest_config.yaml`` —
single source of truth — so any tool measured with this script is
graded on exactly the same code scope.

Purpose
-------
Cross-tool fairness. When benchmarking BioTest against EvoSuite,
Randoop, Pynguin, or a future testing tool:

1. Run the competing tool, get its coverage report (the tool's native
   JaCoCo / coverage.py / gcovr output).
2. Run this script against that report with ``--sut htsjdk --format VCF``
   (or whatever target applies).
3. Compare the number this script prints against BioTest's last run
   measured under the same command.

Because both measurements pull the filter rules from the same config
entry, neither side can be cherry-picked — change the filter once and
both sides see the change.

Usage examples
--------------

BioTest's Run 6 htsjdk/VCF baseline::

    py -3.12 compares/scripts/measure_coverage.py \\
        --report coverage_artifacts/jacoco/jacoco_post_run6.xml \\
        --sut htsjdk --format VCF \\
        --label "BioTest Run 6"

EvoSuite Run 2 on htsjdk/VCF::

    py -3.12 compares/scripts/measure_coverage.py \\
        --report compares/baselines/evosuite/results/run2_180s_jacoco.xml \\
        --sut htsjdk --format VCF \\
        --label "EvoSuite Run 2"

Side-by-side comparison (two reports at once)::

    py -3.12 compares/scripts/measure_coverage.py \\
        --report coverage_artifacts/jacoco/jacoco_post_run6.xml \\
        --report compares/baselines/evosuite/results/run2_180s_jacoco.xml \\
        --sut htsjdk --format VCF \\
        --label "BioTest Run 6" --label "EvoSuite Run 2"
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

# Make BioTest's own coverage primitives importable when this script is
# invoked from inside the repo.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import yaml  # noqa: E402
import xml.etree.ElementTree as ET  # noqa: E402

from test_engine.feedback.coverage_collector import (  # noqa: E402
    parse_filter_rules,
    filter_file_matches,
)


@dataclass
class BucketResult:
    name: str
    covered: int
    total: int

    @property
    def pct(self) -> float:
        return (100.0 * self.covered / self.total) if self.total else 0.0


@dataclass
class MeasurementResult:
    report_path: str
    sut: str
    format_: str
    filter_rules: list[str]
    buckets: list[BucketResult]
    label: str = ""

    @property
    def total_covered(self) -> int:
        return sum(b.covered for b in self.buckets)

    @property
    def total_lines(self) -> int:
        return sum(b.total for b in self.buckets)

    @property
    def weighted_pct(self) -> float:
        t = self.total_lines
        return (100.0 * self.total_covered / t) if t else 0.0


# ---------------------------------------------------------------------------
# Per-format readers
# ---------------------------------------------------------------------------

def _measure_jacoco_xml(
    xml_path: Path,
    filter_rules_text: list[str],
    metric: str = "LINE",
) -> list[BucketResult]:
    """Walk a JaCoCo XML, filter by BioTest's rules, return per-bucket counts.

    ``metric='LINE'`` (default, grounding-preserving) sums JaCoCo
    ``<counter type='LINE'>`` entries — the canonical BioTest coverage
    number (Run 6 htsjdk/VCF = 46.9%). ``metric='BRANCH'`` sums
    ``<counter type='BRANCH'>`` so the same fairness filter can also
    grade branch coverage when the caller reports both metrics (e.g.
    DESIGN.md §3.2 Phase-2 coverage-growth plots).
    """
    metric = metric.upper()
    if metric not in {"LINE", "BRANCH"}:
        raise ValueError(f"metric must be 'LINE' or 'BRANCH', got {metric!r}")
    rules = parse_filter_rules(filter_rules_text)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    buckets: list[BucketResult] = []
    for pkg, incl, excl in rules:
        cov = miss = 0
        pkg_el = next(
            (p for p in root.findall(".//package")
             if p.attrib.get("name") == pkg),
            None,
        )
        if pkg_el is None:
            buckets.append(BucketResult(pkg, 0, 0))
            continue
        for sf in pkg_el.findall("sourcefile"):
            name = sf.attrib.get("name", "")
            if not filter_file_matches(name, incl, excl):
                continue
            for ctr in sf.findall("counter"):
                if ctr.attrib.get("type") == metric:
                    cov += int(ctr.attrib.get("covered", 0))
                    miss += int(ctr.attrib.get("missed", 0))
        buckets.append(BucketResult(pkg, cov, cov + miss))
    return buckets


def _measure_coveragepy_json(json_path: Path, filter_rules_text: list[str]) -> list[BucketResult]:
    """Parse a ``coverage json`` export (Python SUTs).

    coverage.py shape: ``{"files": {"pkg/path/module.py": {"summary":
    {"covered_lines": N, "num_statements": M}}, ...}}``. Filter rules
    are applied loosely: package prefix matches against the file path;
    include/exclude name prefixes match the basename (same convention
    the feedback loop's CoveragePyCollector uses).
    """
    data = json.loads(json_path.read_text(encoding="utf-8"))
    files = data.get("files", {})
    if not isinstance(files, dict):
        return []
    rules = parse_filter_rules(filter_rules_text)
    # One bucket per rule, summed across matching files.
    buckets: list[BucketResult] = []
    import os
    for pkg, incl, excl in rules:
        cov = total = 0
        for fpath, fdata in files.items():
            fpath_norm = fpath.replace("\\", "/")
            if pkg and not (fpath_norm.startswith(pkg) or pkg in fpath_norm):
                continue
            basename = os.path.basename(fpath)
            if not filter_file_matches(basename, incl, excl):
                continue
            summary = fdata.get("summary", {}) if isinstance(fdata, dict) else {}
            cov += int(summary.get("covered_lines", 0))
            total += int(summary.get("num_statements", 0))
        buckets.append(BucketResult(pkg, cov, total))
    return buckets


def _measure_gcovr_json(json_path: Path, filter_rules_text: list[str]) -> list[BucketResult]:
    """Parse a gcovr JSON (C/C++ SUTs).

    gcovr shape: ``{"files": [{"file": "path", "lines": [{"line_number":
    .., "count": ..}, ...]}, ...]}``.
    """
    data = json.loads(json_path.read_text(encoding="utf-8"))
    files = data.get("files", [])
    if not isinstance(files, list):
        return []
    rules = parse_filter_rules(filter_rules_text)
    import os
    buckets: list[BucketResult] = []
    for pkg, incl, excl in rules:
        cov = total = 0
        for entry in files:
            fpath = entry.get("file", "")
            fpath_norm = fpath.replace("\\", "/")
            if pkg and not (fpath_norm.startswith(pkg) or pkg in fpath_norm):
                continue
            basename = os.path.basename(fpath)
            if not filter_file_matches(basename, incl, excl):
                continue
            for ln in entry.get("lines", []):
                total += 1
                if int(ln.get("count", 0)) > 0:
                    cov += 1
        buckets.append(BucketResult(pkg, cov, total))
    return buckets


def _dispatch_reader(
    report_path: Path,
    filter_rules_text: list[str],
    metric: str = "LINE",
) -> list[BucketResult]:
    """Pick the right reader based on extension + content.

    ``metric`` is only honoured by the JaCoCo XML reader today.
    coverage.py / gcovr JSON summaries don't ship per-file branch
    counts in the shape we parse, so ``metric='BRANCH'`` against them
    raises — add support later if we pick up a tool whose JSON
    exposes branches.
    """
    suffix = report_path.suffix.lower()
    if suffix == ".xml":
        return _measure_jacoco_xml(report_path, filter_rules_text, metric=metric)
    if suffix == ".json":
        # coverage.py vs gcovr: coverage.py has `"files": {...}` (dict);
        # gcovr has `"files": [...]` (list). Sniff and dispatch.
        text = report_path.read_text(encoding="utf-8")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Cannot parse JSON report {report_path}: {e}")
        if metric.upper() != "LINE":
            raise RuntimeError(
                f"metric={metric!r} is only supported for JaCoCo XML today; "
                f"{report_path.suffix} reports don't carry branch summary data."
            )
        files = data.get("files")
        if isinstance(files, dict):
            return _measure_coveragepy_json(report_path, filter_rules_text)
        if isinstance(files, list):
            return _measure_gcovr_json(report_path, filter_rules_text)
        raise RuntimeError(
            f"Unknown JSON shape in {report_path}: `files` is neither dict nor list"
        )
    raise RuntimeError(
        f"Unknown report format: {report_path} (expected .xml / .json)"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def measure(
    report_path: Path | str,
    sut: str,
    format_: str,
    config_path: Path | str = "biotest_config.yaml",
    label: str = "",
    metric: str = "LINE",
) -> MeasurementResult:
    """Measure coverage of a single report against BioTest's filter for
    ``(format_, sut)``. Raises if the config doesn't have a filter for
    that combination.

    The filter rules live at
    ``biotest_config.yaml: coverage.target_filters[<FORMAT>][<sut>]``.
    If a future SUT is added, add the rule there — never inline it
    here.

    ``metric`` picks the JaCoCo counter type for JaCoCo XML reports:
    ``'LINE'`` (default, the canonical BioTest number grounded at
    Run 6 = 46.9%) or ``'BRANCH'`` (DESIGN.md §3.2 Phase-2 companion).
    coverage.py and gcovr JSON only expose line-level counts in the
    summary shape we parse — ``_dispatch_reader`` raises if you ask
    them for branch.
    """
    report_path = Path(report_path)
    config_path = Path(config_path)
    if not report_path.exists():
        raise FileNotFoundError(f"Coverage report not found: {report_path}")
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    target_filters = (cfg.get("coverage") or {}).get("target_filters") or {}
    per_fmt = target_filters.get(format_) or target_filters.get(format_.upper())
    if not isinstance(per_fmt, dict):
        raise KeyError(
            f"No coverage.target_filters entry for format {format_!r} "
            f"in {config_path}"
        )
    filter_rules = per_fmt.get(sut)
    if not isinstance(filter_rules, list):
        raise KeyError(
            f"No coverage.target_filters.{format_}.{sut} entry in {config_path}. "
            f"Known SUTs under {format_}: {sorted(per_fmt)}"
        )

    buckets = _dispatch_reader(report_path, filter_rules, metric=metric)
    return MeasurementResult(
        report_path=str(report_path),
        sut=sut,
        format_=format_,
        filter_rules=list(filter_rules),
        buckets=buckets,
        label=label,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _format_single(r: MeasurementResult) -> list[str]:
    lines: list[str] = []
    if r.label:
        header = f"=== {r.label} ({r.sut}/{r.format_}) ==="
    else:
        header = f"=== {r.sut}/{r.format_} ==="
    lines.append(header)
    lines.append(f"  Report:  {r.report_path}")
    lines.append("  Filter rules (from biotest_config.yaml):")
    for rule in r.filter_rules:
        lines.append(f"    - {rule}")
    lines.append("")
    name_w = max((len(b.name) for b in r.buckets), default=40)
    name_w = max(name_w, 30)
    lines.append(f"  {'Bucket':<{name_w}}  {'Covered':>7}/{'Total':<6} {'%':>6}")
    for b in r.buckets:
        lines.append(
            f"  {b.name:<{name_w}}  {b.covered:>7}/{b.total:<6} ({b.pct:>5.1f}%)"
        )
    lines.append(
        f"  {'OVERALL (weighted)':<{name_w}}  "
        f"{r.total_covered:>7}/{r.total_lines:<6} ({r.weighted_pct:>5.1f}%)"
    )
    return lines


def _format_comparison(results: list[MeasurementResult]) -> list[str]:
    if len(results) < 2:
        return []
    lines = ["=== Side-by-side ==="]
    labels = [r.label or Path(r.report_path).name for r in results]
    bucket_names = [b.name for b in results[0].buckets]
    # Verify all reports used the same filter / ordering so the rows align.
    for r in results[1:]:
        if [b.name for b in r.buckets] != bucket_names:
            lines.append(
                "  (reports use different filter buckets — "
                "side-by-side suppressed)"
            )
            return lines
    name_w = max((len(n) for n in bucket_names), default=30)
    name_w = max(name_w, 30)
    header = f"  {'Bucket':<{name_w}}"
    for lbl in labels:
        header += f"  {lbl:>22}"
    lines.append(header)
    for i, bname in enumerate(bucket_names):
        row = f"  {bname:<{name_w}}"
        for r in results:
            b = r.buckets[i]
            row += f"  {b.covered:>5}/{b.total:<4} ({b.pct:>4.1f}%)"
        lines.append(row)
    # Overall row
    row = f"  {'OVERALL (weighted)':<{name_w}}"
    for r in results:
        row += f"  {r.total_covered:>5}/{r.total_lines:<4} ({r.weighted_pct:>4.1f}%)"
    lines.append(row)
    # Delta column (pairwise vs first)
    lines.append("")
    lines.append(f"  {'Deltas vs ' + labels[0] + ':':<{name_w + 2}}")
    base = results[0].weighted_pct
    for r in results[1:]:
        d = r.weighted_pct - base
        lines.append(f"    {r.label or r.report_path:<{name_w}}  {d:+.1f} pp")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Measure a coverage report under BioTest's filter rules. "
            "Use this to grade any testing tool (BioTest or any baseline) "
            "on exactly the same code scope, for fair comparison."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "--report", action="append", required=True,
        help="Path to a coverage report (JaCoCo XML / coverage.py JSON / "
             "gcovr JSON). Pass multiple times to compare side-by-side.",
    )
    ap.add_argument(
        "--label", action="append", default=[],
        help="Display label for the corresponding --report (order-matched). "
             "Optional.",
    )
    ap.add_argument(
        "--sut", required=True,
        help="SUT name as it appears under coverage.target_filters in the "
             "config (e.g. htsjdk, pysam, biopython, seqan3).",
    )
    ap.add_argument(
        "--format", required=True, dest="format_",
        choices=["VCF", "SAM", "vcf", "sam"],
        help="Format (VCF or SAM).",
    )
    ap.add_argument(
        "--config", default="biotest_config.yaml",
        help="Path to the config file that owns the filter rules "
             "(default: biotest_config.yaml).",
    )
    args = ap.parse_args()

    # Zip reports with labels, padding labels with "" if shorter.
    labels = list(args.label) + [""] * max(0, len(args.report) - len(args.label))
    results: list[MeasurementResult] = []
    for path, lbl in zip(args.report, labels):
        r = measure(
            report_path=path,
            sut=args.sut,
            format_=args.format_.upper(),
            config_path=args.config,
            label=lbl,
        )
        results.append(r)

    for r in results:
        for line in _format_single(r):
            print(line)
        print()
    if len(results) >= 2:
        for line in _format_comparison(results):
            print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
