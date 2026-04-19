"""Atheris harness for pysam VCF + SAM parsing.

Run (Linux / WSL2 / macOS; Windows not supported by Atheris):

    python3 compares/harnesses/atheris/fuzz_pysam.py \\
        -atheris_runs=0 \\
        -max_total_time=7200 \\
        -artifact_prefix=compares/results/atheris/pysam_vcf/ \\
        seeds/vcf/

Dispatch between VCF and SAM targets via CLI prefix:

    -- --format=VCF  (default)
    -- --format=SAM

Atheris reports crashes / uncaught Python exceptions as findings. The
harness catches only the exceptions pysam raises for legitimately
malformed input.
"""

from __future__ import annotations

import io
import sys
import tempfile
from pathlib import Path

import atheris

# Delayed imports so Atheris can instrument them when Setup() runs.
with atheris.instrument_imports():
    import pysam


FORMAT = "VCF"   # overridden from argv before Setup()


def _with_temp_input(data: bytes, suffix: str):
    """Write bytes to a temporary file and return its Path."""
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, prefix="atheris-pysam-"
    )
    try:
        tmp.write(data)
        tmp.flush()
        return Path(tmp.name)
    finally:
        tmp.close()


def fuzz_vcf(data: bytes) -> None:
    if not data:
        return
    path = _with_temp_input(data, ".vcf")
    try:
        vf = pysam.VariantFile(str(path))
        try:
            _ = vf.header
            for rec in vf:
                # Touch every lazy-resolved field so we exercise the
                # genotype / INFO decoder paths, not just the record loop.
                _ = rec.pos, rec.id, rec.ref, rec.alts, rec.qual
                _ = dict(rec.info)
                for s in rec.samples.values():
                    _ = dict(s)
        finally:
            vf.close()
    except (OSError, ValueError) as expected:
        # pysam raises ValueError for malformed headers and OSError for
        # file-level problems. Both are expected on adversarial bytes.
        del expected
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def fuzz_sam(data: bytes) -> None:
    if not data:
        return
    path = _with_temp_input(data, ".sam")
    try:
        af = pysam.AlignmentFile(str(path), check_sq=False)
        try:
            _ = af.header
            for rec in af:
                _ = rec.query_name, rec.cigar, rec.reference_start
                _ = rec.query_sequence, rec.query_qualities
                _ = dict(rec.tags) if rec.tags else {}
        finally:
            af.close()
    except (OSError, ValueError) as expected:
        del expected
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def _dispatch(data: bytes) -> None:
    if FORMAT == "SAM":
        fuzz_sam(data)
    else:
        fuzz_vcf(data)


def main() -> None:
    global FORMAT
    argv = list(sys.argv)
    # Strip our own --format=X flag so Atheris doesn't see it.
    cleaned = []
    for tok in argv:
        if tok.startswith("--format="):
            FORMAT = tok.split("=", 1)[1].upper()
        else:
            cleaned.append(tok)

    atheris.Setup(cleaned, _dispatch)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
