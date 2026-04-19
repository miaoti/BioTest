#!/usr/bin/env bash
# Smoke-test every tool inside the BioTest benchmark image. Prints a
# pass/fail line per tool. Non-zero exit if any required tool is
# missing or broken.
#
# Runs inside the image (directly): `bash compares/docker/verify.sh`
# Or from the Windows host: `bash compares/docker/run.sh -- bash compares/docker/verify.sh`.

set -u

PASS=()
FAIL=()
WARN=()

check() {
    local name="$1"; shift
    if "$@" >/dev/null 2>&1; then
        PASS+=("${name}")
        printf '  \033[32mOK\033[0m   %s\n' "${name}"
    else
        FAIL+=("${name}")
        printf '  \033[31mFAIL\033[0m %s  (cmd: %s)\n' "${name}" "$*"
    fi
}

# Like `check`, but a failure is non-fatal — used for optional tools
# (e.g., mull, which is gated on DESIGN.md Risk 1 and only needed for
# the C++ mutation row; its absence is documented as asterisked).
check_optional() {
    local name="$1"; shift
    if "$@" >/dev/null 2>&1; then
        PASS+=("${name}")
        printf '  \033[32mOK\033[0m   %s\n' "${name}"
    else
        WARN+=("${name}")
        printf '  \033[33mWARN\033[0m %s  (cmd: %s)  (optional)\n' "${name}" "$*"
    fi
}

echo "== BioTest benchmark image — tool verification =="
echo

check "bash"                 bash --version
check "git"                  git --version
check "curl"                 curl --version
check "cmake"                cmake --version
check "jq"                   jq --version

echo
echo "-- JVM --"
check "JDK 17 (Temurin)"     java -version
check "javac 17"             javac -version
check "gradle"               gradle --version
check "mvn"                  mvn -version

echo
echo "-- Python (BioTest / 3.12) --"
check "python3.12"           python3.12 --version
check "pip (3.12)"           python3.12 -m pip --version
check "mutmut"               python3.12 -c "import mutmut; print(mutmut.__version__)"
check "coverage.py (3.12)"   python3.12 -m coverage --version
check "pysam (3.12)"         python3.12 -c "import pysam; print(pysam.__version__)"
check "biopython (3.12)"     python3.12 -c "import Bio; print(Bio.__version__)"

echo
echo "-- Python (Atheris venv / 3.11) --"
check "python3.11 venv"      /opt/atheris-venv/bin/python --version
check "atheris"              /opt/atheris-venv/bin/python -c "import atheris; atheris.Setup"
check "pysam (atheris venv)" /opt/atheris-venv/bin/python -c "import pysam; print(pysam.__version__)"
check "biopython (atheris venv)" /opt/atheris-venv/bin/python -c "import Bio; print(Bio.__version__)"

echo
echo "-- C/C++ --"
check "clang-18"             clang --version
check "clang++-18"           clang++ --version
check "lld"                  ld.lld --version
check "llvm-symbolizer"      llvm-symbolizer --version
check "gcovr"                gcovr --version
check "lcov"                 lcov --version
check "seqan3 headers present" test -f /opt/seqan3/include/seqan3/version.hpp
check "seqan3 Clang patch (macro)" bash -c "grep -q 'defined(__clang__)' /opt/seqan3/include/seqan3/utility/type_traits/basic.hpp"
check "seqan3 Clang patch (friend)" bash -c "grep -q 'template <typename range_type, template <typename...> typename derived_t_template' /opt/seqan3/include/seqan3/utility/views/repeat.hpp"
check "seqan3 sam_file compile (Clang 18 + patches)" \
                             bash -c "echo '#include <seqan3/io/sam_file/input.hpp>' | clang++ -std=c++23 -DSEQAN3_DISABLE_COMPILER_CHECK -x c++ -fsyntax-only -"
check "seqan3 sam_file compile (GCC 12)" \
                             bash -c "echo '#include <seqan3/io/sam_file/input.hpp>' | g++-12 -std=c++23 -x c++ -fsyntax-only -"

echo
echo "-- Fuzzers / mutation tools --"
check "jazzer"               /opt/jazzer/jazzer --help
check "libFuzzer stub"       bash -c "printf '#include <cstdint>\n#include <cstddef>\nextern \"C\" int LLVMFuzzerTestOneInput(const uint8_t*, size_t){return 0;}\n' | clang++ -fsanitize=fuzzer -x c++ -o /tmp/_libfuzz_probe -"
check "afl-g++"              bash -c "command -v afl-g++ >/dev/null"
check "afl-fuzz"             bash -c "command -v afl-fuzz >/dev/null"
check "g++-12 (seqan3 AFL++)" bash -c "command -v g++-12 >/dev/null"
check "AFL_PATH populated"   bash -c "test -f \"${AFL_PATH:-/opt/aflpp/lib/afl}/afl-compiler-rt.o\""
check "evosuite jar"         bash -c "test -s /opt/evosuite/evosuite.jar"
check "pit jar"              bash -c "test -s /opt/pit/pitest-command-line.jar"
check_optional "mull (C++ mutation; gated on DESIGN.md Risk 1)" \
                             bash -c "command -v mull-runner-18 >/dev/null || command -v mull-runner >/dev/null"

echo
echo "=============================================="
printf '  PASS: %d\n' "${#PASS[@]}"
printf '  WARN: %d  %s\n' "${#WARN[@]}" "${WARN[*]:-}"
printf '  FAIL: %d  %s\n' "${#FAIL[@]}" "${FAIL[*]:-}"
echo "=============================================="

# Non-zero exit only if a REQUIRED tool is missing. Optional tools
# (check_optional) are allowed to warn without failing CI.
if [[ ${#FAIL[@]} -gt 0 ]]; then
    exit 1
fi
