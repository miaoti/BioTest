// Fuzz harness for seqan3's SAM parsing path.
//
// Produces a binary that can be driven by either libFuzzer OR AFL++.
// The `LLVMFuzzerTestOneInput` entry is the fuzz target. When built
// for libFuzzer (Clang + -fsanitize=fuzzer), libFuzzer provides its
// own `main`. When built for anything else (AFL++, bare testing), we
// provide a simple stdin-reader `main` that calls the target once
// per execution — compatible with AFL++ classic fork-server mode.
//
// Build (libFuzzer + Clang 18 — primary; requires seqan3 Clang patches
// baked into biotest-bench):
//     bash compares/scripts/build_harnesses.sh libfuzzer
//     # → compares/harnesses/libfuzzer/build/seqan3_sam_fuzzer_libfuzzer
//
// Build (AFL++ + GCC 12 — alternate):
//     bash compares/scripts/build_harnesses.sh aflpp
//     # → compares/harnesses/libfuzzer/build-aflpp/seqan3_sam_fuzzer_aflpp
//
// Run (AFL++):
//     AFL_SKIP_CPUFREQ=1 afl-fuzz -i seeds/sam -o /tmp/fuzz-out \
//         -- ./seqan3_sam_fuzzer_aflpp
//
// Run (libFuzzer):
//     ./seqan3_sam_fuzzer_libfuzzer \
//         -artifact_prefix=/tmp/crashes/ \
//         -max_total_time=7200 \
//         seeds/sam
//
// Touching only `id()` and `sequence()` keeps the concept-instantiation
// storm under control — richer fields (cigar_sequence, tags) trigger
// cascading template errors from seqan3's `alphabet_tuple_base`
// constraints under Clang.

#include <cstddef>
#include <cstdint>
#include <exception>
#include <sstream>
#include <string>

#include <seqan3/io/sam_file/input.hpp>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    try {
        std::string buf(reinterpret_cast<const char *>(data), size);
        std::istringstream iss(std::move(buf));

        seqan3::sam_file_input fin{iss, seqan3::format_sam{}};
        for (auto && record : fin) {
            auto const & id = record.id();
            auto const & seq = record.sequence();
            (void)id;
            (void)seq;
        }
    } catch (std::exception const &) {
        // seqan3 throws on malformed input; that's expected, not a bug.
    }

    return 0;
}

// ---- AFL++ / standalone driver ----------------------------------------
// libFuzzer provides its own `main`, so we must NOT define one when
// building the libfuzzer target. The CMake `libfuzzer` target sets
// BIOTEST_HARNESS_LIBFUZZER=1 to suppress this block.
//
// Everywhere else (AFL++, bare binary) we provide a simple stdin->
// LLVMFuzzerTestOneInput shim. AFL++ classic fork-server mode reads
// this main once per input and exits; AFL++ handles the fork-per-input
// loop via its instrumented runtime.

#ifndef BIOTEST_HARNESS_LIBFUZZER
#include <cstdio>

int main() {
    // 1 MiB is well above the size of any real SAM record. Inputs
    // larger than this are truncated; AFL++ stops growing once it
    // stops gaining coverage.
    static unsigned char buf[1 << 20];
    size_t n = std::fread(buf, 1, sizeof(buf), stdin);
    LLVMFuzzerTestOneInput(buf, n);
    return 0;
}
#endif
