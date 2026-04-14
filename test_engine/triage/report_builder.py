"""
Bug report bundle builder.

Creates a directory with all artifacts needed to reproduce and
diagnose a test failure.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .classifier import ClassifiedFailure
from .evidence_formatter import format_evidence
from ..oracles.metamorphic import OracleResult

logger = logging.getLogger(__name__)

_counter_lock = threading.Lock()
_counter = 0


def build_bug_report(
    classified: ClassifiedFailure,
    seed_path: Path,
    transformed_path: Optional[Path],
    oracle_result: OracleResult,
    mr_dict: dict[str, Any],
    output_dir: Path,
) -> Path:
    """
    Create a bug report bundle directory.

    Structure:
        bug_reports/BUG-{timestamp}/
          x.vcf (or x.sam)
          T_x.vcf (or T_x.sam)
          canonical_outputs/
            {parser}_original.json
            {parser}_transformed.json
          logs/
            differences.txt
          evidence.md
          summary.json
    """
    global _counter
    with _counter_lock:
        _counter += 1
        seq = _counter
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    bug_dir = output_dir / f"BUG-{timestamp}_{seq}"
    bug_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy seed files (use read+write to avoid Windows file locking)
    try:
        (bug_dir / seed_path.name).write_bytes(seed_path.read_bytes())
    except OSError as e:
        logger.warning("Could not copy seed file: %s", e)
    if transformed_path and transformed_path.exists():
        try:
            (bug_dir / f"T_{seed_path.name}").write_bytes(
                transformed_path.read_bytes()
            )
        except OSError as e:
            logger.warning("Could not copy transformed file: %s", e)

    # 2. Canonical outputs
    canon_dir = bug_dir / "canonical_outputs"
    canon_dir.mkdir(exist_ok=True)
    if oracle_result.original_result and oracle_result.original_result.canonical_json:
        (canon_dir / f"{classified.parser_name}_original.json").write_text(
            json.dumps(oracle_result.original_result.canonical_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    if oracle_result.transformed_result and oracle_result.transformed_result.canonical_json:
        (canon_dir / f"{classified.parser_name}_transformed.json").write_text(
            json.dumps(oracle_result.transformed_result.canonical_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # 3. Logs
    log_dir = bug_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    if oracle_result.differences:
        (log_dir / "differences.txt").write_text(
            "\n".join(oracle_result.differences),
            encoding="utf-8",
        )
    if oracle_result.original_result and oracle_result.original_result.stderr:
        (log_dir / f"{classified.parser_name}_original_stderr.log").write_text(
            oracle_result.original_result.stderr,
            encoding="utf-8",
        )
    if oracle_result.transformed_result and oracle_result.transformed_result.stderr:
        (log_dir / f"{classified.parser_name}_transformed_stderr.log").write_text(
            oracle_result.transformed_result.stderr,
            encoding="utf-8",
        )

    # 4. Evidence markdown
    evidence_md = format_evidence(mr_dict)
    (bug_dir / "evidence.md").write_text(evidence_md, encoding="utf-8")

    # 5. Summary JSON
    summary = {
        "failure_type": classified.failure_type.value,
        "severity": classified.severity,
        "mr_id": classified.mr_id,
        "mr_name": classified.mr_name,
        "parser_name": classified.parser_name,
        "description": classified.description,
        "difference_count": len(classified.differences),
        "seed_file": seed_path.name,
        "timestamp": timestamp,
    }
    (bug_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    logger.info("Bug report created: %s", bug_dir)
    return bug_dir
