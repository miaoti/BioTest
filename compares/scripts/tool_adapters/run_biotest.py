"""BioTest adapter — invokes the main BioTest pipeline's Phase C.

The adapter contract is "run for N seconds, capture whatever the tool
produced, report exit status." Since `biotest.py` has no native time
budget flag, we enforce the budget via subprocess timeout (SIGTERM on
the wrapper, then SIGKILL on the timer) — same pattern every other
adapter uses.

Coverage growth (DESIGN §4.5):
Alongside the usual `adapter_result.json`, the adapter now emits
`growth_<rep>.json` at the parent of `out_dir` (so a `coverage_sampler`
style multi-rep layout lines up with other tools'
`compares/results/coverage/<tool>/<cell>/growth_{0,1,2}.json`). The
emitter drives a tick-poll loop at the DESIGN §3.2 log ticks
`{1, 10, 60, 300, 1800, 7200}` intersected with the budget: at each
boundary it snapshots whichever coverage artefact biotest.py writes
for the current SUT and measures it through `measure_coverage.py` under
the same scope every other tool uses. Early ticks may read 0 / 0
because biotest's coverage artefacts are written at iteration
boundaries (JaCoCo, gcovr), context exit (coverage.py), or explicit
regeneration (llvm-cov) — not continuously. Line % is propagated
forward across missing samples so the curve stays monotonic and
passes `validate_growth_schema.py`.

Assumptions (documented in §13.2.1 of compares/DESIGN.md):
- Phase A + B have run already. `data/mr_registry.json` exists.
- `biotest_config.yaml` in the repo root has `phase_c.suts` configured
  for the target SUT; we don't synthesize config on the fly.
- BioTest's output lives at its usual paths (`bug_reports/`,
  `data/det_report.json`, `coverage_artifacts/`). We capture those by
  symlinking / copying after the run rather than rerouting stdio.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _base import (  # noqa: E402
    AdapterResult,
    prepare_out_dir,
    run_subprocess_with_timeout,
    count_files,
)


REPO_ROOT = Path(__file__).resolve().parents[3]

# DESIGN §3.2 primary log-tick schedule. The adapter emits a row for
# every tick that fits within the budget; ticks beyond the budget are
# dropped.
DEFAULT_TICKS: tuple[int, ...] = (1, 10, 60, 300, 1800, 7200)


# ---------------------------------------------------------------------------
# Coverage-growth helpers — tick polling + measurement
# ---------------------------------------------------------------------------

def _hash_corpus(corpus_dir: Path) -> str:
    """Matches the sampler-side convention in
    `compares/scripts/coverage_sampler.py::_hash_corpus`."""
    if not corpus_dir.exists():
        return "sha256:empty"
    h = hashlib.sha256()
    for p in sorted(p for p in corpus_dir.rglob("*") if p.is_file()):
        h.update(p.name.encode("utf-8"))
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def _load_cfg_yaml(cfg_path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        return {}
    try:
        return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _live_coverage_artefact(
    sut: str,
    cfg: dict[str, Any],
) -> tuple[Path | None, str]:
    """Return `(artefact_path, kind)` for the current SUT.

    `kind` is one of `{'jacoco', 'coveragepy', 'gcovr', 'llvmcov', ''}`.
    Paths are resolved against `REPO_ROOT` using the same keys biotest.py
    uses (see `biotest_config.yaml: coverage.*`).
    """
    coverage_cfg = (cfg.get("coverage") or {}) if isinstance(cfg, dict) else {}

    if sut == "htsjdk":
        jdir = coverage_cfg.get("jacoco_report_dir")
        if jdir:
            return REPO_ROOT / jdir / "jacoco.xml", "jacoco"
    elif sut in {"biopython", "vcfpy"}:
        data = coverage_cfg.get("coveragepy_data_file")
        if data:
            return REPO_ROOT / data, "coveragepy"
    elif sut == "pysam":
        # pysam uses a directory of coverage.py fragments combined
        # offline. Live mid-run measurement is not wired up — fall
        # through.
        return None, ""
    elif sut == "seqan3":
        gp = coverage_cfg.get("gcovr_report_path")
        if gp:
            return REPO_ROOT / gp, "gcovr"
    elif sut == "noodles":
        np_ = coverage_cfg.get("noodles_report_path")
        if np_:
            return REPO_ROOT / np_, "llvmcov"
    return None, ""


def _import_measure_coverage():
    """Lazy-import `compares/scripts/measure_coverage.py` so the adapter
    still loads on hosts where the scripts dir isn't on PYTHONPATH."""
    scripts_dir = REPO_ROOT / "compares" / "scripts"
    s = str(scripts_dir)
    if s not in sys.path:
        sys.path.insert(0, s)
    import measure_coverage  # noqa: E402
    return measure_coverage


def _measure_artefact(
    artefact: Path,
    kind: str,
    sut: str,
    format_hint: str,
    cfg_path: Path,
) -> tuple[float, float]:
    """Snapshot the artefact and return `(line_pct, branch_pct)`.

    `branch_pct = 0.0` when the backend doesn't emit branch counters in
    the shape `measure_coverage.measure()` parses (coverage.py, gcovr,
    cargo-llvm-cov — see `measure_coverage._dispatch_reader`). JaCoCo
    XML reports both.
    """
    try:
        measure_coverage = _import_measure_coverage()
    except Exception:
        return 0.0, 0.0

    fmt_up = format_hint.upper()

    if kind == "coveragepy":
        # coverage.py keeps the .coverage SQLite open through
        # `PythonCoverageContext`; a direct read races with the tracer's
        # writes, so we copy to a snapshot path and export JSON there.
        snap_dir = artefact.parent / ".biotest_adapter_snap"
        try:
            snap_dir.mkdir(exist_ok=True)
        except OSError:
            return 0.0, 0.0
        snap_id = uuid.uuid4().hex[:8]
        snap_db = snap_dir / f"snap_{snap_id}.db"
        snap_json = snap_dir / f"snap_{snap_id}.json"
        try:
            try:
                shutil.copy2(artefact, snap_db)
            except OSError:
                return 0.0, 0.0
            proc = subprocess.run(
                [sys.executable, "-m", "coverage", "json",
                 "--data-file", str(snap_db), "-o", str(snap_json)],
                capture_output=True, timeout=30, check=False,
            )
            if proc.returncode != 0 or not snap_json.exists():
                return 0.0, 0.0
            res = measure_coverage.measure(
                snap_json, sut=sut, format_=fmt_up,
                config_path=cfg_path, metric="LINE",
            )
            return float(res.weighted_pct), 0.0
        except Exception:
            return 0.0, 0.0
        finally:
            try:
                snap_db.unlink(missing_ok=True)
                snap_json.unlink(missing_ok=True)
            except OSError:
                pass

    if kind == "jacoco":
        try:
            line_r = measure_coverage.measure(
                artefact, sut=sut, format_=fmt_up,
                config_path=cfg_path, metric="LINE",
            )
            branch_r = measure_coverage.measure(
                artefact, sut=sut, format_=fmt_up,
                config_path=cfg_path, metric="BRANCH",
            )
            return float(line_r.weighted_pct), float(branch_r.weighted_pct)
        except Exception:
            return 0.0, 0.0

    if kind in {"gcovr", "llvmcov"}:
        try:
            res = measure_coverage.measure(
                artefact, sut=sut, format_=fmt_up,
                config_path=cfg_path, metric="LINE",
            )
            return float(res.weighted_pct), 0.0
        except Exception:
            return 0.0, 0.0

    return 0.0, 0.0


def _tick_snapshot(
    sut: str,
    format_hint: str,
    cfg_path: Path,
    cfg: dict[str, Any],
    started_at: float,
    last_reading: tuple[float, float],
) -> tuple[float, float]:
    """Read the live coverage artefact and return `(line_pct, branch_pct)`.

    Returns `last_reading` unchanged if the artefact doesn't exist yet,
    if its mtime predates `started_at` (stale from a prior run), or if
    measurement fails. Line and branch are monotonically propagated —
    they never regress during a single rep.
    """
    artefact, kind = _live_coverage_artefact(sut, cfg)
    if artefact is None or not kind:
        return last_reading
    try:
        if not artefact.exists():
            return last_reading
        if artefact.stat().st_mtime < started_at:
            return last_reading  # artefact is from a prior biotest run
    except OSError:
        return last_reading

    line, branch = _measure_artefact(
        artefact, kind, sut, format_hint, cfg_path,
    )
    line = max(line, last_reading[0])
    branch = max(branch, last_reading[1])
    return line, branch


def _rep_index_from_out_dir(out_dir: Path) -> int:
    """Infer rep index from `out_dir.name` if it matches `run_<N>`,
    else default to 0."""
    m = re.match(r"^run_(\d+)$", out_dir.name)
    return int(m.group(1)) if m else 0


def _growth_parent_dir(out_dir: Path) -> Path:
    """Where `growth_<rep>.json` lives. If out_dir is `.../run_N/` the
    growth file goes to `.../`. Otherwise to out_dir itself so a
    standalone invocation still emits something."""
    if re.match(r"^run_\d+$", out_dir.name):
        return out_dir.parent
    return out_dir


def _emit_growth_json(
    *,
    out_dir: Path,
    sut: str,
    format_hint: str,
    time_budget_s: int,
    growth: list[dict[str, Any]],
    seed_corpus_hash: str,
    seed_corpus: Path,
    started: float,
    ended: float,
    ticks_requested: list[int],
    note: str,
) -> Path:
    """Write `growth_<rep>.json` matching DESIGN §4.5 schema. Rep index
    inferred from `out_dir.name` pattern `run_<N>`."""
    rep = _rep_index_from_out_dir(out_dir)
    parent = _growth_parent_dir(out_dir)
    parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "biotest",
        "sut": sut,
        "format": format_hint.upper(),
        "phase": "coverage",
        "run_index": rep,
        "time_budget_s": int(time_budget_s),
        "seed_corpus_hash": seed_corpus_hash,
        "coverage_growth": growth,
        "mutation_score": None,
        "bug_bench": None,
        "extra": {
            "duration_s": round(ended - started, 2),
            "seed_corpus_dir": str(seed_corpus),
            "out_dir": str(out_dir),
            "ticks_requested": list(ticks_requested),
            "note": note,
        },
    }
    out = parent / f"growth_{rep}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def _select_ticks(time_budget_s: int) -> list[int]:
    """Pick the log-tick subset that fits within the budget. Always
    anchors the final tick to `time_budget_s` so downstream validators
    see a sample at the full-budget boundary."""
    ticks = [t for t in DEFAULT_TICKS if t <= time_budget_s]
    if not ticks:
        return [int(time_budget_s)]
    if ticks[-1] != time_budget_s:
        ticks.append(int(time_budget_s))
    return ticks


# ---------------------------------------------------------------------------
# Main run()
# ---------------------------------------------------------------------------

def run(
    sut: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    format_hint: str = "VCF",
    config_path: Path | None = None,
    **_kwargs,
) -> AdapterResult:
    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    started = time.time()

    cfg_path_original = config_path or (REPO_ROOT / "biotest_config.yaml")
    cfg = _load_cfg_yaml(cfg_path_original)

    # CRITICAL (2026-04-23): rewrite `phase_c.seeds_dir` in a per-cell
    # temp config so BioTest actually reads the PoV triggers the bench
    # driver built under `seed_corpus` (`_build_merged_seed_corpus`).
    # Without this, biotest.py reads whatever `seeds_dir` the shared
    # `biotest_config.yaml` points at (seeds/) — the same 33 generic
    # files for every cell — and never sees the bug-specific PoV that
    # would trigger the manifest's anchored bug. That's why the v4
    # rerun hit 2/35 real detections: only vcfpy-171/176 whose bugs
    # happen to fire on generic VCF seeds.
    #
    # The merged corpus layout (per DESIGN.md §5.3 + driver's
    # `_build_merged_seed_corpus`):
    #   <seed_corpus>/
    #     <pov_seeds>        — copied from compares/bug_bench/triggers/
    #     <general_seeds>    — filtered from the tool-agnostic seeds/
    # We point BioTest at the format-specific subdir so the PoV file is
    # in-corpus for Phase C's MR iteration.
    # `test_engine.generators.seeds.SeedCorpus` expects
    # `seeds_dir/{vcf,sam}/*.vcf|*.sam`, but the driver builds the
    # per-cell corpus as a flat directory. Materialize a `{vcf,sam}/`
    # wrapper under `out_dir` populated via symlinks so BioTest's
    # globbing actually sees the PoV alongside the general seeds.
    fmt_sub = format_hint.lower()
    wrapper_root = out_dir / "seeds_wrapper"
    wrapper_fmt_dir = wrapper_root / fmt_sub
    wrapper_fmt_dir.mkdir(parents=True, exist_ok=True)
    ext = "." + fmt_sub
    merged_iter = (
        list(seed_corpus.glob(f"*{ext}"))
        if seed_corpus.exists() else []
    )
    # If the merged corpus has a nested fmt subdir (happens when callers
    # pre-flatten to that shape), fall back to glob-rooted there.
    nested = seed_corpus / fmt_sub
    if not merged_iter and nested.exists():
        merged_iter = list(nested.glob(f"*{ext}"))
    for s in merged_iter:
        dst = wrapper_fmt_dir / s.name
        if dst.exists():
            continue
        # `s` is itself a symlink the driver created under seeds_merged;
        # resolve to the real file so the wrapper is a single-hop link
        # (Windows-Docker 9p can't follow chained symlinks reliably —
        # v5 run hit FileNotFoundError on every cell because Phase C
        # tried to read through the seeds_merged link).
        try:
            target = s.resolve()
        except OSError:
            target = s
        try:
            os.symlink(target, dst)
        except OSError:
            try:
                shutil.copy2(target, dst)
            except OSError:
                pass

    cfg_for_run = dict(cfg) if isinstance(cfg, dict) else {}
    phase_c_cfg = dict(cfg_for_run.get("phase_c", {}) or {})
    phase_c_cfg["seeds_dir"] = str(wrapper_root)
    # 2026-04-24: redirect bug_reports to a container-local path OUTSIDE
    # the 9p mount so Windows-Docker bind-mount thrashing doesn't
    # cascade to ENOMEM on data/mr_registry.json opens. The adapter's
    # per-cell snapshot/diff harvest logic is rerooted to this path
    # below via `bug_src`.
    cell_bug_reports = Path("/tmp") / "biotest_bench_reports" / f"cell_{uuid.uuid4().hex[:8]}"
    cell_bug_reports.mkdir(parents=True, exist_ok=True)
    phase_c_cfg["output_dir"] = str(cell_bug_reports)
    cfg_for_run["phase_c"] = phase_c_cfg

    # Mirror data/mr_registry.json and data/det_report.json into
    # /tmp — same reason as bug_reports. biotest.py's Phase C opens the
    # registry early and the 9p mount ENOMEMs out under sustained
    # bench load even when bug_reports writes go to /tmp.
    #
    # 2026-04-25: when BIOTEST_SAM_REGISTRY is set (by the SAM driver
    # script after Phase B), prefer that path over the default. The
    # default path got contaminated mid-run by something we couldn't
    # narrow down (hybrid SAM+VCF state observed in v6); the fixture
    # path is write-once-by-script and never touched again.
    phase_b_cfg = dict(cfg_for_run.get("phase_b", {}) or {})
    sam_fixture_env = os.environ.get("BIOTEST_SAM_REGISTRY")
    if format_hint.upper() == "SAM" and sam_fixture_env and Path(sam_fixture_env).exists():
        original_registry = Path(sam_fixture_env)
    else:
        original_registry = (REPO_ROOT / phase_b_cfg.get(
            "registry_path", "data/mr_registry.json"
        ))
    cell_registry = Path("/tmp") / "biotest_bench_reports" / (
        f"cell_{uuid.uuid4().hex[:8]}" + "_mr_registry.json"
    )
    try:
        if original_registry.exists():
            cell_registry.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original_registry, cell_registry)
            phase_b_cfg["registry_path"] = str(cell_registry)
            cfg_for_run["phase_b"] = phase_b_cfg
    except OSError:
        # If we can't copy (e.g., 9p read also fails), fall back to
        # the original path — at least the cell fails cleanly later.
        pass
    # det_report can also go to /tmp so BioTest doesn't write through
    # the 9p mount.
    phase_c_cfg["det_report_path"] = str(
        Path("/tmp") / "biotest_bench_reports"
        / (f"cell_{uuid.uuid4().hex[:8]}" + "_det_report.json")
    )
    cfg_for_run["phase_c"] = phase_c_cfg
    tmp_cfg_path = out_dir / "biotest_config.cell.yaml"
    try:
        import yaml
        tmp_cfg_path.write_text(yaml.safe_dump(cfg_for_run, sort_keys=False),
                                 encoding="utf-8")
        cfg_path = tmp_cfg_path
    except Exception:
        # If yaml isn't importable, fall back to the original config —
        # the cell won't see PoVs but at least it runs.
        cfg_path = cfg_path_original

    # Phase C bootstrap (SUT init, seed indexing, coverage agent attach)
    # routinely runs 2–5 minutes before the first MR executes, so a sub-
    # 5-minute budget with --phase C never completes. Short budgets fall
    # back to --dry-run, which validates config parsing + CLI plumbing.
    is_smoke = time_budget_s < 300
    cmd = [
        sys.executable,
        str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg_path),
    ]
    if is_smoke:
        cmd.append("--dry-run")
    else:
        cmd.extend(["--phase", "C"])

    # Snapshot bug_reports/ BEFORE the subprocess so we can diff
    # afterwards and harvest only the reports this run produced. Without
    # this snapshot the harvest would copy every historical bug-report
    # directory (50k+ entries from months of prior BioTest runs) into
    # every Phase 4 cell — fixed 2026-04-20 after the unguarded harvest
    # stalled the first full-bench run on 9p-mounted paths.
    # 2026-04-24: bug_reports lives at the cell-local /tmp path set
    # in the temp config above — NOT the 9p-mounted /work default.
    # This sidesteps the Windows-Docker 9p cascade entirely.
    bug_src = cell_bug_reports
    pre_run_entries: set[str] = set()

    ticks = _select_ticks(int(time_budget_s))
    growth: list[dict[str, Any]] = []

    if is_smoke:
        # --dry-run exits in a second or two. No coverage artefacts get
        # written; just record a zero-valued tick row per the schema.
        exit_code = run_subprocess_with_timeout(cmd, log_file, time_budget_s)
        ended = time.time()
        for t_s in ticks:
            growth.append({"t_s": int(t_s), "line_pct": 0.0, "branch_pct": 0.0})
        _emit_growth_json(
            out_dir=out_dir, sut=sut, format_hint=format_hint,
            time_budget_s=int(time_budget_s), growth=growth,
            seed_corpus_hash=_hash_corpus(seed_corpus),
            seed_corpus=seed_corpus, started=started, ended=ended,
            ticks_requested=ticks,
            note=("smoke-mode (--dry-run); biotest does not write "
                  "coverage artefacts under --dry-run, so every tick "
                  "reports 0."),
        )
    else:
        # Launch biotest.py non-blocking so we can poll coverage mid-run.
        # stdout + stderr stream to the same log file (matches the
        # blocking-variant's behaviour in _base.run_subprocess_with_timeout).
        logfh = log_file.open("ab")
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=logfh,
                stderr=subprocess.STDOUT,
                env=os.environ.copy(),
            )
        except Exception as e:
            logfh.close()
            raise RuntimeError(f"failed to launch biotest.py: {e}") from e

        last_reading: tuple[float, float] = (0.0, 0.0)
        # Hard-cap the wait at budget + 30 s grace (same as
        # `run_subprocess_with_timeout`).
        timeout_at = started + int(time_budget_s) + 30

        try:
            for t_s in ticks:
                target_wall = started + t_s
                # Sleep until the tick boundary or early exit
                while time.time() < target_wall:
                    if proc.poll() is not None:
                        break
                    remaining = target_wall - time.time()
                    time.sleep(min(2.0, max(0.1, remaining)))

                line, branch = _tick_snapshot(
                    sut, format_hint, cfg_path, cfg, started, last_reading,
                )
                growth.append({
                    "t_s": int(t_s),
                    "line_pct": round(float(line), 3),
                    "branch_pct": round(float(branch), 3),
                })
                last_reading = (line, branch)

                # If biotest exited early, stop waking up on future
                # ticks — just pad the rest from last_reading below.
                if proc.poll() is not None and time.time() >= target_wall:
                    continue

            # Wait for biotest to fully exit (it may still be running
            # if the last tick equals the budget).
            try:
                remaining = max(0.0, timeout_at - time.time())
                proc.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    try:
                        proc.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        pass
        finally:
            try:
                logfh.close()
            except OSError:
                pass

        exit_code = proc.returncode if proc.returncode is not None else -1
        ended = time.time()

        # Post-exit measurement — some backends only flush their artefact
        # when the biotest subprocess exits (coverage.py via
        # PythonCoverageContext.__exit__, gcovr via `__gcov_dump` at
        # process end). Re-read once more and bump the final tick row if
        # the fresh reading is higher.
        try:
            post_line, post_branch = _tick_snapshot(
                sut, format_hint, cfg_path, cfg, started, last_reading,
            )
            if growth:
                final = growth[-1]
                if post_line > final["line_pct"]:
                    final["line_pct"] = round(float(post_line), 3)
                if post_branch > final["branch_pct"]:
                    final["branch_pct"] = round(float(post_branch), 3)
                last_reading = (
                    max(last_reading[0], post_line),
                    max(last_reading[1], post_branch),
                )
        except Exception:
            pass

        # Fill any missed ticks (e.g., adapter was killed mid-poll) so
        # validate_growth_schema.py sees the full requested set.
        present = {row["t_s"] for row in growth}
        for t_s in ticks:
            if t_s not in present:
                growth.append({
                    "t_s": int(t_s),
                    "line_pct": round(float(last_reading[0]), 3),
                    "branch_pct": round(float(last_reading[1]), 3),
                })
        growth.sort(key=lambda row: row["t_s"])

        _emit_growth_json(
            out_dir=out_dir, sut=sut, format_hint=format_hint,
            time_budget_s=int(time_budget_s), growth=growth,
            seed_corpus_hash=_hash_corpus(seed_corpus),
            seed_corpus=seed_corpus, started=started, ended=ended,
            ticks_requested=ticks,
            note=(
                "Per-tick snapshots of biotest's live coverage "
                "artefact (jacoco.xml / .coverage / gcovr.json / "
                "llvm-cov.json). Biotest writes these at iteration "
                "boundaries (JaCoCo, gcovr), context exit (coverage.py), "
                "or explicit regeneration (llvm-cov) — not "
                "continuously — so early ticks may read 0 until the "
                "first dump. line_pct is propagated forward across "
                "missing samples so the curve stays monotonic."
            ),
        )

    # Harvest only entries that appeared during this run. Each
    # bug_reports/<id>/ dir contains {orig.vcf, T_orig.vcf,
    # canonical_outputs/, evidence.md, logs/, summary.json}. The
    # driver's silence-on-fix replay (§5.3.1) calls
    # runner.run(trig_path, fmt) against a single file, not a dir, so
    # we land only the parseable trigger seed directly under
    # crashes/. Full evidence dirs go to evidence/ alongside so manual
    # triage can still reach them.
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    if bug_src.exists():
        for entry in bug_src.iterdir():
            if entry.name in pre_run_entries:
                continue
            if entry.is_dir():
                # Move the full evidence dir out of crashes_dir.
                evid_dest = evidence_dir / entry.name
                if not evid_dest.exists():
                    shutil.copytree(entry, evid_dest)
                # Land the transformed seed as the trigger file.
                t_seeds = sorted(p for p in entry.iterdir()
                                 if p.is_file() and p.name.startswith("T_"))
                if t_seeds:
                    trig = crashes_dir / f"{entry.name}__{t_seeds[0].name}"
                    if not trig.exists():
                        shutil.copy2(t_seeds[0], trig)
            else:
                dest = crashes_dir / entry.name
                if not dest.exists():
                    shutil.copy2(entry, dest)

    # BioTest's "corpus" is effectively the seed set it fed into MRs +
    # any synthetic seeds produced during Phase D feedback. For the
    # comparison framework we treat the seed directory as the
    # generated corpus. Symlink rather than copy to avoid 9p-mount
    # thrash when the driver is invoked with --out on a bind-mounted
    # volume.
    for seed in seed_corpus.rglob("*"):
        if seed.is_file():
            dest = corpus_dir / seed.name
            if dest.exists():
                continue
            try:
                os.symlink(seed, dest)
            except OSError:
                shutil.copy2(seed, dest)

    # BioTest's crashes_dir entries are directories (bug_reports/<id>/
    # with the JSON + seed + diff inside), so the file-only count_files
    # helper always reports 0. Count any child entry (file OR dir) to
    # capture real detection signal.
    crash_count = (
        sum(1 for _ in crashes_dir.iterdir()) if crashes_dir.exists() else 0
    )

    return AdapterResult(
        tool="biotest",
        sut=sut,
        time_budget_s=time_budget_s,
        started_at=started,
        ended_at=ended,
        corpus_dir=corpus_dir,
        crashes_dir=crashes_dir,
        log_file=log_file,
        generated_count=count_files(corpus_dir),
        crash_count=crash_count,
        exit_code=exit_code,
        notes=("biotest.py CLI does not expose a native --time-budget-s "
               "flag; the budget is enforced by subprocess timeout. "
               "Phase A + B must have run ahead of time so the MR "
               "registry is populated. Per-tick coverage growth written "
               "to growth_<rep>.json at the parent of out_dir."),
        extra={
            "config": str(cfg_path),
            "format": format_hint.upper(),
            "growth_json": str(_growth_parent_dir(out_dir) /
                               f"growth_{_rep_index_from_out_dir(out_dir)}.json"),
            "ticks_sampled": [row["t_s"] for row in growth],
            "final_line_pct": (growth[-1]["line_pct"] if growth else 0.0),
            "final_branch_pct": (growth[-1]["branch_pct"] if growth else 0.0),
        },
    )


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sut", required=True)
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--format", default="VCF")
    p.add_argument("--config", type=Path, default=None)
    args = p.parse_args()

    res = run(
        args.sut, args.seed_corpus, args.out_dir,
        args.time_budget_s, format_hint=args.format, config_path=args.config,
    )
    res.write_manifest(args.out_dir / "adapter_result.json")
    print(f"[biotest] exit={res.exit_code} corpus={res.generated_count} "
          f"crashes={res.crash_count} t={res.duration_s():.0f}s "
          f"line={res.extra.get('final_line_pct', 0.0):.2f}% "
          f"ticks={res.extra.get('ticks_sampled', [])}")


if __name__ == "__main__":
    _cli()
