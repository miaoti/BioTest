"""
Seed corpus loader.

Tier 1: Handcrafted seeds from seeds/ directory.
Tier 2: Real-world (IGSR/GIAB) — deferred, not yet implemented.
Tier 3: Z3-generated corner cases — see z3_constraints.py.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ..config import SEEDS_DIR

logger = logging.getLogger(__name__)


class SeedCorpus:
    """Loads and manages test seed files."""

    def __init__(self, seeds_dir: Path = SEEDS_DIR):
        self._seeds_dir = seeds_dir
        self._vcf_seeds: list[Path] = []
        self._sam_seeds: list[Path] = []
        self._load()

    def _load(self) -> None:
        """Discover seed files from the seeds directory."""
        vcf_dir = self._seeds_dir / "vcf"
        sam_dir = self._seeds_dir / "sam"

        if vcf_dir.exists():
            self._vcf_seeds = sorted(vcf_dir.glob("*.vcf"))
        if sam_dir.exists():
            self._sam_seeds = sorted(sam_dir.glob("*.sam"))

        logger.info(
            "Seed corpus loaded: %d VCF seeds, %d SAM seeds",
            len(self._vcf_seeds), len(self._sam_seeds),
        )

    @property
    def vcf_seeds(self) -> list[Path]:
        return list(self._vcf_seeds)

    @property
    def sam_seeds(self) -> list[Path]:
        return list(self._sam_seeds)

    def seeds_for_format(self, fmt: str) -> list[Path]:
        """Return seeds for a given format ('VCF' or 'SAM')."""
        if fmt.upper() == "VCF":
            return self.vcf_seeds
        elif fmt.upper() == "SAM":
            return self.sam_seeds
        return []

    @staticmethod
    def read_lines(path: Path) -> list[str]:
        """Read a seed file as a list of lines."""
        return path.read_text(encoding="utf-8").splitlines(keepends=True)
