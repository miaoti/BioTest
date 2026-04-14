"""
LangChain tool wrapping Phase A's SpecIndex for agent use.

The tool applies the Phase A rejection threshold (0.39) to annotate
results as above/below relevance threshold.
"""

from __future__ import annotations

from typing import Optional

from langchain_core.tools import tool
from mr_engine.index_loader import EphemeralSpecIndex, get_ephemeral_index

# Phase A established rejection threshold
REJECTION_THRESHOLD = 0.39


def get_spec_index() -> EphemeralSpecIndex:
    """Get or create the singleton ephemeral SpecIndex."""
    return get_ephemeral_index()


@tool
def query_spec_database(
    question: str,
    n_results: int = 5,
    format_filter: Optional[str] = None,
    severity_filter: Optional[str] = None,
) -> dict:
    """Search the HTS specification database (VCF v4.5, SAM v1) for normative rules.

    Returns chunks with distance scores. Chunks with distance > 0.39 are
    below the relevance threshold and should be treated as unsupported.

    Args:
        question: Natural language query about spec rules.
        n_results: Number of results to return (default 5).
        format_filter: Optional "VCF" or "SAM" to restrict search.
        severity_filter: Optional "CRITICAL", "ADVISORY", or "INFORMATIONAL".
    """
    index = get_spec_index()

    where: dict = {}
    if format_filter:
        where["format"] = format_filter
    if severity_filter:
        where["rule_severity"] = severity_filter

    results = index.query(
        question,
        n_results=n_results,
        where=where or None,
    )

    processed = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        processed.append({
            "chunk_id": results["ids"][0][len(processed)],
            "text": doc,
            "metadata": meta,
            "distance": round(dist, 4),
            "above_threshold": dist > REJECTION_THRESHOLD,
        })

    return {
        "results": processed,
        "rejection_threshold": REJECTION_THRESHOLD,
        "note": "Only trust results where above_threshold is false.",
    }
