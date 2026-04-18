"""
Agent orchestration: create ReAct agent, run MR mining, handle retry loop.

The agent uses LangGraph's create_react_agent with the query_spec_database
tool. On Pydantic validation failure, the error is fed back to the agent
for self-correction (up to MAX_VALIDATION_RETRIES attempts).
"""

from __future__ import annotations

import logging
import random
import re
import time
from typing import Any, Callable, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from mr_engine.llm_factory import get_llm, get_llm_settings
from mr_engine.behavior import BehaviorTarget
from mr_engine.agent.tools import query_spec_database, get_spec_index
from mr_engine.agent.prompts import build_system_prompt
from mr_engine.dsl.compiler import compile_mr_output, CompilationResult

logger = logging.getLogger(__name__)

MAX_VALIDATION_RETRIES = 3


def _rotate_llm(used_models: set[str]) -> tuple[BaseChatModel | None, str | None]:
    """Walk the fallback chain looking for a provider we haven't tried.

    Fallback chain comes from LLMSettings.llm_fallback_models. A model
    is skipped when either (a) we already tried it in this theme, or
    (b) constructing the LangChain client raises (typically because the
    matching provider API key isn't set — e.g. no OpenAI key means we
    skip gpt-* fallbacks instead of crashing).

    Returns (llm, model_name) on success, or (None, None) when the chain
    is exhausted — caller must bail this theme.
    """
    settings = get_llm_settings()
    for candidate in settings.fallback_model_list():
        if candidate in used_models:
            continue
        try:
            llm = get_llm(settings=settings, model_override=candidate)
        except Exception as e:
            logger.info(
                "Fallback model %r unavailable (%s); skipping.",
                candidate, type(e).__name__,
            )
            continue
        return llm, candidate
    return None, None

# Free-tier LLM quotas (Groq Llama 3.3) frequently hit 429 responses
# that carry a Retry-After hint. We parse that hint; if absent, fall
# back to exponential backoff starting at 30 s. Cap at RATE_LIMIT_CAP
# so we never sleep longer than a single phase would run.
RATE_LIMIT_BASE_DELAY_S = 30
RATE_LIMIT_MAX_RETRIES = 4
RATE_LIMIT_CAP_S = 10 * 60   # 10 minutes


_RATE_LIMIT_KEYWORDS = (
    "429", "rate limit", "rate_limit", "ratelimit", "quota",
    "too many requests", "503", "capacity", "overloaded",
    "try again in", "retry after",
)

# Persistent errors — retrying WILL NOT help. Detected so the rate-limit
# helper short-circuits its retry ladder and hands control to the
# fallback-rotation path immediately instead of burning 8 min of sleep.
# These all require human action (add credits / enable billing / upgrade
# plan) so no exponential backoff will fix them.
_PERSISTENT_ERROR_KEYWORDS = (
    "prepayment credits are depleted",
    "prepayment credits depleted",
    "billing",
    "insufficient_quota",
    "insufficient balance",         # DeepSeek 402
    "payment required",
    "please upgrade",
    "account suspended",
    "disabled billing",
    "enable billing",
    "exceeded your current quota",  # often paired with billing action-required
    "decommissioned",               # Groq gemma2-9b-it / mixtral-8x7b
    "no longer supported",
)


def _is_rate_limit_error(exc: BaseException) -> bool:
    """Return True when an exception looks like a rate-limit / 429."""
    err = str(exc).lower()
    if any(kw in err for kw in _RATE_LIMIT_KEYWORDS):
        return True
    # Common HTTP exception types expose a status_code attribute.
    code = getattr(exc, "status_code", None) or getattr(
        getattr(exc, "response", None), "status_code", None
    )
    return code in (429, 503)


def _is_persistent_error(exc: BaseException) -> bool:
    """True when the error won't clear via sleep — rotate, don't retry.

    Billing issues, depleted prepayment credits, suspended accounts.
    Treat these as fatal for the current model so we rotate to the
    next API fallback immediately.
    """
    err = str(exc).lower()
    return any(kw in err for kw in _PERSISTENT_ERROR_KEYWORDS)


def _parse_retry_after_seconds(exc: BaseException) -> Optional[float]:
    """Best-effort parse of provider-specific Retry-After hints.

    Looks for:
      - `Retry-After: <n>` HTTP header if the exception carries a response.
      - Groq's free-form "try again in 37.23s" / "in 2m14s" in the message.
      - Anthropic-style "retry_after" / "retryDelay" JSON fields in the text.
    """
    # Header path (httpx / requests Response).
    response = getattr(exc, "response", None)
    if response is not None:
        headers = getattr(response, "headers", {}) or {}
        retry_after = headers.get("Retry-After") or headers.get("retry-after")
        if retry_after:
            try:
                return float(retry_after)
            except (TypeError, ValueError):
                pass

    msg = str(exc)
    # "try again in 37.23s" or "try again in 37s".
    m = re.search(r"try again in\s+([\d.]+)\s*s", msg, flags=re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    # "try again in 1m30s"
    m = re.search(r"try again in\s+(\d+)m(\d+)?s?", msg, flags=re.IGNORECASE)
    if m:
        minutes = int(m.group(1))
        seconds = int(m.group(2) or 0)
        return float(minutes * 60 + seconds)
    # JSON field patterns.
    m = re.search(r'"retry_?[a-z_]*":\s*"?(\d+(?:\.\d+)?)', msg)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return None


def _invoke_with_rate_limit(
    call: Callable[[], Any],
    *,
    attempt_label: str,
    max_retries: int = RATE_LIMIT_MAX_RETRIES,
) -> Any:
    """Invoke `call` with exponential backoff on rate-limit errors.

    Re-raises non-rate-limit exceptions to the caller (which still has
    its own typed recovery path for tool_use_failed, recursion, etc).
    """
    last_exc: Optional[BaseException] = None
    for i in range(max_retries + 1):
        try:
            return call()
        except Exception as e:
            if not _is_rate_limit_error(e):
                raise
            last_exc = e
            # Short-circuit: persistent errors (billing / depleted
            # credits / suspended account) won't clear via backoff.
            # Raise immediately so the caller's fallback-rotation path
            # can switch providers instead of burning the retry ladder.
            if _is_persistent_error(e):
                logger.warning(
                    "Persistent error on %s (no retry will help): %s",
                    attempt_label, str(e)[:200],
                )
                raise
            if i == max_retries:
                logger.error(
                    "Rate-limit retries exhausted (%s attempt %d/%d): %s",
                    attempt_label, i + 1, max_retries + 1, str(e)[:200],
                )
                raise

            hint = _parse_retry_after_seconds(e)
            if hint is not None:
                # Honour the provider's suggestion plus a small jitter.
                sleep_s = min(hint + random.uniform(0.5, 2.0), RATE_LIMIT_CAP_S)
                src = "provider hint"
            else:
                # Exponential backoff: 30s, 60s, 120s, 240s …
                sleep_s = min(
                    RATE_LIMIT_BASE_DELAY_S * (2 ** i)
                    + random.uniform(0.0, 2.0),
                    RATE_LIMIT_CAP_S,
                )
                src = "exponential"
            logger.warning(
                "Rate-limited on %s (retry %d/%d, %s): sleeping %.1fs — %s",
                attempt_label, i + 1, max_retries, src, sleep_s, str(e)[:150],
            )
            time.sleep(sleep_s)
    # Should be unreachable — loop either returns or re-raises.
    raise last_exc  # type: ignore[misc]


def create_mr_agent(
    target: BehaviorTarget,
    spec_format: str,
    llm: BaseChatModel | None = None,
    blindspot_context: str | None = None,
    primary_target: str = "",
    available_suts: list[str] | None = None,
    runtime_capabilities: set[str] | None = None,
):
    """
    Create a configured ReAct agent for MR mining.

    Args:
        target: Behavior target to investigate.
        spec_format: "VCF" or "SAM".
        llm: LangChain model instance. If None, loads from environment.
        blindspot_context: Optional Phase D blindspot guidance to append.
        primary_target: SUT driving the feedback loop (e.g. "htsjdk").
                        Forwarded to the system prompt so the LLM aligns
                        SUT-specific transforms with this target.
        available_suts: SUT names currently available at runtime. Narrows
                        the set of SUT-specific transforms the agent may
                        pick from.

    Returns:
        A LangGraph Runnable agent.
    """
    if llm is None:
        llm = get_llm()

    system_prompt = build_system_prompt(
        target, spec_format, blindspot_context,
        primary_target=primary_target,
        available_suts=available_suts,
        runtime_capabilities=runtime_capabilities,
    )

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
    primary_target: str = "",
    available_suts: list[str] | None = None,
    runtime_capabilities: set[str] | None = None,
) -> CompilationResult:
    """
    Full MR mining pipeline: agent -> validate -> retry on failure.

    Args:
        target: Behavior target category.
        spec_format: "VCF" or "SAM".
        llm: Optional pre-configured LLM instance.
        blindspot_context: Optional Phase D blindspot guidance.
        primary_target: SUT driving feedback (e.g. "htsjdk"). Surfaced
                        in the system prompt's selection rule so the
                        LLM aligns SUT-specific transforms with this
                        target. Empty string preserves legacy behavior.
        available_suts: Runtime-available SUT names. Narrows SUT-specific
                        transform selection to only those the current
                        environment can actually execute.

    Returns:
        CompilationResult with validated MRs or final errors.
    """
    # Track which LLM models we've used on this theme, for the
    # API-only fallback chain. Never falls back to local — if every
    # API provider is exhausted, the theme bails cleanly.
    settings = get_llm_settings()
    active_llm = llm if llm is not None else get_llm(settings=settings)
    active_model = getattr(active_llm, "model_name", None) or getattr(
        active_llm, "model", None
    ) or settings.llm_model
    used_models: set[str] = {active_model} if active_model else set()

    agent = create_mr_agent(
        target, spec_format, active_llm, blindspot_context,
        primary_target=primary_target,
        available_suts=available_suts,
        runtime_capabilities=runtime_capabilities,
    )
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
            result = _invoke_with_rate_limit(
                lambda: agent.invoke(
                    {"messages": messages},
                    config={"recursion_limit": 25},
                ),
                attempt_label=f"agent.invoke attempt {attempt + 1}",
            )
          except Exception as e:
            err_str = str(e).lower()
            if _is_rate_limit_error(e):
                # Exhausted the backoff budget for the current model.
                # Try rotating to the next API fallback — e.g. Gemini 2.5
                # Flash → 2.0 Flash → Flash-Lite → Groq free models.
                # No local fallback: API-only chain, per operator
                # preference (local models choked on previous runs).
                next_llm, next_model = _rotate_llm(used_models)
                if next_llm is not None and next_model is not None:
                    logger.warning(
                        "Rate-limit budget exhausted on model %r (attempt %d); "
                        "rotating to fallback model %r.",
                        active_model, attempt + 1, next_model,
                    )
                    active_llm = next_llm
                    active_model = next_model
                    used_models.add(next_model)
                    agent = create_mr_agent(
                        target, spec_format, active_llm, blindspot_context,
                        primary_target=primary_target,
                        available_suts=available_suts,
                    )
                    # Retry this same attempt with the new model.
                    # Don't bump `attempt`; we simply "restart" the try.
                    try:
                        result = _invoke_with_rate_limit(
                            lambda: agent.invoke(
                                {"messages": messages},
                                config={"recursion_limit": 25},
                            ),
                            attempt_label=f"agent.invoke attempt {attempt + 1} "
                                          f"(fallback {active_model})",
                        )
                    except Exception as e2:
                        logger.warning(
                            "Fallback %r also failed: %s",
                            active_model, str(e2)[:200],
                        )
                        compilation = CompilationResult(
                            success=False,
                            error_detail=(
                                f"Rate limit on primary AND fallback "
                                f"{active_model!r}: {e2}"
                            ),
                        )
                        continue
                    # result is set; fall through to compilation.
                else:
                    # Entire API fallback chain exhausted — bail the theme.
                    logger.warning(
                        "Rate-limit exhausted on %r and every API fallback "
                        "tried in this theme; bailing. Used: %s",
                        active_model, sorted(used_models),
                    )
                    compilation = CompilationResult(
                        success=False,
                        error_detail=(
                            f"All API models exhausted (tried: "
                            f"{sorted(used_models)}): {e}"
                        ),
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
