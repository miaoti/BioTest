"""
HypoFuzz shim — Rank 7 coverage lever.

HypoFuzz (Zac Hatfield-Dodds, Hypothesis author; hypofuzz.com) plugs real
branch-coverage feedback into Hypothesis's strategy choices. Our main
`@given` test (`test_engine/orchestrator.py::_run_mr_with_hypothesis`)
lives inside an orchestrator closure that pytest can't discover, so this
file exposes top-level `@given`-decorated functions calling the same
dispatch path so HypoFuzz can drive them.

Run normally:   `pytest tests/test_hypofuzz_targets.py`     (Hypothesis only)
Run with HypoFuzz:  `python -m hypofuzz tests/test_hypofuzz_targets.py`
                    or `scripts/run_hypofuzz.py`

Reference:
- Hatfield-Dodds, Zac et al. *HypoFuzz: Adaptive Fuzzing for Hypothesis*
  — https://hypofuzz.com/, https://github.com/Zac-HD/hypofuzz
- Padhye, R., Lemieux, C., Sen, K., Serebryany, K., Sen, K. (2019).
  *JQF: Coverage-Guided Property-Based Testing in Java*. ISSTA'19,
  DOI 10.1145/3293882.3339002 — original Zest algorithm; HypoFuzz is
  the Python successor in the same family.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given, settings, HealthCheck, Phase

from test_engine.generators.seeds import SeedCorpus
from test_engine.generators.dispatch import apply_transform
from test_engine.canonical.vcf_normalizer import normalize_vcf_text
from test_engine.canonical.sam_normalizer import normalize_sam_text


SEEDS_DIR = Path(__file__).parent.parent / "seeds"
_CORPUS: SeedCorpus | None = None


def _corpus() -> SeedCorpus:
    """Lazy singleton — instantiate the corpus once per process."""
    global _CORPUS
    if _CORPUS is None:
        _CORPUS = SeedCorpus(SEEDS_DIR)
    return _CORPUS


# Skip everything if the corpus is empty (CI without fetched seeds).
_HAS_VCF = lambda: bool(_corpus().vcf_seeds)  # noqa: E731
_HAS_SAM = lambda: bool(_corpus().sam_seeds)  # noqa: E731


# ---------------------------------------------------------------------------
# Mirror a handful of the existing transforms as top-level @given tests.
# Each one lifts a strategy and runs the dispatch + reference normalizer
# through the same call path that the orchestrator's closure uses, but as
# a plain pytest test so HypoFuzz can discover + instrument it.
#
# The tests assert *parsability* of the transformed output — a strong
# universal invariant that all our framework transforms preserve. Coverage
# is the side-effect HypoFuzz drives.
# ---------------------------------------------------------------------------


def _vcf_strategy_factory():
    """Late-bind strategies so the corpus is loaded only when tests run."""
    from test_engine.generators.vcf_strategies import st_shuffle_meta_lines
    return st_shuffle_meta_lines(_corpus())


def _sam_strategy_factory():
    from test_engine.generators.sam_strategies import st_permute_optional_tags
    return st_permute_optional_tags(_corpus())


_FAST_SETTINGS = settings(
    max_examples=20,                                # CI-friendly default
    phases=[Phase.explicit, Phase.generate, Phase.target],
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
    deadline=None,
)


@pytest.mark.skipif(
    not (SEEDS_DIR / "vcf").exists() or not list((SEEDS_DIR / "vcf").glob("*.vcf")),
    reason="No VCF seeds present; HypoFuzz target skipped",
)
@_FAST_SETTINGS
@given(params=_vcf_strategy_factory())
def test_vcf_shuffle_meta_lines_keeps_parsable(params):
    """Rank-7 HypoFuzz target on shuffle_meta_lines.

    Invariant: the transformed VCF text must still parse through the
    framework's reference normalizer. HypoFuzz steers @given toward
    branch-coverage-rich examples; we use a fast settings() so the
    pytest run stays sub-second.
    """
    rng_seed = params["rng_seed"]
    lines = params["lines"]
    out = apply_transform("shuffle_meta_lines", lines, seed=rng_seed)
    # Must still parse — no exception
    normalize_vcf_text(out)


@pytest.mark.skipif(
    not (SEEDS_DIR / "sam").exists() or not list((SEEDS_DIR / "sam").glob("*.sam")),
    reason="No SAM seeds present; HypoFuzz target skipped",
)
@_FAST_SETTINGS
@given(params=_sam_strategy_factory())
def test_sam_permute_optional_tags_keeps_parsable(params):
    """Rank-7 HypoFuzz target on permute_optional_tag_fields."""
    rng_seed = params["rng_seed"]
    lines = params["lines"]
    out = apply_transform("permute_optional_tag_fields", lines, seed=rng_seed)
    normalize_sam_text(out)
