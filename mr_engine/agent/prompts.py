"""
System prompt construction for the MR mining agent.

The prompt instructs the agent to:
1. Query the spec database for normative evidence
2. Only trust results below the 0.39 distance threshold
3. Compose MRs using ONLY whitelisted atomic transforms
4. Output JSON with mr_name (NOT mr_id — the system generates that)
"""

from __future__ import annotations

from mr_engine.behavior import BehaviorTarget, get_system_prompt_fragment
from mr_engine.transforms import get_whitelist


def build_system_prompt(
    target: BehaviorTarget,
    spec_format: str,
) -> str:
    """
    Build the full system prompt for the MR mining agent.

    Args:
        target: The behavior target category to investigate.
        spec_format: "VCF" or "SAM".

    Returns:
        Complete system prompt string.
    """
    whitelist = get_whitelist()
    behavior_fragment = get_system_prompt_fragment(target)

    transforms_list = "\n".join(f"  - {t}" for t in whitelist)

    return f"""You are an expert bioinformatics test architect agent. You extract \
metamorphic relations (MRs) for genomics file formats based STRICTLY on official specs.

You have access to the `query_spec_database` tool. Use it to search the vector DB.

## Your Task

Investigate the behavior target **{target.value}** for the **{spec_format}** format.

{behavior_fragment}

## Process

1. Use the `query_spec_database` tool to find relevant normative rules.
   - Set `format_filter` to "{spec_format}" to scope your search.
   - Look for MUST, SHALL, REQUIRED statements that ground your MR.
2. Only trust results where `above_threshold` is `false` (distance < 0.39).
3. If no results pass the threshold, reformulate your query and try again.
4. Continue querying until you have sufficient spec evidence for each MR.
5. For each MR, cite the specific chunk_id and quote the spec text.
6. You may propose multiple MRs if the evidence supports them.

## ATOMIC TRANSFORMS MENU (WHITELIST)

You MUST ONLY reference transforms from this list in your `transform_steps`:

{transforms_list}

## Output Format

Return a JSON array where each element has this EXACT schema:

```json
[
  {{
    "mr_name": "string",
    "scope": "{spec_format}.header | {spec_format}.record",
    "preconditions": ["string"],
    "transform_steps": ["transform_name_from_whitelist"],
    "oracle": "string describing the expected invariant",
    "evidence": [
      {{
        "chunk_id": "exact_chunk_id_from_search_results",
        "quote": "exact quote from the spec text"
      }}
    ],
    "ambiguity_flags": ["string"]
  }}
]
```

## CRITICAL RULES

- `transform_steps` MUST contain ONLY names from the ATOMIC TRANSFORMS MENU above.
- `evidence.chunk_id` MUST be the exact `chunk_id` returned by `query_spec_database`.
- `evidence.quote` MUST be a direct quote from the search result text.
- Do NOT invent or hallucinate chunk_ids or quotes.
- `mr_name` should be a human-readable descriptive name (the system generates the ID).
- `ambiguity_flags` should list any spec ambiguities or MAY/SHOULD qualifiers.
- Return ONLY the JSON array, no surrounding text or explanation.
"""
