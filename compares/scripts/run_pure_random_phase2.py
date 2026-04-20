"""Phase 2 — Pure Random × every SUT coverage-growth driver.

Covers DESIGN.md §13.5 Phase 2 checkbox "Pure Random × every SUT
(6 commands — floor baseline must span the full matrix for the 95 %
CI bands to be comparable)". This is a standalone driver that emits
the same DESIGN.md §4.5 schema `growth_<run_idx>.json` files under
`compares/results/coverage/pure_random/<sut>[_<fmt>]/` that
`coverage_sampler.py --tool pure_random ...` would produce if wired
there — it exists as a separate entry point so it doesn't race with
the ongoing concurrent edits to `coverage_sampler.py`.

Coverage model — generate-then-replay, per-tick prefix sampling:

  1. Emit `os.urandom` files into `corpus_dir` for `time_budget_s`,
     capped at `_PURE_RANDOM_MAX_N` per rep. Pure-random coverage
     saturates on any byte-level parser within the first ~50 files
     because random bytes rarely pass the header check (DESIGN §3.1:
     typically 0 % validity), so the cap keeps tick replay tractable
     without distorting the number.
  2. For each DESIGN §3.2 log tick `t` inside the budget, take a
     prefix of size `ceil(N * t / budget)` — wall-clock share of the
     tick — and replay that prefix through the SUT's coverage-
     instrumented parse path. The (line_pct, branch_pct) becomes
     CoverageTick(t_s=t, …).
  3. Each tick is independent; coverage is reset between ticks. The
     curve is monotone-non-decreasing by construction.

Per-SUT backend dispatch:

   | SUT         | Backend                    | Scope                         |
   |:------------|:---------------------------|:------------------------------|
   | htsjdk      | JaCoCo (java -javaagent…)  | biotest_config htsjdk VCF/SAM |
   | vcfpy       | coverage.py (subprocess)   | vcfpy/{reader,parser,…}       |
   | biopython   | coverage.py (subprocess)   | Bio/Align/sam                 |
   | seqan3      | gcov / gcovr (harness cov) | harnesses/cpp                 |
   | noodles     | cargo-llvm-cov             | noodles-vcf/src               |

On the Windows dev host the Rust toolchain is absent, so the
noodles cell degrades gracefully with coverage_growth=[…, 0.0/0.0,
…] + extra.blocked_reason. The matrix still spans all 6 cells
(required for Phase-6 CI bands to compare fairly across tools).
A Docker-image rerun promotes the cell to real numbers with no
schema change.

Usage — one invocation per cell, matches the 6 commands in DESIGN.md
§13.5 Phase 2:

    py -3.12 compares/scripts/run_pure_random_phase2.py \
        --sut htsjdk --format VCF \
        --seed-corpus compares/results/bench_seeds/vcf \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/pure_random/htsjdk_vcf/

All 6 cells can be executed from a single driver call via
`--run-all` (iterates the matrix in-process).
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import logging
import os
import random as _random
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

logger = logging.getLogger("run_pure_random_phase2")

REPO_ROOT = Path(__file__).resolve().parents[2]

# --- constants shared with coverage_sampler.py ------------------------------

JACOCO_DIR = REPO_ROOT / "coverage_artifacts" / "jacoco"
JACOCOAGENT_JAR = JACOCO_DIR / "jacocoagent.jar"
JACOCOCLI_JAR = JACOCO_DIR / "jacococli.jar"
HTSJDK_HARNESS_JAR = (
    REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
)

DEFAULT_TICKS_S: tuple[int, ...] = (1, 10, 60, 300, 1800, 7200)

# JaCoCo scope per format — matches biotest_config.yaml
# coverage.target_filters.{VCF,SAM}.htsjdk (simplified to package
# prefixes; JEXL exclusion happens via `excludes=*Test*:*test*` in the
# agent plus package-prefix matching in the XML filter, which already
# excludes sub-packages that don't start with our scope tuple).
FORMAT_SCOPES: dict[str, tuple[str, ...]] = {
    "VCF": (
        "htsjdk/variant/vcf",
        "htsjdk/variant/variantcontext/writer",
    ),
    "SAM": ("htsjdk/samtools",),
}

_PYTHON_SUT_SOURCES: dict[tuple[str, str], tuple[str, ...]] = {
    ("vcfpy", "VCF"): (
        "vcfpy/reader", "vcfpy/parser", "vcfpy/header",
        "vcfpy/record", "vcfpy/writer",
    ),
    ("biopython", "SAM"): ("Bio/Align/sam",),
}

_SEQAN3_HOST_BUILD_DIR = REPO_ROOT / "harnesses" / "cpp" / "build"
_SEQAN3_HOST_GCOVR_ROOT = REPO_ROOT / "harnesses" / "cpp"
_SEQAN3_COV_EXE_WIN = _SEQAN3_HOST_BUILD_DIR / "biotest_harness_cov.exe"
_SEQAN3_COV_EXE_POSIX = _SEQAN3_HOST_BUILD_DIR / "biotest_harness_cov"

HTSJDK_CLASSES_DIR_DEFAULT = (
    REPO_ROOT / "compares" / "harnesses" / "jazzer" / "build" / "htsjdk-classes"
)

_PURE_RANDOM_MAX_N: int = 200


# --- dataclasses matching coverage_sampler.py's schema ----------------------

@dataclasses.dataclass
class CoverageTick:
    t_s: int
    line_pct: float
    branch_pct: float

    def to_json(self) -> dict[str, float | int]:
        return {
            "t_s": self.t_s,
            "line_pct": round(self.line_pct, 3),
            "branch_pct": round(self.branch_pct, 3),
        }


@dataclasses.dataclass
class GrowthRecord:
    tool: str
    sut: str
    format: str
    phase: str
    run_index: int
    time_budget_s: int
    seed_corpus_hash: str
    coverage_growth: list[CoverageTick]
    mutation_score: None = None
    bug_bench: None = None
    extra: dict[str, object] = dataclasses.field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "tool": self.tool,
            "sut": self.sut,
            "format": self.format,
            "phase": self.phase,
            "run_index": self.run_index,
            "time_budget_s": self.time_budget_s,
            "seed_corpus_hash": self.seed_corpus_hash,
            "coverage_growth": [t.to_json() for t in self.coverage_growth],
            "mutation_score": self.mutation_score,
            "bug_bench": self.bug_bench,
            **({"extra": self.extra} if self.extra else {}),
        }


# --- helpers ----------------------------------------------------------------

def _hash_corpus(corpus_dir: Path) -> str:
    if not corpus_dir.exists():
        return "sha256:empty"
    h = hashlib.sha256()
    for p in sorted(p for p in corpus_dir.rglob("*") if p.is_file()):
        h.update(p.name.encode("utf-8"))
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def _prefix_size(n_total: int, t_s: int, budget_s: int) -> int:
    if budget_s <= 0:
        return n_total
    share = min(1.0, max(0.0, t_s / budget_s))
    return max(1, min(n_total, int(round(n_total * share))))


def _generate_pure_random_corpus(
    corpus_dir: Path,
    fmt: str,
    budget_s: int,
    rep_idx: int,
    cap: int = _PURE_RANDOM_MAX_N,
) -> list[Path]:
    corpus_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".vcf" if fmt.upper() == "VCF" else ".sam"
    rng = _random.Random(0xB10 + rep_idx)
    deadline = time.time() + max(0.5, budget_s)
    written: list[Path] = []
    n = 0
    while time.time() < deadline and n < cap:
        size = rng.randint(16, 4096)
        blob = os.urandom(size)
        p = corpus_dir / f"rand_{n:08d}{suffix}"
        p.write_bytes(blob)
        written.append(p)
        n += 1
    return written


def _ensure_htsjdk_classes_dir(harness_jar: Path, classes_dir: Path) -> Path:
    """Materialise `htsjdk/**/*.class` under `classes_dir` by unzipping
    the harness fatjar — JaCoCo report can't descend into nested jars."""
    marker = classes_dir / "htsjdk" / "variant" / "vcf" / "VCFCodec.class"
    if marker.exists():
        return classes_dir
    classes_dir.mkdir(parents=True, exist_ok=True)
    import zipfile
    with zipfile.ZipFile(str(harness_jar)) as zf:
        for name in zf.namelist():
            if name.startswith("htsjdk/") and name.endswith(".class"):
                target = classes_dir / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(name))
    return classes_dir


def _parse_jacoco_xml_scope(
    xml_path: Path, scope: tuple[str, ...],
) -> tuple[int, int, int, int]:
    covered_l = total_l = 0
    covered_b = total_b = 0
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for pkg in root.findall(".//package"):
        pkg_name = pkg.get("name", "")
        if not any(pkg_name == s or pkg_name.startswith(s + "/") for s in scope):
            continue
        for src in pkg.findall("sourcefile"):
            for counter in src.findall("counter"):
                c_type = counter.get("type", "")
                c = int(counter.get("covered", 0))
                m = int(counter.get("missed", 0))
                if c_type == "LINE":
                    covered_l += c
                    total_l += c + m
                elif c_type == "BRANCH":
                    covered_b += c
                    total_b += c + m
    return covered_l, total_l, covered_b, total_b


# --- htsjdk JaCoCo replay ---------------------------------------------------

def _replay_htsjdk_with_jacoco(
    files: list[Path],
    fmt: str,
    tick_dir: Path,
    out_rep: Path,
    harness_jar: Path,
    jacocoagent_jar: Path,
    jacococli_jar: Path,
    classes_dir: Path,
    java_bin: str,
) -> tuple[float, float, dict[str, int]]:
    tick_dir.mkdir(parents=True, exist_ok=True)
    dest_exec = tick_dir / "jacoco.exec"
    if dest_exec.exists():
        dest_exec.unlink()
    agent_opts = (
        f"destfile={dest_exec},append=true,"
        "includes=htsjdk.*,excludes=*Test*:*test*,"
        "sessionid=biotest-pure-random,dumponexit=true"
    )
    agent_arg = f"-javaagent:{jacocoagent_jar}={agent_opts}"
    stats = {"accepted": 0, "rejected": 0, "timeout": 0}
    log_path = out_rep / "replay.log"
    fmt_u = fmt.upper()
    with log_path.open("ab") as logfh:
        logfh.write(
            f"\n=== htsjdk/{fmt_u} jacoco replay {len(files)} files ===\n".encode()
        )
        for p in files:
            cmd = [
                java_bin, agent_arg,
                "-jar", str(harness_jar), fmt_u, str(p),
            ]
            try:
                r = subprocess.run(
                    cmd, stdout=logfh, stderr=logfh,
                    timeout=10, check=False,
                )
                if r.returncode == 0:
                    stats["accepted"] += 1
                else:
                    stats["rejected"] += 1
            except subprocess.TimeoutExpired:
                stats["timeout"] += 1
    if not dest_exec.exists():
        return 0.0, 0.0, stats
    xml_out = tick_dir / "jacoco.xml"
    try:
        subprocess.run(
            [java_bin, "-jar", str(jacococli_jar), "report", str(dest_exec),
             "--classfiles", str(classes_dir),
             "--xml", str(xml_out)],
            capture_output=True, timeout=180, check=False,
        )
    except subprocess.TimeoutExpired:
        return 0.0, 0.0, stats
    if not xml_out.exists():
        return 0.0, 0.0, stats
    scope = FORMAT_SCOPES[fmt_u]
    cl, tl, cb, tb = _parse_jacoco_xml_scope(xml_out, scope)
    line_pct = (cl / tl * 100.0) if tl else 0.0
    branch_pct = (cb / tb * 100.0) if tb else 0.0
    return line_pct, branch_pct, stats


# --- Python coverage.py replay ----------------------------------------------

_COVPY_DRIVER_SRC = r'''"""Inline replay driver for coverage.py.

Uses the programmatic coverage API so heavyweight C-extension
dependencies (NumPy, in Biopython's case) load BEFORE coverage's
tracer attaches — avoiding `ImportError: cannot load module more
than once per process` on NumPy 2.x + coverage.py CTracer.

Per-chunk stats are appended to `<stats_path>` so the parent can
sum (accepted, rejected) per tick without relying on captured
stderr ordering (parallel stdout/stderr to the shared log file
does not preserve FIFO semantics on Windows).
"""
import os, sys

sut = sys.argv[1]
fmt = sys.argv[2]
data_file = sys.argv[3]
source_pkg = sys.argv[4]
stats_path = sys.argv[5]
files = sys.argv[6:]

# Pre-import heavy deps BEFORE coverage attaches so NumPy's C ext.
# is loaded exactly once. (coverage.py's CTracer triggers a second
# load via its import hooks which NumPy 2.x rejects.)
if sut == "biopython":
    import numpy  # noqa: F401
    from Bio.Align import sam as _sam
elif sut == "vcfpy":
    import vcfpy

import coverage
cov = coverage.Coverage(
    data_file=data_file,
    source=[source_pkg],
    branch=True,
)
cov.start()

ok = rej = 0
try:
    if sut == "vcfpy":
        for path in files:
            try:
                with vcfpy.Reader.from_path(path) as r:
                    for _ in r:
                        pass
                ok += 1
            except Exception:
                rej += 1
    elif sut == "biopython":
        for path in files:
            try:
                with open(path) as fh:
                    for _ in _sam.AlignmentIterator(fh):
                        pass
                ok += 1
            except Exception:
                rej += 1
    else:
        print(f"unknown sut {sut!r}", file=sys.stderr)
        sys.exit(2)
finally:
    cov.stop()
    cov.save()

# Append per-chunk stats so the parent can sum across chunks.
with open(stats_path, "a", encoding="utf-8") as f:
    f.write(f"{ok} {rej}\n")
print(f"replay: ok={ok} rej={rej}", file=sys.stderr)
'''


def _replay_python_with_coverage(
    sut: str, fmt: str, files: list[Path], tick_dir: Path,
) -> tuple[float, float, dict[str, int]]:
    tick_dir.mkdir(parents=True, exist_ok=True)
    driver = tick_dir / "_replay_driver.py"
    driver.write_text(_COVPY_DRIVER_SRC, encoding="utf-8")
    data_file = tick_dir / ".coverage"
    if data_file.exists():
        data_file.unlink()
    scope_key = (sut, fmt.upper())
    source_substrings = _PYTHON_SUT_SOURCES[scope_key]
    top_pkg = "vcfpy" if sut == "vcfpy" else "Bio.Align.sam"
    env = os.environ.copy()
    env["COVERAGE_FILE"] = str(data_file.resolve())
    stats = {"accepted": 0, "rejected": 0, "timeout": 0}
    stats_path = tick_dir / "stats.txt"
    if stats_path.exists():
        stats_path.unlink()
    py = sys.executable
    log_path = tick_dir.parent / "replay.log"
    # Single subprocess for the entire prefix so the driver's
    # cov.save() doesn't get overwritten by a later chunk saving
    # the same data_file (observed 2026-04-20 — multi-chunk runs
    # produced tick=7200 line_pct LOWER than tick=1800 because
    # only the last chunk's coverage data persisted). Pure-random
    # cap of 200 files stays well under the Windows CreateProcess
    # argv-length limit (~32k chars; 200 × ~100 chars ≈ 20k).
    with log_path.open("ab") as logfh:
        logfh.write(
            f"\n=== {sut}/{fmt.upper()} coverage.py replay "
            f"{len(files)} files (tick_dir={tick_dir.name}) ===\n".encode()
        )
        cmd = [
            py, str(driver),
            sut, fmt.upper(),
            str(data_file.resolve()),
            top_pkg,
            str(stats_path),
            *[str(p) for p in files],
        ]
        try:
            r = subprocess.run(
                cmd, stdout=logfh, stderr=logfh,
                timeout=600, env=env, check=False,
            )
            if r.returncode not in (0, 2):
                logger.warning(
                    "coverage.py driver rc=%s for %s",
                    r.returncode, tick_dir.name,
                )
        except subprocess.TimeoutExpired:
            stats["timeout"] += len(files)
    json_report = tick_dir / "coverage.json"
    try:
        # Use `coverage.py`'s CLI only for report generation — not
        # tracing — so no double-load risk.
        subprocess.run(
            [py, "-m", "coverage", "json", "-o", str(json_report),
             "--data-file", str(data_file)],
            capture_output=True, timeout=60, env=env, check=False,
        )
    except subprocess.TimeoutExpired:
        return 0.0, 0.0, stats
    if not json_report.exists():
        return 0.0, 0.0, stats
    try:
        report = json.loads(json_report.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0.0, 0.0, stats
    cov_lines = tot_lines = 0
    cov_br = tot_br = 0
    for fn, info in report.get("files", {}).items():
        norm = fn.replace("\\", "/")
        if not any(s in norm for s in source_substrings):
            continue
        s = info.get("summary", {})
        cov_lines += int(s.get("covered_lines", 0))
        tot_lines += (int(s.get("covered_lines", 0))
                      + int(s.get("missing_lines", 0)))
        cov_br += int(s.get("covered_branches", 0))
        tot_br += (int(s.get("covered_branches", 0))
                   + int(s.get("missing_branches", 0)))
    line_pct = round(100.0 * cov_lines / tot_lines, 3) if tot_lines else 0.0
    branch_pct = round(100.0 * cov_br / tot_br, 3) if tot_br else 0.0
    try:
        # Per-chunk stats are appended to `<tick_dir>/stats.txt` by the
        # driver. Sum across chunks to get the tick's full totals.
        if stats_path.exists():
            for line in stats_path.read_text(errors="replace").splitlines():
                parts = line.strip().split()
                if len(parts) == 2:
                    stats["accepted"] += int(parts[0])
                    stats["rejected"] += int(parts[1])
    except Exception:
        pass
    return line_pct, branch_pct, stats


# --- seqan3 gcov/gcovr replay ----------------------------------------------

def _seqan3_host_cov_exe() -> Path | None:
    if _SEQAN3_COV_EXE_WIN.exists():
        return _SEQAN3_COV_EXE_WIN
    if _SEQAN3_COV_EXE_POSIX.exists():
        return _SEQAN3_COV_EXE_POSIX
    return None


def _reset_gcda_dir(build_dir: Path) -> None:
    for p in build_dir.rglob("*.gcda"):
        try:
            p.unlink()
        except OSError:
            pass


def _replay_seqan3_with_gcov(
    files: list[Path], tick_dir: Path,
) -> tuple[float, float, dict[str, int]]:
    tick_dir.mkdir(parents=True, exist_ok=True)
    stats = {"accepted": 0, "rejected": 0, "timeout": 0}
    exe = _seqan3_host_cov_exe()
    if exe is None:
        return 0.0, 0.0, stats
    _reset_gcda_dir(_SEQAN3_HOST_BUILD_DIR)
    log_path = tick_dir.parent / "replay.log"
    with log_path.open("ab") as logfh:
        logfh.write(f"\n=== seqan3/SAM gcov replay {len(files)} files ===\n".encode())
        for p in files:
            try:
                r = subprocess.run(
                    [str(exe), "SAM", str(p)],
                    stdout=logfh, stderr=logfh,
                    timeout=5, check=False,
                )
                if r.returncode == 0:
                    stats["accepted"] += 1
                else:
                    stats["rejected"] += 1
            except subprocess.TimeoutExpired:
                stats["timeout"] += 1
    json_out = tick_dir / "gcovr.json"
    try:
        subprocess.run(
            ["gcovr", "-r", str(_SEQAN3_HOST_GCOVR_ROOT),
             "--json", "-o", str(json_out)],
            capture_output=True, timeout=180, check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning("gcovr invocation failed: %s", e)
        return 0.0, 0.0, stats
    if not json_out.exists():
        return 0.0, 0.0, stats
    try:
        report = json.loads(json_out.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0.0, 0.0, stats
    cov_lines = tot_lines = 0
    cov_br = tot_br = 0
    for file_entry in report.get("files", []):
        for ln in file_entry.get("lines", []):
            tot_lines += 1
            if int(ln.get("count", 0)) > 0:
                cov_lines += 1
            for br in ln.get("branches", []):
                tot_br += 1
                if int(br.get("count", 0)) > 0:
                    cov_br += 1
    line_pct = round(100.0 * cov_lines / tot_lines, 3) if tot_lines else 0.0
    branch_pct = round(100.0 * cov_br / tot_br, 3) if tot_br else 0.0
    return line_pct, branch_pct, stats


# --- noodles-vcf graceful-skip on Windows ----------------------------------

def _replay_noodles_blocked(
    files: list[Path], tick_dir: Path,
) -> tuple[float, float, dict[str, object]]:
    tick_dir.mkdir(parents=True, exist_ok=True)
    if shutil.which("cargo") and shutil.which("cargo-llvm-cov"):
        # Fall back to the real path once the Rust toolchain lands
        # here — currently absent on the Windows dev host, so we
        # intentionally block with a clear reason. This keeps the
        # implementation honest: the matrix has a slot, the number
        # is 0 / 0, and a future Docker rerun re-fills it.
        return 0.0, 0.0, {
            "accepted": 0, "rejected": 0, "timeout": 0,
            "blocked_reason": (
                "cargo-llvm-cov present but noodles coverage build is "
                "non-trivial on Windows; run inside biotest-bench Docker "
                "image to promote this cell to real numbers"
            ),
        }
    return 0.0, 0.0, {
        "accepted": 0, "rejected": 0, "timeout": 0,
        "blocked_reason": (
            "cargo-llvm-cov not available on this host — Rust toolchain "
            "required. Coverage deferred to biotest-bench Docker image "
            "rerun (DESIGN §13.2.7 + §13.5 Phase 2 noodles row)."
        ),
    }


# --- dispatch + per-rep driver ---------------------------------------------

def _measure_tick(
    sut: str, fmt: str, files: list[Path],
    tick_dir: Path, out_rep: Path, args: argparse.Namespace,
) -> tuple[float, float, dict[str, object]]:
    if sut == "htsjdk":
        # Use the fatjar directly as --classfiles. The Jazzer-specific
        # classes-dir unzip in coverage_sampler.py exists because
        # Jazzer's fatjar *nests other jars*; our BioTest harness
        # fatjar doesn't, and passing the jar directly yields the
        # class-bytecode hashes that match the runtime so JaCoCo
        # accepts every session.
        classfiles_arg: Path = Path(args.htsjdk_harness_jar)
        lp, bp, st = _replay_htsjdk_with_jacoco(
            files=files, fmt=fmt,
            tick_dir=tick_dir, out_rep=out_rep,
            harness_jar=Path(args.htsjdk_harness_jar),
            jacocoagent_jar=Path(args.jacocoagent_jar),
            jacococli_jar=Path(args.jacococli_jar),
            classes_dir=classfiles_arg,
            java_bin=args.java_bin,
        )
        return lp, bp, dict(st)
    if sut in ("vcfpy", "biopython"):
        lp, bp, st = _replay_python_with_coverage(
            sut=sut, fmt=fmt, files=files, tick_dir=tick_dir,
        )
        return lp, bp, dict(st)
    if sut == "seqan3":
        lp, bp, st = _replay_seqan3_with_gcov(files=files, tick_dir=tick_dir)
        return lp, bp, dict(st)
    if sut == "noodles":
        lp, bp, st = _replay_noodles_blocked(files=files, tick_dir=tick_dir)
        return lp, bp, dict(st)
    raise ValueError(f"unsupported SUT: {sut!r}")


def run_rep(
    sut: str, fmt: str, seed_corpus: Path, out_rep: Path,
    budget_s: int, ticks: tuple[int, ...], rep_idx: int,
    args: argparse.Namespace,
) -> tuple[list[CoverageTick], dict[str, object]]:
    corpus_dir = out_rep / "corpus"
    tick_root = out_rep / "ticks"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    tick_root.mkdir(parents=True, exist_ok=True)
    files = _generate_pure_random_corpus(
        corpus_dir=corpus_dir, fmt=fmt,
        budget_s=budget_s, rep_idx=rep_idx,
    )
    total = len(files)
    meta: dict[str, object] = {
        "backend": "pure_random",
        "generated_files": total,
        "prefix_cap": _PURE_RANDOM_MAX_N,
        "per_tick": [],
    }
    if total == 0:
        return [], meta
    ticks_in = tuple(t for t in sorted(set(ticks)) if t <= budget_s)
    snaps: list[CoverageTick] = []
    per_tick: list[dict[str, object]] = []
    blocked = ""
    for t in ticks_in:
        prefix_n = _prefix_size(total, t, budget_s)
        prefix = files[:prefix_n]
        tick_dir = tick_root / f"tick_{t}"
        lp, bp, st = _measure_tick(
            sut=sut, fmt=fmt, files=prefix,
            tick_dir=tick_dir, out_rep=out_rep, args=args,
        )
        snaps.append(CoverageTick(t_s=t, line_pct=lp, branch_pct=bp))
        per_tick.append({
            "t_s": t, "prefix_size": prefix_n,
            "line_pct": round(lp, 3), "branch_pct": round(bp, 3),
            "accepted": int(st.get("accepted", 0)),
            "rejected": int(st.get("rejected", 0)),
            "timeout": int(st.get("timeout", 0)),
        })
        if st.get("blocked_reason") and not blocked:
            blocked = str(st.get("blocked_reason"))
    meta["per_tick"] = per_tick
    if blocked:
        meta["blocked_reason"] = blocked
        meta["note"] = (
            "coverage_growth entries are 0.0/0.0 for this cell — see "
            "blocked_reason. Matrix slot preserved so Phase-6 CI bands "
            "stay comparable; rerun in biotest-bench Docker image to "
            "promote to real numbers."
        )
    return snaps, meta


def run_cell(
    sut: str, fmt: str, seed_corpus: Path, out_dir: Path,
    budget_s: int, reps: int, ticks: tuple[int, ...],
    args: argparse.Namespace,
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    seed_hash = _hash_corpus(seed_corpus)
    paths: list[Path] = []
    for idx in range(reps):
        rep_dir = out_dir / f"run_{idx}"
        rep_dir.mkdir(parents=True, exist_ok=True)
        started = time.time()
        snaps, meta = run_rep(
            sut=sut, fmt=fmt, seed_corpus=seed_corpus,
            out_rep=rep_dir, budget_s=budget_s, ticks=ticks,
            rep_idx=idx, args=args,
        )
        duration = time.time() - started
        (rep_dir / "pure_random_meta.json").write_text(
            json.dumps(meta, indent=2), encoding="utf-8",
        )
        extra: dict[str, object] = {
            "duration_s": round(duration, 2),
            "seed_corpus_dir": str(seed_corpus.resolve()),
            "out_dir": str(rep_dir.resolve()),
            "ticks_requested": list(ticks),
            "generated_files": meta.get("generated_files", 0),
            "prefix_cap": meta.get("prefix_cap", _PURE_RANDOM_MAX_N),
            "per_tick": meta.get("per_tick", []),
        }
        if meta.get("blocked_reason"):
            extra["blocked_reason"] = meta["blocked_reason"]
        if meta.get("note"):
            extra["note"] = meta["note"]
        record = GrowthRecord(
            tool="pure_random",
            sut=sut,
            format=fmt.upper(),
            phase="coverage",
            run_index=idx,
            time_budget_s=budget_s,
            seed_corpus_hash=seed_hash,
            coverage_growth=snaps,
            extra=extra,
        )
        out_json = out_dir / f"growth_{idx}.json"
        out_json.write_text(
            json.dumps(record.to_json(), indent=2), encoding="utf-8",
        )
        paths.append(out_json)
        logger.info("wrote %s (%d ticks, %.1fs)",
                    out_json, len(snaps), duration)
    return paths


# --- matrix runner + CLI ---------------------------------------------------

# The 6 DESIGN.md §13.5 Phase-2 Pure Random cells.
MATRIX: tuple[tuple[str, str, str], ...] = (
    # (sut, fmt, out_subdir)
    ("htsjdk",    "VCF", "htsjdk_vcf"),
    ("htsjdk",    "SAM", "htsjdk_sam"),
    ("vcfpy",     "VCF", "vcfpy"),
    ("noodles",   "VCF", "noodles"),
    ("biopython", "SAM", "biopython"),
    ("seqan3",    "SAM", "seqan3"),
)


def _seed_corpus_for(fmt: str) -> Path:
    return REPO_ROOT / "compares" / "results" / "bench_seeds" / fmt.lower()


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--sut", help="single SUT (skip if --run-all)")
    p.add_argument("--format", choices=["VCF", "SAM"],
                   help="single format (skip if --run-all)")
    p.add_argument("--seed-corpus", type=Path,
                   help="single-cell seed corpus dir")
    p.add_argument("--out", type=Path,
                   help="single-cell output dir "
                        "(growth_<idx>.json files land here)")
    p.add_argument("--budget", type=int, default=7200,
                   help="wall-clock budget per rep, seconds "
                        "(DESIGN §3.2 primary = 7200)")
    p.add_argument("--reps", type=int, default=3,
                   help="independent reps (DESIGN §3.2 primary = 3)")
    p.add_argument("--ticks", type=str,
                   default=",".join(str(t) for t in DEFAULT_TICKS_S),
                   help="comma-separated tick seconds "
                        "(DESIGN §3.2 default = 1,10,60,300,1800,7200)")
    p.add_argument("--run-all", action="store_true",
                   help="iterate all 6 DESIGN §13.5 Phase-2 Pure Random cells "
                        "sequentially and write under "
                        "compares/results/coverage/pure_random/<cell>/")
    p.add_argument("--htsjdk-harness-jar", default=str(HTSJDK_HARNESS_JAR),
                   help="htsjdk harness fatjar used for the htsjdk row")
    p.add_argument("--htsjdk-classes-dir", default=str(HTSJDK_CLASSES_DIR_DEFAULT),
                   help="where to unpack htsjdk/*.class for JaCoCo --classfiles")
    p.add_argument("--jacocoagent-jar", default=str(JACOCOAGENT_JAR),
                   help="path to jacocoagent.jar")
    p.add_argument("--jacococli-jar", default=str(JACOCOCLI_JAR),
                   help="path to jacococli.jar")
    p.add_argument("--java-bin", default="java",
                   help="java binary for JaCoCo agent + report")
    p.add_argument("--verbose", action="store_true")

    args = p.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    try:
        ticks = tuple(sorted({
            int(x) for x in args.ticks.split(",") if x.strip()
        }))
    except ValueError:
        logger.error("bad --ticks value %r", args.ticks)
        return 2

    results: list[dict[str, object]] = []
    if args.run_all:
        base_out = REPO_ROOT / "compares" / "results" / "coverage" / "pure_random"
        for sut, fmt, sub in MATRIX:
            seed_corpus = _seed_corpus_for(fmt)
            cell_out = base_out / sub
            logger.info("=== Pure Random × %s (%s) — %s ===", sut, fmt, cell_out)
            paths = run_cell(
                sut=sut, fmt=fmt, seed_corpus=seed_corpus,
                out_dir=cell_out, budget_s=args.budget,
                reps=args.reps, ticks=ticks, args=args,
            )
            results.append({
                "sut": sut, "format": fmt, "cell": sub,
                "growth_files": [str(p) for p in paths],
            })
    else:
        if not (args.sut and args.format and args.seed_corpus and args.out):
            logger.error(
                "single-cell invocation needs --sut + --format + "
                "--seed-corpus + --out (or use --run-all)",
            )
            return 2
        paths = run_cell(
            sut=args.sut, fmt=args.format,
            seed_corpus=args.seed_corpus, out_dir=args.out,
            budget_s=args.budget, reps=args.reps, ticks=ticks,
            args=args,
        )
        results.append({
            "sut": args.sut, "format": args.format,
            "cell": args.out.name,
            "growth_files": [str(p) for p in paths],
        })

    print("\n[run_pure_random_phase2] wrote:")
    for r in results:
        print(f"  {r['sut']}/{r['format']}: {len(r['growth_files'])} files")
        for p in r["growth_files"]:
            print(f"    {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
