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


# ---------------------------------------------------------------------------
# Phase 5 of SAM coverage plan — SeedMind-style generator synthesis.
#
# Instead of asking the LLM for K raw files, ask for ONE Python generator
# module and invoke it K times with distinct seeds. Benefits documented
# in SeedMind (arXiv:2411.18143): parameterized edge-case axes beat
# one-shot file generation by ~29 % on coverage.
#
# Safety layers:
#   (1) AST whitelist — reject imports outside a narrow safe set.
#   (2) Subprocess sandbox — Python -I (isolated), 5 s timeout,
#       no network primitives reachable.
#   (3) Per-output byte cap — same as raw-file path.
#   (4) Per-output structural parse — same as raw-file path.
# ---------------------------------------------------------------------------


_ALLOWED_IMPORTS: frozenset[str] = frozenset({
    "random", "string", "itertools", "struct", "math", "textwrap",
    "__future__",
})


class _GeneratorCodeRejected(Exception):
    """AST-whitelist rejection — the LLM shipped an unsafe import."""


def _ast_whitelist_check(src: str) -> None:
    """Raise _GeneratorCodeRejected if `src` imports anything outside
    the safe set.

    We scan the module-level `import` and `from ... import ...` nodes
    only. A generator that *runs* in the sandbox but imports only
    allowed modules is considered safe — the subprocess can't reach
    the network without one of the rejected modules (socket, urllib,
    requests, subprocess, os, sys, etc.).
    """
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        raise _GeneratorCodeRejected(f"syntax error: {e}") from None
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root not in _ALLOWED_IMPORTS:
                    raise _GeneratorCodeRejected(
                        f"disallowed import: {alias.name!r}"
                    )
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            if root and root not in _ALLOWED_IMPORTS:
                raise _GeneratorCodeRejected(
                    f"disallowed from-import: {node.module!r}"
                )


def _run_generator_sandboxed(
    src: str,
    seed: int,
    timeout_s: float = 5.0,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> Optional[str]:
    """Execute the LLM-authored generator in an isolated subprocess.

    Returns the string produced by `generate(seed)`, or None on any
    failure (timeout, exception, bad return type, oversize output).

    The runner script spawns `python -I -c <harness>`; `-I` suppresses
    PYTHON* env vars + user-site imports. The harness writes the result
    to stdout wrapped in a delimiter so we can detect truncated output.
    """
    import subprocess
    import sys as _sys
    import json

    # Embed the generator source inside a tiny harness that: (1) execs
    # it in a fresh namespace, (2) calls generate(seed), (3) prints the
    # result with a prefix/suffix sentinel. JSON-encodes both seed and
    # source to avoid quoting nightmares. Use a raw triple-quoted string
    # so `\n` escape sequences pass through intact when the harness is
    # fed to python -c.
    harness = r'''
import json, sys
src = json.loads(sys.stdin.readline())
seed_val = json.loads(sys.stdin.readline())
ns = {}
exec(src, ns)
gen = ns.get("generate")
if not callable(gen):
    print("__BIOTEST_NO_GENERATE__")
    sys.exit(1)
try:
    out = gen(seed_val)
except Exception as e:
    print("__BIOTEST_EXCEPTION__", type(e).__name__, str(e)[:120])
    sys.exit(2)
if not isinstance(out, str):
    print("__BIOTEST_BAD_RET__", type(out).__name__)
    sys.exit(3)
sys.stdout.write("__BIOTEST_BEGIN__\n")
sys.stdout.write(out)
sys.stdout.write("\n__BIOTEST_END__\n")
'''

    stdin_payload = (
        json.dumps(src).encode("utf-8") + b"\n"
        + json.dumps(seed).encode("utf-8") + b"\n"
    )

    try:
        proc = subprocess.run(
            [_sys.executable, "-I", "-c", harness],
            input=stdin_payload,
            capture_output=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        logger.debug("seed_synth.generator: subprocess timed out after %ss", timeout_s)
        return None

    if proc.returncode != 0:
        logger.debug(
            "seed_synth.generator: subprocess exit %d; stdout head=%r",
            proc.returncode, proc.stdout[:200],
        )
        return None

    text = proc.stdout.decode("utf-8", errors="replace")
    # Normalize CRLF to LF — Windows subprocess stdout is text-mode by
    # default and converts '\n' -> '\r\n', which would break the
    # sentinel-string search below.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    begin = text.find("__BIOTEST_BEGIN__\n")
    end = text.rfind("\n__BIOTEST_END__")
    if begin < 0 or end < 0 or end < begin:
        logger.debug("seed_synth.generator: sentinel markers missing")
        return None

    body = text[begin + len("__BIOTEST_BEGIN__\n"): end]
    if len(body.encode("utf-8")) > max_bytes:
        logger.debug(
            "seed_synth.generator: output %d bytes exceeds cap %d",
            len(body.encode('utf-8')), max_bytes,
        )
        return None
    return body


def synthesize_seeds_via_generator(
    blindspot_context: str,
    fmt: str,
    primary_target: str = "",
    n_seeds: int = 5,
    out_dir: Path = Path("seeds"),
    iteration: int = 0,
    max_bytes: int = DEFAULT_MAX_BYTES,
    llm=None,
    sandbox_timeout_s: float = 5.0,
) -> list[Path]:
    """SeedMind-style generator synthesis.

    Asks the LLM for a single Python generator module, then invokes it
    `n_seeds` times with distinct integer seeds. Each output goes through
    the same `_validate_candidate` pipeline as the raw-file path. Useful
    when the blindspot rules are invariant-driven — a generator can
    encode the invariant once and parameterize every other axis.

    Returns the list of accepted seed paths. Empty list on total failure.
    """
    if not blindspot_context or not blindspot_context.strip():
        logger.info("seed_synth.generator: no blindspot context — skipping")
        return []

    fmt_u = fmt.upper()
    subdir = fmt_u.lower()
    if fmt_u not in ("VCF", "SAM"):
        logger.warning("seed_synth.generator: unsupported format %s", fmt)
        return []

    from .seed_synth_prompts import build_generator_prompt
    prompt = build_generator_prompt(
        blindspot_context, fmt=fmt_u, n=n_seeds, max_bytes=max_bytes,
    )

    try:
        if llm is None:
            from mr_engine.llm_factory import get_llm
            llm = get_llm()
        resp = llm.invoke([HumanMessage(content=prompt)])
    except Exception as e:
        logger.warning("seed_synth.generator: LLM invocation failed: %s", e)
        return []

    raw_text = getattr(resp, "content", "")
    if isinstance(raw_text, list):
        raw_text = "".join(
            p.get("text", "") for p in raw_text if isinstance(p, dict)
        )
    raw_text = (raw_text or "").strip()

    blocks = _extract_fenced_blocks(raw_text)
    if not blocks:
        logger.info(
            "seed_synth.generator: no fenced code blocks (len=%d)", len(raw_text),
        )
        return []

    # Take the first block as the generator source. If the LLM emitted
    # multiple, we ignore the rest — the contract asks for exactly one.
    gen_src = blocks[0]

    try:
        _ast_whitelist_check(gen_src)
    except _GeneratorCodeRejected as e:
        logger.warning("seed_synth.generator: AST whitelist rejected code: %s", e)
        return []

    target_dir = out_dir / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    seen_hashes = _existing_synthetic_hashes(target_dir)

    # Invoke the generator N times with distinct seeds drawn from a
    # deterministic range so the run is reproducible across framework
    # restarts (same iteration + same position -> same seed).
    for idx in range(n_seeds):
        seed_val = 10_000 + iteration * 997 + idx * 31
        body = _run_generator_sandboxed(
            gen_src, seed_val,
            timeout_s=sandbox_timeout_s,
            max_bytes=max_bytes,
        )
        if body is None:
            continue

        normalized = _validate_candidate(body, fmt_u, max_bytes)
        if normalized is None:
            continue

        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        short = digest[:8]
        if short in seen_hashes:
            continue
        path = target_dir / f"synthetic_gen{iteration}_{short}.{subdir}"
        try:
            _atomic_write(path, normalized)
        except OSError as e:
            logger.warning("seed_synth.generator: atomic write failed: %s", e)
            continue
        seen_hashes.add(short)
        written.append(path)

    logger.info(
        "seed_synth.generator: accepted %d of %d generated outputs "
        "(target=%s, fmt=%s, iter=%d)",
        len(written), n_seeds, primary_target, fmt_u, iteration,
    )
    return written
