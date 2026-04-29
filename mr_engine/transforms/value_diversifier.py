"""Rank 9 — Validity-preserving value diversifier.

BioTest's metamorphic transforms (Ranks 1-8) are **semantics-preserving**
by construction: `parse(T(x)) == parse(x)` is the defining MR property.
That makes them excellent for oracle-based bug detection but sub-optimal
for mutation-score adequacy, because mutation operators like Math
(`+` → `-`), RemoveConditional (`>` → `false`), and VoidMethodCall
(delete side-effect) require inputs with **numerical diversity** to
be killed — inputs that produce *different* numerical parser outputs
when a mutant is applied.  See
`compares/results/mutation/biotest/WHY_BIOTEST_UNDERPERFORMS.md`
for the operator-level breakdown.

This module provides a **validity-preserving value diversifier**:
for each seed file, generate N byte-distinct copies where numerical
fields (POS, QUAL, MAPQ, AF, DP, TLEN) have been randomised within
spec-valid ranges.  Each copy parses cleanly through the canonical
normalizer — so every file is a valid corpus input — but produces a
different canonical JSON than the source.

This is intentionally **not** a metamorphic transform.  It doesn't feed
the oracle (we don't compare `parse(T(x))` to `parse(x)` — they won't
match).  It only populates the seed corpus to give mutation tools
the numerical diversity they need to kill arithmetic mutants.

SUT-agnostic: every numerical field is positioned by column index in
the standard VCF/SAM grammar, so adding a new SUT needs zero
diversifier changes.  Specific per-field bounds come from the VCF
and SAM specs (not from any SUT's implementation quirks).

References:
  * Offutt & Untch, "Mutation 2000: Uniting the Orthogonal", Mutation
    Testing for the New Century 2001 — the case for numerical
    diversity as a first-class corpus-selection signal.
  * Padhye et al., ISSTA'19 (Zest) — shows that validity-gated random
    byte-level mutations match coverage-guided fuzzers at ~10× lower
    cost.  This diversifier is Zest restricted to numerical fields
    plus strict validity gating.
"""
from __future__ import annotations

import argparse
import hashlib
import logging
import random
import re
import sys
from pathlib import Path
from typing import Callable, Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

logger = logging.getLogger("value_diversifier")


# ---------------------------------------------------------------------------
# VCF per-field perturbations
# ---------------------------------------------------------------------------

def _perturb_vcf_record(
    line: str, rng: random.Random, pos_max: int = 3_000_000_000,
) -> str:
    """Perturb a single VCF body line (8+ tab-separated columns)."""
    parts = line.rstrip("\r\n").split("\t")
    if len(parts) < 8:
        return line

    # POS (column 2, 1-based) — shift by ±10k or pick fresh within chrom bounds
    try:
        pos = int(parts[1])
        delta = rng.choice([rng.randint(-10_000, 10_000),
                            rng.randint(1, min(pos_max, 2_000_000))])
        new_pos = pos + delta if rng.random() < 0.7 else delta
        parts[1] = str(max(1, min(new_pos, pos_max)))
    except (ValueError, IndexError):
        pass

    # QUAL (column 6) — scale by random factor (0 to 9999)
    try:
        q = parts[5]
        if q != "." and q != "":
            qf = float(q)
            scale = rng.choice([0.0, 0.5, 1.5, 2.0, 10.0])
            parts[5] = f"{qf * scale:.1f}"
    except (ValueError, IndexError):
        pass

    # INFO (column 8) — perturb numeric k=v pairs
    try:
        info = parts[7]
        if info not in (".", ""):
            new_info_parts = []
            for kv in info.split(";"):
                if "=" not in kv:
                    new_info_parts.append(kv)
                    continue
                k, _, v = kv.partition("=")
                # AF — allele frequency [0, 1]
                if k == "AF" and "," not in v:
                    try:
                        float(v); new_info_parts.append(f"{k}={rng.random():.4f}"); continue
                    except ValueError: pass
                # DP — depth [0, 10000]
                if k == "DP":
                    try:
                        int(v); new_info_parts.append(f"{k}={rng.randint(0, 10_000)}"); continue
                    except ValueError: pass
                # MQ — mapping quality [0, 60]
                if k == "MQ":
                    try:
                        float(v); new_info_parts.append(f"{k}={rng.randint(0, 60)}"); continue
                    except ValueError: pass
                new_info_parts.append(kv)
            parts[7] = ";".join(new_info_parts)
    except IndexError:
        pass

    return "\t".join(parts) + "\n"


def diversify_vcf(
    source_text: str, n_variants: int, rng: random.Random,
) -> list[str]:
    """Produce N byte-varied copies of a VCF file with numerical fields perturbed."""
    out: list[str] = []
    lines = source_text.splitlines(keepends=True)
    for _ in range(n_variants):
        mutated: list[str] = []
        for ln in lines:
            if not ln.strip():
                mutated.append(ln); continue
            if ln.startswith("#"):
                mutated.append(ln); continue
            mutated.append(_perturb_vcf_record(ln, rng))
        out.append("".join(mutated))
    return out


# ---------------------------------------------------------------------------
# SAM per-field perturbations
# ---------------------------------------------------------------------------

_SAM_CIGAR_OP_RE = re.compile(r"(\d+)([MIDNSHP=X])")

def _cigar_query_len(cigar: str) -> Optional[int]:
    if cigar == "*" or not cigar:
        return None
    total = 0
    for n, op in _SAM_CIGAR_OP_RE.findall(cigar):
        if op in ("M", "I", "S", "=", "X"):
            total += int(n)
    return total


def _perturb_sam_record(line: str, rng: random.Random) -> str:
    """Perturb one SAM body line (11+ tab-separated columns)."""
    parts = line.rstrip("\r\n").split("\t")
    if len(parts) < 11:
        return line

    # POS (col 4, 1-based)
    try:
        pos = int(parts[3])
        if pos > 0:
            delta = rng.randint(-10_000, 10_000)
            parts[3] = str(max(0, pos + delta))
    except ValueError:
        pass

    # MAPQ (col 5) — [0, 255]; usually [0, 60] in practice
    try:
        int(parts[4])
        parts[4] = str(rng.randint(0, 60))
    except ValueError:
        pass

    # PNEXT (col 8) — mate position
    try:
        pnext = int(parts[7])
        if pnext > 0:
            parts[7] = str(max(0, pnext + rng.randint(-10_000, 10_000)))
    except ValueError:
        pass

    # TLEN (col 9) — insert size, signed
    try:
        tlen = int(parts[8])
        parts[8] = str(tlen + rng.randint(-500, 500))
    except ValueError:
        pass

    # Optional tags — randomise known numeric tag values by type
    for i in range(11, len(parts)):
        tag = parts[i]
        m = re.match(r"^(\w\w):(A|i|f|Z|H|B):(.+)$", tag)
        if not m:
            continue
        name, typ, val = m.groups()
        try:
            if typ == "i":
                parts[i] = f"{name}:{typ}:{int(val) + rng.randint(-100, 100)}"
            elif typ == "f":
                fv = float(val)
                parts[i] = f"{name}:{typ}:{fv * rng.uniform(0.5, 1.5):.4f}"
        except ValueError:
            pass

    return "\t".join(parts) + "\n"


def diversify_sam(
    source_text: str, n_variants: int, rng: random.Random,
) -> list[str]:
    """Produce N byte-varied copies of a SAM file with numerical fields perturbed."""
    out: list[str] = []
    lines = source_text.splitlines(keepends=True)
    for _ in range(n_variants):
        mutated: list[str] = []
        for ln in lines:
            if not ln.strip():
                mutated.append(ln); continue
            if ln.startswith("@"):
                mutated.append(ln); continue
            mutated.append(_perturb_sam_record(ln, rng))
        out.append("".join(mutated))
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def _validate(text: str, fmt: str, sut_validate: Optional[str] = None) -> bool:
    """Validity gate: parse through canonical_normalizer without raising.

    Refinement C (2026-04-22): if `sut_validate` is given, ALSO probe the
    candidate through that SUT's in-process parser. Prevents the biopython
    regression where perturbed files pass the canonical normalizer
    (forgiving, ~70 %) but fail biopython's strict `AlignmentIterator`
    (30 %) — wasting mutation-corpus budget on inputs the target SUT
    rejects at parse time.

    Supported `sut_validate` values (Python SUTs — direct import, no
    subprocess overhead so ~1 ms per file):
      * `biopython` — `Bio.Align.sam.AlignmentIterator`
      * `vcfpy`     — `vcfpy.Reader.from_stream`

    For Java/C++/Rust SUTs the SUT-parser probe is skipped (each probe
    would be a subprocess fork; too expensive in a 10-50k-variant loop).
    The normalizer gate remains; those parsers tend to be more forgiving
    than biopython's anyway, so the regression pattern doesn't manifest.
    """
    try:
        if fmt.upper() == "VCF":
            from test_engine.canonical.vcf_normalizer import normalize_vcf_text
            normalize_vcf_text(text.splitlines(keepends=True))
        else:
            from test_engine.canonical.sam_normalizer import normalize_sam_text
            normalize_sam_text(text.splitlines(keepends=True))
    except Exception:
        return False
    # Refinement C — optional SUT-parser gate.
    if sut_validate:
        sv = sut_validate.lower()
        try:
            if sv == "biopython" and fmt.upper() == "SAM":
                import io as _io
                from Bio.Align import sam as _biopython_sam
                it = _biopython_sam.AlignmentIterator(_io.StringIO(text))
                for _ in it:
                    pass
            elif sv == "vcfpy" and fmt.upper() == "VCF":
                import io as _io
                import vcfpy as _vcfpy
                rdr = _vcfpy.Reader.from_stream(_io.StringIO(text))
                for _ in rdr:
                    pass
                rdr.close()
            # Any other sut_validate value is a no-op (non-Python SUT or
            # format mismatch).
        except Exception:
            return False
    return True


def diversify_directory(
    input_dir: Path, output_dir: Path, fmt: str,
    n_per_seed: int = 10, seed: int = 42, max_bytes: int = 500_000,
    write_to_seeds: bool = True, sut_validate: Optional[str] = None,
) -> dict:
    """Walk input_dir, generate n_per_seed validity-preserving variants per seed,
    write valid ones to output_dir as `diverse_<sha8>.<ext>`.

    `sut_validate` (Refinement C): when set to a Python SUT name
    (currently `biopython` or `vcfpy`), each candidate is also probed
    through that SUT's in-process parser. Files that pass the canonical
    normalizer but fail the SUT parser are rejected before writing.
    Prevents the biopython regression observed in run-3 where strict-
    parser rejects wasted 70 % of the mutation-corpus budget.
    """
    ext = fmt.lower()
    sources = sorted(p for p in input_dir.iterdir()
                     if p.is_file() and p.suffix.lower() == f".{ext}")
    if not sources:
        raise SystemExit(f"value_diversifier: no {ext} files in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    per_file = diversify_vcf if fmt.upper() == "VCF" else diversify_sam
    kept = 0
    rejected_invalid = 0
    rejected_dup = 0
    rejected_size = 0
    seen_hashes: set[str] = set()
    # Pre-populate with existing diverse_*.* to avoid re-writing on re-runs.
    for existing in output_dir.glob(f"diverse_*.{ext}"):
        seen_hashes.add(existing.stem[len("diverse_"):])

    for src in sources:
        try:
            text = src.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for variant in per_file(text, n_per_seed, rng):
            if not variant:
                continue
            if len(variant.encode("utf-8")) > max_bytes:
                rejected_size += 1
                continue
            h = hashlib.sha256(variant.encode("utf-8")).hexdigest()[:16]
            if h in seen_hashes:
                rejected_dup += 1
                continue
            if not _validate(variant, fmt, sut_validate=sut_validate):
                rejected_invalid += 1
                continue
            seen_hashes.add(h)
            dest = output_dir / f"diverse_{h}.{ext}"
            dest.write_text(variant, encoding="utf-8")
            kept += 1

    result = {
        "sources": len(sources),
        "n_per_seed": n_per_seed,
        "attempted": len(sources) * n_per_seed,
        "kept": kept,
        "rejected_invalid": rejected_invalid,
        "rejected_duplicate": rejected_dup,
        "rejected_size": rejected_size,
        "output_dir": str(output_dir),
    }
    logger.info("diversifier result: %s", result)
    return result


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, required=True,
                   help="Directory of source seeds.")
    p.add_argument("--output", type=Path, required=True,
                   help="Output directory (seeds/<fmt>/ is the default target).")
    p.add_argument("--format", required=True, choices=["VCF", "SAM"])
    p.add_argument("--n-per-seed", type=int, default=10,
                   help="How many variants to try per input seed (default 10).")
    p.add_argument("--seed", type=int, default=42,
                   help="RNG seed for reproducibility.")
    p.add_argument("--sut-validate", default=None,
                   help="Refinement C: also probe each candidate through "
                        "this SUT's in-process parser. Supported: biopython "
                        "(SAM), vcfpy (VCF). Java/C++/Rust SUTs are skipped "
                        "(too expensive per-file via subprocess).")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    r = diversify_directory(
        input_dir=args.input.resolve(),
        output_dir=args.output.resolve(),
        fmt=args.format,
        n_per_seed=args.n_per_seed,
        seed=args.seed,
        sut_validate=args.sut_validate,
    )
    import json as _json
    print(_json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
