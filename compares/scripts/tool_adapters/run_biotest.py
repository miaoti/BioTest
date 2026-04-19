"""BioTest adapter — invokes the main BioTest pipeline's Phase C.

The adapter contract is "run for N seconds, capture whatever the tool
produced, report exit status." Since `biotest.py` has no native time
budget flag, we enforce the budget via subprocess timeout (SIGTERM on
the wrapper, then SIGKILL on the timer) — same pattern every other
adapter uses.

Assumptions (documented in §13.2.1 of compares/DESIGN.md):
- Phase A + B have run already. `data/mr_registry.json` exists.
- `biotest_config.yaml` in the repo root has `phase_c.suts` configured
  for the target SUT; we don't synthesize config on the fly.
- BioTest's output lives at its usual paths (`bug_reports/`,
  `data/det_report.json`, `coverage_artifacts/`). We capture those by
  symlinking / copying after the run rather than rerouting stdio.
"""

from __future__ import annotations

import os
import shutil
import sys
import time
from pathlib import Path
import argparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _base import (  # noqa: E402
    AdapterResult,
    prepare_out_dir,
    run_subprocess_with_timeout,
    count_files,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


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

    cfg = config_path or (REPO_ROOT / "biotest_config.yaml")
    # Phase C bootstrap (SUT init, seed indexing, coverage agent attach)
    # routinely runs 2–5 minutes before the first MR executes, so a sub-
    # 5-minute budget with --phase C never completes. Short budgets fall
    # back to --dry-run, which validates config parsing + CLI plumbing.
    is_smoke = time_budget_s < 300
    cmd = [
        sys.executable,
        str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg),
    ]
    if is_smoke:
        cmd.append("--dry-run")
    else:
        cmd.extend(["--phase", "C"])
    exit_code = run_subprocess_with_timeout(cmd, log_file, time_budget_s)
    ended = time.time()

    # BioTest writes outputs to repo-relative paths. Harvest them into
    # the adapter's out_dir so downstream phases (validity probe,
    # coverage sampler) see a uniform layout.
    bug_src = REPO_ROOT / "bug_reports"
    if bug_src.exists():
        for entry in bug_src.iterdir():
            dest = crashes_dir / entry.name
            if not dest.exists():
                if entry.is_dir():
                    shutil.copytree(entry, dest)
                else:
                    shutil.copy2(entry, dest)

    # BioTest's "corpus" is effectively the seed set it fed into MRs +
    # any synthetic seeds produced during Phase D feedback. For the
    # comparison framework we treat the seed directory as the
    # generated corpus.
    for seed in seed_corpus.rglob("*"):
        if seed.is_file():
            dest = corpus_dir / seed.name
            if not dest.exists():
                shutil.copy2(seed, dest)

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
        crash_count=count_files(crashes_dir),
        exit_code=exit_code,
        notes=("biotest.py CLI does not expose a native --time-budget-s "
               "flag; the budget is enforced by subprocess timeout. "
               "Phase A + B must have run ahead of time so the MR "
               "registry is populated."),
        extra={"config": str(cfg), "format": format_hint.upper()},
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
          f"crashes={res.crash_count} t={res.duration_s():.0f}s")


if __name__ == "__main__":
    _cli()
