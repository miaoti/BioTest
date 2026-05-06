"""E1 — Phase A ablation runner (no RAG retrieval; Phase D feedback on).

Naive prompt-stuffing replaces RAG: the full HTS spec text (built by
shared/build_spec_dump.py) is appended to the LLM system prompt, the
query_spec_database tool is reduced to a no-op, and ChromaDB chunk_id
validation is bypassed. Phases B, C, D, E run normally.

Zero source-code modification — uses module-level monkey-patches
applied before biotest is imported.

Corpus isolation:
  * Input corpus is COPIED at startup from main seeds/ to
    <E1>/results/corpus/ — only legitimate input seeds (no kept_*,
    no synthetic_*, no Phase-E sister dirs).
  * Phase E is monkey-patched to write its augmentation output
    (<fmt>_struct/, <fmt>_rawfuzz/) into <E1>/results/corpus/ rather
    than the hardcoded PROJECT_ROOT/seeds tree.
  * <E1>/results/input_manifest.json records every copied file's
    SHA-256 so post-run audits can prove the corpus origin.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

E1_ROOT = Path(__file__).resolve().parent
SHARED_DIR = E1_ROOT.parent / "shared"
PROJECT_ROOT = E1_ROOT.parents[2]
SPEC_DUMP_PATH = SHARED_DIR / "raw_spec_dump.txt"

sys.path.insert(0, str(PROJECT_ROOT))

# Per-format primary_target. Each format's primary should have working
# coverage tooling (so SCC + Phase D feedback fire correctly):
#   VCF: noodles-vcf via cargo-llvm-cov (also: htsjdk/JaCoCo, vcfpy/coverage.py).
#   SAM: htsjdk via JaCoCo (also: biopython/coverage.py, seqan3/gcovr).
# These match the defaults used by the main BioTest 4-rep sweeps.
PRIMARY_TARGET_BY_FORMAT = {
    "VCF": "noodles",
    "SAM": "htsjdk",
}


# ---------------------------------------------------------------------------
# BioTest-generated artifact patterns. Files matching ANY of these are
# excluded from the input corpus copy — they are run outputs from prior
# BioTest invocations, not legitimate input seeds. Listed exhaustively
# so the audit trail is unambiguous.
# ---------------------------------------------------------------------------

EXCLUDED_FILE_PREFIXES = (
    "kept_",         # Rank 8 corpus keeper output
    "synthetic_",    # Rank 1 LLM seed-synth output
    ".kept_",        # Rank 8 audit manifest (.kept_manifest.jsonl)
    ".synthetic_",   # symmetric — defensive
)

# Sister directories under main seeds/ that are entirely BioTest-
# generated (Phase E + Ranks 9/10/11 CLI outputs). Never copied.
EXCLUDED_SISTER_DIRS = (
    "vcf_struct", "sam_struct",        # Rank 12 (Phase E)
    "vcf_rawfuzz", "sam_rawfuzz",      # Rank 13 (Phase E)
    "vcf_diverse", "sam_diverse",      # Rank 9 + Rank 11 (manual CLI)
    "vcf_bytefuzz", "sam_bytefuzz",    # Rank 10 (manual CLI)
)


# ---------------------------------------------------------------------------
# SpecIndex stub — empty collection, no ChromaDB load
# ---------------------------------------------------------------------------

class _StubCollection:
    def get(self, ids=None, **kwargs):
        return {"ids": [], "metadatas": []}

    def query(self, **kwargs):
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

    def count(self):
        return 0


class _StubSpecIndex:
    """E1 stub for EphemeralSpecIndex — returns empty for all queries."""

    _collection = _StubCollection()

    def query(self, question, n_results=5, where=None):
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

    def collection_stats(self):
        return {"collection": "<E1-stub>", "total_documents": 0, "type": "stub"}


_STUB_INDEX = _StubSpecIndex()


# ---------------------------------------------------------------------------
# Patch builders
# ---------------------------------------------------------------------------

def _make_naive_prompt_builder(original_build_fn, spec_text: str):
    """Wrap build_system_prompt so the spec dump is appended to every prompt."""

    def naive_build_system_prompt(*args, **kwargs):
        base = original_build_fn(*args, **kwargs)
        section = (
            "\n\n" + "=" * 60 + "\n"
            "HTS SPECIFICATION (NAIVE PROMPT-STUFFING — Phase A ablation)\n"
            + "=" * 60 + "\n"
            "The query_spec_database tool is disabled in this run.\n"
            "All normative evidence must come from the specification text\n"
            "below. When citing evidence in your MR output, set chunk_id\n"
            "to 'spec-blind' and provide the verbatim quote from the spec;\n"
            "the framework will not validate chunk_ids against ChromaDB\n"
            "in this configuration.\n\n"
            + spec_text
        )
        return base + section

    return naive_build_system_prompt


def _make_stub_hydrate(HydratedEvidence_cls):
    """Stub _hydrate_evidence: skip ChromaDB lookup, default severity=ADVISORY."""

    def stub_hydrate_evidence(raw_evidences, spec_index):
        hydrated = [
            HydratedEvidence_cls(
                chunk_id=ev.chunk_id or "spec-blind",
                quote=ev.quote,
                rule_severity="ADVISORY",
                section_id="<E1-naive>",
            )
            for ev in raw_evidences
        ]
        return hydrated, []

    return stub_hydrate_evidence


def _make_isolated_run_phase_e(biotest_module):
    """Replacement for biotest.run_phase_e that uses cfg['phase_c']['seeds_dir']
    as its seeds_root, instead of biotest.py's hardcoded PROJECT_ROOT/seeds.

    Body is a faithful copy of biotest.py's run_phase_e (as of 2026-04-23,
    biotest.py:1531) with the single line `seeds_root = repo_root / "seeds"`
    replaced. Without this patch, Phase E reads the main seeds/ corpus
    (different from E1's isolated input) and writes <fmt>_struct/<fmt>_rawfuzz
    into PROJECT_ROOT/seeds — polluting both directions.
    """
    import logging
    PhaseEResult = biotest_module.PhaseEResult
    logger = logging.getLogger("biotest")

    def isolated_run_phase_e(cfg):
        t0 = time.monotonic()
        if not cfg.get("phase_e", {}).get("enabled", True):
            return PhaseEResult(success=True, duration_s=0.0)

        seeds_root = Path(cfg["phase_c"]["seeds_dir"])
        result = PhaseEResult(success=True)

        formats: list[str] = []
        for fmt in ("VCF", "SAM"):
            ext = fmt.lower()
            seed_dir = seeds_root / ext
            if seed_dir.is_dir() and any(seed_dir.glob(f"*.{ext}")):
                formats.append(fmt)

        if not formats:
            logger.info("Phase E (E1-isolated): no seed formats — skipping")
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
                logger.info(
                    "Phase E (E1-isolated): Rank 12 (%s) kept %d in %s",
                    fmt, kept, struct_dir,
                )
            except Exception as e:
                logger.warning("Phase E (E1-isolated): Rank 12 (%s) failed — %s", fmt, e)
                result.success = False
                if not result.error:
                    result.error = f"Rank12_{fmt}: {e}"

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
                logger.info(
                    "Phase E (E1-isolated): Rank 13 (%s) kept %d in %s",
                    fmt, kept, rawfuzz_dir,
                )
            except Exception as e:
                logger.warning("Phase E (E1-isolated): Rank 13 (%s) failed — %s", fmt, e)
                result.success = False
                if not result.error:
                    result.error = f"Rank13_{fmt}: {e}"

        result.duration_s = time.monotonic() - t0
        return result

    return isolated_run_phase_e


# ---------------------------------------------------------------------------
# Apply patches (module-level rebinding — no source files touched)
# ---------------------------------------------------------------------------

def apply_e1_patches(spec_text: str) -> dict:
    """Install monkey-patches that disable Phase A's RAG and isolate
    Phase E's I/O. Returns a dict of patch metadata for logging.

    Note: the run_phase_e patch must be applied AFTER `import biotest`,
    so it lives in apply_phase_e_patch() below and runs from main()
    after the biotest module is imported.
    """
    import mr_engine.agent.engine as _engine
    import mr_engine.agent.tools as _tools
    import mr_engine.dsl.compiler as _compiler
    from mr_engine.dsl.models import HydratedEvidence

    _tools.get_ephemeral_index = lambda: _STUB_INDEX

    original_build = _engine.build_system_prompt
    _engine.build_system_prompt = _make_naive_prompt_builder(original_build, spec_text)

    _compiler._hydrate_evidence = _make_stub_hydrate(HydratedEvidence)

    return {
        "tools.get_ephemeral_index": "stub (empty SpecIndex)",
        "engine.build_system_prompt": "wrapped (appends spec dump)",
        "compiler._hydrate_evidence": "stub (no ChromaDB validation)",
    }


def apply_phase_e_patch(biotest_module) -> str:
    """Install the Phase E isolation patch. Must run after `import biotest`."""
    biotest_module.run_phase_e = _make_isolated_run_phase_e(biotest_module)
    return "biotest.run_phase_e: replaced (cfg-driven seeds_root)"


# ---------------------------------------------------------------------------
# E1-strict (E1S) — additional pre-import patches that strip the residual
# Phase-A-derived signals from the LLM's prompt. E1 left these in place
# because naive prompt-stuffing was the comparison goal; E1S removes them
# for a true "no Phase A" ablation.
# ---------------------------------------------------------------------------

def apply_e1_strict_extras() -> dict:
    """E1-strict patches — strip ALL Phase-A-derived content from the
    LLM's prompt:

      1. Replace the entire `build_system_prompt` (engine + prompts
         modules) with a truly-minimal version. Removes the hardcoded
         `_SYSTEM_TEMPLATE` from transforms_menu.py:169 which leaked
         heavy spec hints (RETRIEVAL RULES, PRECONDITION DISCIPLINE
         examples, compound-group hint, "VCFv4.5.tex" example anchors).
      2. Strip transform-menu descriptions to bare names (defense in
         depth — covered by #1 but cheap).
      3. Strip behavior fragment to enum value only (same).
      4. Strip blindspot-ticket spec-rule injection.

    Result: LLM sees format name + behavior-target enum + bare transform
    names + JSON output schema. No spec text, no precondition hints,
    no compound-group hints, no chromadb references.
    """
    import mr_engine.agent.transforms_menu as _menu_mod
    import mr_engine.agent.engine as _engine_mod
    import mr_engine.agent.prompts as _prompts_mod
    import mr_engine.behavior as _beh_mod
    import test_engine.feedback.blindspot_builder as _bs_mod
    from mr_engine.transforms import TRANSFORM_REGISTRY

    # 1. Truly minimal system prompt — replaces engine.build_system_prompt
    # AND prompts.build_system_prompt so any caller in either module
    # picks up the stub. This bypasses the leaky _SYSTEM_TEMPLATE
    # entirely.
    def minimal_build_system_prompt(
        target, spec_format,
        blindspot_context=None,
        primary_target="",
        available_suts=None,
        runtime_capabilities=None,
        query_methods=None,
    ):
        names = sorted([
            name for name, meta in TRANSFORM_REGISTRY.items()
            if spec_format in meta.format
        ])
        prompt = (
            "You produce metamorphic-relation specifications as JSON.\n"
            "\n"
            f"Format: {spec_format}\n"
            f"Target: {target.value}\n"
            "\n"
            "Output ONLY a JSON array. Each object:\n"
            "{\n"
            '  "mr_name": "<short label>",\n'
            f'  "scope": "{spec_format}.header" or "{spec_format}.record",\n'
            '  "preconditions": [],\n'
            '  "transform_steps": ["<name>", ...],\n'
            '  "oracle": "<invariant string>",\n'
            '  "evidence": [{"chunk_id": "spec-blind", "quote": ""}],\n'
            '  "ambiguity_flags": []\n'
            "}\n"
            "\n"
            "Available transform names (use exactly, case-sensitive):\n"
            f"  {', '.join(names)}\n"
            "\n"
            "Rules:\n"
            "- Use only names from the list above.\n"
            "- An empty array [] is valid output if no MR fits.\n"
        )
        if blindspot_context:
            prompt += "\n" + blindspot_context
        return prompt

    _engine_mod.build_system_prompt = minimal_build_system_prompt
    _prompts_mod.build_system_prompt = minimal_build_system_prompt

    # 2. Defense-in-depth: bare transform menu (in case any other code
    # path calls build_transforms_menu directly).
    def bare_transforms_menu(spec_format=None, runtime_capabilities=None):
        names = sorted([
            name for name, meta in TRANSFORM_REGISTRY.items()
            if (not spec_format or spec_format in meta.format)
        ])
        return ", ".join(names) if names else "(none)"

    _menu_mod.build_transforms_menu = bare_transforms_menu

    # 3. Defense-in-depth: bare behavior fragment.
    _beh_mod.get_system_prompt_fragment = lambda t: t.value

    # 4. Strip blindspot-ticket spec rules.
    _orig_build_ticket = _bs_mod.build_blindspot_ticket

    def stripped_build_ticket(*args, **kwargs):
        ticket = _orig_build_ticket(*args, **kwargs)
        ticket.uncovered_rules = []
        ticket.total_uncovered = 0
        ticket.shown_uncovered = 0
        ticket.remaining_uncovered = 0
        ticket.cooling_count = 0
        ticket.rule_scores = []
        return ticket

    _bs_mod.build_blindspot_ticket = stripped_build_ticket

    return {
        "engine.build_system_prompt": "stub (minimal — no spec/chromadb/precondition hints)",
        "prompts.build_system_prompt": "stub (same as engine)",
        "transforms_menu.build_transforms_menu": "stub (bare names)",
        "behavior.get_system_prompt_fragment": "stub (enum value only)",
        "blindspot_builder.build_blindspot_ticket": "wrapped (clears spec rules)",
    }


def apply_e1_strict_patches() -> dict:
    """E1-strict bundle: tools stub + chunk_id stub + (no naive spec
    stuffing) + transform-menu strip + behavior fragment strip + blindspot
    rule strip. Phase E isolation patch must be applied separately
    after `import biotest`.
    """
    import mr_engine.agent.tools as _tools
    import mr_engine.dsl.compiler as _compiler
    from mr_engine.dsl.models import HydratedEvidence

    # Same as E1 patches 1 + 3 (no naive prompt-stuffing).
    _tools.get_ephemeral_index = lambda: _STUB_INDEX
    _compiler._hydrate_evidence = _make_stub_hydrate(HydratedEvidence)

    base = {
        "tools.get_ephemeral_index": "stub (empty SpecIndex)",
        "compiler._hydrate_evidence": "stub (no ChromaDB validation)",
    }
    base.update(apply_e1_strict_extras())
    return base


# ---------------------------------------------------------------------------
# E2 (no Phase D) — bound Phase C runtime so coverage collection runs.
#
# Without Phase D's max_iterations/timeout_minutes, the single Phase C run
# can spend the whole wall budget shrinking failures (Hypothesis Phase.shrink
# loop). When the wall budget kills the harness mid-shrink, biotest.py's
# `with py_cov_ctx:` block never exits → coverage.py never flushes → host
# cells (biopython, vcfpy) end up with status="missing".
#
# Fix: monkey-patch the orchestrator's `settings` symbol so the @settings
# decorator inside `_run_mr_with_hypothesis` filters out Phase.shrink and
# imposes a per-test deadline. Phase C still runs all generated examples
# but cannot get stuck in unbounded shrink storms. This is scoped to the
# orchestrator module — other Hypothesis users are unaffected.
# ---------------------------------------------------------------------------

def apply_e2_phase_c_patch(per_test_deadline_ms: int = 5000) -> dict:
    """Bound Phase C runtime under E2's no-Phase-D config.

    Replaces orchestrator.settings (the imported `from hypothesis import
    settings`) with a wrapper that strips Phase.shrink from any phases
    list and forces deadline=per_test_deadline_ms. Other settings kwargs
    pass through unchanged.
    """
    from test_engine import orchestrator as _orch
    from hypothesis import settings as _orig_settings, Phase as _Phase

    def _e2_settings(*args, **kwargs):
        if "phases" in kwargs and kwargs["phases"]:
            kwargs["phases"] = tuple(
                p for p in kwargs["phases"] if p != _Phase.shrink
            )
        kwargs["deadline"] = per_test_deadline_ms
        return _orig_settings(*args, **kwargs)

    _orch.settings = _e2_settings
    return {
        "orchestrator.settings": (
            f"wrapped: Phase.shrink stripped, deadline={per_test_deadline_ms}ms"
        ),
    }


# ---------------------------------------------------------------------------
# Config overrides + corpus sync
# ---------------------------------------------------------------------------

def _load_main_config() -> dict:
    main_yaml = PROJECT_ROOT / "biotest_config.yaml"
    return yaml.safe_load(main_yaml.read_text(encoding="utf-8"))


def _redirect_outputs(cfg: dict, results_root: Path, corpus_root: Path, fmt: str) -> None:
    """Rewrite every config path that biotest writes to so E1's outputs
    land under <results_root>/, not the main run's directories. Also
    set the format filter and primary target for this format.
    """
    r = results_root

    cfg["phase_b"]["registry_path"] = str(r / "mr_registry.json")
    # phase_c.seeds_dir is the working corpus dir despite the legacy key
    # name. The Phase E patch reads from it too.
    cfg["phase_c"]["seeds_dir"] = str(corpus_root)
    cfg["phase_c"]["output_dir"] = str(r / "bug_reports")
    cfg["phase_c"]["det_report_path"] = str(r / "det_report.json")
    cfg["phase_c"]["format_filter"] = fmt

    cov = cfg.setdefault("coverage", {})
    cov["jacoco_report_dir"] = str(r / "coverage" / "jacoco")
    cov["coveragepy_data_file"] = str(r / "coverage" / ".coverage")
    cov["pysam_coverage_dir"] = str(r / "coverage" / "pysam")
    cov["gcovr_report_path"] = str(r / "coverage" / "gcovr.json")
    cov["noodles_report_path"] = str(r / "coverage" / "noodles" / "llvm-cov.json")
    cov["noodles_profile_dir"] = str(r / "coverage" / "noodles")

    fb = cfg.setdefault("feedback_control", {})
    fb["state_path"] = str(r / "feedback_state.json")
    fb["attempts_path"] = str(r / "rule_attempts.json")
    fb["primary_target"] = PRIMARY_TARGET_BY_FORMAT[fmt]

    cfg.setdefault("phase_a", {})["enabled"] = False


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sync_input_corpus(cfg: dict) -> dict:
    """Copy legitimate input seeds from main seeds/ tree into <E1>/results/corpus/.

    Filters out BioTest-generated artifacts on both axes:
      1. files inside main seeds/<fmt>/ whose name starts with one of
         EXCLUDED_FILE_PREFIXES (kept_*, synthetic_*) — Phase B/C/D
         outputs from prior runs;
      2. main seeds/<fmt>_struct, /<fmt>_rawfuzz, /<fmt>_diverse,
         /<fmt>_bytefuzz sister directories — Phase E + manual CLI
         outputs from prior runs.

    Writes a SHA-256 manifest to <E1>/results/input_manifest.json so
    post-run audits can prove the input corpus origin.
    """
    src = PROJECT_ROOT / "seeds"
    dst_root = Path(cfg["phase_c"]["seeds_dir"])
    dst_root.mkdir(parents=True, exist_ok=True)

    manifest: dict = {
        "schema_version": 1,
        "source_root": str(src),
        "destination_root": str(dst_root),
        "excluded_file_prefixes": list(EXCLUDED_FILE_PREFIXES),
        "excluded_sister_dirs": list(EXCLUDED_SISTER_DIRS),
        "copied": [],
        "skipped_artifacts": [],
        "skipped_sister_dirs_present": [],
    }

    # Detect (but do not copy) any sister dirs in main seeds/ that
    # exist — visibility for the audit log.
    for d in EXCLUDED_SISTER_DIRS:
        if (src / d).exists():
            manifest["skipped_sister_dirs_present"].append(d)

    for sub in ("vcf", "sam", "ref"):
        src_sub = src / sub
        if not src_sub.is_dir():
            continue
        dst_sub = dst_root / sub
        dst_sub.mkdir(parents=True, exist_ok=True)
        for f in sorted(src_sub.iterdir()):
            if not f.is_file():
                continue
            if f.name.startswith(EXCLUDED_FILE_PREFIXES):
                manifest["skipped_artifacts"].append(f"{sub}/{f.name}")
                continue
            target = dst_sub / f.name
            if not target.exists():
                shutil.copy2(f, target)
            manifest["copied"].append({
                "path": f"{sub}/{f.name}",
                "size_bytes": target.stat().st_size,
                "sha256": _sha256(target),
            })

    return manifest


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="E1 — Phase A ablation runner")
    parser.add_argument(
        "--format", required=True, choices=("VCF", "SAM"),
        help="Format scope for this run. Determines SUTs exercised + primary_target.",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Apply patches + sync corpus + dump effective config; do not run.",
    )
    args = parser.parse_args()

    fmt = args.format
    results_root = E1_ROOT / "results" / fmt.lower()
    corpus_root = results_root / "corpus"
    input_manifest_path = results_root / "input_manifest.json"

    if not SPEC_DUMP_PATH.exists():
        print(
            f"ERROR: {SPEC_DUMP_PATH} not found.\n"
            f"Run: py -3.12 {SHARED_DIR / 'build_spec_dump.py'}",
            file=sys.stderr,
        )
        return 1

    spec_text = SPEC_DUMP_PATH.read_text(encoding="utf-8")
    print(f"[E1/{fmt}] Loaded spec dump: {len(spec_text):,} chars")

    patch_log = apply_e1_patches(spec_text)
    print(f"[E1/{fmt}] Patches applied (pre-import):")
    for name, what in patch_log.items():
        print(f"  - {name}: {what}")

    cfg = _load_main_config()
    _redirect_outputs(cfg, results_root, corpus_root, fmt)

    results_root.mkdir(parents=True, exist_ok=True)
    manifest = _sync_input_corpus(cfg)
    input_manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(
        f"[E1/{fmt}] Input corpus synced: {len(manifest['copied'])} files copied, "
        f"{len(manifest['skipped_artifacts'])} BioTest artifacts skipped, "
        f"{len(manifest['skipped_sister_dirs_present'])} BioTest sister dirs skipped"
    )
    print(f"[E1/{fmt}] Input manifest: {input_manifest_path}")
    print(f"[E1/{fmt}] format_filter={fmt}, primary_target={PRIMARY_TARGET_BY_FORMAT[fmt]}")

    eff_cfg_path = results_root / "effective_config.yaml"
    eff_cfg_path.write_text(
        yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"[E1/{fmt}] Effective config: {eff_cfg_path}")

    # Import biotest AFTER the engine/tools/compiler patches are in place,
    # then patch run_phase_e (which must reference biotest.PhaseEResult).
    import biotest
    phase_e_log = apply_phase_e_patch(biotest)
    print(f"[E1/{fmt}] Patches applied (post-import):")
    print(f"  - {phase_e_log}")

    if args.check:
        print(f"[E1/{fmt}] --check passed; not running pipeline.")
        return 0

    return biotest.run_pipeline(cfg, phase_filter="B,C,D,E")


if __name__ == "__main__":
    sys.exit(main())
