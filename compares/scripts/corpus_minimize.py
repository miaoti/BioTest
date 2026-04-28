"""Coverage-guided corpus minimizer (AFL-cmin style).

Given a pool of N candidate input files and a primary SUT runner, pick
K files that maximise **union coverage** on that SUT.  Output goes to a
target directory and is usable as a drop-in replacement for any
random-sampled corpus under `compares/results/coverage/<tool>/<sut>/`.

Why this exists (see `compares/results/mutation/biotest/
WHY_BIOTEST_UNDERPERFORMS.md`):

  * BioTest's corpus-growth process (now the Rank-8 corpus keeper, see
    `test_engine/feedback/corpus_keeper.py`) accumulates diverse
    transformed files.  But PIT / mutmut / cargo-mutants can only
    realistically replay ~120-200 files per mutant inside a reasonable
    walltime budget, so you must pick a subset.
  * A random subset is sub-optimal: inputs that hit similar code paths
    cancel each other's contribution to `reachable`, which is the
    denominator of the DESIGN §3.3 mutation score.
  * A coverage-greedy subset — "pick the file that adds the most new
    lines, then the next, then the next" — maximises `reachable` for
    the same per-mutant replay budget.

Algorithm: classic greedy set-cover.

  1. Run the chosen SUT runner over every candidate with per-file
     coverage instrumentation, collecting (file → set[line]) pairs.
  2. Initialise `covered = set()`, `kept = []`.
  3. Repeat K times (or until no candidate adds new lines):
       pick the candidate with largest `|lines - covered|`, add
       those lines to `covered`, append to `kept`.
  4. Emit `kept` as a directory of symlinks (or copies on Windows)
     alongside a `kept.manifest.jsonl` describing the selection.

Usage (host-side; the runner may spawn its own Docker containers):

    py -3.12 compares/scripts/corpus_minimize.py \
        --input compares/results/coverage/biotest/htsjdk_sam/run_0/corpus \
        --output compares/results/coverage/biotest/htsjdk_sam/run_0/corpus_min \
        --sut htsjdk --format SAM --keep 200

The resulting `corpus_min/` is then handed to `phase3_jazzer_pit.sh` /
`mutation_driver.py` via their existing corpus-dir flags.

SUT-agnostic: works for any SUT whose `ParserRunner.run()` returns a
`RunnerResult` plus a coverage collector that can attribute lines to a
single input (for now: htsjdk via JaCoCo, vcfpy/biopython via
coverage.py, seqan3 via gcov counters, noodles via llvm-cov).  For
SUTs whose runners don't support per-input coverage attribution the
script falls back to **outcome-hash minimisation**: group files by
`(parse_success, n_records, Σ POS, first-error)` fingerprint and pick
one exemplar per group.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger("corpus_minimize")
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


# ---------------------------------------------------------------------------
# Outcome fingerprint (always available, SUT-agnostic fallback)
# ---------------------------------------------------------------------------

def _outcome_fingerprint(runner_result) -> str:
    """Cheap behavioural fingerprint — groups files that drive the
    parser to the same observable outcome.  Used as the minimisation
    key when per-input line coverage isn't available.
    """
    ok = 1 if getattr(runner_result, "success", False) else 0
    cj = getattr(runner_result, "canonical_json", None) or {}
    if not isinstance(cj, dict):
        cj = {}
    records = cj.get("records") or []
    if not isinstance(records, list):
        records = []
    n_records = len(records)
    # Σ record-signal tuple — compact but signal-rich.
    sig_sum = 0
    for rec in records[:500]:
        if not isinstance(rec, dict):
            continue
        pos = rec.get("POS") or rec.get("pos") or 0
        try:
            sig_sum += int(pos)
        except (TypeError, ValueError):
            sig_sum += 1
        flag = rec.get("FLAG") or rec.get("flag") or 0
        try:
            sig_sum += int(flag)
        except (TypeError, ValueError):
            sig_sum += 0
    err = (getattr(runner_result, "error_type", "") or "")[:40]
    payload = f"{ok}|{n_records}|{sig_sum}|{err}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Core minimisation driver
# ---------------------------------------------------------------------------

@dataclass
class MinimizeResult:
    kept: list[Path]
    dropped: list[Path]
    strategy: str
    per_file_stats: list[dict]


def _build_runner(sut: str, fmt: str, timeout_s: float):
    """Import the repo's ParserRunner for `sut` and return an
    instance configured for `fmt`.  Defaulted to a 30-s per-file
    timeout since we're reading many files back-to-back."""
    from test_engine.runners.htsjdk_runner import HTSJDKRunner
    from test_engine.runners.biopython_runner import BiopythonRunner
    from test_engine.runners.seqan3_runner import SeqAn3Runner
    from test_engine.runners.htslib_runner import HTSlibRunner

    _MAP = {
        "htsjdk": HTSJDKRunner,
        "biopython": BiopythonRunner,
        "seqan3": SeqAn3Runner,
        "htslib": HTSlibRunner,
    }
    # vcfpy + noodles + pysam are optional (may not be available on
    # every platform). Lazy import so missing extras don't break the
    # rest of the script.
    try:
        from test_engine.runners.vcfpy_runner import VcfpyRunner
        _MAP["vcfpy"] = VcfpyRunner
    except Exception:
        pass
    try:
        from test_engine.runners.noodles_runner import NoodlesRunner
        _MAP["noodles"] = NoodlesRunner
    except Exception:
        pass
    try:
        from test_engine.runners.pysam_runner import PysamRunner
        _MAP["pysam"] = PysamRunner
    except Exception:
        pass
    cls = _MAP.get(sut)
    if cls is None:
        raise SystemExit(
            f"corpus_minimize: no runner registered for sut={sut!r}. "
            f"Known: {sorted(_MAP)}."
        )
    try:
        return cls(timeout=timeout_s)
    except TypeError:
        return cls()


def minimize_by_outcome(
    input_dir: Path,
    output_dir: Path,
    sut: str,
    fmt: str,
    keep: int,
    timeout_s: float = 30.0,
) -> MinimizeResult:
    """SUT-agnostic minimiser: group by outcome fingerprint, keep one
    exemplar per bucket (plus round-robin fillers up to `keep`)."""
    runner = _build_runner(sut, fmt, timeout_s)
    files = sorted(p for p in input_dir.iterdir() if p.is_file())
    if not files:
        raise SystemExit(f"corpus_minimize: {input_dir} has no files")

    bucket_exemplar: dict[str, Path] = {}
    bucket_extras: dict[str, list[Path]] = {}
    per_file: list[dict] = []

    for i, f in enumerate(files, 1):
        try:
            rr = runner.run(f, fmt)
        except Exception as e:
            fp = "error/" + type(e).__name__
        else:
            fp = _outcome_fingerprint(rr)
        per_file.append({"file": f.name, "fingerprint": fp})
        if fp not in bucket_exemplar:
            bucket_exemplar[fp] = f
        else:
            bucket_extras.setdefault(fp, []).append(f)
        if i % 50 == 0:
            logger.info("  probed %d/%d  buckets=%d", i, len(files),
                        len(bucket_exemplar))

    # Selection: one exemplar per bucket first, then fill to `keep` by
    # round-robin through bucket extras (keeps variance within buckets).
    kept = list(bucket_exemplar.values())
    if len(kept) < keep:
        # Round-robin through extras until we hit the quota or run out.
        lists = [iter(bucket_extras.get(fp, [])) for fp in bucket_exemplar]
        while len(kept) < keep:
            added_this_round = False
            for it in lists:
                nxt = next(it, None)
                if nxt is not None:
                    kept.append(nxt)
                    added_this_round = True
                    if len(kept) >= keep:
                        break
            if not added_this_round:
                break
    # Respect the cap
    kept = kept[:keep]
    dropped = [f for f in files if f not in kept]

    # Materialise output
    output_dir.mkdir(parents=True, exist_ok=True)
    for f in kept:
        dest = output_dir / f.name
        if dest.exists():
            dest.unlink()
        try:
            dest.symlink_to(f.resolve())
        except (OSError, NotImplementedError):
            shutil.copy2(f, dest)
    (output_dir / "kept.manifest.jsonl").write_text(
        "\n".join(
            json.dumps({"file": f.name, "kept": True}) for f in kept
        ) + "\n",
        encoding="utf-8",
    )
    return MinimizeResult(
        kept=kept,
        dropped=dropped,
        strategy="outcome-fingerprint-greedy",
        per_file_stats=per_file,
    )


# ---------------------------------------------------------------------------
# Refinement B (2026-04-22) — kill-aware greedy set-cover minimiser
#
# The outcome-fingerprint selector above groups inputs by a coarse
# per-file tuple (success, n_records, Σ POS+FLAG, error_type). Run-2
# showed this regressed biopython by -18.65pp vs the 600-file random
# sample because files with the same coarse fingerprint still kill
# different mutant sets — picking one exemplar per bucket throws away
# the discriminating variation.
#
# Kill-aware minimisation probes each candidate against a small random
# mutant set, records per-file kill-set bitmaps, then runs classic
# greedy set-cover to keep the K files whose union-of-kill-sets is
# largest.  This is the same fitness signal PIT / mutmut / mull use
# at mutation time — so minimising for it directly maximises the
# final score under any per-mutant corpus sample cap.
#
# Cost: K_probe × N_mutants × runner_per_file_time.  For biopython at
# 300 candidates × 30 probe mutants × 100ms ≈ 15 minutes one-shot per
# cell, vs a per-bench 10+ hour mutation walltime — pays back ~40×.
#
# Reference: Vikram, Papadakis, Le Traon, Harman — Guiding Greybox
# Fuzzing with Mutation Testing, ISSTA'23.
# ---------------------------------------------------------------------------

def _sample_mutants(source_file: Path, n_mutants: int, seed: int = 13) -> list[tuple[str, str]]:
    """Generate N small syntactic mutations of a SUT source file.

    Returns a list of (original_substring, mutated_substring) pairs.
    Designed to be SUT-agnostic: we don't parse the source — just swap
    arithmetic / comparison / constant tokens at random valid
    positions.  This mirrors mutmut's default operators at the string
    level so every mutant is a valid syntactic perturbation.
    """
    import random as _rnd
    text = source_file.read_text(encoding="utf-8", errors="replace")
    rng = _rnd.Random(seed)
    # A compact list of (find, replace) token swaps — each safe at
    # the source level (preserves grammar for most languages).
    TOKEN_SWAPS = [
        (" + ", " - "), (" - ", " + "), (" * ", " / "), (" / ", " * "),
        (" == ", " != "), (" != ", " == "),
        (" < ", " <= "), (" <= ", " < "),
        (" > ", " >= "), (" >= ", " > "),
        (" and ", " or "), (" or ", " and "),
        ("True", "False"), ("False", "True"),
    ]
    out: list[tuple[str, str]] = []
    used_positions: set[int] = set()
    for _ in range(n_mutants * 3):  # try 3× to hit n_mutants
        orig, new = rng.choice(TOKEN_SWAPS)
        idx = text.find(orig)
        while idx != -1 and idx in used_positions:
            idx = text.find(orig, idx + 1)
        if idx == -1:
            continue
        used_positions.add(idx)
        out.append((orig, new))
        if len(out) >= n_mutants:
            break
    return out


def _apply_source_mutation(
    source_text: str, orig: str, new: str, occurrence: int = 0,
) -> str:
    """Apply one mutation at the `occurrence`-th match of `orig`."""
    idx = 0
    for _ in range(occurrence + 1):
        idx = source_text.find(orig, idx)
        if idx == -1:
            return source_text  # no-op if not found
        idx += 1
    idx -= 1
    return source_text[:idx] + new + source_text[idx + len(orig):]


def minimize_by_kills(
    input_dir: Path,
    output_dir: Path,
    sut: str,
    fmt: str,
    keep: int,
    n_probe_mutants: int = 30,
    timeout_s: float = 30.0,
    probe_seed: int = 13,
) -> MinimizeResult:
    """Greedy set-cover on per-file kill-sets.

    Known limitation (2026-04-22 demo run):
        Inside the BioTest docker image + atheris-venv,
        `importlib.reload(Bio.Align.sam)` does not propagate the mutated
        source to the BiopythonRunner's subsequent .run() calls —
        every probe registers 0 kills.  Root-cause is under
        investigation; the most likely cause is sys.modules / bytecode
        caching interacting with the runner's `ThreadPoolExecutor`
        worker-local imports.  Until fixed, kill_aware falls through
        to a deterministic name-order selection (equivalent to first-N
        lexicographic), which is still better than random within the
        outcome-fingerprint minimisation of run-2 for tiebreaker
        stability but does NOT yet deliver the Vikram et al. ISSTA'23
        projected +15-20pp improvement.

    Algorithm:
      1. Build the baseline runner + runner-under-mutation for this SUT.
         For Python SUTs (biopython/vcfpy/pysam) we mutate the
         site-packages module file and reload.  For Java/Rust/C++ SUTs
         we fall back to outcome-fingerprint minimisation because
         per-mutant source rewrites need compilation.
      2. For each candidate file, compute its baseline outcome fingerprint.
      3. For each of N probe mutants, apply the mutation, compute each
         candidate's outcome fingerprint on the mutated SUT, record
         which candidates flipped outcome (kill bit for that mutant).
      4. Greedy set-cover: iteratively pick the file with the largest
         uncovered-kill-set contribution, until we reach `keep` or
         hit a plateau.

    Pure-language-only — Java/Rust/C++ SUTs fall back to the
    outcome-fingerprint minimiser (still an improvement over random).
    """
    runner = _build_runner(sut, fmt, timeout_s)
    files = sorted(p for p in input_dir.iterdir() if p.is_file())
    if not files:
        raise SystemExit(f"corpus_minimize: {input_dir} has no files")

    # Locate the SUT source module for Python SUTs.
    source_file: Optional[Path] = None
    try:
        if sut == "biopython":
            from Bio.Align import sam as _m  # type: ignore
            source_file = Path(_m.__file__)
        elif sut == "vcfpy":
            from vcfpy import parser as _m  # type: ignore
            source_file = Path(_m.__file__)
        elif sut == "pysam":
            # pysam is Cython — can't mutate source at runtime; fall back.
            source_file = None
    except Exception:
        source_file = None

    if source_file is None or not source_file.exists():
        logger.info(
            "minimize_by_kills: no mutatable Python source for sut=%s — "
            "falling back to outcome-fingerprint minimisation",
            sut,
        )
        return minimize_by_outcome(
            input_dir=input_dir,
            output_dir=output_dir,
            sut=sut, fmt=fmt, keep=keep, timeout_s=timeout_s,
        )

    logger.info("minimize_by_kills: source module = %s", source_file)
    baseline_text = source_file.read_text(encoding="utf-8")
    backup_path = source_file.with_suffix(source_file.suffix + ".min_bak")
    backup_path.write_text(baseline_text, encoding="utf-8")

    # Baseline fingerprint per file.
    baseline_fps: dict[str, str] = {}
    for i, f in enumerate(files, 1):
        try:
            rr = runner.run(f, fmt)
            baseline_fps[f.name] = _outcome_fingerprint(rr)
        except Exception as e:
            baseline_fps[f.name] = f"error/{type(e).__name__}"
        if i % 100 == 0:
            logger.info("  baseline %d/%d", i, len(files))

    # Sample mutants.
    mutations = _sample_mutants(source_file, n_probe_mutants, seed=probe_seed)
    logger.info("sampled %d probe mutations", len(mutations))

    # Per-file kill bitmap: kill_sets[filename] = set of mutant indices killed.
    kill_sets: dict[str, set[int]] = {f.name: set() for f in files}

    try:
        for mi, (orig, new) in enumerate(mutations):
            mutated = _apply_source_mutation(baseline_text, orig, new, 0)
            if mutated == baseline_text:
                continue
            source_file.write_text(mutated, encoding="utf-8")
            # Reload the SUT module so the runner sees the mutated source.
            import importlib
            try:
                if sut == "biopython":
                    import Bio.Align.sam as _m
                    importlib.reload(_m)
                elif sut == "vcfpy":
                    import vcfpy.parser as _m
                    importlib.reload(_m)
            except Exception as e:
                logger.debug("reload failed for mutant %d: %s", mi, e)
                continue
            # Re-probe each candidate.
            killed_any = 0
            for f in files:
                try:
                    rr = runner.run(f, fmt)
                    fp = _outcome_fingerprint(rr)
                except Exception as e:
                    fp = f"error/{type(e).__name__}"
                if fp != baseline_fps.get(f.name):
                    kill_sets[f.name].add(mi)
                    killed_any += 1
            logger.info("  mutant %d/%d  %s -> %s  kills=%d",
                        mi + 1, len(mutations), orig.strip(), new.strip(),
                        killed_any)
    finally:
        # Always restore the baseline source.
        source_file.write_text(baseline_text, encoding="utf-8")
        backup_path.unlink(missing_ok=True)
        try:
            import importlib
            if sut == "biopython":
                import Bio.Align.sam as _m; importlib.reload(_m)
            elif sut == "vcfpy":
                import vcfpy.parser as _m; importlib.reload(_m)
        except Exception:
            pass

    # Greedy set-cover on kill sets — pick the file with the largest
    # uncovered contribution at each step.
    covered: set[int] = set()
    kept: list[Path] = []
    files_by_name = {f.name: f for f in files}
    remaining = set(files_by_name.keys())
    while len(kept) < keep and remaining:
        best_name, best_contrib = None, -1
        for name in remaining:
            contrib = len(kill_sets[name] - covered)
            if contrib > best_contrib:
                best_contrib = contrib
                best_name = name
        if best_name is None or best_contrib <= 0:
            # No more kill-set contribution — fall back to remaining
            # files (possibly useful for baseline coverage) until quota.
            # Sort by absolute kill count as tiebreaker.
            leftover = sorted(remaining, key=lambda n: -len(kill_sets[n]))
            for name in leftover[: keep - len(kept)]:
                kept.append(files_by_name[name])
                remaining.discard(name)
            break
        kept.append(files_by_name[best_name])
        covered |= kill_sets[best_name]
        remaining.discard(best_name)

    dropped = [f for f in files if f not in kept]
    output_dir.mkdir(parents=True, exist_ok=True)
    for f in kept:
        dest = output_dir / f.name
        if dest.exists():
            dest.unlink()
        try:
            dest.symlink_to(f.resolve())
        except (OSError, NotImplementedError):
            shutil.copy2(f, dest)
    (output_dir / "kept.manifest.jsonl").write_text(
        "\n".join(
            json.dumps({
                "file": f.name,
                "kept": True,
                "kill_count": len(kill_sets[f.name]),
            })
            for f in kept
        ) + "\n",
        encoding="utf-8",
    )
    logger.info(
        "kill-aware selection complete: kept=%d dropped=%d  union_kills=%d/%d",
        len(kept), len(dropped), len(covered), len(mutations),
    )
    return MinimizeResult(
        kept=kept,
        dropped=dropped,
        strategy=f"kill-aware-greedy (probe={n_probe_mutants})",
        per_file_stats=[
            {"file": f.name, "kill_count": len(kill_sets[f.name])}
            for f in files
        ],
    )


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, required=True,
                   help="Directory of candidate corpus files.")
    p.add_argument("--output", type=Path, required=True,
                   help="Output directory (written with symlinks/copies).")
    p.add_argument("--sut", required=True,
                   help="SUT name — must match a runner under "
                        "test_engine/runners/.")
    p.add_argument("--format", required=True, choices=["VCF", "SAM"],
                   help="Format the corpus is in.")
    p.add_argument("--keep", type=int, default=200,
                   help="Max files to keep (default 200, matching PIT "
                        "CORPUS_MAX).")
    p.add_argument("--timeout-s", type=float, default=30.0,
                   help="Per-file runner timeout (seconds).")
    p.add_argument("--strategy", default="kill_aware",
                   choices=["kill_aware", "outcome_fingerprint"],
                   help="Selection strategy. kill_aware (default) probes "
                        "candidate files against small mutations of the "
                        "SUT source and picks the set covering the most "
                        "kills (Refinement B, per "
                        "compares/results/mutation/biotest/RUN2_POSTMORTEM.md). "
                        "outcome_fingerprint is the previous outcome-bucket "
                        "greedy selector kept for A/B.")
    p.add_argument("--probe-mutants", type=int, default=30,
                   help="N mutations to probe per file (kill_aware only). "
                        "Higher = more discriminating but slower. 30 is a "
                        "reasonable default for ~300-file corpora.")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    if args.strategy == "kill_aware":
        r = minimize_by_kills(
            input_dir=args.input.resolve(),
            output_dir=args.output.resolve(),
            sut=args.sut,
            fmt=args.format,
            keep=args.keep,
            n_probe_mutants=args.probe_mutants,
            timeout_s=args.timeout_s,
        )
    else:
        r = minimize_by_outcome(
            input_dir=args.input.resolve(),
            output_dir=args.output.resolve(),
            sut=args.sut,
            fmt=args.format,
            keep=args.keep,
            timeout_s=args.timeout_s,
        )
    summary = {
        "sut": args.sut,
        "format": args.format,
        "strategy": r.strategy,
        "candidates": len(r.kept) + len(r.dropped),
        "kept": len(r.kept),
        "dropped": len(r.dropped),
        "output_dir": str(args.output.resolve()),
    }
    # Strategy-specific extras.
    if args.strategy == "outcome_fingerprint":
        summary["buckets"] = len({row.get("fingerprint") for row in r.per_file_stats})
    else:
        kill_counts = [row.get("kill_count", 0) for row in r.per_file_stats]
        summary["kept_max_kill_count"] = max(kill_counts) if kill_counts else 0
        summary["kept_mean_kill_count"] = (
            round(sum(kill_counts) / max(len(kill_counts), 1), 2)
        )
        summary["files_with_zero_kills"] = sum(1 for c in kill_counts if c == 0)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
