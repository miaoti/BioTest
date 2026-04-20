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
  # Works inside biotest-bench (seqan3 Clang patches baked into the
  # image at /opt/seqan3/). If you're running this on bare WSL2
  # without biotest-bench, re-apply the two patches in DESIGN.md
  # §13.2.4 first.
  local dir="$ROOT/compares/harnesses/libfuzzer"
  echo "[harness] libFuzzer (Clang 18) @ $dir"
  mkdir -p "$dir/build"
  cd "$dir/build"
  local cxx="${CXX:-$(command -v clang++-18 || command -v clang++)}"
  if [[ -z "$cxx" ]]; then
    echo "[harness] ERROR: clang++ not found; install Clang 18+" >&2
    return 1
  fi
  cmake -DCMAKE_CXX_COMPILER="$cxx" \
        -DCMAKE_CXX_FLAGS="-DSEQAN3_DISABLE_COMPILER_CHECK" ..
  make seqan3_sam_fuzzer_libfuzzer
  cd - >/dev/null
}

build_libfuzzer_cov() {
  # Offline coverage-replay binary. Same seqan3 source as the libFuzzer
  # target, but built with --coverage (gcov instrumentation) so it
  # emits .gcda files per invocation. Reads one corpus file on stdin
  # via the default main() and exits. Used by coverage_sampler.py to
  # measure cumulative line coverage at log ticks.
  local dir="$ROOT/compares/harnesses/libfuzzer"
  echo "[harness] libFuzzer coverage replay (Clang 18 + --coverage) @ $dir"
  mkdir -p "$dir/build-cov"
  cd "$dir/build-cov"
  local cxx="${CXX:-$(command -v clang++-18 || command -v clang++)}"
  if [[ -z "$cxx" ]]; then
    echo "[harness] ERROR: clang++ not found; install Clang 18+" >&2
    return 1
  fi
  cmake -DCMAKE_CXX_COMPILER="$cxx" \
        -DCMAKE_CXX_FLAGS="-DSEQAN3_DISABLE_COMPILER_CHECK" ..
  make seqan3_sam_fuzzer_cov
  cd - >/dev/null
}

build_aflpp() {
  # AFL++ + GCC 12. Works today; this is the production C++ fuzzer
  # target for the comparison.
  local dir="$ROOT/compares/harnesses/libfuzzer"
  echo "[harness] AFL++ (g++-12) @ $dir"
  mkdir -p "$dir/build-aflpp"
  cd "$dir/build-aflpp"
  if ! command -v afl-g++ >/dev/null 2>&1; then
    echo "[harness] ERROR: afl-g++ not on PATH; install AFL++ or rebuild the biotest-bench image" >&2
    return 1
  fi
  if ! command -v g++-12 >/dev/null 2>&1; then
    echo "[harness] ERROR: g++-12 not on PATH (seqan3 needs libstdc++ 12)" >&2
    return 1
  fi
  # afl-g++ needs AFL_PATH to locate afl-compiler-rt.o. biotest-bench
  # sets this in the image; export a default here for host-side builds
  # that skip the image.
  : "${AFL_PATH:=/opt/aflpp/lib/afl}"
  export AFL_PATH
  cmake -DCMAKE_CXX_COMPILER=g++-12 "$dir"
  make seqan3_sam_fuzzer_aflpp
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
      build_aflpp || echo "[harness] AFL++ skipped (missing GCC 12 / AFL++)"
      build_libfuzzer || echo "[harness] libFuzzer skipped (missing Clang 18 / patched seqan3)"
      build_libfuzzer_cov || echo "[harness] libFuzzer coverage replay skipped (missing Clang 18 / patched seqan3)"
      build_atheris_env
      ;;
    jazzer)         build_jazzer ;;
    aflpp)          build_aflpp ;;
    libfuzzer)      build_libfuzzer ;;
    libfuzzer_cov)  build_libfuzzer_cov ;;
    atheris)        build_atheris_env ;;
    *) echo "[harness] unknown target $tgt; try 'all', 'jazzer', 'aflpp', 'libfuzzer', 'libfuzzer_cov', 'atheris'"; exit 1 ;;
  esac
done

echo "[harness] done"
