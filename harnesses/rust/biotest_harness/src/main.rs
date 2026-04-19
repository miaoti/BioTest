// biotest_harness — TEMPLATE skeleton for a Rust-language SUT.
//
// Fill in the FILL_IN sections with calls into your SUT's crate.
// CLI shapes mirror the Java + C harnesses:
//   biotest_harness <VCF|SAM> <path>                    → parse mode
//   biotest_harness --mode discover_methods <VCF|SAM>   → discover mode
//   biotest_harness --mode query <VCF|SAM> <path> \
//                    --methods n1,n2,n3                  → query mode
//
// Reference: Chen-Kuo-Liu-Tse 2018 §3.2; MR-Scout TOSEM 2024
// (arXiv:2304.07548); rustdoc-json RFC #2963.
//
// Onboarding: see harnesses/rust/README.md.

use serde_json::{json, Value};
use std::env;
use std::process::ExitCode;

// FILL_IN: replace this stub with your SUT's parsed-record type.
struct Record;

// FILL_IN: open `path`, parse, return the first record (or None on error).
fn parse_input(_path: &str, _fmt: &str) -> Option<Record> {
    None
}

// FILL_IN: dispatch — return a serde_json::Value for the named method.
// Uncomment + extend the example match arms once you have your SUT type:
//
//     "is_structural" => json!(rec.is_structural()),
//     "n_alleles"     => json!(rec.n_alleles()),
//     "chrom"         => json!(rec.chrom()),
fn dispatch_method(_name: &str, _rec: &Record) -> Value {
    json!({"__error__": "unknown method"})
}

// ---------------------------------------------------------------------
// Discovered methods manifest. Generated once via:
//   py -3.12 -m harnesses._reflect.rustdoc_parser \
//       --rustdoc-json target/doc/<crate>.json \
//       --type Record --sut-name my_rust_parser
// Either embed the resulting JSON here or read it from a sibling file
// at runtime. Keeping it embedded means the binary is self-contained.
// ---------------------------------------------------------------------
const METHODS_MANIFEST_VCF: &str = r#"{"methods":[]}"#;
const METHODS_MANIFEST_SAM: &str = r#"{"methods":[]}"#;

fn run_parse(fmt: &str, path: &str) -> ExitCode {
    let _ = parse_input(path, fmt);
    // FILL_IN: emit your canonical JSON. Match the schema in
    // test_engine/canonical/schema.py (CanonicalVcf or CanonicalSam).
    println!("{}", "{}");
    ExitCode::SUCCESS
}

fn run_discover(fmt: &str) -> ExitCode {
    let manifest = match fmt.to_ascii_uppercase().as_str() {
        "VCF" => METHODS_MANIFEST_VCF,
        "SAM" => METHODS_MANIFEST_SAM,
        _ => {
            eprintln!("discover_methods: unknown format {}", fmt);
            return ExitCode::FAILURE;
        }
    };
    println!("{}", manifest);
    ExitCode::SUCCESS
}

fn run_query(fmt: &str, path: &str, methods_csv: &str) -> ExitCode {
    let rec = parse_input(path, fmt);
    let mut results = serde_json::Map::new();
    for name in methods_csv.split(',').map(|s| s.trim()).filter(|s| !s.is_empty()) {
        let value = match &rec {
            None => json!({"__error__": "parse_failed"}),
            Some(r) => dispatch_method(name, r),
        };
        results.insert(name.to_string(), value);
    }
    println!("{}", json!({"method_results": Value::Object(results)}));
    ExitCode::SUCCESS
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!(
            "Usage:\n\
             \t{0} <VCF|SAM> <path>                            # parse\n\
             \t{0} --mode discover_methods <VCF|SAM>           # discover\n\
             \t{0} --mode query <VCF|SAM> <path> --methods n1,n2  # query",
            args[0],
        );
        return ExitCode::FAILURE;
    }
    if args[1] == "--mode" && args.len() >= 3 {
        let mode = &args[2];
        if mode == "discover_methods" && args.len() >= 4 {
            return run_discover(&args[3]);
        }
        if mode == "query" && args.len() >= 7 && args[5] == "--methods" {
            return run_query(&args[3], &args[4], &args[6]);
        }
        eprintln!("Bad --mode invocation");
        return ExitCode::FAILURE;
    }
    if args.len() < 3 {
        eprintln!("parse mode requires <VCF|SAM> <path>");
        return ExitCode::FAILURE;
    }
    run_parse(&args[1], &args[2])
}
