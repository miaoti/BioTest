#!/usr/bin/env bash
# Run1-based noodles/VCF sweep inside biotest-bench:
#   rep 0  -- full A,D,E (canonical run; produces mr_registry + Phase E corpus)
#   reps 1..3 -- restore rep 0's mr_registry, run --phase C only, vary RNG.
# Std across reps reflects Phase C / Hypothesis nondeterminism only.
set -euo pipefail

export PATH=/root/.cargo/bin:$PATH
WORK=/work
OUT_ROOT="${WORK}/compares/results/coverage/biotest_4rep_run1based_20260426/noodles_vcf_container"
mkdir -p "${OUT_ROOT}"
LOG="${OUT_ROOT}/run.log"
: > "${LOG}"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S)] $*" | tee -a "${LOG}"; }

log "===== biotest-bench noodles/VCF run1-based 4-rep sweep ====="

if ! python3.12 -c "import yaml, rich, hypothesis, chromadb" >/dev/null 2>&1; then
  python3.12 -m pip install --quiet --no-warn-script-location -r "${WORK}/requirements.txt" >>"${LOG}" 2>&1
fi
python3.12 -c "import yaml, rich, hypothesis, chromadb; print('deps OK')" | tee -a "${LOG}"

# Build cov-instrumented noodles harness once.
cd "${WORK}/harnesses/rust/noodles_harness"
log "Step 2: RUSTFLAGS=-Cinstrument-coverage cargo build --release"
RUSTFLAGS='-C instrument-coverage' cargo build --release --locked \
    --manifest-path "${WORK}/harnesses/rust/noodles_harness/Cargo.toml" \
    >>"${LOG}" 2>&1 \
    || { log "build failed"; exit 1; }
mkdir -p target/llvm-cov-target/release
ln -sfn "${WORK}/harnesses/rust/noodles_harness/target/release/noodles_harness" \
        target/llvm-cov-target/release/noodles_harness
cd "${WORK}"

# 5-seed corpus, no kept_*/synthetic_*.
SEEDS_SMALL="${OUT_ROOT}/seeds_small"
mkdir -p "${SEEDS_SMALL}/vcf" "${SEEDS_SMALL}/sam"
python3.12 - <<'PY' "${WORK}" "${SEEDS_SMALL}" 5
import os, pathlib, shutil, sys
repo, out_root, n = sys.argv[1], pathlib.Path(sys.argv[2]), int(sys.argv[3])
for fmt in ("vcf", "sam"):
    src = pathlib.Path(repo) / "seeds" / fmt
    dst = out_root / fmt
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(src.glob(f"*.{fmt}"))
    eligible = [p for p in files
                if not p.name.startswith("kept_")
                and not p.name.startswith("synthetic_")]
    for s in eligible[:n]:
        link = dst / s.name
        if link.exists(): continue
        try: os.symlink(s.resolve(), link)
        except OSError: shutil.copy2(s, link)
ref = pathlib.Path(repo) / "seeds" / "ref"
if ref.exists() and not (out_root / "ref").exists():
    shutil.copytree(ref, out_root / "ref")
print(f"seeds staged at {out_root}")
PY

STATE_FILES=(
  "${WORK}/data/mr_registry.json"
  "${WORK}/data/feedback_state.json"
  "${WORK}/data/rule_attempts.json"
  "${WORK}/data/coverage_report.json"
  "${WORK}/data/det_report.json"
  "${WORK}/data/scc_report.json"
)
STATE_DIR="${OUT_ROOT}/run1_state"

for rep in 0 1 2 3; do
  log ""
  if [ "${rep}" = "0" ]; then
    log "### noodles/VCF -- rep ${rep} (Run 1 / canonical) --"
  else
    log "### noodles/VCF -- rep ${rep} (continuation from Run 1) --"
  fi
  # All reps full pipeline. Reps 1..3 differ only in starting state
  # (restored from run1_state) so Phase B re-mining sees Run 1's MRs.
  PHASES="A,D,E"
  ENABLE_FB=true
  BUDGET=5400

  if [ "${rep}" = "0" ]; then
    for f in "${STATE_FILES[@]}"; do [[ -f "${f}" ]] && rm -f "${f}"; done
  else
    mkdir -p "${WORK}/data"
    for f in "${STATE_FILES[@]}"; do
      name=$(basename "${f}")
      if [ -f "${STATE_DIR}/${name}" ]; then
        cp "${STATE_DIR}/${name}" "${f}"
      fi
    done
  fi
  rm -f "${WORK}/coverage_artifacts/noodles/llvm-cov.json"
  rm -f "${WORK}"/coverage_artifacts/noodles/*.profraw 2>/dev/null || true

  REP_DIR="${OUT_ROOT}/run_${rep}"
  mkdir -p "${REP_DIR}"
  CFG="${REP_DIR}/biotest_config.rep${rep}.yaml"
  python3.12 - <<PY "${WORK}" "${CFG}" "${SEEDS_SMALL}" "${rep}" "${ENABLE_FB}"
import yaml, sys, pathlib
repo, cfg_path, seeds, rep, enable = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5] == "true"
cfg = yaml.safe_load(pathlib.Path(repo, "biotest_config.yaml").read_text("utf-8"))
cfg.setdefault("phase_c", {})["format_filter"] = "VCF"
cfg["phase_c"]["seeds_dir"] = seeds
cfg["phase_c"]["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}
fb = cfg.setdefault("feedback_control", {})
fb["enabled"] = enable
fb["primary_target"] = "noodles"
if enable:
    fb["max_iterations"] = 2
    fb["plateau_patience"] = 4
    fb["coverage_plateau_patience"] = 4
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
  log "  cmd: python3.12 biotest.py --config ${CFG} --phase ${PHASES}"
  t0=$(date +%s)
  timeout --kill-after=60 ${BUDGET} python3.12 "${WORK}/biotest.py" \
    --config "${CFG}" --phase ${PHASES} --verbose \
    > "${BIOTEST_LOG}" 2>&1 || true
  t1=$(date +%s)
  elapsed=$((t1 - t0))
  log "  elapsed=${elapsed}s"

  if [ "${rep}" = "0" ]; then
    mkdir -p "${STATE_DIR}"
    for f in "${STATE_FILES[@]}"; do
      [[ -f "${f}" ]] && cp "${f}" "${STATE_DIR}/"
    done
    log "  froze Run 1 state to ${STATE_DIR}"
  fi

  MEASURE_OUT="${REP_DIR}/measurement.json"
  if [[ -f "${WORK}/coverage_artifacts/noodles/llvm-cov.json" ]]; then
    python3.12 - <<PY "${WORK}" "${rep}" "${elapsed}" "${MEASURE_OUT}" "${PHASES}"
import json, pathlib, subprocess, sys
repo, rep, elapsed, out, phases = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
proc = subprocess.run([
    "python3.12", f"{repo}/compares/scripts/measure_coverage.py",
    "--report", f"{repo}/coverage_artifacts/noodles/llvm-cov.json",
    "--sut", "noodles", "--format", "VCF",
], capture_output=True, text=True, cwd=repo)
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
  "covered": covered, "total": total, "phases": phases,
  "max_iterations": 2,
  "rep_kind": "run1_canonical" if rep == 0 else "replica_from_run1",
  "status": "ok" if total else "missing",
  "source": "coverage_artifacts/noodles/llvm-cov.json",
}
pathlib.Path(out).write_text(json.dumps(payload, indent=2), "utf-8")
print(json.dumps(payload, indent=2))
PY
  else
    echo "{\"cell\":\"noodles_vcf\",\"sut\":\"noodles\",\"format\":\"VCF\",\"rep\":${rep},\"elapsed_s\":${elapsed},\"line_pct\":0.0,\"covered\":0,\"total\":0,\"phases\":\"${PHASES}\",\"rep_kind\":\"$([ ${rep} -eq 0 ] && echo run1_canonical || echo replica_from_run1)\",\"status\":\"missing\"}" > "${MEASURE_OUT}"
  fi

  line=$(python3.12 -c "import json; d=json.load(open('${MEASURE_OUT}')); print(f\"line={d['line_pct']:.2f}%% covered={d['covered']}/{d['total']} status={d['status']}\")")
  log "  -> ${line}"
done

log ""
log "===== noodles/VCF run1-based sweep complete ====="
