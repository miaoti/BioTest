"""Atheris harness for Biopython's SAM parsing path (Bio.Align.sam).

Run (Linux / WSL2 / macOS):

    python3 compares/harnesses/atheris/fuzz_biopython.py \\
        -atheris_runs=0 \\
        -max_total_time=7200 \\
        -artifact_prefix=compares/results/atheris/biopython_sam/ \\
        seeds/sam/

Biopython has no VCF parser — only SAM is fuzzed here.

Atheris reports uncaught exceptions as findings. The harness catches
only the exceptions Biopython raises for legitimately malformed input.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import atheris

with atheris.instrument_imports():
    # Bio.Align.sam is the modern SAM parser entry point.
    import Bio.Align  # noqa: F401
    from Bio.Align import sam as _biopython_sam  # noqa: F401


def fuzz_sam(data: bytes) -> None:
    if not data:
        return
    try:
        text = data.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        return

    buf = io.StringIO(text)
    try:
        alignments = _biopython_sam.AlignmentIterator(buf)
        for aln in alignments:
            _ = aln.target
            _ = aln.query
            _ = aln.score if hasattr(aln, "score") else None
            _ = str(aln.coordinates) if hasattr(aln, "coordinates") else None
    except (ValueError, StopIteration, AttributeError) as expected:
        del expected


def main() -> None:
    atheris.Setup(sys.argv, fuzz_sam)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
