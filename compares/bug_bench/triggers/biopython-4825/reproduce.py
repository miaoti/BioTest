"""Time a 10 000-record SAM parse under Biopython pre/post fix.

Usage (inside biotest-bench):

    # Pre-fix (slow):
    /work/compares/results/sut-envs/biopython/bin/pip install --force-reinstall biopython==1.85
    /work/compares/results/sut-envs/biopython/bin/python reproduce.py

    # Post-fix (fast):
    /work/compares/results/sut-envs/biopython/bin/pip install --force-reinstall biopython==1.86
    /work/compares/results/sut-envs/biopython/bin/python reproduce.py

Detection: pre-fix parse time >> post-fix parse time for the same
file, with identical record counts. DESIGN §13.4.4 treats that gap
as the bug-detection signal.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
LARGE = HERE / "large.sam"


def main() -> None:
    if not LARGE.exists():
        subprocess.check_call([sys.executable, str(HERE / "generate_large_sam.py")])

    from Bio.Align import sam as biopython_sam

    with LARGE.open("r", encoding="ascii") as fh:
        start = time.perf_counter()
        alns = list(biopython_sam.AlignmentIterator(fh))
        elapsed = time.perf_counter() - start

    print(f"records: {len(alns)}  elapsed: {elapsed:.2f}s")
    # Empirical threshold on a modern laptop:
    #   pre-fix  1.85:  ~4-6 s for 10k records
    #   post-fix 1.86:  ~0.5-1 s for 10k records
    # A factor-of-5 slowdown is the detection signal for the bench.


if __name__ == "__main__":
    main()
