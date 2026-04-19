"""
Multi-language coverage collection abstraction.

Collects filtered code coverage from each SUT's parser modules:
  - JaCoCo XML for Java (htsjdk)
  - coverage.py for Python (biopython, pysam)
  - gcovr JSON for C++ (seqan3)

Architecture:
  - Whitelist Filtering: Each collector only processes files/packages
    that match a configurable whitelist (e.g., htsjdk.variant.vcf).
  - Line Range Aggregation: Uncovered lines are collapsed into compact
    ranges (e.g., "10-13, 50, 52") to prevent LLM Token Overflow when
    generating Blindspot Tickets.
  - Graceful Degradation: If a tool is not installed, the collector
    returns available=False and the loop continues without it.
"""

from __future__ import annotations

import json
import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Line Range Aggregation Helper
# ---------------------------------------------------------------------------

def parse_filter_rules(
    entries: list[str],
) -> list[tuple[str, tuple[str, ...], tuple[str, ...]]]:
    """Parse `target_filters` config entries into (package, includes, excludes)
    triples.

    Supported syntax per entry:
      "pkg/path"                    → package only, all files included
      "pkg/path::VCF,Variant"       → include files starting with VCF or Variant
      "pkg/path::-BCF2,-JEXL"       → exclude files starting with BCF2 or JEXL
      "pkg/path::VCF,-BCF2"         → mixed: include VCF*, ALSO exclude BCF2*

    A sourcefile is admitted iff:
      (no include prefixes OR filename matches some include prefix)
      AND (no exclude prefix matches the filename).
    """
    out: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = []
    for entry in entries:
        if "::" in entry:
            pkg, raw = entry.split("::", 1)
            includes: list[str] = []
            excludes: list[str] = []
            for p in raw.split(","):
                p = p.strip()
                if not p:
                    continue
                if p.startswith("-"):
                    excludes.append(p[1:])
                else:
                    includes.append(p)
            out.append((pkg.strip(), tuple(includes), tuple(excludes)))
        else:
            out.append((entry.strip(), (), ()))
    return out


def _pattern_matches(src_name: str, pattern: str) -> bool:
    """Match a sourcefile against a single pattern.

    Supported forms:
      "Foo"        prefix match        src_name.startswith("Foo")
      "Foo*"       prefix match        same as above (explicit wildcard)
      "*Foo"       suffix match        src_name.endswith("Foo")
      "*Foo*"      contains match      "Foo" in src_name
    """
    if pattern.startswith("*") and pattern.endswith("*") and len(pattern) >= 2:
        return pattern[1:-1] in src_name
    if pattern.startswith("*"):
        return src_name.endswith(pattern[1:])
    if pattern.endswith("*"):
        return src_name.startswith(pattern[:-1])
    # No wildcards — default to prefix match (backward compat).
    return src_name.startswith(pattern)


def filter_file_matches(
    src_name: str,
    includes: tuple[str, ...],
    excludes: tuple[str, ...],
) -> bool:
    """Decide whether a sourcefile name passes the include/exclude filter.

    Each pattern supports optional `*` wildcards — see `_pattern_matches`.
    """
    if includes and not any(_pattern_matches(src_name, p) for p in includes):
        return False
    if excludes and any(_pattern_matches(src_name, p) for p in excludes):
        return False
    return True


def _aggregate_ranges(lines: list[int]) -> list[str]:
    """
    Collapse contiguous line numbers into compact range strings.

    [10, 11, 12, 13, 50, 52] -> ["10-13", "50", "52"]

    This prevents LLM Token Overflow when generating Blindspot Tickets.
    """
    if not lines:
        return []

    sorted_lines = sorted(set(lines))
    ranges: list[str] = []
    start = sorted_lines[0]
    end = start

    for ln in sorted_lines[1:]:
        if ln == end + 1:
            end = ln
        else:
            ranges.append(f"{start}-{end}" if end > start else str(start))
            start = end = ln

    ranges.append(f"{start}-{end}" if end > start else str(start))
    return ranges


def _format_uncovered_regions(
    filename: str,
    missed_lines: list[int],
    max_ranges: int = 5,
) -> list[str]:
    """
    Format uncovered line ranges for a single file.

    Returns: ["VCFCodec.java:10-13", "VCFCodec.java:50-52"]
    Caps at max_ranges to keep output compact.
    """
    ranges = _aggregate_ranges(missed_lines)
    if not ranges:
        return []
    # Truncate if too many ranges
    if len(ranges) > max_ranges:
        ranges = ranges[:max_ranges] + [f"...+{len(ranges) - max_ranges} more"]
    return [f"{filename}:{r}" for r in ranges]


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------

@dataclass
class CoverageResult:
    """Coverage data from a single SUT."""
    parser_name: str
    language: str
    covered_lines: int = 0
    total_lines: int = 0
    line_coverage_pct: float = 0.0
    uncovered_regions: list[str] = field(default_factory=list)
    available: bool = True
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Abstract Base
# ---------------------------------------------------------------------------

class CoverageCollector(ABC):
    """Abstract base for per-SUT coverage collection."""

    @abstractmethod
    def collect(self, format_filter: Optional[list[str]] = None) -> CoverageResult: ...

    @abstractmethod
    def is_available(self) -> bool: ...


# ---------------------------------------------------------------------------
# JaCoCo Collector (Java / htsjdk)
# ---------------------------------------------------------------------------

class JaCoCoCollector(CoverageCollector):
    """
    Parse JaCoCo XML report for htsjdk.

    Whitelist Filtering: Only processes <package> nodes whose names
    match the whitelist (e.g., htsjdk/variant/vcf, htsjdk/samtools).

    Extracts missed lines from <line> tags where mi > 0 (missed
    instructions) or mb > 0 (missed branches), then aggregates
    into compact ranges.

    If only a jacoco.exec binary exists (no XML yet), converts it
    using the JaCoCo CLI tool before parsing.
    """

    def __init__(
        self,
        report_dir: Path,
        filter_packages: Optional[list[str]] = None,
        cli_jar: Optional[Path] = None,
        classfiles_dir: Optional[Path] = None,
    ):
        self.report_dir = report_dir
        self.filter_packages = filter_packages or [
            "htsjdk/variant/vcf",
            "htsjdk/samtools",
        ]
        self.cli_jar = cli_jar
        self.classfiles_dir = classfiles_dir

    def is_available(self) -> bool:
        xml_report = self.report_dir / "jacoco.xml"
        exec_report = self.report_dir / "jacoco.exec"
        return xml_report.exists() or exec_report.exists()

    def _ensure_xml(self) -> Optional[Path]:
        """Convert jacoco.exec -> jacoco.xml if needed.

        If a cached XML exists AND is older than the backing .exec file,
        invalidate it so the conversion below regenerates a fresh report.
        Without this guard, repeated Phase C / Phase D iterations that
        append new blocks into jacoco.exec were being reported against a
        stale XML snapshot — coverage from the most recent runs was
        literally invisible. This is a bug-fix; the happy path (XML
        exists and is current) still short-circuits to the fast return.
        """
        import shutil
        import subprocess

        xml_path = self.report_dir / "jacoco.xml"
        exec_path = self.report_dir / "jacoco.exec"

        # Cache invalidation: if .exec was touched after .xml was written,
        # the XML is stale — drop it so we regenerate below.
        if xml_path.exists() and exec_path.exists():
            try:
                if exec_path.stat().st_mtime > xml_path.stat().st_mtime:
                    xml_path.unlink()
            except OSError as e:
                logger.warning("Could not check JaCoCo XML freshness: %s", e)

        if xml_path.exists():
            return xml_path

        if not exec_path.exists():
            return None

        # Need CLI JAR and classfiles to convert
        cli = self.cli_jar or self.report_dir / "jacococli.jar"
        if not cli.exists():
            logger.warning("JaCoCo CLI JAR not found at %s, cannot convert .exec to .xml", cli)
            return None

        classfiles = self.classfiles_dir
        if not classfiles or not classfiles.exists():
            logger.warning("No classfiles dir for JaCoCo report generation")
            return None

        try:
            java = shutil.which("java")
            if not java:
                return None
            cmd = [
                java, "-jar", str(cli), "report", str(exec_path),
                "--classfiles", str(classfiles),
                "--xml", str(xml_path),
            ]
            subprocess.run(cmd, capture_output=True, timeout=60)
            if xml_path.exists():
                logger.info("Generated JaCoCo XML report: %s", xml_path)
                return xml_path
        except Exception as e:
            logger.warning("JaCoCo exec->XML conversion failed: %s", e)

        return None

    def collect(self, format_filter: Optional[list[str]] = None) -> CoverageResult:
        # Try to convert .exec -> .xml if needed
        report = self._ensure_xml()
        if report is None:
            return CoverageResult(
                parser_name="htsjdk",
                language="Java",
                available=False,
                error=f"JaCoCo report not found in {self.report_dir}",
            )

        # Use format-specific filter if provided, else fall back to default whitelist
        active_filter = format_filter if format_filter else self.filter_packages

        parsed_rules = parse_filter_rules(active_filter)

        def package_rule(pkg_name: str) -> Optional[tuple[tuple[str, ...], tuple[str, ...]]]:
            """Return (includes, excludes) for this package, or None if not listed."""
            for rule_pkg, includes, excludes in parsed_rules:
                if pkg_name == rule_pkg:
                    return (includes, excludes)
            return None

        try:
            tree = ET.parse(report)
            root = tree.getroot()

            total_covered = 0
            total_missed = 0
            all_uncovered_regions: list[str] = []

            for pkg in root.findall(".//package"):
                pkg_name = pkg.get("name", "")
                rule = package_rule(pkg_name)
                if rule is None:
                    continue
                includes, excludes = rule

                for src in pkg.findall("sourcefile"):
                    src_name = src.get("name", "")
                    # Apply sourcefile-name prefix filter: include-list + exclude-list
                    if not filter_file_matches(src_name, includes, excludes):
                        continue

                    missed_lines: list[int] = []

                    # Extract per-line coverage from <line> tags
                    for line_tag in src.findall("line"):
                        nr = int(line_tag.get("nr", 0))
                        mi = int(line_tag.get("mi", 0))  # missed instructions
                        ci = int(line_tag.get("ci", 0))  # covered instructions
                        mb = int(line_tag.get("mb", 0))  # missed branches

                        if ci > 0 or mi > 0:
                            if mi > 0 or mb > 0:
                                missed_lines.append(nr)
                                total_missed += 1
                            else:
                                total_covered += 1

                    # If no <line> tags, fall back to <counter type="LINE"> at the
                    # sourcefile level only (not recursive — avoids double-counting
                    # method-level counters).
                    if not src.findall("line"):
                        for counter in src.findall("counter"):
                            if counter.get("type") == "LINE":
                                c = int(counter.get("covered", 0))
                                m = int(counter.get("missed", 0))
                                total_covered += c
                                total_missed += m

                    # Aggregate missed lines into compact ranges
                    if missed_lines:
                        qualified_name = f"{pkg_name}/{src_name}"
                        regions = _format_uncovered_regions(
                            qualified_name, missed_lines
                        )
                        all_uncovered_regions.extend(regions)

            total = total_covered + total_missed
            pct = (total_covered / total * 100) if total > 0 else 0.0

            return CoverageResult(
                parser_name="htsjdk",
                language="Java",
                covered_lines=total_covered,
                total_lines=total,
                line_coverage_pct=round(pct, 1),
                uncovered_regions=all_uncovered_regions[:30],
            )
        except Exception as e:
            return CoverageResult(
                parser_name="htsjdk",
                language="Java",
                available=False,
                error=f"JaCoCo parse error: {e}",
            )


# ---------------------------------------------------------------------------
# coverage.py Collector (Python / biopython, pysam)
# ---------------------------------------------------------------------------

class CoveragePyCollector(CoverageCollector):
    """
    Collect coverage.py data for Python-based SUTs.

    Supports two modes:
    1. Direct API: Uses coverage.CoverageData to read .coverage SQLite DB
    2. XML fallback: Parses coverage.xml if generated by `coverage xml`

    Filters by files matching source_filter patterns.
    """

    def __init__(
        self,
        parser_name: str,
        coverage_file: Path,
        source_filter: Optional[list[str]] = None,
    ):
        self.parser_name = parser_name
        self.coverage_file = coverage_file
        self.source_filter = source_filter or []

    def is_available(self) -> bool:
        # Check if coverage.py data file or XML exists
        if self.coverage_file.exists():
            try:
                import coverage as _  # noqa: F401
                return True
            except ImportError:
                pass
        # Check for XML fallback
        xml_path = self.coverage_file.with_suffix(".xml")
        return xml_path.exists()

    def collect(self, format_filter: Optional[list[str]] = None) -> CoverageResult:
        # Use format-specific filter if provided, else fall back to default
        active_filter = format_filter if format_filter else self.source_filter

        # Try direct API first
        if self.coverage_file.exists():
            try:
                return self._collect_via_api(active_filter)
            except Exception as e:
                logger.debug("coverage.py API failed, trying XML: %s", e)

        # Try XML fallback
        xml_path = self.coverage_file.with_suffix(".xml")
        if xml_path.exists():
            return self._collect_via_xml(xml_path, active_filter)

        return CoverageResult(
            parser_name=self.parser_name,
            language="Python",
            available=False,
            error="No .coverage data or coverage.xml found",
        )

    def _collect_via_api(self, active_filter: list[str]) -> CoverageResult:
        """Collect using coverage.py Python API."""
        import coverage

        cov = coverage.Coverage(data_file=str(self.coverage_file))
        cov.load()

        total_covered = 0
        total_missed = 0
        all_regions: list[str] = []

        for filepath in cov.get_data().measured_files():
            # Normalize to forward slashes so filters like "Bio/Align/sam"
            # match on Windows where measured_files() returns backslashed paths.
            norm_path = filepath.replace("\\", "/")
            if active_filter and not any(
                f.replace("\\", "/").replace(".", "/") in norm_path
                for f in active_filter
            ):
                continue

            # analysis2 returns: (filename, statements, excluded, missing,
            #                      formatted_missing). statements is the
            # full list of TRACKED executable lines, not executed ones.
            # Executed = statements - missing.
            _, statements, _excluded, missing, *_ = cov.analysis2(filepath)
            stmt_count = len(statements)
            miss_count = len(missing)
            covered_count = stmt_count - miss_count

            total_covered += covered_count
            total_missed += miss_count

            if missing:
                short_name = Path(filepath).name
                regions = _format_uncovered_regions(short_name, sorted(missing))
                all_regions.extend(regions)

        total = total_covered + total_missed
        pct = (total_covered / total * 100) if total > 0 else 0.0

        return CoverageResult(
            parser_name=self.parser_name,
            language="Python",
            covered_lines=total_covered,
            total_lines=total,
            line_coverage_pct=round(pct, 1),
            uncovered_regions=all_regions[:30],
        )

    def _collect_via_xml(self, xml_path: Path, active_filter: list[str]) -> CoverageResult:
        """Parse coverage.xml (Cobertura format)."""
        tree = ET.parse(xml_path)
        root = tree.getroot()

        total_covered = 0
        total_missed = 0
        all_regions: list[str] = []

        for cls in root.findall(".//class"):
            filename = cls.get("filename", "")
            norm_path = filename.replace("\\", "/")
            if active_filter and not any(
                f.replace("\\", "/").replace(".", "/") in norm_path
                for f in active_filter
            ):
                continue

            missed_lines: list[int] = []
            for line in cls.findall(".//line"):
                nr = int(line.get("number", 0))
                hits = int(line.get("hits", 0))
                if hits > 0:
                    total_covered += 1
                else:
                    total_missed += 1
                    missed_lines.append(nr)

            if missed_lines:
                short_name = Path(filename).name
                regions = _format_uncovered_regions(short_name, missed_lines)
                all_regions.extend(regions)

        total = total_covered + total_missed
        pct = (total_covered / total * 100) if total > 0 else 0.0

        return CoverageResult(
            parser_name=self.parser_name,
            language="Python",
            covered_lines=total_covered,
            total_lines=total,
            line_coverage_pct=round(pct, 1),
            uncovered_regions=all_regions[:30],
        )


# ---------------------------------------------------------------------------
# Pysam Docker Coverage Collector
# ---------------------------------------------------------------------------

class PysamDockerCoverageCollector(CoverageCollector):
    """
    Collect coverage from pysam Docker runs.

    The Docker harness writes .coverage.<pid> fragments to a mounted
    volume. This collector combines them with `coverage combine` and
    reads the merged data.
    """

    def __init__(
        self,
        coverage_dir: Path,
        source_filter: Optional[list[str]] = None,
    ):
        self.coverage_dir = coverage_dir
        self.source_filter = source_filter or ["pysam"]

    def is_available(self) -> bool:
        if not self.coverage_dir.exists():
            return False
        # Check for any .coverage.* fragment files
        return any(self.coverage_dir.glob(".coverage.*"))

    def collect(self, format_filter: Optional[list[str]] = None) -> CoverageResult:
        # The Docker harness writes summary.*.json alongside .coverage.* fragments.
        # The summary contains per-file executed/total/missing line counts
        # computed inside the container where source files are accessible.
        summaries = list(self.coverage_dir.glob("summary.*.json"))
        if not summaries and not list(self.coverage_dir.glob(".coverage.*")):
            return CoverageResult(
                parser_name="pysam",
                language="Python",
                available=False,
                error="No pysam Docker coverage data found",
            )

        active_filter = format_filter if format_filter else self.source_filter

        try:
            total_covered = 0
            total_missed = 0
            all_regions: list[str] = []

            if summaries:
                # Use the summary JSON (accurate: computed inside container).
                # Summary was already filtered to the target package inside the
                # container, so all entries are relevant. Only apply active_filter
                # if it contains path fragments that could match bare filenames.
                for summary_path in summaries:
                    data = json.loads(summary_path.read_text(encoding="utf-8"))
                    for filename, stats in data.items():
                        total_covered += stats.get("executed", 0)
                        total_missed += stats.get("total", 0) - stats.get("executed", 0)
                        missing = stats.get("missing", [])
                        if missing:
                            regions = _format_uncovered_regions(filename, missing)
                            all_regions.extend(regions)
            else:
                # Fallback: read .coverage.* fragments (executed count only)
                import coverage
                for frag_path in self.coverage_dir.glob(".coverage.*"):
                    cov = coverage.Coverage(data_file=str(frag_path))
                    cov.load()
                    for filepath in cov.get_data().measured_files():
                        if active_filter and not any(f in filepath for f in active_filter):
                            continue
                        executed = cov.get_data().lines(filepath) or []
                        total_covered += len(executed)

            total = total_covered + total_missed
            pct = (total_covered / total * 100) if total > 0 else 0.0

            return CoverageResult(
                parser_name="pysam",
                language="Python",
                covered_lines=total_covered,
                total_lines=total,
                line_coverage_pct=round(pct, 1),
                uncovered_regions=all_regions[:30],
            )
        except Exception as e:
            return CoverageResult(
                parser_name="pysam",
                language="Python",
                available=False,
                error=f"pysam coverage read error: {e}",
            )


# ---------------------------------------------------------------------------
# gcovr Collector (C++ / seqan3)
# ---------------------------------------------------------------------------

class GcovrCollector(CoverageCollector):
    """
    Collect gcovr data for C++ SUTs (seqan3).

    Reads gcovr JSON output and filters to relevant source directories.
    Extracts per-line coverage and aggregates uncovered ranges.

    If gcovr is installed and .gcda files exist (from a --coverage build),
    runs `gcovr` to generate the JSON report before parsing.
    """

    def __init__(
        self,
        report_path: Path,
        filter_dirs: Optional[list[str]] = None,
        build_dir: Optional[Path] = None,
        source_root: Optional[Path] = None,
    ):
        self.report_path = report_path
        self.filter_dirs = filter_dirs or []
        self.build_dir = build_dir      # Where .gcda files live
        self.source_root = source_root  # SeqAn3 source root for gcovr -r

    def is_available(self) -> bool:
        if self.report_path.exists():
            return True
        # Can we generate the report from .gcda files?
        if self.build_dir and self.build_dir.exists():
            import shutil
            if shutil.which("gcovr"):
                gcda_files = list(self.build_dir.rglob("*.gcda"))
                return len(gcda_files) > 0
        return False

    def _ensure_report(self) -> bool:
        """Generate gcovr JSON from .gcda files if report is missing."""
        if self.report_path.exists():
            return True
        if not self.build_dir or not self.build_dir.exists():
            return False
        import shutil
        import subprocess as _sp
        if not shutil.which("gcovr"):
            return False
        try:
            self.report_path.parent.mkdir(parents=True, exist_ok=True)
            cmd = ["gcovr", "--json", str(self.report_path)]
            if self.source_root:
                cmd.extend(["-r", str(self.source_root)])
            cmd.append(str(self.build_dir))
            _sp.run(cmd, capture_output=True, timeout=120)
            return self.report_path.exists()
        except Exception as e:
            logger.warning("gcovr report generation failed: %s", e)
            return False

    def collect(self, format_filter: Optional[list[str]] = None) -> CoverageResult:
        if not self._ensure_report():
            return CoverageResult(
                parser_name="seqan3",
                language="C++",
                available=False,
                error=f"gcovr report not available (no .gcda data or gcovr not installed)",
            )

        active_filter = format_filter if format_filter else self.filter_dirs

        try:
            with open(self.report_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            total_covered = 0
            total_missed = 0
            all_regions: list[str] = []

            for file_data in data.get("files", []):
                filename = file_data.get("filename", "")
                if active_filter and not any(
                    d in filename for d in active_filter
                ):
                    continue

                missed_lines: list[int] = []
                for line_data in file_data.get("lines", []):
                    ln = line_data.get("line_number", 0)
                    count = line_data.get("count", 0)
                    if count > 0:
                        total_covered += 1
                    else:
                        total_missed += 1
                        missed_lines.append(ln)

                if missed_lines:
                    short_name = Path(filename).name
                    regions = _format_uncovered_regions(short_name, missed_lines)
                    all_regions.extend(regions)

            total = total_covered + total_missed
            pct = (total_covered / total * 100) if total > 0 else 0.0

            return CoverageResult(
                parser_name="seqan3",
                language="C++",
                covered_lines=total_covered,
                total_lines=total,
                line_coverage_pct=round(pct, 1),
                uncovered_regions=all_regions[:30],
            )
        except Exception as e:
            return CoverageResult(
                parser_name="seqan3",
                language="C++",
                available=False,
                error=f"gcovr parse error: {e}",
            )


# ---------------------------------------------------------------------------
# Python Coverage Context Manager
# ---------------------------------------------------------------------------

class PythonCoverageContext:
    """
    Context manager that instruments Phase C execution with coverage.py.

    Wraps the entire Phase C test suite run so all in-process Python
    runner calls (Biopython, pysam native) are measured.

    Uses source= pointing to the installed package directories so
    coverage.py measures site-packages code (normally excluded).

    Usage:
        ctx = PythonCoverageContext(data_file=".coverage", source_filter=["Bio/Align/sam"])
        with ctx:
            run_phase_c(cfg)
        # .coverage file is now written; CoveragePyCollector can read it
    """

    def __init__(self, data_file: str = ".coverage", source_filter: Optional[list[str]] = None):
        self._data_file = data_file
        self._source_filter = source_filter or []
        self._cov = None

    def _resolve_source_dirs(self) -> list[str]:
        """Resolve source_filter patterns to actual installed package directories.

        e.g., "Bio/Align/sam" -> "C:/Python312/.../Bio/Align" (parent dir of sam.py)
        """
        import importlib
        dirs = set()
        for pattern in self._source_filter:
            # Convert file path pattern to module name
            # "Bio/Align/sam.py" -> "Bio.Align.sam"
            mod_name = pattern.replace("/", ".").replace("\\", ".").rstrip(".py")
            try:
                mod = importlib.import_module(mod_name)
                if hasattr(mod, "__file__") and mod.__file__:
                    dirs.add(str(Path(mod.__file__).parent))
            except ImportError:
                # Try parent module
                parts = mod_name.rsplit(".", 1)
                if len(parts) > 1:
                    try:
                        mod = importlib.import_module(parts[0])
                        if hasattr(mod, "__file__") and mod.__file__:
                            dirs.add(str(Path(mod.__file__).parent))
                    except ImportError:
                        pass
        return list(dirs)

    def __enter__(self):
        try:
            import coverage
            import sys

            source_dirs = self._resolve_source_dirs()
            if not source_dirs:
                logger.debug("No source dirs resolved for coverage, skipping")
                return self

            # Intentionally DO NOT delete the .coverage data file between
            # iterations — coverage.py appends so Phase D feedback sees
            # cumulative line coverage across iterations, matching JaCoCo's
            # append=true semantics. Cross-run clearing is handled by
            # scripts/clean_artifacts.py.

            # Evict target modules AND their parent packages from sys.modules
            # so coverage.py's tracer instruments them when they are re-imported
            # during Phase C. Parent eviction is needed because `from Bio.Align
            # import sam` resolves via the cached Bio.Align attribute chain;
            # evicting only the leaf module can leave the import short-
            # circuited through the cached parent.
            module_roots: set[str] = set()
            for pattern in self._source_filter:
                norm = pattern.replace("/", ".").replace("\\", ".")
                if norm.endswith(".py"):
                    norm = norm[:-3]
                parts = norm.split(".")
                for i in range(1, len(parts) + 1):
                    module_roots.add(".".join(parts[:i]))

            to_evict = [m for m in list(sys.modules.keys())
                        if any(m == r or m.startswith(r + ".") for r in module_roots)]
            for m in to_evict:
                del sys.modules[m]

            # Reset runner availability caches so runners re-import under the
            # tracer the first time they are asked whether they're available.
            try:
                import test_engine.runners.biopython_runner as _br
                _br._biopython_available = None
            except ImportError:
                pass

            # Use source_pkgs (cover the whole Bio.Align package) alongside
            # source=source_dirs. source_pkgs is more reliable on Windows
            # and with submodule-level imports. Explicit concurrency='thread'
            # ensures tracing follows into ThreadPoolExecutor workers that
            # runners (e.g. BiopythonRunner) use.
            source_pkgs: list[str] = []
            for pattern in self._source_filter:
                norm = pattern.replace("/", ".").replace("\\", ".")
                if norm.endswith(".py"):
                    norm = norm[:-3]
                parts = norm.split(".")
                # Use parent package (e.g. 'Bio.Align') for broad coverage
                if len(parts) >= 2:
                    source_pkgs.append(".".join(parts[:-1]))
                else:
                    source_pkgs.append(norm)

            self._cov = coverage.Coverage(
                data_file=self._data_file,
                source=source_dirs,
                source_pkgs=source_pkgs or None,
                concurrency=["thread"],
                config_file=False,  # ignore any stray .coveragerc
            )
            self._cov.start()
            logger.info(
                "Python coverage started (data_file=%s, source=%s, source_pkgs=%s, evicted=%d modules)",
                self._data_file, source_dirs, source_pkgs, len(to_evict),
            )
        except ImportError:
            logger.debug("coverage.py not installed, Python coverage disabled")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cov:
            try:
                self._cov.stop()
                self._cov.save()
                # Emit a diagnostic so silent failures are visible.
                data = self._cov.get_data()
                traced = 0
                for fp in data.measured_files():
                    if data.lines(fp):
                        traced += 1
                logger.info(
                    "Python coverage saved to %s (%d files traced with >0 lines)",
                    self._data_file, traced,
                )
                if traced == 0:
                    logger.warning(
                        "Python coverage ran but traced 0 lines — likely a "
                        "tracer-install race. Check that target modules are "
                        "imported inside the coverage context."
                    )
                    # Delete the empty data file so downstream collectors
                    # report 'not available' rather than reading a file full
                    # of zero-line entries that then get misinterpreted.
                    from pathlib import Path as _P
                    try:
                        _p = _P(self._data_file)
                        if _p.exists():
                            _p.unlink()
                            logger.debug("Removed empty coverage file %s", _p)
                    except OSError:
                        pass
            except Exception as e:
                logger.error("Python coverage save failed: %s", e)
        return False  # Don't suppress exceptions


# ---------------------------------------------------------------------------
# Multi-Collector Aggregator
# ---------------------------------------------------------------------------

class MultiCoverageCollector:
    """Aggregates per-SUT coverage collectors with graceful degradation.

    Per Flow.md Phase D §1.3 "Primary Target vs Auxiliary Oracles", coverage
    is collected ONLY for the primary target SUT. Other SUTs participate
    purely as differential oracles; measuring their coverage would waste
    work and add noise to the feedback signal. Each collector is tagged
    with its SUT name so `collect_all(primary_target=...)` can filter.
    """

    def __init__(self, cfg: dict[str, Any]):
        # list of (sut_name, collector) so we can filter by primary target.
        self.collectors: list[tuple[str, CoverageCollector]] = []
        self._target_filters: dict[str, list[str]] = cfg.get("target_filters", {})
        self._build_collectors(cfg)

    def _build_collectors(self, cfg: dict[str, Any]) -> None:
        """Build collectors from config, skip unavailable ones."""
        if not cfg.get("enabled", False):
            return

        # JaCoCo for htsjdk
        jacoco_dir = cfg.get("jacoco_report_dir")
        if jacoco_dir:
            self.collectors.append(("htsjdk", JaCoCoCollector(
                report_dir=Path(jacoco_dir),
                filter_packages=cfg.get("jacoco_filter_packages"),
                cli_jar=Path(cfg["jacoco_cli_jar"]) if cfg.get("jacoco_cli_jar") else None,
                classfiles_dir=Path(cfg["jacoco_classfiles_dir"]) if cfg.get("jacoco_classfiles_dir") else None,
            )))

        # coverage.py for Python SUTs
        coveragepy_file = cfg.get("coveragepy_data_file", ".coverage")
        source_filter = cfg.get("coveragepy_source_filter", [])
        if source_filter:
            for src in source_filter:
                name = "biopython" if "Bio" in src else "pysam"
                self.collectors.append((name, CoveragePyCollector(
                    parser_name=name,
                    coverage_file=Path(coveragepy_file),
                    source_filter=[src],
                )))

        # pysam Docker coverage (fragments from mounted volume)
        pysam_cov_dir = cfg.get("pysam_coverage_dir")
        if pysam_cov_dir:
            self.collectors.append(("pysam", PysamDockerCoverageCollector(
                coverage_dir=Path(pysam_cov_dir),
                source_filter=cfg.get("pysam_source_filter", ["pysam"]),
            )))

        # gcovr for seqan3
        gcovr_report = cfg.get("gcovr_report_path")
        if gcovr_report:
            self.collectors.append(("seqan3", GcovrCollector(
                report_path=Path(gcovr_report),
                filter_dirs=cfg.get("gcovr_filter_dirs", []),
                build_dir=Path(cfg["gcovr_build_dir"]) if cfg.get("gcovr_build_dir") else None,
                source_root=Path(cfg["gcovr_source_root"]) if cfg.get("gcovr_source_root") else None,
            )))

    def _resolve_sut_filter(
        self, format_context: str, sut_name: str,
    ) -> Optional[list[str]]:
        """Pick the coverage filter list for a specific SUT + format.

        Supports two YAML shapes for `coverage.target_filters`:

        Nested (preferred, explicit per-SUT scope — required when onboarding
        a new SUT):

            target_filters:
              VCF:
                htsjdk: [htsjdk/variant/vcf, ...]
                pysam:  [pysam]

        Legacy flat (applied to all SUTs; some entries are ignored by
        collectors for other languages):

            target_filters:
              VCF: [htsjdk/variant/vcf, ..., pysam]

        Returns None if no filter is configured for this (fmt, sut).
        """
        if not format_context:
            return None
        fmt_entry = self._target_filters.get(format_context.upper())
        if fmt_entry is None:
            return None
        if isinstance(fmt_entry, list):
            return fmt_entry  # legacy flat
        if isinstance(fmt_entry, dict):
            return fmt_entry.get(sut_name)
        logger.warning(
            "target_filters.%s must be list (legacy) or dict (per-SUT); got %s",
            format_context.upper(), type(fmt_entry).__name__,
        )
        return None

    def collect_all(
        self,
        format_context: str = "",
        primary_target: str = "",
    ) -> list[CoverageResult]:
        """Collect coverage scoped to the primary target SUT.

        Args:
            format_context: Current format being tested ("VCF" or "SAM").
                            If set, coverage is filtered to format-relevant
                            paths via target_filters config — and further
                            per-SUT when the YAML uses the nested shape.
            primary_target: If set (e.g. "htsjdk"), only that SUT's
                            collector runs. Other SUTs are skipped because
                            Phase D's feedback signal is driven solely by
                            the primary target (Flow.md §1.3). Leave empty
                            to fall back to all-SUT collection (legacy).
        """
        active: list[tuple[str, CoverageCollector]] = [
            (n, c) for (n, c) in self.collectors
            if (not primary_target) or n == primary_target
        ]

        results = []
        for sut_name, collector in active:
            sut_filter = self._resolve_sut_filter(format_context, sut_name)
            if collector.is_available():
                try:
                    results.append(collector.collect(format_filter=sut_filter))
                except Exception as e:
                    logger.warning("Coverage collection failed: %s", e)
            else:
                logger.debug(
                    "Coverage collector %s not available, skipping",
                    type(collector).__name__,
                )
        return results
