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
    # Primary-SUT weighted line coverage per iteration (same number
    # the Executive Summary and coverage_notes/ use). Optional — when
    # biotest.py can't compute it we push 0.0 and the coverage-plateau
    # check skips gracefully.
    coverage_history: list[float] = field(default_factory=list)
    start_time: float = 0.0

    def to_dict(self) -> dict:
        return {
            "iteration": self.iteration,
            "scc_history": self.scc_history,
            "enforced_history": self.enforced_history,
            "demoted_history": self.demoted_history,
            "coverage_history": self.coverage_history,
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
        state.coverage_history = data.get("coverage_history", [])
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
        # Minimum enforced-MR count before the catastrophic fuse is armed.
        # With only 1-2 MRs the demotion ratio is statistically meaningless
        # (one bad MR = 50-100%). We require a real sample before halting.
        self.catastrophic_min_sample = cfg.get("catastrophic_min_sample", 5)
        # Coverage-delta early-stop (grounded in Run 7 data, 2026-04-20):
        # if weighted line coverage moves less than `min_coverage_delta_pp`
        # for `coverage_plateau_patience` consecutive iterations, stop.
        # Kills runs that would otherwise burn budget on flat iterations
        # while SCC is still technically moving.
        self.min_coverage_delta_pp = cfg.get("min_coverage_delta_pp", 0.3)
        self.coverage_plateau_patience = cfg.get("coverage_plateau_patience", 2)
        self.state = IterationState(start_time=time.monotonic())

    @property
    def elapsed_minutes(self) -> float:
        return (time.monotonic() - self.state.start_time) / 60.0

    def record_iteration(
        self,
        scc_percent: float,
        enforced_count: int,
        demoted_count: int,
        coverage_percent: float = 0.0,
    ) -> None:
        """Record results from one iteration.

        ``coverage_percent`` is the primary SUT's weighted line-coverage
        number for this iteration (same value plotted in Executive
        Summary). Optional: default 0.0 disables the coverage-plateau
        early-stop for runs where the caller can't compute it.
        """
        self.state.iteration += 1
        self.state.scc_history.append(scc_percent)
        self.state.enforced_history.append(enforced_count)
        self.state.demoted_history.append(demoted_count)
        self.state.coverage_history.append(coverage_percent)
        logger.info(
            "Iteration %d: SCC=%.1f%%, coverage=%.1f%%, enforced=%d, demoted=%d",
            self.state.iteration, scc_percent, coverage_percent,
            enforced_count, demoted_count,
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

        # 4. Catastrophic halt (only after at least 1 iteration AND enough
        #    enforced MRs to make the ratio statistically meaningful).
        #    With fewer than catastrophic_min_sample MRs, a single failure
        #    could trip the fuse (e.g., 1-of-1 = 100%). That yields false
        #    halts when Phase B happens to mine few MRs but the tool is
        #    working correctly.
        if self.state.demoted_history and self.state.enforced_history:
            latest_demoted = self.state.demoted_history[-1]
            latest_enforced = self.state.enforced_history[-1]
            if (latest_enforced >= self.catastrophic_min_sample
                    and latest_enforced > 0):
                demotion_rate = latest_demoted / latest_enforced
                if demotion_rate > self.catastrophic_threshold:
                    return TerminationResult(
                        should_stop=True,
                        reason=(
                            f"catastrophic_halt (demotion_rate={demotion_rate:.0%} > "
                            f"{self.catastrophic_threshold:.0%}, n={latest_enforced})"
                        ),
                    )

        # 5. SCC plateau early-stop
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

        # 6. Coverage-delta plateau early-stop (Run 7 lesson — the run
        #    kept going for 5.5 h while weighted line coverage inched up
        #    +0.1–0.2 pp per iter, i.e., per-iter cost way above
        #    per-iter benefit). Stop when every recent iter moved
        #    coverage by less than `min_coverage_delta_pp` vs the
        #    patience-sized baseline.
        if (
            self.min_coverage_delta_pp > 0
            and len(self.state.coverage_history) >= self.coverage_plateau_patience + 1
            and any(c > 0 for c in self.state.coverage_history)
        ):
            recent_cov = self.state.coverage_history[-self.coverage_plateau_patience:]
            baseline_cov = self.state.coverage_history[
                -(self.coverage_plateau_patience + 1)
            ]
            if baseline_cov > 0 and all(
                (c - baseline_cov) < self.min_coverage_delta_pp for c in recent_cov
            ):
                latest_cov = recent_cov[-1]
                return TerminationResult(
                    should_stop=True,
                    reason=(
                        f"coverage_plateau (weighted coverage moved "
                        f"<{self.min_coverage_delta_pp:.1f} pp for "
                        f"{self.coverage_plateau_patience} iter - "
                        f"{baseline_cov:.1f}% -> {latest_cov:.1f}%)"
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
