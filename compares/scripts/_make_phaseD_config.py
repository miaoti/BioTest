"""Write a Phase-D + seed_synthesis config to a target path. Runs inside Docker."""
import sys
import yaml
from pathlib import Path

if len(sys.argv) < 3:
    print("usage: _make_phaseD_config.py <bug_id> <target_cfg_path>")
    sys.exit(2)

bug_id = sys.argv[1]
target = Path(sys.argv[2])

cfg = yaml.safe_load(open("/work/biotest_config.yaml", encoding="utf-8").read())
cell_dir = f"/work/compares/results/bug_bench/biotest_phaseD_synth_2026_04_29/biotest/{bug_id}"

cfg.setdefault("feedback_control", {})
cfg["feedback_control"].setdefault("seed_synthesis", {})
cfg["feedback_control"]["seed_synthesis"]["enabled"] = True
cfg["feedback_control"]["seed_synthesis"]["max_seeds_per_iteration"] = 8
cfg["feedback_control"]["max_iterations"] = 4

cfg["phase_c"]["format_filter"] = "VCF"
cfg["phase_c"]["output_dir"] = f"{cell_dir}/bug_reports"
cfg["phase_c"]["det_report_path"] = f"{cell_dir}/det_report.json"
cfg["phase_c"]["seeds_dir"] = f"{cell_dir}/seeds_in"

target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
print(f"wrote {target}")
