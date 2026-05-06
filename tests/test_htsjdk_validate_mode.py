"""Integration test for the htsjdk parse_validate harness mode (Refine L2).

The harness has a new --mode parse_validate path that calls
SAMRecord.isValid() / getAlignmentBlocks() / validateCigar() etc on every
record, wrapped in try/catch. This test verifies:

1. The mode is reachable from the CLI (smoke).
2. The Python HTSJDKRunner dispatches to it when the env var is set.
3. The output JSON has the expected extra "validated_record_count" field.
4. Coverage signals visible (the test does not run JaCoCo here — that
   is the cell cascade's responsibility — but it asserts the harness JAR
   actually produced a non-empty parse).
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS_JAR = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
SEED_FILE = REPO_ROOT / "seeds" / "sam" / "minimal_tags.sam"


@pytest.mark.skipif(not HARNESS_JAR.exists(),
                    reason="Java harness JAR not built")
@pytest.mark.skipif(shutil.which("java") is None,
                    reason="java not on PATH")
class TestHtsjdkParseValidateMode:
    def test_cli_smoke(self):
        """Direct java -jar invocation with --mode parse_validate."""
        proc = subprocess.run(
            ["java", "-jar", str(HARNESS_JAR),
             "--mode", "parse_validate", "SAM", str(SEED_FILE)],
            capture_output=True, text=True, encoding="utf-8", timeout=60,
        )
        assert proc.returncode == 0, f"harness failed: {proc.stderr}"
        out = json.loads(proc.stdout)
        assert out["format"] == "SAM"
        assert out["mode"] == "parse_validate"
        assert "validated_record_count" in out
        assert out["validated_record_count"] >= 1
        # Records have the same shape as plain parse.
        assert len(out["records"]) == out["validated_record_count"]

    def test_cli_rejects_vcf_format(self):
        """parse_validate is SAM-only; VCF should error out."""
        # Use any existing VCF seed for the input path
        vcf_seed = REPO_ROOT / "seeds" / "vcf"
        candidates = list(vcf_seed.glob("*.vcf"))
        if not candidates:
            pytest.skip("no VCF seed available")
        proc = subprocess.run(
            ["java", "-jar", str(HARNESS_JAR),
             "--mode", "parse_validate", "VCF", str(candidates[0])],
            capture_output=True, text=True, encoding="utf-8", timeout=60,
        )
        assert proc.returncode == 1
        assert "only supports SAM" in proc.stderr

    def test_runner_dispatches_when_env_set(self):
        """The Python HTSJDKRunner switches to parse_validate when the env
        var is set. Compares output between the two modes and asserts the
        validate-mode output has the extra field."""
        # Lazy import — pytest collection doesn't need the module if tests
        # are skipped.
        sys.path.insert(0, str(REPO_ROOT))
        from test_engine.runners.htsjdk_runner import HTSJDKRunner

        runner = HTSJDKRunner()
        if not runner.is_available():
            pytest.skip("HTSJDK runner not available")

        # Plain mode (env var unset)
        os.environ.pop("BIOTEST_HTSJDK_SAM_PARSE_VALIDATE", None)
        plain = runner.run(SEED_FILE, "SAM", timeout_s=60)
        assert plain.success
        assert "validated_record_count" not in (plain.canonical_json or {})

        # Validate mode (env var set)
        os.environ["BIOTEST_HTSJDK_SAM_PARSE_VALIDATE"] = "1"
        try:
            validate = runner.run(SEED_FILE, "SAM", timeout_s=60)
        finally:
            os.environ.pop("BIOTEST_HTSJDK_SAM_PARSE_VALIDATE", None)
        assert validate.success
        assert "validated_record_count" in validate.canonical_json
        # Records present in both — record_count should match.
        assert len(plain.canonical_json["records"]) == validate.canonical_json["validated_record_count"]
