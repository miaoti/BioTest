"""
Phase C configuration: paths, timeouts, parser registry.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SEEDS_DIR = PROJECT_ROOT / "seeds"
BUG_REPORTS_DIR = PROJECT_ROOT / "bug_reports"
HARNESSES_DIR = PROJECT_ROOT / "harnesses"
MR_REGISTRY_PATH = PROJECT_ROOT / "data" / "mr_registry.json"

# SUT locations
SUT_DIR = PROJECT_ROOT / "SUTfolder"
HTSJDK_DIR = SUT_DIR / "java" / "htsjdk"
BIOPYTHON_DIR = SUT_DIR / "python" / "biopython"
SEQAN3_DIR = SUT_DIR / "cpp" / "seqan3"

# ---------------------------------------------------------------------------
# Runner configuration
# ---------------------------------------------------------------------------

DEFAULT_TIMEOUT_S = 30.0
SUBPROCESS_TIMEOUT_S = 60.0

# Java
JAVA_CMD = "java"

# Parser-format support matrix
PARSER_FORMAT_MAP: dict[str, list[str]] = {
    "VCF": ["htsjdk", "pysam"],
    "SAM": ["htsjdk", "biopython", "pysam", "seqan3"],
}

# ---------------------------------------------------------------------------
# Coverage output
# ---------------------------------------------------------------------------

COVERAGE_DIR = PROJECT_ROOT / "coverage_artifacts"

# ---------------------------------------------------------------------------
# DET report output
# ---------------------------------------------------------------------------

DET_REPORT_PATH = PROJECT_ROOT / "data" / "det_report.json"
