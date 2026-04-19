// libFuzzer harness for seqan3's SAM / BAM parsing path.
//
// GATED on Risk 1 in compares/DESIGN.md §9: the current BioTest C++
// harness does not link seqan3 on Windows/MinGW. This fuzzer requires a
// Linux/WSL2 build with Clang 18+ and libseqan3-dev. Seqan3 requires
// C++23. See harnesses/cpp/README.md for the WSL2 rewrite story.
//
// Build (from compares/harnesses/libfuzzer/):
//     mkdir -p build && cd build
//     cmake -DCMAKE_CXX_COMPILER=clang++-18 ..
//     make seqan3_sam_fuzzer
//
// Run:
//     ./build/seqan3_sam_fuzzer \
//         -seed_corpus=../../../../seeds/sam \
//         -max_total_time=7200 \
//         -artifact_prefix=../../../results/libfuzzer/seqan3_sam/ \
//         ./corpus/
//
// Seqan3 does NOT support VCF; no companion VCF fuzzer exists.

#include <cstddef>
#include <cstdint>
#include <sstream>
#include <string>

#include <seqan3/io/sam_file/input.hpp>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    try {
        // Route the byte stream through an istringstream so we don't
        // touch the filesystem per iteration (libFuzzer hot path).
        std::string buf(reinterpret_cast<const char *>(data), size);
        std::istringstream iss(std::move(buf));

        seqan3::sam_file_input fin{iss, seqan3::format_sam{}};
        for (auto &&record : fin) {
            // Resolve every lazy field so downstream decoder paths fire.
            auto const & id = record.id();
            auto const & flag = record.flag();
            auto const & ref_id = record.reference_id();
            auto const & ref_pos = record.reference_position();
            auto const & mapq = record.mapping_quality();
            auto const & cigar = record.cigar_sequence();
            auto const & seq = record.sequence();
            auto const & qual = record.base_qualities();
            auto const & tags = record.tags();

            (void)id;
            (void)flag;
            (void)ref_id;
            (void)ref_pos;
            (void)mapq;
            (void)cigar;
            (void)seq;
            (void)qual;
            (void)tags;
        }
    } catch (std::exception const &) {
        // seqan3 throws on malformed input; that's expected, not a bug.
    }

    return 0;
}
