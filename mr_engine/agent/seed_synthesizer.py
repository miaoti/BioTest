"""
LLM-driven seed synthesis (Rank 1 coverage lever).

Takes the blindspot ticket (uncovered code slices + spec rules), asks the LLM
for raw VCF/SAM files that exercise those uncovered code paths, validates each
candidate, and writes accepted ones to the seed corpus under:
    seeds/vcf/synthetic_iter{N}_{hash8}.vcf
    seeds/sam/synthetic_iter{N}_{hash8}.sam

Next iteration's Phase C re-instantiates SeedCorpus (glob-based) and picks up
the new seeds automatically. Existing MRs then transform the richer corpus,
reaching code paths that the original hand-curated + real-world seeds miss.

Design notes:
- NO ReAct agent, NO tools. Plain `llm.invoke([HumanMessage(prompt)])`, mirroring
  the synthesis fallback at engine.py:717.
- Validation pipeline is strict — the gate is that the seed must *parse* through
  the framework's canonical normalizers, same gate every Phase C seed faces.
- Content-hash dedup: we never write two bit-identical seeds.
- Atomic write (write .tmp, rename on success): prevents partial files being
  globbed mid-write by a concurrent SeedCorpus._load.
- Fail-soft: one bad candidate never aborts the batch; we emit what we can.

Grounded in SeedMind (2024), SeedAIchemy (2025), TitanFuzz (ISSTA'23),
Fuzz4All (ICSE'24).
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
from pathlib import Path
from typing import Optional

from langchain_core.messages import HumanMessage

from .seed_synth_prompts import build_prompt

logger = logging.getLogger(__name__)

# Triple-fenced block regex. Matches ```vcf / ```sam / ``` (no lang) / any
# language tag — we don't care about the tag, only that the block is fenced.
# Captures the body (non-greedy, across newlines).
_FENCE_RE = re.compile(
    r"```(?:[\w-]*)\s*\n(.*?)```",
    re.DOTALL,
)

DEFAULT_MAX_BYTES = 500 * 1024


def synthesize_seeds(
    blindspot_context: str,
    fmt: str,
    primary_target: str = "",
    n_seeds: int = 5,
    out_dir: Path = Path("seeds"),
    iteration: int = 0,
    max_bytes: int = DEFAULT_MAX_BYTES,
    llm=None,
) -> list[Path]:
    """Synthesize VCF/SAM seeds from a blindspot ticket.

    Args:
        blindspot_context: Raw text produced by
            `BlindspotTicket.to_prompt_fragment()` — contains Top-K uncovered
            rules and the "UNCOVERED CODE" block.
        fmt: "VCF" or "SAM".
        primary_target: Name of the primary SUT (logging only).
        n_seeds: How many seeds to request from the LLM. The validation pipeline
            may accept fewer.
        out_dir: Root of the seed corpus. New seeds land at
            `out_dir/{vcf,sam}/synthetic_iter{N}_{hash8}.{vcf,sam}`.
        iteration: Phase D iteration number, embedded in filenames.
        max_bytes: Per-file size cap (matches fetch_real_world.py's 500 KB).
        llm: Optional BaseChatModel. Falls back to `get_llm()` if None.

    Returns:
        List of paths written. Empty list on total failure (logged, not raised).
    """
    if not blindspot_context or not blindspot_context.strip():
        logger.info("seed_synth: no blindspot context — skipping")
        return []

    fmt_u = fmt.upper()
    subdir = fmt_u.lower()
    if fmt_u not in ("VCF", "SAM"):
        logger.warning("seed_synth: unsupported format %s — skipping", fmt)
        return []

    prompt = build_prompt(
        blindspot_context, fmt=fmt_u, n=n_seeds, max_bytes=max_bytes,
    )

    try:
        if llm is None:
            from mr_engine.llm_factory import get_llm
            llm = get_llm()
        resp = llm.invoke([HumanMessage(content=prompt)])
    except Exception as e:
        logger.warning(
            "seed_synth: LLM invocation failed for %s/%s: %s",
            primary_target, fmt_u, e,
        )
        return []

    raw_text = getattr(resp, "content", "")
    if isinstance(raw_text, list):
        # Some providers return List[dict]; join text parts.
        raw_text = "".join(
            p.get("text", "") for p in raw_text if isinstance(p, dict)
        )
    raw_text = (raw_text or "").strip()

    candidates = _extract_fenced_blocks(raw_text)
    if not candidates:
        logger.info(
            "seed_synth: no fenced blocks in LLM response (len=%d); discarding",
            len(raw_text),
        )
        return []

    logger.info(
        "seed_synth: LLM returned %d candidate blocks (target=%s, fmt=%s, iter=%d)",
        len(candidates), primary_target, fmt_u, iteration,
    )

    target_dir = out_dir / subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    seen_hashes = _existing_synthetic_hashes(target_dir)

    for idx, body in enumerate(candidates):
        result = _validate_candidate(body, fmt_u, max_bytes)
        if result is None:
            continue
        normalized_body = result

        digest = hashlib.sha256(normalized_body.encode("utf-8")).hexdigest()
        short = digest[:8]
        if short in seen_hashes:
            logger.debug(
                "seed_synth: candidate %d/%d is a hash dup of existing synth "
                "seed (hash=%s) — skipping", idx + 1, len(candidates), short,
            )
            continue

        path = target_dir / f"synthetic_iter{iteration}_{short}.{subdir}"
        try:
            _atomic_write(path, normalized_body)
        except OSError as e:
            logger.warning("seed_synth: atomic write failed for %s: %s", path, e)
            continue

        seen_hashes.add(short)
        written.append(path)

    logger.info(
        "seed_synth: accepted %d of %d candidates (target=%s, fmt=%s, iter=%d)",
        len(written), len(candidates), primary_target, fmt_u, iteration,
    )
    return written


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _extract_fenced_blocks(text: str) -> list[str]:
    """Extract every triple-fenced code block body from the LLM response.

    Ignores the language tag — some models emit ```vcf, some ```, some
    ```Text. We accept any. Empty-body blocks are dropped.
    """
    blocks = _FENCE_RE.findall(text)
    out: list[str] = []
    for b in blocks:
        # Preserve internal newlines; strip only leading/trailing blank lines.
        stripped = b.strip("\r\n")
        if stripped:
            out.append(stripped)
    return out


def _validate_candidate(
    body: str,
    fmt: str,
    max_bytes: int,
) -> Optional[str]:
    """Apply the hard-gate pipeline. Returns normalized text on accept,
    None on reject. Each rejection is logged at DEBUG."""
    # (1) header check
    if fmt == "VCF":
        if not body.startswith("##fileformat=VCF"):
            logger.debug(
                "seed_synth: reject — VCF candidate missing `##fileformat=VCF` prefix",
            )
            return None
    else:  # SAM
        if not (body.startswith("@HD") or body.startswith("@SQ")):
            logger.debug(
                "seed_synth: reject — SAM candidate missing `@HD` or `@SQ` prefix",
            )
            return None

    # (2) size check
    body_bytes = body.encode("utf-8")
    if len(body_bytes) > max_bytes:
        logger.debug(
            "seed_synth: reject — candidate %d bytes exceeds cap %d",
            len(body_bytes), max_bytes,
        )
        return None

    # (3) structural parse through framework normalizer — same gate every
    # Phase C seed faces. Import lazily to avoid circular imports.
    try:
        if fmt == "VCF":
            from test_engine.canonical.vcf_normalizer import normalize_vcf_text
            normalize_vcf_text(body.splitlines(keepends=True))
        else:
            from test_engine.canonical.sam_normalizer import normalize_sam_text
            normalize_sam_text(body.splitlines(keepends=True))
    except Exception as e:
        logger.debug(
            "seed_synth: reject — normalizer raised %s: %s",
            type(e).__name__, str(e)[:150],
        )
        return None

    # Normalize trailing newline so the hash is stable across edits that
    # only differ in end-of-file whitespace.
    if not body.endswith("\n"):
        body = body + "\n"
    return body


def _existing_synthetic_hashes(target_dir: Path) -> set[str]:
    """Pull the hash8 segment out of every synthetic_iter*_*.{vcf,sam} name
    already on disk so we skip regenerating duplicates across iterations."""
    seen: set[str] = set()
    for p in target_dir.glob("synthetic_iter*_*"):
        # filename: synthetic_iter{N}_{hash8}.{vcf,sam}
        stem = p.stem  # synthetic_iter{N}_{hash8}
        parts = stem.rsplit("_", 1)
        if len(parts) == 2 and len(parts[1]) == 8:
            seen.add(parts[1])
    return seen


def _atomic_write(path: Path, text: str) -> None:
    """Write `text` to `path` atomically: write to `path.tmp`, then rename.

    Prevents a concurrent SeedCorpus glob from seeing a half-written file
    when it re-loads mid-iteration.
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    # utf-8 + explicit newline handling so Windows doesn't translate '\n'
    # to '\r\n' silently (the normalizer accepts either, but tests hash the
    # bytes and we want stability).
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)  # atomic on POSIX and Windows
