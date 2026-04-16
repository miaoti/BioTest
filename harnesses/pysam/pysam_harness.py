#!/usr/bin/env python3
"""
pysam canonical JSON harness — runs inside Docker container.

Usage:
    python pysam_harness.py VCF /data/input.vcf
    python pysam_harness.py SAM /data/input.sam
    python pysam_harness.py --coverage /cov/dir VCF /data/input.vcf

Outputs canonical JSON to stdout. Errors go to stderr with exit code 1.

CRITICAL: pysam uses 0-based coordinates for ALL formats (including VCF).
This harness adds +1 to POS for both VCF and SAM, and +1 to PNEXT for SAM.

CRITICAL: When --coverage is used, coverage.py MUST start before any pysam
import so it can instrument the module. The coverage setup is done at the
very top of main() before the lazy pysam import in parse_vcf/parse_sam.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


def parse_vcf(path: Path) -> dict[str, Any]:
    """Parse VCF via pysam into canonical dict."""
    import pysam

    vcf = pysam.VariantFile(str(path))
    header = vcf.header

    # Header
    meta: dict[str, Any] = {}
    for rec in header.records:
        if rec.type == "GENERIC":
            continue
        key = rec.key
        if hasattr(rec, "items") and callable(rec.items):
            fields = dict(rec.items())
            entry_id = fields.get("ID", "")
            if key not in meta:
                meta[key] = {}
            if isinstance(meta[key], dict):
                meta[key][entry_id] = fields

    samples = list(header.samples)

    # Records
    records = []
    for rec in vcf:
        # CRITICAL: pysam rec.pos is 0-based! Add +1 for 1-based canonical.
        pos = rec.pos + 1

        rec_id = None if rec.id is None else rec.id
        alt = list(rec.alts) if rec.alts else []
        qual = None if rec.qual is None else float(rec.qual)

        # FILTER
        filt = sorted(list(rec.filter.keys())) if rec.filter else []

        # INFO
        info: dict[str, Any] = {}
        for key in rec.info:
            val = rec.info[key]
            if isinstance(val, tuple):
                val = list(val)
            info[key] = val
        info = dict(sorted(info.items()))

        # Samples
        sample_data: dict[str, dict] = {}
        for sample_name in samples:
            sample = rec.samples[sample_name]
            fields: dict[str, Any] = {}
            for key in sample.keys():
                val = sample[key]
                if isinstance(val, tuple):
                    val = list(val)
                fields[key] = val
            sample_data[sample_name] = fields

        fmt = list(rec.format.keys()) if rec.format else None

        records.append({
            "CHROM": rec.chrom,
            "POS": pos,
            "ID": rec_id,
            "REF": rec.ref,
            "ALT": alt,
            "QUAL": qual,
            "FILTER": filt,
            "INFO": info,
            "FORMAT": fmt,
            "samples": sample_data if sample_data else None,
        })

    vcf.close()

    return {
        "format": "VCF",
        "header": {
            "fileformat": str(header.version) if hasattr(header, "version") else "",
            "meta": meta,
            "samples": samples,
        },
        "records": records,
    }


def parse_sam(path: Path) -> dict[str, Any]:
    """Parse SAM via pysam into canonical dict."""
    import pysam

    sam = pysam.AlignmentFile(str(path), "r")
    header = sam.header

    # Header
    hd = dict(header.get("HD", {})) if "HD" in header else None
    sq = [dict(s) for s in header.get("SQ", [])]
    rg = [dict(r) for r in header.get("RG", [])]
    pg = [dict(p) for p in header.get("PG", [])]
    co = sorted(header.get("CO", []))

    # Records
    records = []
    for read in sam:
        # CRITICAL: pysam reference_start is 0-based! Add +1.
        pos = None if read.is_unmapped else read.reference_start + 1
        pnext = None
        if read.next_reference_start is not None and read.next_reference_start >= 0:
            pnext = read.next_reference_start + 1

        # CIGAR
        cigar = None
        if read.cigartuples:
            op_map = {0: "M", 1: "I", 2: "D", 3: "N", 4: "S", 5: "H", 6: "P", 7: "=", 8: "X"}
            cigar = [{"op": op_map.get(op, "?"), "len": length}
                     for op, length in read.cigartuples]

        # Tags
        tags = {}
        for tag_name, tag_val in read.get_tags(with_value_type=True):
            tag_type = tag_val[0] if isinstance(tag_val, tuple) else "Z"
            val = tag_val[1] if isinstance(tag_val, tuple) else tag_val
            tags[tag_name] = {"type": tag_type, "value": val}
        tags = dict(sorted(tags.items()))

        records.append({
            "QNAME": read.query_name,
            "FLAG": read.flag,
            "RNAME": None if read.reference_name is None else read.reference_name,
            "POS": pos,
            "MAPQ": read.mapping_quality,
            "CIGAR": cigar,
            "RNEXT": None if read.next_reference_name is None else read.next_reference_name,
            "PNEXT": pnext,
            "TLEN": read.template_length,
            "SEQ": None if read.query_sequence is None else read.query_sequence,
            "QUAL": None if read.query_qualities is None else "".join(
                chr(q + 33) for q in read.query_qualities
            ),
            "tags": tags,
        })

    sam.close()

    return {
        "format": "SAM",
        "header": {"HD": hd, "SQ": sq, "RG": rg, "PG": pg, "CO": co},
        "records": records,
    }


def _run_parse(fmt: str, input_path: Path) -> None:
    """Core parse-and-emit logic."""
    if fmt == "VCF":
        result = parse_vcf(input_path)
    elif fmt == "SAM":
        result = parse_sam(input_path)
    else:
        print(f"Unsupported format: {fmt}", file=sys.stderr)
        sys.exit(1)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)


def main():
    # Parse args: [--coverage /cov/dir] FORMAT INPUT_FILE
    args = sys.argv[1:]
    coverage_dir = None

    if args and args[0] == "--coverage":
        if len(args) < 2:
            print("--coverage requires a directory argument", file=sys.stderr)
            sys.exit(1)
        coverage_dir = Path(args[1])
        args = args[2:]

    if len(args) != 2:
        print(
            f"Usage: {sys.argv[0]} [--coverage /cov/dir] <VCF|SAM> <input_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    fmt = args[0].upper()
    input_path = Path(args[1])

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Coverage must start BEFORE pysam is imported (parse_vcf/parse_sam
    # import pysam at function call time). We instrument the pysam
    # site-packages directory so coverage.py traces into it.
    _cov_instance = None
    if coverage_dir:
        try:
            import coverage as _cov
            import os

            # Point source= at the pysam package dir so coverage.py
            # instruments site-packages (normally excluded).
            import importlib.util
            pysam_spec = importlib.util.find_spec("pysam")
            pysam_dir = str(Path(pysam_spec.origin).parent) if pysam_spec and pysam_spec.origin else None

            cov_file = str(coverage_dir / f".coverage.{os.getpid()}")
            _cov_instance = _cov.Coverage(
                data_file=cov_file,
                source=[pysam_dir] if pysam_dir else None,
            )
            _cov_instance.start()
        except Exception as e:
            # Coverage was explicitly requested; failing silently would
            # produce a harness result with no .coverage.* file and the
            # host-side collector would record zero coverage, poisoning
            # Phase D's SCC signal. Fail loudly instead.
            print(f"Coverage setup FAILED (requested via --coverage): {e}", file=sys.stderr)
            try:
                (coverage_dir / f"coverage_setup_failed.{os.getpid()}.log").write_text(
                    f"{type(e).__name__}: {e}\n", encoding="utf-8"
                )
            except Exception:
                pass
            sys.exit(2)

    try:
        _run_parse(fmt, input_path)
    except Exception as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if _cov_instance:
            _cov_instance.stop()
            _cov_instance.save()
            # Write a coverage summary JSON for the host-side collector.
            # This includes total lines per file (which the host can't compute
            # because the source files are inside the container).
            try:
                import os
                summary = {}
                data = _cov_instance.get_data()
                for filepath in data.measured_files():
                    executed = data.lines(filepath) or []
                    # Read source to count total lines
                    total_lines = 0
                    try:
                        with open(filepath, "r") as src:
                            total_lines = sum(1 for _ in src)
                    except OSError:
                        total_lines = len(executed)
                    fname = Path(filepath).name
                    summary[fname] = {
                        "executed": len(executed),
                        "total": total_lines,
                        "missing": sorted(set(range(1, total_lines + 1)) - set(executed)),
                    }
                summary_path = coverage_dir / f"summary.{os.getpid()}.json"
                import json as _json
                with open(summary_path, "w") as f:
                    _json.dump(summary, f, indent=2)
            except Exception:
                pass  # Best-effort


if __name__ == "__main__":
    main()
