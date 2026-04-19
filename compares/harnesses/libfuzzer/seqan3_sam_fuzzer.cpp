// libFuzzer harness for seqan3's SAM parsing path.
//
// GATED on Risk 1 in compares/DESIGN.md §9. Requires Linux / WSL2
// Clang 18+ and libseqan3-dev v3.1.0+ (plus the xxsds/sdsl-lite v3
// headers that the biotest-bench Dockerfile pulls into
// /opt/sdsl-lite/include). The Dockerfile has verified this works.
//
// Build (from compares/harnesses/libfuzzer/):
//     mkdir -p build && cd build
//     cmake -DCMAKE_CXX_COMPILER=clang++-18 ..
//     make seqan3_sam_fuzzer
//
// Run:
//     ./build/seqan3_sam_fuzzer \
//         -seed_corpus=../../../seeds/sam \
//         -max_total_time=7200 \
//         -artifact_prefix=../../../results/libfuzzer/seqan3_sam/
//
// Field touching is deliberately minimal: seqan3 3.1's sam_record
// exposes many methods but most trigger cascading template
// instantiations on header-only types (seqan3::cigar, alphabet_tuple)
// that blow clang's error budget at compile time. The minimal `id()`
// + `sequence()` pair is enough to force full SAM parsing inside
// format_sam, which is the code path we care about.

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
