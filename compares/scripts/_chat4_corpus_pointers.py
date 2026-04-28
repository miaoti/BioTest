#!/usr/bin/env python3
"""Emit corpus_pointers.json for chat4_300 pure_random cells.

Tells Chat 6 where the per-cell pure_random corpus dirs live inside the
biotest-bench-setup container. Corpora are NOT copied to the host
(millions of files per cell would tank the 9p share inode budget).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path, required=True,
                   help="Path inside the container, e.g. /tmp/bug_bench_chat4")
    p.add_argument("--container", default="biotest-bench-setup")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    out = {
        "schema_version": "1",
        "tool": "pure_random",
        "sut": "noodles",
        "format": "VCF",
        "container": args.container,
        "container_corpus_root": str(args.bench_root / "pure_random"),
        "host_path_note": (
            "Corpora are NOT copied to the host. To replay these inputs "
            "from Chat 6, exec into the container and walk "
            f"{args.bench_root}/pure_random/<bug_id>/corpus/. File counts "
            "are huge (millions); sample randomly via `shuf -n N` rather "
            "than iterating the whole dir to avoid 9p inode pressure."
        ),
        "cells": [],
    }

    pr_root = args.bench_root / "pure_random"
    for cell in sorted(pr_root.iterdir() if pr_root.exists() else []):
        if not cell.is_dir():
            continue
        corpus = cell / "corpus"
        n = sum(1 for _ in corpus.iterdir()) if corpus.exists() else 0
        out["cells"].append({
            "bug_id": cell.name,
            "corpus_dir": str(corpus),
            "corpus_file_count": n,
            "has_result_json": (cell / "result.json").exists(),
            "sample_command_example": (
                f"docker exec {args.container} bash -c "
                f"\"ls {corpus} | shuf -n 1000 | "
                f"while read f; do echo {corpus}/$f; done\""
            ),
        })

    args.out.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {args.out} ({len(out['cells'])} cells)")


if __name__ == "__main__":
    main()
