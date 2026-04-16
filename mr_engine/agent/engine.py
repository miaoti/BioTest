"""
Agent orchestration: create ReAct agent, run MR mining, handle retry loop.

The agent uses LangGraph's create_react_agent with the query_spec_database
tool. On Pydantic validation failure, the error is fed back to the agent
for self-correction (up to MAX_VALIDATION_RETRIES attempts).
"""

from __future__ import annotations

import logging
import time
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
    blindspot_context: str | None = None,
):
    """
    Create a configured ReAct agent for MR mining.

    Args:
        target: Behavior target to investigate.
        spec_format: "VCF" or "SAM".
        llm: LangChain model instance. If None, loads from environment.
        blindspot_context: Optional Phase D blindspot guidance to append.

    Returns:
        A LangGraph Runnable agent.
    """
    if llm is None:
        llm = get_llm()

    system_prompt = build_system_prompt(target, spec_format, blindspot_context)

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
    blindspot_context: str | None = None,
) -> CompilationResult:
    """
    Full MR mining pipeline: agent -> validate -> retry on failure.

    Args:
        target: Behavior target category.
        spec_format: "VCF" or "SAM".
        llm: Optional pre-configured LLM instance.
        blindspot_context: Optional Phase D blindspot guidance.

    Returns:
        CompilationResult with validated MRs or final errors.
    """
    agent = create_mr_agent(target, spec_format, llm, blindspot_context)
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
            # Sample a few real chunk_ids to anchor the model
            sample_ids = _sample_chunk_ids(spec_index, spec_format, n=5)
            sample_hint = (
                f"\n\nHere are {len(sample_ids)} REAL chunk_ids from ChromaDB for {spec_format} "
                f"(use these exact strings or call query_spec_database to find more):\n"
                + "\n".join(f"  {cid}" for cid in sample_ids)
            ) if sample_ids else ""
            correction_msg = (
                f"Your previous output failed validation:\n\n"
                f"{compilation.error_detail}\n\n"
                f"IMPORTANT: For each evidence entry, you MUST use the exact 'chunk_id' "
                f"string returned by query_spec_database. The format is: "
                f"'VCFv4.5.tex::{{Exact Section Title}}::p{{N}}' — do NOT substitute "
                f"generic names like 'Section 3' or 'Header'."
                f"{sample_hint}\n\n"
                f"Call query_spec_database again to get valid chunk_ids, then copy verbatim. "
                f"Return corrected JSON only."
            )
            messages = [HumanMessage(content=correction_msg)]

        # Run agent (with rate limit retry + tool_use_failed recovery)
        raw_output: str | None = None
        try:
            result = agent.invoke({"messages": messages})
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "quota" in err_str or "503" in err_str:
                wait = 60
                logger.warning("Rate limited, waiting %ds before retry...", wait)
                time.sleep(wait)
                try:
                    result = agent.invoke({"messages": messages})
                except Exception as e2:
                    return CompilationResult(
                        success=False,
                        error_detail=f"API error after rate-limit retry: {e2}",
                    )
            elif "tool_use_failed" in err_str or "failed_generation" in str(e):
                # Some models (e.g. Llama 4 Scout) emit the final JSON as a
                # function-call body instead of plain text.  Groq returns a 400
                # with the generated content in the error payload — rescue it.
                raw_output = _extract_from_tool_use_error(e)
                if raw_output:
                    logger.info(
                        "Rescued JSON from tool_use_failed error (attempt %d)", attempt + 1
                    )
                    result = None  # skip normal extraction below
                else:
                    return CompilationResult(
                        success=False,
                        error_detail=f"Agent invocation error: {e}",
                    )
            else:
                return CompilationResult(
                    success=False,
                    error_detail=f"Agent invocation error: {e}",
                )

        # Extract JSON from the agent's final response
        if raw_output is None:
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


def _sample_chunk_ids(spec_index, spec_format: str, n: int = 5) -> list[str]:
    """Return n real chunk_ids from ChromaDB for the given format."""
    try:
        fmt = spec_format.upper()
        result = spec_index._collection.query(
            query_texts=[f"{fmt} ordering invariance normative rules"],
            n_results=n,
            where={"format": fmt} if fmt in ("VCF", "SAM") else None,
            include=[],
        )
        return result["ids"][0] if result and result["ids"] else []
    except Exception:
        return []


def _extract_from_tool_use_error(exc: Exception) -> str | None:
    """
    Some models (e.g. Llama 4 Scout on Groq) emit the final JSON answer as a
    function-call body, causing a 400 tool_use_failed error. The actual
    generated text is embedded in the error response under 'failed_generation'.
    This function extracts it so the compiler can still validate the MRs.
    """
    import re as _re

    err_str = str(exc)
    # The error body contains 'failed_generation': '...' or "failed_generation": "..."
    match = _re.search(r"'failed_generation':\s*'(.*)'", err_str, _re.DOTALL)
    if not match:
        match = _re.search(r'"failed_generation":\s*"(.*)"', err_str, _re.DOTALL)
    if match:
        raw = match.group(1)
        # Unescape common escape sequences from the repr
        raw = raw.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')
        return raw.strip()
    return None
