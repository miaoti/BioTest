"""
System prompt construction for the MR mining agent.

All menu-generation and template logic lives in transforms_menu.py.
This module provides the string-valued wrapper used by engine.py.
"""

from __future__ import annotations

from mr_engine.behavior import BehaviorTarget, get_system_prompt_fragment
from mr_engine.agent.transforms_menu import build_system_prompt_template


def build_system_prompt(
    target: BehaviorTarget,
    spec_format: str,
    blindspot_context: str | None = None,
    primary_target: str = "",
    available_suts: list[str] | None = None,
    runtime_capabilities: set[str] | None = None,
) -> str:
    """
    Return the complete system prompt string for one mining run.

    Uses build_system_prompt_template() so the transforms menu is always
    derived from the live TRANSFORM_REGISTRY.

    Args:
        target:            The behavior target category to investigate.
        spec_format:       "VCF" or "SAM".
        blindspot_context: Optional Phase D blindspot guidance to append.
        primary_target:    Name of the SUT driving this run's feedback
                           loop (e.g. "htsjdk"). Surfaced as a hard
                           selection rule at the top of the prompt so
                           the LLM aligns SUT-specific transforms
                           (`htsjdk_write_roundtrip` vs
                           `pysam_vcf_write_roundtrip`) with the actual
                           target. Without this, the agent sees every
                           registered writer equally and picks any.
        available_suts:    SUT names currently available in the runtime
                           environment. Used to narrow the set of
                           SUT-specific transforms the agent can pick
                           from — transforms targeting an absent SUT
                           would otherwise no-op silently and waste an
                           MR slot.
        runtime_capabilities: Set of runtime-gated capability tags
                           (see `transforms_menu.KNOWN_RUNTIME_PRECONDITIONS`).
                           Transforms whose preconditions name a
                           known-runtime tag NOT in this set are hidden
                           from the menu entirely, so the LLM can't
                           propose a transform that would silently
                           no-op in the current environment.

    Returns:
        Complete system prompt string (plain text, no LangChain objects).
    """
    template = build_system_prompt_template(
        spec_format=spec_format,
        runtime_capabilities=runtime_capabilities,
    )
    messages = template.format_messages(
        spec_format=spec_format,
        behavior_target=target.value,
        behavior_description=get_system_prompt_fragment(target),
    )
    prompt = messages[0].content

    # Prepend the primary-target block so it's the first thing the agent
    # reads. Kept compact — the full transforms menu already describes
    # each individual transform's contextual hint + preconditions.
    header = _build_primary_target_block(primary_target, available_suts)
    if header:
        prompt = header + "\n\n" + prompt

    if blindspot_context:
        prompt += "\n\n" + blindspot_context

    return prompt


def _build_primary_target_block(
    primary_target: str,
    available_suts: list[str] | None,
) -> str:
    """Render the 'PRIMARY TARGET FOR THIS RUN' header block.

    Returns an empty string when no primary target is configured — in
    that legacy "test all SUTs equally" mode the old prompt shape is
    preserved so existing tests and behavior don't shift unexpectedly.
    """
    if not primary_target and not available_suts:
        return ""

    lines: list[str] = [
        "=" * 60,
        "PRIMARY TARGET FOR THIS RUN",
        "=" * 60,
    ]
    if primary_target:
        lines.append(
            f"The primary System Under Test is: **{primary_target}**. "
            "Coverage, SCC, and quarantine decisions are scored against "
            "this SUT specifically; other SUTs act as auxiliary voters "
            "in the consensus oracle."
        )
    if available_suts:
        lines.append(
            "Available SUTs in this runtime: "
            + ", ".join(sorted(available_suts))
            + "."
        )
    lines.extend([
        "",
        "WRITER-TRANSFORM NOTE:",
        "  - `sut_write_roundtrip` is a SUT-AGNOSTIC writer-roundtrip "
        "transform. It invokes whichever SUT the orchestrator has "
        "nominated as primary at Phase C time (via its "
        "`run_write_roundtrip` method). Use it freely for "
        "round_trip_invariance MRs — you do NOT need to pick per-SUT "
        "writer names; there's only ONE writer transform in the menu.",
        "  - All other transforms (shuffle_meta_lines, permute_ALT, "
        "vcf_bcf_round_trip, etc.) are pure text operations and SUT-"
        "agnostic. Propose them whenever the MR's semantics call for "
        "it, regardless of which SUT is primary.",
        "  - SUT availability matters only for result interpretation: "
        "SCC / coverage are scored against the PRIMARY target, so its "
        "pass/fail is what drives the feedback loop. Other SUTs' "
        "outputs are auxiliary voters in the consensus oracle.",
    ])
    return "\n".join(lines)
