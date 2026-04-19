"""
LLM-driven MR synthesis (Rank 6 coverage lever).

Rank 1 (``seed_synthesizer``) synthesizes raw VCF/SAM FILES targeting
uncovered code; Rank 6 synthesizes new METAMORPHIC RELATIONS over the
existing transform whitelist targeting the same uncovered code. The
resulting MRs are routed through the regular compiler pipeline
(``mr_engine/dsl/compiler.py::compile_mr_output``) so all the same
validators apply — whitelist, compound groups, query_methods, evidence
hydration — and the result plugs into the Phase D registry merge path
exactly like Phase B output.

Design notes:
- NO ReAct agent, NO tools. Plain ``llm.invoke([HumanMessage(prompt)])``,
  matching ``seed_synthesizer.synthesize_seeds``.
- Validation is the SAME pipeline Phase B uses, so the LLM cannot invent
  new transforms or ship query_methods=[] when query_method_roundtrip is
  present. The compiler rejects those and we log + return an empty list.
- Evidence hydration uses a SpecIndex (ephemeral or persistent) loaded by
  the caller, identical to Phase B.
- Fail-soft: any LLM or compile failure is logged and returns [], never
  raises.

Grounded in Fuzz4All (ICSE'24), PromptFuzz (CCS'24), ChatAFL (NDSS'24).
"""

from __future__ import annotations

import logging
from typing import Optional

from langchain_core.messages import HumanMessage

from mr_engine.dsl.compiler import compile_mr_output
from mr_engine.dsl.models import MetamorphicRelation
from mr_engine.transforms import get_whitelist

from .mr_synth_prompts import build_prompt

logger = logging.getLogger(__name__)


def synthesize_mrs(
    blindspot_context: str,
    fmt: str,
    spec_index,
    primary_target: str = "",
    n_mrs: int = 5,
    query_methods: Optional[list[dict]] = None,
    exemplars: Optional[list[dict]] = None,
    llm=None,
) -> list[MetamorphicRelation]:
    """Synthesize new MRs targeting the uncovered-code blindspot.

    Args:
        blindspot_context: Text produced by
            ``BlindspotTicket.to_prompt_fragment()`` — the same shape Phase B
            and Rank 1 seed synthesis already consume.
        fmt: "VCF" or "SAM".
        spec_index: SpecIndex / EphemeralSpecIndex used for evidence
            hydration during compilation. The caller is responsible for
            building one appropriate for the current run.
        primary_target: SUT name, used only for log lines.
        n_mrs: Upper bound on MRs the LLM is asked to emit. The compiler
            may accept fewer — that is fine.
        query_methods: Optional Rank-5 catalog from
            ``runner.discover_query_methods(fmt)`` — if present the prompt
            invites the LLM to compose MRs using ``query_method_roundtrip``.
        exemplars: Optional list of accepted MRs from the registry to
            anchor the LLM on the expected JSON shape.
        llm: Optional BaseChatModel. Falls back to ``get_llm()`` if None.

    Returns:
        List of fully compiled MetamorphicRelation objects (possibly empty).
    """
    if not blindspot_context or not blindspot_context.strip():
        logger.info("mr_synth: no blindspot context — skipping")
        return []

    fmt_u = fmt.upper()
    if fmt_u not in ("VCF", "SAM"):
        logger.warning("mr_synth: unsupported format %s — skipping", fmt)
        return []

    whitelist = get_whitelist()
    if not whitelist:
        logger.warning("mr_synth: empty transform whitelist — skipping")
        return []

    prompt = build_prompt(
        blindspot_context=blindspot_context,
        fmt=fmt_u,
        whitelist=whitelist,
        n=n_mrs,
        query_methods=query_methods,
        exemplars=exemplars,
    )

    try:
        if llm is None:
            from mr_engine.llm_factory import get_llm
            llm = get_llm()
        resp = llm.invoke([HumanMessage(content=prompt)])
    except Exception as e:
        logger.warning(
            "mr_synth: LLM invocation failed for %s/%s: %s",
            primary_target, fmt_u, e,
        )
        return []

    raw_text = getattr(resp, "content", "")
    if isinstance(raw_text, list):
        raw_text = "".join(
            p.get("text", "") for p in raw_text if isinstance(p, dict)
        )
    raw_text = (raw_text or "").strip()
    if not raw_text:
        logger.info("mr_synth: empty LLM response for %s/%s", primary_target, fmt_u)
        return []

    result = compile_mr_output(raw_text, spec_index)
    if not result.success:
        logger.info(
            "mr_synth: compile rejected %s/%s batch: %s",
            primary_target, fmt_u, (result.error_detail or "")[:200],
        )
        return []

    relations = result.relations or []
    logger.info(
        "mr_synth: accepted %d synthesized MR(s) for %s/%s",
        len(relations), primary_target, fmt_u,
    )
    return relations
