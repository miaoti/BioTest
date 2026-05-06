"""Unit tests for `scale_max_examples` and the orchestrator's per-MR
budget scaling integration.

Why this exists: across the 4-big-run cascade measurements, rep 0 had
the highest coverage and reps 1-3 plateaued lower (e.g. htsjdk_vcf
45.9 → 33.9 → 32.9 → 32.9). The cause is that as the cascade corpus
grows, a fixed Hypothesis `max_examples=50` gives each seed fewer picks,
under-sampling the high-coverage curated seeds. The
`scale_max_examples` helper is the fix; these tests pin its formula
and edge cases.
"""

import math
from pathlib import Path

import pytest

from test_engine.orchestrator import scale_max_examples, run_test_suite


# ---------------------------------------------------------------------------
# scale_max_examples — formula + edge cases
# ---------------------------------------------------------------------------

class TestScaleMaxExamples:
    def test_below_baseline_returns_base(self):
        # Small corpus — no shrinkage.
        assert scale_max_examples(50, 20, baseline_corpus_size=33) == 50

    def test_at_baseline_returns_base(self):
        # Exactly at baseline — formula returns base.
        assert scale_max_examples(50, 33) == 50

    def test_4x_baseline_doubles(self):
        # corpus = 4*baseline → sqrt(4) = 2 → scaled = 100.
        assert scale_max_examples(50, 132, baseline_corpus_size=33) == 100

    def test_corpus_1100_pins_exact_value(self):
        # sqrt(1100/33) ≈ 5.7735 → 50 * 5.7735 = 288.675 → round to 289.
        # Pinning the exact integer locks the formula against silent
        # round-mode changes.
        assert scale_max_examples(50, 1100, baseline_corpus_size=33) == 289

    def test_cap_clamps_high_corpora(self):
        # 10000 seeds would naturally yield ~870, cap at 400.
        assert scale_max_examples(50, 10000, baseline_corpus_size=33, cap=400) == 400

    def test_cap_zero_treated_as_no_cap(self):
        # cap=0 should be ignored (defensive — config might pass 0).
        result = scale_max_examples(50, 10000, baseline_corpus_size=33, cap=0)
        assert result > 400  # not clamped

    def test_cap_negative_treated_as_no_cap(self):
        result = scale_max_examples(50, 10000, baseline_corpus_size=33, cap=-1)
        assert result > 400

    def test_cap_above_natural_value_no_op(self):
        # cap higher than natural scaled value → no clamp.
        natural = scale_max_examples(50, 132, baseline_corpus_size=33)
        with_cap = scale_max_examples(50, 132, baseline_corpus_size=33, cap=10000)
        assert natural == with_cap == 100

    def test_cap_below_base_does_not_violate_floor(self):
        # Misconfigured cap (< base) must NOT shrink below base —
        # docstring promises ``return >= base`` always.
        result = scale_max_examples(50, 1000, baseline_corpus_size=33, cap=10)
        assert result == 50, (
            f"cap=10 < base=50 should not violate the base floor; got {result}"
        )

    def test_zero_corpus_returns_base(self):
        # Empty corpus is a defensive edge case (orchestrator skips, but
        # the helper must not divide by zero).
        assert scale_max_examples(50, 0) == 50

    def test_zero_baseline_returns_base(self):
        assert scale_max_examples(50, 100, baseline_corpus_size=0) == 50

    def test_negative_corpus_returns_base(self):
        assert scale_max_examples(50, -5) == 50

    def test_negative_baseline_returns_base(self):
        assert scale_max_examples(50, 100, baseline_corpus_size=-1) == 50

    def test_base_zero_returns_zero_floor(self):
        # base=0 with positive scale should still cap at 0 (max(0, 0) = 0).
        assert scale_max_examples(0, 100, baseline_corpus_size=33) == 0

    def test_base_one_corpus_huge(self):
        # base=1 corpus=10000 baseline=33 → sqrt(303) ≈ 17.4 → 17.
        result = scale_max_examples(1, 10000, baseline_corpus_size=33)
        assert result == 17

    def test_monotonic_in_corpus_size(self):
        # Scaled value should be non-decreasing as corpus grows.
        prev = 0
        for size in (33, 100, 250, 500, 1000, 2000, 5000):
            cur = scale_max_examples(50, size, baseline_corpus_size=33, cap=10000)
            assert cur >= prev, f"non-monotonic at size={size}: {prev} -> {cur}"
            prev = cur

    def test_idempotent_when_re_passed(self):
        # Calling scale on the result should be a no-op when corpus
        # equals baseline (scale=1).
        scaled = scale_max_examples(50, 132, baseline_corpus_size=33)
        again = scale_max_examples(scaled, 33, baseline_corpus_size=33)
        assert again == scaled

    def test_formula_matches_documented_sqrt(self):
        # Sanity-check the exact sqrt formula for a non-square ratio.
        # corpus=200, baseline=50 → sqrt(4) = 2 → 50*2 = 100.
        assert scale_max_examples(50, 200, baseline_corpus_size=50) == 100
        # corpus=300, baseline=50 → sqrt(6) ≈ 2.449 → 50*2.449 ≈ 122.5 → 122.
        assert scale_max_examples(50, 300, baseline_corpus_size=50) == 122


# ---------------------------------------------------------------------------
# Integration: run_test_suite accepts the new parameters without error
# ---------------------------------------------------------------------------

class TestRunTestSuiteAcceptsScalingParams:
    """Verify the new kwargs are wired correctly. Doesn't assert on
    coverage (DummyRunners don't have real Hypothesis strategies
    mapped); just that the call succeeds and the params don't raise."""

    def test_kwargs_accepted_in_static_mode(self, tmp_path):
        from tests.test_orchestrator_mocked import (
            AgreeingRunner,
            fixture_seeds as _fixture_seeds_factory,
        )
        # Re-construct the seeds fixture inline (pytest fixture functions
        # aren't directly callable across modules).
        seeds = tmp_path / "seeds"
        (seeds / "vcf").mkdir(parents=True)
        (seeds / "sam").mkdir(parents=True)
        live = Path(__file__).parent.parent / "seeds"
        for n in ("minimal_single.vcf", "minimal_multisample.vcf",
                 "spec_example.vcf"):
            src = live / "vcf" / n
            if src.exists():
                (seeds / "vcf" / n).write_bytes(src.read_bytes())

        import json as _json
        reg = tmp_path / "reg.json"
        reg.write_text(_json.dumps({
            "enforced": [{
                "mr_id": "fix1",
                "mr_name": "fix1",
                "scope": "VCF.record",
                "preconditions": [],
                "transform_steps": ["shuffle_info_field_kv"],
                "oracle": "",
                "evidence": [],
            }],
            "quarantine": [],
            "summary": {"total": 1, "enforced_count": 1, "quarantine_count": 0},
        }), encoding="utf-8")

        result = run_test_suite(
            runners=[AgreeingRunner("a"), AgreeingRunner("b")],
            registry_path=reg,
            seeds_dir=seeds,
            output_dir=tmp_path / "bugs",
            format_filter="VCF",
            use_hypothesis=False,                          # static path
            max_examples=50,
            max_examples_corpus_scaling=True,              # new — should be no-op in static mode
            max_examples_baseline_corpus_size=10,
            max_examples_cap=200,
        )
        # Static mode: 1 MR × 3 seeds × 2 runners = 6 metamorphic + 3 differential = 9.
        # The exact count isn't important here; we're verifying the call
        # didn't blow up on the new kwargs.
        assert result.total_tests > 0
