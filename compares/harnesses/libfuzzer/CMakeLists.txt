# libFuzzer harness build shim for seqan3 SAM parsing.
#
# Prereqs (see compares/DESIGN.md §9 Risk 1):
#   - Linux / WSL2 Ubuntu 22.04+
#   - Clang 18+ with libFuzzer support
#   - seqan3 >= 3.3.0 headers (in /opt/seqan3/include inside biotest-bench)
#   - sdsl-lite v3 headers (in /opt/sdsl-lite/include)
#
# Build:
#   mkdir -p build && cd build
#   cmake -DCMAKE_CXX_COMPILER=clang++-18 ..
#   make seqan3_sam_fuzzer
#
# We deliberately do NOT use `find_package(seqan3)` because the upstream
# seqan3-config.cmake wires up a target that adds flags (SEQAN3_SUBMODULES_DIR,
# sdsl include dirs) we already handle via CPLUS_INCLUDE_PATH in the
# Docker image. Going header-only keeps the build config the same across
# distro-apt and clone-from-source installs.

cmake_minimum_required(VERSION 3.20)
project(biotest_libfuzzer_harnesses CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# libFuzzer + AddressSanitizer + UBSan = the "fuzzer" triumvirate.
set(FUZZER_FLAGS "-g -O1 -fsanitize=fuzzer,address,undefined")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${FUZZER_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${FUZZER_FLAGS}")

add_executable(seqan3_sam_fuzzer seqan3_sam_fuzzer.cpp)

# seqan3 requires the C++23 iostream model + cereal / range-v3 headers.
# cereal + range-v3 come from apt (libcereal-dev, librange-v3-dev); the
# paths land on the default include path. seqan3 + sdsl-lite are
# clone-mounted and injected via CPLUS_INCLUDE_PATH in the Dockerfile;
# no per-target include flag is needed here.
