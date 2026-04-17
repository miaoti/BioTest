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
    # Once the ReAct agent hits recursion-limit on a given run we stop
    # retrying through it (the local model will just loop again). Switch
    # to single-shot synthesis for all remaining attempts.
    react_is_broken = False

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

        # Run agent (with rate limit retry + tool_use_failed recovery).
        # recursion_limit caps the number of ReAct tool-call hops per attempt;
        # without it, slow local LLMs can spend 10+ min looping before hitting
        # LangGraph's default of 25. 25 is enough for thorough spec lookup on
        # harder themes (compound transforms, nuanced rules) that need several
        # query_spec_database calls to anchor evidence.
        raw_output: str | None = None
        result = None

        if react_is_broken:
            # Skip the ReAct agent entirely — go straight to synthesis.
            # This avoids burning another 3+ minutes in the broken loop.
            logger.info(
                "Attempt %d: skipping ReAct (earlier recursion failure), "
                "going direct to synthesis fallback.",
                attempt + 1,
            )
            raw_output = _synthesize_from_recursion_failure(
                None, target, spec_format, blindspot_context, llm
            )
            if not raw_output:
                compilation = CompilationResult(
                    success=False,
                    error_detail=(
                        "Synthesis fallback produced no output "
                        "(ReAct already failed with recursion limit)."
                    ),
                )
                continue
            # Fall through to compilation step below (raw_output set,
            # result stays None so normal extraction is skipped).
        else:
          try:
            result = agent.invoke(
                {"messages": messages},
                config={"recursion_limit": 25},
            )
          except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate" in err_str or "quota" in err_str or "503" in err_str:
                wait = 60
                logger.warning(
                    "Rate limited on attempt %d (%s), waiting %ds before retry...",
                    attempt + 1, type(e).__name__, wait,
                )
                time.sleep(wait)
                try:
                    result = agent.invoke(
                        {"messages": messages},
                        config={"recursion_limit": 25},
                    )
                except Exception as e2:
                    logger.warning(
                        "Agent error after rate-limit retry on attempt %d: %s",
                        attempt + 1, e2,
                    )
                    # Feed this into the retry loop instead of bailing out.
                    compilation = CompilationResult(
                        success=False,
                        error_detail=f"API error after rate-limit retry: {e2}",
                    )
                    continue
            elif "tool_use_failed" in err_str or "failed_generation" in str(e):
                # Some models (e.g. Llama 4 Scout) emit the final JSON as a
                # function-call body instead of plain text.  Groq returns a 400
                # with the generated content in the error payload — rescue it.
                raw_output = _extract_from_tool_use_error(e)
                if raw_output:
                    logger.info(
                        "Rescued JSON from tool_use_failed error (attempt %d)", attempt + 1
                    )
                    result = None
                else:
                    logger.warning(
                        "tool_use_failed on attempt %d with no recoverable JSON: %s",
                        attempt + 1, str(e)[:200],
                    )
                    compilation = CompilationResult(
                        success=False,
                        error_detail=f"tool_use_failed (unrecoverable): {e}",
                    )
                    continue
            elif type(e).__name__ == "GraphRecursionError" or "recursion limit" in err_str:
                # The ReAct agent looped without stopping. Local LLMs like
                # qwen3-coder do this — they keep calling query_spec_database
                # instead of synthesizing the MR JSON. Set a flag so all
                # subsequent retries skip the broken ReAct path entirely
                # and go straight to single-shot synthesis.
                logger.warning(
                    "GraphRecursionError on attempt %d; falling back to "
                    "single-shot synthesis (and skipping ReAct on future retries).",
                    attempt + 1,
                )
                react_is_broken = True
                raw_output = _synthesize_from_recursion_failure(
                    e, target, spec_format, blindspot_context, llm
                )
                if raw_output:
                    result = None  # skip normal extraction
                    logger.info(
                        "Synthesis fallback produced %d chars of output",
                        len(raw_output),
                    )
                else:
                    compilation = CompilationResult(
                        success=False,
                        error_detail=(
                            f"ReAct loop hit recursion limit and synthesis "
                            f"fallback extracted no usable tool context."
                        ),
                    )
                    continue
            else:
                # Unknown agent invocation error — log and retry, don't bail.
                # Historically this silently returned, causing whole themes to
                # produce 0 MRs with no log trail.  Now we let the retry loop
                # give us three more chances before giving up.
                logger.warning(
                    "Agent invocation error on attempt %d (%s): %s",
                    attempt + 1, type(e).__name__, str(e)[:200],
                )
                compilation = CompilationResult(
                    success=False,
                    error_detail=f"Agent invocation error ({type(e).__name__}): {e}",
                )
                continue

        # Extract JSON from the agent's final response
        if raw_output is None:
            raw_output = _extract_text_from_response(result) if result is not None else ""
        logger.debug("Agent raw output (attempt %d):\n%s", attempt + 1, (raw_output or "")[:500])

        if not raw_output or not raw_output.strip():
            logger.warning(
                "Empty agent output on attempt %d (result had no AI message content)",
                attempt + 1,
            )
            compilation = CompilationResult(
                success=False,
                error_detail="Agent returned no text output (empty message chain)",
            )
            continue

        # Explicit empty-array answer from the synthesis fallback means
        # "no MRs apply for this target/format combo" — a legitimate
        # outcome (e.g. VCF/normalization_invariance where our whitelist
        # has no VCF-applicable transforms). Treat as success with zero
        # relations so the theme doesn't spin through 3 more retries.
        if raw_output.strip() in ("[]", '[ ]'):
            logger.info(
                "Synthesis returned empty array — no applicable MRs for "
                "%s/%s; terminating theme cleanly.",
                spec_format, target.value,
            )
            return CompilationResult(success=True, relations=[])

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


# Per-target probe queries used when the ReAct loop aborts. The queries
# are hand-tuned to surface the spec sections most likely to yield
# evidence for each behavior category, without the agent having to
# discover them through iteration.
_FALLBACK_QUERIES: dict[str, list[str]] = {
    "ordering_invariance": [
        "header line order meta-information any order",
        "field ordering not significant structured line",
        "may appear in any order",
        # BCF dictionary and CSQ/ANN record ordering
        "BCF dictionary contigs INFO FORMAT order",
        "CSQ ANN annotation record order not significant",
    ],
    "semantics_preserving_permutation": [
        "ALT allele order permutation genotype indices",
        "Number=A values order matches ALT",
        "genotype index refers to ALT position",
    ],
    "normalization_invariance": [
        "CIGAR adjacent operations merge split equivalent",
        "hard soft clipping H S normalization",
        "normalized representation equivalent alignment",
        # Variant normalization (Tan 2015) + multi-allelic split
        "variant normalization left alignment parsimony",
        "common prefix suffix trim REF ALT",
        "multi-allelic split join records",
    ],
    "rejection_invariance": [
        "must not begin byte order mark BOM",
        "invalid character read name QNAME restriction",
        "tab separator field delimiter required",
    ],
    "coordinate_indexing_invariance": [
        "1-based coordinate system POS field",
        "closed interval 0-based BAM",
        "position coordinate specification",
    ],
    "round_trip_invariance": [
        "text binary equivalent BCF2 VCF round trip",
        "parse serialize preserves information",
        "lossless conversion header record",
        # BCF binary representation + dictionary encoding
        "BCF binary representation VCF equivalent",
        "BCF header dictionary contigs INFO FORMAT",
    ],
}


def _synthesize_from_recursion_failure(
    exc: Exception,
    target: BehaviorTarget,
    spec_format: str,
    blindspot_context: Optional[str],
    llm: Optional[BaseChatModel],
) -> str:
    """Rescue path when the ReAct loop hits the recursion limit.

    Rather than letting the local LLM continue to spin, we do a small
    hardcoded retrieval pass (3 queries) plus ONE non-agentic synthesis
    call. No tool loop — the LLM only produces JSON, it cannot call the
    tool again.
    """
    try:
        queries = _FALLBACK_QUERIES.get(
            target.value,
            ["normative requirement specification rule", "must shall required"],
        )
        retrieved_blocks: list[str] = []
        seen_chunk_ids: set[str] = set()
        for q in queries:
            try:
                out = query_spec_database.invoke({
                    "question": q,
                    "n_results": 3,
                    "format_filter": spec_format,
                })
            except Exception as qe:
                logger.debug("Fallback query '%s' failed: %s", q, qe)
                continue
            for r in out.get("results", []):
                if r.get("above_threshold"):
                    continue  # reject noise
                cid = r.get("chunk_id", "")
                if not cid or cid in seen_chunk_ids:
                    continue
                seen_chunk_ids.add(cid)
                snippet = (r.get("text") or "")[:400].replace("\n", " ")
                sev = (r.get("metadata") or {}).get("rule_severity", "?")
                retrieved_blocks.append(
                    f"chunk_id: {cid}\n  severity: {sev}\n  text: {snippet}"
                )

        if not retrieved_blocks:
            logger.info(
                "Fallback retrieval produced no below-threshold chunks for "
                "%s/%s — emitting empty MR array (no applicable evidence).",
                spec_format, target.value,
            )
            return "[]"

        # Non-agentic synthesis. The LLM only emits JSON — no tool binding.
        from mr_engine.agent.transforms_menu import build_transforms_menu
        menu = build_transforms_menu(spec_format=spec_format)

        synth_prompt = (
            "You are a JSON-only emitter. Produce exactly one JSON array of "
            "Metamorphic Relations — no prose, no markdown fences, no commentary.\n\n"
            f"Context:\n- Format: {spec_format}\n- Behavior target: {target.value}\n"
            f"- {len(retrieved_blocks)} pre-retrieved spec chunks below are the "
            "ONLY evidence available. Do not invent chunk_ids.\n\n"
            "Evidence:\n"
            + "\n\n".join(retrieved_blocks)
            + "\n\nAtomic transforms whitelist (transform_steps strings MUST match exactly):\n"
            + menu
            + "\n\nOutput schema — return a JSON array with 0 to 2 objects:\n"
              '[{\n'
              '  "mr_name": "short human label",\n'
              f'  "scope": "{spec_format}.header" | "{spec_format}.record",\n'
              '  "preconditions": ["str"],\n'
              '  "transform_steps": ["name_from_whitelist_only"],\n'
              '  "oracle": "invariant that must hold after the transform",\n'
              '  "evidence": [{"chunk_id": "<exact chunk_id from Evidence section>", '
              '"quote": "<verbatim sentence from that chunk>"}],\n'
              '  "ambiguity_flags": []\n'
              '}]\n\n'
              "HARD RULES:\n"
              "- First non-whitespace character of your reply MUST be `[`.\n"
              "- Last non-whitespace character MUST be `]`.\n"
              "- If no chunk justifies an MR, output exactly `[]` and stop.\n"
              "- Do NOT wrap in ```json fences.\n"
              "- Do NOT call any tool — just emit JSON.\n"
        )
        if blindspot_context:
            synth_prompt += "\n\nBlindspot guidance:\n" + blindspot_context

        model = llm if llm is not None else get_llm()
        resp = model.invoke([HumanMessage(content=synth_prompt)])
        out_text = getattr(resp, "content", "")
        if isinstance(out_text, list):
            # Some providers return List[dict]; join text parts.
            out_text = "".join(
                p.get("text", "") for p in out_text if isinstance(p, dict)
            )
        out_text = (out_text or "").strip()
        # Strip common markdown fence wrapping some local models add anyway.
        if out_text.startswith("```"):
            # remove first line fence and trailing ``` line
            lines = out_text.splitlines()
            if lines:
                lines = lines[1:] if lines[0].startswith("```") else lines
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                out_text = "\n".join(lines).strip()
        return out_text
    except Exception as syn_e:
        logger.warning("Synthesis fallback itself failed: %s", syn_e)
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
