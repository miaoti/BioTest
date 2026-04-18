"""
Unit tests for the majority-voting consensus oracle.

Covers the four bucket-counting cases:
  1. Strict majority wins.
  2. Tie broken by authoritative (htslib) voter.
  3. Tie with no authority → inconclusive.
  4. htslib rejected-as-invalid signal surfaces.
"""

from __future__ import annotations

from test_engine.oracles.consensus import (
    AUTHORITATIVE_PARSERS,
    EXCLUDED_FROM_CONSENSUS,
    ConsensusResult,
    build_eligibility_map,
    get_consensus_output,
)
from test_engine.runners.base import ParserRunner, RunnerResult


def _res(name: str, value: dict | None = None, error_type: str | None = None, stderr: str = "") -> RunnerResult:
    return RunnerResult(
        success=value is not None,
        canonical_json=value,
        parser_name=name,
        format_type="VCF",
        error_type=error_type,
        stderr=stderr,
    )


class _FakeRunner:
    """Stub for build_eligibility_map — it only reads name + supported_formats."""
    def __init__(self, name: str, formats: set[str]):
        self.name = name
        self.supported_formats = formats


def test_strict_majority_wins():
    """3/4 parsers agree — consensus is the majority value; dissenter recorded."""
    a = {"x": 1}
    b = {"x": 2}
    outputs = {
        "htsjdk": _res("htsjdk", a),
        "pysam": _res("pysam", a),
        "biopython": _res("biopython", a),
        "seqan3": _res("seqan3", b),
    }
    cons = get_consensus_output(outputs)
    assert not cons.is_inconclusive
    assert cons.consensus_value == a
    assert set(cons.winning_voters) == {"htsjdk", "pysam", "biopython"}
    assert cons.dissenting_voters == ["seqan3"]
    assert not cons.htslib_rejected_as_invalid


def test_htslib_breaks_tie():
    """2 vs 2 with htslib in one bucket → htslib's bucket wins."""
    a = {"x": 1}
    b = {"x": 2}
    outputs = {
        "htsjdk": _res("htsjdk", a),
        "pysam": _res("pysam", a),
        "biopython": _res("biopython", b),
        "htslib": _res("htslib", b),
    }
    cons = get_consensus_output(outputs)
    assert not cons.is_inconclusive
    assert cons.consensus_value == b
    assert "htslib" in cons.winning_voters
    assert set(cons.winning_voters) == {"htslib", "biopython"}
    assert "htsjdk tie-breaker" in cons.reason or "htslib tie-breaker" in cons.reason


def test_three_way_split_without_htslib_is_inconclusive():
    """3-way split with no authority → is_inconclusive=True."""
    outputs = {
        "htsjdk": _res("htsjdk", {"x": 1}),
        "pysam": _res("pysam", {"x": 2}),
        "seqan3": _res("seqan3", {"x": 3}),
    }
    cons = get_consensus_output(outputs)
    assert cons.is_inconclusive
    assert cons.consensus_value is None


def test_reference_runner_is_a_regular_voter():
    """The reference normalizer is an independent implementation and
    votes alongside the real SUTs (see EXCLUDED_FROM_CONSENSUS doc)."""
    assert "reference" not in EXCLUDED_FROM_CONSENSUS
    outputs = {
        "htsjdk": _res("htsjdk", {"x": 1}),
        "pysam": _res("pysam", {"x": 2}),
        "reference": _res("reference", {"x": 1}),
    }
    cons = get_consensus_output(outputs)
    # reference + htsjdk → 2/3 majority, pysam dissents.
    assert not cons.is_inconclusive
    assert cons.consensus_value == {"x": 1}
    assert set(cons.winning_voters) == {"htsjdk", "reference"}
    assert cons.dissenting_voters == ["pysam"]


def test_htslib_invalid_signal():
    """htslib error with 'invalid' in stderr sets htslib_rejected_as_invalid."""
    outputs = {
        "htsjdk": _res("htsjdk", {"x": 1}),
        "pysam": _res("pysam", {"x": 1}),
        "htslib": _res("htslib", error_type="parse_error", stderr="Invalid VCF header"),
    }
    cons = get_consensus_output(outputs)
    assert cons.htslib_rejected_as_invalid
    # Remaining voters (htsjdk+pysam) agree → still a 2/2 majority among voters
    assert not cons.is_inconclusive
    assert cons.consensus_value == {"x": 1}
    assert "htslib" in cons.failing_parsers


def test_all_failures_is_inconclusive():
    outputs = {
        "htsjdk": _res("htsjdk", error_type="crash", stderr="boom"),
        "pysam": _res("pysam", error_type="crash", stderr="boom"),
    }
    cons = get_consensus_output(outputs)
    assert cons.is_inconclusive
    assert set(cons.failing_parsers) == {"htsjdk", "pysam"}


def test_single_voter_trivially_consensus():
    """A lone voter's value is consensus (edge case for len(results) < 2 upstream)."""
    outputs = {"pysam": _res("pysam", {"x": 1})}
    cons = get_consensus_output(outputs)
    assert not cons.is_inconclusive
    assert cons.consensus_value == {"x": 1}
    assert cons.winning_voters == ["pysam"]


def test_parser_matches_consensus_helper():
    a = {"x": 1}
    b = {"x": 2}
    outputs = {
        "htsjdk": _res("htsjdk", a),
        "pysam": _res("pysam", a),
        "biopython": _res("biopython", b),
    }
    cons = get_consensus_output(outputs)
    assert cons.parser_matches_consensus("htsjdk") is True
    assert cons.parser_matches_consensus("biopython") is False
    # Non-voter should return None
    assert cons.parser_matches_consensus("reference") is None


def test_authoritative_parsers_includes_htslib():
    """Guard against accidental rename of the authoritative tuple."""
    assert "htslib" in AUTHORITATIVE_PARSERS


# ---------------------------------------------------------------------------
# Format-Aware Eligibility
# ---------------------------------------------------------------------------

def test_self_reported_ineligible_is_dropped():
    """A runner that returned error_type='ineligible' must not count as a vote."""
    outputs = {
        "htsjdk": _res("htsjdk", {"x": 1}),
        "pysam": _res("pysam", {"x": 1}),
        "biopython": _res("biopython", error_type="ineligible",
                          stderr="Biopython only supports SAM format"),
    }
    cons = get_consensus_output(outputs, format_context="VCF")
    assert "biopython" in cons.ineligible_parsers
    assert "biopython" not in cons.dissenting_voters
    assert "biopython" not in cons.failing_parsers
    # The two remaining parsers agree → clean 2/2 majority.
    assert not cons.is_inconclusive
    assert cons.consensus_value == {"x": 1}


def test_capability_map_filter_drops_sam_only_parser_on_vcf():
    """Even if biopython returns a (nonsensical) canonical_json, the map
    drops it when running VCF tests — biopython's supported_formats
    does not include VCF."""
    outputs = {
        "htsjdk": _res("htsjdk", {"x": 1}),
        "pysam": _res("pysam", {"x": 1}),
        "biopython": _res("biopython", {"x": 2}),   # hallucinated vote
        "seqan3": _res("seqan3", {"x": 3}),         # hallucinated vote
    }
    caps = {
        "htsjdk": {"VCF", "SAM"},
        "pysam": {"VCF", "SAM"},
        "biopython": {"SAM"},
        "seqan3": {"SAM"},
    }
    cons = get_consensus_output(outputs, format_context="VCF", eligibility_map=caps)
    assert set(cons.ineligible_parsers) == {"biopython", "seqan3"}
    # Only VCF-capable parsers vote: both agree → majority.
    assert not cons.is_inconclusive
    assert cons.consensus_value == {"x": 1}
    # Phantom "different" votes must not leak in as dissent.
    assert cons.dissenting_voters == []


def test_sam_run_silences_vcf_only_parsers_symmetrically():
    """Running SAM, a hypothetical VCF-only parser would be silent too."""
    outputs = {
        "biopython": _res("biopython", {"s": 1}),
        "seqan3": _res("seqan3", {"s": 1}),
        "htsjdk": _res("htsjdk", {"s": 1}),
        "vcfonly": _res("vcfonly", {"s": 42}),
    }
    caps = {
        "biopython": {"SAM"},
        "seqan3": {"SAM"},
        "htsjdk": {"VCF", "SAM"},
        "vcfonly": {"VCF"},
    }
    cons = get_consensus_output(outputs, format_context="SAM", eligibility_map=caps)
    assert "vcfonly" in cons.ineligible_parsers
    assert cons.consensus_value == {"s": 1}


def test_empty_format_context_preserves_legacy_behavior():
    """Backward compat: when format_context is empty, every non-excluded
    runner that produced a canonical_json votes as before."""
    outputs = {
        "a": _res("a", {"x": 1}),
        "b": _res("b", {"x": 1}),
        "c": _res("c", {"x": 2}),
    }
    # Even with a capability map, no format → no filter.
    caps = {"a": {"VCF"}, "b": {"VCF"}, "c": {"SAM"}}
    cons = get_consensus_output(outputs, format_context="", eligibility_map=caps)
    assert cons.ineligible_parsers == []
    assert not cons.is_inconclusive


def test_build_eligibility_map_reads_runner_attributes():
    runners = [
        _FakeRunner("htsjdk", {"VCF", "SAM"}),
        _FakeRunner("biopython", {"SAM"}),
        _FakeRunner("seqan3", {"SAM"}),
        _FakeRunner("htslib", {"VCF", "SAM"}),
    ]
    caps = build_eligibility_map(runners)
    assert caps["htsjdk"] == {"VCF", "SAM"}
    assert caps["biopython"] == {"SAM"}
    assert caps["seqan3"] == {"SAM"}
    assert caps["htslib"] == {"VCF", "SAM"}


def test_parser_is_ineligible_helper():
    outputs = {
        "htsjdk": _res("htsjdk", {"x": 1}),
        "biopython": _res("biopython", error_type="ineligible", stderr="SAM only"),
    }
    cons = get_consensus_output(outputs, format_context="VCF")
    assert cons.parser_is_ineligible("biopython") is True
    assert cons.parser_is_ineligible("htsjdk") is False
    # Ineligible parsers must also return None for matches_consensus.
    assert cons.parser_matches_consensus("biopython") is None


def test_ineligible_parsers_do_not_trigger_htslib_invalid_signal():
    """htslib error with error_type='ineligible' (not 'parse_error') must
    NOT be treated as a malformed-input rejection."""
    outputs = {
        "htsjdk": _res("htsjdk", {"x": 1}),
        "pysam": _res("pysam", {"x": 1}),
        "htslib": _res("htslib", error_type="ineligible",
                       stderr="HTSlib CLI for BAM not found in PATH"),
    }
    cons = get_consensus_output(outputs, format_context="VCF")
    assert "htslib" in cons.ineligible_parsers
    assert cons.htslib_rejected_as_invalid is False
