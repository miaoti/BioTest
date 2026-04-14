"""
T1-T3: Runner defense & exception handling tests.

Tests that runners gracefully degrade when external environments
crash, timeout, or are unavailable — without crashing the main process.
"""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from test_engine.runners.base import RunnerResult
from test_engine.runners.htsjdk_runner import HTSJDKRunner
from test_engine.runners.pysam_runner import PysamRunner, _check_pysam
from test_engine.runners.biopython_runner import BiopythonRunner
from test_engine.runners.seqan3_runner import SeqAn3Runner


SEEDS_DIR = Path(__file__).parent.parent / "seeds"


# ===========================================================================
# T1: Timeout interception — subprocess must not hang the main process
# ===========================================================================

class TestTimeoutHandling:
    """Runner must catch TimeoutExpired and return error_type='timeout'."""

    def test_htsjdk_timeout_returns_graceful_result(self, tmp_path):
        """Mock subprocess.run to raise TimeoutExpired."""
        jar = tmp_path / "fake.jar"
        jar.write_text("fake")
        runner = HTSJDKRunner(jar_path=jar, java_cmd="java")

        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"

        with patch("test_engine.runners.htsjdk_runner.subprocess.run") as mock_run, \
             patch("test_engine.runners.htsjdk_runner.shutil.which", return_value="java"), \
             patch("test_engine.runners.htsjdk_runner.shutil.copy2"):
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="java", timeout=5)
            result = runner.run(seed, "VCF", timeout_s=5.0)

        assert isinstance(result, RunnerResult)
        assert result.success is False
        assert result.error_type == "timeout"
        assert result.parser_name == "htsjdk"
        assert "timed out" in result.stderr

    def test_seqan3_timeout_returns_graceful_result(self, tmp_path):
        """SeqAn3 subprocess timeout must not crash."""
        binary = tmp_path / "fake_harness.exe"
        binary.write_text("fake")
        runner = SeqAn3Runner(binary_path=binary)

        seed = SEEDS_DIR / "sam" / "minimal_tags.sam"

        with patch("test_engine.runners.seqan3_runner.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="harness", timeout=10)
            result = runner.run(seed, "SAM", timeout_s=10.0)

        assert result.success is False
        assert result.error_type == "timeout"
        assert result.parser_name == "seqan3"


# ===========================================================================
# T2: Crash log capturing — stderr must be preserved for triage
# ===========================================================================

class TestCrashLogCapturing:
    """Runner must capture stderr from crashed subprocesses."""

    def test_htsjdk_nonzero_exit_preserves_stderr(self, tmp_path):
        """Non-zero exit code + Java stack trace must be captured in stderr."""
        jar = tmp_path / "fake.jar"
        jar.write_text("fake")
        runner = HTSJDKRunner(jar_path=jar, java_cmd="java")

        fake_stderr = (
            "java.lang.NullPointerException: Cannot invoke method on null\n"
            "\tat htsjdk.variant.vcf.VCFCodec.decode(VCFCodec.java:123)\n"
            "\tat BioTestHarness.parseVcf(BioTestHarness.java:55)\n"
        )
        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stdout = ""
        mock_proc.stderr = fake_stderr

        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"

        with patch("test_engine.runners.htsjdk_runner.subprocess.run", return_value=mock_proc), \
             patch("test_engine.runners.htsjdk_runner.shutil.which", return_value="java"), \
             patch("test_engine.runners.htsjdk_runner.shutil.copy2"):
            result = runner.run(seed, "VCF")

        assert result.success is False
        assert result.error_type == "crash"
        assert result.exit_code == 1
        assert "NullPointerException" in result.stderr
        assert "VCFCodec.decode" in result.stderr

    def test_htsjdk_malformed_json_reports_parse_error(self, tmp_path):
        """stdout with invalid JSON must be caught and reported."""
        jar = tmp_path / "fake.jar"
        jar.write_text("fake")
        runner = HTSJDKRunner(jar_path=jar, java_cmd="java")

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "THIS IS NOT JSON {broken"
        mock_proc.stderr = ""

        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"

        with patch("test_engine.runners.htsjdk_runner.subprocess.run", return_value=mock_proc), \
             patch("test_engine.runners.htsjdk_runner.shutil.which", return_value="java"), \
             patch("test_engine.runners.htsjdk_runner.shutil.copy2"):
            result = runner.run(seed, "VCF")

        assert result.success is False
        assert result.error_type == "parse_error"
        assert "Invalid JSON" in result.stderr

    def test_seqan3_crash_preserves_stderr(self, tmp_path):
        """C++ segfault stderr must be captured."""
        binary = tmp_path / "fake_harness.exe"
        binary.write_text("fake")
        runner = SeqAn3Runner(binary_path=binary)

        mock_proc = MagicMock()
        mock_proc.returncode = 139  # SIGSEGV
        mock_proc.stdout = ""
        mock_proc.stderr = "Segmentation fault (core dumped)"

        seed = SEEDS_DIR / "sam" / "minimal_tags.sam"

        with patch("test_engine.runners.seqan3_runner.subprocess.run", return_value=mock_proc):
            result = runner.run(seed, "SAM")

        assert result.success is False
        assert result.error_type == "crash"
        assert result.exit_code == 139
        assert "Segmentation fault" in result.stderr


# ===========================================================================
# T3: Availability guards — unavailable runners must be skipped gracefully
# ===========================================================================

class TestAvailabilityGuards:
    """Runners must report unavailability without crashing."""

    def test_htsjdk_unavailable_when_no_java(self):
        """If java is not on PATH, is_available() must be False."""
        runner = HTSJDKRunner(java_cmd="nonexistent_java_binary_xyz")
        assert runner.is_available() is False

    def test_htsjdk_unavailable_when_no_jar(self, tmp_path):
        """If JAR doesn't exist, is_available() must be False."""
        runner = HTSJDKRunner(jar_path=tmp_path / "does_not_exist.jar")
        assert runner.is_available() is False

    def test_htsjdk_run_when_unavailable_returns_error(self, tmp_path):
        """Calling run() on unavailable runner must not crash."""
        runner = HTSJDKRunner(jar_path=tmp_path / "nope.jar")
        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
        result = runner.run(seed, "VCF")
        assert result.success is False
        assert result.error_type == "parse_error"

    def test_pysam_availability_detection(self):
        """pysam runner must detect installation state."""
        runner = PysamRunner()
        # Whether True or False, it must not crash
        avail = runner.is_available()
        assert isinstance(avail, bool)

    def test_pysam_run_when_unavailable(self):
        """If pysam not installed, run() must return error, not crash."""
        import test_engine.runners.pysam_runner as mod
        original = mod._pysam_available
        try:
            mod._pysam_available = False
            runner = PysamRunner()
            seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
            result = runner.run(seed, "VCF")
            assert result.success is False
            assert "not installed" in result.stderr
        finally:
            mod._pysam_available = original

    def test_seqan3_unavailable_when_no_binary(self, tmp_path):
        """If compiled binary doesn't exist, is_available() must be False."""
        runner = SeqAn3Runner(binary_path=tmp_path / "nope.exe")
        assert runner.is_available() is False

    def test_biopython_rejects_vcf_format(self):
        """Biopython runner must reject VCF format explicitly."""
        runner = BiopythonRunner()
        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
        # Force availability to True for this test
        import test_engine.runners.biopython_runner as mod
        original = mod._biopython_available
        try:
            mod._biopython_available = True
            result = runner.run(seed, "VCF")
            assert result.success is False
            assert "only supports SAM" in result.stderr
        finally:
            mod._biopython_available = original

    def test_seqan3_rejects_vcf_format(self, tmp_path):
        """SeqAn3 runner must reject VCF format explicitly."""
        binary = tmp_path / "fake.exe"
        binary.write_text("fake")
        runner = SeqAn3Runner(binary_path=binary)
        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
        result = runner.run(seed, "VCF")
        assert result.success is False
        assert "only supports SAM" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
