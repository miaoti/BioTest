r"""Phase-2 coverage-growth sampler (DESIGN.md §3.2, §4.5, §13.5 Phase 2).

For a single (tool, SUT, format) cell this script runs the configured
fuzzer for the requested wall-clock budget `--reps` times and emits one
`growth_<run_idx>.json` per rep under the output directory, matching the
DESIGN.md §4.5 schema:

    {
      "tool":            "jazzer",
      "sut":             "htsjdk",
      "format":          "VCF" | "SAM",
      "phase":           "coverage",
      "run_index":       0,
      "time_budget_s":   7200,
      "seed_corpus_hash": "sha256:...",
      "coverage_growth": [
        {"t_s": 1,    "line_pct": 1.9, "branch_pct": 0.8},
        {"t_s": 10,   "line_pct": 18.4, "branch_pct": 12.1},
        ...
        {"t_s": 7200, "line_pct": 46.2, "branch_pct": 38.5}
      ],
      "mutation_score":  null,
      "bug_bench":       null
    }

Implementation model — **chunked JaCoCo TCP sampling**:

  * JaCoCo's `jacocoagent.jar` is attached to Jazzer's JVM in
    `output=tcpserver` mode, which exposes the live runtime coverage
    snapshot over a local TCP socket.
  * A watcher thread dumps that snapshot at each log tick by calling
    `jacococli.jar dump ... --reset=false`, producing
    `tick_<t>.exec` files without perturbing the running fuzzer.
  * After the budget expires the sampler terminates Jazzer, converts
    each `tick_<t>.exec` into line + branch % via `jacococli report`,
    and writes the growth JSON.

Tooling prerequisites (all present in `biotest-bench:latest`):

  * `/opt/jazzer/jazzer` (native launcher, JDK 17).
  * `/work/coverage_artifacts/jacoco/jacocoagent.jar` — attached via
    `--jvm_args=-javaagent\:...`.
  * `/work/coverage_artifacts/jacoco/jacococli.jar` — used for both
    `dump` (over TCP) and `report` (off-line XML generation).
  * `/work/compares/harnesses/jazzer/build/libs/biotest-jazzer.jar` —
    fatjar that also holds the `htsjdk.*` classfiles JaCoCo will need
    as `--classfiles` when reporting.

Cells implemented today:

  * **Jazzer × htsjdk** (VCF/SAM) — JaCoCo TCP-server agent + periodic
    `jacococli dump` at each tick; post-hoc `jacococli report` converts
    each `tick_<t>.exec` into line+branch %.
  * **Atheris × vcfpy / biopython** — Docker exec of the coverage-aware
    harness `fuzz_vcfpy.py` / `fuzz_biopython.py`. The harness runs a
    `coverage.Coverage` instance scoped to the SUT package with
    `branch=True`, snapshots the in-memory database via a
    `threading.Timer` at each requested tick, and writes
    `harness_growth.json` when libFuzzer exits. This sampler parses
    that file back into `CoverageTick`s.
  * **cargo-fuzz × noodles-vcf** (VCF) — cargo-fuzz runs the libFuzzer-
    instrumented target; at each tick the corpus is replayed through a
    cargo-llvm-cov-instrumented `noodles_harness` sibling binary, then
    `cargo llvm-cov report --json` is parsed and filtered by the
    `noodles-vcf` path substring.
  * **libFuzzer × seqan3** (SAM, DESIGN.md §13.2.4) — libFuzzer with
    `-fork=1 -ignore_crashes=1` runs the throughput harness
    (`seqan3_sam_fuzzer_libfuzzer`, built with
    `-fsanitize=fuzzer,address,undefined`). At each tick the corpus is
    replayed through the sibling `seqan3_sam_fuzzer_cov` binary
    (built with `--coverage`) and gcovr aggregates the `.gcda` into
    JSON filtered by `(seqan3/io/sam_file, format_sam, cigar)`. Both
    binaries share the same `LLVMFuzzerTestOneInput` source file via
    `compares/harnesses/libfuzzer/CMakeLists.txt`.

Remaining rows (AFL++/seqan3, Pure-random/*) follow the same dispatch
shape; stubs drop into `_dispatch_run` as they come online per
DESIGN.md §13.5.

Usage (inside `biotest-bench` via `bash compares/docker/run.sh bash -c ...`):

    # Jazzer × htsjdk
    python3.12 compares/scripts/coverage_sampler.py \
        --tool jazzer --sut htsjdk --format VCF \
        --seed-corpus compares/results/bench_seeds/vcf \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/jazzer/htsjdk_vcf/

    # libFuzzer × seqan3 (SAM only — DESIGN §13.5 Phase 2 libFuzzer row)
    python3.12 compares/scripts/coverage_sampler.py \
        --tool libfuzzer --sut seqan3 --format SAM \
        --seed-corpus compares/results/bench_seeds/sam \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/libfuzzer/seqan3/

    # Atheris × biopython (callable from Windows host via docker)
    python3.12 compares/scripts/coverage_sampler.py \
        --tool atheris --sut biopython --format SAM \
        --seed-corpus compares/results/bench_seeds/sam \
        --budget 7200 --reps 3 \
        --out compares/results/coverage/atheris/biopython/
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import logging
import os
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

logger = logging.getLogger("coverage_sampler")

REPO_ROOT = Path(__file__).resolve().parents[2]
JACOCO_DIR = REPO_ROOT / "coverage_artifacts" / "jacoco"
JACOCOAGENT_JAR = JACOCO_DIR / "jacocoagent.jar"
JACOCOCLI_JAR = JACOCO_DIR / "jacococli.jar"
JAZZER_JAR = REPO_ROOT / "compares" / "harnesses" / "jazzer" / "build" / "libs" / "biotest-jazzer.jar"
JAZZER_BIN_DEFAULT = "/opt/jazzer/jazzer"

# cargo-fuzz × noodles-vcf backend (DESIGN.md §13.2.7 + §13.5 Phase 2).
NOODLES_HARNESS_DIR = REPO_ROOT / "harnesses" / "rust" / "noodles_harness"
NOODLES_MANIFEST = NOODLES_HARNESS_DIR / "Cargo.toml"
CARGO_FUZZ_HARNESS_DIR = REPO_ROOT / "compares" / "harnesses" / "cargo_fuzz"
CARGO_BIN_DEFAULT = "/root/.cargo/bin"

# libFuzzer × seqan3 backend (DESIGN.md §13.2.4 + §13.5 Phase 2).
LIBFUZZER_DIR = REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
LIBFUZZER_BIN_DEFAULT = LIBFUZZER_DIR / "build" / "seqan3_sam_fuzzer_libfuzzer"
LIBFUZZER_COV_BUILD_DIR_DEFAULT = LIBFUZZER_DIR / "build-cov"
LIBFUZZER_COV_BIN_DEFAULT = LIBFUZZER_COV_BUILD_DIR_DEFAULT / "seqan3_sam_fuzzer_cov"
SEQAN3_SRC_ROOT_DEFAULT = Path("/opt/seqan3/include")  # inside biotest-bench
# Matches biotest_config.yaml: coverage.target_filters.SAM.seqan3.
SEQAN3_SAM_SCOPE: tuple[str, ...] = ("seqan3/io/sam_file", "format_sam", "cigar")

# JaCoCo `report` chokes on fatjars that nest other jars (the Jazzer
# runtime bundles `jazzer_bootstrap.jar` inside `biotest-jazzer.jar`),
# so we extract the `htsjdk/` tree to a plain directory and pass that as
# `--classfiles`. Cheap one-off — the 1.1 k classes unzip in <1s and the
# dir is reused across reps.
HTSJDK_CLASSES_DIR_DEFAULT = (
    REPO_ROOT / "compares" / "harnesses" / "jazzer" / "build" / "htsjdk-classes"
)

# Log ticks at which coverage is sampled (DESIGN.md §3.2).
DEFAULT_TICKS_S: tuple[int, ...] = (1, 10, 60, 300, 1800, 7200)

# Per-format scope is NOT hardcoded here — we delegate to the fairness
# recipe (compares/scripts/measure_coverage.py + biotest_config.yaml
# :coverage.target_filters) so any tool measured against a given
# (format, sut) sees exactly the same filter rules the feedback loop +
# all baselines see. Change rules once in biotest_config.yaml; every
# measurement picks them up automatically. See compares/scripts/README.md.

JAZZER_TARGET_CLASS: dict[str, tuple[str, tuple[str, ...]]] = {
    "VCF": (
        "VCFCodecFuzzer",
        ("htsjdk.variant.vcf.**", "htsjdk.variant.variantcontext.**"),
    ),
    "SAM": (
        "SAMCodecFuzzer",
        ("htsjdk.samtools.**",),
    ),
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hash_corpus(corpus_dir: Path) -> str:
    """Stable sha256 of `(sorted filename, file bytes)` pairs. Empty or
    missing dir returns a deterministic sentinel so the hash is never
    blank in the output JSON."""
    if not corpus_dir.exists():
        return "sha256:empty"
    h = hashlib.sha256()
    entries = sorted(p for p in corpus_dir.rglob("*") if p.is_file())
    for p in entries:
        h.update(p.name.encode("utf-8"))
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def _seed_copy(src: Path, dst: Path) -> int:
    """Flat-copy every file under `src` into `dst`. Returns count."""
    dst.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        return 0
    n = 0
    for p in src.rglob("*"):
        if p.is_file():
            shutil.copy2(p, dst / p.name)
            n += 1
    return n


def _pick_free_port(start: int = 6300) -> int:
    """Probe a free TCP port starting at `start`. Jazzer + jacocoagent
    bind to `address=*,port=<n>`; we need a distinct port per rep so
    concurrent reps don't collide if the caller ever parallelises."""
    port = start
    for _ in range(50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"could not find a free port >= {start}")


def _ensure_htsjdk_classes_dir(harness_jar: Path, classes_dir: Path) -> Path:
    """Materialise `htsjdk/**/*.class` under `classes_dir` by unzipping
    the harness fatjar. Idempotent — skips unzip when the root marker
    class is already present. JaCoCo's `report` command cannot descend
    into nested jars (Jazzer bundles its own runtime jar inside the
    fatjar), so we need a flat class tree on disk."""
    marker = classes_dir / "htsjdk" / "variant" / "vcf" / "VCFCodec.class"
    if marker.exists():
        return classes_dir
    classes_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["unzip", "-o", "-q", str(harness_jar), "htsjdk/*", "-d", str(classes_dir)]
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    if r.returncode != 0 or not marker.exists():
        raise RuntimeError(
            f"could not extract htsjdk classes from {harness_jar} into "
            f"{classes_dir}: rc={r.returncode} "
            f"stderr={r.stderr.decode(errors='replace')[:200]}"
        )
    return classes_dir


def _wait_for_port(port: int, deadline_s: float) -> bool:
    """Busy-wait until `port` accepts a TCP connection or deadline passes."""
    while time.time() < deadline_s:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.2)
    return False


# ---------------------------------------------------------------------------
# Coverage measurement — delegates to the fairness recipe
# (compares/scripts/measure_coverage.py + biotest_config.yaml) so the
# number this sampler prints is the same number the feedback loop + any
# baseline tool would print. Filter rules live in
# biotest_config.yaml:coverage.target_filters[<FMT>][<sut>] — change
# there, every measurement sees it. See compares/scripts/README.md.
# ---------------------------------------------------------------------------

# Import the fairness-recipe CLI as a module. `measure_coverage.py` has
# no shebang-less import path, so we load it by spec.
import importlib.util as _importlib_util

_MC_SPEC = _importlib_util.spec_from_file_location(
    "measure_coverage", Path(__file__).resolve().parent / "measure_coverage.py"
)
_measure_coverage = _importlib_util.module_from_spec(_MC_SPEC)
sys.modules.setdefault("measure_coverage", _measure_coverage)
_MC_SPEC.loader.exec_module(_measure_coverage)
_FAIR_MEASURE = _measure_coverage.measure


def _exec_to_tick(
    exec_path: Path,
    classfiles: Path,
    sut: str,
    format_hint: str,
    config_path: Path,
    t_s: int,
    java_bin: str,
    jacococli_jar: Path,
    work_dir: Path,
) -> CoverageTick:
    """Convert a single `.exec` snapshot into a `CoverageTick`.

    Steps:
      1. `jacococli report --xml` converts the exec into a per-package
         / per-sourcefile JaCoCo XML.
      2. `measure_coverage.measure(xml, sut, fmt, config, metric=…)`
         applies BioTest's authoritative filter rules (JEXL-exclude
         etc.) and returns the filtered, weighted line / branch %.
    """
    xml_out = work_dir / f"tick_{t_s}.xml"
    cmd = [
        java_bin, "-jar", str(jacococli_jar), "report", str(exec_path),
        "--classfiles", str(classfiles),
        "--xml", str(xml_out),
    ]
    # Short timeout: report generation on a small htsjdk fatjar is fast.
    proc = subprocess.run(cmd, capture_output=True, timeout=180)
    if proc.returncode != 0 or not xml_out.exists():
        logger.warning(
            "jacococli report failed for %s (rc=%s stderr=%s)",
            exec_path.name, proc.returncode, proc.stderr.decode(errors="replace")[:200],
        )
        return CoverageTick(t_s=t_s, line_pct=0.0, branch_pct=0.0)

    try:
        line_r = _FAIR_MEASURE(
            report_path=xml_out, sut=sut, format_=format_hint.upper(),
            config_path=config_path, metric="LINE",
        )
        branch_r = _FAIR_MEASURE(
            report_path=xml_out, sut=sut, format_=format_hint.upper(),
            config_path=config_path, metric="BRANCH",
        )
    except Exception as exc:
        logger.warning(
            "measure_coverage failed for %s (%s) — emitting zero tick",
            xml_out.name, exc,
        )
        return CoverageTick(t_s=t_s, line_pct=0.0, branch_pct=0.0)

    return CoverageTick(
        t_s=t_s,
        line_pct=line_r.weighted_pct,
        branch_pct=branch_r.weighted_pct,
    )


# ---------------------------------------------------------------------------
# Jazzer runner (one rep; attaches jacocoagent, samples ticks)
# ---------------------------------------------------------------------------

def _run_jazzer_rep(
    sut: str,
    format_hint: str,
    seed_corpus: Path,
    out_rep: Path,
    time_budget_s: int,
    ticks: tuple[int, ...],
    jazzer_bin: str,
    harness_jar: Path,
    classes_dir: Path,
    jacocoagent_jar: Path,
    jacococli_jar: Path,
    java_bin: str,
    tcp_port_start: int,
    config_path: Path,
) -> list[CoverageTick]:
    """Run one Jazzer rep with JaCoCo TCP sampling. Returns the ordered
    list of CoverageTick snapshots (one per tick that fell inside the
    budget; ticks beyond the budget are dropped)."""
    if sut != "htsjdk":
        raise ValueError(f"_run_jazzer_rep only supports sut=htsjdk, got {sut!r}")

    corpus_dir = out_rep / "corpus"
    crashes_dir = out_rep / "crashes"
    exec_dir = out_rep / "jacoco_exec"
    log_file = out_rep / "tool.log"
    for d in (corpus_dir, crashes_dir, exec_dir):
        d.mkdir(parents=True, exist_ok=True)
    _seed_copy(seed_corpus, corpus_dir)

    fmt = format_hint.upper()
    target_class, instrument_globs = JAZZER_TARGET_CLASS[fmt]

    # Unique TCP port so concurrent reps don't collide.
    port = _pick_free_port(tcp_port_start)

    # JaCoCo TCP-server agent. Jazzer's `--jvm_args` separator is ':',
    # which the javaagent syntax also uses — so escape with backslash.
    agent_opts = (
        f"output=tcpserver,address=127.0.0.1,port={port},"
        "includes=htsjdk.*,excludes=*Test*:*test*,sessionid=biotest-phase2,dumponexit=true"
    )
    agent_arg = f"-javaagent\\:{jacocoagent_jar}={agent_opts}"

    cmd = [
        jazzer_bin,
        f"--jvm_args={agent_arg}",
        f"--cp={harness_jar}",
        f"--target_class={target_class}",
    ]
    for glob in instrument_globs:
        cmd.append(f"--instrumentation_includes={glob}")
    reproducers_dir = out_rep / "reproducers"
    reproducers_dir.mkdir(exist_ok=True)
    cmd.extend([
        # Keep fuzzing past the first finding — Phase 2 is a coverage
        # race, not a bug hunt. Findings still land in crashes_dir.
        # `--keep_going` is a Jazzer option (double-dash) rather than a
        # libFuzzer option (single-dash); default is 1, so we lift it
        # generously to soak through the known-crash shape space.
        "--keep_going=1000000",
        # Java reproducer stubs default to cwd ('.'); pin them into a
        # per-rep subdir so they don't pollute the repo root.
        f"--reproducer_path={reproducers_dir}",
        f"-artifact_prefix={crashes_dir}{os.sep}",
        f"-max_total_time={time_budget_s}",
        str(corpus_dir),
    ])

    # Scrub JAZZER_* from env — Jazzer auto-parses those as CLI options
    # and a lingering JAZZER_VERSION poisons startup (DESIGN.md §13.2.2).
    child_env = {k: v for k, v in os.environ.items() if not k.startswith("JAZZER_")}

    logger.info(
        "rep %s: starting jazzer (target=%s port=%s budget=%ds)",
        out_rep.name, target_class, port, time_budget_s,
    )

    ticks_in_budget = tuple(t for t in sorted(set(ticks)) if t <= time_budget_s)
    tick_snapshots: list[CoverageTick] = []
    tick_exec_paths: dict[int, Path] = {}

    # Belt + suspenders: also pin cwd to the reproducers dir so any
    # stray file-write from Jazzer / htsjdk lands there, not at /work.
    with log_file.open("ab") as logfh:
        proc = subprocess.Popen(
            cmd,
            stdout=logfh,
            stderr=subprocess.STDOUT,
            env=child_env,
            cwd=str(reproducers_dir),
            # New process group on POSIX so SIGTERM propagates.
            preexec_fn=os.setsid if os.name != "nt" else None,
        )

    # Wait up to 30s for the agent's TCP port to open.
    agent_ready = _wait_for_port(port, deadline_s=time.time() + 30.0)
    if not agent_ready:
        logger.warning(
            "rep %s: agent did not bind port %s within 30s — tick sampling "
            "may be degraded", out_rep.name, port,
        )

    started = time.time()

    def _dump_tick(t_s: int) -> Path | None:
        exec_path = exec_dir / f"tick_{t_s}.exec"
        cmd = [
            java_bin, "-jar", str(jacococli_jar), "dump",
            "--address", "127.0.0.1", "--port", str(port),
            "--destfile", str(exec_path),
            # Keep the running coverage counters intact — each tick is a
            # cumulative snapshot, not a delta.
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=30)
        except subprocess.TimeoutExpired:
            logger.warning("rep %s: jacoco dump @ t=%ds timed out", out_rep.name, t_s)
            return None
        if r.returncode != 0:
            logger.warning(
                "rep %s: jacoco dump @ t=%ds failed (rc=%s stderr=%s)",
                out_rep.name, t_s, r.returncode,
                r.stderr.decode(errors="replace")[:200],
            )
            return None
        return exec_path

    # Tick-sampling loop runs in the main thread (simpler lifecycle than
    # a watcher — we're blocked on Jazzer anyway).
    for t in ticks_in_budget:
        # Sleep until this tick's wall-clock target.
        target_wall = started + t
        now = time.time()
        if now < target_wall:
            # If Jazzer exits before we reach this tick, break out.
            while time.time() < target_wall:
                if proc.poll() is not None:
                    break
                time.sleep(min(0.5, max(0.05, target_wall - time.time())))
        if proc.poll() is not None:
            logger.info(
                "rep %s: jazzer exited at ~t=%.1fs (before tick %ds); "
                "last-ditch snapshot will be the final exec dump",
                out_rep.name, time.time() - started, t,
            )
            break
        exec_path = _dump_tick(t)
        if exec_path is not None:
            tick_exec_paths[t] = exec_path

    # Budget reached (or Jazzer already exited). Make sure Jazzer is down.
    if proc.poll() is None:
        try:
            if os.name == "nt":
                proc.terminate()
            else:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            logger.warning("rep %s: jazzer did not terminate in 15s — killing", out_rep.name)
            try:
                if os.name == "nt":
                    proc.kill()
                else:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=5)

    # Convert each tick exec to a coverage % via `jacococli report` +
    # the fairness recipe. Filter rules come from
    # biotest_config.yaml:coverage.target_filters[<FMT>][<sut>] —
    # identical to what the feedback loop + any baseline tool sees.
    for t, exec_path in sorted(tick_exec_paths.items()):
        tick = _exec_to_tick(
            exec_path=exec_path,
            classfiles=classes_dir,
            sut=sut,
            format_hint=fmt,
            config_path=config_path,
            t_s=t,
            java_bin=java_bin,
            jacococli_jar=jacococli_jar,
            work_dir=exec_dir,
        )
        tick_snapshots.append(tick)

    # If we have no ticks (Jazzer crashed before the first tick or the
    # agent never bound), try one final dump from the dumponexit file
    # — the agent writes this to the current working directory as
    # `jacoco.exec` when dumponexit=true. Not a hard guarantee but worth
    # a shot for short budgets.
    if not tick_snapshots:
        fallback = Path.cwd() / "jacoco.exec"
        if fallback.exists():
            moved = exec_dir / "tick_final.exec"
            shutil.move(str(fallback), str(moved))
            # Attribute the snapshot to the smallest requested tick so
            # the downstream plot has SOMETHING at the low-t end.
            t0 = ticks_in_budget[0] if ticks_in_budget else min(ticks)
            tick_snapshots.append(_exec_to_tick(
                exec_path=moved, classfiles=classes_dir,
                sut=sut, format_hint=fmt, config_path=config_path,
                t_s=t0, java_bin=java_bin, jacococli_jar=jacococli_jar,
                work_dir=exec_dir,
            ))

    logger.info(
        "rep %s: done (%d tick snapshots)", out_rep.name, len(tick_snapshots),
    )
    return tick_snapshots


# ---------------------------------------------------------------------------
# cargo-fuzz × noodles-vcf backend (Rust / cargo-llvm-cov replay)
# ---------------------------------------------------------------------------
#
# Coverage model: cargo-fuzz runs the libFuzzer-driven `noodles_vcf_target`
# binary for the wall-clock budget. libFuzzer itself writes mutated inputs
# to `<out_rep>/corpus/` as it finds coverage-increasing bytes. At each
# DESIGN.md §3.2 log tick the sampler thread (a) clears the cargo-llvm-cov
# profile cache, (b) replays the current corpus through a separate,
# cargo-llvm-cov-instrumented build of `harnesses/rust/noodles_harness`
# (NOT the fuzz target — the fuzz-target binary links libFuzzer's own
# instrumentation which is not source-based-coverage compatible), and
# (c) shells out to `cargo llvm-cov report --json` and parses out the
# noodles-vcf-scoped line/branch counters. The same JSON shape and path
# filter that `test_engine.feedback.coverage_collector.NoodlesCoverageCollector`
# uses at Phase D — kept parallel on purpose.


def _cargo_env() -> dict[str, str]:
    env = os.environ.copy()
    if CARGO_BIN_DEFAULT not in env.get("PATH", ""):
        env["PATH"] = f"{CARGO_BIN_DEFAULT}:{env.get('PATH', '')}"
    return env


# Direct LLVM-toolchain pipeline — avoids cargo-llvm-cov's
# workspace-only instrumentation, which hides noodles-vcf under 0/0 lines.
# `llvm-profdata` + `llvm-cov` ship with rustup's `llvm-tools-preview`
# component (DESIGN §13.2.7 prereq).

LLVM_TOOLS_DIR = Path(
    "/root/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/"
    "rustlib/x86_64-unknown-linux-gnu/bin"
)


def _llvm_tool(name: str) -> Path:
    p = LLVM_TOOLS_DIR / name
    if not p.exists():
        raise RuntimeError(
            f"{name} missing at {p}. Install rustup's 'llvm-tools-preview' "
            "component (DESIGN §13.2.7)."
        )
    return p


def _build_instrumented_noodles_harness() -> tuple[Path, dict[str, str]]:
    """Build `noodles_harness` with source-based LLVM coverage instrumentation
    applied to ALL crates (so noodles-vcf dependency code is covered).

    Returns (binary_path, replay_env). `replay_env` carries RUSTFLAGS +
    LLVM_PROFILE_FILE so callers running the binary can extend it to a
    unique profraw path per replay.
    """
    logger.info("building instrumented noodles_harness (RUSTFLAGS -C instrument-coverage)…")
    env = _cargo_env()
    env["RUSTFLAGS"] = "-C instrument-coverage"
    # Keep the target dir on disk across ticks so incremental rebuilds are fast.
    proc = subprocess.run(
        ["cargo", "build", "--release",
         "--manifest-path", str(NOODLES_MANIFEST)],
        env=env, capture_output=True, text=True, timeout=1800,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"instrumented cargo build failed (rc={proc.returncode}):\n"
            f"stderr:\n{proc.stderr[-2000:]}"
        )
    binary = NOODLES_HARNESS_DIR / "target" / "release" / "noodles_harness"
    if not binary.exists():
        raise RuntimeError(
            f"cargo build succeeded but noodles_harness binary not found at {binary}"
        )
    logger.info("  instrumented binary: %s", binary)
    return binary, env


def _replay_corpus_instrumented(
    binary: Path,
    corpus_dir: Path,
    replay_log: Path,
    instr_env: dict[str, str],
    profile_dir: Path,
) -> dict[str, int]:
    """Replay every file in `corpus_dir` through the instrumented binary.

    Each invocation writes a .profraw to `profile_dir/cov-%p-%m.profraw`.
    Returns {accepted, rejected, timeout, total}.
    """
    profile_dir.mkdir(parents=True, exist_ok=True)
    env = dict(instr_env)
    env["LLVM_PROFILE_FILE"] = str(profile_dir / "cov-%p-%m.profraw")
    counts = {"accepted": 0, "rejected": 0, "timeout": 0}
    files = [p for p in corpus_dir.iterdir() if p.is_file()]
    with replay_log.open("ab") as logfh:
        logfh.write(f"\n=== replay {len(files)} files ===\n".encode())
        for p in files:
            try:
                r = subprocess.run(
                    [str(binary), "VCF", str(p)],
                    stdout=logfh, stderr=logfh,
                    timeout=5, env=env, check=False,
                )
                if r.returncode == 0:
                    counts["accepted"] += 1
                else:
                    counts["rejected"] += 1
            except subprocess.TimeoutExpired:
                counts["timeout"] += 1
    counts["total"] = len(files)
    return counts


def _merge_profraws(profile_dir: Path, out_profdata: Path) -> bool:
    """Merge every .profraw in `profile_dir` into `out_profdata`. Returns
    True on success; logs + returns False otherwise.
    """
    raws = list(profile_dir.glob("cov-*.profraw"))
    if not raws:
        return False
    cmd = [str(_llvm_tool("llvm-profdata")), "merge", "-sparse",
           "-o", str(out_profdata), *[str(p) for p in raws]]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        logger.warning("llvm-profdata merge failed: %s", r.stderr[-400:])
        return False
    return out_profdata.exists()


def _llvm_cov_export_json(
    binary: Path, profdata: Path,
) -> dict | None:
    cmd = [str(_llvm_tool("llvm-cov")), "export", "-format=text",
           f"-instr-profile={profdata}", str(binary)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        logger.warning("llvm-cov export failed: %s", r.stderr[-400:])
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        logger.warning("llvm-cov export JSON decode failed: %s", e)
        return None


# Back-compat alias — older callers invoke the cargo-llvm-cov helpers.
def _cargo_llvm_cov_clean(instr_env: dict[str, str] | None = None) -> None:
    """No-op under the direct-LLVM flow: per-tick profile dirs isolate the
    snapshots so there's no global cache to clean. Kept so the older call
    site in `_run_cargo_fuzz_rep` stays source-compatible."""
    return None


def _cargo_llvm_cov_report_json() -> dict | None:
    env = _cargo_env()
    cmd = [
        "cargo", "llvm-cov", "report", "--json",
        "--manifest-path", str(NOODLES_MANIFEST),
    ]
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        logger.warning("cargo llvm-cov report failed: %s", proc.stderr[-400:])
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        logger.warning("cargo llvm-cov report JSON decode failed: %s", e)
        return None


def _summarise_noodles_report(report: dict) -> dict[str, float | int]:
    """Filter the cargo-llvm-cov JSON to files whose path contains
    `noodles-vcf`, sum line + branch counters, and compute percentages."""
    line_cov = line_tot = 0
    branch_cov = branch_tot = 0
    region_cov = region_tot = 0
    files_counted = 0
    for run in report.get("data", []):
        for f in run.get("files", []):
            fn = f.get("filename", "").replace("\\", "/")
            if "noodles-vcf" not in fn:
                continue
            files_counted += 1
            s = f.get("summary", {})
            line_cov += int(s.get("lines", {}).get("covered", 0))
            line_tot += int(s.get("lines", {}).get("count", 0))
            branch_cov += int(s.get("branches", {}).get("covered", 0))
            branch_tot += int(s.get("branches", {}).get("count", 0))
            region_cov += int(s.get("regions", {}).get("covered", 0))
            region_tot += int(s.get("regions", {}).get("count", 0))
    return {
        "line_pct": round(100.0 * line_cov / line_tot, 3) if line_tot else 0.0,
        "branch_pct": round(100.0 * branch_cov / branch_tot, 3) if branch_tot else 0.0,
        "region_pct": round(100.0 * region_cov / region_tot, 3) if region_tot else 0.0,
        "line_covered": line_cov,
        "line_total": line_tot,
        "branch_covered": branch_cov,
        "branch_total": branch_tot,
        "noodles_files": files_counted,
    }


def _run_cargo_fuzz_rep(
    sut: str,
    format_hint: str,
    seed_corpus: Path,
    out_rep: Path,
    time_budget_s: int,
    ticks: tuple[int, ...],
    instrumented_binary: Path,
    instr_env: dict[str, str],
) -> list[CoverageTick]:
    """Run one cargo-fuzz rep with cargo-llvm-cov corpus-replay sampling.

    Spawns the cargo-fuzz adapter in a background thread for `time_budget_s`
    seconds. At each log tick inside the budget, snapshots the corpus,
    replays it through the instrumented noodles_harness, and produces a
    `CoverageTick` via `cargo llvm-cov report --json`.
    """
    if sut != "noodles":
        raise ValueError(f"_run_cargo_fuzz_rep only supports sut=noodles, got {sut!r}")
    if format_hint.upper() != "VCF":
        raise ValueError("cargo-fuzz × noodles is VCF-only")

    sys.path.insert(0, str(Path(__file__).resolve().parent / "tool_adapters"))
    import run_cargo_fuzz  # noqa: WPS433 — deferred import

    corpus_dir = out_rep / "corpus"
    replay_log = out_rep / "replay.log"
    replay_log.touch()

    ticks_in_budget = tuple(t for t in sorted(set(ticks)) if t <= time_budget_s)

    adapter_holder: list[object] = []

    def _fuzz_worker() -> None:
        try:
            res = run_cargo_fuzz.run(
                sut=sut,
                seed_corpus=seed_corpus,
                out_dir=out_rep,
                time_budget_s=time_budget_s,
                format_hint=format_hint,
            )
            adapter_holder.append(res)
        except Exception as e:  # noqa: BLE001
            logger.exception("cargo-fuzz adapter raised")
            adapter_holder.append(e)

    thread = threading.Thread(target=_fuzz_worker, name=f"cargo-fuzz-{out_rep.name}")
    started = time.time()
    thread.start()

    snapshots: list[CoverageTick] = []

    for tk in ticks_in_budget:
        target_wall = started + tk
        # Wait until the tick lands (or the fuzzer finishes early).
        while time.time() < target_wall and thread.is_alive():
            time.sleep(min(0.5, max(0.05, target_wall - time.time())))

        if not corpus_dir.exists():
            logger.warning("rep %s: corpus dir not ready at t=%ds", out_rep.name, tk)
            snapshots.append(CoverageTick(t_s=tk, line_pct=0.0, branch_pct=0.0))
            continue

        # Per-tick profile dir — so each tick's coverage measurement is
        # independent (and inspection-friendly). The llvm-profdata merge
        # folds the profraws into one profdata, then llvm-cov export
        # renders the JSON.
        tick_profile_dir = out_rep / "profile" / f"tick_{tk}"
        if tick_profile_dir.exists():
            shutil.rmtree(tick_profile_dir)
        replay_counts = _replay_corpus_instrumented(
            instrumented_binary, corpus_dir, replay_log, instr_env,
            tick_profile_dir,
        )
        profdata = tick_profile_dir / "merged.profdata"
        report = None
        if _merge_profraws(tick_profile_dir, profdata):
            report = _llvm_cov_export_json(instrumented_binary, profdata)
        if report is None:
            snapshots.append(CoverageTick(t_s=tk, line_pct=0.0, branch_pct=0.0))
            continue
        summary = _summarise_noodles_report(report)
        logger.info(
            "rep %s: tick t=%ds  line=%.2f%%  branch=%.2f%%  "
            "files_replayed=%d accepted=%d rejected=%d",
            out_rep.name, tk, summary["line_pct"], summary["branch_pct"],
            replay_counts["total"], replay_counts["accepted"],
            replay_counts["rejected"],
        )
        snapshots.append(CoverageTick(
            t_s=tk,
            line_pct=float(summary["line_pct"]),
            branch_pct=float(summary["branch_pct"]),
        ))

    thread.join(timeout=time_budget_s + 120)

    adapter_result = (adapter_holder[0]
                      if adapter_holder and not isinstance(adapter_holder[0], Exception)
                      else None)
    if adapter_result is None and adapter_holder:
        logger.warning("rep %s: adapter raised: %s", out_rep.name, adapter_holder[0])

    # Persist the adapter manifest per rep so downstream tools can find it.
    if adapter_result is not None:
        try:
            adapter_result.write_manifest(out_rep / "adapter_result.json")
        except Exception:  # noqa: BLE001
            logger.exception("failed to write adapter manifest")

    return snapshots


# ---------------------------------------------------------------------------
# Atheris × vcfpy backend (Python / coverage.py in-process snapshotting)
# ---------------------------------------------------------------------------
#
# Coverage model: `fuzz_vcfpy.py` owns the `coverage.Coverage` instance
# scoped to `source=['vcfpy']` with `branch=True`. It spawns a daemon
# thread that calls `cov.save()` at each requested tick and writes a
# coverage_growth record to `<rep>/harness_growth.json`. This sampler
# simply shells into the biotest-bench image's Python 3.11 atheris-venv,
# passes the cov-* flags, and reads the harness-written JSON back when
# libFuzzer exits (SIGABRT / exit-77 on first crash, or natural exit at
# `-max_total_time=`).
#
# No cargo-llvm-cov-style post-hoc replay is needed because coverage.py
# instruments vcfpy's Python bytecode in-process, so the tick values are
# the *actual* coverage state at each wall-clock tick inside the fuzz
# loop. Identical methodology to the existing Phase-D pipeline's
# CoveragePyCollector (test_engine/feedback/coverage_collector.py:388).


def _docker_path(host_path: Path) -> str:
    """Rewrite an absolute host path to its /work-rooted container form.

    The `biotest-bench` image's run.sh mounts the repo at /work; every
    adapter inside the container must receive paths through that prefix.
    """
    try:
        rel = host_path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise RuntimeError(
            f"host path {host_path} is not under repo root {REPO_ROOT}"
        ) from exc
    return "/work/" + str(rel).replace("\\", "/")


def _docker_mount_src() -> str:
    """Mount source for `docker run -v`.

    Docker's `-v <source>:<target>[:<mode>]` parses on the first colon,
    so a Windows drive-letter path like `C:/Users/...:/work` has two
    colons and Docker interprets `/work` as the mount mode ("invalid
    mode: /work" error).

    Normalise to the `/c/Users/...` form that Docker Desktop maps to
    the host drive transparently (same mapping MinGW / Git-Bash already
    expose at the shell level).
    """
    norm = str(REPO_ROOT).replace("\\", "/")
    if len(norm) >= 2 and norm[1] == ":":
        drive = norm[0].lower()
        rest = norm[2:]
        if not rest.startswith("/"):
            rest = "/" + rest
        return f"/{drive}{rest}"
    return norm


def _run_atheris_rep(
    sut: str,
    format_hint: str,
    seed_corpus: Path,
    out_rep: Path,
    time_budget_s: int,
    ticks: tuple[int, ...],
    opts: argparse.Namespace,
) -> list[CoverageTick]:
    """Run one Atheris rep via `docker run` of the biotest-bench image.

    The coverage-aware harness owns the snapshot loop (see
    `compares/harnesses/atheris/fuzz_vcfpy.py` and
    `compares/harnesses/atheris/fuzz_biopython.py`); this function is just
    a shell wrapper that collects the harness's per-tick JSON back into
    the sampler's `CoverageTick` dataclass.

    Routes by SUT:
        vcfpy     → fuzz_vcfpy.py     (VCF)
        biopython → fuzz_biopython.py (SAM — DESIGN.md §13.5 Phase 2)
    """
    _ATHERIS_CELLS = {
        ("vcfpy", "VCF"):     "compares/harnesses/atheris/fuzz_vcfpy.py",
        ("biopython", "SAM"): "compares/harnesses/atheris/fuzz_biopython.py",
    }
    cell_key = (sut, format_hint.upper())
    if cell_key not in _ATHERIS_CELLS:
        raise NotImplementedError(
            f"_run_atheris_rep: ({sut!r}, {format_hint!r}) not wired yet. "
            "Add a coverage-aware harness following fuzz_vcfpy.py / "
            "fuzz_biopython.py and extend _ATHERIS_CELLS."
        )
    default_harness_rel = _ATHERIS_CELLS[cell_key]

    corpus_dir = out_rep / "corpus"
    crashes_dir = out_rep / "crashes"
    log_file = out_rep / "tool.log"
    for d in (corpus_dir, crashes_dir):
        d.mkdir(parents=True, exist_ok=True)
    _seed_copy(seed_corpus, corpus_dir)

    cov_data_file = out_rep / ".coverage"
    growth_out = out_rep / "harness_growth.json"

    # Remove stale harness-growth + coverage files from previous reps so
    # the tick list starts empty. `fuzz_vcfpy.py` also deletes the
    # .coverage file defensively but belt-and-braces is cheap here.
    for stale in (growth_out, cov_data_file):
        try:
            stale.unlink()
        except FileNotFoundError:
            pass

    tick_arg = ",".join(str(t) for t in sorted(set(ticks)))

    harness_rel = getattr(opts, "atheris_harness", None) or default_harness_rel
    in_ctr_corpus = _docker_path(corpus_dir)
    in_ctr_crashes = _docker_path(crashes_dir).rstrip("/") + "/"
    in_ctr_cov = _docker_path(cov_data_file)
    in_ctr_growth = _docker_path(growth_out)

    atheris_image = getattr(opts, "atheris_image", "biotest-bench:latest")
    atheris_python = getattr(
        opts, "atheris_python", "/opt/atheris-venv/bin/python",
    )

    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{_docker_mount_src()}:/work",
        "-w", "/work",
        "-e", "PYTHONPATH=/work",
        "-e", "MSYS_NO_PATHCONV=1",
        atheris_image,
        atheris_python,
        f"/work/{harness_rel}",
        f"--format={format_hint.upper()}",
        f"--cov-data-file={in_ctr_cov}",
        f"--cov-growth-out={in_ctr_growth}",
        f"--cov-sample-ticks={tick_arg}",
        f"-artifact_prefix={in_ctr_crashes}",
        f"-max_total_time={time_budget_s}",
        "-atheris_runs=0",
        # Phase 2 is a coverage-growth race, not a bug hunt. Tell
        # libFuzzer to keep running past every finding so the tick loop
        # accumulates coverage over the full budget (DESIGN §13.5 Phase 2).
        "-ignore_crashes=1",
        "-ignore_ooms=1",
        "-ignore_timeouts=1",
        in_ctr_corpus,
    ]

    child_env = os.environ.copy()
    child_env.setdefault("MSYS_NO_PATHCONV", "1")

    logger.info(
        "rep %s: starting atheris × %s (budget=%ds ticks=%s harness=%s)",
        out_rep.name, sut, time_budget_s, tick_arg, harness_rel,
    )
    logger.debug("docker cmd: %s", " ".join(docker_cmd))

    started_wall = time.time()
    timeout_s = time_budget_s + 300  # grace for coverage finalize
    with log_file.open("ab") as logfh:
        try:
            proc = subprocess.run(
                docker_cmd,
                stdout=logfh,
                stderr=subprocess.STDOUT,
                timeout=timeout_s,
                env=child_env,
                check=False,
            )
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            logger.warning("rep %s: docker-run hit outer timeout", out_rep.name)
            exit_code = -1

    # The harness's finalizer writes the growth JSON inside a
    # try/finally, so missing-file == docker misfire.
    if not growth_out.exists():
        logger.error(
            "rep %s: harness did not write %s (exit=%s) — see %s",
            out_rep.name, growth_out, exit_code, log_file,
        )
        return []

    try:
        payload = json.loads(growth_out.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.error("rep %s: could not parse %s: %s", out_rep.name, growth_out, exc)
        return []

    snapshots: list[CoverageTick] = []
    seen_ticks: set[int] = set()
    for rec in payload.get("coverage_growth", []):
        t = rec.get("t_s")
        lp = rec.get("line_pct")
        bp = rec.get("branch_pct")
        if t is None or lp is None:
            continue
        snapshots.append(CoverageTick(
            t_s=int(t),
            line_pct=float(lp),
            branch_pct=float(bp) if bp is not None else 0.0,
        ))
        seen_ticks.add(int(t))

    # Atheris's libFuzzer driver calls `_exit()` on budget-expiry, which
    # bypasses both Python's finally and atexit handlers — so the
    # snapshot thread never records the tick == budget, and coverage.py's
    # internal atexit never runs either. Recover any missing ticks ≤
    # budget post-hoc by reading the terminal .coverage file (the
    # snapshot thread's prior cov.save() calls persist state
    # incrementally, so the data on disk represents the latest
    # fully-flushed coverage state).
    requested_ticks = [t for t in sorted(set(ticks)) if t <= time_budget_s]
    missing_ticks = [t for t in requested_ticks if t not in seen_ticks]
    if missing_ticks and cov_data_file.exists():
        final_line_pct, final_branch_pct = _compute_final_pct_from_cov(
            cov_data_file=cov_data_file,
            atheris_image=atheris_image,
            atheris_python=atheris_python,
            child_env=child_env,
        )
        if final_line_pct is not None:
            for t in missing_ticks:
                snapshots.append(CoverageTick(
                    t_s=int(t),
                    line_pct=final_line_pct,
                    branch_pct=final_branch_pct or 0.0,
                ))
                logger.info(
                    "rep %s: post-hoc tick %ds — line=%.2f%% branch=%.2f%% "
                    "(from terminal .coverage)",
                    out_rep.name, t, final_line_pct, final_branch_pct or 0.0,
                )
        else:
            logger.warning(
                "rep %s: missing ticks %s but post-hoc finalize returned no data",
                out_rep.name, missing_ticks,
            )

    snapshots.sort(key=lambda s: s.t_s)

    (out_rep / "atheris_meta.json").write_text(json.dumps({
        "exit_code": exit_code,
        "time_budget_s": time_budget_s,
        "ticks_requested": sorted(set(ticks)),
        "ticks_from_live_thread": sorted(seen_ticks),
        "ticks_post_hoc": sorted(set(missing_ticks) & set(requested_ticks)),
        "harness_growth_json": str(growth_out),
        "coverage_data_file": str(cov_data_file),
        "docker_image": atheris_image,
        "atheris_python": atheris_python,
        "started_wall": started_wall,
        "duration_s": round(time.time() - started_wall, 2),
    }, indent=2), encoding="utf-8")

    logger.info(
        "rep %s: atheris done (%d ticks, exit=%s)",
        out_rep.name, len(snapshots), exit_code,
    )
    return snapshots


def _compute_final_pct_from_cov(
    cov_data_file: Path,
    atheris_image: str,
    atheris_python: str,
    child_env: dict[str, str],
) -> tuple[float | None, float | None]:
    """Shell into the atheris image and total the saved .coverage db.

    Used to fill any tick == budget slot the live snapshot thread
    missed because libFuzzer's `_exit()` killed Python before the
    thread woke up.
    """
    in_ctr = _docker_path(cov_data_file)
    probe = (
        "import os, json, tempfile, coverage;"
        f"cov = coverage.Coverage(data_file={in_ctr!r},"
        " source=['vcfpy'], branch=True, config_file=False);"
        " cov.load();"
        " fd, p = tempfile.mkstemp(suffix='.json'); os.close(fd);"
        " cov.json_report(outfile=p);"
        " r = json.loads(open(p).read()); os.unlink(p);"
        " print(json.dumps(r.get('totals', {})))"
    )
    finalize_cmd = [
        "docker", "run", "--rm",
        "-v", f"{_docker_mount_src()}:/work",
        "-w", "/work",
        atheris_image,
        atheris_python,
        "-c", probe,
    ]
    try:
        proc = subprocess.run(
            finalize_cmd, capture_output=True, text=True,
            timeout=120, env=child_env, check=False,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("post-hoc finalize raised: %s", exc)
        return None, None
    if proc.returncode != 0 or not proc.stdout.strip():
        logger.warning(
            "post-hoc finalize failed rc=%s stderr=%s",
            proc.returncode, proc.stderr[-300:] if proc.stderr else "",
        )
        return None, None
    try:
        totals = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as exc:
        logger.warning("post-hoc finalize parse failed: %s", exc)
        return None, None
    covered = int(totals.get("covered_lines", 0))
    missing_l = int(totals.get("missing_lines", 0))
    total_l = covered + missing_l
    cb = int(totals.get("covered_branches", 0))
    tb = int(totals.get("num_branches", 0))
    line_pct = round(covered / total_l * 100.0, 2) if total_l else None
    branch_pct = round(cb / tb * 100.0, 2) if tb else None
    return line_pct, branch_pct


# ---------------------------------------------------------------------------
# libFuzzer × seqan3 backend (C++ / gcov corpus-replay)
# ---------------------------------------------------------------------------
#
# Coverage model parallels the cargo-fuzz × noodles-vcf backend above, but
# uses gcov instrumentation instead of LLVM source-based coverage because
# seqan3 is a header-only C++ library and the existing
# `GcovrCollector` in test_engine/feedback/coverage_collector.py already
# speaks gcovr JSON.
#
#   * `seqan3_sam_fuzzer_libfuzzer` runs with `-fsanitize=fuzzer,address,
#     undefined` for throughput; it is NOT `--coverage`-instrumented.
#   * `seqan3_sam_fuzzer_cov` is the sibling binary, same source file,
#     built with `-g -O0 --coverage`. Its stdin-reader `main()` consumes
#     ONE file per invocation and calls `LLVMFuzzerTestOneInput`; `.gcda`
#     files accumulate next to the `.gcno` files in build-cov's CMakeFiles
#     directory.
#   * At each log tick we snapshot corpus files whose mtime ≤ `t0 + tick`
#     (seed files carry their original mtimes via shutil.copy2, so they
#     land in the earliest tick), replay the cumulative slice through
#     the cov binary, run `gcovr --gcov-executable 'llvm-cov-18 gcov'`
#     (Clang's gcov format needs llvm-cov as the frontend), and filter
#     the JSON by the three scope substrings from biotest_config.yaml.


def _prune_gcda(build_cov_dir: Path) -> None:
    for gcda in build_cov_dir.rglob("*.gcda"):
        try:
            gcda.unlink()
        except OSError:
            pass


def _libfuzzer_replay_corpus(
    cov_bin: Path,
    build_cov_dir: Path,
    files: Iterable[Path],
    per_input_timeout_s: float = 5.0,
) -> tuple[int, int]:
    """Replay `files` through the coverage binary. Returns (replayed, errors)."""
    replayed = 0
    errors = 0
    for f in files:
        try:
            with f.open("rb") as fh:
                res = subprocess.run(
                    [str(cov_bin)],
                    stdin=fh,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=str(build_cov_dir),
                    timeout=per_input_timeout_s,
                )
            replayed += 1
            if res.returncode != 0:
                errors += 1
        except subprocess.TimeoutExpired:
            errors += 1
        except OSError:
            errors += 1
    return replayed, errors


def _gcovr_json_report(
    build_cov_dir: Path, src_root: Path, out_json: Path,
) -> bool:
    """Aggregate .gcda/.gcno under build_cov_dir into a gcovr JSON report."""
    out_json.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "gcovr", "--json",
        "--root", str(src_root),
        "--gcov-executable", "llvm-cov-18 gcov",
        "--output", str(out_json),
        str(build_cov_dir),
    ]
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        logger.warning("gcovr timed out")
        return False
    if res.returncode != 0:
        logger.warning(
            "gcovr failed rc=%s: %s",
            res.returncode, res.stderr.decode(errors="replace")[:300],
        )
        return False
    return out_json.exists() and out_json.stat().st_size > 0


def _parse_gcovr_scope(
    report_path: Path, scope: tuple[str, ...],
) -> tuple[int, int, int, int, int]:
    """Return (scoped_files, covered_lines, total_lines, covered_branches, total_branches)."""
    data = json.loads(report_path.read_text(encoding="utf-8"))
    total_l = covered_l = total_b = covered_b = scoped = 0
    for f in data.get("files", []):
        name = f.get("file", "")
        if not any(k in name for k in scope):
            continue
        scoped += 1
        for line in f.get("lines", []):
            if line.get("gcovr/noncode"):
                continue
            total_l += 1
            if line.get("count", 0) > 0:
                covered_l += 1
            for br in line.get("branches", []):
                total_b += 1
                if br.get("count", 0) > 0:
                    covered_b += 1
    return scoped, covered_l, total_l, covered_b, total_b


def _run_libfuzzer_rep(
    sut: str,
    format_hint: str,
    seed_corpus: Path,
    out_rep: Path,
    time_budget_s: int,
    ticks: tuple[int, ...],
    libfuzzer_bin: Path,
    cov_bin: Path,
    cov_build_dir: Path,
    src_root: Path,
    scope: tuple[str, ...] = SEQAN3_SAM_SCOPE,
) -> list[CoverageTick]:
    """Run one libFuzzer rep + cumulative gcov corpus-replay sampling."""
    if sut != "seqan3":
        raise ValueError(f"_run_libfuzzer_rep only supports sut=seqan3, got {sut!r}")
    if format_hint.upper() != "SAM":
        raise ValueError("libFuzzer × seqan3 is SAM-only (seqan3 has no VCF parser)")

    corpus_dir = out_rep / "corpus"
    crashes_dir = out_rep / "crashes"
    log_file = out_rep / "tool.log"
    scratch_json = out_rep / "_gcovr_scratch.json"
    for d in (corpus_dir, crashes_dir):
        d.mkdir(parents=True, exist_ok=True)
    log_file.touch(exist_ok=True)
    _seed_copy(seed_corpus, corpus_dir)

    ticks_in_budget = tuple(t for t in sorted(set(ticks)) if t <= time_budget_s)
    snapshots: list[CoverageTick] = []

    logger.info(
        "rep %s: starting libfuzzer × seqan3 (budget=%ds ticks=%s)",
        out_rep.name, time_budget_s, list(ticks_in_budget),
    )

    # `-fork=1 -ignore_crashes=1` keeps libFuzzer alive across crashes
    # so coverage keeps growing throughout the budget. The default
    # behaviour (exit on first deadly signal) is documented in
    # DESIGN §13.2.4 for signal-hunting smoke tests but wrong for a
    # Phase 2 coverage-growth run — we want the fuzzer to soak the
    # full `--budget`. Fork-mode also isolates crashing inputs in a
    # child process so the parent's mutation loop keeps feeding the
    # corpus regardless of how many inputs blow up.
    cmd = [
        str(libfuzzer_bin),
        "-fork=1",
        "-ignore_crashes=1",
        f"-artifact_prefix={crashes_dir}{os.sep}",
        f"-max_total_time={time_budget_s}",
        str(corpus_dir),
    ]
    logfh = log_file.open("ab")
    proc = subprocess.Popen(
        cmd,
        stdout=logfh,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid if os.name != "nt" else None,
    )

    t0 = time.time()
    try:
        for tick in ticks_in_budget:
            target_wall = t0 + tick
            # Fork-mode libFuzzer shouldn't exit before max_total_time,
            # but if it does (e.g. SIGKILL, parent crash) we STILL keep
            # sampling ticks against the final corpus so the growth JSON
            # has one datapoint per requested tick. Plot code downstream
            # expects an uninterrupted series.
            while time.time() < target_wall:
                time.sleep(min(0.5, max(0.05, target_wall - time.time())))

            cutoff = t0 + tick
            slice_files = sorted(
                (p for p in corpus_dir.iterdir()
                 if p.is_file() and p.stat().st_mtime <= cutoff),
                key=lambda p: (p.stat().st_mtime, p.name),
            )
            measure_started = time.time()
            _prune_gcda(cov_build_dir)
            replayed, errors = _libfuzzer_replay_corpus(
                cov_bin, cov_build_dir, slice_files,
            )
            if not _gcovr_json_report(cov_build_dir, src_root, scratch_json):
                snapshots.append(CoverageTick(t_s=tick, line_pct=0.0, branch_pct=0.0))
                logger.warning(
                    "rep %s: tick t=%ds gcovr failed after replaying %d files",
                    out_rep.name, tick, replayed,
                )
                continue
            scoped, cov_l, tot_l, cov_b, tot_b = _parse_gcovr_scope(
                scratch_json, scope,
            )
            line_pct = (cov_l / tot_l * 100.0) if tot_l else 0.0
            branch_pct = (cov_b / tot_b * 100.0) if tot_b else 0.0
            snapshots.append(CoverageTick(
                t_s=tick, line_pct=line_pct, branch_pct=branch_pct,
            ))
            logger.info(
                "rep %s: tick t=%ds  replay=%d line=%.2f%% branch=%.2f%% "
                "scoped_files=%d replay_errors=%d measure=%.1fs",
                out_rep.name, tick, replayed, line_pct, branch_pct,
                scoped, errors, time.time() - measure_started,
            )
    finally:
        if proc.poll() is None:
            try:
                if os.name == "nt":
                    proc.terminate()
                else:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                logger.warning(
                    "rep %s: libfuzzer did not terminate in 30s — killing",
                    out_rep.name,
                )
                try:
                    if os.name == "nt":
                        proc.kill()
                    else:
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait(timeout=5)
        logfh.close()

    final_corpus = sum(1 for p in corpus_dir.iterdir() if p.is_file())
    crashes = sum(1 for p in crashes_dir.iterdir() if p.is_file())
    (out_rep / "adapter_result.json").write_text(json.dumps({
        "tool": "libfuzzer",
        "sut": sut,
        "time_budget_s": time_budget_s,
        "started_at": t0,
        "ended_at": time.time(),
        "corpus_dir": str(corpus_dir),
        "crashes_dir": str(crashes_dir),
        "log_file": str(log_file),
        "generated_count": final_corpus,
        "crash_count": crashes,
        "exit_code": proc.returncode if proc.returncode is not None else -1,
        "extra": {
            "binary": str(libfuzzer_bin),
            "cov_replay_binary": str(cov_bin),
            "coverage_scope": list(scope),
        },
    }, indent=2), encoding="utf-8")

    try:
        scratch_json.unlink()
    except FileNotFoundError:
        pass

    logger.info(
        "rep %s: libfuzzer done (%d ticks, final_corpus=%d crashes=%d)",
        out_rep.name, len(snapshots), final_corpus, crashes,
    )
    return snapshots


# ---------------------------------------------------------------------------
# Orchestrator (per-tool dispatch + multi-rep loop)
# ---------------------------------------------------------------------------

def _dispatch_run(
    tool: str,
    sut: str,
    format_hint: str,
    seed_corpus: Path,
    out_rep: Path,
    time_budget_s: int,
    ticks: tuple[int, ...],
    opts: argparse.Namespace,
    rep_idx: int,
) -> list[CoverageTick]:
    """Route to the per-tool backend. Today only Jazzer is implemented —
    other rows follow the same `(spawn fuzzer → dump snapshots → parse
    coverage)` pattern and land here in follow-on commits."""
    if tool == "jazzer":
        classes_dir = _ensure_htsjdk_classes_dir(
            harness_jar=Path(opts.harness_jar),
            classes_dir=Path(opts.htsjdk_classes_dir),
        )
        return _run_jazzer_rep(
            sut=sut,
            format_hint=format_hint,
            seed_corpus=seed_corpus,
            out_rep=out_rep,
            time_budget_s=time_budget_s,
            ticks=ticks,
            jazzer_bin=opts.jazzer_bin,
            harness_jar=Path(opts.harness_jar),
            classes_dir=classes_dir,
            jacocoagent_jar=Path(opts.jacocoagent_jar),
            jacococli_jar=Path(opts.jacococli_jar),
            java_bin=opts.java_bin,
            tcp_port_start=opts.jacoco_port_start + rep_idx,
            config_path=Path(opts.config),
        )
    if tool == "cargo_fuzz":
        # Build the instrumented binary once per run_cell() invocation and
        # cache it on `opts` so reps 1..N reuse it. `opts` is the argparse
        # Namespace so stashing there is safe and ephemeral per process.
        if not getattr(opts, "_cargo_fuzz_instrumented_binary", None):
            binary, instr_env = _build_instrumented_noodles_harness()
            opts._cargo_fuzz_instrumented_binary = binary
            opts._cargo_fuzz_instr_env = instr_env
        return _run_cargo_fuzz_rep(
            sut=sut,
            format_hint=format_hint,
            seed_corpus=seed_corpus,
            out_rep=out_rep,
            time_budget_s=time_budget_s,
            ticks=ticks,
            instrumented_binary=opts._cargo_fuzz_instrumented_binary,
            instr_env=opts._cargo_fuzz_instr_env,
        )
    if tool == "atheris":
        return _run_atheris_rep(
            sut=sut,
            format_hint=format_hint,
            seed_corpus=seed_corpus,
            out_rep=out_rep,
            time_budget_s=time_budget_s,
            ticks=ticks,
            opts=opts,
        )
    if tool == "libfuzzer":
        return _run_libfuzzer_rep(
            sut=sut,
            format_hint=format_hint,
            seed_corpus=seed_corpus,
            out_rep=out_rep,
            time_budget_s=time_budget_s,
            ticks=ticks,
            libfuzzer_bin=Path(opts.libfuzzer_bin),
            cov_bin=Path(opts.libfuzzer_cov_bin),
            cov_build_dir=Path(opts.libfuzzer_cov_build_dir),
            src_root=Path(opts.seqan3_src_root),
            scope=SEQAN3_SAM_SCOPE,
        )
    raise NotImplementedError(
        f"coverage_sampler does not yet support tool={tool!r} — "
        "'jazzer', 'cargo_fuzz', 'atheris', and 'libfuzzer' are wired. "
        "Add a backend alongside the existing _run_<tool>_rep functions "
        "following the same pattern."
    )


def run_cell(
    tool: str,
    sut: str,
    format_hint: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    reps: int,
    ticks: tuple[int, ...],
    opts: argparse.Namespace,
    *,
    start_rep_idx: int = 0,
) -> list[Path]:
    """Run `reps` independent reps of one (tool, SUT, format) cell and
    write a `growth_<idx>.json` per rep. Returns the list of paths.

    `start_rep_idx` lets parallel invocations claim disjoint rep slots —
    three concurrent sampler processes with `--reps 1
    --start-rep-idx {0,1,2}` produce `growth_{0,1,2}.json` under the
    same cell dir without overwriting.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    seed_hash = _hash_corpus(seed_corpus)
    paths: list[Path] = []
    for rep in range(reps):
        idx = start_rep_idx + rep
        rep_dir = out_dir / f"run_{idx}"
        rep_dir.mkdir(parents=True, exist_ok=True)
        started = time.time()
        snapshots = _dispatch_run(
            tool=tool,
            sut=sut,
            format_hint=format_hint,
            seed_corpus=seed_corpus,
            out_rep=rep_dir,
            time_budget_s=time_budget_s,
            ticks=ticks,
            opts=opts,
            rep_idx=idx,
        )
        duration = time.time() - started

        record = GrowthRecord(
            tool=tool,
            sut=sut,
            format=format_hint.upper(),
            phase="coverage",
            run_index=idx,
            time_budget_s=time_budget_s,
            seed_corpus_hash=seed_hash,
            coverage_growth=snapshots,
            extra={
                "duration_s": round(duration, 2),
                "seed_corpus_dir": str(seed_corpus.resolve()),
                "out_dir": str(rep_dir.resolve()),
                "ticks_requested": list(ticks),
            },
        )
        out_json = out_dir / f"growth_{idx}.json"
        out_json.write_text(json.dumps(record.to_json(), indent=2), encoding="utf-8")
        paths.append(out_json)
        logger.info("wrote %s (%d ticks, %.1fs)", out_json, len(snapshots), duration)
    return paths


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--tool", required=True,
                   help="fuzzer name (currently only 'jazzer' is implemented)")
    p.add_argument("--sut", required=True,
                   help="SUT name (e.g. htsjdk)")
    p.add_argument("--format", required=True, choices=["VCF", "SAM"],
                   help="corpus format — drives harness target_class + scope")
    p.add_argument("--seed-corpus", type=Path, required=True,
                   help="directory of seed files (flat-copied into each rep's corpus)")
    p.add_argument("--out", type=Path, required=True,
                   help="output directory; growth_<idx>.json files land here")
    p.add_argument("--budget", type=int, default=7200,
                   help="wall-clock budget per rep, seconds (DESIGN §3.2 primary = 7200)")
    p.add_argument("--reps", type=int, default=3,
                   help="independent reps (DESIGN §3.2 primary = 3)")
    p.add_argument("--ticks", type=str, default=",".join(str(t) for t in DEFAULT_TICKS_S),
                   help="comma-separated tick seconds (DESIGN §3.2 default = 1,10,60,300,1800,7200)")

    p.add_argument("--jazzer-bin", default=JAZZER_BIN_DEFAULT,
                   help="path to the `jazzer` native launcher")
    p.add_argument("--harness-jar", default=str(JAZZER_JAR),
                   help="path to the BioTest Jazzer harness fatjar")
    p.add_argument("--htsjdk-classes-dir", default=str(HTSJDK_CLASSES_DIR_DEFAULT),
                   help="directory to unpack htsjdk/*.class into for JaCoCo --classfiles (auto-created)")
    p.add_argument("--jacocoagent-jar", default=str(JACOCOAGENT_JAR),
                   help="path to jacocoagent.jar")
    p.add_argument("--jacococli-jar", default=str(JACOCOCLI_JAR),
                   help="path to jacococli.jar")
    p.add_argument("--java-bin", default="java",
                   help="java binary to run jacococli with (CLI only; Jazzer uses its own JDK)")
    p.add_argument("--jacoco-port-start", type=int, default=6300,
                   help="TCP port the agent binds to; rep N uses start+N")
    p.add_argument("--config", default=str(REPO_ROOT / "biotest_config.yaml"),
                   help="Path to biotest_config.yaml — the single source of "
                        "truth for coverage.target_filters (the fairness "
                        "recipe, see compares/scripts/measure_coverage.py). "
                        "Change filter rules there, not here.")

    p.add_argument("--atheris-image", default="biotest-bench:latest",
                   help="Docker image holding the Atheris-venv; used by "
                        "the atheris backend.")
    p.add_argument("--atheris-python", default="/opt/atheris-venv/bin/python",
                   help="Path (inside the atheris image) to the Python 3.11 "
                        "interpreter that hosts atheris + vcfpy + coverage.py.")
    p.add_argument("--atheris-harness",
                   default=None,
                   help="Repo-relative path to the coverage-aware atheris "
                        "harness. Defaults to fuzz_vcfpy.py for sut=vcfpy "
                        "and fuzz_biopython.py for sut=biopython.")

    p.add_argument("--libfuzzer-bin",
                   default=str(LIBFUZZER_BIN_DEFAULT),
                   help="Path to the throughput libFuzzer binary "
                        "(seqan3_sam_fuzzer_libfuzzer).")
    p.add_argument("--libfuzzer-cov-bin",
                   default=str(LIBFUZZER_COV_BIN_DEFAULT),
                   help="Path to the --coverage-instrumented replay binary "
                        "(seqan3_sam_fuzzer_cov). Built separately with "
                        "`bash compares/scripts/build_harnesses.sh libfuzzer_cov`.")
    p.add_argument("--libfuzzer-cov-build-dir",
                   default=str(LIBFUZZER_COV_BUILD_DIR_DEFAULT),
                   help="Build directory that holds the cov binary's .gcno/.gcda "
                        "files; `.gcda` files are pruned before each tick replay.")
    p.add_argument("--seqan3-src-root",
                   default=str(SEQAN3_SRC_ROOT_DEFAULT),
                   help="Seqan3 source root passed to gcovr --root. Inside "
                        "biotest-bench this is /opt/seqan3/include.")

    p.add_argument("--verbose", action="store_true")
    p.add_argument("--start-rep-idx", type=int, default=0,
                   help="Starting index for growth_<idx>.json / run_<idx>/ "
                        "sub-directories. Use with --reps 1 across three "
                        "concurrent sampler processes to collect three "
                        "parallel reps into the same cell dir without "
                        "overwriting each other.")

    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    try:
        ticks = tuple(sorted({int(x) for x in args.ticks.split(",") if x.strip()}))
    except ValueError:
        logger.error("bad --ticks value %r", args.ticks)
        return 2

    # Hard-fail early if required artefacts for this tool are missing —
    # otherwise the first rep burns its full budget only to find tooling
    # absent. Per-tool prereq lists so --tool cargo_fuzz doesn't demand
    # the JaCoCo fat jars and vice versa.
    if args.tool == "jazzer":
        required = [Path(args.harness_jar), Path(args.jacocoagent_jar),
                    Path(args.jacococli_jar)]
    elif args.tool == "cargo_fuzz":
        required = [NOODLES_MANIFEST]
    elif args.tool == "libfuzzer":
        required = [Path(args.libfuzzer_bin), Path(args.libfuzzer_cov_bin),
                    Path(args.libfuzzer_cov_build_dir),
                    Path(args.seqan3_src_root)]
        if shutil.which("gcovr") is None:
            logger.error("gcovr not on PATH — install gcovr or run inside biotest-bench")
            return 2
        if shutil.which("llvm-cov-18") is None:
            logger.error("llvm-cov-18 not on PATH — Clang's gcov output needs llvm-cov-18 as the frontend")
            return 2
    else:
        required = []
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        logger.error("missing required artefacts for tool=%s: %s", args.tool, missing)
        return 2

    paths = run_cell(
        tool=args.tool,
        sut=args.sut,
        format_hint=args.format,
        seed_corpus=args.seed_corpus,
        out_dir=args.out,
        time_budget_s=args.budget,
        reps=args.reps,
        ticks=ticks,
        opts=args,
        start_rep_idx=args.start_rep_idx,
    )
    print(f"[coverage_sampler] wrote {len(paths)} growth file(s):")
    for p in paths:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
