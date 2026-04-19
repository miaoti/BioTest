"""
Abstract base class for parser runners and the RunnerResult model.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel


class RunnerResult(BaseModel):
    """Result of running a parser on an input file.

    `error_type` values:
      - "timeout"     — subprocess exceeded timeout_s.
      - "crash"       — unexpected runtime failure (NPE, segfault, etc.).
      - "parse_error" — runner parsed the file but rejected its contents.
      - "ineligible"  — the format was outside this runner's declared
                        supported_formats (e.g. HTSlibRunner asked for
                        BAM, BiopythonRunner asked for VCF). Consensus
                        DISCARDS these results entirely — they do not
                        count as "different" votes, nor are they listed
                        under dissenting/failing voters.
    """
    success: bool
    canonical_json: Optional[dict[str, Any]] = None
    stderr: str = ""
    exit_code: int = 0
    duration_ms: float = 0.0
    parser_name: str
    format_type: str
    error_type: Optional[str] = None


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

    # ------------------------------------------------------------------
    # OPTIONAL: write_roundtrip contract
    # ------------------------------------------------------------------
    # Runners that expose a parse→serialize round-trip (parse the input,
    # re-emit it through the SUT's own public writer API, return the
    # rewritten text) implement `run_write_roundtrip` and set
    # `supports_write_roundtrip = True`. The single SUT-agnostic
    # `sut_write_roundtrip` transform (in mr_engine/transforms/vcf.py)
    # dispatches to whichever runner is nominated as primary at
    # Phase C time — so the ROUND_TRIP_INVARIANCE theme's writer tests
    # stay one transform in the MR registry regardless of how many SUTs
    # the user has wired up.
    #
    # This method deliberately DOES NOT default to parse-then-manually-
    # serialize — that would silently mask a missing writer and report
    # coverage that didn't actually exercise the SUT's write path.
    # Default is "not supported": raise NotImplementedError so the
    # dispatch layer can safely fall through to a no-op.
    supports_write_roundtrip: bool = False

    def run_write_roundtrip(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = 30.0,
    ) -> "RunnerResult":
        """Parse `input_path` and re-serialize via the SUT's writer.

        Return a RunnerResult whose `canonical_json["rewritten_text"]`
        holds the re-serialized bytes decoded as str. Runners without
        a native write API raise NotImplementedError; the dispatch
        layer treats this as "no-op, return input unchanged".
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not implement run_write_roundtrip"
        )

    # ------------------------------------------------------------------
    # OPTIONAL: API-query contract (Rank 5 lever)
    # ------------------------------------------------------------------
    # Runners that can invoke scalar-returning public query methods on
    # their parsed objects (e.g. VariantContext.isStructural(),
    # SAMRecord.isProperPair()) implement `run_query_methods` + set
    # `supports_query_methods = True`. The runner-agnostic
    # `query_method_roundtrip` transform dispatches to whichever runner
    # is primary, same pattern as `sut_write_roundtrip`.
    #
    # Discovery is opt-in too: `discover_query_methods(fmt)` returns a
    # list of dicts {name, returns, args} that the Phase B LLM prompt
    # renders, so MR mining can reference method names the primary SUT
    # actually exposes — no hardcoded per-SUT method lists in the
    # framework.
    #
    # Citation — API-level / query-method metamorphic relations: Chen,
    # Kuo, Liu, Tse (ACM CSUR 2018) §3.2; MR-Scout (Xu et al., TOSEM
    # 2024, arXiv:2304.07548) — mines query-method MRs from existing
    # tests and reports +13.5 pp line coverage on 701 OSS projects.
    supports_query_methods: bool = False

    def discover_query_methods(
        self,
        format_type: str,
    ) -> list[dict[str, Any]]:
        """Return a list of query-method descriptors the LLM can reference.

        Each entry is a dict with keys:
          - "name": method or property name.
          - "returns": return-type hint string ("bool", "int", "str", "Enum").
          - "args": list of argument-type hints (empty list = nullary).

        The framework filters for scalar-returning, effectively-nullary
        methods whose call is deterministic on a single parsed record.
        Default returns []: runner advertises no introspectable API.
        """
        return []

    def run_query_methods(
        self,
        input_path: Path,
        format_type: str,
        method_names: list[str],
        timeout_s: float = 30.0,
    ) -> "RunnerResult":
        """Parse `input_path`, invoke each named query method on the
        first parsed record, return a RunnerResult whose
        `canonical_json["method_results"]` maps method name → scalar.

        The oracle (`query_consensus.py`) compares `method_results` maps
        across x and T(x). Runners without introspection raise
        NotImplementedError; the dispatch layer treats this as no-op.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not implement run_query_methods"
        )
