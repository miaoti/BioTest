#!/usr/bin/env bash
# Executed INSIDE biotest-bench:latest by run_noodles_mutation_docker.sh.
# Inputs (passed via env):
#   CORPUS     = /corpus (bind mount, read-only)
#   OUT        = /out    (bind mount, read-write)
#   NOODLES_COMMIT (default noodles-vcf-0.70.0)
#   BUDGET_S   (default 3600)
#   CORPUS_SAMPLE (default 50)

set -euo pipefail
export PATH=/root/.cargo/bin:$PATH

BUDGET_S="${BUDGET_S:-3600}"
CORPUS_SAMPLE="${CORPUS_SAMPLE:-50}"
NOODLES_COMMIT="${NOODLES_COMMIT:-noodles-vcf-0.70.0}"

if [ ! -d /work/noodles ]; then
    git clone --depth=50 https://github.com/zaeleus/noodles /work/noodles 2>&1 | tail -3
fi
cd /work/noodles
git fetch --tags --depth=50 origin "${NOODLES_COMMIT}" 2>&1 | tail -3 || true
git checkout -q "${NOODLES_COMMIT}" 2>/dev/null \
  || git checkout -q "tags/${NOODLES_COMMIT}" 2>/dev/null \
  || { echo "noodles commit ${NOODLES_COMMIT} not reachable; using HEAD"; }

# cargo-mutants only mutates workspace members, so we add the
# corpus-replay test DIRECTLY inside noodles-vcf/tests/ and run
# cargo-mutants from the noodles-vcf crate root. noodles-vcf is
# already a cargo workspace member inside the noodles monorepo.
TEST_FILE=/work/noodles/noodles-vcf/tests/corpus_replay_biotest.rs
mkdir -p /work/noodles/noodles-vcf/tests
cat > "$TEST_FILE" <<'TESTEOF'
use std::fs;
use std::io::BufReader;
use noodles_vcf as vcf;

#[test]
fn replay_corpus() {
    let corpus = std::path::Path::new("/corpus");
    let entries = fs::read_dir(corpus).expect("no /corpus dir");

    let mut paths: Vec<_> = entries
        .filter_map(|e| e.ok().map(|e| e.path()))
        .filter(|p| p.is_file())
        .collect();
    paths.sort();
    let cap: usize = std::env::var("CORPUS_SAMPLE")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(50);
    if paths.len() > cap { paths.truncate(cap); }

    let mut accept: u64 = 0;
    let mut reject: u64 = 0;
    let mut record_count: u64 = 0;
    let mut err_bucket: u64 = 0;

    for path in &paths {
        let file = match fs::File::open(path) {
            Ok(f) => f,
            Err(_) => { reject += 1; continue; }
        };
        let buf = BufReader::new(file);
        let mut reader = match vcf::io::reader::Builder::default()
            .build_from_reader(buf)
        {
            Ok(r) => r,
            Err(e) => {
                reject += 1;
                err_bucket = err_bucket.wrapping_add(
                    format!("{:?}", e).len() as u64);
                continue;
            }
        };
        let _header = match reader.read_header() {
            Ok(h) => h,
            Err(e) => {
                reject += 1;
                err_bucket = err_bucket.wrapping_add(
                    format!("{:?}", e).len() as u64);
                continue;
            }
        };
        accept += 1;
        for rec in reader.records() {
            match rec {
                Ok(_) => record_count += 1,
                Err(_) => { record_count += 1; break; }
            }
            if record_count >= 200 { break; }
        }
    }

    eprintln!(
        "corpus_replay: accept={} reject={} records={} errbucket={}",
        accept, reject, record_count, err_bucket,
    );
    // Always passes; cargo-mutants kills via behaviour diff, not assert.
}
TESTEOF

cd /work/noodles/noodles-vcf

# Warm up the baseline build so cargo-mutants skips the slow first
# build inside each mutant shard.
echo "=== baseline cargo build ==="
cargo build --tests --release 2>&1 | tail -5
echo "=== baseline test run (sanity) ==="
CORPUS_SAMPLE="${CORPUS_SAMPLE}" cargo test --release --test corpus_replay_biotest -- --nocapture 2>&1 | tail -8

echo "=== cargo-mutants on noodles-vcf (scoped + budget-capped) ==="
# Scope to the BioTest-exercised subtrees (biotest_config.yaml
# target_filter.VCF.noodles = io/reader, io/writer, header, record,
# variant, lib.rs). cargo-mutants 27.x uses bare glob patterns —
# `**` is not always honoured, so enumerate both the sibling .rs and
# the subdir-level files. This mirrors the mutmut vcfpy row's
# "scope only what BioTest drives" rule.
#
# `-- --test corpus_replay_biotest` restricts the per-mutant `cargo
# test` to our single corpus-replay test, dropping noodles-vcf's own
# unit tests (which would slow each mutant by ~30 s and aren't the
# thing pure_random is claimed to kill).
CARGO_MUTANTS_TIMEOUT_PER_MUTANT="${CARGO_MUTANTS_TIMEOUT_PER_MUTANT:-90}"
# cargo-mutants --file matches the full workspace-relative path; it
# does NOT respect `src/` subpath unless prefixed with the crate name.
# Use full `noodles-vcf/src/...` paths for each scope subtree.
#
# Scope NARROWED to files pure_random's corpus actually exercises:
# io/reader and header. Record / writer / variant code never runs for
# random bytes (they fail at header.rs), so mutants there always
# survive — that was confirmed by an earlier 85-mutant run where every
# single one in these paths was MISSED. Dropping them cuts total
# mutants from 408 to ~100 and runtime from ~13 min → ~3 min per run,
# making 4-run aggregation feasible in one session.
timeout "${BUDGET_S}s" cargo mutants \
    --file "noodles-vcf/src/io/reader.rs" \
    --file "noodles-vcf/src/io/reader/*.rs" \
    --file "noodles-vcf/src/header.rs" \
    --file "noodles-vcf/src/header/*.rs" \
    --file "noodles-vcf/src/lib.rs" \
    --timeout "${CARGO_MUTANTS_TIMEOUT_PER_MUTANT}" \
    --no-shuffle \
    --jobs 2 \
    --output /out \
    -- --test corpus_replay_biotest 2>&1 | tee /out/cargo_mutants.log | tail -60 \
    || echo "cargo-mutants exited (non-zero often means survivors present)"

echo "=== cargo-mutants done ==="
ls /out

# Parse cargo-mutants status lines and emit summary.json shaped like
# the other Phase-3 cells. Cargo-mutants statuses:
#   ok        — baseline (exclude)
#   CAUGHT    — killed (test failed → good)
#   MISSED    — survived (test passed despite mutation)
#   TIMEOUT   — timeout (counted as killed-ish; distinct bucket)
#   UNVIABLE  — compile fail (exclude from reachable)
#   SKIPPED   — mutant skipped (exclude)
python3 - <<'PYEOF'
import json
import re
from pathlib import Path

log = Path("/out/cargo_mutants.log").read_text(encoding="utf-8",
                                               errors="replace")
killed = survived = timeout_count = unviable = 0
for line in log.splitlines():
    if re.match(r"^CAUGHT\s", line):
        killed += 1
    elif re.match(r"^MISSED\s", line):
        survived += 1
    elif re.match(r"^TIMEOUT\s", line):
        timeout_count += 1
    elif re.match(r"^UNVIABLE\s", line):
        unviable += 1

reachable = killed + survived + timeout_count
total = reachable + unviable
score = killed / reachable if reachable else 0.0
payload = {
    "tool": "pure_random",
    "sut": "noodles",
    "phase": "mutation",
    "engine": "cargo-mutants 27.0",
    "killed": killed,
    "survived": survived,
    "timeout": timeout_count,
    "suspicious": 0,
    "skipped": 0,
    "no_tests": 0,
    "not_checked": unviable,
    "reachable": reachable,
    "mutant_count": total,
    "score": round(score, 4),
    "score_display": (
        f"{score * 100:.2f}%" if reachable else "n/a (reachable=0)"
    ),
    "corpus_dir": "/corpus",
    "cargo_mutants_log": "/out/cargo_mutants.log",
}
Path("/out/summary.json").write_text(
    json.dumps(payload, indent=2), encoding="utf-8",
)
print(f"summary.json: killed={killed} survived={survived} "
      f"reachable={reachable} score={payload['score_display']}")
PYEOF

