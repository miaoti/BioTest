"""Coverage-growth corpus keeper.

DESIGN — addresses the Phase-3 diagnostic (`compares/results/mutation/biotest/
WHY_BIOTEST_UNDERPERFORMS.md`): coverage-guided fuzzers (jazzer, atheris,
libfuzzer, cargo-fuzz) grow their corpus *during* the run — every input
that hits a new edge gets kept, every other input is thrown away.  After
a long run the kept corpus is a fitness-selected set rich in edge
cases.  BioTest historically deleted every transformed file at
`transformed_path.unlink()` and never benefited from the byte-level
diversity the semantics-preserving transforms produce.

The keeper hooks into `orchestrator._run_single_test` and, before the
unlink, saves any transformed input that **at least one** parser runner
accepted (`RunnerResult.success`) to `seeds/<fmt>/kept_<sha8>.{vcf,sam}`.
The next `SeedCorpus()` instantiation picks these up via the same
`glob("*.vcf")` / `glob("*.sam")` the existing Tier-1 / Tier-2 seeds use,
so downstream Phase B/C/D code needs no changes.

Why this works in one pass without adding per-input coverage
instrumentation:

  * BioTest's transforms are *semantics-preserving*, so every
    successfully-parsing transformed file is BY CONSTRUCTION a valid
    input for the SUT — no validity filtering needed.
  * Content-SHA dedup guarantees that identical transforms don't
    inflate the pool.
  * FIFO eviction caps the pool size and rotates in fresh material
    across iterations.
  * Every future Phase-D iteration's LLM / Hypothesis / static
    executor draws from the expanded `seeds/<fmt>/` glob — the
    feedback loop closes automatically.

The keeper is intentionally coverage-*free* at hook time (no per-input
instrumentation): the *next* Phase-D iteration's aggregate coverage
measurement is where the selection-pressure shows up, and that's the
measurement we already compute.  This keeps hot-path cost ~1ms per
transformed file (one `sha256` + one `shutil.copy2`), which matters
because `_run_single_test` is inside the Hypothesis inner loop.

Generalisation: the keeper is SUT-agnostic — it uses the `fmt` scope
string already in every MR dict, and `RunnerResult.success` is the
universal "did this runner accept it" flag every runner implements.
Adding a new SUT / new format costs zero keeper changes.
"""
from __future__ import annotations

import hashlib
import json
import logging
import shutil
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Optional

logger = logging.getLogger(__name__)

_DEFAULT_MAX_FILES_PER_FORMAT = 2000
_FILENAME_PREFIX = "kept_"
_MANIFEST_FILENAME = ".kept_manifest.jsonl"


@dataclass
class KeepDecision:
    """What the keeper did with one call — returned for logging/telemetry."""
    kept: bool = False
    path: Optional[Path] = None
    reason: str = ""
    dedup_hash: str = ""


@dataclass
class CorpusKeeper:
    """Append-only, content-hash-deduped, FIFO-capped corpus keeper.

    Thread-safe: wraps disk ops in a single RLock so Hypothesis'
    parallel example draws don't race.

    Directory layout:
        <seeds_dir>/vcf/kept_<sha8>.vcf      # same dir SeedCorpus globs
        <seeds_dir>/vcf/.kept_manifest.jsonl # not *.vcf so not picked up
        <seeds_dir>/sam/kept_<sha8>.sam
        <seeds_dir>/sam/.kept_manifest.jsonl
    """
    seeds_dir: Path
    enabled: bool = True
    max_files_per_format: int = _DEFAULT_MAX_FILES_PER_FORMAT
    # Internal — initialised in __post_init__.
    _seen_hashes: dict[str, set[str]] = field(default_factory=dict, repr=False)
    _seen_canonical: dict[str, set[str]] = field(default_factory=dict, repr=False)
    _lock: threading.RLock = field(default_factory=threading.RLock, repr=False)
    _kept_this_session: int = 0
    _skipped_duplicate: int = 0
    _skipped_ast_dup: int = 0
    # Coverage-guided culling support (Rank 8b, 2026-04-30): track the
    # files kept since the last `reset_iteration_tracking()` so the
    # post-Phase-C culler can measure each one's per-file coverage and
    # delete those that didn't add new lines vs the prior corpus.
    _kept_paths_this_iteration: list[Path] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if not self.enabled:
            return
        self.seeds_dir.mkdir(parents=True, exist_ok=True)
        for fmt in ("vcf", "sam"):
            fmt_dir = self.seeds_dir / fmt
            fmt_dir.mkdir(parents=True, exist_ok=True)
            self._seen_hashes[fmt] = set()
            self._seen_canonical[fmt] = set()
            # Re-populate the dedup sets from whatever's already on disk
            # so running the tool twice in a row doesn't re-save the
            # same content under a new filename. We recover byte-hashes
            # from filenames; canonical-hashes are read from the
            # manifest lines.
            for p in fmt_dir.glob(f"{_FILENAME_PREFIX}*.{fmt}"):
                h = p.stem[len(_FILENAME_PREFIX):]
                self._seen_hashes[fmt].add(h)
            manifest = fmt_dir / _MANIFEST_FILENAME
            if manifest.exists():
                import json as _json
                for ln in manifest.read_text(encoding="utf-8").splitlines():
                    if not ln.strip():
                        continue
                    try:
                        rec = _json.loads(ln)
                    except _json.JSONDecodeError:
                        continue
                    ch = rec.get("canonical_hash")
                    if ch:
                        self._seen_canonical[fmt].add(ch)

    # ----- public API ------------------------------------------------------

    def maybe_keep(
        self,
        transformed_path: Path,
        fmt: str,
        mr_id: str,
        source_seed: Optional[Path] = None,
        any_runner_success: bool = True,
        canonical_json_hash: Optional[str] = None,
        source_canonical_hash: Optional[str] = None,
    ) -> KeepDecision:
        """Decide whether to keep a transformed file and persist if so.

        Eligibility (all must hold):
          * keeper is enabled;
          * `any_runner_success` is True (at least one runner parsed it);
          * file still exists and is non-empty;
          * content hash is not already in the kept set;
          * Refinement A (2026-04-22): if `canonical_json_hash` is provided,
            it must differ from every already-kept canonical-hash for this
            format AND (if `source_canonical_hash` is provided) it must
            differ from the source seed's canonical hash. This rejects
            inputs that are byte-distinct but parse to the identical AST
            (classic `shuffle_meta_lines` case). Without this gate, a
            semantics-preserving MR deposits N byte-variants that add
            zero `reachable` to the PIT/mutmut denominator.
          * pool is under the per-format cap (or we can FIFO-evict).

        `canonical_json_hash` is a short sha256 of the primary SUT's
        `RunnerResult.canonical_json` (orchestrator computes it). When
        absent we fall back to byte-hash-only dedup for backward
        compatibility.
        """
        if not self.enabled:
            return KeepDecision(reason="keeper_disabled")
        if not any_runner_success:
            return KeepDecision(reason="no_runner_accepted")
        fmt_l = fmt.lower()
        if fmt_l not in ("vcf", "sam"):
            return KeepDecision(reason=f"unsupported_format:{fmt_l}")
        try:
            raw = transformed_path.read_bytes()
        except OSError as e:
            return KeepDecision(reason=f"read_error:{e.__class__.__name__}")
        if not raw:
            return KeepDecision(reason="empty_file")

        sha8 = hashlib.sha256(raw).hexdigest()[:16]
        with self._lock:
            if sha8 in self._seen_hashes[fmt_l]:
                self._skipped_duplicate += 1
                return KeepDecision(kept=False, dedup_hash=sha8, reason="duplicate")

            # Refinement A — canonical-AST-diff gating.
            if canonical_json_hash:
                if (source_canonical_hash
                        and canonical_json_hash == source_canonical_hash):
                    self._skipped_ast_dup += 1
                    return KeepDecision(
                        kept=False, dedup_hash=sha8,
                        reason="canonical_ast_equals_source",
                    )
                if canonical_json_hash in self._seen_canonical[fmt_l]:
                    self._skipped_ast_dup += 1
                    return KeepDecision(
                        kept=False, dedup_hash=sha8,
                        reason="canonical_ast_already_kept",
                    )

            fmt_dir = self.seeds_dir / fmt_l
            self._enforce_cap(fmt_dir, fmt_l)

            dest = fmt_dir / f"{_FILENAME_PREFIX}{sha8}.{fmt_l}"
            try:
                dest.write_bytes(raw)
            except OSError as e:
                return KeepDecision(
                    kept=False,
                    dedup_hash=sha8,
                    reason=f"write_error:{e.__class__.__name__}",
                )
            self._seen_hashes[fmt_l].add(sha8)
            if canonical_json_hash:
                self._seen_canonical[fmt_l].add(canonical_json_hash)
            self._kept_this_session += 1
            self._kept_paths_this_iteration.append(dest)
            self._append_manifest(fmt_dir, {
                "sha": sha8,
                "path": dest.name,
                "mr_id": mr_id,
                "source_seed": source_seed.name if source_seed else None,
                "kept_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "bytes": len(raw),
                "canonical_hash": canonical_json_hash,
            })
            return KeepDecision(kept=True, path=dest, dedup_hash=sha8, reason="new")

    # ----- coverage-guided culling (Rank 8b, 2026-04-30) -------------------

    def reset_iteration_tracking(self) -> None:
        """Forget the per-iteration kept-file list.

        Call at the start of each Phase D iteration so
        ``cull_by_coverage`` only sees this iteration's additions, not
        cumulative since process start.
        """
        with self._lock:
            self._kept_paths_this_iteration = []

    def get_kept_this_iteration(self) -> list[Path]:
        """Snapshot of files kept since the last reset (for tests/diagnostics)."""
        with self._lock:
            return list(self._kept_paths_this_iteration)

    def cull_by_coverage(
        self,
        measure_lines: Callable[[Path], frozenset[tuple[str, int]]],
        baseline_lines: Optional[frozenset[tuple[str, int]]] = None,
        log_decisions: bool = True,
    ) -> dict:
        """Delete kept files that didn't add new coverage lines.

        For each file kept since the last ``reset_iteration_tracking()``:
          1. call ``measure_lines(path)`` to get the (file, line) tuples
             the primary SUT executed when parsing it;
          2. compute ``new = lines - accumulated``;
          3. if ``new`` is empty, ``unlink`` the file from disk and
             remove it from the keeper's dedup state;
          4. otherwise, fold ``new`` into ``accumulated`` and keep it.

        Why this is the "Zest-style filter" the README hints at: the
        plain ``maybe_keep`` retains a file whenever **at least one
        runner accepted** it, which keeps a lot of byte-distinct
        derivatives that hit the same code paths as their parents. This
        method retroactively removes those duplicates by replaying each
        kept file through the primary SUT under coverage tracking and
        only retaining files that contribute at least one previously-
        unseen line.

        Args:
            measure_lines: Callback that runs the primary SUT on a single
                file and returns a frozenset of (source_file, line_number)
                tuples. The frozenset shape lets tests inject mock
                coverage easily; production callers build it via
                ``test_engine.feedback.coverage_culler``.
            baseline_lines: Optional coverage that already existed
                BEFORE this iteration's kept-file additions (e.g. from
                the curated + previously-kept corpus). Files that only
                cover a subset of this set are culled. ``None`` =
                empty — order-dependent culling within the iteration's
                additions only.
            log_decisions: emit one ``logger.info`` per file with the
                kept/culled outcome. Off when called from tight test
                loops that don't want log noise.

        Returns:
            ``{"total": int, "kept": int, "culled": int,
              "baseline_size": int, "final_size": int}``.

        Thread-safety: snapshots the kept-list under the keeper's lock,
        then releases it for the (potentially slow) ``measure_lines``
        calls. State mutations after that re-acquire the lock.
        """
        with self._lock:
            paths = list(self._kept_paths_this_iteration)
            self._kept_paths_this_iteration = []

        accum: set[tuple[str, int]] = (
            set(baseline_lines) if baseline_lines is not None else set()
        )
        baseline_size = len(accum)
        kept: list[Path] = []
        culled: list[Path] = []

        for p in paths:
            if not p.exists():
                # Already gone (e.g. FIFO eviction during the iteration).
                continue
            try:
                hit = measure_lines(p)
            except Exception as e:
                # Defensive: a measurement failure must NOT delete a
                # file. Keep it and log; the next iteration may succeed.
                logger.warning(
                    "cull_by_coverage: measure_lines failed for %s "
                    "(%s); keeping the file",
                    p.name, e,
                )
                kept.append(p)
                continue

            new = hit - accum
            if not new:
                # No new coverage — cull.
                self._delete_kept_file(p)
                culled.append(p)
                if log_decisions:
                    logger.info(
                        "cull_by_coverage: deleted %s "
                        "(0 new lines vs accumulated=%d)",
                        p.name, len(accum),
                    )
            else:
                accum |= new
                kept.append(p)
                if log_decisions:
                    logger.info(
                        "cull_by_coverage: kept %s "
                        "(+%d lines; accumulated=%d)",
                        p.name, len(new), len(accum),
                    )

        return {
            "total": len(paths),
            "kept": len(kept),
            "culled": len(culled),
            "baseline_size": baseline_size,
            "final_size": len(accum),
        }

    def _delete_kept_file(self, path: Path) -> None:
        """Remove a kept file from disk AND from the dedup state.

        Order is deliberate: drop the dedup hash UNDER the lock FIRST,
        then ``unlink`` outside the lock. The opposite order would open
        a TOCTOU window where the file is gone but the byte-hash is
        still present, so a concurrent ``maybe_keep`` of identical
        bytes would skip writing thinking the dup was already on disk.

        Best-effort — a missing file or stale state must not raise. The
        canonical-hash set is NOT touched: we kept the file because its
        canonical AST was novel; the byte-distinct dedup is what we
        invalidate so a future identical bytes input can be re-tried.
        """
        fmt_l = path.parent.name  # "vcf" or "sam" by directory layout
        sha8: Optional[str] = None
        if path.stem.startswith(_FILENAME_PREFIX):
            sha8 = path.stem[len(_FILENAME_PREFIX):]
        if sha8 is not None:
            with self._lock:
                self._seen_hashes.get(fmt_l, set()).discard(sha8)
        try:
            path.unlink()
        except OSError:
            pass

    # ----- introspection ---------------------------------------------------

    def stats(self) -> dict[str, int | dict[str, int]]:
        with self._lock:
            return {
                "enabled": self.enabled,
                "max_files_per_format": self.max_files_per_format,
                "kept_this_session": self._kept_this_session,
                "skipped_duplicate": self._skipped_duplicate,
                "skipped_ast_dup": self._skipped_ast_dup,
                "pool_size": {fmt: len(s) for fmt, s in self._seen_hashes.items()},
                "canonical_buckets": {
                    fmt: len(s) for fmt, s in self._seen_canonical.items()
                },
            }

    # ----- internals -------------------------------------------------------

    def _enforce_cap(self, fmt_dir: Path, fmt_l: str) -> None:
        """FIFO-evict the oldest kept files once we exceed the cap.

        Stat mtime is used as the rough arrival-time signal — cheaper
        than threading a per-entry timestamp manifest, and "oldest
        file loses" is the only policy worth implementing here.
        """
        pool = sorted(
            fmt_dir.glob(f"{_FILENAME_PREFIX}*.{fmt_l}"),
            key=lambda p: p.stat().st_mtime,
        )
        overflow = len(pool) - (self.max_files_per_format - 1)
        if overflow <= 0:
            return
        for victim in pool[:overflow]:
            try:
                victim.unlink()
            except OSError:
                continue
            self._seen_hashes[fmt_l].discard(
                victim.stem[len(_FILENAME_PREFIX):]
            )
            logger.debug("corpus_keeper evicted %s", victim.name)

    def _append_manifest(self, fmt_dir: Path, row: dict) -> None:
        try:
            with (fmt_dir / _MANIFEST_FILENAME).open(
                "a", encoding="utf-8"
            ) as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        except OSError:
            # Manifest is informational; a write failure should not
            # break the keep decision.
            pass


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

def from_config(
    cfg: dict,
    seeds_dir: Path,
) -> CorpusKeeper:
    """Build a CorpusKeeper from the `phase_c.corpus_keeper` config block.

    Default is *enabled*: the keeper costs ~1 ms per MR execution and
    pays back across iterations.  To disable, set:

        phase_c:
          corpus_keeper:
            enabled: false

    or tune:

        phase_c:
          corpus_keeper:
            enabled: true                # default true
            max_files_per_format: 2000   # default 2000 per (vcf, sam)
    """
    phase_c_cfg = cfg.get("phase_c", {}) if isinstance(cfg, dict) else {}
    ck_cfg = phase_c_cfg.get("corpus_keeper", {}) or {}
    return CorpusKeeper(
        seeds_dir=seeds_dir,
        enabled=bool(ck_cfg.get("enabled", True)),
        max_files_per_format=int(
            ck_cfg.get("max_files_per_format", _DEFAULT_MAX_FILES_PER_FORMAT)
        ),
    )
