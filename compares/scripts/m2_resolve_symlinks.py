"""Resolve Docker-internal symlinks (/work/...) in m2_cmin output dirs.

corpus_minimize.py runs inside biotest-bench and creates symlinks pointing
to /work/<rel>. Those targets are valid inside Docker but break on the
Windows host. The mutation_driver.py vcfpy path needs to read the corpus
dir on the host before shelling into Docker, so this script re-materialises
each cmin output dir as host-side file copies, using the kept.manifest.jsonl
+ the original input corpus dir as the source.

Mapping (cell → input corpus dir):
  vcfpy_biotest      → compares/results/coverage/biotest_rep_<r>/vcfpy/run_0/corpus
  biopython_biotest  → compares/results/coverage/biotest_rep_<r>/biopython/run_0/corpus
  biopython_atheris  → compares/results/coverage/atheris/biopython/run_<r>/corpus
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def input_dir_for(cell: str, rep: int) -> Path:
    if cell == "vcfpy_biotest":
        return REPO / f"compares/results/coverage/biotest_rep_{rep}/vcfpy/run_0/corpus"
    if cell == "biopython_biotest":
        return REPO / f"compares/results/coverage/biotest_rep_{rep}/biopython/run_0/corpus"
    if cell == "biopython_atheris":
        return REPO / f"compares/results/coverage/atheris/biopython/run_{rep}/corpus"
    raise ValueError(f"unknown cell {cell!r}")


def rebuild_dir(cmin_dir: Path, input_dir: Path) -> tuple[int, int]:
    """Re-materialise cmin_dir as host file copies of the kept set,
    based on `kept.manifest.jsonl`. Returns (n_copied, n_missing)."""
    manifest_path = cmin_dir / "kept.manifest.jsonl"
    if not manifest_path.exists():
        print(f"  skip (no manifest): {cmin_dir}")
        return 0, 0
    kept_names: list[str] = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        name = obj.get("file")
        if isinstance(name, str):
            kept_names.append(name)

    # Wipe and re-create the dir with real file copies.
    for child in cmin_dir.iterdir():
        if child.name == "kept.manifest.jsonl":
            continue
        try:
            child.unlink()
        except (OSError, IsADirectoryError):
            shutil.rmtree(child, ignore_errors=True)

    n_copied = n_missing = 0
    for name in kept_names:
        src = input_dir / name
        if not src.exists():
            n_missing += 1
            continue
        shutil.copy2(src, cmin_dir / name)
        n_copied += 1
    return n_copied, n_missing


def main() -> int:
    cells = ["vcfpy_biotest", "biopython_biotest", "biopython_atheris"]
    total_c = total_m = 0
    for cell in cells:
        for rep in range(4):
            input_d = input_dir_for(cell, rep)
            for strat in ("kf", "of"):
                cmin_d = REPO / f"compares/results/m2_cmin/{cell}/rep_{rep}/{strat}"
                if not cmin_d.exists():
                    continue
                c, m = rebuild_dir(cmin_d, input_d)
                total_c += c; total_m += m
                print(f"{cmin_d.relative_to(REPO)}: copied={c} missing={m}")
    print(f"\nTOTAL: copied={total_c} missing={total_m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
