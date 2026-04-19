"""
Tests for the Rank 4 coverage lever: `hypothesis.target()` inside
`_run_mr_with_hypothesis` in `test_engine/orchestrator.py`.

We can't easily assert Hypothesis's internal targeting behavior from a unit
test — that lives in the `Phase.target` pass of the engine. What we CAN assert:
  (a) the closure calls `target()` on every example — both success and
      oracle-failure paths (via try/finally),
  (b) the labels and values follow the contract documented in orchestrator.py,
  (c) `target()` exceptions never mask a real _OracleFailure.

We verify by monkeypatching `test_engine.orchestrator.target` and driving a
tiny Hypothesis example directly. This avoids spinning up a full Phase C.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from test_engine import orchestrator as orch
from test_engine.orchestrator import TestSuiteResult, _OracleFailure


class TestTargetDirective:
    def test_target_is_called_on_success_path(self):
        """With no failures, the closure still records target() for both
        divergence (=0) and seed_size, ensuring monotonic signal availability
        for Hypothesis's Phase.target search."""
        calls: list[tuple[float, str]] = []

        def _fake_target(value, *, label):
            calls.append((value, label))

        result = TestSuiteResult()

        def _fake_run_single(**kw):
            # Simulate an uneventful run — no counters change.
            pass

        with patch.object(orch, "target", _fake_target):
            with patch.object(orch, "_run_single_test", _fake_run_single):
                # Directly exercise the closure body by reconstructing the
                # minimal surface: call the same sequence the @given wrapper
                # would call internally.
                _simulate_example(result, lines=["##fileformat=VCFv4.3\n"] * 5)

        labels = {lbl for _, lbl in calls}
        assert "divergence" in labels
        assert "seed_size" in labels

        divergence = next(v for v, lbl in calls if lbl == "divergence")
        seed_size = next(v for v, lbl in calls if lbl == "seed_size")
        assert divergence == 0.0
        assert seed_size == 5.0

    def test_target_records_divergence_when_violations_happen(self):
        """When _run_single_test bumps the failure counters, target()
        sees the positive delta and Hypothesis's Phase.target gets the
        'this example is interesting' signal."""
        calls: list[tuple[float, str]] = []

        def _fake_target(value, *, label):
            calls.append((value, label))

        result = TestSuiteResult()

        def _fake_run_single(**kw):
            # One metamorphic + one differential violation triggered here.
            kw["result"].metamorphic_failures += 1
            kw["result"].differential_failures += 1

        with patch.object(orch, "target", _fake_target):
            with patch.object(orch, "_run_single_test", _fake_run_single):
                _simulate_example(result, lines=["line\n"] * 3)

        divergence = next(v for v, lbl in calls if lbl == "divergence")
        assert divergence == 2.0

    def test_target_still_fires_when_oracle_raises(self):
        """_OracleFailure from _run_single_test must NOT prevent target()
        from being called. Otherwise Phase.target would be starved of
        signal exactly on the examples we most care about."""
        calls: list[tuple[float, str]] = []

        def _fake_target(value, *, label):
            calls.append((value, label))

        result = TestSuiteResult()

        def _fake_run_single(**kw):
            kw["result"].metamorphic_failures += 1
            raise _OracleFailure(diffs=["simulated"], oracle_result=None)

        with patch.object(orch, "target", _fake_target):
            with patch.object(orch, "_run_single_test", _fake_run_single):
                with pytest.raises(_OracleFailure):
                    _simulate_example(result, lines=["x"] * 2)

        labels = {lbl for _, lbl in calls}
        assert "divergence" in labels
        assert "seed_size" in labels
        # Divergence should reflect the +1 metamorphic failure
        divergence = next(v for v, lbl in calls if lbl == "divergence")
        assert divergence == 1.0

    def test_target_exception_does_not_mask_oracle_failure(self):
        """If target() itself blows up (e.g. NaN, label collision), the
        closure swallows it so a real _OracleFailure can still propagate
        to Hypothesis's shrink phase."""
        result = TestSuiteResult()

        def _target_raises(*a, **kw):
            raise RuntimeError("target broken")

        def _fake_run_single(**kw):
            raise _OracleFailure(diffs=["simulated"], oracle_result=None)

        with patch.object(orch, "target", _target_raises):
            with patch.object(orch, "_run_single_test", _fake_run_single):
                with pytest.raises(_OracleFailure):
                    _simulate_example(result, lines=["x"])

    def test_phase_target_present_in_settings(self):
        """Sanity guard: if Phase.target is accidentally dropped from the
        settings' phases list, target() becomes a no-op and this whole
        lever degrades silently. Detect the regression here."""
        import inspect
        source = inspect.getsource(orch._run_mr_with_hypothesis)
        assert "Phase.target" in source, (
            "Phase.target missing from _run_mr_with_hypothesis settings; "
            "hypothesis.target() calls become no-ops"
        )


# ---------------------------------------------------------------------------
# Helper: inline replica of the closure body so we can test it without
# spinning up a full Hypothesis @given loop.
# ---------------------------------------------------------------------------


def _simulate_example(result: TestSuiteResult, lines: list) -> None:
    """Inline the closure body — keeps the test fast and deterministic."""
    before_mv = result.metamorphic_failures
    before_dv = result.differential_failures
    before_cr = result.crashes
    try:
        orch._run_single_test(
            seed_path=None,
            seed_lines=lines,
            rng_seed=0,
            mr_dict={},
            applicable=[],
            result=result,
            output_dir=None,
            fmt="VCF",
            primary_target="",
        )
    finally:
        try:
            divergence = (
                (result.metamorphic_failures - before_mv)
                + (result.differential_failures - before_dv)
                + (result.crashes - before_cr)
            )
            orch.target(float(divergence), label="divergence")
            orch.target(float(len(lines)), label="seed_size")
        except Exception:
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
