# Build shim for the seqan3 SAM fuzzer harness.
#
# Two targets build the same source file (`seqan3_sam_fuzzer.cpp`)
# with different coverage + fuzzer runtimes:
#
#   seqan3_sam_fuzzer_libfuzzer
#       Clang 18 + libFuzzer + AddressSanitizer. PRIMARY C++ fuzzer
#       for the bug bench. Requires the two seqan3 Clang patches
#       baked into biotest-bench (DESIGN §13.2.4): the
#       SEQAN3_IS_CONSTEXPR macro short-circuit and the repeat_view
#       friend-declaration fix.
#
#   seqan3_sam_fuzzer_aflpp
#       GCC 12 + AFL++ (via afl-g++). Verified alternate target;
#       compiles on vanilla seqan3 without the Clang patches.
#
# Build one or both:
#   mkdir -p build && cd build
#   cmake -DCMAKE_CXX_COMPILER=clang++-18 ..      # only libfuzzer target
#   cmake -DCMAKE_CXX_COMPILER=g++-12 ..          # only aflpp target
#
# Both targets use the same `LLVMFuzzerTestOneInput` entry signature;
# the code is portable between libFuzzer and AFL++.

cmake_minimum_required(VERSION 3.20)
project(biotest_cpp_fuzz_harnesses CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# seqan3 + sdsl-lite are injected via CPLUS_INCLUDE_PATH in the
# biotest-bench image (see Dockerfile) and via -I on the host.

# -------- Target 1: libFuzzer (Clang 18) --------
# Unblocked on 2026-04-19 via two in-tree seqan3 patches applied by
# the biotest-bench Dockerfile: (a) SEQAN3_IS_CONSTEXPR short-circuits
# to `true` under __clang__ (the original uses __builtin_constant_p
# which Clang evaluates differently than GCC in concept contexts);
# (b) `repeat_view`'s friend declaration of `random_access_iterator_base`
# matches the real 3-param template signature, not the 2-param one.
# Both patches are idempotent and documented in the Dockerfile.
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    # List form (not quoted string) so CMake splits on spaces and each
    # flag reaches clang++ as its own argv entry. The sanitize triple
    # produces an in-process coverage-guided fuzzer with memory safety.
    set(FUZZER_FLAGS -g -O1 -fsanitize=fuzzer,address,undefined)
    add_executable(seqan3_sam_fuzzer_libfuzzer seqan3_sam_fuzzer.cpp)
    # BIOTEST_HARNESS_LIBFUZZER=1 suppresses our stdin-reader main()
    # because libFuzzer provides its own.
    target_compile_definitions(seqan3_sam_fuzzer_libfuzzer PRIVATE
        BIOTEST_HARNESS_LIBFUZZER=1)
    target_compile_options(seqan3_sam_fuzzer_libfuzzer PRIVATE
        ${FUZZER_FLAGS})
    target_link_options(seqan3_sam_fuzzer_libfuzzer PRIVATE
        ${FUZZER_FLAGS})
    message(STATUS "Building libFuzzer target (Clang)")
endif()

# -------- Target 2: AFL++ (GCC 12, production) --------
# CMake doesn't know how to invoke afl-g++ natively; we wrap the
# compile in a custom command so Make delegates to AFL++'s wrapper.
find_program(AFL_GXX afl-g++)
find_program(GXX_12 g++-12)
if(AFL_GXX AND GXX_12)
    # AFL++'s wrapper reads AFL_CC/AFL_CXX from the env to pick which
    # underlying compiler it should drive. Pin it to g++-12 because
    # seqan3 needs libstdc++ 12.
    add_custom_target(seqan3_sam_fuzzer_aflpp ALL
        COMMAND ${CMAKE_COMMAND} -E env AFL_CXX=${GXX_12}
                ${AFL_GXX} -std=c++23 -O2 -g
                ${CMAKE_CURRENT_SOURCE_DIR}/seqan3_sam_fuzzer.cpp
                -o ${CMAKE_CURRENT_BINARY_DIR}/seqan3_sam_fuzzer_aflpp
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Building AFL++ target (afl-g++ + g++-12)"
        VERBATIM)
    message(STATUS "AFL++ + g++-12 found, aflpp target enabled")
else()
    message(WARNING "afl-g++ or g++-12 missing; aflpp target skipped")
endif()

# -------- Target 3: Coverage replay (Clang 18, --coverage / gcov) --------
# Offline replay binary that consumes ONE corpus file on stdin,
# calls LLVMFuzzerTestOneInput, and emits .gcda files for gcovr to
# aggregate into a JSON report. Used by compares/scripts/coverage_sampler.py
# to measure cumulative coverage at log ticks against the libFuzzer
# corpus — libFuzzer's own binary is built for speed (no gcov), so
# coverage measurement happens out-of-band against this sibling.
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    # --coverage expands to -fprofile-arcs -ftest-coverage at compile +
    # -lgcov at link. -O0 keeps line-level fidelity; -g embeds source
    # paths so gcovr can map .gcno/.gcda back to headers under
    # /opt/seqan3/include.
    set(COV_FLAGS -g -O0 --coverage)
    add_executable(seqan3_sam_fuzzer_cov seqan3_sam_fuzzer.cpp)
    # BIOTEST_HARNESS_LIBFUZZER is NOT set here — we want the stdin-
    # reader main() that drives a single invocation per exec.
    target_compile_options(seqan3_sam_fuzzer_cov PRIVATE ${COV_FLAGS})
    target_link_options(seqan3_sam_fuzzer_cov PRIVATE ${COV_FLAGS})
    message(STATUS "Building coverage replay target (Clang + --coverage)")
endif()

# If no compatible target was enabled above, error out. Otherwise a
# bare `make` silently produces nothing and confuses the adapter.
if(NOT (CMAKE_CXX_COMPILER_ID STREQUAL "Clang") AND NOT (AFL_GXX AND GXX_12))
    message(FATAL_ERROR
        "Neither the libFuzzer (Clang) nor the AFL++ (afl-g++ + g++-12) "
        "target is buildable. Install one of them.")
endif()
