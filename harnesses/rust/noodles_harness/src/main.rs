// BioTest noodles-vcf harness — minimal 2026-04-20 rewrite.
//
// The previous implementation hand-rolled a canonical-JSON serializer that
// tracked every noodles-vcf 0.x API surface and drifted with each crate
// bump. For the Phase-1 validity probe (and the Phase-4 bug-bench signal
// classifier) the harness only needs to answer two questions per input
// file:
//
//   1. Did the parser accept this file?   (exit 0 vs non-zero)
//   2. How many records did it read?       (cheap integer counter)
//
// Full canonical-JSON parity with BioTestHarness.java lives in follow-on
// work (see §13.2.7 mutation-compat notes). Until then, this stub keeps
// `is_available()` true in `NoodlesRunner`, lets the validity probe count
// `parse_success` / `generated_total`, and prints a canonical-ish stub JSON
// so downstream consumers don't choke on an empty stdout.
//
// Usage:
//   noodles_harness VCF <input.vcf>
//   noodles_harness --mode write_roundtrip VCF <input> <output>

use std::env;
use std::fs::File;
use std::io::{self, BufReader, BufWriter, Write as IoWrite};
use std::path::Path;
use std::process::ExitCode;

use noodles_vcf as vcf;
use noodles_vcf::variant::io::Write as VcfWrite;
use serde_json::json;

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    let argv: Vec<&str> = args.iter().map(String::as_str).collect();

    match argv.as_slice() {
        [_, "--mode", "write_roundtrip", fmt, input, output] => {
            if fmt.to_uppercase() != "VCF" {
                eprintln!("write_roundtrip: VCF only (got {fmt})");
                return ExitCode::from(1);
            }
            match write_roundtrip(Path::new(input), Path::new(output)) {
                Ok(()) => ExitCode::SUCCESS,
                Err(e) => {
                    eprintln!("write_roundtrip error: {e}");
                    ExitCode::from(1)
                }
            }
        }
        [_, fmt, input] => {
            if fmt.to_uppercase() != "VCF" {
                eprintln!(
                    "noodles_harness currently supports VCF only (got {fmt})."
                );
                return ExitCode::from(1);
            }
            match parse_vcf(Path::new(input)) {
                Ok((header_fmt, record_count, sample_count)) => {
                    let stub = json!({
                        "format": "VCF",
                        "header": {
                            "fileformat": header_fmt,
                            "sample_count": sample_count,
                        },
                        "records_read": record_count,
                    });
                    let stdout = io::stdout();
                    let mut lock = stdout.lock();
                    if let Err(e) = serde_json::to_writer(&mut lock, &stub) {
                        eprintln!("serialize error: {e}");
                        return ExitCode::from(1);
                    }
                    let _ = lock.write_all(b"\n");
                    ExitCode::SUCCESS
                }
                Err(e) => {
                    eprintln!("parse error: {e}");
                    ExitCode::from(1)
                }
            }
        }
        _ => {
            eprintln!(
                "usage:\n  {bin} VCF <input_file>\n  \
                 {bin} --mode write_roundtrip VCF <input> <output>",
                bin = args.first().map(String::as_str).unwrap_or("noodles_harness"),
            );
            ExitCode::from(1)
        }
    }
}

fn parse_vcf(
    path: &Path,
) -> Result<(String, usize, usize), Box<dyn std::error::Error>> {
    let file = File::open(path)?;
    let mut reader =
        vcf::io::reader::Builder::default().build_from_reader(BufReader::new(file))?;
    let header = reader.read_header()?;

    // FileFormat doesn't implement Display on every noodles-vcf minor;
    // Debug is stable across the 0.x range.
    let header_fmt = format!("{:?}", header.file_format());
    let sample_count = header.sample_names().len();

    let mut count = 0usize;
    let mut record = vcf::Record::default();
    while reader.read_record(&mut record)? != 0 {
        count += 1;
    }
    Ok((header_fmt, count, sample_count))
}

fn write_roundtrip(
    input: &Path,
    output: &Path,
) -> Result<(), Box<dyn std::error::Error>> {
    let in_file = File::open(input)?;
    let mut reader =
        vcf::io::reader::Builder::default().build_from_reader(BufReader::new(in_file))?;
    let header = reader.read_header()?;

    let out_file = File::create(output)?;
    let mut writer = vcf::io::writer::Writer::new(BufWriter::new(out_file));
    writer.write_header(&header)?;

    let mut record = vcf::Record::default();
    while reader.read_record(&mut record)? != 0 {
        // noodles-vcf 0.70 exposes the write trait as
        // `noodles_vcf::variant::io::Write`; aliased above so the
        // std::io::Write import isn't shadowed.
        VcfWrite::write_variant_record(&mut writer, &header, &record)?;
    }
    Ok(())
}
