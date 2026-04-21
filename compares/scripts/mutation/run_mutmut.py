"""Thin wrapper around ``mutmut run`` that monkey-patches around two
of its built-in assumptions we can't satisfy cleanly from a config
file:

  1. ``CatchOutput`` replaces sys.stdout/stderr with a
     TextIOBase-style object that lacks ``fileno()`` / ``isatty()``.
     pytest's capture / terminal-reporter plugins call those methods
     at startup and raise, which pytest then surfaces as exit code 4
     (= ``BadTestExecutionCommandsException`` in mutmut's book) —
     even though the tests themselves would pass. The fix: add the
     two missing methods to CatchOutput.redirect so pytest sees a
     well-formed TTY-less stream.

  2. ``PytestRunner.execute_pytest`` calls ``pytest.main()`` in-process
     from inside each forked child. Even with (1) fixed, in-process
     pytest sometimes tripped over leftover argparse / sys.argv state
     across sequential calls in the same interpreter. The subprocess
     path is more isolation and barely slower once per-mutant setup
     cost dominates. The fix: shell out to ``python -m pytest`` via
     subprocess so every mutant gets a clean interpreter.

After the patches are applied the module hands control to mutmut's
click CLI so ``python3.12 <this file> run [args...]`` is a drop-in
replacement for ``python3.12 -m mutmut run [args...]``.
"""

from __future__ import annotations

import os
import subprocess
import sys

import mutmut.__main__ as _mm
# The trampoline mutmut injects into every mutated file does
# ``from __main__ import record_trampoline_hit`` (and, less often,
# ``MutmutProgrammaticFailException``). When our wrapper is invoked as
# ``python3.12 /path/to/run_mutmut.py`` instead of ``python3.12 -m
# mutmut``, ``__main__`` is this file — so those imports fail unless
# we re-export the names here.
from mutmut.__main__ import (  # noqa: F401
    MutmutProgrammaticFailException,
    record_trampoline_hit,
)


# --- Patch 1: give CatchOutput.redirect fileno/isatty -----------------------

_orig_catch_init = _mm.CatchOutput.__init__


def _patched_catch_init(self, callback=lambda s: None, show_spinner=False,
                        spinner_title=None):
    _orig_catch_init(
        self, callback=callback, show_spinner=show_spinner,
        spinner_title=spinner_title,
    )
    # Give pytest what it expects from a stream wrapper.  A real file
    # descriptor is required by pytest's capture machinery; fall back
    # to the original stdout's fd so pytest's dup2 chain works.
    real_stdout_fd = sys.__stdout__.fileno()

    def fileno(_self=self.redirect):
        return real_stdout_fd

    def isatty(_self=self.redirect):
        return False

    def flush(_self=self.redirect):
        return None

    self.redirect.fileno = fileno
    self.redirect.isatty = isatty
    self.redirect.flush = flush


_mm.CatchOutput.__init__ = _patched_catch_init


# --- Patch 2: keep execute_pytest in-process ---------------------------------
#
# Initially I tried swapping execute_pytest to subprocess. That broke
# mutmut's trampoline: the trampoline does
# ``from __main__ import record_trampoline_hit`` during the stats
# phase, which only works when pytest runs in the same interpreter as
# mutmut (so __main__ is mutmut.__main__). Subprocess pytest has
# __main__ = pytest itself and the import fails. We therefore keep
# pytest.main() in-process — Patch 1 (fileno/isatty on CatchOutput)
# alone was enough to stop pytest from exiting 4.


# --- Delegate to mutmut's click entrypoint ----------------------------------

if __name__ == "__main__":
    _mm.cli()
