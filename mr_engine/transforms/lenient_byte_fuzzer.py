"""Rank 13 — Lenient byte-level fuzzer (error-path diversifier).

Motivation (per run-5 post-mortem + Rank 12 VCF-gap diagnostic
2026-04-23):

Rank 10 (`byte_fuzzer.py`) gates every candidate through the canonical
normalizer (`normalize_{vcf,sam}_text`), which enforces spec-semantic
validity. That's right for Ranks 1-11, whose goal is to feed the
METAMORPHIC ORACLE (parse(T(x)) == parse(x)) — non-parseable inputs
break the invariant.

But PIT / cargo-mutants / mull don't need metamorphic-valid inputs:
their oracle compares the unmutated parse outcome to the mutated parse
outcome. A file that parses (even to an error) DETERMINISTICALLY is
already a useful mutation-test input — if a mutant changes the exact
error class or error count, that's a kill.

Jazzer's advantage on htsjdk_vcf (+47 kills on AbstractVCFCodec's
error-handling branches) comes from its corpus containing **byte-
corrupted but structurally-recognizable VCF files** — things htsjdk
LENIENT parses to a specific IOException, triggering kills when a
mutation changes the thrown exception class.

Rank 13 produces those files:
  * Start from a clean seed.
  * Apply 2-5 random byte-level mutations (bit-flip, byte-sub,
    insert/delete, per Rank 10's _OPERATORS).
  * Gate only on: file has ≥1 line (minimal structure) and is <max_bytes.
    NO semantic validity check — let the mutation-oracle be the judge.

This intentionally drops the normalizer gate. Ranks 1-11 preserve
metamorphic semantics; Rank 13 is purely a MUTATION-KILL-CORPUS
generator feeding PIT-style oracles that don't need metamorphic
invariants.

Output: `seeds/<fmt>_rawfuzz/rawfuzz_<sha8>.{vcf,sam}`. Used by
Phase-3 mutation staging, not by Phase-C MR loop (which requires
metamorphic-valid inputs).

References:
  * Miller, Fredriksen & So, CACM'90 — "An Empirical Study of the
    Reliability of UNIX Utilities" showed random byte perturbation
    finds bugs in ~30% of utilities without any structural gating.
  * Padhye et al., ISSTA'19 (Zest) — byte-level fuzzing with
    structural gate beats pure random by 10×, but the structural
    gate is *covers new branches*, not *parses validly*.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

logger = logging.getLogger("lenient_byte_fuzzer")


def _flip_bit(data: bytearray, rng: random.Random) -> None:
    if not data:
        return
    idx = rng.randrange(len(data))
    data[idx] ^= (1 << rng.randrange(8))


def _sub_byte_any(data: bytearray, rng: random.Random) -> None:
    """Any byte value (including non-printable). Jazzer-style."""
    if not data:
        return
    idx = rng.randrange(len(data))
    data[idx] = rng.randrange(0, 256)


def _sub_byte_printable(data: bytearray, rng: random.Random) -> None:
    if not data:
        return
    idx = rng.randrange(len(data))
    data[idx] = rng.randrange(0x20, 0x7f)


def _sub_digit(data: bytearray, rng: random.Random) -> None:
    pos = [i for i, b in enumerate(data) if 0x30 <= b <= 0x39]
    if not pos:
        return
    data[rng.choice(pos)] = rng.randrange(0x30, 0x3a)


def _insert_byte(data: bytearray, rng: random.Random) -> None:
    if not data:
        return
    idx = rng.randrange(len(data))
    data.insert(idx, rng.randrange(0, 256))


def _delete_byte(data: bytearray, rng: random.Random) -> None:
    if len(data) <= 1:
        return
    idx = rng.randrange(len(data))
    del data[idx]


def _flip_tab_to_space(data: bytearray, rng: random.Random) -> None:
    """Flip a random \\t to space (triggers field-delimiter errors)."""
    positions = [i for i, b in enumerate(data) if b == 0x09]
    if not positions:
        return
    data[rng.choice(positions)] = 0x20


def _duplicate_line(data: bytearray, rng: random.Random) -> None:
    """Duplicate a random line (triggers record-iterator-state branches)."""
    text = bytes(data).decode("utf-8", errors="replace")
    lines = text.split("\n")
    if len(lines) < 2:
        return
    idx = rng.randrange(len(lines) - 1)
    lines.insert(idx, lines[idx])
    new_text = "\n".join(lines)
    data.clear()
    data.extend(new_text.encode("utf-8", errors="replace"))


_OPERATORS = [
    # Jazzer-style: full byte range + structural perturbations.
    (_flip_bit,          0.25),
    (_sub_byte_any,      0.20),   # any byte, including non-printable
    (_sub_byte_printable, 0.15),
    (_sub_digit,         0.15),
    (_flip_tab_to_space, 0.10),
    (_insert_byte,       0.07),
    (_delete_byte,       0.05),
    (_duplicate_line,    0.03),
]


def _weighted_choice(rng: random.Random, weighted):
    r = rng.random()
    acc = 0.0
    for item, w in weighted:
        acc += w
        if r <= acc:
            return item
    return weighted[-1][0]


def _mutate(source_bytes: bytes, fmt: str, rng: random.Random,
            n_mutations: int) -> bytes:
    """Apply n byte-level ops. Header lines (VCF `#`, SAM `@`) are kept
    as a weakly-enforced structural anchor — we mutate only non-header
    portions so that SOME parser initialisation happens before the
    garbage hits."""
    lines = source_bytes.split(b"\n")
    prefix = b"#" if fmt.upper() == "VCF" else b"@"
    header = [ln for ln in lines if ln.startswith(prefix) or not ln]
    body = [ln for ln in lines if ln and not ln.startswith(prefix)]
    if not body:
        return source_bytes
    for _ in range(n_mutations):
        if not body:
            break
        idx = rng.randrange(len(body))
        buf = bytearray(body[idx])
        op = _weighted_choice(rng, _OPERATORS)
        op(buf, rng)
        body[idx] = bytes(buf)
    return b"\n".join(header + body)


def _weak_gate(data: bytes, fmt: str) -> bool:
    """Only reject obviously-useless files.

    Rejection criteria:
      * Empty
      * No newline (single line)
      * Contains NUL bytes at file start (likely binary/corrupted header)
    We DO NOT gate on parseability — the oracle will evaluate it.
    """
    if not data:
        return False
    if b"\n" not in data:
        return False
    # Accept anything else — including files with embedded NULs in body,
    # malformed field counts, or invalid Unicode. Parser error-path
    # diversity is exactly what we want.
    return True


def fuzz_directory(
    input_dir: Path, output_dir: Path, fmt: str,
    n_per_seed: int = 30, mutations_per_variant: int = 4,
    seed: int = 42, max_bytes: int = 500_000,
) -> dict:
    """Generate lenient byte-fuzzed variants. NO semantic validity gate."""
    ext = fmt.lower()
    sources = sorted(p for p in input_dir.iterdir()
                     if p.is_file() and p.suffix.lower() == f".{ext}"
                     and not p.name.startswith(("kept_", "diverse_",
                                                "bytefuzz_", "bv_",
                                                "struct_", "rawfuzz_")))
    if not sources:
        raise SystemExit(f"lenient_byte_fuzzer: no {ext} files in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    kept = 0
    rejected_weak = 0
    rejected_dup = 0
    rejected_size = 0
    seen_hashes: set[str] = set()
    for existing in output_dir.glob(f"rawfuzz_*.{ext}"):
        seen_hashes.add(existing.stem[len("rawfuzz_"):])

    for src in sources:
        try:
            src_bytes = src.read_bytes()
        except OSError:
            continue
        for _ in range(n_per_seed):
            mbytes = _mutate(src_bytes, fmt, rng, mutations_per_variant)
            if len(mbytes) > max_bytes:
                rejected_size += 1
                continue
            if not _weak_gate(mbytes, fmt):
                rejected_weak += 1
                continue
            h = hashlib.sha256(mbytes).hexdigest()[:16]
            if h in seen_hashes:
                rejected_dup += 1
                continue
            seen_hashes.add(h)
            (output_dir / f"rawfuzz_{h}.{ext}").write_bytes(mbytes)
            kept += 1

    result = {
        "sources": len(sources),
        "n_per_seed": n_per_seed,
        "mutations_per_variant": mutations_per_variant,
        "attempted": len(sources) * n_per_seed,
        "kept": kept,
        "rejected_weak_gate": rejected_weak,
        "rejected_duplicate": rejected_dup,
        "rejected_size": rejected_size,
        "output_dir": str(output_dir),
    }
    logger.info("lenient_byte_fuzzer result: %s", result)
    return result


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--format", required=True, choices=["VCF", "SAM"])
    p.add_argument("--n-per-seed", type=int, default=30)
    p.add_argument("--mutations-per-variant", type=int, default=4)
    p.add_argument("--seed", type=int, default=42)
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
    )
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
