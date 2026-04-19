#!/usr/bin/env bash
# Build the Jazzer and libFuzzer harnesses for the comparative
# evaluation. Atheris harnesses are pure Python and need no build step
# beyond `pip install -r compares/harnesses/atheris/requirements.txt`.
#
# Usage:
#   bash compares/scripts/build_harnesses.sh            # build everything
#   bash compares/scripts/build_harnesses.sh jazzer     # build only Jazzer
#   bash compares/scripts/build_harnesses.sh libfuzzer  # build only libFuzzer
#
# libFuzzer requires Linux/WSL2 + Clang 18+ + libseqan3-dev (DESIGN §9).

set -euo pipefail

TARGETS="${*:-all}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

build_jazzer() {
  local dir="$ROOT/compares/harnesses/jazzer"
  echo "[harness] Jazzer @ $dir"
  cd "$dir"
  if [[ -x "./gradlew" ]]; then
    ./gradlew jazzerHarness
  elif command -v gradle >/dev/null 2>&1; then
    gradle jazzerHarness
  else
    echo "[harness] ERROR: neither ./gradlew nor gradle on PATH" >&2
    return 1
  fi
  cd - >/dev/null
}

build_libfuzzer() {
  local dir="$ROOT/compares/harnesses/libfuzzer"
  echo "[harness] libFuzzer @ $dir"
  mkdir -p "$dir/build"
  cd "$dir/build"
  # Prefer clang++-18; fall back to clang++ in PATH.
  local cxx="${CXX:-$(command -v clang++-18 || command -v clang++)}"
  if [[ -z "$cxx" ]]; then
    echo "[harness] ERROR: clang++ not found; install Clang 18+" >&2
    return 1
  fi
  cmake -DCMAKE_CXX_COMPILER="$cxx" ..
  make seqan3_sam_fuzzer
  cd - >/dev/null
}

build_atheris_env() {
  echo "[harness] Atheris requirements (Linux / WSL2 / macOS only)"
  local req="$ROOT/compares/harnesses/atheris/requirements.txt"
  if [[ "$(uname -s)" == "MINGW"* || "$(uname -s)" == "MSYS"* || "$(uname -s)" == "CYGWIN"* ]]; then
    echo "[harness] SKIP: Atheris does not support Windows"
    return 0
  fi
  python3 -m pip install -r "$req"
}

for tgt in $TARGETS; do
  case "$tgt" in
    all)
      build_jazzer
      build_libfuzzer || echo "[harness] libFuzzer skipped (gated on Linux/Clang/seqan3)"
      build_atheris_env
      ;;
    jazzer)      build_jazzer ;;
    libfuzzer)   build_libfuzzer ;;
    atheris)     build_atheris_env ;;
    *) echo "[harness] unknown target $tgt; try 'all', 'jazzer', 'libfuzzer', 'atheris'"; exit 1 ;;
  esac
done

echo "[harness] done"
