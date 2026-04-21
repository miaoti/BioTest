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

// Phase 3 mutation-test mode (DESIGN §3.3 + §13.5 Phase 3):
// defining BIOTEST_HARNESS_MUT_DIGEST turns the single-input harness
// into a deterministic digest emitter that prints one line to stdout
// capturing (parse outcome, record count, id-hash, seq-length-sum).
// The Phase 3 mutation driver uses that line as the per-file
// observable: any mutation that shifts it between baseline + mutated
// runs is a kill, matching the "parse-success flip / canonical-JSON
// diff / crash flip" kill semantics of DESIGN §3.3.
#ifdef BIOTEST_HARNESS_MUT_DIGEST
#  include <cstdio>
#  include <cstdlib>
#endif

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
#ifdef BIOTEST_HARNESS_MUT_DIGEST
        std::printf("empty\n");
#endif
        return 0;
    }

    try {
        std::string buf(reinterpret_cast<const char *>(data), size);
        std::istringstream iss(std::move(buf));

        seqan3::sam_file_input fin{iss, seqan3::format_sam{}};
#ifdef BIOTEST_HARNESS_MUT_DIGEST
        std::size_t nrec = 0;
        std::size_t id_hash = 0;
        std::size_t seq_len_sum = 0;
#endif
        for (auto && record : fin) {
            auto const & id = record.id();
            auto const & seq = record.sequence();
            (void)id;
            (void)seq;
#ifdef BIOTEST_HARNESS_MUT_DIGEST
            ++nrec;
            // Rolling hash over ID characters (djb2-ish, modulo wrap).
            std::size_t h = 5381;
            for (char c : id) {
                h = ((h << 5) + h) + static_cast<unsigned char>(c);
            }
            id_hash ^= h;
            // Use size(seq) rather than .size() because seqan3's
            // sequence() yields a range-view in some configurations.
            std::size_t n = 0;
            for (auto && _ : seq) { (void)_; ++n; }
            seq_len_sum ^= n + (nrec * 2654435761ULL);
#endif
        }
#ifdef BIOTEST_HARNESS_MUT_DIGEST
        std::printf("ok %zu %zu %zu\n", nrec, id_hash, seq_len_sum);
#endif
    } catch (std::exception const &e) {
#ifdef BIOTEST_HARNESS_MUT_DIGEST
        // Collapse the exception message to a short, deterministic
        // fingerprint: first 40 chars, suffixed by message length.
        std::string m = e.what() ? e.what() : "";
        std::size_t len = m.size();
        if (m.size() > 40) { m.resize(40); m += "..."; }
        std::printf("throw %s [%zu]\n", m.c_str(), len);
#else
        (void)e;
#endif
    } catch (...) {
#ifdef BIOTEST_HARNESS_MUT_DIGEST
        std::printf("throw unknown\n");
#endif
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
