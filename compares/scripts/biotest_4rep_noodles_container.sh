#!/usr/bin/env bash
# Container-side 4-rep full-pipeline sweep for the noodles/VCF cell.
#
# Runs inside biotest-bench (Linux, cargo 1.95 + cargo-llvm-cov 0.8.5 +
# OpenJDK 17 + Python 3.10). The host sweep can only measure SUTs whose
# coverage backends exist on Windows/MinGW; noodles needs cargo-llvm-cov
# which only lives in the bench image. This script runs after the host
# sweep finishes, installs Python deps, builds an instrumented noodles
# harness once, then re-runs biotest.py --phase A,B,C,D four times with
# fresh state per rep.
#
# Usage (from host):
#   docker exec biotest-bench-setup bash /work/compares/scripts/biotest_4rep_noodles_container.sh
set -euo pipefail

export PATH=/root/.cargo/bin:$PATH
WORK=/work
# OUT_ROOT can be overridden via env for the fresh-sweep / run1-based
# variants; defaults to the original 2026-04-23 dir for backward compat.
OUT_ROOT="${OUT_ROOT:-${WORK}/compares/results/coverage/biotest_4rep_fullD_20260423/noodles_vcf_container}"
mkdir -p "${OUT_ROOT}"
LOG="${OUT_ROOT}/run.log"
: > "${LOG}"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S)] $*" | tee -a "${LOG}"; }

log "===== biotest-bench noodles/VCF 4-rep sweep (full Phase A,B,C,D) ====="

# Step 1 — Python deps (idempotent)
log "Step 1: pip install -r requirements.txt"
if ! python3.12 -c "import yaml, rich, hypothesis, chromadb" >/dev/null 2>&1; then
  python3.12 -m pip install --quiet --no-warn-script-location -r "${WORK}/requirements.txt" >>"${LOG}" 2>&1 \
    || { log "pip install failed"; exit 1; }
fi
python3.12 -c "import yaml, rich, hypothesis, chromadb; print('deps OK')" | tee -a "${LOG}"

# Step 2 — build cov-instrumented noodles harness ONCE.
# We use raw `RUSTFLAGS=-C instrument-coverage cargo build` (not
# `cargo llvm-cov --no-report run`) because cargo-llvm-cov 0.8.5's
# build path produces an instrumented binary whose rlib metadata for
# external crates llvm-cov export cannot enumerate (only main.rs ends
# up in the report). The raw RUSTFLAGS path produces an instrumented
# binary that llvm-cov export sees with all 168 noodles-vcf files.
log "Step 2: RUSTFLAGS=-Cinstrument-coverage cargo build --release"
cd "${WORK}/harnesses/rust/noodles_harness"
RUSTFLAGS='-C instrument-coverage' cargo build --release --locked \
    --manifest-path "${WORK}/harnesses/rust/noodles_harness/Cargo.toml" \
    >>"${LOG}" 2>&1 \
    || { log "cargo build with instrument-coverage failed"; exit 1; }
# Mirror the binary to llvm-cov-target/release/ where biotest_config.yaml
# expects it. Symlink not copy so disk stays light.
mkdir -p target/llvm-cov-target/release
ln -sfn "${WORK}/harnesses/rust/noodles_harness/target/release/noodles_harness" \
        target/llvm-cov-target/release/noodles_harness
ls -la target/release/noodles_harness target/llvm-cov-target/release/noodles_harness | tee -a "${LOG}"
cd "${WORK}"

# Step 3 — 4 reps of biotest --phase A,B,C,D with primary=noodles
STATE_FILES=(
  "${WORK}/data/mr_registry.json"
  "${WORK}/data/feedback_state.json"
  "${WORK}/data/rule_attempts.json"
  "${WORK}/data/coverage_report.json"
  "${WORK}/data/det_report.json"
  "${WORK}/data/scc_report.json"
)

SEEDS_SMALL="${OUT_ROOT}/seeds_small"
mkdir -p "${SEEDS_SMALL}/vcf" "${SEEDS_SMALL}/sam"
# Use ALL non-BioTest-generated seeds (33 VCF, 67 SAM) — required for
# DESIGN §3 compute parity with Jazzer × htsjdk (each rep gets ~7200 s
# wall budget; biotest needs a correspondingly rich corpus to use it).
python3.12 - <<'PY' "${WORK}" "${SEEDS_SMALL}"
import os, pathlib, shutil, sys
repo, out_root = sys.argv[1], pathlib.Path(sys.argv[2])
for fmt in ("vcf", "sam"):
    src = pathlib.Path(repo) / "seeds" / fmt
    dst = out_root / fmt
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(src.glob(f"*.{fmt}"))
    eligible = [p for p in files
                if not p.name.startswith("kept_")
                and not p.name.startswith("synthetic_")]
    for s in eligible:
        link = dst / s.name
        if link.exists(): continue
        try: os.symlink(s.resolve(), link)
        except OSError: shutil.copy2(s, link)
    print(f"  {fmt}: staged {len(eligible)} seeds at {dst}")
ref = pathlib.Path(repo) / "seeds" / "ref"
if ref.exists() and not (out_root / "ref").exists():
    shutil.copytree(ref, out_root / "ref")
PY

for rep in 0 1 2 3; do
  log ""
  log "### noodles/VCF -- rep ${rep} --"
  # Reset state files so Phase B/D start fresh each rep.
  for f in "${STATE_FILES[@]}"; do [[ -f "${f}" ]] && rm -f "${f}"; done
  # Reset noodles cov artefacts.
  rm -f "${WORK}/coverage_artifacts/noodles/llvm-cov.json"
  rm -f "${WORK}"/coverage_artifacts/noodles/*.profraw 2>/dev/null || true

  # Per-rep config.
  REP_DIR="${OUT_ROOT}/run_${rep}"
  mkdir -p "${REP_DIR}"
  CFG="${REP_DIR}/biotest_config.rep${rep}.yaml"
  python3.12 - <<PY "${WORK}" "${CFG}" "${SEEDS_SMALL}" "${rep}"
import yaml, sys, pathlib
repo, cfg_path, seeds, rep = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
cfg = yaml.safe_load(pathlib.Path(repo, "biotest_config.yaml").read_text("utf-8"))
cfg.setdefault("phase_c", {})["format_filter"] = "VCF"
cfg["phase_c"]["seeds_dir"] = seeds
cfg["phase_c"]["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}
fb = cfg.setdefault("feedback_control", {})
fb["enabled"] = True
fb["primary_target"] = "noodles"
fb["max_iterations"] = 4
fb["plateau_patience"] = 5
fb["coverage_plateau_patience"] = 5
fb["timeout_minutes"] = 110
cfg["phase_e"] = {
    "enabled": True,
    "structural_max_per_seed": 10,
    "rawfuzz_n_per_seed": 2,
    "rawfuzz_seed": 42 + rep,
}
cfg.setdefault("global", {})["seed_rng"] = 42 + rep
pathlib.Path(cfg_path).write_text(yaml.safe_dump(cfg, sort_keys=False), "utf-8")
print(f"wrote {cfg_path}")
PY

  BIOTEST_LOG="${REP_DIR}/biotest.log"
  log "  cmd: python3.12 biotest.py --config ${CFG} --phase A,B,C,D"
  t0=$(date +%s)
  # --phase A,D,E: D wraps Phase B+C per iteration with coverage; E is
  # corpus augmentation (Rank 12 structural + Rank 13 rawfuzz) added
  # to the canonical pipeline 2026-04-25. Phase E runs after coverage
  # is already collected so it doesn't change the reported number,
  # but it IS the canonical pipeline so we run it for completeness.
  # DESIGN §3 compute parity: 7200 s per rep (matches Jazzer × htsjdk).
  timeout --kill-after=60 7200 python3.12 "${WORK}/biotest.py" \
    --config "${CFG}" --phase A,D,E --verbose \
    > "${BIOTEST_LOG}" 2>&1 || true
  t1=$(date +%s)
  elapsed=$((t1 - t0))
  log "  elapsed=${elapsed}s"

  # Measure noodles coverage via measure_coverage.py.
  MEASURE_OUT="${REP_DIR}/measurement.json"
  if [[ -f "${WORK}/coverage_artifacts/noodles/llvm-cov.json" ]]; then
    # Parse the fairness-filter output into a compact JSON.
    python3.12 - <<PY "${WORK}" "${rep}" "${elapsed}" "${MEASURE_OUT}"
import json, pathlib, subprocess, sys
repo, rep, elapsed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
proc = subprocess.run([
    "python3.12", f"{repo}/compares/scripts/measure_coverage.py",
    "--report", f"{repo}/coverage_artifacts/noodles/llvm-cov.json",
    "--sut", "noodles", "--format", "VCF",
], capture_output=True, text=True)
stdout = proc.stdout
line_pct = covered = total = 0.0
for ln in stdout.splitlines():
    if "OVERALL" in ln and "weighted" in ln:
        tail = ln.split(")", 1)[1].strip()
        frac, pct = tail.split("(")
        c, t = frac.strip().split("/")
        pct = pct.replace("%", "").replace(")", "").strip()
        line_pct, covered, total = float(pct), int(c), int(t)
        break
payload = {
  "cell": "noodles_vcf", "sut": "noodles", "format": "VCF",
  "rep": rep, "elapsed_s": elapsed, "line_pct": line_pct,
  "covered": covered, "total": total, "phases": "A,B,C,D",
  "max_iterations": 4, "status": "ok" if total else "missing",
  "source": "coverage_artifacts/noodles/llvm-cov.json",
}
pathlib.Path(out).write_text(json.dumps(payload, indent=2), "utf-8")
print(json.dumps(payload, indent=2))
PY
  else
    echo "{\"cell\":\"noodles_vcf\",\"sut\":\"noodles\",\"format\":\"VCF\",\"rep\":${rep},\"elapsed_s\":${elapsed},\"line_pct\":0.0,\"covered\":0,\"total\":0,\"status\":\"missing\"}" > "${MEASURE_OUT}"
  fi

  line=$(python3.12 -c "import json; d=json.load(open('${MEASURE_OUT}')); print(f\"line={d['line_pct']:.2f}%% covered={d['covered']}/{d['total']} status={d['status']}\")")
  log "  -> ${line}"
done

log ""
log "===== noodles/VCF container sweep complete ====="
