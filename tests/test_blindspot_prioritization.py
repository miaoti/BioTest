"""
Unit tests for the prioritized-queue refactor of blindspot_builder.

Covers:
  - _complexity_score grows with length + keyword density.
  - _proximity_score is non-zero only when rule tokens overlap slice tokens.
  - _format_penalty zeros an on-format rule and penalises off-format.
  - _prioritise_rules applies (fmt, -complexity, -proximity, sev) order.
  - build_blindspot_ticket respects max_rules_per_iteration and surfaces
    total/shown/remaining counters.
  - to_prompt_fragment embeds the FOCUS DIRECTIVE and queue counters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from test_engine.feedback.blindspot_builder import (
    BlindspotTicket,
    CodeSlice,
    _build_slice_token_set,
    _complexity_score,
    _format_penalty,
    _prioritise_rules,
    _proximity_score,
    build_blindspot_ticket,
)
from test_engine.feedback.coverage_collector import CoverageResult
from test_engine.feedback.scc_tracker import SCCReport


# ---------------------------------------------------------------------------
# Scoring primitives
# ---------------------------------------------------------------------------

def test_complexity_score_monotonic_in_length():
    short = {"spec_text": "The parser must accept lowercase chromosomes."}
    long_ = {
        "spec_text": (
            "The parser must accept lowercase chromosomes. When the input "
            "contains ambiguous entries, the parser shall split them into "
            "separate records unless the user explicitly disables splitting. "
            "Additionally, parsers should preserve ordering except when "
            "required by Section 1.6.2; see § 3."
        )
    }
    assert _complexity_score(long_) > _complexity_score(short)


def test_complexity_score_rewards_keywords():
    plain = {"spec_text": "Hello world, this is a benign sentence." * 3}
    dense = {
        "spec_text": (
            "MUST be parsed. SHALL be normalized. REQUIRED field. "
            "When Number=A the array must carry per-alt values. "
            "Only if the BCF dictionary is present."
        )
    }
    assert _complexity_score(dense) > _complexity_score(plain)


def test_complexity_score_empty_rule():
    assert _complexity_score({}) == 0
    assert _complexity_score({"spec_text": ""}) == 0


def test_proximity_score_finds_overlap():
    rule = {"spec_text": "BCF dictionary indices MUST be remapped on write."}
    slice_tokens = {"bcfheader", "dictionary", "remap", "vcfwriter", "indices"}
    assert _proximity_score(rule, slice_tokens) > 0.0


def test_proximity_score_zero_when_no_overlap():
    rule = {"spec_text": "Phased genotypes are separated by pipe characters."}
    slice_tokens = {"filelock", "compression", "gzipinputstream"}
    assert _proximity_score(rule, slice_tokens) == 0.0


def test_proximity_score_empty_slice_set_is_zero():
    rule = {"spec_text": "anything"}
    assert _proximity_score(rule, set()) == 0.0


def test_format_penalty_matches_and_mismatches():
    assert _format_penalty({"format": "VCF"}, "VCF") == 0
    assert _format_penalty({"format": "SAM"}, "VCF") == 10
    # Empty format_context → no filter applied.
    assert _format_penalty({"format": "SAM"}, "") == 0


# ---------------------------------------------------------------------------
# Priority sort integration
# ---------------------------------------------------------------------------

def _rule(chunk_id: str, severity: str, text: str, fmt: str = "VCF") -> dict:
    return {
        "chunk_id": chunk_id,
        "severity": severity,
        "section_id": chunk_id.split("::")[-2] if "::" in chunk_id else "",
        "format": fmt,
        "text_snippet": text,
    }


def test_format_penalty_outranks_complexity():
    """A complex SAM rule should lose to a simple VCF rule in a VCF context."""
    simple_vcf = _rule("vcf::simple::p1", "CRITICAL", "Line parser must accept ##fileformat.", "VCF")
    complex_sam = _rule(
        "sam::complex::p1", "CRITICAL",
        ("The SAM specification defines multiple optional tags and requires "
         "that parsers handle hard-clip, soft-clip, and deletion operators "
         "consistently when CIGAR strings span long regions. When Number=A "
         "style rules conflict, the parser must pick the max cardinality."),
        fmt="SAM",
    )
    ranked = _prioritise_rules([complex_sam, simple_vcf], [], "VCF")
    assert ranked[0][0] is simple_vcf
    assert ranked[1][0] is complex_sam


def test_complexity_breaks_ties_within_format():
    short_vcf = _rule("vcf::short::p1", "CRITICAL", "BCF rule.", "VCF")
    long_vcf = _rule(
        "vcf::long::p2", "CRITICAL",
        ("The BCF codec MUST preserve dictionary ordering when the writer "
         "emits sequences; additionally, SHALL re-index references and "
         "REQUIRED to honor Number=A. When xref § 6.2.1 applies, see "
         "Section 4."),
        "VCF",
    )
    ranked = _prioritise_rules([short_vcf, long_vcf], [], "VCF")
    assert ranked[0][0] is long_vcf


def test_proximity_breaks_ties_at_equal_complexity():
    text = "The parser MUST preserve ordering and parse records correctly."
    proximal = _rule("vcf::prox::p1", "CRITICAL", text + " BCF dictionary.", "VCF")
    distant = _rule("vcf::dist::p2", "CRITICAL", text + " Unrelated phrase.", "VCF")
    code_slices = [CodeSlice(
        file_label="BCFDictionaryCodec.java",
        line_start=100, line_end=110,
        source_lines=["void writeDictionary(BCFDictionary dict) {"] * 10,
    )]
    ranked = _prioritise_rules([distant, proximal], code_slices, "VCF")
    # Proximal rule should beat the distant one.
    assert ranked[0][0] is proximal


# ---------------------------------------------------------------------------
# Builder-level integration
# ---------------------------------------------------------------------------

def test_top_k_windowing_and_queue_counters(tmp_path):
    # Build 20 fake uncovered rules all in VCF format.
    blind = [
        _rule(f"vcf::r{i}::p1", "CRITICAL", f"Rule {i} MUST do something.", "VCF")
        for i in range(20)
    ]
    scc = SCCReport(
        total_rules=20,
        covered_count=0,
        scc_percent=0.0,
        blind_spots=[r["chunk_id"] for r in blind],
        blind_spot_details=blind,
    )

    ticket = build_blindspot_ticket(
        scc_report=scc,
        coverage_results=[],
        existing_mr_ids=[],
        spec_index=None,
        iteration=1,
        primary_target="htsjdk",
        source_roots=None,
        format_context="VCF",
        max_rules_per_iteration=5,
    )

    assert ticket.total_uncovered == 20
    assert ticket.shown_uncovered == 5
    assert ticket.remaining_uncovered == 15
    assert len(ticket.uncovered_rules) == 5
    assert len(ticket.rule_scores) == 5
    # The shown rules must each appear in the original queue.
    shown_ids = {r["chunk_id"] for r in ticket.uncovered_rules}
    orig_ids = {r["chunk_id"] for r in blind}
    assert shown_ids <= orig_ids


def test_prompt_fragment_contains_focus_directive_and_counters():
    blind = [
        _rule(f"vcf::r{i}::p1", "CRITICAL", f"Rule {i} MUST do something.", "VCF")
        for i in range(8)
    ]
    scc = SCCReport(
        total_rules=8,
        covered_count=0,
        scc_percent=0.0,
        blind_spots=[r["chunk_id"] for r in blind],
        blind_spot_details=blind,
    )
    ticket = build_blindspot_ticket(
        scc_report=scc,
        coverage_results=[],
        existing_mr_ids=[],
        spec_index=None,
        iteration=2,
        primary_target="htsjdk",
        source_roots=None,
        format_context="VCF",
        max_rules_per_iteration=3,
    )
    frag = ticket.to_prompt_fragment()
    assert "Total Blindspots = 8" in frag
    assert "Injecting Top 3" in frag
    assert "5 rules remaining" in frag
    assert "FOCUS DIRECTIVE" in frag
    assert "EXCLUSIVELY" in frag
    # Iteration number surfaces.
    assert "iteration 2" in frag


def test_empty_queue_renders_empty_fragment():
    scc = SCCReport(
        total_rules=0,
        covered_count=0,
        scc_percent=100.0,
        blind_spots=[],
        blind_spot_details=[],
    )
    ticket = build_blindspot_ticket(
        scc_report=scc,
        coverage_results=[],
        existing_mr_ids=[],
        spec_index=None,
        iteration=1,
        primary_target="htsjdk",
        source_roots=None,
        format_context="VCF",
        max_rules_per_iteration=5,
    )
    # Nothing to show — prompt fragment should be empty.
    assert ticket.total_uncovered == 0
    assert ticket.shown_uncovered == 0
    assert ticket.remaining_uncovered == 0
    assert ticket.to_prompt_fragment() == ""


def test_max_rules_larger_than_queue_does_not_overshoot():
    blind = [_rule(f"vcf::r{i}", "CRITICAL", f"R{i}", "VCF") for i in range(3)]
    scc = SCCReport(
        total_rules=3,
        covered_count=0,
        scc_percent=0.0,
        blind_spots=[r["chunk_id"] for r in blind],
        blind_spot_details=blind,
    )
    ticket = build_blindspot_ticket(
        scc_report=scc,
        coverage_results=[],
        existing_mr_ids=[],
        spec_index=None,
        iteration=1,
        primary_target="htsjdk",
        source_roots=None,
        format_context="VCF",
        max_rules_per_iteration=50,
    )
    assert ticket.shown_uncovered == 3
    assert ticket.remaining_uncovered == 0
