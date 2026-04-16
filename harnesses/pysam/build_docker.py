#!/usr/bin/env python3
"""
Build the biotest-pysam Docker image.

Usage:
    python build_docker.py          # Build image
    python build_docker.py --test   # Build + smoke test
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

IMAGE_NAME = "biotest-pysam:latest"
DOCKERFILE_DIR = Path(__file__).resolve().parent


def check_docker():
    """Verify Docker is available and running."""
    if not shutil.which("docker"):
        print("ERROR: Docker not found on PATH", file=sys.stderr)
        sys.exit(1)
    try:
        subprocess.run(
            ["docker", "info"],
            capture_output=True, timeout=10,
        )
    except (subprocess.TimeoutExpired, Exception):
        print("ERROR: Docker daemon is not running", file=sys.stderr)
        sys.exit(1)
    print("Docker is available and running.")


def build_image():
    """Build the biotest-pysam Docker image."""
    print(f"Building {IMAGE_NAME} from {DOCKERFILE_DIR}...")
    result = subprocess.run(
        ["docker", "build", "-t", IMAGE_NAME, str(DOCKERFILE_DIR)],
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"ERROR: Docker build failed (exit {result.returncode})", file=sys.stderr)
        sys.exit(1)
    print(f"Successfully built {IMAGE_NAME}")


def smoke_test():
    """Quick test: parse a minimal VCF string inside the container."""
    print("Running smoke test...")
    # Create a minimal VCF in a temp dir and mount it
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="biotest_pysam_test_"))
    vcf = tmp / "test.vcf"
    vcf.write_text(
        "##fileformat=VCFv4.3\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
        "chr1\t100\t.\tA\tT\t30\tPASS\t.\n",
        encoding="utf-8",
    )

    # Docker on Windows: convert path for bind mount
    mount_path = str(tmp).replace("\\", "/")

    result = subprocess.run(
        [
            "docker", "run", "--rm",
            "-v", f"{mount_path}:/data",
            IMAGE_NAME,
            "VCF", "/data/test.vcf",
        ],
        capture_output=True, text=True, timeout=30,
    )

    # Cleanup
    import shutil as _shutil
    _shutil.rmtree(tmp, ignore_errors=True)

    if result.returncode != 0:
        print(f"Smoke test FAILED:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    import json
    data = json.loads(result.stdout)
    assert data["format"] == "VCF"
    assert len(data["records"]) == 1
    assert data["records"][0]["POS"] == 100  # 1-based
    print("Smoke test PASSED: VCF parsed correctly, POS=100 (1-based)")


def main():
    parser = argparse.ArgumentParser(description="Build biotest-pysam Docker image")
    parser.add_argument("--test", action="store_true", help="Run smoke test after build")
    args = parser.parse_args()

    check_docker()
    build_image()
    if args.test:
        smoke_test()
    print("Done.")


if __name__ == "__main__":
    main()
