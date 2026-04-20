// cargo-fuzz target for the noodles-vcf Rust VCF parser.
//
// The libFuzzer runtime feeds `data: &[u8]` into `fuzz_target!`; we
// wrap it in a `Cursor` and drive the noodles-vcf streaming reader
// through header + records. Panics / aborts bubble up as libFuzzer
// findings (same signal class as the seqan3 libFuzzer harness).
//
// Pairs with the shared noodles-vcf version pin in
// `compares/harnesses/cargo_fuzz/fuzz/Cargo.toml`, which
// `bug_bench_driver._install_noodles` rewrites per-bug.
//
// Added 2026-04-20 as part of the pysam → vcfpy+noodles refactor
// (DESIGN §2.1, §4.1, §13.2.7).

#![no_main]

use libfuzzer_sys::fuzz_target;
use std::io::Cursor;

use noodles_vcf as vcf;

fuzz_target!(|data: &[u8]| {
    let mut reader = vcf::io::reader::Builder::default()
        .build_from_reader(Cursor::new(data))
        .ok()
        .map(|r| r);

    if let Some(mut reader) = reader.take() {
        // Header: malformed bytes → Err, which is a legitimate rejection
        // path and NOT a bug. Panic-class crashes are the findings we care
        // about, and those propagate automatically.
        let _ = reader.read_header();

        // Records: stream-parse until EOF or Err.
        let mut buf = String::new();
        loop {
            buf.clear();
            match reader.read_record(&mut buf) {
                Ok(0) => break,              // EOF
                Ok(_) => { /* consumed */ }
                Err(_) => break,             // rejection = not a crash
            }
        }
    }
});
