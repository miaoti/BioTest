# Build shim for the seqan3 SAM fuzzer harness.
#
# Two targets build the same source file (`seqan3_sam_fuzzer.cpp`)
# with different coverage + fuzzer runtimes:
#
#   seqan3_sam_fuzzer_libfuzzer
#       Clang 18 + libFuzzer + AddressSanitizer. DESIGN §9 Risk 1:
#       currently BLOCKED — Clang 18 rejects seqan3 3.x
#       `alphabet_tuple_base` concept constraints. Kept in the tree
#       so the target is ready the day seqan3 ships Clang support.
#
#   seqan3_sam_fuzzer_aflpp
#       GCC 12 + AFL++ (via afl-g++). Works today because GCC accepts
#       seqan3's concept declarations. This is the production C++
#       fuzzer for the comparison matrix.
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

# -------- Target 1: libFuzzer (Clang 18, gated) --------
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    set(FUZZER_FLAGS "-g -O1 -fsanitize=fuzzer,address,undefined")
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

# If no compatible target was enabled above, error out. Otherwise a
# bare `make` silently produces nothing and confuses the adapter.
if(NOT (CMAKE_CXX_COMPILER_ID STREQUAL "Clang") AND NOT (AFL_GXX AND GXX_12))
    message(FATAL_ERROR
        "Neither the libFuzzer (Clang) nor the AFL++ (afl-g++ + g++-12) "
        "target is buildable. Install one of them.")
endif()
