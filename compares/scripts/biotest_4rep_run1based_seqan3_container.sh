#!/usr/bin/env bash
# Run1-based seqan3/SAM sweep inside biotest-bench:
#   rep 0  -- full A,D,E with USE_SEQAN3 harness (canonical run)
#   reps 1..3 -- restore rep 0's mr_registry, run --phase C only, vary RNG.
set -euo pipefail

WORK=/work
OUT_ROOT="${WORK}/compares/results/coverage/biotest_4rep_run1based_20260426/seqan3_sam_container"
mkdir -p "${OUT_ROOT}"
LOG="${OUT_ROOT}/run.log"
: > "${LOG}"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S)] $*" | tee -a "${LOG}"; }

log "===== biotest-bench seqan3/SAM run1-based 4-rep sweep ====="

if ! python3.12 -c "import yaml, rich, hypothesis, chromadb, gcovr" >/dev/null 2>&1; then
  python3.12 -m pip install --quiet --no-warn-script-location -r "${WORK}/requirements.txt" gcovr lxml >>"${LOG}" 2>&1
fi
python3.12 -c "import yaml, rich, hypothesis, chromadb; import gcovr; print('deps OK')" | tee -a "${LOG}"

# Build seqan3-instrumented harness once.
HARNESS_SRC="${WORK}/harnesses/cpp/biotest_harness.cpp"
HARNESS_BIN="${WORK}/harnesses/cpp/build/biotest_harness_cov_seqan3"
log "Step 2: clang++-18 -fprofile-arcs -ftest-coverage -DUSE_SEQAN3 build"
if [[ ! -x "${HARNESS_BIN}" ]] || [[ "${HARNESS_SRC}" -nt "${HARNESS_BIN}" ]]; then
  rm -f "${WORK}/harnesses/cpp/build/"*.gcda "${WORK}/harnesses/cpp/build/"*.gcno
  clang++-18 -std=c++23 -O0 -g \
    -DNDEBUG -DUSE_SEQAN3 -DSEQAN3_DISABLE_COMPILER_CHECK \
    -isystem /opt/seqan3/include \
    -fprofile-arcs -ftest-coverage \
    "${HARNESS_SRC}" \
    -o "${HARNESS_BIN}" >>"${LOG}" 2>&1 \
    || { log "build failed"; exit 1; }
fi
ls -la "${HARNESS_BIN}" | tee -a "${LOG}"

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
    log "### seqan3/SAM -- rep ${rep} (Run 1 / canonical) --"
  else
    log "### seqan3/SAM -- rep ${rep} (continuation from Run 1) --"
  fi
  PHASES="A,D,E"
  ENABLE_FB=true
  BUDGET=3600

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
  rm -f "${WORK}/coverage_artifacts/gcovr.json"
  rm -f "${WORK}/harnesses/cpp/build/"*.gcda

  REP_DIR="${OUT_ROOT}/run_${rep}"
  mkdir -p "${REP_DIR}"
  CFG="${REP_DIR}/biotest_config.rep${rep}.yaml"
  python3.12 - <<PY "${WORK}" "${CFG}" "${SEEDS_SMALL}" "${rep}" "${HARNESS_BIN}" "${ENABLE_FB}"
import yaml, sys, pathlib
repo, cfg_path, seeds, rep, hbin, enable = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6] == "true"
cfg = yaml.safe_load(pathlib.Path(repo, "biotest_config.yaml").read_text("utf-8"))
cfg.setdefault("phase_c", {})["format_filter"] = "SAM"
cfg["phase_c"]["seeds_dir"] = seeds
cfg["phase_c"]["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}
for sut in cfg["phase_c"]["suts"]:
    if sut.get("name") == "seqan3":
        sut["adapter"] = hbin
        sut["coverage_binary"] = hbin
fb = cfg.setdefault("feedback_control", {})
fb["enabled"] = enable
fb["primary_target"] = "seqan3"
if enable:
    fb["max_iterations"] = 2
    fb["plateau_patience"] = 4
    fb["coverage_plateau_patience"] = 4
    fb.setdefault("seed_synthesis", {})["enabled"] = False
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
  cd "${WORK}"
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

  python3.12 -m gcovr --json -o "${WORK}/coverage_artifacts/gcovr.json" \
    --root /opt/seqan3/include \
    --filter '.*seqan3.*' \
    --gcov-executable 'llvm-cov-18 gcov' \
    "${WORK}/harnesses/cpp/build" >>"${LOG}" 2>&1 || true

  MEASURE_OUT="${REP_DIR}/measurement.json"
  if [[ -f "${WORK}/coverage_artifacts/gcovr.json" ]]; then
    python3.12 - <<PY "${WORK}" "${rep}" "${elapsed}" "${MEASURE_OUT}" "${PHASES}"
import json, pathlib, subprocess, sys
repo, rep, elapsed, out, phases = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
proc = subprocess.run([
    "python3.12", f"{repo}/compares/scripts/measure_coverage.py",
    "--report", f"{repo}/coverage_artifacts/gcovr.json",
    "--sut", "seqan3", "--format", "SAM",
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
  "cell": "seqan3_sam", "sut": "seqan3", "format": "SAM",
  "rep": rep, "elapsed_s": elapsed, "line_pct": line_pct,
  "covered": covered, "total": total, "phases": phases,
  "max_iterations": 2,
  "rep_kind": "run1_canonical" if rep == 0 else "replica_from_run1",
  "status": "ok" if total else "missing",
  "source": "coverage_artifacts/gcovr.json",
}
pathlib.Path(out).write_text(json.dumps(payload, indent=2), "utf-8")
print(json.dumps(payload, indent=2))
PY
  else
    echo "{\"cell\":\"seqan3_sam\",\"sut\":\"seqan3\",\"format\":\"SAM\",\"rep\":${rep},\"elapsed_s\":${elapsed},\"line_pct\":0.0,\"covered\":0,\"total\":0,\"phases\":\"${PHASES}\",\"rep_kind\":\"$([ ${rep} -eq 0 ] && echo run1_canonical || echo replica_from_run1)\",\"status\":\"missing\"}" > "${MEASURE_OUT}"
  fi

  line=$(python3.12 -c "import json; d=json.load(open('${MEASURE_OUT}')); print(f\"line={d['line_pct']:.2f}%% covered={d['covered']}/{d['total']} status={d['status']}\")")
  log "  -> ${line}"
done

log ""
log "===== seqan3/SAM run1-based sweep complete ====="
