"""
Phase 6 tests — seeds/minimize_corpus.py.

Key invariants:
- Tier-1 seeds (hand-curated) are NEVER pruned — operator-chosen
  contract per the plan; debugging anchors stay intact.
- The greedy cover preserves the edge union across kept seeds.
- `--i-understand-this-is-an-approximation` is required for live runs.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from seeds.minimize_corpus import (
    _is_candidate_for_pruning,
    _greedy_minimum_cover,
    MINIMIZE_SCOPE,
)


class TestTierOnePreservation:
    @pytest.mark.parametrize("name", [
        "spec_example.sam",
        "minimal_tags.sam",
        "complex_cigar.sam",
        "minimal_single.vcf",
        "minimal_multisample.vcf",
        "htsjdk_coordinate_sorted.sam",
    ])
    def test_tier1_seeds_are_never_candidates(self, name):
        # Hand-curated (no real_world_ / synthetic_ prefix) — never pruned.
        p = REPO_ROOT / "seeds" / "sam" / name
        assert not _is_candidate_for_pruning(p)

    @pytest.mark.parametrize("name", [
        "real_world_htslib_ce_1.sam",
        "real_world_bcftools_view.vcf",
        "synthetic_iter3_abc123.vcf",
    ])
    def test_tier2_synthetic_seeds_are_candidates(self, name):
        p = REPO_ROOT / "seeds" / "sam" / name
        assert _is_candidate_for_pruning(p)

    def test_minimize_scope_is_exactly_two_prefixes(self):
        # Future edits that widen MINIMIZE_SCOPE should be deliberate
        # — lock the operator-chosen policy.
        assert MINIMIZE_SCOPE == frozenset({"real_world_", "synthetic_"})


class TestGreedyCover:
    def test_picks_seed_with_max_unique_edges(self):
        # Three seeds, two distinct edges, one common edge.
        # Optimal cover = {seed_a, seed_b}.
        seed_a = Path("a")
        seed_b = Path("b")
        seed_c = Path("c")
        per_seed = {
            seed_a: {"file.py:1", "file.py:2"},
            seed_b: {"file.py:3", "file.py:2"},
            seed_c: {"file.py:2"},  # strictly redundant
        }
        kept = _greedy_minimum_cover(per_seed)
        assert seed_c not in kept
        assert seed_a in kept
        assert seed_b in kept

    def test_empty_input_returns_empty_set(self):
        assert _greedy_minimum_cover({}) == set()

    def test_preserves_edge_union(self):
        seeds = {
            Path("a"): {"1", "2", "3"},
            Path("b"): {"2", "4"},
            Path("c"): {"5"},
        }
        kept = _greedy_minimum_cover(seeds)
        kept_union = set().union(*(seeds[p] for p in kept))
        full_union = set().union(*seeds.values())
        assert kept_union == full_union


class TestCLI:
    def test_live_run_requires_ack_flag(self, tmp_path):
        # Live run without --dry-run AND without the ack flag must exit 2.
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "seeds" / "minimize_corpus.py"),
             "--seeds-dir", str(tmp_path)],
            capture_output=True, text=True,
        )
        assert res.returncode == 2
        assert "requires" in res.stderr.lower()

    def test_dry_run_does_not_require_ack(self, tmp_path):
        # Dry-run must NOT require the ack flag (safe-to-preview contract).
        (tmp_path / "sam").mkdir()
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "seeds" / "minimize_corpus.py"),
             "--dry-run", "--seeds-dir", str(tmp_path)],
            capture_output=True, text=True,
        )
        assert res.returncode == 0
