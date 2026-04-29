#!/usr/bin/env python3
"""
BioTest Grand Orchestrator
==========================

Unified CLI that drives the entire metamorphic testing pipeline:

    Phase A  →  Spec Ingestion & RAG Index
    Phase B  →  Agentic MR Mining & DSL Compilation
    Phase C  →  Cross-Execution & Differential Testing

Usage:
    py -3.12 biotest.py                          # Full pipeline
    py -3.12 biotest.py --phase C                # Phase C only
    py -3.12 biotest.py --config custom.yaml     # Custom config
    py -3.12 biotest.py --dry-run                # Validate config only
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

# ---------------------------------------------------------------------------
# Force UTF-8 stdout on Windows so the final summary (and any logged MR /
# spec text containing unicode like ≥, →, or Chinese comments from the
# LLM) doesn't crash the process with UnicodeEncodeError under cp1252.
# Must run BEFORE the rich Console is constructed — rich caches the
# encoding of the underlying file at init time.
# ---------------------------------------------------------------------------
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Rich console setup
# ---------------------------------------------------------------------------

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich import box

console = Console()
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Project root (this file lives at BioTest/)
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent


# ===========================================================================
# Configuration loader
# ===========================================================================

def load_config(path: Path) -> dict[str, Any]:
    """Load and validate the YAML configuration file."""
    if not path.exists():
        console.print(f"[red bold]Config not found:[/] {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if not isinstance(cfg, dict):
        console.print("[red bold]Invalid config: root must be a YAML mapping")
        sys.exit(1)

    return cfg


# ---------------------------------------------------------------------------
# Runtime-capability resolver
# ---------------------------------------------------------------------------
#
# Reads class-level attributes on the registered runner classes to derive
# which `transforms_menu.KNOWN_RUNTIME_PRECONDITIONS` tags the current
# environment satisfies. The result is handed to Phase B's mining prompt
# so the LLM never sees transforms whose runtime preconditions aren't
# met (otherwise the transform would silently no-op and waste an MR slot
# — see sut_write_roundtrip for the motivating case).
#
# This is READ-ONLY inspection of runner class attributes — no runner
# instances are constructed, no subprocesses spawned. Fast and safe to
# call at Phase B time.

def _resolve_primary_coverage_report(
    cfg: dict[str, Any],
    primary_target: str,
    format_context: str | None,
) -> tuple[Path | None, list[str] | None]:
    """Resolve the raw coverage-report path + filter rules for the primary SUT.

    Purpose (Tier 2a of the plateau plan): give the blindspot builder a
    format-agnostic pointer to whichever report this SUT produced this
    iteration, plus the SAME filter rules the feedback loop uses so the
    per-class gap block aligns with the weighted-VCF (or -SAM) score.

    Returns ``(None, None)`` when the primary SUT has no live report or
    when the report format isn't yet plumbed — callers treat that as
    "skip the class-gap block". No assumption is made that primary_target
    is any particular SUT; dispatch is keyed on the name we see in config.
    """
    if not primary_target:
        return None, None
    cov = cfg.get("coverage", {}) or {}
    target_filters = cov.get("target_filters", {}) or {}
    fmt = (format_context or "").upper()
    # target_filters is nested <FORMAT>:<sut>:[rules…]; pick the rules
    # for the primary SUT under the current format if present.
    filter_rules: list[str] | None = None
    per_fmt = target_filters.get(fmt) or target_filters.get(fmt.lower())
    if isinstance(per_fmt, dict):
        rules = per_fmt.get(primary_target)
        if isinstance(rules, list) and rules:
            filter_rules = rules

    # Dispatch by SUT language / collector family. No per-SUT hardcoded
    # class names — just the report location each collector already
    # writes to.
    if primary_target == "htsjdk":
        jdir = cov.get("jacoco_report_dir")
        if jdir:
            xml = PROJECT_ROOT / jdir / "jacoco.xml"
            return (xml if xml.exists() else None), filter_rules
    elif primary_target in {"biopython", "pysam", "vcfpy"}:
        # coverage.py writes a binary SQLite .coverage file; convert it
        # on the fly to JSON so the blindspot builder can read a
        # standard shape. Fail-soft: if the coverage CLI isn't
        # available, return (None, None).
        import shutil
        import subprocess
        if primary_target == "biopython":
            data = cov.get("coveragepy_data_file")
        elif primary_target == "vcfpy":
            data = cov.get("coveragepy_data_file")
        else:  # pysam
            data = cov.get("pysam_coverage_combined_file") or cov.get("pysam_coverage_dir")
        if not data:
            return None, filter_rules
        data_path = PROJECT_ROOT / data
        if not data_path.exists():
            return None, filter_rules
        json_out = data_path.parent / f"{data_path.stem}_classgaps.json"
        # Only regenerate the JSON if the .coverage file is newer.
        try:
            if (
                not json_out.exists()
                or json_out.stat().st_mtime < data_path.stat().st_mtime
            ):
                cov_cli = shutil.which("coverage") or shutil.which("python")
                if cov_cli:
                    subprocess.run(
                        ["coverage", "json", "--data-file", str(data_path),
                         "-o", str(json_out)],
                        check=False, capture_output=True, timeout=30,
                    )
        except Exception as e:
            logger.debug("coverage.py JSON export failed: %s", e)
            return None, filter_rules
        return (json_out if json_out.exists() else None), filter_rules
    elif primary_target == "seqan3":
        gpath = cov.get("gcovr_report_path")
        if gpath:
            gj = PROJECT_ROOT / gpath
            return (gj if gj.exists() else None), filter_rules
    elif primary_target == "noodles":
        npath = cov.get("noodles_report_path")
        if npath:
            nj = PROJECT_ROOT / npath
            return (nj if nj.exists() else None), filter_rules
    # Any other SUT — return empty (block will be skipped in the prompt).
    return None, filter_rules


def _compute_runtime_capabilities(
    primary_target: str,
    available_suts: list[str],
) -> set[str]:
    """Return the set of runtime capability tags currently satisfied.

    Tags map 1:1 with `transforms_menu.KNOWN_RUNTIME_PRECONDITIONS`:
      - `primary_sut_has_writer`        — primary runner class sets
                                          `supports_write_roundtrip = True`.
      - `primary_sut_has_query_methods` — primary runner class sets
                                          `supports_query_methods = True`.
      - `pysam_runtime_reachable`       — pysam SUT is enabled.
      - `htsjdk_runtime_reachable`      — htsjdk SUT is enabled.
      - `bcf_codec_available`           — either pysam or htsjdk is enabled.
    """
    caps: set[str] = set()

    # Import runner classes lazily (they pull in subprocess/Docker
    # modules — keep the biotest.py top-level light).
    from test_engine.runners.htsjdk_runner import HTSJDKRunner
    from test_engine.runners.pysam_runner import PysamRunner
    from test_engine.runners.biopython_runner import BiopythonRunner
    from test_engine.runners.seqan3_runner import SeqAn3Runner
    from test_engine.runners.htslib_runner import HTSlibRunner
    from test_engine.runners.vcfpy_runner import VcfpyRunner
    from test_engine.runners.noodles_runner import NoodlesRunner
    from test_engine.runners.reference_runner import ReferenceRunner

    _SUT_CLASSES = {
        "htsjdk": HTSJDKRunner,
        "pysam": PysamRunner,
        "biopython": BiopythonRunner,
        "seqan3": SeqAn3Runner,
        "htslib": HTSlibRunner,
        "vcfpy": VcfpyRunner,
        "noodles": NoodlesRunner,
        "reference": ReferenceRunner,
    }

    enabled = set(available_suts or [])

    # Reachability tags per enabled SUT. Conservative: we tag it as
    # "reachable" if it's enabled in config — the runner's own
    # is_available() will catch missing binaries at Phase C time.
    if "pysam" in enabled:
        caps.add("pysam_runtime_reachable")
    if "htsjdk" in enabled:
        caps.add("htsjdk_runtime_reachable")

    # BCF codec is provided by pysam (via libhts). htsjdk's BCF support
    # is in a separate package we don't currently invoke for our BCF
    # round-trip transform, so we key this strictly off pysam.
    if "pysam" in enabled:
        caps.add("bcf_codec_available")

    # Primary SUT writer: inspect the CLASS attribute, not an instance,
    # so no harness process starts here.
    primary_cls = _SUT_CLASSES.get(primary_target)
    if primary_cls and getattr(primary_cls, "supports_write_roundtrip", False):
        caps.add("primary_sut_has_writer")
    # Rank-5 query-methods MRs are only viable when the primary SUT's
    # runner exposes the discovery + invocation hooks. Without this tag
    # the transforms_menu filter hides `query_method_roundtrip` from the
    # LLM prompt — see transforms_menu.KNOWN_RUNTIME_PRECONDITIONS.
    if primary_cls and getattr(primary_cls, "supports_query_methods", False):
        caps.add("primary_sut_has_query_methods")

    # Phase 3 of SAM coverage plan — SAM<->BAM<->CRAM round-trip gates.
    # `samtools` on PATH (or the htslib SUT's configured samtools_path)
    # is what the round-trip transforms shell out to.
    import shutil as _shutil
    if _shutil.which("samtools"):
        caps.add("samtools_available")
    # Toy CRAM reference is committed; fatter setups can override by
    # pointing `cram_reference` elsewhere. A missing reference file or
    # unreadable .fa disables the CRAM lever cleanly.
    from pathlib import Path as _Path
    _toy_ref = _Path(__file__).resolve().parent / "seeds" / "ref" / "toy.fa"
    if _toy_ref.exists():
        caps.add("cram_reference_available")

    return caps


# ===========================================================================
# Phase result containers
# ===========================================================================

@dataclass
class PhaseAResult:
    success: bool = False
    chunk_count: int = 0
    vcf_chunks: int = 0
    sam_chunks: int = 0
    duration_s: float = 0.0
    error: Optional[str] = None


@dataclass
class PhaseBResult:
    success: bool = False
    themes_tested: list[str] = field(default_factory=list)
    total_mined: int = 0
    enforced: int = 0
    quarantine: int = 0
    duration_s: float = 0.0
    error: Optional[str] = None


@dataclass
class PhaseCResult:
    success: bool = False
    total_tests: int = 0
    metamorphic_failures: int = 0
    differential_failures: int = 0
    crashes: int = 0
    det_rate: float = 0.0
    seeds_used: int = 0
    variants_generated: int = 0
    bugs_found: int = 0
    runners_used: list[str] = field(default_factory=list)
    duration_s: float = 0.0
    error: Optional[str] = None
    det_tracker: Any = None  # DETTracker from Phase C, used by Phase D quarantine


@dataclass
class PhaseDResult:
    success: bool = False
    iterations_completed: int = 0
    final_scc_percent: float = 0.0
    total_mrs_enforced: int = 0
    total_mrs_quarantined: int = 0
    total_demoted: int = 0
    termination_reason: str = ""
    scc_history: list[float] = field(default_factory=list)
    # Code coverage tracking — primary-SUT, format-scoped. Each list
    # entry is the primary target's line-coverage percentage at the end
    # of that iteration. `final_coverage_pct` / `final_coverage_covered`
    # / `final_coverage_total` hold the last snapshot, used by the
    # Executive Summary.
    coverage_history: list[float] = field(default_factory=list)
    final_coverage_pct: float = 0.0
    final_coverage_covered: int = 0
    final_coverage_total: int = 0
    coverage_target: str = ""  # primary SUT name (e.g. "htsjdk")
    coverage_language: str = ""  # "Java" / "Python" / "C++"
    duration_s: float = 0.0
    error: Optional[str] = None


# ===========================================================================
# Phase A: Spec Ingestion
# ===========================================================================

def run_phase_a(cfg: dict[str, Any]) -> PhaseAResult:
    """Execute Phase A: fetch specs, parse, chunk, and index into ChromaDB."""
    phase_cfg = cfg.get("phase_a", {})
    if not phase_cfg.get("enabled", True):
        return PhaseAResult(success=True)

    t0 = time.monotonic()
    try:
        from spec_ingestor.main import step_ingest, step_parse, step_index

        # Step 1: Ingest from GitHub
        console.print("  [dim]Fetching specs from GitHub...[/]")
        sha, files = step_ingest()

        # Step 2: Parse LaTeX → chunks
        console.print("  [dim]Parsing LaTeX and chunking...[/]")
        chunks = step_parse(sha, files)

        # Count by format
        vcf_count = sum(1 for c in chunks if c.format == "VCF")
        sam_count = sum(1 for c in chunks if c.format == "SAM")

        # Step 3: Index into ChromaDB
        console.print("  [dim]Indexing into ChromaDB...[/]")
        spec_index = step_index(chunks)
        stats = spec_index.collection_stats()

        return PhaseAResult(
            success=True,
            chunk_count=stats.get("document_count", len(chunks)),
            vcf_chunks=vcf_count,
            sam_chunks=sam_count,
            duration_s=time.monotonic() - t0,
        )
    except Exception as e:
        return PhaseAResult(
            success=False,
            error=str(e),
            duration_s=time.monotonic() - t0,
        )


# ===========================================================================
# Phase B: MR Mining
# ===========================================================================

def run_phase_b(
    cfg: dict[str, Any],
    blindspot_context: str | None = None,
    merge_mode: bool = False,
) -> PhaseBResult:
    """Execute Phase B: mine MRs using the agentic RAG engine.

    Args:
        cfg: Full config dict.
        blindspot_context: Optional Phase D blindspot guidance appended to system prompt.
        merge_mode: If True, APPEND newly mined MRs to existing registry (dedup by mr_id).
                    If False (default), OVERWRITE registry with new MRs only.
    """
    phase_cfg = cfg.get("phase_b", {})
    if not phase_cfg.get("enabled", True):
        return PhaseBResult(success=True)

    t0 = time.monotonic()
    try:
        from mr_engine.behavior import BehaviorTarget, get_all_targets
        from mr_engine.agent.engine import mine_mrs
        from mr_engine.registry import triage, export_registry, merge_registries

        # Single-source-of-truth format: `phase_c.format_filter` is the
        # ONE knob (see biotest_config.yaml). If the user explicitly
        # overrides `phase_b.formats`, honor that; otherwise derive.
        phase_c_filter = (cfg.get("phase_c", {}).get("format_filter") or "").upper()
        phase_b_formats_override = phase_cfg.get("formats")

        if phase_b_formats_override:
            # Explicit override — use as-is, then apply the filter guard.
            formats = list(phase_b_formats_override)
        elif phase_c_filter:
            # Derive from the Phase C filter (the usual path).
            formats = [phase_c_filter]
            console.print(
                f"  [dim]Phase B format derived from phase_c.format_filter=[bold]"
                f"{phase_c_filter}[/][/]"
            )
        else:
            # No filter anywhere → mine VCF by default (historical behavior).
            formats = ["VCF"]

        theme_names = phase_cfg.get("themes", [])
        registry_path = phase_cfg.get("registry_path", "data/mr_registry.json")

        # Even when `formats` was set explicitly, the Phase C filter still
        # clamps it. This is the wasted-LLM-calls guard: you can't mine
        # SAM MRs that will never be tested in a VCF-only run.
        if phase_c_filter:
            dropped = [f for f in formats if f.upper() != phase_c_filter]
            formats = [f for f in formats if f.upper() == phase_c_filter]
            if dropped:
                console.print(
                    f"  [dim]Scoping Phase B to phase_c.format_filter=[bold]"
                    f"{phase_c_filter}[/] — dropping {dropped} from mining to "
                    f"avoid off-scope MRs.[/]"
                )
            if not formats:
                console.print(
                    f"  [red bold]Configuration error:[/] phase_c.format_filter="
                    f"{phase_c_filter} but phase_b.formats={phase_b_formats_override!r} "
                    f"has no overlap. Nothing to mine. Aborting Phase B."
                )
                return PhaseBResult(
                    success=False,
                    error=(
                        f"phase_c.format_filter={phase_c_filter} has no overlap "
                        f"with phase_b.formats={phase_b_formats_override!r}"
                    ),
                    duration_s=time.monotonic() - t0,
                )

        # Resolve themes to BehaviorTarget enums
        all_targets = get_all_targets()
        if theme_names:
            targets = [t for t in all_targets if t.value in theme_names]
        else:
            targets = all_targets

        themes_tested = [t.value for t in targets]
        all_relations = []
        theme_errors: list[str] = []

        # Primary target + available SUTs are surfaced to the mining
        # prompt so the LLM can align SUT-specific transforms (e.g.
        # sut_write_roundtrip) with the actual SUT this run is
        # measuring, and hide transforms whose runtime preconditions
        # aren't satisfied.
        primary_target_for_prompt = (
            cfg.get("feedback_control", {}).get("primary_target", "") or ""
        )
        available_suts_for_prompt = [
            s["name"]
            for s in cfg.get("phase_c", {}).get("suts", [])
            if s.get("enabled", True) and s.get("name")
        ]
        runtime_caps_for_prompt = _compute_runtime_capabilities(
            primary_target=primary_target_for_prompt,
            available_suts=available_suts_for_prompt,
        )
        if runtime_caps_for_prompt:
            console.print(
                f"  [dim]Runtime capabilities for Phase B menu: "
                f"{sorted(runtime_caps_for_prompt)}[/]"
            )

        # Rank 5 — discover the primary SUT's API surface ONCE per Phase B
        # run, pass to mine_mrs so the LLM can construct API_QUERY_INVARIANCE
        # MRs naming methods that actually exist on the live SUT. Reuses
        # `_build_runners` and picks out the primary one — no duplication
        # of the factory map.
        # Per Chen-Kuo-Liu-Tse 2018 §3.2 + MR-Scout (TOSEM 2024).
        primary_query_methods_by_fmt: dict[str, list[dict]] = {}
        if primary_target_for_prompt:
            try:
                discovery_runners = _build_runners(cfg)
                primary_runner = next(
                    (r for r in discovery_runners
                     if getattr(r, "name", None) == primary_target_for_prompt),
                    None,
                )
                if primary_runner is not None and getattr(
                    primary_runner, "supports_query_methods", False,
                ):
                    for f in formats:
                        primary_query_methods_by_fmt[f] = (
                            primary_runner.discover_query_methods(f)
                        )
                    n_total = sum(
                        len(v) for v in primary_query_methods_by_fmt.values()
                    )
                    if n_total:
                        console.print(
                            f"  [dim]Discovered {n_total} query methods on "
                            f"primary {primary_target_for_prompt} for Rank 5[/]"
                        )
            except Exception as e:
                logger.warning(
                    "Query-method discovery failed (Rank 5 disabled): %s", e,
                )

        for fmt in formats:
            for target in targets:
                console.print(f"  [dim]Mining {fmt} / {target.value}...[/]")
                result = mine_mrs(
                    target, fmt,
                    blindspot_context=blindspot_context,
                    primary_target=primary_target_for_prompt,
                    available_suts=available_suts_for_prompt,
                    runtime_capabilities=runtime_caps_for_prompt,
                    query_methods=primary_query_methods_by_fmt.get(fmt),
                )
                if result.success and result.relations:
                    all_relations.extend(result.relations)
                    console.print(
                        f"    [green]OK[/] mined {len(result.relations)} MR(s) "
                        f"for {fmt}/{target.value}"
                    )
                else:
                    # Surface the reason instead of silently skipping.
                    detail = (result.error_detail or "no relations returned")
                    console.print(
                        f"    [yellow]0 MRs[/] for {fmt}/{target.value}: "
                        f"{detail[:120]}"
                    )
                    # An explicit LLM error (rate limit / billing / API)
                    # counts as a theme failure; "success=True but 0
                    # relations" is legitimate (LLM said "no MRs apply").
                    if not result.success:
                        theme_errors.append(f"{fmt}/{target.value}: {detail[:80]}")

        # Triage
        registry = triage(all_relations)
        out_path = str(PROJECT_ROOT / registry_path)
        if merge_mode:
            # Phase D iteration: append new MRs to existing registry
            merge_registries(out_path, registry)
        else:
            # Fresh start: overwrite registry with current batch only
            export_registry(registry, out_path)

        # Phase B FAILS when EVERY theme errored AND no prior MRs exist.
        # Mining 0 MRs is fine if we merged into a non-empty registry
        # (Phase D iteration) or if the LLM genuinely found nothing for
        # this theme. But "every theme blew up with an API error" is NOT
        # a pass — it's the primary symptom of the "fake run" concern.
        total_themes = max(len(formats) * len(targets), 1)
        all_themes_errored = len(theme_errors) == total_themes
        enforced_in_registry = len(registry.enforced)
        # If we merged into an existing registry, check its combined size.
        if merge_mode:
            try:
                import json as _j
                existing = _j.loads(Path(out_path).read_text(encoding="utf-8"))
                enforced_in_registry = len(existing.get("enforced", []))
            except Exception:
                pass
        phase_b_real_pass = (
            (not all_themes_errored) or enforced_in_registry > 0
        )

        return PhaseBResult(
            success=phase_b_real_pass,
            themes_tested=themes_tested,
            total_mined=len(all_relations),
            enforced=len(registry.enforced),
            quarantine=len(registry.quarantine),
            duration_s=time.monotonic() - t0,
            error=(
                None if phase_b_real_pass
                else f"All {total_themes} themes errored: "
                     + "; ".join(theme_errors[:3])
            ),
        )
    except Exception as e:
        return PhaseBResult(
            success=False,
            error=str(e),
            duration_s=time.monotonic() - t0,
        )


# ===========================================================================
# Phase C: Cross-Execution
# ===========================================================================

def _build_runners(cfg: dict[str, Any]) -> list:
    """Build runner instances from YAML SUT configuration.

    Only real SUTs are listed in the config (htsjdk, biopython, seqan3).
    The reference runner is always appended automatically as a baseline —
    it is framework infrastructure, not a System Under Test.
    """
    from test_engine.runners.htsjdk_runner import HTSJDKRunner
    from test_engine.runners.biopython_runner import BiopythonRunner
    from test_engine.runners.seqan3_runner import SeqAn3Runner
    from test_engine.runners.pysam_runner import PysamRunner
    from test_engine.runners.htslib_runner import HTSlibRunner
    from test_engine.runners.vcfpy_runner import VcfpyRunner
    from test_engine.runners.noodles_runner import NoodlesRunner
    from test_engine.runners.reference_runner import ReferenceRunner

    sut_cfgs = cfg.get("phase_c", {}).get("suts", [])
    runner_map = {
        "htsjdk": lambda c: HTSJDKRunner(
            jar_path=Path(c["adapter"]) if c.get("adapter") else None,
            java_cmd=c.get("java_cmd", "java"),
            coverage_jvm_args=c.get("coverage_jvm_args"),
            coverage_exec_dir=Path(c["coverage_exec_dir"]) if c.get("coverage_exec_dir") else None,
        ),
        "biopython": lambda c: BiopythonRunner(),
        "seqan3": lambda c: SeqAn3Runner(
            binary_path=Path(c["adapter"]) if c.get("adapter") else None,
            coverage_binary_path=Path(c["coverage_binary"]) if c.get("coverage_binary") else None,
        ),
        "pysam": lambda c: PysamRunner(
            coverage_dir=Path(c["coverage_dir"]) if c.get("coverage_dir") else None,
        ),
        # vcfpy (bihealth) — pure-Python VCF parser, in-process.
        "vcfpy": lambda c: VcfpyRunner(),
        # noodles-vcf — pure-Rust VCF parser via compiled subprocess harness.
        "noodles": lambda c: NoodlesRunner(
            binary_path=Path(c["adapter"]) if c.get("adapter") else None,
            coverage_binary_path=Path(c["coverage_binary"]) if c.get("coverage_binary") else None,
            llvm_profile_dir=Path(c["llvm_profile_dir"]) if c.get("llvm_profile_dir") else None,
        ),
        # htslib is the CLI gold standard (samtools + bcftools). Acts as
        # the tie-breaker voter in the consensus oracle — see
        # test_engine/oracles/consensus.py.
        "htslib": lambda c: HTSlibRunner(
            bcftools_path=c.get("bcftools_path"),
            samtools_path=c.get("samtools_path"),
        ),
    }

    runners = []
    for sut in sut_cfgs:
        name = sut.get("name", "")
        if not sut.get("enabled", True):
            continue
        factory = runner_map.get(name)
        if factory:
            runners.append(factory(sut))

    # Auto-enable htslib when the binaries are on PATH and no explicit
    # entry appears in the config. The CLI is strictly additive — it
    # only activates the tie-breaker branch in consensus.py, nothing
    # else changes when it's absent.
    if not any(getattr(r, "name", "") == "htslib" for r in runners):
        auto = HTSlibRunner()
        if auto.is_available():
            runners.append(auto)

    # Always add the reference runner as baseline (not a SUT, not a voter)
    runners.append(ReferenceRunner())

    return runners


def run_phase_c(cfg: dict[str, Any]) -> PhaseCResult:
    """Execute Phase C: cross-execution and differential testing."""
    phase_cfg = cfg.get("phase_c", {})
    if not phase_cfg.get("enabled", True):
        return PhaseCResult(success=True)

    t0 = time.monotonic()
    try:
        from test_engine.orchestrator import run_test_suite
        from test_engine.generators.seeds import SeedCorpus

        runners = _build_runners(cfg)
        available = [r for r in runners if r.is_available()]

        if not available:
            return PhaseCResult(
                success=False,
                error="No parser runners available",
                duration_s=time.monotonic() - t0,
            )

        registry_path = PROJECT_ROOT / cfg.get("phase_b", {}).get(
            "registry_path", "data/mr_registry.json"
        )
        seeds_dir = PROJECT_ROOT / phase_cfg.get("seeds_dir", "seeds")
        output_dir = PROJECT_ROOT / phase_cfg.get("output_dir", "bug_reports")
        format_filter = phase_cfg.get("format_filter")
        det_report = PROJECT_ROOT / phase_cfg.get("det_report_path", "data/det_report.json")

        # Count seeds
        corpus = SeedCorpus(seeds_dir)
        vcf_seeds = len(corpus.vcf_seeds)
        sam_seeds = len(corpus.sam_seeds)
        total_seeds = vcf_seeds + sam_seeds

        primary_target_c = cfg.get("phase_d", {}).get("primary_target", "") or ""
        # Phase D primary_target is still under feedback_control in the YAML.
        if not primary_target_c:
            primary_target_c = cfg.get("feedback_control", {}).get("primary_target", "") or ""

        # Fix #2 (Run 9 lesson): optional consensus quorum loosening.
        # Default 0.501 preserves strict-majority semantics. For high-
        # disagreement domains (e.g. SAM with 6 voters) the user can
        # drop to ~0.34 to accept plurality-of-three. Uniqueness of the
        # top bucket is still enforced inside get_consensus_output, so
        # no weaker-than-plurality results ever count.
        # Format-aware consensus defaults (Run-9 lessons):
        #   - SAM: loose by default (0.34 plurality, field-level tol).
        #     Spec-allowed variance is high (RNEXT="=", optional-tag
        #     ordering, float precision); strict consensus floods
        #     quarantine with false positives.
        #   - VCF: strict by default (0.501 majority, no tolerance).
        #     Run-6 baseline 46.9% was measured under strict and must
        #     stay reproducible.
        # Users who want to override either way set the explicit key in
        # `biotest_config.yaml: feedback_control`.
        _fmt_u = (format_filter or "").upper()
        _quorum_default = 0.34 if _fmt_u == "SAM" else 0.501
        # Default field_tolerance=True for BOTH SAM and VCF. The audit
        # in coverage_notes/phase4/oracle_and_detection_audit.md showed
        # the full-record bucket path left VCF voters disagreeing on
        # 46/47 correct inputs; strict bucketing on variant-identity
        # fields (CHROM+POS+REF+ALT) combined with the post-normalizer
        # is what actually lets the consensus oracle find real bugs.
        _tolerance_default = _fmt_u in ("SAM", "VCF")
        quorum = float(
            cfg.get("feedback_control", {}).get(
                "consensus_quorum_fraction", _quorum_default,
            )
        )
        field_tolerance = bool(
            cfg.get("feedback_control", {}).get(
                "consensus_field_tolerance", _tolerance_default,
            )
        )
        # Rank 8 lever — coverage-growth corpus keeper (see
        # test_engine/feedback/corpus_keeper.py for rationale). Builds
        # an accumulating pool of successfully-parsed transformed
        # inputs under seeds/<fmt>/kept_<sha8>.{vcf,sam}, dedup'd by
        # content hash and FIFO-capped per format. The SeedCorpus glob
        # in subsequent iterations picks them up automatically — no
        # wiring changes beyond this construct call. Configure via
        # phase_c.corpus_keeper.{enabled, max_files_per_format}.
        from test_engine.feedback.corpus_keeper import from_config as _ck_from_cfg
        corpus_keeper = _ck_from_cfg(cfg, seeds_dir)

        result = run_test_suite(
            runners=available,
            registry_path=registry_path,
            seeds_dir=seeds_dir,
            output_dir=output_dir,
            format_filter=format_filter,
            primary_target=primary_target_c,
            consensus_quorum_fraction=quorum,
            consensus_field_tolerance=field_tolerance,
            corpus_keeper=corpus_keeper,
        )

        # Export DET report
        det_report.parent.mkdir(parents=True, exist_ok=True)
        result.det_tracker.export(str(det_report))

        # Phase C PASSES when we actually ran tests. An empty registry
        # (0 enforced MRs) means Phase C had NOTHING to execute — that
        # looks like a pass in the old code ("no failures") but it's
        # the "fake run" symptom: the upstream mining step failed and
        # we're silently rubber-stamping it.
        real_pass = result.total_tests > 0
        err = None if real_pass else (
            "Phase C executed 0 tests — registry has no enforced MRs to run. "
            "Phase B probably produced no output (check LLM errors)."
        )
        return PhaseCResult(
            success=real_pass,
            total_tests=result.total_tests,
            metamorphic_failures=result.metamorphic_failures,
            differential_failures=result.differential_failures,
            crashes=result.crashes,
            det_rate=result.det_tracker.det_rate,
            seeds_used=total_seeds,
            variants_generated=result.total_tests,  # Each test generates a variant
            bugs_found=len(result.bug_reports),
            runners_used=[r.name for r in available],
            duration_s=time.monotonic() - t0,
            det_tracker=result.det_tracker,
            error=err,
        )
    except Exception as e:
        return PhaseCResult(
            success=False,
            error=str(e),
            duration_s=time.monotonic() - t0,
        )


# ===========================================================================
# Phase D: Feedback-Driven Loop
# ===========================================================================

def run_phase_d(cfg: dict[str, Any]) -> PhaseDResult:
    """Execute Phase D: iterative feedback loop (B -> C -> coverage -> steer)."""
    feedback_cfg = cfg.get("feedback_control", {})
    if not feedback_cfg.get("enabled", False):
        return PhaseDResult(success=True, termination_reason="disabled")

    t0 = time.monotonic()
    try:
        import json as _json
        from test_engine.feedback.loop_controller import LoopController
        from test_engine.feedback.scc_tracker import SCCTracker
        from test_engine.feedback.coverage_collector import MultiCoverageCollector
        from test_engine.feedback.blindspot_builder import build_blindspot_ticket
        from test_engine.feedback.quarantine_manager import evaluate_quarantine, apply_quarantine
        from test_engine.feedback.rule_attempts import RuleAttemptTracker
        from mr_engine.registry import triage, merge_registries

        # Format-aware max_iterations (Run-11 lesson, 2026-04-21).
        # Without user override, SAM caps at 2 iters (Jazzer paradigm
        # ceiling reached in 2h budget; iters 3-4 re-run without new
        # coverage) and VCF stays at 4. An explicit max_iterations
        # key in biotest_config.yaml overrides either default.
        # `format_context` hasn't been resolved yet at this point in
        # the function, so read the format from the config directly.
        _fc_view = dict(feedback_cfg)
        _fmt_for_iter = (cfg.get("phase_c", {}).get("format_filter") or "").upper()
        if "max_iterations" not in feedback_cfg:
            _fc_view["max_iterations"] = 2 if _fmt_for_iter == "SAM" else 4
        controller = LoopController(_fc_view)
        scc_tracker = SCCTracker(PROJECT_ROOT / "data" / "parsed")
        coverage_collector = MultiCoverageCollector(cfg.get("coverage", {}))

        # Primary Target: this SUT drives the feedback loop.
        # Other SUTs are auxiliary differential oracles only.
        primary_target = feedback_cfg.get("primary_target", "")
        format_context = cfg.get("phase_c", {}).get("format_filter", "") or ""
        if primary_target:
            console.print(f"  [dim]Primary target:[/] [bold]{primary_target}[/] (drives evolution)")
        else:
            console.print("  [dim]No primary target set — all SUTs drive evolution equally[/]")
        if format_context:
            console.print(f"  [dim]Format context:[/] [bold]{format_context}[/] (feedback scoped to this format)")

        # Guard: primary_target must actually support the format being tested.
        # Otherwise coverage collection for primary would record no data,
        # SCC would be 0 forever, and quarantine decisions meaningless.
        # This matters because biopython and seqan3 are SAM-only.
        _SUT_FORMATS = {
            "htsjdk": {"VCF", "SAM"},
            "pysam": {"VCF", "SAM"},
            "biopython": {"SAM"},
            "seqan3": {"SAM"},
            "reference": {"VCF", "SAM"},
        }
        if primary_target and format_context:
            supported = _SUT_FORMATS.get(primary_target, set())
            if supported and format_context.upper() not in supported:
                console.print(
                    f"  [red bold]Configuration error:[/] "
                    f"primary_target=[bold]{primary_target}[/] does not support "
                    f"format=[bold]{format_context}[/] (supports: "
                    f"{sorted(supported) or 'unknown'}). "
                    f"Feedback signal would be garbage. Aborting Phase D."
                )
                return PhaseDResult(
                    success=False,
                    error=(
                        f"primary_target={primary_target} does not support "
                        f"format={format_context} (supports {sorted(supported)})"
                    ),
                    duration_s=0.0,
                )

        registry_path = PROJECT_ROOT / cfg.get("phase_b", {}).get(
            "registry_path", "data/mr_registry.json"
        )
        # Allow per-cell isolation in parallel sweeps via cfg overrides.
        # Defaults keep historical behaviour (PROJECT_ROOT/data/...).
        state_path = Path(cfg.get("feedback_control", {}).get(
            "state_path", PROJECT_ROOT / "data" / "feedback_state.json"
        ))
        attempts_path = Path(cfg.get("feedback_control", {}).get(
            "attempts_path", PROJECT_ROOT / "data" / "rule_attempts.json"
        ))
        state_path.parent.mkdir(parents=True, exist_ok=True)
        attempts_path.parent.mkdir(parents=True, exist_ok=True)

        # Resume from crash if state file exists
        if state_path.exists():
            controller.load_state(state_path)
            logger.info("Resumed Phase D from iteration %d", controller.state.iteration)

        # Per-rule failure/cooldown tracker. Persists across Phase D runs
        # so an unrecoverable session picks up where it left off.
        attempt_tracker = RuleAttemptTracker.load(attempts_path)
        if attempt_tracker.records:
            logger.info(
                "Loaded rule_attempts: %d rules tracked, %d currently cooling",
                len(attempt_tracker.records),
                len(attempt_tracker.currently_cooled_ids(controller.state.iteration)),
            )

        # Track SCC covered-ids across iterations so we can tell the
        # attempt tracker which rules just became covered.
        prev_covered_rules: set[str] = set()
        blindspot_text: str | None = None
        total_demoted = 0

        # Per-iteration primary-SUT code coverage history. Used by the
        # Executive Summary to show progression (e.g. 25% -> 28% -> 31%).
        coverage_history: list[float] = []
        final_cov_pct = 0.0
        final_cov_covered = 0
        final_cov_total = 0
        final_cov_language = ""

        for iteration in range(controller.state.iteration, controller.max_iterations):
            # Check termination before each iteration
            term = controller.check_termination()
            if term.should_stop:
                console.print(f"  [yellow]Stopping:[/] {term.reason}")
                break

            console.print(f"\n  [bold cyan]--- Iteration {iteration + 1} ---[/]")

            # Rank 1 lever — LLM-driven seed synthesis, runs BEFORE Phase B
            # so any synthesized seeds are on disk when SeedCorpus re-loads
            # at Phase C time. Conceptually parallel to MR mining (both
            # consume the same blindspot ticket), implemented sequentially
            # to avoid ChromaDB concurrency + filesystem-race complexity.
            # Fail-soft: any failure here is logged and skipped, never
            # aborts the iteration.
            synth_cfg = feedback_cfg.get("seed_synthesis", {}) or {}
            if synth_cfg.get("enabled", False) and blindspot_text:
                try:
                    from mr_engine.agent.seed_synthesizer import synthesize_seeds
                    phase_c_cfg = cfg.get("phase_c", {}) or {}
                    seeds_dir = PROJECT_ROOT / phase_c_cfg.get("seeds_dir", "seeds")
                    synth_fmt = (format_context or "VCF").upper()
                    console.print(
                        f"  [dim]Synthesizing seeds ({synth_fmt}, Phase D Rank 1)...[/]"
                    )
                    new_seeds = synthesize_seeds(
                        blindspot_context=blindspot_text,
                        fmt=synth_fmt,
                        primary_target=primary_target or "",
                        n_seeds=int(synth_cfg.get("max_seeds_per_iteration", 5)),
                        out_dir=seeds_dir,
                        iteration=iteration + 1,
                        max_bytes=int(synth_cfg.get("max_file_bytes", 500 * 1024)),
                    )
                    if new_seeds:
                        console.print(
                            f"    [green]Synth:[/] {len(new_seeds)} new seeds landed"
                        )

                    # Phase 5 of SAM coverage plan — SeedMind-style
                    # generator-mode synthesis, off-by-default. One LLM
                    # call produces a Python generator; we invoke it K
                    # times for K distinct outputs. Runs alongside the
                    # raw-file synthesis above so both strategies
                    # contribute to the corpus in the same iteration.
                    gen_enabled = bool(synth_cfg.get("generator_mode", False))
                    if gen_enabled:
                        from mr_engine.agent.seed_synthesizer import (
                            synthesize_seeds_via_generator,
                        )
                        console.print(
                            f"  [dim]Synthesizing via generator ({synth_fmt}, "
                            f"Phase D Rank 1b SeedMind)...[/]"
                        )
                        gen_seeds = synthesize_seeds_via_generator(
                            blindspot_context=blindspot_text,
                            fmt=synth_fmt,
                            primary_target=primary_target or "",
                            n_seeds=int(synth_cfg.get("max_seeds_per_iteration", 5)),
                            out_dir=seeds_dir,
                            iteration=iteration + 1,
                            max_bytes=int(synth_cfg.get("max_file_bytes", 500 * 1024)),
                            sandbox_timeout_s=float(
                                synth_cfg.get("generator_timeout_s", 5.0)
                            ),
                        )
                        if gen_seeds:
                            console.print(
                                f"    [green]Gen:[/] {len(gen_seeds)} generator outputs landed"
                            )
                except Exception as e:
                    logger.warning("Seed synthesis failed (non-fatal): %s", e)
                    console.print(f"    [yellow]Synth failed (non-fatal):[/] {e}")

            # Rank 6 lever — LLM-driven MR SYNTHESIS. Same blindspot ticket
            # as Rank 1, but the LLM emits new MRs (transform_steps + oracle
            # + evidence) rather than raw files. Validated through the same
            # compile_mr_output pipeline as Phase B, merged into the
            # registry before Phase B's ReAct mining so Phase C picks up
            # both. Disabled by default — flip feedback_control.mr_synthesis.
            # enabled to true once Rank 5 impact is baselined.
            # Per Fuzz4All (ICSE'24), PromptFuzz (CCS'24), ChatAFL (NDSS'24).
            mr_synth_cfg = feedback_cfg.get("mr_synthesis", {}) or {}
            if mr_synth_cfg.get("enabled", False) and blindspot_text:
                try:
                    from mr_engine.agent.mr_synthesizer import synthesize_mrs
                    from mr_engine.index_loader import get_ephemeral_index
                    from mr_engine.registry import triage, merge_registries
                    synth_fmt = (format_context or "VCF").upper()
                    # Rank 5 catalog for the primary SUT — gives the
                    # synthesizer usable method names so query_method_roundtrip
                    # MRs aren't rejected by the non-empty-query_methods
                    # validator.
                    rank5_query_methods: list[dict] = []
                    mutator_catalog: list[dict] = []
                    try:
                        rank5_runners = _build_runners(cfg)
                        rank5_primary = next(
                            (r for r in rank5_runners
                             if getattr(r, "name", None) == primary_target),
                            None,
                        )
                        if rank5_primary is not None and getattr(
                            rank5_primary, "supports_query_methods", False,
                        ):
                            rank5_query_methods = (
                                rank5_primary.discover_query_methods(synth_fmt)
                            )
                        # Tier 2b — mutator catalog (opt-in after Runs 7/8
                        # showed no measurable pp gain). Set
                        # feedback_control.prompt_enrichment.mutator_catalog: true
                        # per-run when you want the catalog surfaced to Rank 6.
                        _pe_cfg_r6 = feedback_cfg.get("prompt_enrichment", {}) or {}
                        if (
                            _pe_cfg_r6.get("mutator_catalog", False)
                            and rank5_primary is not None
                            and getattr(rank5_primary, "supports_mutator_methods", False)
                        ):
                            mutator_catalog = (
                                rank5_primary.discover_mutator_methods(synth_fmt)
                            )
                    except Exception as qe:
                        logger.info(
                            "Rank 6: method discovery skipped (%s)", qe,
                        )
                    console.print(
                        f"  [dim]Synthesizing MRs ({synth_fmt}, Phase D Rank 6)...[/]"
                    )
                    new_mrs = synthesize_mrs(
                        blindspot_context=blindspot_text,
                        fmt=synth_fmt,
                        spec_index=get_ephemeral_index(),
                        primary_target=primary_target or "",
                        n_mrs=int(mr_synth_cfg.get("max_mrs_per_iteration", 5)),
                        query_methods=rank5_query_methods or None,
                        mutator_catalog=mutator_catalog or None,
                    )
                    if new_mrs:
                        merged_registry = triage(new_mrs)
                        merge_registries(str(registry_path), merged_registry)
                        console.print(
                            f"    [green]Synth:[/] {len(new_mrs)} new MR(s) "
                            f"merged into registry"
                        )
                except Exception as e:
                    logger.warning("MR synthesis failed (non-fatal): %s", e)
                    console.print(f"    [yellow]MR synth failed (non-fatal):[/] {e}")

            # Phase B: Mine MRs with blindspot context.
            # merge_mode=True: accumulate MRs across iterations (dedup by mr_id).
            console.print("  [dim]Mining MRs (Phase B)...[/]")
            phase_b_result = run_phase_b(
                cfg,
                blindspot_context=blindspot_text,
                merge_mode=True,
            )
            icon = "[green]OK[/]" if phase_b_result.success else "[red]FAIL[/]"
            console.print(f"    B: {icon} ({phase_b_result.enforced} mined this round)")

            # Phase C: Execute tests (with Python coverage instrumentation)
            console.print("  [dim]Running tests (Phase C)...[/]")
            from test_engine.feedback.coverage_collector import PythonCoverageContext
            cov_cfg = cfg.get("coverage", {})
            py_cov_ctx = PythonCoverageContext(
                data_file=cov_cfg.get("coveragepy_data_file", ".coverage"),
                source_filter=cov_cfg.get("coveragepy_source_filter", []),
            ) if cov_cfg.get("enabled", False) else None

            if py_cov_ctx:
                with py_cov_ctx:
                    phase_c_result = run_phase_c(cfg)
            else:
                phase_c_result = run_phase_c(cfg)
            icon = "[green]OK[/]" if phase_c_result.success else "[red]FAIL[/]"
            console.print(
                f"    C: {icon} ({phase_c_result.total_tests} tests, "
                f"{phase_c_result.bugs_found} bugs)"
            )

            # Collect code coverage — primary SUT only (Flow.md Phase D §1.3)
            coverage_results = coverage_collector.collect_all(
                format_context=format_context,
                primary_target=primary_target or "",
            )

            # Primary-SUT coverage snapshot for THIS iteration. Pick the
            # matching collector (there should be exactly one when a
            # primary_target is set). Persist history + final values on
            # the PhaseDResult so the Executive Summary can render them.
            iter_cov_pct = 0.0
            iter_cov_covered = 0
            iter_cov_total = 0
            iter_cov_language = ""
            iter_cov_uncovered: list[str] = []
            for cov in coverage_results:
                if primary_target and cov.parser_name != primary_target:
                    continue
                if not cov.available:
                    continue
                iter_cov_pct = cov.line_coverage_pct
                iter_cov_covered = cov.covered_lines
                iter_cov_total = cov.total_lines
                iter_cov_language = cov.language
                iter_cov_uncovered = list(cov.uncovered_regions or [])
                break

            if coverage_results:
                cov_label = (
                    f"{primary_target}={iter_cov_pct:.1f}% "
                    f"({iter_cov_covered}/{iter_cov_total} lines)"
                    if iter_cov_total else "no primary-SUT data"
                )
                console.print(
                    f"    Coverage: {len(coverage_results)} SUT(s) collected -> {cov_label}"
                )

            # Capture primary-SUT coverage into Phase D's running history.
            coverage_history.append(iter_cov_pct)
            if iter_cov_total:
                final_cov_pct = iter_cov_pct
                final_cov_covered = iter_cov_covered
                final_cov_total = iter_cov_total
                final_cov_language = iter_cov_language or final_cov_language

            # Persist a per-iteration coverage snapshot. Overwritten each
            # iteration with the latest state so the JSON always reflects
            # the most recent numbers (plus the full history list).
            cov_report = {
                "primary_target": primary_target,
                "format_context": format_context,
                "iteration": iteration + 1,
                "final_coverage_pct": final_cov_pct,
                "final_coverage_covered": final_cov_covered,
                "final_coverage_total": final_cov_total,
                "final_coverage_language": final_cov_language,
                "coverage_history": coverage_history,
                "uncovered_regions_sample": iter_cov_uncovered[:20],
            }
            cov_report_path = Path(cfg.get("feedback_control", {}).get(
                "coverage_report_path",
                PROJECT_ROOT / "data" / "coverage_report.json",
            ))
            cov_report_path.parent.mkdir(parents=True, exist_ok=True)
            cov_report_path.write_text(
                _json.dumps(cov_report, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            # Compute SCC (target-centric: primary target failures demote rules,
            # UNLESS another parser endorsed the MR per cross-validation "良民证")
            registry_data = _json.loads(registry_path.read_text(encoding="utf-8"))
            primary_failed_mr_ids: set[str] = set()
            if primary_target and phase_c_result.det_tracker:
                # First pass: collect endorsements across ALL parsers.
                endorsed_mrs: set[str] = set()
                for event in phase_c_result.det_tracker.events:
                    if (event.test_type == "metamorphic"
                            and event.passed
                            and event.parser_names):
                        endorsed_mrs.add(event.mr_id)
                # Second pass: only count a primary failure as blind-spot
                # evidence when NO parser endorsed the MR.
                for event in phase_c_result.det_tracker.events:
                    if (not event.passed
                            and primary_target in event.parser_names
                            and event.test_type == "metamorphic"
                            and event.mr_id not in endorsed_mrs):
                        primary_failed_mr_ids.add(event.mr_id)
                if primary_failed_mr_ids:
                    console.print(
                        f"    [dim]{primary_target} failed {len(primary_failed_mr_ids)} MR(s) "
                        f"with no cross-parser endorsement — those rules stay as blind spots[/]"
                    )
                if endorsed_mrs:
                    console.print(
                        f"    [dim]{len(endorsed_mrs)} MR(s) endorsed by >=1 parser - "
                        f"kept in SCC via cross-validation rule[/]"
                    )

            scc_report = scc_tracker.compute_scc(
                registry_data.get("enforced", []),
                primary_failed_mr_ids=primary_failed_mr_ids,
                format_context=format_context,
            )
            scc_report_path = Path(cfg.get("feedback_control", {}).get(
                "scc_report_path",
                PROJECT_ROOT / "data" / "scc_report.json",
            ))
            scc_report_path.parent.mkdir(parents=True, exist_ok=True)
            scc_report.export(scc_report_path)

            # ── Record attempt outcomes against the cooldown tracker ──
            # Rules that just became covered get their failure history
            # wiped; rules that were shown but stayed uncovered get their
            # failure_count incremented and enter cooldown. This is what
            # prevents "dying on the hardest 5 rules forever" (惩罚/冷却).
            now_covered = set(scc_report.covered_rules)
            newly_covered = now_covered - prev_covered_rules
            outcomes = attempt_tracker.record_outcome(
                iteration=iteration + 1,
                newly_covered_chunk_ids=newly_covered,
            )
            prev_covered_rules = now_covered
            if outcomes:
                covered_now = sum(1 for o in outcomes.values() if o["outcome"].startswith("covered"))
                uncovered_now = sum(1 for o in outcomes.values() if o["outcome"] == "uncovered")
                if uncovered_now:
                    console.print(
                        f"    [dim]Cooldown: {uncovered_now} rule(s) stayed uncovered "
                        f"and entered backoff; {covered_now} cleared.[/]"
                    )
                logger.info("Rule attempt outcomes: %s", outcomes)
            attempt_tracker.save(attempts_path)

            scc_color = (
                "green" if scc_report.scc_percent >= 95
                else "yellow" if scc_report.scc_percent >= 50
                else "red"
            )
            console.print(
                f"    SCC: [{scc_color}]{scc_report.scc_percent:.1f}%[/] "
                f"({scc_report.covered_count}/{scc_report.total_rules} rules)"
            )

            # Layer 4: Auto-quarantine bad MRs
            from test_engine.orchestrator import run_test_suite
            # Use det_tracker from phase_c if available
            decisions = evaluate_quarantine(
                phase_c_result.det_tracker or _build_empty_tracker(),
                registry_data,
                primary_target=primary_target or "",
            )
            demoted = apply_quarantine(
                [d for d in decisions if d.demoted],
                registry_path,
            )
            total_demoted += demoted
            if demoted:
                console.print(f"    [yellow]Quarantined: {demoted} MR(s)[/]")

            # Record iteration. Passes the primary-SUT weighted line
            # coverage so the controller's Run-7-lesson coverage-plateau
            # early-stop can fire — prevents burning budget on flat
            # iterations while SCC is still inching up.
            controller.record_iteration(
                scc_percent=scc_report.scc_percent,
                enforced_count=len(registry_data.get("enforced", [])),
                demoted_count=demoted,
                coverage_percent=iter_cov_pct,
            )
            controller.save_state(state_path)

            # Layer 3: Build blindspot ticket for next iteration
            try:
                from mr_engine.index_loader import get_ephemeral_index
                spec_index = get_ephemeral_index()
            except Exception:
                spec_index = None

            # Resolve source roots for code slice extraction
            source_roots_cfg = feedback_cfg.get("source_roots", {})
            active_source_roots: list[Path] = []
            if primary_target and primary_target in source_roots_cfg:
                root = PROJECT_ROOT / source_roots_cfg[primary_target]
                if root.exists():
                    active_source_roots.append(root)
            else:
                # No primary target: collect all roots
                for name, rel in source_roots_cfg.items():
                    root = PROJECT_ROOT / rel
                    if root.exists():
                        active_source_roots.append(root)

            max_rules_per_iter = int(
                feedback_cfg.get("max_rules_per_iteration", 5)
            )

            # Phase 4 of SAM coverage plan — reachability filter.
            # Operator-editable section-to-capability mapping lives under
            # phase_a.rule_capability_tags; the runner class declares each
            # capability via `supports_<cap> = True`. Rules whose section
            # requires an unsupported capability get +20 priority penalty
            # so the LLM doesn't burn Top-K slots on unreachable rules.
            rule_cap_tags = (
                cfg.get("phase_a", {}).get("rule_capability_tags")
            )
            supported_caps: set[str] = set()
            if primary_target:
                # Recompute the class lookup locally — _compute_runtime_capabilities
                # encapsulates it but returns a different tag set. We only
                # need the per-runner capability flags here.
                from test_engine.runners.htsjdk_runner import HTSJDKRunner
                from test_engine.runners.pysam_runner import PysamRunner
                from test_engine.runners.biopython_runner import BiopythonRunner
                from test_engine.runners.seqan3_runner import SeqAn3Runner
                from test_engine.runners.htslib_runner import HTSlibRunner
                from test_engine.runners.reference_runner import ReferenceRunner
                _cls_by_name = {
                    "htsjdk": HTSJDKRunner, "pysam": PysamRunner,
                    "biopython": BiopythonRunner, "seqan3": SeqAn3Runner,
                    "htslib": HTSlibRunner, "reference": ReferenceRunner,
                }
                primary_cls = _cls_by_name.get(primary_target)
                if primary_cls and rule_cap_tags:
                    for cap in rule_cap_tags.keys():
                        if getattr(primary_cls, f"supports_{cap}", False):
                            supported_caps.add(cap)

            # Tier 2a — per-class blindspot. Opt-in after Runs 7/8 showed
            # the block added prompt tokens without measurable pp gain on
            # the current plateau. Set
            # feedback_control.prompt_enrichment.per_class_blindspot: true
            # per-run when you want the richer blindspot.
            _pe_cfg = feedback_cfg.get("prompt_enrichment", {}) or {}
            if _pe_cfg.get("per_class_blindspot", False):
                primary_cov_path, primary_cov_filter = _resolve_primary_coverage_report(
                    cfg, primary_target, format_context
                )
            else:
                primary_cov_path, primary_cov_filter = None, None

            ticket = build_blindspot_ticket(
                scc_report=scc_report,
                coverage_results=coverage_results,
                existing_mr_ids=[mr["mr_id"] for mr in registry_data.get("enforced", [])],
                spec_index=spec_index,
                iteration=iteration + 1,
                primary_target=primary_target,
                source_roots=active_source_roots,
                format_context=format_context or "",
                max_rules_per_iteration=max_rules_per_iter,
                attempt_tracker=attempt_tracker,
                rule_capability_tags=rule_cap_tags,
                supported_capabilities=supported_caps,
                primary_coverage_report_path=primary_cov_path,
                coverage_filter_rules_text=primary_cov_filter,
            )
            blindspot_text = ticket.to_prompt_fragment()
            attempt_tracker.save(attempts_path)
            if ticket.total_uncovered:
                console.print(
                    f"    [dim]Queue: Total Blindspots = {ticket.total_uncovered} | "
                    f"Injecting Top {ticket.shown_uncovered} into this ticket | "
                    f"{ticket.remaining_uncovered} rules remaining "
                    f"({ticket.cooling_count} cooling down).[/]"
                )

        # Final termination check
        final_term = controller.check_termination()
        reason = final_term.reason if final_term.should_stop else "all_iterations_complete"

        return PhaseDResult(
            success=True,
            iterations_completed=controller.state.iteration,
            final_scc_percent=controller.state.scc_history[-1] if controller.state.scc_history else 0.0,
            total_mrs_enforced=controller.state.enforced_history[-1] if controller.state.enforced_history else 0,
            total_mrs_quarantined=total_demoted,
            total_demoted=total_demoted,
            termination_reason=reason,
            scc_history=controller.state.scc_history,
            coverage_history=coverage_history,
            final_coverage_pct=final_cov_pct,
            final_coverage_covered=final_cov_covered,
            final_coverage_total=final_cov_total,
            coverage_target=primary_target or "",
            coverage_language=final_cov_language,
            duration_s=time.monotonic() - t0,
        )
    except Exception as e:
        import traceback
        logger.error("Phase D error: %s\n%s", e, traceback.format_exc())
        return PhaseDResult(
            success=False,
            error=str(e),
            duration_s=time.monotonic() - t0,
        )


def _build_empty_tracker():
    """Build an empty DETTracker for fallback."""
    from test_engine.oracles.det_tracker import DETTracker
    return DETTracker()


# ===========================================================================
# Phase E: Corpus Augmentation (Rank 12 structural + Rank 13 lenient byte
# fuzzer). Auto-runs after Phase D so the seed corpus that downstream
# Phase-3 mutation testing reads from contains the structural-variety
# and error-path-diversity inputs Run-6 / Run-7 measured to add ~5–20
# kills per cell. Outputs are spec-derived and SUT-agnostic.
# ===========================================================================

@dataclass
class PhaseEResult:
    success: bool = False
    sam_struct_kept: int = 0
    sam_rawfuzz_kept: int = 0
    vcf_struct_kept: int = 0
    vcf_rawfuzz_kept: int = 0
    duration_s: float = 0.0
    error: Optional[str] = None


def run_phase_e(cfg: dict[str, Any]) -> "PhaseEResult":
    """Apply Rank 12 (structural_diversifier) and Rank 13 (lenient byte
    fuzzer) over the Phase-D-completed seed corpus.

    Outputs:
      seeds/<fmt>_struct/   — Rank 12 structural variants
      seeds/<fmt>_rawfuzz/  — Rank 13 lenient byte-fuzz variants

    These are picked up automatically by phase3_jazzer_pit.sh,
    phase3_atheris_biopython.sh, and mutation_driver.py at the
    Phase-3 mutation-staging step (when TOOL=biotest*).

    Default-on. Disable via biotest_config.yaml:
        phase_e:
            enabled: false
    """
    from pathlib import Path as _Path
    t0 = time.monotonic()
    if not cfg.get("phase_e", {}).get("enabled", True):
        return PhaseEResult(success=True, duration_s=0.0)

    repo_root = _Path(__file__).resolve().parent
    seeds_root = repo_root / "seeds"
    result = PhaseEResult(success=True)

    # Per-format augmentation. Skip a format if its primary seed dir is
    # empty — Rank 12/13 need at least one source seed to read header
    # shape / build reasonable variants.
    formats: list[str] = []
    for fmt in ("VCF", "SAM"):
        ext = fmt.lower()
        seed_dir = seeds_root / ext
        if seed_dir.is_dir() and any(seed_dir.glob(f"*.{ext}")):
            formats.append(fmt)

    if not formats:
        logger.info("Phase E: no seed formats available — skipping")
        result.duration_s = time.monotonic() - t0
        return result

    cfg_pe = cfg.get("phase_e", {})
    struct_max_per_seed = int(cfg_pe.get("structural_max_per_seed", 200))
    rawfuzz_n_per_seed = int(cfg_pe.get("rawfuzz_n_per_seed", 10))
    rawfuzz_seed = int(cfg_pe.get("rawfuzz_seed", 42))

    for fmt in formats:
        ext = fmt.lower()
        in_dir = seeds_root / ext
        struct_dir = seeds_root / f"{ext}_struct"
        rawfuzz_dir = seeds_root / f"{ext}_rawfuzz"

        # Rank 12 — structural variant generator
        try:
            from mr_engine.transforms.structural_diversifier import (
                generate_structural_directory,
            )
            r = generate_structural_directory(
                input_dir=in_dir, output_dir=struct_dir, fmt=fmt,
                max_per_seed=struct_max_per_seed,
            )
            kept = int(r.get("kept", 0))
            if fmt == "SAM":
                result.sam_struct_kept = kept
            else:
                result.vcf_struct_kept = kept
            logger.info("Phase E: Rank 12 (%s structural) kept %d files in %s",
                        fmt, kept, struct_dir)
        except Exception as e:
            logger.warning("Phase E: Rank 12 (%s) failed — %s", fmt, e)
            result.success = False
            if not result.error:
                result.error = f"Rank12_{fmt}: {e}"

        # Rank 13 — lenient byte fuzzer
        try:
            from mr_engine.transforms.lenient_byte_fuzzer import fuzz_directory
            r = fuzz_directory(
                input_dir=in_dir, output_dir=rawfuzz_dir, fmt=fmt,
                n_per_seed=rawfuzz_n_per_seed, mutations_per_variant=4,
                seed=rawfuzz_seed,
            )
            kept = int(r.get("kept", 0))
            if fmt == "SAM":
                result.sam_rawfuzz_kept = kept
            else:
                result.vcf_rawfuzz_kept = kept
            logger.info("Phase E: Rank 13 (%s lenient byte fuzz) kept %d files in %s",
                        fmt, kept, rawfuzz_dir)
        except Exception as e:
            logger.warning("Phase E: Rank 13 (%s) failed — %s", fmt, e)
            result.success = False
            if not result.error:
                result.error = f"Rank13_{fmt}: {e}"

    result.duration_s = time.monotonic() - t0
    return result


# ===========================================================================
# Rich console output — Executive Summary
# ===========================================================================

def _status_icon(success: bool) -> str:
    return "[green]PASS[/]" if success else "[red]FAIL[/]"


def _fmt_duration(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.1f}s"
    m, s = divmod(seconds, 60)
    return f"{int(m)}m {s:.0f}s"


def print_banner():
    """Print the BioTest ASCII banner."""
    banner = Text.from_markup(
        "[bold cyan]"
        "  ____  _       _____         _   \n"
        " | __ )(_) ___ |_   _|__  ___| |_ \n"
        " |  _ \\| |/ _ \\  | |/ _ \\/ __| __|\n"
        " | |_) | | (_) | | |  __/\\__ \\ |_ \n"
        " |____/|_|\\___/  |_|\\___||___/\\__|\n"
        "[/]"
    )
    console.print(banner)
    console.print(
        "[dim]Metamorphic & Differential Testing for Bioinformatics Parsers[/]\n"
    )


def print_config_summary(cfg: dict[str, Any]):
    """Print a compact summary of the loaded configuration."""
    table = Table(
        title="Configuration", box=box.SIMPLE_HEAVY, title_style="bold white",
        show_header=False, pad_edge=False,
    )
    table.add_column("Key", style="cyan", width=20)
    table.add_column("Value", style="white")

    # Specs
    specs = cfg.get("phase_a", {}).get("specs", [])
    spec_str = ", ".join(f"{s['format']} v{s['version']}" for s in specs)
    table.add_row("Spec Versions", spec_str or "default")

    # Effective test format (single source of truth for this run).
    # Derived from phase_c.format_filter; highlighted so the operator can
    # verify at a glance exactly which format the run will exercise.
    fmt_filter = cfg.get("phase_c", {}).get("format_filter")
    if fmt_filter:
        table.add_row("Test Format", f"[bold green]{fmt_filter}[/] (cascades to B, C, D)")
    else:
        table.add_row("Test Format", "[yellow]ALL[/] (phase_c.format_filter=null)")

    # Themes
    themes = cfg.get("phase_b", {}).get("themes", ["all"])
    table.add_row("MR Themes", ", ".join(themes))

    # SUTs
    suts = cfg.get("phase_c", {}).get("suts", [])
    enabled_suts = [s["name"] for s in suts if s.get("enabled", True)]
    table.add_row("Active SUTs", ", ".join(enabled_suts) or "none")

    # Phases
    phases = []
    if cfg.get("phase_a", {}).get("enabled", True):
        phases.append("A")
    if cfg.get("phase_b", {}).get("enabled", True):
        phases.append("B")
    if cfg.get("phase_c", {}).get("enabled", True):
        phases.append("C")
    if cfg.get("feedback_control", {}).get("enabled", True):
        phases.append("D")
    table.add_row("Enabled Phases", " -> ".join(phases))

    console.print(table)
    console.print()


def print_executive_summary(
    cfg: dict[str, Any],
    phase_a: PhaseAResult,
    phase_b: PhaseBResult,
    phase_c: PhaseCResult,
    total_duration: float,
    phase_d: Optional[PhaseDResult] = None,
    phase_e: Optional["PhaseEResult"] = None,
):
    """Print the final executive summary with rich formatting."""
    console.print()
    console.rule("[bold white]Executive Summary", style="cyan")
    console.print()

    # ---- Phase Results Table ----
    results_table = Table(
        title="Phase Results",
        box=box.ROUNDED,
        title_style="bold white",
        header_style="bold cyan",
    )
    results_table.add_column("Phase", style="white", width=12)
    results_table.add_column("Status", justify="center", width=8)
    results_table.add_column("Duration", justify="right", width=10)
    results_table.add_column("Details", style="dim")

    # Phase A row
    a_details = f"{phase_a.chunk_count} chunks" if phase_a.success else (phase_a.error or "skipped")
    if phase_a.chunk_count:
        a_details += f" (VCF: {phase_a.vcf_chunks}, SAM: {phase_a.sam_chunks})"
    results_table.add_row(
        "A: Ingest",
        _status_icon(phase_a.success),
        _fmt_duration(phase_a.duration_s),
        a_details,
    )

    # Phase B row
    b_details = (
        f"{phase_b.enforced} enforced, {phase_b.quarantine} quarantine"
        if phase_b.success and phase_b.total_mined
        else (phase_b.error or "skipped")
    )
    results_table.add_row(
        "B: Mine MRs",
        _status_icon(phase_b.success),
        _fmt_duration(phase_b.duration_s),
        b_details,
    )

    # Phase C row
    c_details = (
        f"{phase_c.total_tests} tests, {phase_c.bugs_found} bugs found"
        if phase_c.success
        else (phase_c.error or "skipped")
    )
    results_table.add_row(
        "C: Execute",
        _status_icon(phase_c.success),
        _fmt_duration(phase_c.duration_s),
        c_details,
    )

    # Phase D row
    if phase_d and phase_d.termination_reason != "not_requested":
        d_details = (
            f"{phase_d.iterations_completed} iter, "
            f"SCC={phase_d.final_scc_percent:.1f}%, "
            f"stop: {phase_d.termination_reason}"
            if phase_d.success
            else (phase_d.error or "skipped")
        )
        results_table.add_row(
            "D: Feedback",
            _status_icon(phase_d.success),
            _fmt_duration(phase_d.duration_s),
            d_details,
        )

    # Phase E row
    if phase_e and (phase_e.duration_s > 0 or phase_e.error):
        kept_total = (phase_e.vcf_struct_kept + phase_e.vcf_rawfuzz_kept
                      + phase_e.sam_struct_kept + phase_e.sam_rawfuzz_kept)
        e_details = (
            f"+{kept_total} corpus files "
            f"(VCF: {phase_e.vcf_struct_kept} struct + {phase_e.vcf_rawfuzz_kept} rawfuzz; "
            f"SAM: {phase_e.sam_struct_kept} struct + {phase_e.sam_rawfuzz_kept} rawfuzz)"
            if phase_e.success
            else (phase_e.error or "skipped")
        )
        results_table.add_row(
            "E: Augment",
            _status_icon(phase_e.success),
            _fmt_duration(phase_e.duration_s),
            e_details,
        )

    console.print(results_table)
    console.print()

    # ---- Test Metrics Panel ----
    if phase_c.total_tests > 0:
        metrics = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
        metrics.add_column("Metric", style="white", width=28)
        metrics.add_column("Value", style="bold", justify="right", width=12)

        # Format & version
        specs = cfg.get("phase_a", {}).get("specs", [])
        for s in specs:
            metrics.add_row(
                f"Format Tested",
                f"{s['format']} v{s['version']}",
            )

        # Themes
        themes = phase_b.themes_tested or cfg.get("phase_b", {}).get("themes", [])
        metrics.add_row("Themes Tested", str(len(themes)))
        for t in themes:
            metrics.add_row(f"  [dim]{t}[/]", "")

        metrics.add_row("", "")
        metrics.add_row("Seeds Used", str(phase_c.seeds_used))
        metrics.add_row("Variants Generated", str(phase_c.variants_generated))
        metrics.add_row("Runners", ", ".join(phase_c.runners_used))
        metrics.add_row("", "")
        metrics.add_row("Total Tests", str(phase_c.total_tests))
        metrics.add_row("Metamorphic Failures", str(phase_c.metamorphic_failures))
        metrics.add_row("Differential Failures", str(phase_c.differential_failures))
        metrics.add_row("Crashes", str(phase_c.crashes))
        metrics.add_row("", "")

        # DET rate with color
        det_pct = phase_c.det_rate * 100
        if det_pct == 0:
            det_color = "green"
        elif det_pct < 20:
            det_color = "yellow"
        else:
            det_color = "red"
        metrics.add_row(
            "[bold]DET Rate[/]",
            f"[bold {det_color}]{det_pct:.1f}%[/]",
        )
        metrics.add_row(
            "[bold]Bugs / DETs Found[/]",
            f"[bold {'red' if phase_c.bugs_found else 'green'}]{phase_c.bugs_found}[/]",
        )

        console.print(Panel(metrics, title="Test Metrics", border_style="cyan"))
        console.print()

    # ---- Total Duration ----
    console.print(
        f"  [bold]Total Pipeline Duration:[/]  [cyan]{_fmt_duration(total_duration)}[/]"
    )
    console.print()

    # ---- Phase D SCC Panel ----
    if phase_d and phase_d.scc_history:
        scc_text = " -> ".join(f"{s:.1f}%" for s in phase_d.scc_history)
        scc_color = (
            "green" if phase_d.final_scc_percent >= 95
            else "yellow" if phase_d.final_scc_percent >= 50
            else "red"
        )
        console.print(Panel(
            f"[bold]SCC Progression:[/] {scc_text}\n"
            f"[bold]Final SCC:[/] [{scc_color}]{phase_d.final_scc_percent:.1f}%[/]\n"
            f"[bold]Termination:[/] {phase_d.termination_reason}\n"
            f"[bold]MRs Quarantined:[/] {phase_d.total_demoted}",
            title="Phase D: Feedback Loop",
            border_style="cyan",
        ))
        console.print()

    # ---- Code Coverage Panel (primary SUT only, format-scoped) ----
    if phase_d and phase_d.final_coverage_total:
        cov_text = " -> ".join(f"{c:.1f}%" for c in phase_d.coverage_history) \
                   if phase_d.coverage_history else f"{phase_d.final_coverage_pct:.1f}%"
        cov_color = (
            "green" if phase_d.final_coverage_pct >= 70
            else "yellow" if phase_d.final_coverage_pct >= 30
            else "red"
        )
        console.print(Panel(
            f"[bold]Primary SUT:[/] {phase_d.coverage_target} "
            f"([dim]{phase_d.coverage_language}[/])\n"
            f"[bold]Coverage Progression:[/] {cov_text}\n"
            f"[bold]Final Coverage:[/] [{cov_color}]"
            f"{phase_d.final_coverage_pct:.1f}%[/] "
            f"({phase_d.final_coverage_covered}/{phase_d.final_coverage_total} "
            f"format-scoped lines)",
            title="Code Coverage",
            border_style="magenta",
        ))
        console.print()

    # ---- Final Verdict ----
    d_ok = phase_d.success if phase_d else True
    all_ok = phase_a.success and phase_b.success and phase_c.success and d_ok
    if all_ok and phase_c.bugs_found == 0:
        console.print(Panel(
            "[bold green]ALL CLEAR[/] — No bugs detected across all parsers.",
            border_style="green",
        ))
    elif all_ok and phase_c.bugs_found > 0:
        console.print(Panel(
            f"[bold yellow]BUGS DETECTED[/] — {phase_c.bugs_found} difference-exposing "
            f"test(s) found. Check [cyan]bug_reports/[/] for details.",
            border_style="yellow",
        ))
    else:
        failed = []
        if not phase_a.success:
            failed.append("A")
        if not phase_b.success:
            failed.append("B")
        if not phase_c.success:
            failed.append("C")
        if phase_d and not phase_d.success:
            failed.append("D")
        console.print(Panel(
            f"[bold red]PIPELINE FAILED[/] — Phase(s) {', '.join(failed)} encountered errors.",
            border_style="red",
        ))


# ===========================================================================
# Main pipeline orchestration
# ===========================================================================

def run_pipeline(cfg: dict[str, Any], phase_filter: Optional[str] = None):
    """Run the full A → B → C → D pipeline or selected phases."""
    total_t0 = time.monotonic()

    phase_a_result = PhaseAResult(success=True)
    phase_b_result = PhaseBResult(success=True)
    phase_c_result = PhaseCResult(success=True)
    phase_d_result = PhaseDResult(success=True, termination_reason="not_requested")
    phase_e_result = PhaseEResult(success=True)

    # Default: run ALL five phases. Phase E (corpus augmentation —
    # Ranks 12+13) was added 2026-04-23 after Run-7/8 measured those
    # ranks adding 5–20 kills per cell; making them part of the
    # auto-pipeline means a default `python biotest.py` produces the
    # same corpus the mutation-score harness reads from. Disable
    # individually via --phases A,B,C,D or biotest_config.yaml flags.
    phases_to_run = {"A", "B", "C", "D", "E"}
    if phase_filter:
        phases_to_run = {p.strip().upper() for p in phase_filter.split(",")}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:

        # --- Phase A ---
        if "A" in phases_to_run and cfg.get("phase_a", {}).get("enabled", True):
            task = progress.add_task("[cyan]Phase A:[/] Ingesting specifications...", total=None)
            phase_a_result = run_phase_a(cfg)
            progress.remove_task(task)
            icon = "[green]OK[/]" if phase_a_result.success else "[red]FAIL[/]"
            console.print(f"  Phase A: {icon}  ({_fmt_duration(phase_a_result.duration_s)})")

        # --- Phase B ---
        if "B" in phases_to_run and cfg.get("phase_b", {}).get("enabled", True):
            task = progress.add_task("[cyan]Phase B:[/] Mining metamorphic relations...", total=None)
            phase_b_result = run_phase_b(cfg)
            progress.remove_task(task)
            icon = "[green]OK[/]" if phase_b_result.success else "[red]FAIL[/]"
            console.print(f"  Phase B: {icon}  ({_fmt_duration(phase_b_result.duration_s)})")

        # --- Phase C ---
        if "C" in phases_to_run and cfg.get("phase_c", {}).get("enabled", True):
            task = progress.add_task("[cyan]Phase C:[/] Running cross-execution tests...", total=None)
            # Wrap Phase C in coverage.py when Phase D isn't also going to
            # run, so standalone --phase C invocations still populate the
            # coverage.py data file for Python SUTs. Phase D already wraps
            # its own Phase C calls, so skip when D will follow.
            cov_cfg = cfg.get("coverage", {})
            _cov_ctx = None
            if cov_cfg.get("enabled", False) and "D" not in phases_to_run:
                from test_engine.feedback.coverage_collector import PythonCoverageContext
                _cov_ctx = PythonCoverageContext(
                    data_file=cov_cfg.get("coveragepy_data_file", ".coverage"),
                    source_filter=cov_cfg.get("coveragepy_source_filter", []),
                )
            if _cov_ctx is not None:
                with _cov_ctx:
                    phase_c_result = run_phase_c(cfg)
            else:
                phase_c_result = run_phase_c(cfg)
            progress.remove_task(task)
            icon = "[green]OK[/]" if phase_c_result.success else "[red]FAIL[/]"
            console.print(f"  Phase C: {icon}  ({_fmt_duration(phase_c_result.duration_s)})")

        # --- Phase D ---
        if "D" in phases_to_run:
            task = progress.add_task("[cyan]Phase D:[/] Feedback-driven loop...", total=None)
            phase_d_result = run_phase_d(cfg)
            progress.remove_task(task)
            icon = "[green]OK[/]" if phase_d_result.success else "[red]FAIL[/]"
            console.print(f"  Phase D: {icon}  ({_fmt_duration(phase_d_result.duration_s)})")

        # --- Phase E (corpus augmentation — Ranks 12 + 13) ---
        if "E" in phases_to_run and cfg.get("phase_e", {}).get("enabled", True):
            task = progress.add_task("[cyan]Phase E:[/] Corpus augmentation (Ranks 12 + 13)...", total=None)
            phase_e_result = run_phase_e(cfg)
            progress.remove_task(task)
            icon = "[green]OK[/]" if phase_e_result.success else "[red]FAIL[/]"
            kept_total = (phase_e_result.vcf_struct_kept + phase_e_result.vcf_rawfuzz_kept
                          + phase_e_result.sam_struct_kept + phase_e_result.sam_rawfuzz_kept)
            console.print(f"  Phase E: {icon}  ({_fmt_duration(phase_e_result.duration_s)}, "
                          f"+{kept_total} corpus files: "
                          f"VCF struct={phase_e_result.vcf_struct_kept}, rawfuzz={phase_e_result.vcf_rawfuzz_kept}; "
                          f"SAM struct={phase_e_result.sam_struct_kept}, rawfuzz={phase_e_result.sam_rawfuzz_kept})")

    total_duration = time.monotonic() - total_t0

    # Print summary
    print_executive_summary(
        cfg, phase_a_result, phase_b_result, phase_c_result,
        total_duration, phase_d_result, phase_e_result,
    )

    # Exit code
    all_ok = (
        phase_a_result.success and phase_b_result.success
        and phase_c_result.success and phase_d_result.success
        and phase_e_result.success
    )
    return 0 if all_ok else 1


# ===========================================================================
# CLI entry point
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        prog="biotest",
        description="BioTest Grand Orchestrator — Metamorphic Testing Pipeline",
    )
    parser.add_argument(
        "--config", "-c",
        default="biotest_config.yaml",
        help="Path to YAML config file (default: biotest_config.yaml)",
    )
    parser.add_argument(
        "--phase", "-p",
        default=None,
        help="Run specific phase(s): A, B, C, or comma-separated (e.g. 'B,C')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and print summary without executing",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    # Banner
    print_banner()

    # Load config
    config_path = PROJECT_ROOT / args.config
    cfg = load_config(config_path)
    console.print(f"  [dim]Config loaded from:[/] {config_path.name}\n")
    print_config_summary(cfg)

    # Dry run?
    if args.dry_run:
        console.print("[yellow]Dry run mode — no phases executed.[/]")
        return 0

    # Run
    exit_code = run_pipeline(cfg, phase_filter=args.phase)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
