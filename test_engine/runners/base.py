"""
Abstract base class for parser runners and the RunnerResult model.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel


class RunnerResult(BaseModel):
    """Result of running a parser on an input file."""
    success: bool
    canonical_json: Optional[dict[str, Any]] = None
    stderr: str = ""
    exit_code: int = 0
    duration_ms: float = 0.0
    parser_name: str
    format_type: str
    error_type: Optional[str] = None  # "timeout" | "crash" | "parse_error"


class ParserRunner(ABC):
    """Abstract base for parser runners."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Short name: 'htsjdk', 'pysam', 'biopython', 'seqan3'."""
        ...

    @property
    @abstractmethod
    def supported_formats(self) -> set[str]:
        """Set of format strings: {'VCF', 'SAM'}."""
        ...

    @abstractmethod
    def run(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        """Parse the input file and return canonical JSON."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this runner's parser is installed and functional."""
        ...

    def supports(self, format_type: str) -> bool:
        """Check if this runner supports the given format."""
        return format_type.upper() in self.supported_formats
