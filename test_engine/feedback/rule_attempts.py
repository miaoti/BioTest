"""
Per-rule failure / cooldown tracker — the "backoff" half of the
Prioritized-Queueing mechanism.

Problem this solves:
    Top-K prioritization on its own can starve the queue. If rule R is
    the hardest and therefore ranked #1, and the LLM can't cover it in
    iteration 1 or 2, the same rule will re-rank #1 in iteration 3
    forever — the other 307 rules never get a shot. "惩罚 / 冷却机制"
    (penalty / cool-down) says: when a rule is shown but stays
    uncovered after the iteration, temporarily demote it so the queue
    can make progress elsewhere. "换个思路，曲线救国."

Contract:
    - `record_attempt(iteration, chunk_ids)` at the END of building the
      ticket — these rules are now "shown" in iteration `iteration`.
    - `record_outcome(iteration, newly_covered_chunk_ids)` AFTER the
      iteration's Phase C runs. For every chunk_id that was shown but
      NOT newly covered, failure_count is incremented and the rule is
      marked cooled until `iteration + cooldown_duration(failure_count)`.
      Covered rules have their records WIPED so they re-enter the queue
      clean if they ever become uncovered again.
    - `is_cooling(chunk_id, iteration)` — consulted by the Top-K picker
      in `blindspot_builder` to skip rules that are still in cooldown.
    - `failure_count(chunk_id)` — used as a secondary sort-key penalty
      so that even after cooldown expires, repeat-offenders are ranked
      below first-timers among equally-proximate, equally-complex rules.

Persistence:
    JSON file at `data/rule_attempts.json` — written by Phase D after
    every iteration, loaded on resume.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


# Cooldown schedule: how many iterations to skip a rule after N failures.
# Exponential with a ceiling so no rule is cooled forever.
#   1 failure  → 1 iter skip
#   2 failures → 2 iter skip
#   3 failures → 4 iter skip
#   4+ fails   → 4 iter skip (capped at MAX_COOLDOWN_ITERATIONS)
MAX_COOLDOWN_ITERATIONS = 4


def cooldown_duration(failure_count: int) -> int:
    """Iterations to skip after `failure_count` consecutive failures."""
    if failure_count <= 0:
        return 0
    return min(2 ** (failure_count - 1), MAX_COOLDOWN_ITERATIONS)


@dataclass
class RuleRecord:
    """Per-chunk attempt history."""
    failure_count: int = 0
    last_shown_iteration: int = -1
    cooled_until_iteration: int = -1  # rule is hidden while iter <= this
    total_attempts: int = 0

    def to_dict(self) -> dict:
        return {
            "failure_count": self.failure_count,
            "last_shown_iteration": self.last_shown_iteration,
            "cooled_until_iteration": self.cooled_until_iteration,
            "total_attempts": self.total_attempts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RuleRecord":
        return cls(
            failure_count=int(data.get("failure_count", 0)),
            last_shown_iteration=int(data.get("last_shown_iteration", -1)),
            cooled_until_iteration=int(data.get("cooled_until_iteration", -1)),
            total_attempts=int(data.get("total_attempts", 0)),
        )


@dataclass
class RuleAttemptTracker:
    """Persistent store of per-rule attempt outcomes."""
    records: dict[str, RuleRecord] = field(default_factory=dict)
    # Chunk IDs shown in the most recent ticket, for the
    # record_outcome() callback to know what to score.
    pending_shown: set[str] = field(default_factory=set)
    pending_iteration: int = -1

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def failure_count(self, chunk_id: str) -> int:
        rec = self.records.get(chunk_id)
        return rec.failure_count if rec else 0

    def is_cooling(self, chunk_id: str, iteration: int) -> bool:
        """True iff `iteration` is still within the rule's cooldown window."""
        rec = self.records.get(chunk_id)
        if rec is None:
            return False
        return iteration <= rec.cooled_until_iteration

    def cooldown_remaining(self, chunk_id: str, iteration: int) -> int:
        """How many more iterations until this rule can be shown again."""
        rec = self.records.get(chunk_id)
        if rec is None:
            return 0
        return max(0, rec.cooled_until_iteration - iteration + 1)

    def currently_cooled_ids(self, iteration: int) -> set[str]:
        return {cid for cid in self.records if self.is_cooling(cid, iteration)}

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def record_attempt(self, iteration: int, chunk_ids: Iterable[str]) -> None:
        """Mark these rules as shown to the LLM in `iteration`.

        Called by `blindspot_builder.build_blindspot_ticket` AFTER the
        Top-K has been chosen. The outcome is scored by a later
        `record_outcome` call once Phase C finishes.
        """
        shown = {cid for cid in chunk_ids if cid}
        self.pending_iteration = iteration
        self.pending_shown = shown
        for cid in shown:
            rec = self.records.setdefault(cid, RuleRecord())
            rec.last_shown_iteration = iteration
            rec.total_attempts += 1

    def record_outcome(
        self,
        iteration: int,
        newly_covered_chunk_ids: Iterable[str],
    ) -> dict[str, dict]:
        """Score each pending shown rule as covered / still-uncovered.

        Returns a {chunk_id: {"outcome": ..., "failure_count": N, ...}}
        diagnostic dict suitable for logging.
        """
        covered = {cid for cid in newly_covered_chunk_ids if cid}
        outcomes: dict[str, dict] = {}

        for cid in self.pending_shown:
            if cid in covered:
                # Clean slate — rule was successfully covered.
                self.records.pop(cid, None)
                outcomes[cid] = {"outcome": "covered"}
                continue

            rec = self.records.setdefault(cid, RuleRecord())
            rec.failure_count += 1
            skip_n = cooldown_duration(rec.failure_count)
            rec.cooled_until_iteration = iteration + skip_n
            outcomes[cid] = {
                "outcome": "uncovered",
                "failure_count": rec.failure_count,
                "cooldown_iterations": skip_n,
                "cooled_until_iteration": rec.cooled_until_iteration,
            }

        # Also give rules that are NOT in pending_shown a free pass:
        # if they became covered by side-effect (e.g. an MR from a
        # previous iteration finally exercised this rule), wipe them.
        for cid in list(covered - self.pending_shown):
            if cid in self.records:
                self.records.pop(cid)
                outcomes[cid] = {"outcome": "covered_indirectly"}

        self.pending_shown = set()
        self.pending_iteration = -1
        return outcomes

    def forget(self, chunk_id: str) -> None:
        """Remove a rule from the tracker entirely (admin / test hook)."""
        self.records.pop(chunk_id, None)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "pending_iteration": self.pending_iteration,
            "pending_shown": sorted(self.pending_shown),
            "records": {cid: rec.to_dict() for cid, rec in self.records.items()},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RuleAttemptTracker":
        tracker = cls()
        tracker.pending_iteration = int(data.get("pending_iteration", -1))
        tracker.pending_shown = set(data.get("pending_shown", []))
        for cid, rec_data in (data.get("records") or {}).items():
            tracker.records[cid] = RuleRecord.from_dict(rec_data)
        return tracker

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        import os
        os.replace(tmp, path)

    @classmethod
    def load(cls, path: Path) -> "RuleAttemptTracker":
        if not path.exists():
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Could not read %s (%s); starting fresh tracker", path, e)
            return cls()
        return cls.from_dict(data)
