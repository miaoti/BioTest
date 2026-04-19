"""
Static checks on biotest.py that catch NameErrors before runtime.

The full Phase D loop is an async, iteration-driven, LLM-calling
monster — it's expensive to exercise end-to-end, and NameErrors in
rarely-entered branches (the reachability-filter wiring, the
generator-mode branch) can survive the regular unit suite. These tests
AST-parse + pyflakes the module so undefined names surface in seconds.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
BIOTEST_PY = REPO_ROOT / "biotest.py"


def test_biotest_module_compiles():
    """biotest.py must at least parse to bytecode; syntax errors should
    never ship."""
    src = BIOTEST_PY.read_text(encoding="utf-8")
    compile(src, str(BIOTEST_PY), "exec")


def test_biotest_no_undefined_names_in_feedback_loop():
    """Use pyflakes (stdlib-only fallback: py_compile is not enough
    because NameError is a runtime thing, but pyflakes does a static
    scan)."""
    try:
        import pyflakes.api  # noqa: F401
    except ImportError:
        pytest.skip("pyflakes not installed; skipping static name check")

    from pyflakes.api import checkPath
    from pyflakes.reporter import Reporter
    import io

    out = io.StringIO()
    err = io.StringIO()
    rep = Reporter(out, err)
    checkPath(str(BIOTEST_PY), rep)

    combined = out.getvalue() + err.getvalue()
    # pyflakes emits "undefined name 'X'" for NameError-equivalent cases
    # at parse time. We ONLY fail the test on that specific signature —
    # unused-import / shadow warnings are out of scope here.
    bad_lines = [
        ln for ln in combined.splitlines()
        if "undefined name" in ln
    ]
    assert not bad_lines, (
        "biotest.py has undefined names that will NameError at runtime:\n"
        + "\n".join(bad_lines)
    )
