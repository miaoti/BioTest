"""
Feedback loop controller with 5 termination conditions.

Manages iteration state and evaluates whether the Phase D loop
should continue or stop.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class IterationState:
    """Serializable state of the feedback loop."""
    iteration: int = 0
    scc_history: list[float] = field(default_factory=list)
    enforced_history: list[int] = field(default_factory=list)
    demoted_history: list[int] = field(default_factory=list)
    start_time: float = 0.0

    def to_dict(self) -> dict:
        return {
            "iteration": self.iteration,
            "scc_history": self.scc_history,
            "enforced_history": self.enforced_history,
            "demoted_history": self.demoted_history,
        }

    def save(self, path: Path) -> None:
        """Save state for crash recovery."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "IterationState":
        """Load state from a previous run."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        state = cls()
        state.iteration = data.get("iteration", 0)
        state.scc_history = data.get("scc_history", [])
        state.enforced_history = data.get("enforced_history", [])
        state.demoted_history = data.get("demoted_history", [])
        return state


@dataclass
class TerminationResult:
    """Result of a termination check."""
    should_stop: bool
    reason: str  # e.g., "plateau", "target_achieved", "budget", "catastrophic", "timeout"


class LoopController:
    """
    Controls the Phase D feedback loop.

    Evaluates 5 termination conditions in priority order:
    1. Timeout: total elapsed time exceeds timeout_minutes
    2. Target achieved: SCC >= target_scc_percent
    3. Budget exhaustion: iteration >= max_iterations
    4. Catastrophic halt: >50% of new enforced MRs demoted this iteration
    5. Plateau: SCC unchanged for plateau_patience consecutive rounds
    """

    def __init__(self, cfg: dict):
        self.max_iterations = cfg.get("max_iterations", 5)
        self.plateau_patience = cfg.get("plateau_patience", 2)
        self.target_scc_percent = cfg.get("target_scc_percent", 95.0)
        self.timeout_minutes = cfg.get("timeout_minutes", 120)
        self.catastrophic_threshold = cfg.get("catastrophic_threshold", 0.5)
        self.state = IterationState(start_time=time.monotonic())

    @property
    def elapsed_minutes(self) -> float:
        return (time.monotonic() - self.state.start_time) / 60.0

    def record_iteration(
        self,
        scc_percent: float,
        enforced_count: int,
        demoted_count: int,
    ) -> None:
        """Record results from one iteration."""
        self.state.iteration += 1
        self.state.scc_history.append(scc_percent)
        self.state.enforced_history.append(enforced_count)
        self.state.demoted_history.append(demoted_count)
        logger.info(
            "Iteration %d: SCC=%.1f%%, enforced=%d, demoted=%d",
            self.state.iteration, scc_percent, enforced_count, demoted_count,
        )

    def check_termination(self) -> TerminationResult:
        """Evaluate all 5 termination conditions."""

        # 1. Timeout
        if self.elapsed_minutes >= self.timeout_minutes:
            return TerminationResult(
                should_stop=True,
                reason=f"timeout ({self.elapsed_minutes:.0f}min >= {self.timeout_minutes}min)",
            )

        # 2. Target achieved
        if self.state.scc_history:
            latest_scc = self.state.scc_history[-1]
            if latest_scc >= self.target_scc_percent:
                return TerminationResult(
                    should_stop=True,
                    reason=f"target_achieved (SCC={latest_scc:.1f}% >= {self.target_scc_percent}%)",
                )

        # 3. Budget exhaustion
        if self.state.iteration >= self.max_iterations:
            return TerminationResult(
                should_stop=True,
                reason=f"budget_exhausted (iteration={self.state.iteration} >= {self.max_iterations})",
            )

        # 4. Catastrophic halt (only after at least 1 iteration)
        if self.state.demoted_history and self.state.enforced_history:
            latest_demoted = self.state.demoted_history[-1]
            latest_enforced = self.state.enforced_history[-1]
            if latest_enforced > 0:
                demotion_rate = latest_demoted / latest_enforced
                if demotion_rate > self.catastrophic_threshold:
                    return TerminationResult(
                        should_stop=True,
                        reason=(
                            f"catastrophic_halt (demotion_rate={demotion_rate:.0%} > "
                            f"{self.catastrophic_threshold:.0%})"
                        ),
                    )

        # 5. Plateau early-stop
        if len(self.state.scc_history) >= self.plateau_patience + 1:
            recent = self.state.scc_history[-self.plateau_patience:]
            baseline = self.state.scc_history[-(self.plateau_patience + 1)]
            if all(abs(s - baseline) < 0.5 for s in recent):
                return TerminationResult(
                    should_stop=True,
                    reason=(
                        f"plateau (SCC unchanged at ~{baseline:.1f}% "
                        f"for {self.plateau_patience} iterations)"
                    ),
                )

        return TerminationResult(should_stop=False, reason="")

    def save_state(self, path: Path) -> None:
        """Save state for crash recovery."""
        self.state.save(path)

    def load_state(self, path: Path) -> None:
        """Resume from a previous run."""
        if path.exists():
            self.state = IterationState.load(path)
            self.state.start_time = time.monotonic()
            logger.info("Resumed from iteration %d", self.state.iteration)
