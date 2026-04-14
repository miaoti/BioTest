"""
DET (Difference-Exposing Test) rate tracker.

Accumulates test events and computes DET rates per MR and per parser pair.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class DETEvent:
    """A single test execution event."""
    mr_id: str
    test_type: str           # "metamorphic" | "differential"
    parser_names: list[str]
    passed: bool
    difference_count: int
    seed_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DETTracker:
    """Tracks DET rates across test runs."""

    events: list[DETEvent] = field(default_factory=list)

    def record(self, event: DETEvent) -> None:
        """Record a test event."""
        self.events.append(event)

    @property
    def total_tests(self) -> int:
        return len(self.events)

    @property
    def disagreements(self) -> int:
        return sum(1 for e in self.events if not e.passed)

    @property
    def det_rate(self) -> float:
        """Overall DET rate = disagreements / total_tests."""
        if self.total_tests == 0:
            return 0.0
        return self.disagreements / self.total_tests

    def det_rate_by_mr(self) -> dict[str, dict[str, float]]:
        """DET rate broken down by MR ID."""
        by_mr: dict[str, list[bool]] = {}
        for e in self.events:
            by_mr.setdefault(e.mr_id, []).append(e.passed)
        return {
            mr_id: {
                "total": len(results),
                "failures": sum(1 for p in results if not p),
                "det_rate": round(sum(1 for p in results if not p) / len(results), 4),
            }
            for mr_id, results in by_mr.items()
        }

    def det_rate_by_type(self) -> dict[str, dict[str, float]]:
        """DET rate broken down by test type (metamorphic vs differential)."""
        by_type: dict[str, list[bool]] = {}
        for e in self.events:
            by_type.setdefault(e.test_type, []).append(e.passed)
        return {
            test_type: {
                "total": len(results),
                "failures": sum(1 for p in results if not p),
                "det_rate": round(sum(1 for p in results if not p) / len(results), 4),
            }
            for test_type, results in by_type.items()
        }

    def summary(self) -> dict:
        """Return summary statistics as JSON-serializable dict."""
        return {
            "total_tests": self.total_tests,
            "disagreements": self.disagreements,
            "det_rate": round(self.det_rate, 4),
            "by_mr": self.det_rate_by_mr(),
            "by_type": self.det_rate_by_type(),
            "timestamp": datetime.now().isoformat(),
        }

    def export(self, path: str) -> None:
        """Export tracker state to JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.summary(), f, indent=2, ensure_ascii=False)
        logger.info("DET report exported to %s", path)
