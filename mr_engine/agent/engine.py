"""
Agent orchestration: create ReAct agent, run MR mining, handle retry loop.

The agent uses LangGraph's create_react_agent with the query_spec_database
tool. On Pydantic validation failure, the error is fed back to the agent
for self-correction (up to MAX_VALIDATION_RETRIES attempts).
"""

from __future__ import annotations

import logging
from typing import Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from mr_engine.llm_factory import get_llm
from mr_engine.behavior import BehaviorTarget
from mr_engine.agent.tools import query_spec_database, get_spec_index
from mr_engine.agent.prompts import build_system_prompt
from mr_engine.dsl.compiler import compile_mr_output, CompilationResult

logger = logging.getLogger(__name__)

MAX_VALIDATION_RETRIES = 3


def create_mr_agent(
    target: BehaviorTarget,
    spec_format: str,
    llm: BaseChatModel | None = None,
):
    """
    Create a configured ReAct agent for MR mining.

    Args:
        target: Behavior target to investigate.
        spec_format: "VCF" or "SAM".
        llm: LangChain model instance. If None, loads from environment.

    Returns:
        A LangGraph Runnable agent.
    """
    if llm is None:
        llm = get_llm()

    system_prompt = build_system_prompt(target, spec_format)

    agent = create_react_agent(
        model=llm,
        tools=[query_spec_database],
        prompt=system_prompt,
    )
    return agent


def mine_mrs(
    target: BehaviorTarget,
    spec_format: str,
    llm: BaseChatModel | None = None,
) -> CompilationResult:
    """
    Full MR mining pipeline: agent -> validate -> retry on failure.

    Args:
        target: Behavior target category.
        spec_format: "VCF" or "SAM".
        llm: Optional pre-configured LLM instance.

    Returns:
        CompilationResult with validated MRs or final errors.
    """
    agent = create_mr_agent(target, spec_format, llm)
    spec_index = get_spec_index()

    user_message = (
        f"Find metamorphic relations for {spec_format} testing "
        f"targeting {target.value}. Query the spec database for evidence."
    )

    compilation: CompilationResult | None = None

    for attempt in range(MAX_VALIDATION_RETRIES + 1):
        if attempt == 0:
            logger.info(
                "Mining MRs: format=%s, target=%s (attempt %d)",
                spec_format, target.value, attempt + 1,
            )
            messages = [HumanMessage(content=user_message)]
        else:
            logger.info(
                "Retry %d/%d: feeding validation error back to agent",
                attempt, MAX_VALIDATION_RETRIES,
            )
            correction_msg = (
                f"Your previous output failed validation:\n\n"
                f"{compilation.error_detail}\n\n"
                f"Please fix the issues and return corrected JSON only."
            )
            messages = [HumanMessage(content=correction_msg)]

        # Run agent
        result = agent.invoke({"messages": messages})

        # Extract JSON from the agent's final response
        raw_output = _extract_text_from_response(result)
        logger.debug("Agent raw output (attempt %d):\n%s", attempt + 1, raw_output[:500])

        # Compile: validate + hydrate + hash
        compilation = compile_mr_output(raw_output, spec_index)

        if compilation.success:
            logger.info(
                "Successfully compiled %d MRs on attempt %d",
                len(compilation.relations), attempt + 1,
            )
            return compilation

        logger.warning(
            "Compilation failed (attempt %d): %s",
            attempt + 1, compilation.error_detail[:200],
        )

    # Return last failed result
    return compilation  # type: ignore[return-value]


def _extract_text_from_response(agent_result: dict) -> str:
    """Extract text content from the agent's final message."""
    messages = agent_result.get("messages", [])
    # Walk backwards to find the last AI message with content
    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        if content and isinstance(content, str) and content.strip():
            return content
    return ""
