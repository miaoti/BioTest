"""Verify noodles coverage filter on representative llvm-cov path shapes."""
from pathlib import Path
import yaml

with open("biotest_config.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

from test_engine.feedback.coverage_collector import MultiCoverageCollector

mc = MultiCoverageCollector(cfg["coverage"])
sut_filter = mc._resolve_sut_filter("VCF", "noodles")
crate_anchor = cfg["coverage"].get("noodles_crate_anchor", "noodles-vcf")
print(f"crate_anchor: {crate_anchor!r}")
print(f"sub-paths   : {sut_filter}\n")

# Representative llvm-cov filename shapes, covering:
#   - crates.io pulls (version-suffixed path)
#   - git dep (bare crate name + commit dir)
#   - path dep (submodule / local tree)
#   - other crates pulled as transitive deps
PATHS = [
    # KEEP: reader/model in noodles-vcf under various Cargo resolution flavors
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\lib.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\header.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\header\line.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\record\ids.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\variant\record_buf.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\io\reader.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\io\reader\header.rs",
    r"C:\Users\miaot\.cargo\git\checkouts\noodles-xyz\abc123\noodles-vcf\src\io\reader\record.rs",
    r"SUTfolder/rust/noodles-vcf/src/io/reader.rs",   # path dep

    # DROP: excluded sub-paths in noodles-vcf (writer/indexed/async/fs/compression)
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\io\writer.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\io\writer\record.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\io\indexed_reader.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\io\compression_method.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\async.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-vcf-0.70.0\src\fs.rs",

    # DROP: other crates pulled as transitive deps of noodles-vcf
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-core-0.18.0\src\region.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\noodles-bgzf-0.40.0\src\reader.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\serde-1.0.214\src\lib.rs",
    r"C:\Users\miaot\.cargo\registry\src\index.crates.io-ab123\serde_json-1.0.128\src\lib.rs",

    # DROP: our own harness
    r"harnesses\rust\noodles_harness\src\main.rs",
]

# Replicate NoodlesCoverageCollector match logic
def match(path: str) -> bool:
    norm = path.replace("\\", "/")
    if crate_anchor and crate_anchor not in norm:
        return False
    if sut_filter and not any(
        f.replace("\\", "/").replace(".", "/") in norm for f in sut_filter
    ):
        return False
    return True

print(f"{'KEEP?':<6}{'PATH'}")
for p in PATHS:
    print(f"{('KEEP' if match(p) else 'DROP'):<6}{p}")
