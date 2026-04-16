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
) -> str:
    """
    Return the complete system prompt string for one mining run.

    Uses build_system_prompt_template() so the transforms menu is always
    derived from the live TRANSFORM_REGISTRY.

    Args:
        target:            The behavior target category to investigate.
        spec_format:       "VCF" or "SAM".
        blindspot_context: Optional Phase D blindspot guidance to append.

    Returns:
        Complete system prompt string (plain text, no LangChain objects).
    """
    template = build_system_prompt_template(spec_format=spec_format)
    messages = template.format_messages(
        spec_format=spec_format,
        behavior_target=target.value,
        behavior_description=get_system_prompt_fragment(target),
    )
    prompt = messages[0].content

    if blindspot_context:
        prompt += "\n\n" + blindspot_context

    return prompt
