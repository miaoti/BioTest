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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

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

def run_phase_b(cfg: dict[str, Any]) -> PhaseBResult:
    """Execute Phase B: mine MRs using the agentic RAG engine."""
    phase_cfg = cfg.get("phase_b", {})
    if not phase_cfg.get("enabled", True):
        return PhaseBResult(success=True)

    t0 = time.monotonic()
    try:
        from mr_engine.behavior import BehaviorTarget, get_all_targets
        from mr_engine.agent.engine import mine_mrs
        from mr_engine.registry import triage, export_registry

        formats = phase_cfg.get("formats", ["VCF"])
        theme_names = phase_cfg.get("themes", [])
        registry_path = phase_cfg.get("registry_path", "data/mr_registry.json")

        # Resolve themes to BehaviorTarget enums
        all_targets = get_all_targets()
        if theme_names:
            targets = [t for t in all_targets if t.value in theme_names]
        else:
            targets = all_targets

        themes_tested = [t.value for t in targets]
        all_relations = []

        for fmt in formats:
            for target in targets:
                console.print(f"  [dim]Mining {fmt} / {target.value}...[/]")
                result = mine_mrs(target, fmt)
                if result.success and result.relations:
                    all_relations.extend(result.relations)

        # Triage
        registry = triage(all_relations)
        out_path = str(PROJECT_ROOT / registry_path)
        export_registry(registry, out_path)

        return PhaseBResult(
            success=True,
            themes_tested=themes_tested,
            total_mined=len(all_relations),
            enforced=len(registry.enforced),
            quarantine=len(registry.quarantine),
            duration_s=time.monotonic() - t0,
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
    """Build runner instances from YAML SUT configuration."""
    from test_engine.runners.base import ParserRunner
    from test_engine.runners.htsjdk_runner import HTSJDKRunner
    from test_engine.runners.pysam_runner import PysamRunner
    from test_engine.runners.biopython_runner import BiopythonRunner
    from test_engine.runners.seqan3_runner import SeqAn3Runner
    from test_engine.runners.reference_runner import ReferenceRunner

    sut_cfgs = cfg.get("phase_c", {}).get("suts", [])
    runner_map = {
        "htsjdk": lambda c: HTSJDKRunner(
            jar_path=Path(c["adapter"]) if c.get("adapter") else None,
            java_cmd=c.get("java_cmd", "java"),
        ),
        "biopython": lambda c: BiopythonRunner(),
        "pysam": lambda c: PysamRunner(),
        "seqan3": lambda c: SeqAn3Runner(
            binary_path=Path(c["adapter"]) if c.get("adapter") else None,
        ),
        "reference": lambda c: ReferenceRunner(),
    }

    runners = []
    for sut in sut_cfgs:
        name = sut.get("name", "")
        if not sut.get("enabled", True):
            continue
        factory = runner_map.get(name)
        if factory:
            runners.append(factory(sut))

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

        result = run_test_suite(
            runners=available,
            registry_path=registry_path,
            seeds_dir=seeds_dir,
            output_dir=output_dir,
            format_filter=format_filter,
        )

        # Export DET report
        det_report.parent.mkdir(parents=True, exist_ok=True)
        result.det_tracker.export(str(det_report))

        return PhaseCResult(
            success=True,
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
        )
    except Exception as e:
        return PhaseCResult(
            success=False,
            error=str(e),
            duration_s=time.monotonic() - t0,
        )


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
    table.add_row("Enabled Phases", " -> ".join(phases))

    console.print(table)
    console.print()


def print_executive_summary(
    cfg: dict[str, Any],
    phase_a: PhaseAResult,
    phase_b: PhaseBResult,
    phase_c: PhaseCResult,
    total_duration: float,
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

    # ---- Final Verdict ----
    all_ok = phase_a.success and phase_b.success and phase_c.success
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
        console.print(Panel(
            f"[bold red]PIPELINE FAILED[/] — Phase(s) {', '.join(failed)} encountered errors.",
            border_style="red",
        ))


# ===========================================================================
# Main pipeline orchestration
# ===========================================================================

def run_pipeline(cfg: dict[str, Any], phase_filter: Optional[str] = None):
    """Run the full A → B → C pipeline or a single phase."""
    total_t0 = time.monotonic()

    phase_a_result = PhaseAResult(success=True)
    phase_b_result = PhaseBResult(success=True)
    phase_c_result = PhaseCResult(success=True)

    phases_to_run = {"A", "B", "C"}
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
            phase_c_result = run_phase_c(cfg)
            progress.remove_task(task)
            icon = "[green]OK[/]" if phase_c_result.success else "[red]FAIL[/]"
            console.print(f"  Phase C: {icon}  ({_fmt_duration(phase_c_result.duration_s)})")

    total_duration = time.monotonic() - total_t0

    # Print summary
    print_executive_summary(cfg, phase_a_result, phase_b_result, phase_c_result, total_duration)

    # Exit code
    all_ok = phase_a_result.success and phase_b_result.success and phase_c_result.success
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
