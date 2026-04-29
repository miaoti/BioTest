#!/usr/bin/env python3
"""One-shot re-measure of a cargo-llvm-cov JSON under the broader
``noodles-vcf`` substring scope that the Phase-2 cargo-fuzz sampler
(compares/scripts/coverage_sampler.py::_summarise_noodles_report) uses.

Gives an apples-to-apples number against cargo-fuzz's 22.72% baseline
— that baseline was computed with this broader filter, not the
6-subpath filter in biotest_config.yaml:coverage.target_filters.VCF.noodles.
"""
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "coverage_artifacts/noodles/llvm-cov.json"
data = json.load(open(path))
cov = total = 0
files_counted = 0
for run in data.get("data", []):
    for f in run.get("files", []):
        fn = f.get("filename", "").replace("\\", "/")
        if "noodles-vcf" not in fn:
            continue
        files_counted += 1
        s = f.get("summary", {}).get("lines", {})
        cov += int(s.get("covered", 0))
        total += int(s.get("count", 0))
pct = 100.0 * cov / total if total else 0.0
print(f"{path}")
print(f"  scope: any file whose path contains 'noodles-vcf' "
      f"(Phase-2 cargo-fuzz sampler scope)")
print(f"  {files_counted} files, {cov}/{total} lines ({pct:.2f}%)")
