"""Verify vcfpy VCF filter scopes exactly to the runner's read path."""
import os
from pathlib import Path

import yaml

with open("biotest_config.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

from test_engine.feedback.coverage_collector import MultiCoverageCollector

mc = MultiCoverageCollector(cfg["coverage"])

import coverage
cov = coverage.Coverage(source_pkgs=["vcfpy"], concurrency=["thread"])
cov.start()
from test_engine.runners.vcfpy_runner import VcfpyRunner
res = VcfpyRunner().run(Path("seeds/vcf/htsjdk_ex2.vcf"), "VCF", timeout_s=20)
cov.stop(); cov.save()

filt = mc._resolve_sut_filter("VCF", "vcfpy")
print(f"vcfpy VCF filter: {filt}\n")

total_before = (0, 0)
total_after = (0, 0)
print("Per-file:")
for f in sorted(cov.get_data().measured_files()):
    if "vcfpy" not in f:
        continue
    normp = f.replace("\\", "/")
    matches = any(x.replace("\\", "/").replace(".", "/") in normp for x in filt)
    _, stmts, _exc, missing, *_ = cov.analysis2(f)
    executed = len(stmts) - len(missing)
    stem = os.path.basename(f)
    mark = "KEEP" if matches else "DROP"
    print(f"  [{mark}]  {stem:20s} tracked={len(stmts):5d} executed={executed:5d}")
    total_before = (total_before[0] + executed, total_before[1] + len(stmts))
    if matches:
        total_after = (total_after[0] + executed, total_after[1] + len(stmts))

print()
bc, bt = total_before
ac, at = total_after
print(f"BEFORE filter: {bc}/{bt}  =  {100*bc/bt:.1f}%")
print(f"AFTER  filter: {ac}/{at}  =  {100*ac/at:.1f}%")
