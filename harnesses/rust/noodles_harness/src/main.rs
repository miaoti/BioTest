// BioTest canonical-JSON harness for noodles-vcf.
//
// Usage:
//   noodles_harness VCF <input.vcf>      -> canonical JSON to stdout
//
// Exit 0 on success; non-zero with message on stderr otherwise. This
// mirrors the contract in test_engine/canonical/schema.py and every
// other SUT harness (harnesses/java/BioTestHarness.java,
// harnesses/pysam/pysam_harness.py, harnesses/cpp/biotest_harness.cpp).
//
// noodles-vcf uses 1-based POS natively for the text VCF reader; no
// +1 shim required (unlike pysam's Cython stack).
//
// Coverage build (only run when you want per-line Rust coverage):
//   cargo install cargo-llvm-cov     # once
//   cargo llvm-cov --no-report \
//       --manifest-path harnesses/rust/noodles_harness/Cargo.toml \
//       run -- VCF seeds/vcf/minimal_single.vcf
//   cargo llvm-cov report --json \
//       --manifest-path harnesses/rust/noodles_harness/Cargo.toml \
//       > coverage_artifacts/noodles/llvm-cov.json

use std::collections::BTreeMap;
use std::env;
use std::fs::File;
use std::io::{self, BufReader, Write};
use std::path::Path;
use std::process::ExitCode;

use noodles_vcf as vcf;
use serde_json::{json, Map, Value};

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!(
            "usage: {} <VCF> <input_file>",
            args.first().map(String::as_str).unwrap_or("noodles_harness")
        );
        return ExitCode::from(1);
    }
    let fmt = args[1].to_uppercase();
    let input = &args[2];

    if fmt != "VCF" {
        eprintln!(
            "noodles_harness currently supports VCF only (got {fmt}). \
             SAM via noodles-sam can be added as a follow-on harness."
        );
        return ExitCode::from(1);
    }

    match parse_vcf(Path::new(input)) {
        Ok(v) => {
            let stdout = io::stdout();
            let mut lock = stdout.lock();
            if let Err(e) = serde_json::to_writer_pretty(&mut lock, &v) {
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

fn parse_vcf(path: &Path) -> Result<Value, Box<dyn std::error::Error>> {
    let file = File::open(path)?;
    let mut reader = vcf::io::reader::Builder::default().build_from_reader(BufReader::new(file))?;

    let header = reader.read_header()?;

    // ----------------------------------------------------------------
    // Header → canonical
    // ----------------------------------------------------------------
    let fileformat = format!("{}", header.file_format());

    let mut meta: Map<String, Value> = Map::new();

    // INFO
    let mut info_map = Map::new();
    for (id, rec) in header.infos() {
        let mut fields = Map::new();
        fields.insert("ID".into(), Value::String(id.to_string()));
        fields.insert("Number".into(), Value::String(format!("{}", rec.number())));
        fields.insert("Type".into(), Value::String(format!("{:?}", rec.ty())));
        fields.insert("Description".into(), Value::String(rec.description().to_string()));
        info_map.insert(id.to_string(), Value::Object(fields));
    }
    if !info_map.is_empty() {
        meta.insert("INFO".into(), Value::Object(info_map));
    }

    // FORMAT
    let mut format_map = Map::new();
    for (id, rec) in header.formats() {
        let mut fields = Map::new();
        fields.insert("ID".into(), Value::String(id.to_string()));
        fields.insert("Number".into(), Value::String(format!("{}", rec.number())));
        fields.insert("Type".into(), Value::String(format!("{:?}", rec.ty())));
        fields.insert("Description".into(), Value::String(rec.description().to_string()));
        format_map.insert(id.to_string(), Value::Object(fields));
    }
    if !format_map.is_empty() {
        meta.insert("FORMAT".into(), Value::Object(format_map));
    }

    // FILTER
    let mut filter_map = Map::new();
    for (id, rec) in header.filters() {
        let mut fields = Map::new();
        fields.insert("ID".into(), Value::String(id.to_string()));
        fields.insert("Description".into(), Value::String(rec.description().to_string()));
        filter_map.insert(id.to_string(), Value::Object(fields));
    }
    if !filter_map.is_empty() {
        meta.insert("FILTER".into(), Value::Object(filter_map));
    }

    // contig
    let mut contig_map = Map::new();
    for (id, rec) in header.contigs() {
        let mut fields = Map::new();
        fields.insert("ID".into(), Value::String(id.to_string()));
        if let Some(len) = rec.length() {
            fields.insert("length".into(), Value::Number(serde_json::Number::from(len as u64)));
        }
        contig_map.insert(id.to_string(), Value::Object(fields));
    }
    if !contig_map.is_empty() {
        meta.insert("contig".into(), Value::Object(contig_map));
    }

    let samples: Vec<Value> = header
        .sample_names()
        .iter()
        .map(|s| Value::String(s.to_string()))
        .collect();

    // ----------------------------------------------------------------
    // Records → canonical
    // ----------------------------------------------------------------
    let mut records: Vec<Value> = Vec::new();
    let mut record = vcf::Record::default();

    while reader.read_record(&mut record)? != 0 {
        let chrom = record.reference_sequence_name().to_string();

        let pos_i64 = match record.variant_start() {
            Some(p) => match p {
                Ok(p) => usize::from(p) as i64,
                Err(e) => return Err(Box::new(e)),
            },
            None => 0,
        };

        let id: Option<String> = {
            let ids_text = record.ids().as_ref().to_string();
            if ids_text.is_empty() || ids_text == "." {
                None
            } else {
                Some(ids_text)
            }
        };

        let reference_bases = record.reference_bases().to_string();

        let alt: Vec<Value> = {
            let raw = record.alternate_bases().as_ref().to_string();
            if raw.is_empty() || raw == "." {
                vec![]
            } else {
                raw.split(',').map(|s| Value::String(s.to_string())).collect()
            }
        };

        let qual: Value = match record.quality_score() {
            Some(q) => match q {
                Ok(q) => Value::from(q as f64),
                Err(_) => Value::Null,
            },
            None => Value::Null,
        };

        // FILTER: sort to match canonical multiset semantics
        let mut filter: Vec<String> = Vec::new();
        let raw_filters = record.filters().as_ref().to_string();
        if !raw_filters.is_empty() && raw_filters != "." {
            for f in raw_filters.split(';') {
                filter.push(f.to_string());
            }
        }
        filter.sort();

        // INFO: iterate and coerce; sort keys
        let mut info_entries: BTreeMap<String, Value> = BTreeMap::new();
        for item in record.info().iter(&header) {
            let (key, val) = match item {
                Ok(kv) => kv,
                Err(e) => return Err(Box::new(e)),
            };
            let key_s = key.to_string();
            let v_json = match val {
                Some(v) => Value::String(format!("{v:?}")),
                None => Value::Null,
            };
            info_entries.insert(key_s, v_json);
        }
        let info_val: Value = Value::Object(
            info_entries
                .into_iter()
                .collect::<serde_json::Map<String, Value>>(),
        );

        // FORMAT + samples
        let mut fmt_keys: Option<Vec<Value>> = None;
        let mut sample_map: Map<String, Value> = Map::new();
        let samples_view = record.samples();
        let keys = samples_view.keys();
        let keys_text = keys.as_ref().to_string();
        if !keys_text.is_empty() && keys_text != "." {
            let key_list: Vec<String> = keys_text.split(':').map(String::from).collect();
            fmt_keys = Some(key_list.iter().cloned().map(Value::String).collect());

            for (sample_name, sample) in header.sample_names().iter().zip(samples_view.iter()) {
                let mut entry = Map::new();
                for (k, v) in key_list.iter().zip(sample.values()) {
                    let v_json = match v {
                        Some(v) => Value::String(format!("{v:?}")),
                        None => Value::Null,
                    };
                    entry.insert(k.clone(), v_json);
                }
                sample_map.insert(sample_name.to_string(), Value::Object(entry));
            }
        }

        records.push(json!({
            "CHROM": chrom,
            "POS": pos_i64,
            "ID": id,
            "REF": reference_bases,
            "ALT": alt,
            "QUAL": qual,
            "FILTER": filter,
            "INFO": info_val,
            "FORMAT": fmt_keys,
            "samples": if sample_map.is_empty() { Value::Null } else { Value::Object(sample_map) },
        }));
    }

    Ok(json!({
        "format": "VCF",
        "header": {
            "fileformat": fileformat,
            "meta": Value::Object(meta),
            "samples": samples,
        },
        "records": records,
    }))
}
