#!/usr/bin/env bash
# Create the per-SUT install environments the bug_bench_driver swaps
# versions into.
#
# Each Python SUT gets a dedicated venv so `pip install pysam==0.20.0`
# doesn't clobber the interpreter that runs the bench driver itself.
# htsjdk gets a versioned-JAR directory; seqan3 gets a source clone
# that bug_bench_driver checks out at pre-fix / post-fix commits.
#
# All environments live under the mounted /work tree
# (compares/results/...) so they persist across `docker run --rm`.
#
# Usage:
#   bash compares/scripts/prepare_sut_install_envs.sh
#
# Idempotent: venvs and directories are reused if they already exist.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SUT_ENVS="${REPO_ROOT}/compares/results/sut-envs"
mkdir -p "${SUT_ENVS}"

# Pick the most-recent compatible Python. Atheris's 3.11 venv is a good
# default because its site-packages already has pysam + biopython
# installed; copying from it is faster than a fresh pip install. Fall
# back to the system python3.11 otherwise.
PYTHON_BIN="${PYTHON_BIN:-python3.11}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    echo "[sut-envs] ERROR: ${PYTHON_BIN} not on PATH; set PYTHON_BIN=..." >&2
    exit 1
fi

make_venv() {
    local name="$1"
    local pip_pkg="$2"
    local import_name="$3"
    local default_version="$4"
    local path="${SUT_ENVS}/${name}"
    if [[ -x "${path}/bin/python" ]]; then
        echo "[sut-envs] ${name}: exists at ${path}"
    else
        echo "[sut-envs] ${name}: creating venv at ${path}"
        "${PYTHON_BIN}" -m venv "${path}"
        "${path}/bin/pip" install --quiet --upgrade pip
        "${path}/bin/pip" install --quiet "${pip_pkg}==${default_version}"
    fi
    # Probe the importable module name, not the PyPI distribution name
    # (biopython → import Bio, scikit-learn → import sklearn, etc.).
    # Non-fatal so a single probe failure doesn't kill the rest of the
    # script.
    if ! "${path}/bin/python" -c "import ${import_name}; print('${name} venv:', ${import_name}.__version__)"; then
        echo "[sut-envs] ${name}: probe failed; venv exists but import ${import_name} did not" >&2
    fi
}

# Python SUTs — venvs per SUT, seeded with a baseline version.
# bug_bench_driver.py will `pip install --force-reinstall <sut>==<ver>`
# to swap between pre-fix and post-fix anchors per DESIGN.md §5.3.
#
# pysam is retained as a voter (DESIGN §2.6 / §9 Risk 4), NOT a primary
# SUT; the venv is kept so the differential oracle can call into the
# installed pysam at oracle time.
make_venv pysam     pysam     pysam 0.22.1
make_venv biopython biopython Bio   1.85
# vcfpy (2026-04-20) — new primary VCF SUT, replaces pysam in the
# scored primary matrix. Same Python 3.11 interpreter family as the
# other Atheris-driven SUTs.
make_venv vcfpy     vcfpy     vcfpy 0.14.0

# htsjdk — a versioned-JAR directory that bug_bench_driver populates on
# demand via `curl https://repo.maven.apache.org/maven2/.../htsjdk-<v>.jar`.
HTSJDK_JARS="${REPO_ROOT}/compares/baselines/evosuite/fatjar/versioned"
mkdir -p "${HTSJDK_JARS}"
echo "[sut-envs] htsjdk: versioned-JAR dir ready at ${HTSJDK_JARS}"
ls -1 "${HTSJDK_JARS}" 2>/dev/null | sed 's/^/  - /' || true

# seqan3 — source clone for commit-SHA checkout. Shallow clone; the
# driver will deepen if it needs to check out a historical commit.
SEQAN3_SRC="${REPO_ROOT}/compares/baselines/seqan3/source"
if [[ -d "${SEQAN3_SRC}/.git" ]]; then
    echo "[sut-envs] seqan3: source clone exists at ${SEQAN3_SRC}"
else
    echo "[sut-envs] seqan3: cloning to ${SEQAN3_SRC}"
    mkdir -p "${SEQAN3_SRC%/*}"
    git clone --depth 50 https://github.com/seqan/seqan3 "${SEQAN3_SRC}"
fi
cd "${SEQAN3_SRC}"
echo "[sut-envs] seqan3: HEAD = $(git rev-parse --short HEAD) on $(git rev-parse --abbrev-ref HEAD)"
cd - >/dev/null

echo
echo "[sut-envs] done"
