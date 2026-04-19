# libFuzzer harness build shim for seqan3 SAM parsing.
#
# Prereqs (see compares/DESIGN.md §9 Risk 1):
#   - Linux / WSL2 Ubuntu 22.04+
#   - Clang 18+ with libFuzzer support
#   - libseqan3-dev (C++23)
#
# Build:
#   mkdir -p build && cd build
#   cmake -DCMAKE_CXX_COMPILER=clang++-18 ..
#   make seqan3_sam_fuzzer

cmake_minimum_required(VERSION 3.20)
project(biotest_libfuzzer_harnesses CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# seqan3 via installed libseqan3-dev (preferred) or seqan3-config.cmake.
find_package(seqan3 REQUIRED)

# libFuzzer + AddressSanitizer + UBSan = the "fuzzer" triumvirate.
set(FUZZER_FLAGS "-g -O1 -fsanitize=fuzzer,address,undefined")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${FUZZER_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${FUZZER_FLAGS}")

add_executable(seqan3_sam_fuzzer seqan3_sam_fuzzer.cpp)
target_link_libraries(seqan3_sam_fuzzer PRIVATE seqan3::seqan3)
