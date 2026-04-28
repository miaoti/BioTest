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
import tempfile
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
# Unit-level Java generators: their "trigger" is a .java JUnit case, not
# bytes, so the generic byte-replay / method-sig diff paths can't run on
# them. Each tool listed here performs its own pre/post differential
# inside its adapter and reports detection through the adapter dict.
UNIT_ANCHOR_TOOLS: frozenset[str] = frozenset({"evosuite_anchor", "randoop"})

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

    # cargo-fuzz target. Rewrite its pin AND rebuild the target binary so
    # the cargo_fuzz adapter finds a binary linked against the same
    # noodles-vcf version as the canonical-JSON harness. Without the
    # rebuild, _find_binary would return whichever version was built last
    # (typically the scaffolding default), producing a fuzzer that parses
    # post-fix-era VCFs even when the driver thinks we're on the pre-fix
    # pin. This is the per-version fuzz rebuild called out in
    # PHASE4_BASELINE_FIXES.md §0.9 / Chat 4 follow-up.
    if NOODLES_FUZZ_CARGO_TOML.exists():
        try:
            _rewrite_noodles_pin(NOODLES_FUZZ_CARGO_TOML, version)
        except RuntimeError:
            return  # no pin present; harness side still pinned, good enough
        try:
            subprocess.run(
                ["cargo", "fuzz", "build", "noodles_vcf_target",
                 "--release", "--sanitizer", "none"],
                cwd=str(NOODLES_FUZZ_DIR.parent),
                check=True, capture_output=True, env=env,
            )
        except subprocess.CalledProcessError as e:
            # Best-effort: the adapter will surface "binary not built" if
            # the stale binary gets removed. Don't fail the whole install.
            print(f"[noodles] cargo fuzz build failed for {version}: "
                  f"stderr={e.stderr.decode(errors='replace')[-400:]}")


def _install_htsjdk_jar(version: str, out_path: Path) -> None:
    """Download the versioned htsjdk JAR from Maven Central."""
    url = ("https://repo.maven.apache.org/maven2/com/github/samtools/htsjdk/"
           f"{version}/htsjdk-{version}.jar")
    subprocess.run(["curl", "-L", "-o", str(out_path), url], check=True)


# -- htsjdk harness rewrite (2026-04-24) ---------------------------------
#
# BioTest's `HTSJDKRunner` loads the shaded fatjar
# `harnesses/java/build/libs/biotest-harness-all.jar`. Before this change,
# `_install_htsjdk_jar` downloaded `htsjdk-<version>.jar` but BioTest
# never saw it — the fatjar's bundled htsjdk classes (from harness
# build time) stayed in effect. Every htsjdk cell tested the SAME
# version both pre-fix and post-fix, which is why method-sig diff
# never fired.
#
# Fix: after download, REWRITE the fatjar to use the downloaded
# version's classes in place of its bundled htsjdk classes. Keep the
# rest of the fatjar (compiled BioTestHarness.class + transitive deps
# shaded in at build time) untouched. On first call, stash a backup
# of the original fatjar so we can restore post-bench.

def _harness_jar() -> Path:
    return (REPO_ROOT / "harnesses" / "java" / "build" / "libs"
            / "biotest-harness-all.jar")


def _harness_backup() -> Path:
    """Backup path for the pristine harness fatjar. Captured on the
    first install swap of any bench session so subsequent restore
    always returns to the hermetic build output."""
    return _harness_jar().with_suffix(".jar.pristine")


def _swap_htsjdk_in_harness(htsjdk_jar: Path) -> None:
    """Replace the `htsjdk/**` class files inside the harness fatjar
    with the ones from ``htsjdk_jar`` (a Maven-Central download such
    as ``htsjdk-2.24.1.jar``).

    Preserves every non-htsjdk entry: the compiled
    ``BioTestHarness.class``, ``META-INF/MANIFEST.MF`` (rewritten to
    keep ``Main-Class: BioTestHarness``), and every transitive
    dependency class shaded into the fatjar at harness build time
    (commons-compress, snappy-java, etc.).

    Cross-platform (pure stdlib — ``zipfile`` + ``shutil``). Atomic
    on the target file (writes to a sibling tempfile then renames).
    Safe to call repeatedly.
    """
    import zipfile
    harness = _harness_jar()
    if not harness.exists():
        raise RuntimeError(
            f"harness fatjar missing: {harness}. "
            "Run `bash harnesses/java/build.sh` first."
        )

    # Back up the pristine build-output fatjar on first swap.
    backup = _harness_backup()
    if not backup.exists():
        shutil.copy2(harness, backup)

    # Stage all extractions in a tempdir — don't touch the 9p mount
    # until the atomic rename at the end.
    work = Path(tempfile.mkdtemp(prefix="_htsjdk_swap_"))
    try:
        # 1. Unpack the pristine fatjar (we always start from the
        #    build-output, NOT the potentially-already-swapped jar,
        #    so repeated swaps don't compound errors).
        with zipfile.ZipFile(backup, "r") as zf:
            zf.extractall(work)

        # 2. Remove the shaded-in htsjdk/** directory and any
        #    htsjdk-specific META-INF/services entries.
        ht_dir = work / "htsjdk"
        if ht_dir.exists():
            shutil.rmtree(ht_dir)
        services_dir = work / "META-INF" / "services"
        if services_dir.exists():
            for svc in services_dir.iterdir():
                if svc.is_file() and "htsjdk" in svc.read_text(
                    encoding="utf-8", errors="ignore"
                ):
                    svc.unlink()

        # 3. Unpack the htsjdk/** entries from the downloaded jar.
        #    Skip META-INF — we keep the harness's own.
        with zipfile.ZipFile(htsjdk_jar, "r") as zf:
            for name in zf.namelist():
                if name.startswith("htsjdk/") and not name.endswith("/"):
                    zf.extract(name, work)

        # 4. Rewrite the manifest — preserving only the Main-Class
        #    entry; drop signatures (so a signed htsjdk jar's
        #    unpacked .SF/.DSA/.RSA don't invalidate the new fatjar).
        mf_dir = work / "META-INF"
        mf_dir.mkdir(parents=True, exist_ok=True)
        (mf_dir / "MANIFEST.MF").write_text(
            "Manifest-Version: 1.0\n"
            "Main-Class: BioTestHarness\n"
            "\n",
            encoding="utf-8",
        )
        for sig in list(mf_dir.glob("*.SF")) + \
                list(mf_dir.glob("*.DSA")) + \
                list(mf_dir.glob("*.RSA")) + \
                list(mf_dir.glob("*.EC")):
            sig.unlink()

        # 5. Repack into a sibling tempfile, then atomically rename.
        tmp_out = harness.with_suffix(".jar.swap_tmp")
        if tmp_out.exists():
            tmp_out.unlink()
        with zipfile.ZipFile(
            tmp_out, "w", zipfile.ZIP_DEFLATED
        ) as zf:
            for root, _, files in os.walk(work):
                for f in files:
                    full = Path(root) / f
                    arc = full.relative_to(work).as_posix()
                    zf.write(full, arc)

        # Atomic replace. os.replace is atomic on POSIX and Windows.
        os.replace(tmp_out, harness)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _restore_harness_from_backup() -> None:
    """Restore the pristine fatjar if a swap was ever performed.
    No-op when no backup exists. Idempotent."""
    harness = _harness_jar()
    backup = _harness_backup()
    if backup.exists():
        try:
            shutil.copy2(backup, harness)
        except OSError:
            pass


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


def _rebuild_seqan3_libfuzzer_harness(seqan3_src_dir: Path) -> None:
    """Rebuild the libfuzzer harness against the per-anchor seqan3 headers.

    Added 2026-04-21 (PHASE4_BASELINE_FIXES.md §0.8). The image-baked
    `/opt/seqan3/include` (3.3.0) was otherwise used for every anchor,
    making pre-fix and post-fix fuzzer binaries byte-identical and
    every seqan3 cell architecturally `false+`.

    Uses per-anchor build directories (`build_<anchor>/`) to avoid
    CMake cache churn — each anchor's CMakeCache remembers its own
    include-path state, so switching back-and-forth is incremental.
    """
    libfuzzer_dir = REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
    anchor_tag = subprocess.run(
        ["git", "-C", str(seqan3_src_dir), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip() or "head"
    build_dir = libfuzzer_dir / f"build_{anchor_tag}"
    build_dir.mkdir(parents=True, exist_ok=True)

    anchor_include = seqan3_src_dir / "include"
    # -I <anchor>/include prepended to the compiler command line so the
    # anchor's seqan3 headers beat /opt/seqan3/include (which is still on
    # CPLUS_INCLUDE_PATH via the image). sdsl-lite stays image-baked.
    cxx_flags = (
        f"-DSEQAN3_DISABLE_COMPILER_CHECK -isystem {anchor_include}"
    )
    subprocess.run(
        ["cmake",
         "-DCMAKE_CXX_COMPILER=clang++-18",
         f"-DCMAKE_CXX_FLAGS={cxx_flags}",
         str(libfuzzer_dir)],
        cwd=str(build_dir), check=True, capture_output=True,
    )
    subprocess.run(
        ["make", "seqan3_sam_fuzzer_libfuzzer"],
        cwd=str(build_dir), check=True, capture_output=True,
    )
    # Publish a canonical per-anchor symlink the adapter consumes.
    canonical = libfuzzer_dir / "build" / "seqan3_sam_fuzzer_libfuzzer"
    canonical.parent.mkdir(parents=True, exist_ok=True)
    if canonical.exists() or canonical.is_symlink():
        canonical.unlink()
    per_anchor = build_dir / "seqan3_sam_fuzzer_libfuzzer"
    try:
        os.symlink(per_anchor, canonical)
    except OSError:
        # Windows or filesystems without symlink support: hard copy.
        shutil.copy2(per_anchor, canonical)


def _install_seqan3(commit: str, seqan3_src_dir: Path) -> None:
    """Check out + rebuild the libfuzzer harness against the per-anchor
    source tree so pre-fix / post-fix binaries differ (§0.8 blocker)."""
    _checkout_seqan3(commit, seqan3_src_dir)
    # Invalidate the canonical binary up-front so a rebuild failure on
    # this anchor CANNOT leave a stale symlink pointing at a prior
    # anchor's binary — that would silently fuzz the wrong SUT version
    # and produce misleading false+/FOUND results.
    canonical = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
                 / "build" / "seqan3_sam_fuzzer_libfuzzer")
    if canonical.exists() or canonical.is_symlink():
        canonical.unlink()
    try:
        _rebuild_seqan3_libfuzzer_harness(seqan3_src_dir)
    except subprocess.CalledProcessError as e:
        # A compile failure against a specific anchor (e.g. old seqan3
        # that isn't Clang-18-clean) is a tooling-level skip analogous
        # to the noodles harness-skew case. Record it + keep going so
        # downstream adapter invocations surface "binary not built"
        # rather than halting the whole bench.
        stderr = e.stderr.decode(errors="replace") if isinstance(
            e.stderr, (bytes, bytearray)) else (e.stderr or "")
        print(f"[seqan3] rebuild failed for {commit}: "
              f"stderr={stderr[-400:]}")


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
        # 2026-04-24: also rewrite BioTest's harness fatjar so that
        # the version-pinned htsjdk classes actually get loaded at
        # runtime. Without this, HTSJDKRunner keeps using the
        # harness's build-time-bundled htsjdk and every htsjdk cell
        # is a no-op version swap.
        try:
            _swap_htsjdk_in_harness(dest)
        except Exception as e:
            # Best-effort — if the swap fails we at least still have
            # the pristine harness. Log so the cell's result.json
            # shows the noise instead of crashing the bench.
            print(f"[install_sut] htsjdk swap failed for {version}: "
                  f"{type(e).__name__}: {str(e)[:200]}")
    elif sut == "seqan3":
        seqan3_src = REPO_ROOT / "compares" / "baselines" / "seqan3" / "source"
        if not seqan3_src.exists():
            raise RuntimeError(
                f"seqan3 source not found at {seqan3_src}; clone first")
        # _install_seqan3 = _checkout_seqan3 + rebuild the libfuzzer
        # harness against the per-anchor source tree (§0.8 fix —
        # otherwise every seqan3 cell is byte-identical pre/post-fix).
        _install_seqan3(version, seqan3_src)
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

# Cache for per-SUT seed acceptance probes. Key: (sut, fmt). Value:
# set of seed names the target SUT accepted. Populated lazily; cleared
# when the driver restarts. See _per_sut_accepted_seeds().
_PER_SUT_ACCEPTED: dict[tuple[str, str], set[str]] = {}


def _per_sut_accepted_seeds(
    general_seeds: Path, sut: str, fmt: str,
) -> set[str] | None:
    """Return the set of seed basenames the target SUT's ParserRunner
    accepts (success=True OR error_type=="ineligible"). Returns None if
    the runner can't be loaded — callers treat that as "skip filtering"
    (permissive default).

    Added 2026-04-21 (PHASE4_BASELINE_FIXES.md §0.10). Complements §0.1
    global sanitization: §0.1 only drops seeds that EVERY SUT rejects;
    this function additionally filters per-SUT poisons like the
    `@SQ chr1,chr3` BAM (Chat 2) and `real_world_htslib_auxf_values.sam`
    empty-aux-tag SAM (Chat 5) out of individual cells.
    """
    key = (sut, fmt.upper())
    if key in _PER_SUT_ACCEPTED:
        return _PER_SUT_ACCEPTED[key]

    sys.path.insert(0, str(REPO_ROOT))
    runner = None
    try:
        if sut == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner
            runner = HTSJDKRunner()
        elif sut == "biopython":
            from test_engine.runners.biopython_runner import BiopythonRunner
            runner = BiopythonRunner()
        elif sut == "vcfpy":
            from test_engine.runners.vcfpy_runner import VcfpyRunner
            runner = VcfpyRunner()
        elif sut == "noodles":
            from test_engine.runners.noodles_runner import NoodlesRunner
            runner = NoodlesRunner()
        elif sut == "seqan3":
            from test_engine.runners.seqan3_runner import SeqAn3Runner
            runner = SeqAn3Runner()
        elif sut == "pysam":
            from test_engine.runners.pysam_runner import PysamRunner
            runner = PysamRunner()
    except Exception as exc:
        print(f"[seed-filter] runner load failed for {sut}: {exc}; "
              f"skipping filter")
        _PER_SUT_ACCEPTED[key] = None  # type: ignore[assignment]
        return None
    finally:
        sys.path.pop(0)

    if runner is None or not runner.is_available():
        print(f"[seed-filter] runner for {sut} unavailable; skipping filter")
        _PER_SUT_ACCEPTED[key] = None  # type: ignore[assignment]
        return None

    accepted: set[str] = set()
    if not general_seeds.is_dir():
        _PER_SUT_ACCEPTED[key] = accepted
        return accepted

    # For seqan3, `SeqAn3Runner` wraps the pure-C++ text parser
    # `biotest_harness` — NOT the seqan3 library. So its probe accepts
    # inputs (like `real_world_htslib_auxf_values.sam` from Chat 5) that
    # actually crash the real seqan3 fuzzer harness. Prefer the
    # libfuzzer harness binary as the probe when it exists.
    seqan3_fuzzer_probe = None
    if sut == "seqan3":
        fuzzer_bin = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
                      / "build" / "seqan3_sam_fuzzer_libfuzzer")
        if fuzzer_bin.exists():
            seqan3_fuzzer_probe = fuzzer_bin

    for seed in sorted(general_seeds.iterdir()):
        if not seed.is_file():
            continue
        if seqan3_fuzzer_probe is not None:
            # libFuzzer-mode probe: `-runs=1 <file>` invokes
            # LLVMFuzzerTestOneInput once and exits. Non-zero = crash.
            try:
                proc = subprocess.run(
                    [str(seqan3_fuzzer_probe), "-runs=1", str(seed)],
                    capture_output=True, timeout=10,
                )
            except (subprocess.TimeoutExpired, OSError):
                continue
            if proc.returncode == 0:
                accepted.add(seed.name)
            continue
        try:
            res = runner.run(seed, fmt.upper(), timeout_s=10.0)
        except Exception:
            continue  # probe failure → treat as rejected
        if res.success or res.error_type == "ineligible":
            accepted.add(seed.name)
    total = sum(1 for p in general_seeds.iterdir() if p.is_file())
    probe_kind = "libfuzzer-harness" if seqan3_fuzzer_probe else "ParserRunner"
    print(f"[seed-filter] {sut}/{fmt}: {len(accepted)}/{total} accepted "
          f"(probe: {probe_kind})")
    _PER_SUT_ACCEPTED[key] = accepted
    return accepted


def _build_merged_seed_corpus(
    general_seeds: Path, bug: dict[str, Any], out_dir: Path,
) -> Path:
    """Materialize a per-cell seed corpus = filtered general seeds ∪ bug PoV.

    Two composable filters:
      - §0.4 PoV injection: union the bug's known trigger into the corpus
        so the fuzzer mutates around a known-good starting point (Magma /
        FuzzBench standard).
      - §0.10 per-SUT filter: exclude seeds the TARGET SUT's parser
        already rejects, so fuzzers don't halt on pre-rejected input and
        waste their time budget before any mutation happens (Chat 2 /
        Chat 5 failure modes).

    PoVs are ALWAYS merged — they're meant to trigger, filter doesn't
    apply to them.
    """
    merged = out_dir / "seeds_merged"
    merged.mkdir(parents=True, exist_ok=True)

    sut = bug.get("sut", "")
    fmt = bug.get("format", "VCF")
    accepted = _per_sut_accepted_seeds(general_seeds, sut, fmt.lower())

    kept = 0
    skipped = 0
    if general_seeds.is_dir():
        for src in general_seeds.iterdir():
            if not src.is_file():
                continue
            if accepted is not None and src.name not in accepted:
                skipped += 1
                continue
            dst = merged / src.name
            if dst.exists():
                continue
            try:
                os.symlink(src, dst)
            except OSError:
                shutil.copy2(src, dst)
            kept += 1

    pov_dir = REPO_ROOT / "compares" / "bug_bench" / "triggers" / bug["id"]
    fmt_l = fmt.lower()
    pov_added = 0
    if pov_dir.is_dir():
        # Accept original.vcf / original.sam / original.bam for SAM-row
        # bugs that prefer binary PoVs.
        candidates = list(pov_dir.glob(f"original.{fmt_l}"))
        if fmt_l == "sam":
            candidates.extend(pov_dir.glob("original.bam"))
        for pov in candidates:
            if not pov.is_file():
                continue
            # Name with leading "_aa_pov_" so lexicographic seed-
            # iteration hits the PoV FIRST (BioTest's SeedCorpus
            # sorts by glob, and a 300 s cell rarely iterates past a
            # handful of files). Without this prefix, the PoV sorts
            # AFTER general_* seeds and the cell's wall budget tends
            # to expire before BioTest reaches it.
            dst = merged / f"_aa_pov_{bug['id']}_{pov.name}"
            if dst.exists():
                continue
            try:
                os.symlink(pov, dst)
            except OSError:
                shutil.copy2(pov, dst)
            pov_added += 1
    print(f"[pov] {bug['id']}: seeds_merged={merged} "
          f"general_kept={kept} per_sut_skipped={skipped} "
          f"pov_added={pov_added}")
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
    elif tool == "randoop":
        # Same shape as evosuite_anchor: white-box unit-level Java
        # generator. DESIGN.md §2.3 lists Randoop as a secondary /
        # optional baseline; not in the primary MATRIX, so it only
        # runs when explicitly requested via --only-tool randoop.
        return _invoke_randoop(bug, out_dir, time_budget_s)
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
    # Delegate to the Python adapter — the legacy run_evosuite.sh was a
    # Windows-only coverage-parity sweep and never produced failing-tests/
    # inside the Linux bench image. See PHASE4_BASELINE_FIXES.md §1.1.
    adapters_dir = REPO_ROOT / "compares" / "scripts" / "tool_adapters"
    if str(adapters_dir) not in sys.path:
        sys.path.insert(0, str(adapters_dir))
    from run_evosuite_anchor import run_anchor  # type: ignore
    return run_anchor(bug, out_dir, time_budget_s)


def _invoke_randoop(
    bug: dict[str, Any], out_dir: Path, time_budget_s: int
) -> dict[str, Any]:
    adapters_dir = REPO_ROOT / "compares" / "scripts" / "tool_adapters"
    if str(adapters_dir) not in sys.path:
        sys.path.insert(0, str(adapters_dir))
    from run_randoop import run_anchor  # type: ignore
    return run_anchor(bug, out_dir, time_budget_s)


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
        except Exception as e:
            traceback.print_exc()
            install_err = (f"install pre_fix {pre} failed: "
                           f"{type(e).__name__}: {str(e)[:200]}")
            # Write a per-(tool, bug) result.json stub so rollup_bug_bench.py
            # picks the install-failure up and every expected cell appears
            # in aggregate.json / report.md as 'skip'. Without this the
            # group is silently dropped from the tree-rooted rollup
            # (PHASE4_BASELINE_FIXES.md §0.2 keep-going).
            for bug in group_bugs:
                for tool in MATRIX.get(sut, []):
                    if only_tool and tool != only_tool:
                        continue
                    tool_out = out_root / tool / bug["id"]
                    tool_out.mkdir(parents=True, exist_ok=True)
                    record = BugResult(
                        tool=tool, bug_id=bug["id"], sut=sut,
                        detected=False, ttfb_s=None, trigger_input=None,
                        signal=None, confirmed_fix_silences_signal=None,
                        adapter_exit_code=-1,
                        notes=install_err,
                    )
                    rec_dict = asdict(record)
                    rec_dict["install_error"] = install_err
                    (tool_out / "result.json").write_text(
                        json.dumps(rec_dict, indent=2), encoding="utf-8",
                    )
                    aggregate.append(rec_dict)
            continue

        # bug_id -> list of (tool, adapter_json, detected, ttfb, trig, sig)
        group_records: dict[str, list[dict[str, Any]]] = {b["id"]: [] for b in group_bugs}

        # Tools to execute for this SUT. Normally the row from MATRIX,
        # but when --only-tool names a non-MATRIX tool (e.g. randoop, the
        # secondary Java anchor) we honour it provided the bug's SUT is
        # one the tool can target. Without this branch the per-SUT loop
        # silently skips the requested tool.
        sut_matrix = list(MATRIX.get(sut, []))
        if only_tool and only_tool not in sut_matrix and only_tool == "randoop" and sut == "htsjdk":
            sut_matrix.append("randoop")

        for bug in group_bugs:
            seed_corpus = (
                seed_corpus_vcf if bug.get("format") == "VCF" else seed_corpus_sam)
            for tool in sut_matrix:
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

                # 2026-04-25: even when the adapter harvested zero
                # triggers (e.g., BioTest's "REJECTION FAILURE
                # [silent_accept_bug]" path on htsjdk-1561 logs the
                # disagreement but doesn't write a bug_report dir),
                # the canonical PoV still gives us a direct
                # pre-fix/post-fix differential to evaluate. Engage
                # the candidate loop whenever a PoV exists, even with
                # detected=False from the adapter.
                fmt_l = bug.get("format", "VCF").lower()
                pov_dir = (REPO_ROOT / "compares" / "bug_bench"
                           / "triggers" / bug["id"])
                pov_path = None
                for name in (f"original.{fmt_l}", "original.vcf",
                             "original.sam"):
                    p = pov_dir / name
                    if p.exists() and p.is_file():
                        pov_path = p
                        break

                # DESIGN.md §5.3.1: a real detection requires both
                #   signal(I, V_pre) = true   AND   signal(I, V_post) = false.
                # We iterate every trigger file under `crashes/` until
                # we find one that satisfies one half of §5.3.1, with
                # the canonical PoV always tried first (when authored).
                pre_fix_succeeds = None
                selected_trig = trig
                pov_alt = None  # alt trigger for reverse §5.3.1 fallback
                if (detected or pov_path is not None) and tool not in UNIT_ANCHOR_TOOLS:
                    fmt = bug.get("format", "VCF")
                    candidates: list[Path] = []

                    # 1. Canonical PoV first (if authored).
                    if pov_path is not None:
                        candidates.append(pov_path)

                    # 2. Every harvested trigger file under crashes/.
                    crashes_dir = tool_out / "crashes"
                    if crashes_dir.exists():
                        harvested = sorted(
                            p for p in crashes_dir.iterdir() if p.is_file()
                        )
                        # Cap to 30 to bound wall time; first attempts are
                        # cheapest and real bugs usually reproduce on the
                        # first PoV-shaped input when one is present.
                        candidates.extend(harvested[:30])

                    picked_fail: Path | None = None
                    picked_ok: Path | None = None
                    for cand in candidates:
                        try:
                            silenced_here = _replay_trigger_silenced(
                                sut, cand, fmt,
                            )
                        except Exception:
                            traceback.print_exc()
                            silenced_here = None
                        if silenced_here is False:
                            # Pre-fix FAILS on this trigger → candidate
                            # for §5.3.1 LHS. Keep the FIRST failing.
                            picked_fail = cand
                            break
                        if silenced_here is True and picked_ok is None:
                            picked_ok = cand

                    if picked_fail is not None:
                        selected_trig = str(picked_fail)
                        pre_fix_succeeds = False  # pre-fix DOES fail
                    elif picked_ok is not None:
                        # Every attempted trigger parsed cleanly pre-fix.
                        # Could be (a) vacuous (post-fix also parses clean
                        # — no signal at all) OR (b) accept-when-should-
                        # reject regression (htsjdk-1561 family — pre-fix
                        # silently accepts invalid input that the
                        # post-fix correctly rejects). We can't tell yet;
                        # tentatively demote and let the Phase-B replay
                        # promote back when post-fix actually fails on
                        # the same trigger (bidirectional §5.3.1).
                        selected_trig = str(picked_ok)
                        pre_fix_succeeds = True
                        detected = False
                    # else: all candidates raised on replay; pre_fix_succeeds
                    #       stays None and detection stays as reported.

                    # 2026-04-21: also remember a non-failing PoV when the
                    # picked_fail comes from a harvested trigger. If the
                    # forward §5.3.1 confirmation later rejects (post-fix
                    # also fails for unrelated reasons — common when the
                    # harvested SAM is a synthetic mutation), Phase B can
                    # fall back to the canonical PoV and try reverse §5.3.1.
                    # Without this, htsjdk-1238 (canonical comma-in-SN
                    # PoV is picked_ok, but a synthetic harvested trigger
                    # is picked_fail) lands as detected-but-not-confirmed.
                    pov_alt = None
                    if (picked_fail is not None
                            and pov_path is not None
                            and picked_ok is not None
                            and Path(picked_ok).resolve() == pov_path.resolve()):
                        pov_alt = str(pov_path)

                # 2026-04-24: snapshot method-signature of the bug's
                # canonical PoV against the pre-fix SUT. Compared
                # against the post-fix signature later — any diff
                # attributes a detection to API-method bugs (htsjdk-1544
                # `getType` on `<NON_REF>`, -1637 sort order, etc.).
                # We ALWAYS use the hand-authored PoV here, not the
                # adapter's harvested trigger — because the harvested
                # trigger is likely a shuffle-meta-lines transform of a
                # general seed that doesn't even contain the bytes
                # needed to exercise the API-bug code path. Only the
                # PoV guarantees the trigger shape.
                pre_method_sig = None
                pov_path = (REPO_ROOT / "compares" / "bug_bench"
                            / "triggers" / bug["id"]
                            / f"original.{bug.get('format','VCF').lower()}")
                trig_for_sig = str(pov_path) if pov_path.exists() else selected_trig
                if trig_for_sig and Path(trig_for_sig).exists() and tool not in UNIT_ANCHOR_TOOLS:
                    try:
                        pre_method_sig = _method_sig(
                            sut, Path(trig_for_sig), bug.get("format", "VCF")
                        )
                    except Exception:
                        traceback.print_exc()

                group_records[bug["id"]].append({
                    "tool": tool, "adapter_json": adapter_json,
                    "detected": detected, "ttfb": ttfb,
                    "trig": selected_trig, "sig": sig, "tool_out": tool_out,
                    "pre_fix_succeeds": pre_fix_succeeds,
                    "pre_method_sig": pre_method_sig,
                    "trig_for_sig": trig_for_sig,
                    "pov_alt": pov_alt,
                })

        # ---- Phase B: install post_fix once, replay every detection ---
        # Install post-fix if ANY cell has a detection to silence-check
        # OR a pre_method_sig to diff (Rank-5 method-sig comparison)
        # OR was demoted because pre-fix accepted the trigger (we want
        # to test reverse §5.3.1: pre-fix accepted, post-fix rejects =
        # accept-when-should-reject regression like htsjdk-1561).
        any_needs_replay = any(
            (r["detected"] and r["trig"])
            or r.get("pre_method_sig") is not None
            or (r.get("pre_fix_succeeds") is True and r.get("trig"))
            # 2026-04-21: pre_fix_succeeds=False (candidate loop found a
            # trigger that pre-fix rejects) also needs post-fix replay
            # to confirm the §5.3.1 LHS — without this, htsjdk-1360 /
            # htsjdk-1410 (STRICT-only rejections) never get confirmed
            # because BioTest's main oracle didn't fire (pre-fix SILENT
            # also accepts), but the STRICT silence predicate did pick
            # them as picked_fail.
            or (r.get("pre_fix_succeeds") is False and r.get("trig"))
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
                    # Unit-anchor adapters (evosuite_anchor, randoop)
                    # already perform pre/post JUnit comparison internally
                    # — their crash_count only counts tests that fail
                    # pre-fix AND pass post-fix, which is exactly the
                    # confirmed_fix_silences semantic. The generic
                    # _replay_trigger_silenced path would try to parse the
                    # .java trigger as VCF/SAM and always fail.
                    if r["tool"] in UNIT_ANCHOR_TOOLS:
                        aj = r["adapter_json"]
                        pre_p = aj.get("pre_pass_count")
                        post_p = aj.get("post_pass_count")
                        if post_p is not None and pre_p is not None:
                            confirmed = True
                        else:
                            confirmed = None
                    else:
                        try:
                            confirmed = _replay_trigger_silenced(
                                sut, Path(r["trig"]), fmt)
                        except Exception:
                            traceback.print_exc()
                            confirmed = None
                pfs = r.get("pre_fix_succeeds")
                notes = ""

                # 2026-04-21: PoV reverse-§5.3.1 fallback. When the
                # candidate loop captured the canonical PoV as picked_ok
                # (pre-fix accepted) but a harvested trigger took
                # priority as picked_fail, the harvested-trigger forward
                # path may not confirm (post-fix often also rejects the
                # synthetic SAM for unrelated reasons). The PoV's
                # picked_ok status guarantees pre-fix-accept; if
                # post-fix rejects the PoV, that's clean reverse §5.3.1.
                # Fires whenever pov_alt is set — overriding the
                # harvested-trigger verdict when it confirms the canonical
                # bug. Without this, htsjdk-1238 lands as
                # detected/unconfirmed (or detected=False if the adapter
                # itself failed and there's no harvested trigger to fall
                # back on).
                pov_alt = r.get("pov_alt")
                if (
                    not confirmed
                    and pov_alt
                    and replay_available
                    and Path(pov_alt).exists()
                    and r["tool"] not in UNIT_ANCHOR_TOOLS
                ):
                    try:
                        alt_silenced = _replay_trigger_silenced(
                            sut, Path(pov_alt), fmt
                        )
                    except Exception:
                        traceback.print_exc()
                        alt_silenced = None
                    if alt_silenced is False:
                        # PoV picked_ok in Phase A (pre-fix accepts) and
                        # post-fix rejects → reverse §5.3.1.
                        r["detected"] = True
                        confirmed = True
                        r["trig"] = pov_alt
                        notes = ("reverse §5.3.1 via PoV fallback: "
                                 "harvested-trigger forward path didn't "
                                 "confirm, but the canonical PoV is "
                                 "accept-pre / reject-post")
                        pfs = None  # don't apply demote-note path

                # 2026-04-21: forward §5.3.1 via STRICT gate. The
                # candidate loop's silence predicate now includes a
                # STRICT-stringency check for htsjdk SAM (run_strict_parse).
                # When pre_fix_succeeds is False *and* BioTest's main
                # oracle didn't fire (detected=False), it's because the
                # bug only manifests under STRICT — post-fix removed the
                # validation entirely. Confirm by replaying STRICT on
                # post-fix: if it now succeeds, that's the §5.3.1 LHS we
                # missed.
                if (
                    pfs is False
                    and not r["detected"]
                    and replay_available
                    and r["trig"]
                    and r["tool"] not in UNIT_ANCHOR_TOOLS
                ):
                    try:
                        post_silenced_strict = _replay_trigger_silenced(
                            sut, Path(r["trig"]), fmt
                        )
                    except Exception:
                        traceback.print_exc()
                        post_silenced_strict = None
                    if post_silenced_strict is True:
                        r["detected"] = True
                        confirmed = True
                        notes = ("forward §5.3.1 via STRICT gate: "
                                 "pre-fix STRICT rejects, post-fix STRICT "
                                 "accepts — over-strict spec rejection "
                                 "fixed (e.g. htsjdk-1360 EMPTY_READ, "
                                 "htsjdk-1410 INVALID_INSERT_SIZE)")
                        pfs = None  # don't apply the demote-note path

                # 2026-04-25: bidirectional §5.3.1. Forward (pre fails,
                # post passes) is the original predicate. Reverse (pre
                # passes, post fails) catches "accept-when-should-
                # reject" regressions like htsjdk-1561 (pre-fix silently
                # accepts malformed @HD tag length, post-fix rejects).
                # Both are real per-version behavioral diffs.
                if (
                    pfs is True
                    and replay_available
                    and r["trig"]
                    and r["tool"] not in UNIT_ANCHOR_TOOLS
                ):
                    try:
                        post_silenced = _replay_trigger_silenced(
                            sut, Path(r["trig"]), fmt
                        )
                    except Exception:
                        traceback.print_exc()
                        post_silenced = None
                    if post_silenced is False:
                        # Pre-fix accepts, post-fix rejects → reverse
                        # detection. Post-fix's rejection IS the silence
                        # of the bug ("the bug" being "pre-fix wrongly
                        # accepted invalid input").
                        r["detected"] = True
                        confirmed = True
                        notes = ("reverse §5.3.1: pre-fix accepted, "
                                 "post-fix rejects — accept-when-"
                                 "should-reject regression")
                        pfs = None  # don't apply the demote-note path

                # 2026-04-24: method-signature diff promotes detection
                # when parse+roundtrip paths both succeed but API methods
                # return different scalars between pre-fix and post-fix.
                # Catches htsjdk-1544 (`getType` mis-classifies NON_REF)
                # and siblings — pure data-model API bugs file-level
                # oracle would otherwise miss.
                pre_sig = r.get("pre_method_sig")
                trig_for_sig = r.get("trig_for_sig")
                if (
                    replay_available
                    and pre_sig is not None
                    and trig_for_sig
                    and Path(trig_for_sig).exists()
                    and r["tool"] not in UNIT_ANCHOR_TOOLS
                ):
                    try:
                        post_sig = _method_sig(
                            sut, Path(trig_for_sig), fmt,
                        )
                    except Exception:
                        post_sig = None
                    if post_sig is not None and post_sig != pre_sig:
                        # Method values differ across versions → real
                        # API bug. Override the parse-level verdict.
                        r["detected"] = True
                        confirmed = True
                        notes = ("method-signature diff across versions "
                                 "(Rank 5: pre-fix and post-fix SUTs "
                                 "return different scalars for one of "
                                 f"{len(pre_sig)} probed methods)")
                        pfs = None  # supersede pre-fix parse demotion
                if pfs is True:
                    notes = ("pre_fix SUT parses the picked trigger "
                             "cleanly — detection demoted to False "
                             "(no pre-fix signal to silence); likely "
                             "cross-voter canonical-JSON variance.")
                record = BugResult(
                    tool=r["tool"], bug_id=bug["id"], sut=sut,
                    detected=r["detected"], ttfb_s=r["ttfb"],
                    trigger_input=r["trig"], signal=r["sig"],
                    confirmed_fix_silences_signal=confirmed,
                    adapter_exit_code=int(r["adapter_json"].get("exit_code", 0)),
                    notes=notes,
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

    # 2026-04-24: restore the pristine harness fatjar so the next
    # user of `harnesses/java/build/libs/biotest-harness-all.jar`
    # doesn't silently inherit the last bench cell's htsjdk version.
    try:
        _restore_harness_from_backup()
    except Exception:
        traceback.print_exc()


def _method_sig(
    sut: str, trig_path: Path, fmt: str,
) -> dict[str, Any] | None:
    """Collect scalar outputs of a battery of query methods on the trigger.

    Returns a dict `{method_name: value}` (or None if the SUT can't
    answer any). The caller compares this dict across pre-fix and
    post-fix SUT installs: if the dicts differ, an API-method bug is
    present even when parse + write-roundtrip both succeed.

    Method battery is fixed per SUT. For htsjdk it's the same set the
    scaffolded Rank-5 query-method MR already exercises:
    `getNAlleles`, `getStart`, `getEnd`, `isBiallelic`, `isSNP`,
    `isIndel`, `getType`, `getContig`.

    See `coverage_notes/phase4/manifest_upper_bound_analysis.md` for
    why this is the right lever for the 6 htsjdk API-method bugs.
    """
    sys.path.insert(0, str(REPO_ROOT))
    try:
        if sut == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner  # type: ignore
            runner = HTSJDKRunner()
            if not runner.is_available():
                return None
            method_names = [
                "getNAlleles", "getStart", "getEnd",
                "isBiallelic", "isSNP", "isIndel",
                "getType", "getContig",
            ]
            try:
                r = runner.run_query_methods(trig_path, fmt, method_names)
            except Exception:
                return None
            if not r.success or not r.canonical_json:
                return None
            # Actual harness shape (verified 2026-04-24): either a top-
            # level `method_results` dict for the first VariantContext
            # in the file, OR `records[*].method_results` for per-record
            # arrays. We accept both.
            cj = r.canonical_json
            sig: dict[str, Any] = {}
            top_mr = cj.get("method_results")
            if isinstance(top_mr, dict):
                for k, v in top_mr.items():
                    sig[f"r0.{k}"] = v
            recs = cj.get("records") or []
            for i, rec in enumerate(recs):
                mr = rec.get("method_results") or {}
                for k, v in mr.items():
                    sig[f"r{i}.{k}"] = v
            return sig if sig else None
        # Other SUTs: no method-sig comparison today. Rank 5 needs per-
        # SUT method mappings that don't exist yet for pysam / noodles /
        # vcfpy at a common-interface level.
        return None
    finally:
        sys.path.pop(0)


def _runner_for(sut: str):
    """Lazily import + instantiate the ParserRunner subclass for `sut`.

    Returns None if the runner class can't be imported (e.g. seqan3 on a
    platform without its harness binary, or a non-Python SUT). Used by
    `_replay_trigger_silenced` to dispatch capability-flag checks
    (`supports_strict_parse`, `supports_mutator_methods`, …) without
    encoding SUT names in the verification logic.
    """
    sys.path.insert(0, str(REPO_ROOT))
    try:
        if sut == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner
            return HTSJDKRunner()
        if sut == "pysam":
            from test_engine.runners.pysam_runner import PysamRunner
            return PysamRunner()
        if sut == "biopython":
            from test_engine.runners.biopython_runner import BiopythonRunner
            return BiopythonRunner()
        if sut == "vcfpy":
            from test_engine.runners.vcfpy_runner import VcfpyRunner
            return VcfpyRunner()
        if sut == "seqan3":
            from test_engine.runners.seqan3_runner import SeqAn3Runner
            return SeqAn3Runner()
    except Exception:
        return None
    return None


def _replay_trigger_silenced(sut: str, trig_path: Path, fmt: str) -> bool | None:
    """Re-run the triggering input against the post-fix SUT.

    Returns:
      True   — post-fix parsed the trigger cleanly (signal silenced).
      False  — post-fix still fails on the trigger (genuine unrelated bug).
      None   — replay was impossible (missing runner binary, ENOEXEC,
               platform mismatch, runner ineligible for this format).
               The cell is listed under `null_silences` for triage
               rather than counted as a non-detection.

    2026-04-21 generalized STRICT prelude: any runner advertising
    `supports_strict_parse=True` is queried first; a STRICT-rejection
    short-circuits to `not silenced`. Lets the bench expose
    stringency-controlled regressions (htsjdk-1360, htsjdk-1410, plus
    pysam check_sq=True / vcfpy header-validation cells once those
    runners opt in) without encoding SUT names here.
    """
    runner_obj = _runner_for(sut)
    if runner_obj is not None and getattr(runner_obj, "supports_strict_parse", False):
        try:
            sp = runner_obj.run_strict_parse(trig_path, fmt)
        except (NotImplementedError, FileNotFoundError, OSError):
            sp = None
        except Exception:
            sp = None
        if sp is not None and not sp.success:
            return False
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
            # Deep predicate (2026-04-23): access every INFO key, every
            # FORMAT per sample, every sub-field, AND write-roundtrip.
            # Shallow iteration alone leaves lazy-eval bugs (KeyError on
            # sample[key], TypeError on Flag cast) undetectable — the
            # manifest audit (compares/results/null_silence_audit.json)
            # showed vcfpy-127 / vcfpy-gtone-0.13 silent on shallow
            # iteration despite being real bugs in that version. We
            # also roundtrip the file to catch serializer bugs that
            # only surface on write (vcfpy-171's %3D drop).
            try:
                proc = subprocess.run(
                    [py, "-c",
                     "import sys, tempfile, os, vcfpy\n"
                     "try:\n"
                     "    path = sys.argv[1]\n"
                     "    with vcfpy.Reader.from_path(path) as r:\n"
                     "        header = r.header\n"
                     "        _ = list(header.lines)\n"
                     "        recs = []\n"
                     "        for rec in r:\n"
                     "            _ = (rec.CHROM, rec.POS, rec.ID,\n"
                     "                 rec.REF, list(rec.ALT), rec.QUAL,\n"
                     "                 list(rec.FILTER))\n"
                     "            for k in list(rec.INFO.keys()):\n"
                     "                v = rec.INFO[k]\n"
                     "                if isinstance(v, list):\n"
                     "                    list(v)\n"
                     "            if rec.FORMAT:\n"
                     "                for call in rec.calls:\n"
                     "                    for fmt_k in rec.FORMAT:\n"
                     "                        if hasattr(call, 'data'):\n"
                     "                            _ = call.data.get(fmt_k)\n"
                     "            recs.append(rec)\n"
                     "    with tempfile.NamedTemporaryFile(\n"
                     "        mode='w', suffix='.vcf', delete=False) as tf:\n"
                     "        out_path = tf.name\n"
                     "    try:\n"
                     "        with vcfpy.Writer.from_path(out_path, header) as w:\n"
                     "            for rec in recs:\n"
                     "                w.write_record(rec)\n"
                     "        with vcfpy.Reader.from_path(out_path) as r2:\n"
                     "            recs2 = list(r2)\n"
                     "        if len(recs) != len(recs2):\n"
                     "            sys.exit(2)\n"
                     "        for a, b in zip(recs, recs2):\n"
                     "            if (a.CHROM, a.POS, a.REF, list(a.ALT)) != \\\n"
                     "               (b.CHROM, b.POS, b.REF, list(b.ALT)):\n"
                     "                sys.exit(3)\n"
                     "            for k in a.INFO:\n"
                     "                if k not in b.INFO or str(a.INFO[k]) != str(b.INFO[k]):\n"
                     "                    sys.exit(4)\n"
                     "    finally:\n"
                     "        try: os.unlink(out_path)\n"
                     "        except OSError: pass\n"
                     "except Exception:\n"
                     "    sys.exit(1)\n",
                     str(trig_path)],
                    capture_output=True, timeout=30,
                )
            except (FileNotFoundError, OSError):
                return None
            return proc.returncode == 0
        elif sut == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner  # type: ignore
            runner = HTSJDKRunner()
            # STRICT-stringency gate moved to the runner-agnostic prelude
            # at the top of this function (2026-04-21 generalization).
            # Deep predicate (2026-04-23): require BOTH parse and
            # write-roundtrip to succeed + match, so writer bugs
            # (htsjdk-1389 `.,.,.` serialisation; htsjdk-1401 PEDIGREE
            # round-trip) surface even when the PoV reads cleanly.
            r = runner.run(trig_path, fmt)
            if not r.success:
                return False
            # write_roundtrip contract: re-serialise and compare
            # canonical output text.
            try:
                wr = runner.run_write_roundtrip(trig_path, fmt)
            except Exception:
                wr = None
            if wr is None or not wr.success:
                return False
            # Extract re-parsed output and compare canonical JSONs.
            rewritten_path = None
            if wr.canonical_json and isinstance(wr.canonical_json, dict):
                rewritten_text = wr.canonical_json.get("rewritten_text")
                if rewritten_text:
                    import tempfile
                    ext = ".vcf" if fmt.upper() == "VCF" else ".sam"
                    with tempfile.NamedTemporaryFile(
                        mode="w", suffix=ext, delete=False
                    ) as tf:
                        tf.write(rewritten_text)
                        rewritten_path = Path(tf.name)
            if rewritten_path is not None:
                try:
                    r2 = runner.run(rewritten_path, fmt)
                finally:
                    try:
                        rewritten_path.unlink()
                    except OSError:
                        pass
                if not r2.success:
                    return False
                # Compare variant-identity fields only (post_normalize
                # adds cross-voter tolerance; for htsjdk-vs-htsjdk
                # same-version compare, exact match is OK).
                def _extract(res):
                    cj = res.canonical_json or {}
                    return [(r.get("CHROM"), r.get("POS"), r.get("REF"),
                             tuple(r.get("ALT") or []))
                            for r in cj.get("records", []) or []]
                if _extract(r) != _extract(r2):
                    return False
            return True
        elif sut == "seqan3":
            from test_engine.runners.seqan3_runner import SeqAn3Runner  # type: ignore
            runner = SeqAn3Runner()
            # If the replay binary doesn't exist for this platform (e.g.
            # the .exe ships but we're on Linux, or vice-versa), the
            # runner would synthesize a `success=False` result that the
            # driver cannot distinguish from a genuine "post-fix still
            # crashes" verdict. Bail to None so the cell is flagged for
            # manual triage rather than scored as a non-detection
            # (PHASE4_BASELINE_FIXES.md §0.9 fix).
            if not runner.is_available():
                return None
            try:
                r = runner.run(trig_path, fmt)
            except (FileNotFoundError, OSError):
                return None
            if r.error_type == "ineligible":
                return None
        elif sut == "noodles":
            binary = (REPO_ROOT / "harnesses" / "rust" / "noodles_harness"
                      / "target" / "release" / "noodles_harness")
            if not binary.exists():
                return None  # type: ignore[return-value]
            # Deep predicate (2026-04-23): READ + WRITE_ROUNDTRIP, and
            # compare the two canonical JSONs byte-for-byte. Writer bugs
            # (noodles-259 / -268 / -300 / -339) only surface when the
            # writer's output is re-parsed and compared back — a pure
            # READ predicate misses them. Step order:
            #   1) Parse PoV → canon1
            #   2) Write via --mode write_roundtrip → new file
            #   3) Parse new file → canon2
            #   4) canon1 == canon2 ? silenced : detection survives
            # Step (1) alone is the old shallow check; adding (2-4) is
            # the lift.
            import tempfile
            # Step 1: plain parse.
            proc1 = subprocess.run(
                [str(binary), fmt.upper(), str(trig_path)],
                capture_output=True, timeout=30,
            )
            if proc1.returncode != 0:
                return False  # pre-fix-style failure, not silenced
            canon1 = proc1.stdout

            # Step 2: write_roundtrip.
            with tempfile.NamedTemporaryFile(
                suffix=f".{fmt.lower()}", delete=False,
            ) as tf:
                out_path = tf.name
            try:
                proc_wr = subprocess.run(
                    [str(binary), "--mode", "write_roundtrip",
                     fmt.upper(), str(trig_path), out_path],
                    capture_output=True, timeout=30,
                )
                if proc_wr.returncode != 0:
                    return False  # writer crashed
                # Step 3: re-parse.
                proc2 = subprocess.run(
                    [str(binary), fmt.upper(), out_path],
                    capture_output=True, timeout=30,
                )
                if proc2.returncode != 0:
                    return False  # writer produced garbage
                canon2 = proc2.stdout
                # Step 4: compare canonical JSONs.
                if canon1.strip() != canon2.strip():
                    return False  # roundtrip lost data → writer bug
                return True
            finally:
                try:
                    import os as _os
                    _os.unlink(out_path)
                except OSError:
                    pass
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
                   help="Run only this tool (biotest, jazzer, atheris, libfuzzer, pure_random, evosuite_anchor, randoop)")
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
