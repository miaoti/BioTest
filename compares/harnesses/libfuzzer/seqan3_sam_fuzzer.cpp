// Fuzz harness for seqan3's SAM parsing path.
//
// Produces a binary that can be driven by either libFuzzer OR AFL++.
// The `LLVMFuzzerTestOneInput` entry is the fuzz target. Under AFL++
// we also provide a `main()` that pumps stdin into the fuzz target in
// persistent mode (1000× faster than classic fork mode).
//
// Build (production — AFL++ + GCC 12, works today):
//     cd compares/harnesses/libfuzzer
//     mkdir -p build && cd build
//     cmake -DCMAKE_CXX_COMPILER=g++-12 ..
//     make seqan3_sam_fuzzer_aflpp
//
// Build (libFuzzer + Clang 18, GATED on DESIGN §9 Risk 1):
//     cmake -DCMAKE_CXX_COMPILER=clang++-18 ..
//     make seqan3_sam_fuzzer_libfuzzer
//
// Run (AFL++):
//     mkdir -p /tmp/fuzz-out
//     afl-fuzz -i seeds/sam -o /tmp/fuzz-out -- ./seqan3_sam_fuzzer_aflpp
//
// Run (libFuzzer, when unblocked):
//     ./seqan3_sam_fuzzer_libfuzzer -seed_corpus=seeds/sam -max_total_time=7200
//
// Touching only `id()` and `sequence()` keeps the concept-instantiation
// storm under control — richer fields (cigar_sequence, tags) trigger
// cascading template errors from `alphabet_tuple_base`'s constraints.

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

// ---- AFL++ persistent-mode driver -------------------------------------
// Only compiled when afl-clang / afl-g++ is the front end. libFuzzer
// provides its own `main`, so we must NOT define one under that
// toolchain. AFL++'s wrapper defines `__AFL_HAVE_MANUAL_CONTROL` in
// persistent mode.

#ifdef __AFL_HAVE_MANUAL_CONTROL
#include <unistd.h>
#include <cstring>

// Declared but not defined by us; AFL++ provides the implementation
// via its linker magic when it sees these identifiers.
extern "C" void __AFL_INIT(void);
extern "C" int  __AFL_LOOP(unsigned int);

int main() {
    __AFL_INIT();
    // 1 MiB is well above the size of any real SAM record; inputs
    // larger than this are simply truncated — AFL++ stops growing
    // them quickly since they hit a plateau in coverage.
    static unsigned char buf[1 << 20];
    while (__AFL_LOOP(10000)) {
        ssize_t n = read(0, buf, sizeof(buf));
        if (n < 0) return 0;
        LLVMFuzzerTestOneInput(buf, static_cast<size_t>(n));
    }
    return 0;
}
#endif
