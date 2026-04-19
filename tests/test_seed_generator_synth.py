"""
Phase 5 tests — generator-mode seed synthesis (SeedMind pattern).

Covers the local components (AST whitelist + sandbox execution); the
end-to-end LLM call is covered by the integration suite and is skipped
offline.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from mr_engine.agent.seed_synthesizer import (
    _ast_whitelist_check,
    _GeneratorCodeRejected,
    _run_generator_sandboxed,
    _ALLOWED_IMPORTS,
)


# ---------------------------------------------------------------------------
# AST whitelist
# ---------------------------------------------------------------------------

class TestAstWhitelist:
    def test_accepts_allowed_imports(self):
        _ast_whitelist_check(
            "import random\nimport string\n"
            "from itertools import chain\n"
            "def generate(seed: int) -> str:\n"
            "    return 'x'\n"
        )

    @pytest.mark.parametrize("module", [
        "os", "subprocess", "socket", "urllib", "requests", "importlib",
        "ctypes", "multiprocessing", "sys", "pathlib",
    ])
    def test_rejects_dangerous_imports(self, module):
        with pytest.raises(_GeneratorCodeRejected):
            _ast_whitelist_check(f"import {module}\n")

    @pytest.mark.parametrize("module", [
        "os", "subprocess", "socket", "urllib.request",
    ])
    def test_rejects_dangerous_from_imports(self, module):
        with pytest.raises(_GeneratorCodeRejected):
            _ast_whitelist_check(f"from {module} import thing\n")

    def test_rejects_syntax_error(self):
        with pytest.raises(_GeneratorCodeRejected):
            _ast_whitelist_check("def broken(:\n")

    def test_allowed_imports_covers_safe_essentials(self):
        # The allowed set should contain random + string + itertools
        # (the workhorse trio for format generators); everything else is
        # a judgment call the plan explicitly made.
        must_have = {"random", "string", "itertools", "struct", "math"}
        assert must_have.issubset(_ALLOWED_IMPORTS)


# ---------------------------------------------------------------------------
# Sandbox execution
# ---------------------------------------------------------------------------

class TestSandbox:
    # Use a raw string so the escape sequences reach the subprocess's
    # Python parser as actual `\t` / `\n` escape-sequence TOKENS, not
    # as actual tab/newline bytes (which would terminate the string
    # literal inside the generator's return statement).
    GOOD_GENERATOR = r'''import random
def generate(seed: int) -> str:
    rng = random.Random(seed)
    return "@HD\tVN:1.6\n@SQ\tSN:chr1\tLN:1000\n" + str(rng.randint(0, 99)) + "\n"
'''

    def test_runs_good_generator_and_returns_deterministic_output(self):
        a = _run_generator_sandboxed(self.GOOD_GENERATOR, seed=42)
        b = _run_generator_sandboxed(self.GOOD_GENERATOR, seed=42)
        assert a == b
        assert a is not None and a.startswith("@HD")

    def test_different_seeds_give_different_outputs(self):
        a = _run_generator_sandboxed(self.GOOD_GENERATOR, seed=1)
        b = _run_generator_sandboxed(self.GOOD_GENERATOR, seed=2)
        assert a != b

    def test_missing_generate_is_rejected(self):
        src = "def helper(): return 'foo'\n"
        assert _run_generator_sandboxed(src, seed=0) is None

    def test_exception_in_generator_is_rejected(self):
        src = "def generate(seed): raise ValueError('boom')\n"
        assert _run_generator_sandboxed(src, seed=0) is None

    def test_non_string_return_is_rejected(self):
        src = "def generate(seed): return 42\n"
        assert _run_generator_sandboxed(src, seed=0) is None

    def test_timeout_kills_infinite_loop(self):
        src = (
            "def generate(seed):\n"
            "    while True:\n"
            "        pass\n"
        )
        # 1-second budget — the infinite loop should trip the timeout.
        out = _run_generator_sandboxed(src, seed=0, timeout_s=1.0)
        assert out is None

    def test_output_over_size_cap_rejected(self):
        # Generate 1 MB of text; cap at 10 KB.
        src = (
            "def generate(seed):\n"
            "    return 'A' * (1024 * 1024)\n"
        )
        out = _run_generator_sandboxed(src, seed=0, max_bytes=10 * 1024)
        assert out is None
