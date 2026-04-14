"""
Format Phase B HydratedEvidence into Markdown for bug reports.
"""

from __future__ import annotations

from typing import Any


def format_evidence(mr_dict: dict[str, Any]) -> str:
    """
    Convert an MR dict (from mr_registry.json) into a readable
    Markdown document for inclusion in bug reports.
    """
    lines = [
        f"# Evidence Report: {mr_dict['mr_name']}",
        f"**MR ID**: `{mr_dict['mr_id']}`",
        f"**Scope**: {mr_dict['scope']}",
        f"**Oracle**: {mr_dict.get('oracle', 'N/A')}",
        "",
        "## Transform Steps",
    ]
    for step in mr_dict.get("transform_steps", []):
        lines.append(f"- `{step}`")

    preconditions = mr_dict.get("preconditions", [])
    if preconditions:
        lines.extend(["", "## Preconditions"])
        for p in preconditions:
            lines.append(f"- {p}")

    lines.extend(["", "## Specification Evidence", ""])

    for i, ev in enumerate(mr_dict.get("evidence", []), 1):
        lines.extend([
            f"### Evidence {i}",
            f"- **Chunk ID**: `{ev.get('chunk_id', 'N/A')}`",
            f"- **Section**: {ev.get('section_id', 'N/A')}",
            f"- **Severity**: {ev.get('rule_severity', 'N/A')}",
            f"- **Quote**:",
            f"  > {ev.get('quote', 'N/A')}",
            "",
        ])

    flags = mr_dict.get("ambiguity_flags", [])
    if flags:
        lines.extend(["## Ambiguity Flags", ""])
        for flag in flags:
            lines.append(f"- {flag}")

    return "\n".join(lines)
