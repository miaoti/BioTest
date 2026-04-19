"""
Unit tests for Phase 4 of the SAM coverage plan.

The reachability penalty sinks blindspot rules whose spec section
requires a capability the primary target does not declare. Covers:

- Tagged rule with a missing capability → +20 penalty.
- Tagged rule with the capability declared → 0 penalty.
- Untagged rule → 0 penalty regardless of capabilities.
- Empty config → filter disabled (every rule scores 0).
- Priority ordering: on-format unreachable still sinks below on-format
  reachable (reach_pen is a soft priority knob, not a hard drop).
"""
from __future__ import annotations

import pytest

from test_engine.feedback.blindspot_builder import (
    _prioritise_rules,
    _reachability_penalty,
)


RULE_SAM_INDEX = {
    "chunk_id": "SAMv1.tex::Basic binning index::p288",
    "severity": "CRITICAL",
    "section_id": "Basic binning index",
    "format": "SAM",
    "text_snippet": "",
}

RULE_SAM_ALIGNMENT = {
    "chunk_id": "SAMv1.tex::Alignment section::p050",
    "severity": "CRITICAL",
    "section_id": "Alignment section",
    "format": "SAM",
    "text_snippet": "",
}

RULE_VCF = {
    "chunk_id": "VCFv4.5.tex::Meta lines::p001",
    "severity": "CRITICAL",
    "section_id": "Meta lines",
    "format": "VCF",
    "text_snippet": "",
}

CAP_TAGS = {
    "index_io": ["binning index", "BAI", "CSI"],
    "cram_io": ["CRAM"],
}


def test_reachability_penalty_unreachable_rule():
    # Index-section rule with NO supporting capability — full penalty.
    assert _reachability_penalty(RULE_SAM_INDEX, CAP_TAGS, set()) == 20


def test_reachability_penalty_reachable_rule():
    # Same rule but the runner declares supports_index_io=True — no penalty.
    assert _reachability_penalty(
        RULE_SAM_INDEX, CAP_TAGS, {"index_io"}
    ) == 0


def test_reachability_penalty_untagged_rule():
    # "Alignment section" doesn't match any capability substring → 0.
    assert _reachability_penalty(RULE_SAM_ALIGNMENT, CAP_TAGS, set()) == 0


def test_reachability_penalty_empty_config_disables_filter():
    # No config at all — every rule must score 0.
    assert _reachability_penalty(RULE_SAM_INDEX, None, set()) == 0
    assert _reachability_penalty(RULE_SAM_INDEX, {}, set()) == 0


def test_priority_puts_reachable_above_unreachable():
    # Both rules are on-format SAM; only the binning rule is unreachable.
    rules = [RULE_SAM_INDEX, RULE_SAM_ALIGNMENT]
    ranked = _prioritise_rules(
        rules=rules,
        code_slices=[],
        format_context="SAM",
        rule_capability_tags=CAP_TAGS,
        supported_capabilities=set(),
    )
    # "Alignment section" (reachable) should be first; "Basic binning
    # index" (unreachable) second.
    assert ranked[0][0]["section_id"] == "Alignment section"
    assert ranked[1][0]["section_id"] == "Basic binning index"


def test_format_penalty_still_beats_reachability():
    # Off-format rule (fmt_pen=10) sinks below on-format unreachable
    # (reach_pen=20) only when fmt_pen > reach_pen. Current weights:
    # fmt_pen is the FIRST sort dimension, so a VCF rule in a SAM run
    # gets fmt_pen=10, which sorts BELOW a SAM rule with reach_pen=20
    # because (0,20) < (10,0) lexicographically. Lock this invariant.
    rules = [RULE_VCF, RULE_SAM_INDEX]
    ranked = _prioritise_rules(
        rules=rules,
        code_slices=[],
        format_context="SAM",
        rule_capability_tags=CAP_TAGS,
        supported_capabilities=set(),
    )
    # On-format unreachable wins over off-format reachable.
    assert ranked[0][0]["format"] == "SAM"
    assert ranked[1][0]["format"] == "VCF"
