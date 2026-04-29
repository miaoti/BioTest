"""Rank 10 — Byte-level fuzzer with validity gate.

Motivation (per run-3 diagnostic, `compares/results/mutation/biotest/
RUN3_FINAL.md`): Rank 9 (value diversifier) moved the htsjdk SAM cell
by +2.17pp (closed 25 % of its baseline gap) but didn't help htsjdk VCF
/ vcfpy / noodles. Those cells need **tokenizer-edge diversity** — byte
positions where a `RemoveConditional_EQUAL_ELSE` mutant in the parser's
character-by-character state machine would flip — which Rank 9's
structured per-field perturbation can't produce.

Rank 10 adds byte-level mutation with the **same validity gate** Rank 9
uses. Random bit-flips, byte substitutions, byte inserts, and byte
deletes are applied at random positions in each source seed; each
candidate is filtered through the canonical normalizer (and optionally
through the primary SUT's parser, same Refinement C mechanism).

Why this is NOT full libFuzzer integration:
  * No per-SUT-language harness — byte operations are format-agnostic.
  * No coverage feedback at the byte-fuzzer level — the downstream
    mutation-score run is the fitness signal.
  * No new dependency — `random.getrandbits()` + the existing
    `normalize_{vcf,sam}_text` gate we already have.
  * No competition with `compares/DESIGN.md`'s fairness claim — the
    output goes through the same seed-corpus pipeline Ranks 1/8/9 feed,
    not through a new oracle.

Semantically this is **Zest** (Padhye et al. ISSTA'19) restricted to
byte-level mutation + validity gating, with the gate intentionally
scoped to "parses without error" rather than "covers new branches"
(we let the mutation-score downstream be the branch-coverage signal).

Output: `seeds/<fmt>_bytefuzz/bytefuzz_<sha8>.{vcf,sam}`. Kept
separate from `seeds/<fmt>/` so Phase C's MR loop (which globs
`seeds/<fmt>/*.<ext>`) doesn't pick them up — mutation-score staging
explicitly unions the directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import random
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

logger = logging.getLogger("byte_fuzzer")


# ---------------------------------------------------------------------------
# Byte-level mutation operators
# ---------------------------------------------------------------------------

def _flip_random_bit(data: bytearray, rng: random.Random) -> None:
    if not data: return
    idx = rng.randrange(len(data))
    bit = 1 << rng.randrange(8)
    data[idx] ^= bit


def _sub_random_byte(data: bytearray, rng: random.Random) -> None:
    if not data: return
    idx = rng.randrange(len(data))
    # Prefer printable ASCII so chances of staying text-valid are higher.
    data[idx] = rng.randrange(0x20, 0x7f)


def _insert_random_byte(data: bytearray, rng: random.Random) -> None:
    if not data: return
    idx = rng.randrange(len(data))
    data.insert(idx, rng.randrange(0x20, 0x7f))


def _delete_random_byte(data: bytearray, rng: random.Random) -> None:
    if len(data) <= 1: return
    idx = rng.randrange(len(data))
    del data[idx]


def _sub_random_digit(data: bytearray, rng: random.Random) -> None:
    """Swap one ASCII digit with another random digit — high chance of staying valid."""
    digit_positions = [i for i, b in enumerate(data) if 0x30 <= b <= 0x39]
    if not digit_positions: return
    idx = rng.choice(digit_positions)
    data[idx] = rng.randrange(0x30, 0x3a)


_OPERATORS = [
    # Bias toward digit-swap (high-yield for valid outputs) and bit-flip
    # (broadest diversity). Insert/delete are structural and often break
    # TSV column counts; kept but rarer.
    (_sub_random_digit, 0.35),
    (_flip_random_bit,  0.30),
    (_sub_random_byte,  0.20),
    (_insert_random_byte, 0.075),
    (_delete_random_byte, 0.075),
]


def _weighted_choice(rng: random.Random, weighted: list[tuple]):
    r = rng.random()
    acc = 0.0
    for item, w in weighted:
        acc += w
        if r <= acc: return item
    return weighted[-1][0]


# ---------------------------------------------------------------------------
# Per-format mutation — target record lines only, preserve header verbatim
# ---------------------------------------------------------------------------

def _mutate_once(source_bytes: bytes, fmt: str, rng: random.Random,
                 n_mutations: int) -> bytes:
    """Apply `n_mutations` random byte-level ops to the non-header portion
    of the file. Header lines (VCF `#`-prefix, SAM `@`-prefix) are kept
    verbatim to give parsers a chance to initialise before the first
    mutated record hits them."""
    lines = source_bytes.split(b"\n")
    header_prefix = b"#" if fmt.upper() == "VCF" else b"@"
    header_lines = [ln for ln in lines if ln.startswith(header_prefix) or not ln]
    body_lines = [ln for ln in lines if ln and not ln.startswith(header_prefix)]
    if not body_lines:
        return source_bytes
    # Mutate a random subset of body lines.
    for _ in range(n_mutations):
        if not body_lines: break
        idx = rng.randrange(len(body_lines))
        buf = bytearray(body_lines[idx])
        op = _weighted_choice(rng, _OPERATORS)
        op(buf, rng)
        body_lines[idx] = bytes(buf)
    return b"\n".join(header_lines + body_lines)


def _validate(text: str, fmt: str, sut_validate: Optional[str] = None) -> bool:
    """Same gate Rank 9 uses — re-export to keep this module independent."""
    from mr_engine.transforms.value_diversifier import _validate as _v9_validate
    return _v9_validate(text, fmt, sut_validate=sut_validate)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def fuzz_directory(
    input_dir: Path, output_dir: Path, fmt: str,
    n_per_seed: int = 20, mutations_per_variant: int = 3,
    seed: int = 42, max_bytes: int = 500_000,
    sut_validate: Optional[str] = None,
) -> dict:
    """Generate byte-mutated variants of each seed, validity-gated."""
    ext = fmt.lower()
    sources = sorted(p for p in input_dir.iterdir()
                     if p.is_file() and p.suffix.lower() == f".{ext}"
                     and not p.name.startswith("kept_")
                     and not p.name.startswith("bytefuzz_")
                     and not p.name.startswith("diverse_"))
    if not sources:
        raise SystemExit(f"byte_fuzzer: no {ext} files in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    kept = 0
    rejected_invalid = 0
    rejected_dup = 0
    rejected_size = 0
    seen_hashes: set[str] = set()
    for existing in output_dir.glob(f"bytefuzz_*.{ext}"):
        seen_hashes.add(existing.stem[len("bytefuzz_"):])

    for src in sources:
        try:
            src_bytes = src.read_bytes()
        except OSError:
            continue
        for _ in range(n_per_seed):
            variant_bytes = _mutate_once(src_bytes, fmt, rng,
                                         mutations_per_variant)
            if not variant_bytes or len(variant_bytes) > max_bytes:
                rejected_size += 1
                continue
            h = hashlib.sha256(variant_bytes).hexdigest()[:16]
            if h in seen_hashes:
                rejected_dup += 1
                continue
            try:
                text = variant_bytes.decode("utf-8", errors="replace")
            except UnicodeDecodeError:
                rejected_invalid += 1
                continue
            if not _validate(text, fmt, sut_validate=sut_validate):
                rejected_invalid += 1
                continue
            seen_hashes.add(h)
            dest = output_dir / f"bytefuzz_{h}.{ext}"
            dest.write_bytes(variant_bytes)
            kept += 1

    result = {
        "sources": len(sources),
        "n_per_seed": n_per_seed,
        "mutations_per_variant": mutations_per_variant,
        "attempted": len(sources) * n_per_seed,
        "kept": kept,
        "rejected_invalid": rejected_invalid,
        "rejected_duplicate": rejected_dup,
        "rejected_size": rejected_size,
        "output_dir": str(output_dir),
        "sut_validate": sut_validate,
    }
    logger.info("byte_fuzzer result: %s", result)
    return result


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, required=True,
                   help="Directory of source seeds.")
    p.add_argument("--output", type=Path, required=True,
                   help="Output directory (seeds/<fmt>_bytefuzz/ is the convention).")
    p.add_argument("--format", required=True, choices=["VCF", "SAM"])
    p.add_argument("--n-per-seed", type=int, default=20,
                   help="How many variants to try per input seed (default 20).")
    p.add_argument("--mutations-per-variant", type=int, default=3,
                   help="Number of byte-level mutations per variant (default 3).")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--sut-validate", default=None,
                   help="Optional SUT-parser gate (biopython / vcfpy).")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    r = fuzz_directory(
        input_dir=args.input.resolve(),
        output_dir=args.output.resolve(),
        fmt=args.format,
        n_per_seed=args.n_per_seed,
        mutations_per_variant=args.mutations_per_variant,
        seed=args.seed,
        sut_validate=args.sut_validate,
    )
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
