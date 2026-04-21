"""Phase-4 orchestrator for the real-bug benchmark.

Modes:
    --verify-only        pre-flight install-verification only (no fuzzing)
    (default)            full bug-bench run

For every verified bug in the manifest, for every tool eligible for the
bug's SUT row (see DESIGN.md §4.1):
    1. Install the pre-fix SUT version (pip / Maven / git checkout).
    2. Run the tool for --time-budget-s seconds against the pre-fix SUT.
    3. Record TTFB + detection outcome.
    4. Install the post-fix version; replay the detecting input;
       confirm the signal disappears.
    5. Write per-(tool, bug) JSON under --out.

The tool-adapter contract is defined in `tool_adapters/_base.py`.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTERS_DIR = REPO_ROOT / "compares" / "scripts" / "tool_adapters"

# Python SUT install venvs live under compares/results/sut-envs/. These
# were created by compares/scripts/prepare_sut_install_envs.sh. Routing
# `pip install pysam==<old-version>` through the Python 3.11 venv (not
# 3.12) is required because pre-0.21 pysam has no 3.12 wheels and its
# sdist build has dependency-rot on modern setuptools.
SUT_VENV_PYSAM_PIP = (REPO_ROOT / "compares" / "results" / "sut-envs"
                      / "pysam" / "bin" / "pip")
SUT_VENV_PYSAM_PY = (REPO_ROOT / "compares" / "results" / "sut-envs"
                     / "pysam" / "bin" / "python")
SUT_VENV_BIO_PIP = (REPO_ROOT / "compares" / "results" / "sut-envs"
                    / "biopython" / "bin" / "pip")
SUT_VENV_BIO_PY = (REPO_ROOT / "compares" / "results" / "sut-envs"
                   / "biopython" / "bin" / "python")
# vcfpy venv — created 2026-04-20 by prepare_sut_install_envs.sh.
# Same 3.11 interpreter family as pysam/biopython.
SUT_VENV_VCFPY_PIP = (REPO_ROOT / "compares" / "results" / "sut-envs"
                      / "vcfpy" / "bin" / "pip")
SUT_VENV_VCFPY_PY = (REPO_ROOT / "compares" / "results" / "sut-envs"
                     / "vcfpy" / "bin" / "python")
# noodles-vcf — version swap rewrites BOTH Cargo.toml files so the
# canonical-JSON harness and the cargo-fuzz target stay on the same
# noodles-vcf crate version. Both rebuild in the same helper call.
NOODLES_HARNESS_DIR = (REPO_ROOT / "harnesses" / "rust" / "noodles_harness")
NOODLES_CARGO_TOML = NOODLES_HARNESS_DIR / "Cargo.toml"
NOODLES_FUZZ_DIR = (REPO_ROOT / "compares" / "harnesses" / "cargo_fuzz" / "fuzz")
NOODLES_FUZZ_CARGO_TOML = NOODLES_FUZZ_DIR / "Cargo.toml"

# Ensure adapter module imports resolve.
sys.path.insert(0, str(ADAPTERS_DIR))

# Row membership per DESIGN.md §4.1 slim matrix. seqan3 uses libFuzzer
# (Clang 18 + in-tree seqan3 patches; DESIGN §13.2.4). AFL++ is an
# alternate on the same harness source — swap "libfuzzer" → "aflpp"
# here if the Clang build ever regresses.
MATRIX: dict[str, list[str]] = {
    "htsjdk":    ["biotest", "jazzer", "pure_random", "evosuite_anchor"],
    "vcfpy":     ["biotest", "atheris", "pure_random"],
    "noodles":   ["biotest", "cargo_fuzz", "pure_random"],
    "biopython": ["biotest", "atheris", "pure_random"],
    "seqan3":    ["biotest", "libfuzzer", "pure_random"],
    # pysam is retained as a voter in the differential/consensus oracle
    # (see DESIGN §2.6 + §9 Risk 4). It is NOT a scored primary SUT any
    # more, so no MATRIX row — bug_bench_driver skips SUTs absent from
    # MATRIX. Historical pysam-era bugs live in Appendix A.6.
}


@dataclass
class BugResult:
    tool: str
    bug_id: str
    sut: str
    detected: bool
    ttfb_s: float | None
    trigger_input: str | None
    signal: str | None
    confirmed_fix_silences_signal: bool | None
    adapter_exit_code: int
    notes: str = ""


# ---------- SUT install helpers ---------------------------------------

def _install_pysam(version: str) -> None:
    # Route through the sut-env Python 3.11 venv because pre-0.21 pysam
    # has no modern Python wheels. On a fresh host without the venv,
    # run `bash compares/scripts/prepare_sut_install_envs.sh` first.
    if not SUT_VENV_PYSAM_PIP.exists():
        raise RuntimeError(
            f"pysam sut-env venv missing at {SUT_VENV_PYSAM_PIP.parent.parent}. "
            "Run: bash compares/scripts/prepare_sut_install_envs.sh")
    subprocess.run(
        [str(SUT_VENV_PYSAM_PIP), "install", "--force-reinstall",
         f"pysam=={version}"],
        check=True, capture_output=True,
    )


def _install_biopython(version: str) -> None:
    if not SUT_VENV_BIO_PIP.exists():
        raise RuntimeError(
            f"biopython sut-env venv missing at {SUT_VENV_BIO_PIP.parent.parent}. "
            "Run: bash compares/scripts/prepare_sut_install_envs.sh")
    # Skip the expensive pip install when the venv already has the right
    # version. The sut-env lives on the 9p /work share and hits
    # `[Errno 12] Cannot allocate memory` under multi-chat I/O pressure
    # on Windows Docker Desktop.
    py = SUT_VENV_BIO_PIP.parent / "python"
    probe = subprocess.run(
        [str(py), "-c",
         "import Bio, numpy; print(Bio.__version__)"],
        capture_output=True, text=True,
    )
    if probe.returncode == 0 and probe.stdout.strip() == version:
        return
    subprocess.run(
        [str(SUT_VENV_BIO_PIP), "install", "--force-reinstall",
         f"biopython=={version}"],
        check=True, capture_output=True,
    )


def _install_vcfpy(version: str) -> None:
    """Pip --force-reinstall vcfpy into /opt/atheris-venv.

    Targets the atheris venv on the container's overlay FS rather than
    the /work-mounted sut-env. The atheris adapter invokes its fuzzer
    with /opt/atheris-venv/bin/python (see compares/scripts/tool_adapters/
    run_atheris.py), so installing there keeps the pre-fix pin coherent
    with the interpreter actually doing the fuzzing. The /work-mounted
    venv additionally hits `[Errno 12] Cannot allocate memory` under
    concurrent multi-chat I/O pressure on Windows Docker Desktop's 9p
    share, which the overlay FS sidesteps entirely.
    """
    pip = Path("/opt/atheris-venv/bin/pip")
    if not pip.exists():
        raise RuntimeError(
            f"atheris venv pip missing at {pip}. "
            "Run the bench image with the atheris layer.")
    # --no-build-isolation lets pip use the atheris venv's already-installed
    # setuptools/wheel rather than spin up a clean build env every time,
    # which is the surface that fails in the 9p/sut-env regime.
    cmd = [str(pip), "install", "--force-reinstall",
           "--no-build-isolation", f"vcfpy=={version}"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        return
    # PyPI install failed. Some old vcfpy releases either
    #   (a) are not on PyPI at all (≤0.8.x were git-only), or
    #   (b) have a setup.py that imports the removed pip.req API (≤0.11.0).
    # Fall back to cloning from GitHub and patching setup.py before install.
    stderr = proc.stderr or ""
    fall_back = (
        "No matching distribution found" in stderr
        or "No module named 'pip.req'" in stderr
    )
    if not fall_back:
        raise subprocess.CalledProcessError(
            proc.returncode, cmd, output=proc.stdout, stderr=stderr,
        )
    _install_vcfpy_from_git(version, pip)


def _install_vcfpy_from_git(version: str, pip: Path) -> None:
    """Clone vcfpy from GitHub, patch setup.py, and install from the work tree.

    Two failure modes addressed:
    - 0.11.0-era setup.py imports ``from pip.req import parse_requirements``
      and ``pip.download.PipSession`` which modern pip no longer exposes.
      We swap the imports for a minimal pure-python requirements reader.
    - 0.8.x releases were never published to PyPI; the GitHub tag ``vX.Y.Z``
      is their only distribution surface.
    """
    import re
    import shutil
    workdir = Path(f"/tmp/vcfpy-build-{version}")
    if workdir.exists():
        shutil.rmtree(workdir)
    subprocess.run(
        ["git", "clone", "--depth", "5", "--branch", f"v{version}",
         "https://github.com/bihealth/vcfpy", str(workdir)],
        check=True, capture_output=True,
    )
    setup_py = workdir / "setup.py"
    text = setup_py.read_text(encoding="utf-8")
    if "from pip.req" in text:
        text = text.replace(
            "import pip\nfrom pip.req import parse_requirements\n",
            "",
        )
        text = text.replace(
            "import versioneer",
            "def _parse_reqs(path):\n"
            "    import os\n"
            "    if not os.path.exists(path):\n"
            "        return []\n"
            "    out = []\n"
            "    with open(path) as f:\n"
            "        for line in f:\n"
            "            line = line.split(\"#\", 1)[0].strip()\n"
            "            if line and not line.startswith(\"-\"):\n"
            "                out.append(line)\n"
            "    return out\n\n"
            "import versioneer",
        )
        text = re.sub(
            r"parse_requirements\(\s*([^,]+?),"
            r"\s*session=pip\.download\.PipSession\(\)\s*\)",
            r"_parse_reqs(\1)",
            text,
        )
        text = re.sub(
            r"\[\s*str\(ir\.req\)\s+for\s+ir\s+in\s+(.+?)\s*\]",
            r"list(\1)",
            text,
            flags=re.DOTALL,
        )
        text = text.replace("\nimport pip\n", "\n")
        setup_py.write_text(text, encoding="utf-8")
    subprocess.run(
        [str(pip), "install", "--force-reinstall",
         "--no-build-isolation", str(workdir)],
        check=True, capture_output=True,
    )


def _rewrite_noodles_pin(cargo_toml: Path, version: str) -> None:
    """Rewrite the `noodles-vcf = ...` version pin in a Cargo.toml file.

    Idempotent: if the pin is already the target version, this is a no-op
    and the function returns successfully. A prior bug (fixed 2026-04-20)
    treated "text unchanged after re.sub" as "regex didn't match", which
    produced spurious "could not find version pin" errors whenever the
    anchor group's target version happened to equal the current pin.
    """
    import re
    text = cargo_toml.read_text(encoding="utf-8")
    patterns = [
        (r'(noodles-vcf\s*=\s*")[^"]+(")',
         rf'\g<1>{version}\g<2>'),
        (r'(noodles-vcf\s*=\s*\{[^}]*version\s*=\s*")[^"]+(")',
         rf'\g<1>{version}\g<2>'),
    ]
    new_text = text
    total_subs = 0
    for pat, repl in patterns:
        new_text, n = re.subn(pat, repl, new_text)
        total_subs += n
    if total_subs == 0:
        raise RuntimeError(
            f"could not find noodles-vcf version pin in {cargo_toml}")
    if new_text != text:
        cargo_toml.write_text(new_text, encoding="utf-8")


def _install_noodles(version: str) -> None:
    """Pin noodles-vcf = "<version>" in BOTH Cargo.tomls and rebuild.

    Added 2026-04-20. Rewrites the canonical-JSON harness AND the
    cargo-fuzz target so they stay on the same crate version, then
    runs `cargo build --release` on each. Incremental cargo keeps
    per-swap wall-time ≤ 30-60 s after the first build.

    If the cargo-fuzz target hasn't been scaffolded yet, only the
    canonical-JSON harness is rewritten — the driver still works on
    the canonical-JSON side and the cargo-fuzz adapter will surface
    its own "binary not built" error at adapter-invoke time.
    """
    if not NOODLES_CARGO_TOML.exists():
        raise RuntimeError(
            f"noodles harness Cargo.toml missing at {NOODLES_CARGO_TOML}. "
            "Run: bash compares/scripts/prepare_sut_install_envs.sh")

    # Primary harness (canonical-JSON). Always rewrite + rebuild.
    _rewrite_noodles_pin(NOODLES_CARGO_TOML, version)
    # cargo ships under /root/.cargo/bin inside biotest-bench:latest;
    # docker exec doesn't inherit login-shell PATH, so subprocess lookup
    # fails without this prepend (fixed 2026-04-20).
    env = os.environ.copy()
    env["PATH"] = f"/root/.cargo/bin:{env.get('PATH', '')}"
    subprocess.run(
        ["cargo", "build", "--release",
         "--manifest-path", str(NOODLES_CARGO_TOML)],
        check=True, capture_output=True, env=env,
    )

    # cargo-fuzz target. Best-effort: if the fuzz Cargo.toml exists,
    # keep its pin in sync. The `cargo fuzz build` rebuild is left to
    # adapter-invoke time (cargo-fuzz needs Clang + its own wrapper).
    if NOODLES_FUZZ_CARGO_TOML.exists():
        try:
            _rewrite_noodles_pin(NOODLES_FUZZ_CARGO_TOML, version)
        except RuntimeError:
            pass  # no pin present; don't fail the whole install swap


def _install_htsjdk_jar(version: str, out_path: Path) -> None:
    """Download the versioned htsjdk JAR from Maven Central."""
    url = ("https://repo.maven.apache.org/maven2/com/github/samtools/htsjdk/"
           f"{version}/htsjdk-{version}.jar")
    subprocess.run(["curl", "-L", "-o", str(out_path), url], check=True)


def _checkout_seqan3(commit: str, seqan3_src_dir: Path) -> None:
    # Resolve rev-spec (e.g. "edbfa956f^") to a concrete SHA first — otherwise
    # git checkout mis-interprets "^"/"~" as a pathspec and fails.
    resolved = subprocess.run(
        ["git", "-C", str(seqan3_src_dir), "rev-parse", commit],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    subprocess.run(
        ["git", "-C", str(seqan3_src_dir), "checkout", "-f", resolved],
        check=True,
    )


def install_sut(sut: str, anchor: dict[str, Any], which: str) -> None:
    """Install the pre-fix or post-fix SUT version in the current env."""
    if anchor.get("type") == "feature_gap":
        raise RuntimeError("feature_gap entries should be pre-filtered out")
    version = anchor[which]
    if version in ("PENDING_VERIFICATION", "N/A") or "PENDING" in str(version):
        raise RuntimeError(
            f"anchor.{which}={version!r} is unverified; run --verify-only first")

    if sut == "pysam":
        _install_pysam(version)
    elif sut == "biopython":
        _install_biopython(version)
    elif sut == "vcfpy":
        _install_vcfpy(version)
    elif sut == "noodles":
        _install_noodles(version)
    elif sut == "htsjdk":
        # Drop the versioned JAR into a known path the htsjdk runner uses.
        dest = REPO_ROOT / "compares" / "baselines" / "evosuite" / "fatjar" / (
            f"htsjdk-{version}.jar")
        dest.parent.mkdir(parents=True, exist_ok=True)
        _install_htsjdk_jar(version, dest)
    elif sut == "seqan3":
        seqan3_src = REPO_ROOT / "compares" / "baselines" / "seqan3" / "source"
        if not seqan3_src.exists():
            raise RuntimeError(
                f"seqan3 source not found at {seqan3_src}; clone first")
        _checkout_seqan3(version, seqan3_src)
    else:
        raise RuntimeError(f"unknown sut: {sut}")


# ---------- Verification ----------------------------------------------

def verify_bug(bug: dict[str, Any], *, install: bool = False) -> tuple[bool, str]:
    """Check bug is runnable. If `install=True`, also exercise both
    pre-fix and post-fix installs (slow — only used in --verify-only).

    Default behaviour (install=False) is a metadata-only check: we
    confirm the anchor is present and not marked PENDING/feature_gap.
    The main anchor-grouped loop (run_bench) handles real install
    failures by wrapping install_sut in a try/except and recording a
    cell-level error record — so preflight-installing every bug here
    would just double the install-swap count for no gain.
    """
    anchor = bug["anchor"]
    if anchor.get("type") == "feature_gap":
        return False, "feature_gap: drop"
    pre = anchor.get("pre_fix", "")
    post = anchor.get("post_fix", "")
    if "PENDING" in pre or "PENDING" in post or pre in ("", "N/A") or post in ("", "N/A"):
        return False, (
            f"pending verification (pre_fix={pre!r} post_fix={post!r}); "
            f"rule: {anchor.get('verification_rule')}"
        )

    if install:
        try:
            install_sut(bug["sut"], anchor, "pre_fix")
            install_sut(bug["sut"], anchor, "post_fix")
        except Exception as e:
            return False, f"install failed: {e}"
        return True, "installable"
    return True, "anchor ok"


# ---------- Adapter dispatch ------------------------------------------

def _build_merged_seed_corpus(
    general_seeds: Path, bug: dict[str, Any], out_dir: Path,
) -> Path:
    """Materialize a per-cell seed corpus = general seeds ∪ bug PoV.

    PoV-seed injection is standard Magma / FuzzBench practice when the
    benchmark's purpose is detection attribution rather than discovery
    from scratch. Rationale + citation in PHASE4_BASELINE_FIXES.md §0.4.
    The merged dir lives at `<out_dir>/seeds_merged/` so it's auditable
    per cell. Uses symlinks where possible (fast, zero-copy) and falls
    back to shutil.copy2 on file systems that disallow symlinks.
    """
    merged = out_dir / "seeds_merged"
    merged.mkdir(parents=True, exist_ok=True)

    if general_seeds.is_dir():
        for src in general_seeds.iterdir():
            if src.is_file():
                dst = merged / src.name
                if dst.exists():
                    continue
                try:
                    os.symlink(src, dst)
                except OSError:
                    shutil.copy2(src, dst)

    pov_dir = REPO_ROOT / "compares" / "bug_bench" / "triggers" / bug["id"]
    fmt = bug.get("format", "VCF").lower()
    pov_added = 0
    if pov_dir.is_dir():
        # Accept original.vcf / original.sam / original.bam for SAM-row
        # bugs that prefer binary PoVs.
        candidates = list(pov_dir.glob(f"original.{fmt}"))
        if fmt == "sam":
            candidates.extend(pov_dir.glob("original.bam"))
        for pov in candidates:
            if not pov.is_file():
                continue
            dst = merged / f"pov_{bug['id']}_{pov.name}"
            if dst.exists():
                continue
            try:
                os.symlink(pov, dst)
            except OSError:
                shutil.copy2(pov, dst)
            pov_added += 1
    print(f"[pov] {bug['id']}: seeds_merged={merged} pov_added={pov_added}")
    return merged


def invoke_adapter(
    tool: str, bug: dict[str, Any], out_dir: Path, time_budget_s: int,
    seed_corpus: Path,
) -> dict[str, Any]:
    """Dispatch to the named adapter; return its JSON result."""
    if tool == "biotest":
        from run_biotest import run as _run  # type: ignore
    elif tool == "jazzer":
        from run_jazzer import run as _run  # type: ignore
    elif tool == "atheris":
        from run_atheris import run as _run  # type: ignore
    elif tool == "libfuzzer":
        from run_libfuzzer import run as _run  # type: ignore
    elif tool == "aflpp":
        from run_aflpp import run as _run  # type: ignore
    elif tool == "cargo_fuzz":
        from run_cargo_fuzz import run as _run  # type: ignore
    elif tool == "pure_random":
        from run_pure_random import run as _run  # type: ignore
    elif tool == "evosuite_anchor":
        # Delegate to the existing shell-based EvoSuite pipeline.
        # EvoSuite generates JUnit cases, not bytes — seed corpus is
        # unused, PoV injection is a no-op for this adapter.
        return _invoke_evosuite_anchor(bug, out_dir, time_budget_s)
    else:
        raise RuntimeError(f"unknown tool {tool!r}")

    merged_seeds = _build_merged_seed_corpus(seed_corpus, bug, out_dir)
    result = _run(
        sut=bug["sut"],
        seed_corpus=merged_seeds,
        out_dir=out_dir,
        time_budget_s=time_budget_s,
        format_hint=bug.get("format", "VCF"),
    )
    return result.to_json()


def _invoke_evosuite_anchor(
    bug: dict[str, Any], out_dir: Path, time_budget_s: int
) -> dict[str, Any]:
    script = REPO_ROOT / "compares" / "scripts" / "run_evosuite.sh"
    log_file = out_dir / "tool.log"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_file.touch()
    started = time.time()
    try:
        subprocess.run(
            ["bash", str(script), "--budget", str(time_budget_s),
             "--out", str(out_dir)],
            timeout=time_budget_s + 60, check=False,
            stdout=log_file.open("ab"), stderr=subprocess.STDOUT,
        )
        exit_code = 0
    except subprocess.TimeoutExpired:
        exit_code = -1
    except Exception:
        exit_code = 1
    ended = time.time()
    return {
        "tool": "evosuite_anchor",
        "sut": bug["sut"],
        "exit_code": exit_code,
        "started_at": started,
        "ended_at": ended,
        "corpus_dir": str(out_dir / "evosuite-tests"),
        "crashes_dir": str(out_dir / "failing-tests"),
        "log_file": str(log_file),
    }


# ---------- Detection predicate ---------------------------------------

def detection_from_adapter(
    adapter_json: dict[str, Any], bug: dict[str, Any],
) -> tuple[bool, float | None, str | None, str | None]:
    """Compute (detected, ttfb_s, trigger_input_path, signal) from adapter output.

    This is a minimal implementation. For a crash-finding tool we trust
    the adapter's crash count. For BioTest we would additionally parse
    its DET report — TODO hook that up during Phase-0 smoke test.
    """
    crashes = adapter_json.get("crash_count", 0)
    if crashes > 0:
        duration = float(adapter_json.get("ended_at", 0)
                         - adapter_json.get("started_at", 0))
        # TTFB estimation: without per-crash timestamps we use mid-point.
        ttfb = duration * 0.5
        crashes_dir = Path(adapter_json.get("crashes_dir", ""))
        sample = next(iter(crashes_dir.glob("*"))) if crashes_dir.exists() else None
        return (
            True,
            ttfb,
            str(sample) if sample else None,
            bug.get("expected_signal", {}).get("type", "crash"),
        )
    return False, None, None, None


# ---------- Main loop -------------------------------------------------

def _group_by_anchor(bugs: list[dict[str, Any]]) -> dict[tuple, list[dict[str, Any]]]:
    """Group bugs by shared (sut, anchor-type, pre_fix, post_fix).

    Halves install-swap overhead: bugs that share an anchor install
    pre_fix once, run all their tools, then install post_fix once for
    the replay-silencing sweep. See DESIGN.md §13.5 Phase 4.
    """
    from collections import OrderedDict
    groups: dict[tuple, list[dict[str, Any]]] = OrderedDict()
    for bug in bugs:
        a = bug["anchor"]
        key = (bug["sut"], a.get("type"), a.get("pre_fix"), a.get("post_fix"))
        groups.setdefault(key, []).append(bug)
    return groups


def run_bench(
    manifest_path: Path,
    out_root: Path,
    time_budget_s: int,
    seed_corpus_vcf: Path,
    seed_corpus_sam: Path,
    only_sut: str | None = None,
    only_tool: str | None = None,
    only_bug: str | None = None,
) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out_root.mkdir(parents=True, exist_ok=True)
    aggregate: list[dict[str, Any]] = []

    # Filter once up-front; anchor-group the survivors.
    candidates: list[dict[str, Any]] = []
    for bug in manifest.get("bugs", []):
        if only_sut and bug["sut"] != only_sut:
            continue
        if only_bug and bug["id"] != only_bug:
            continue
        ok, reason = verify_bug(bug)
        if not ok:
            print(f"[skip] {bug['id']}: {reason}")
            continue
        candidates.append(bug)

    anchor_groups = _group_by_anchor(candidates)
    print(f"[orchestrator] {len(candidates)} bug(s) in {len(anchor_groups)} "
          f"anchor group(s) — "
          f"{2 * len(anchor_groups)} install-swaps (vs "
          f"{2 * len(candidates)} without grouping)")

    for (sut, _atype, pre, post), group_bugs in anchor_groups.items():
        print(f"\n[group] {sut}  {pre} -> {post}  ({len(group_bugs)} bug(s))")

        # ---- Phase A: install pre_fix once, run all tools on all bugs --
        try:
            install_sut(sut, group_bugs[0]["anchor"], "pre_fix")
        except Exception:
            traceback.print_exc()
            for bug in group_bugs:
                aggregate.append({
                    "bug_id": bug["id"], "sut": sut,
                    "error": f"install pre_fix {pre} failed",
                })
            continue

        # bug_id -> list of (tool, adapter_json, detected, ttfb, trig, sig)
        group_records: dict[str, list[dict[str, Any]]] = {b["id"]: [] for b in group_bugs}

        for bug in group_bugs:
            seed_corpus = (
                seed_corpus_vcf if bug.get("format") == "VCF" else seed_corpus_sam)
            for tool in MATRIX.get(sut, []):
                if only_tool and tool != only_tool:
                    continue
                tool_out = out_root / tool / bug["id"]
                tool_out.mkdir(parents=True, exist_ok=True)
                print(f"[run] {tool} @ {bug['id']}  t={time_budget_s}s")
                try:
                    adapter_json = invoke_adapter(
                        tool, bug, tool_out, time_budget_s, seed_corpus,
                    )
                except Exception:
                    traceback.print_exc()
                    adapter_json = {"exit_code": 99, "error": "adapter_raise"}

                detected, ttfb, trig, sig = detection_from_adapter(adapter_json, bug)
                group_records[bug["id"]].append({
                    "tool": tool, "adapter_json": adapter_json,
                    "detected": detected, "ttfb": ttfb,
                    "trig": trig, "sig": sig, "tool_out": tool_out,
                })

        # ---- Phase B: install post_fix once, replay every detection ---
        any_needs_replay = any(
            r["detected"] and r["trig"]
            for recs in group_records.values() for r in recs
        )
        if any_needs_replay:
            try:
                install_sut(sut, group_bugs[0]["anchor"], "post_fix")
                replay_available = True
            except Exception:
                traceback.print_exc()
                replay_available = False
        else:
            replay_available = False

        for bug in group_bugs:
            fmt = bug.get("format", "VCF")
            for r in group_records[bug["id"]]:
                confirmed = None
                if r["detected"] and r["trig"] and replay_available:
                    try:
                        confirmed = _replay_trigger_silenced(
                            sut, Path(r["trig"]), fmt)
                    except Exception:
                        traceback.print_exc()
                        confirmed = None
                record = BugResult(
                    tool=r["tool"], bug_id=bug["id"], sut=sut,
                    detected=r["detected"], ttfb_s=r["ttfb"],
                    trigger_input=r["trig"], signal=r["sig"],
                    confirmed_fix_silences_signal=confirmed,
                    adapter_exit_code=int(r["adapter_json"].get("exit_code", 0)),
                )
                (r["tool_out"] / "result.json").write_text(
                    json.dumps(asdict(record), indent=2), encoding="utf-8"
                )
                aggregate.append(asdict(record))

    (out_root / "aggregate.json").write_text(
        json.dumps({"results": aggregate}, indent=2), encoding="utf-8"
    )
    print(f"[done] wrote {len(aggregate)} records to "
          f"{out_root/'aggregate.json'}")


def _replay_trigger_silenced(sut: str, trig_path: Path, fmt: str) -> bool:
    """Re-run the triggering input against the post-fix SUT; return True
    iff the signal has vanished."""
    # Minimal: call the repo's existing ParserRunner and check success.
    sys.path.insert(0, str(REPO_ROOT))
    try:
        if sut == "pysam":
            from test_engine.runners.pysam_runner import PysamRunner  # type: ignore
            r = PysamRunner().run(trig_path, fmt)
        elif sut == "biopython":
            from test_engine.runners.biopython_runner import BiopythonRunner  # type: ignore
            r = BiopythonRunner().run(trig_path, fmt)
        elif sut == "vcfpy":
            py = "/opt/atheris-venv/bin/python"
            proc = subprocess.run(
                [py, "-c",
                 "import sys, vcfpy\n"
                 "try:\n"
                 "    with vcfpy.Reader.from_path(sys.argv[1]) as r:\n"
                 "        [_ for _ in r]\n"
                 "except Exception:\n"
                 "    sys.exit(1)\n",
                 str(trig_path)],
                capture_output=True, timeout=30,
            )
            return proc.returncode == 0
        elif sut == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner  # type: ignore
            r = HTSJDKRunner().run(trig_path, fmt)
        elif sut == "seqan3":
            from test_engine.runners.seqan3_runner import SeqAn3Runner  # type: ignore
            r = SeqAn3Runner().run(trig_path, fmt)
        elif sut == "noodles":
            import subprocess
            binary = (REPO_ROOT / "harnesses" / "rust" / "noodles_harness"
                      / "target" / "release" / "noodles_harness")
            if not binary.exists():
                return None  # type: ignore[return-value]
            proc = subprocess.run(
                [str(binary), str(trig_path)],
                capture_output=True, timeout=30,
            )
            return proc.returncode == 0
        else:
            return False
        # Silenced means: post-fix SUT handles the trigger cleanly.
        return bool(r.success)
    finally:
        sys.path.pop(0)


def _verify_only(manifest_path: Path, out_path: Path | None) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    verified: list[str] = []
    dropped: list[dict[str, str]] = []
    for bug in manifest.get("bugs", []):
        # --verify-only explicitly wants to exercise both installs.
        ok, reason = verify_bug(bug, install=True)
        if ok:
            verified.append(bug["id"])
            print(f"[ok]   {bug['id']}")
        else:
            dropped.append({"id": bug["id"], "reason": reason})
            print(f"[drop] {bug['id']}: {reason}")
    print(f"\nSummary: {len(verified)} verified, {len(dropped)} dropped "
          f"of {len(manifest.get('bugs', []))} candidates.")
    if out_path:
        out_path.write_text(
            json.dumps({"verified": verified, "dropped": dropped}, indent=2),
            encoding="utf-8",
        )


# ---------- CLI -------------------------------------------------------

def _cli() -> None:
    p = argparse.ArgumentParser(description="Phase-4 bug-bench orchestrator")
    p.add_argument("--manifest", type=Path,
                   default=REPO_ROOT/"compares"/"bug_bench"/"manifest.json")
    p.add_argument("--out", type=Path,
                   default=REPO_ROOT/"compares"/"results"/"bug_bench")
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--seed-corpus-vcf", type=Path,
                   default=REPO_ROOT/"seeds"/"vcf")
    p.add_argument("--seed-corpus-sam", type=Path,
                   default=REPO_ROOT/"seeds"/"sam")
    p.add_argument("--only-sut", default=None,
                   help="Run only bugs for this SUT (htsjdk, pysam, biopython, seqan3)")
    p.add_argument("--only-tool", default=None,
                   help="Run only this tool (biotest, jazzer, atheris, libfuzzer, pure_random, evosuite_anchor)")
    p.add_argument("--only-bug", default=None,
                   help="Run only this bug id (e.g. pysam-1308) — useful for iterative debugging")
    p.add_argument("--verify-only", action="store_true")
    p.add_argument("--dropped-out", type=Path, default=None,
                   help="write a verify summary JSON to this path")
    args = p.parse_args()

    if args.verify_only:
        _verify_only(args.manifest, args.dropped_out)
        return

    run_bench(
        manifest_path=args.manifest,
        out_root=args.out,
        time_budget_s=args.time_budget_s,
        seed_corpus_vcf=args.seed_corpus_vcf,
        seed_corpus_sam=args.seed_corpus_sam,
        only_sut=args.only_sut,
        only_tool=args.only_tool,
        only_bug=args.only_bug,
    )


if __name__ == "__main__":
    _cli()
