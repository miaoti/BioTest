// BioTest corpus-oracle test for cargo-mutants (Phase 3).
//
// This integration test re-enacts DESIGN.md §3.3's "test-kill protocol":
// for each file in the Phase-2 cargo-fuzz accepted corpus, parse the
// file with the (possibly mutated) noodles-vcf, and compute a
// deterministic fingerprint of the per-file outcome. Compare that
// fingerprint to a pre-captured baseline captured against the
// unmutated crate. On any divergence, the test panics → cargo test
// fails → cargo-mutants records the mutant as caught (killed).
//
// Two modes driven by env vars:
//   BIOTEST_BASELINE_MODE=capture BIOTEST_BASELINE_JSON=<path>
//     → read corpus, write fingerprint to <path>, never fail.
//   BIOTEST_BASELINE_MODE=check (default when JSON exists)
//     → read corpus + fingerprint, panic on mismatch.
//
// Other env:
//   BIOTEST_CORPUS_DIR  — directory containing VCF files (required).
//   BIOTEST_CORPUS_SAMPLE — max files to replay (deterministic
//                            first-N after sort). Default 200.
//   BIOTEST_PER_FILE_TIMEOUT_MS — not currently enforced (the fuzz
//                                 corpus is bounded already), but
//                                 reserved to match DESIGN §3.3
//                                 semantics on future adversarial
//                                 inputs.
//
// Cargo-mutants passes env vars through to `cargo test`, so setting
// these at `cargo mutants` invocation time propagates to the test.

use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::io::{BufReader, Cursor};
use std::path::{Path, PathBuf};

use noodles_vcf as vcf;

#[derive(Debug, Clone, PartialEq, Eq)]
struct FileOutcome {
    accepted: bool,
    record_count: usize,
    sample_count: usize,
    first_error: Option<String>,
}

impl FileOutcome {
    fn fingerprint(&self) -> String {
        format!(
            "accepted={}/records={}/samples={}/err={}",
            self.accepted,
            self.record_count,
            self.sample_count,
            self.first_error.as_deref().unwrap_or(""),
        )
    }
}

fn parse_one(path: &Path) -> FileOutcome {
    // Read into memory so the parser is driven over a Cursor<[u8]> —
    // removes any file-system-timing variance between reps.
    let bytes = match fs::read(path) {
        Ok(b) => b,
        Err(e) => {
            return FileOutcome {
                accepted: false,
                record_count: 0,
                sample_count: 0,
                first_error: Some(format!("read:{e}")),
            };
        }
    };

    let mut reader = match vcf::io::reader::Builder::default()
        .build_from_reader(BufReader::new(Cursor::new(bytes)))
    {
        Ok(r) => r,
        Err(e) => {
            return FileOutcome {
                accepted: false,
                record_count: 0,
                sample_count: 0,
                first_error: Some(shorten_err(e)),
            };
        }
    };

    let header = match reader.read_header() {
        Ok(h) => h,
        Err(e) => {
            return FileOutcome {
                accepted: false,
                record_count: 0,
                sample_count: 0,
                first_error: Some(shorten_err(e)),
            };
        }
    };
    let sample_count = header.sample_names().len();

    let mut record_count = 0usize;
    let mut record = vcf::Record::default();
    loop {
        match reader.read_record(&mut record) {
            Ok(0) => break,
            Ok(_) => record_count += 1,
            Err(e) => {
                return FileOutcome {
                    accepted: false,
                    record_count,
                    sample_count,
                    first_error: Some(shorten_err(e)),
                };
            }
        }
    }
    FileOutcome {
        accepted: true,
        record_count,
        sample_count,
        first_error: None,
    }
}

fn shorten_err<E: std::fmt::Display>(e: E) -> String {
    let s = e.to_string();
    if s.len() > 80 { s[..80].to_string() } else { s }
}

fn corpus_files(dir: &Path, sample: usize) -> Vec<PathBuf> {
    let mut v: Vec<PathBuf> = fs::read_dir(dir)
        .unwrap_or_else(|e| panic!("corpus dir {dir:?}: {e}"))
        .filter_map(|r| r.ok())
        .map(|e| e.path())
        .filter(|p| p.is_file())
        .collect();
    v.sort();
    v.truncate(sample);
    v
}

fn load_fingerprint(path: &Path) -> BTreeMap<String, String> {
    let raw = fs::read_to_string(path).expect("read baseline json");
    // Hand-parse: {"name": "fingerprint", ...} — avoid adding a
    // serde_json dep to the oracle crate-graph (noodles-vcf already
    // depends on serde_json transitively but we keep the oracle lean).
    // The file we write ourselves is a flat JSON object with string
    // keys and string values, one entry per line for legibility.
    let mut map = BTreeMap::new();
    for line in raw.lines() {
        let l = line.trim().trim_end_matches(',');
        if l.is_empty() || l == "{" || l == "}" { continue; }
        // Expect  "name": "fingerprint"
        let (k, v) = l.split_once("\":").expect("malformed baseline line");
        let key = k.trim().trim_start_matches('"').to_string();
        let val = v.trim().trim_start_matches('"').trim_end_matches('"').to_string();
        map.insert(key, val);
    }
    map
}

fn write_fingerprint(path: &Path, fp: &BTreeMap<String, String>) {
    use std::io::Write as IoWrite;
    let mut s = String::from("{\n");
    let last = fp.len().saturating_sub(1);
    for (i, (k, v)) in fp.iter().enumerate() {
        let comma = if i == last { "" } else { "," };
        s.push_str(&format!("  \"{k}\": \"{v}\"{comma}\n"));
    }
    s.push_str("}\n");
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).ok();
    }
    let mut f = fs::File::create(path).expect("create baseline");
    f.write_all(s.as_bytes()).expect("write baseline");
}

#[test]
fn corpus_oracle() {
    let corpus_dir = env::var("BIOTEST_CORPUS_DIR").unwrap_or_else(|_| {
        panic!("BIOTEST_CORPUS_DIR env var required (DESIGN §3.3 corpus location)")
    });
    let corpus_dir = PathBuf::from(corpus_dir);
    let sample: usize = env::var("BIOTEST_CORPUS_SAMPLE")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(200);

    let baseline_json = env::var("BIOTEST_BASELINE_JSON").unwrap_or_else(|_| {
        panic!("BIOTEST_BASELINE_JSON env var required")
    });
    let baseline_json = PathBuf::from(baseline_json);

    let mode = env::var("BIOTEST_BASELINE_MODE").unwrap_or_else(|_| "check".to_string());

    let files = corpus_files(&corpus_dir, sample);
    let mut fp = BTreeMap::new();
    for p in &files {
        let name = p.file_name().unwrap().to_string_lossy().into_owned();
        let outcome = parse_one(p);
        fp.insert(name, outcome.fingerprint());
    }

    match mode.as_str() {
        "capture" => {
            write_fingerprint(&baseline_json, &fp);
            eprintln!("[oracle] captured baseline ({} files) → {}",
                      fp.len(), baseline_json.display());
        }
        _ => {
            assert!(baseline_json.exists(),
                    "baseline file missing: {}", baseline_json.display());
            let baseline = load_fingerprint(&baseline_json);
            let mut diffs: Vec<String> = Vec::new();
            // Compare every file in current fp against baseline.
            for (k, v) in &fp {
                match baseline.get(k) {
                    Some(b) if b == v => {}
                    Some(b) => diffs.push(format!("{k}: {b} → {v}")),
                    None => diffs.push(format!("{k}: (missing in baseline) → {v}")),
                }
            }
            // Also flag entries in baseline that disappeared (unlikely
            // — same corpus files — but belt-and-braces).
            for k in baseline.keys() {
                if !fp.contains_key(k) {
                    diffs.push(format!("{k}: (disappeared from current)"));
                }
            }
            if !diffs.is_empty() {
                let preview: Vec<String> = diffs.iter().take(5).cloned().collect();
                panic!(
                    "oracle divergence on {} of {} files; first up-to-5:\n  {}",
                    diffs.len(),
                    fp.len(),
                    preview.join("\n  "),
                );
            }
            eprintln!("[oracle] {} files match baseline", fp.len());
        }
    }
}
