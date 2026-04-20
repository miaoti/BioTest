"""Inline replay driver for coverage.py.

Uses the programmatic coverage API so heavyweight C-extension
dependencies (NumPy, in Biopython's case) load BEFORE coverage's
tracer attaches — avoiding `ImportError: cannot load module more
than once per process` on NumPy 2.x + coverage.py CTracer.
"""
import os, sys

sut = sys.argv[1]
fmt = sys.argv[2]
data_file = sys.argv[3]
source_pkg = sys.argv[4]
files = sys.argv[5:]

# Pre-import heavy deps BEFORE coverage attaches so NumPy's C ext.
# is loaded exactly once. (coverage.py's CTracer triggers a second
# load via its import hooks which NumPy 2.x rejects.)
if sut == "biopython":
    import numpy  # noqa: F401
    from Bio.Align import sam as _sam
elif sut == "vcfpy":
    import vcfpy

import coverage
cov = coverage.Coverage(
    data_file=data_file,
    source=[source_pkg],
    branch=True,
)
cov.start()

ok = rej = 0
try:
    if sut == "vcfpy":
        for path in files:
            try:
                with vcfpy.Reader.from_path(path) as r:
                    for _ in r:
                        pass
                ok += 1
            except Exception:
                rej += 1
    elif sut == "biopython":
        for path in files:
            try:
                with open(path) as fh:
                    for _ in _sam.AlignmentIterator(fh):
                        pass
                ok += 1
            except Exception:
                rej += 1
    else:
        print(f"unknown sut {sut!r}", file=sys.stderr)
        sys.exit(2)
finally:
    cov.stop()
    cov.save()

print(f"replay: ok={ok} rej={rej}", file=sys.stderr)
