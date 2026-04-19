"""Shared contract for tool adapters used by the comparative evaluation.

Every adapter exposes a single function:

    run(sut: str, seed_corpus: Path, out_dir: Path,
        time_budget_s: int, **kwargs) -> AdapterResult

`AdapterResult` is the uniform record `coverage_sampler.py` and
`bug_bench_driver.py` consume. Tools that don't report a metric leave it
at its sentinel default.
"""

from __future__ import annotations

import dataclasses
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


@dataclasses.dataclass
class AdapterResult:
    tool: str
    sut: str
    time_budget_s: int
    started_at: float
    ended_at: float
    corpus_dir: Path
    crashes_dir: Path
    log_file: Path
    generated_count: int = -1
    accepted_count: int = -1
    crash_count: int = -1
    exit_code: int = 0
    notes: str = ""
    extra: dict[str, Any] = dataclasses.field(default_factory=dict)

    def duration_s(self) -> float:
        return self.ended_at - self.started_at

    def to_json(self) -> dict[str, Any]:
        d = dataclasses.asdict(self)
        for k in ("corpus_dir", "crashes_dir", "log_file"):
            d[k] = str(d[k])
        return d

    def write_manifest(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_json(), indent=2), encoding="utf-8")


def prepare_out_dir(out_dir: Path) -> tuple[Path, Path, Path]:
    """Create the standard (corpus, crashes, log) tree under out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    corpus = out_dir / "corpus"
    crashes = out_dir / "crashes"
    corpus.mkdir(exist_ok=True)
    crashes.mkdir(exist_ok=True)
    log_file = out_dir / "tool.log"
    log_file.touch(exist_ok=True)
    return corpus, crashes, log_file


def seed_copy(src_corpus: Path, dst_corpus: Path) -> int:
    """Copy every file from src_corpus into dst_corpus (flat). Returns count."""
    if not src_corpus.exists():
        return 0
    n = 0
    for p in src_corpus.rglob("*"):
        if p.is_file():
            shutil.copy2(p, dst_corpus / p.name)
            n += 1
    return n


def run_subprocess_with_timeout(
    cmd: list[str], log_file: Path, time_budget_s: int, env: dict | None = None
) -> int:
    """Run cmd, stream output to log_file, hard-cap at time_budget_s."""
    with log_file.open("ab") as logfh:
        try:
            result = subprocess.run(
                cmd,
                stdout=logfh,
                stderr=subprocess.STDOUT,
                timeout=time_budget_s + 30,
                env=env,
                check=False,
            )
            return result.returncode
        except subprocess.TimeoutExpired:
            return -1


def count_files(directory: Path) -> int:
    if not directory.exists():
        return 0
    return sum(1 for p in directory.iterdir() if p.is_file())
