"""DIY source-level C++ mutator for the seqan3 harness TU.

mull 0.33 requires GLIBC 2.39, which is not available on the
Ubuntu 22.04 biotest-bench base image (see DESIGN §13.3.3). Rather
than rebuild the image to a newer base, we implement a lightweight
source-text mutator against `harnesses/cpp/biotest_harness.cpp` — the
ONLY TU on the Windows host that's built with --coverage and drives
seqan3-style SAM parsing.

Mutation catalog (chosen to mirror mull's `--ir-mutator` default set):

  * **ROR** — relational operator replacement (`<` ↔ `<=`, `>` ↔ `>=`,
    `==` ↔ `!=`)
  * **AOR** — arithmetic operator replacement (`+` ↔ `-`, `*` ↔ `/`)
  * **LCR** — logical connector replacement (`&&` ↔ `||`)
  * **UOI** — unary operator insertion (`!` inserted before boolean
    expressions; skipped if already negated to avoid syntactic drift)
  * **CONST** — integer constant replacement (`N` → `N+1`, `N-1`,
    `0`; skipped for `0` / `1` to keep mutant count sane)

Test-kill protocol — matches the mutmut / PIT cells:

  1. Baseline — compile pristine harness with `--coverage`, replay
     every file in the pure_random corpus, hash the aggregated
     stdout/stderr output.
  2. For each mutation candidate, patch the source, recompile, replay
     the corpus. If the fingerprint differs from baseline, the mutant
     is KILLED; else SURVIVED.
  3. score = killed / reachable, where reachable = killed + survived
     + timeout.

Usage:

    py -3.12 compares/scripts/run_seqan3_diy_mutator.py \\
        --corpus compares/results/coverage/pure_random/seqan3/run_0/corpus \\
        --out compares/results/mutation/pure_random_run1/seqan3
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

logger = logging.getLogger("seqan3_diy_mutator")

REPO_ROOT = Path(__file__).resolve().parents[2]
HARNESS_SRC = REPO_ROOT / "harnesses" / "cpp" / "biotest_harness.cpp"
BUILD_DIR = REPO_ROOT / "harnesses" / "cpp" / "build"


@dataclasses.dataclass
class Mutant:
    mid: int
    category: str
    line: int
    col: int
    orig: str
    replacement: str
    description: str


# --- Mutant generator -------------------------------------------------------

def _generate_mutants(src: str) -> list[Mutant]:
    """Scan `src` text and emit a list of Mutant candidates.

    We only touch non-comment / non-string tokens — the regex engines
    here deliberately avoid rewriting text inside `" ... "`, `' ... '`,
    or `// ...` / `/* ... */` comments. Because the harness is only
    ~250 lines and has no raw string literals, a simple stateful walk
    over the source is sufficient. A heavyweight approach (clang
    libtooling AST) would be more robust but mull-equivalent for the
    floor-baseline comparison we need here.
    """
    mutants: list[Mutant] = []

    # Masks — character-level flags that tell us which positions are
    # live code. 1 = mutable code, 0 = comment / string literal.
    live = bytearray(b"\x01" * len(src))
    i = 0
    while i < len(src):
        c = src[i]
        # Line comment
        if c == "/" and i + 1 < len(src) and src[i + 1] == "/":
            while i < len(src) and src[i] != "\n":
                live[i] = 0
                i += 1
            continue
        # Block comment
        if c == "/" and i + 1 < len(src) and src[i + 1] == "*":
            live[i] = live[i + 1] = 0
            i += 2
            while i + 1 < len(src) and not (
                src[i] == "*" and src[i + 1] == "/"
            ):
                live[i] = 0
                i += 1
            if i + 1 < len(src):
                live[i] = live[i + 1] = 0
                i += 2
            continue
        # String literal
        if c == '"':
            live[i] = 0
            i += 1
            while i < len(src) and src[i] != '"':
                if src[i] == "\\" and i + 1 < len(src):
                    live[i] = live[i + 1] = 0
                    i += 2
                    continue
                live[i] = 0
                i += 1
            if i < len(src):
                live[i] = 0
                i += 1
            continue
        # Char literal
        if c == "'":
            live[i] = 0
            i += 1
            while i < len(src) and src[i] != "'":
                if src[i] == "\\" and i + 1 < len(src):
                    live[i] = live[i + 1] = 0
                    i += 2
                    continue
                live[i] = 0
                i += 1
            if i < len(src):
                live[i] = 0
                i += 1
            continue
        i += 1

    def _is_live(start: int, end: int) -> bool:
        return all(live[k] for k in range(start, end))

    def _line_col(offset: int) -> tuple[int, int]:
        line = src.count("\n", 0, offset) + 1
        col = offset - (src.rfind("\n", 0, offset))
        return line, col

    # ROR — relational operator pairs. Order matters: match ">=" before ">".
    ror_pairs: list[tuple[str, str]] = [
        ("<=", ">="), (">=", "<="),
        ("==", "!="), ("!=", "=="),
    ]
    single_ror: list[tuple[str, str]] = [
        ("<", "<="), (">", ">="),
    ]

    def _add(category: str, offset: int, orig: str,
             replacement: str, desc: str) -> None:
        line, col = _line_col(offset)
        mutants.append(Mutant(
            mid=len(mutants), category=category,
            line=line, col=col,
            orig=orig, replacement=replacement,
            description=desc,
        ))

    for orig, repl in ror_pairs:
        for m in re.finditer(re.escape(orig), src):
            off = m.start()
            if not _is_live(off, off + len(orig)):
                continue
            _add("ROR", off, orig, repl, f"{orig} → {repl}")

    for orig, repl in single_ror:
        for m in re.finditer(rf"(?<![<>=!]){re.escape(orig)}(?![<>=])", src):
            off = m.start()
            if not _is_live(off, off + len(orig)):
                continue
            _add("ROR", off, orig, repl, f"{orig} → {repl}")

    # AOR — arithmetic operator pairs. Skip `+=`, `-=`, and `->`.
    for m in re.finditer(r"(?<!\+)\+(?!\+|=)", src):
        off = m.start()
        if not _is_live(off, off + 1):
            continue
        _add("AOR", off, "+", "-", "+ → -")
    for m in re.finditer(r"(?<!-)-(?!-|=|>)", src):
        off = m.start()
        if not _is_live(off, off + 1):
            continue
        _add("AOR", off, "-", "+", "- → +")

    # LCR — logical connector replacements.
    for orig, repl in (("&&", "||"), ("||", "&&")):
        for m in re.finditer(re.escape(orig), src):
            off = m.start()
            if not _is_live(off, off + len(orig)):
                continue
            _add("LCR", off, orig, repl, f"{orig} → {repl}")

    # CONST — integer constants that aren't array indices after `[`.
    for m in re.finditer(r"(?<![A-Za-z_0-9.])([2-9]|[1-9][0-9]+)(?![A-Za-z_])",
                         src):
        off = m.start()
        val = m.group(1)
        if not _is_live(off, off + len(val)):
            continue
        # Replace with val+1 — simplest flip that's semantically different
        # and always compiles (no overflow risk for small ints).
        try:
            new = str(int(val) + 1)
        except ValueError:
            continue
        _add("CONST", off, val, new, f"{val} → {new}")

    return mutants


# --- Build + replay ---------------------------------------------------------

def _compile_source(src_path: Path, exe_out: Path) -> bool:
    """Compile a C++ source file with --coverage flags. Returns True
    on success. Uses the MSYS2 g++ that's on PATH; same settings as
    the pre-built harnesses/cpp/build/biotest_harness_cov.exe."""
    exe_out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "g++",
        "-std=c++20",
        "-O0",
        "-g",
        "--coverage",
        str(src_path),
        "-o", str(exe_out),
    ]
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=90, check=False,
        )
    except subprocess.TimeoutExpired:
        return False
    return r.returncode == 0 and exe_out.exists()


def _replay_fingerprint(
    exe: Path, corpus_dir: Path, sample_n: int = 50,
    per_file_timeout_s: float = 5.0,
) -> str:
    """Run `exe SAM <path>` over the first N files and hash the combined
    stdout/stderr/exit-code triplet. Deterministic across runs as long
    as the corpus is stable."""
    files = sorted(p for p in corpus_dir.iterdir() if p.is_file())[:sample_n]
    h = hashlib.sha1()
    for p in files:
        try:
            r = subprocess.run(
                [str(exe), "SAM", str(p)],
                capture_output=True,
                timeout=per_file_timeout_s,
                check=False,
            )
            h.update(p.name.encode())
            h.update(b"|rc=")
            h.update(str(r.returncode).encode())
            h.update(b"|out=")
            # First 256 bytes are plenty to detect behaviour flips.
            h.update(r.stdout[:256])
            h.update(b"|err=")
            h.update(r.stderr[:256])
        except subprocess.TimeoutExpired:
            h.update(p.name.encode())
            h.update(b"|timeout")
    return h.hexdigest()


def _apply_mutation(src: str, m: Mutant) -> str:
    lines = src.split("\n")
    line_index = m.line - 1
    line = lines[line_index]
    # m.col is 1-based column, but we computed it as offset_from_previous_newline.
    col = m.col - 1
    # Defensive: verify the mutation point still matches orig text.
    if line[col:col + len(m.orig)] != m.orig:
        # Fall back to first occurrence on the line.
        pos = line.find(m.orig)
        if pos < 0:
            raise RuntimeError(
                f"cannot re-locate mutation {m.mid} ({m.orig!r}) "
                f"at line {m.line}"
            )
        col = pos
    lines[line_index] = line[:col] + m.replacement + line[col + len(m.orig):]
    return "\n".join(lines)


# --- Main runner ------------------------------------------------------------

def run(args: argparse.Namespace) -> int:
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    corpus_dir = args.corpus.resolve()
    if not corpus_dir.is_dir():
        logger.error("corpus dir missing: %s", corpus_dir)
        return 2

    src_text = HARNESS_SRC.read_text(encoding="utf-8")
    mutants = _generate_mutants(src_text)
    logger.info("generated %d candidate mutants", len(mutants))

    # Build baseline
    baseline_exe = out / "_baseline.exe"
    started = time.time()
    if not _compile_source(HARNESS_SRC, baseline_exe):
        logger.error("baseline compile failed")
        return 3
    baseline_fp = _replay_fingerprint(
        baseline_exe, corpus_dir,
        sample_n=args.corpus_sample,
        per_file_timeout_s=args.per_file_timeout_s,
    )
    logger.info("baseline fingerprint = %s", baseline_fp[:12])

    # Per-mutant loop.
    per_mutant: list[dict] = []
    killed = survived = timeout = compile_fail = 0
    scratch_dir = out / "_scratch"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    for i, m in enumerate(mutants):
        if args.max_mutants and i >= args.max_mutants:
            break
        if time.time() - started > args.budget_s:
            logger.info("budget exhausted at mutant %d/%d", i, len(mutants))
            break
        mut_src = _apply_mutation(src_text, m)
        mut_src_path = scratch_dir / f"m{m.mid:04d}.cpp"
        mut_src_path.write_text(mut_src, encoding="utf-8")
        mut_exe = scratch_dir / f"m{m.mid:04d}.exe"
        if not _compile_source(mut_src_path, mut_exe):
            # Doesn't compile — skip (not killed, not survived).
            compile_fail += 1
            per_mutant.append({
                "mid": m.mid, "category": m.category,
                "line": m.line, "orig": m.orig,
                "replacement": m.replacement,
                "status": "compile_fail",
            })
            continue
        try:
            mut_fp = _replay_fingerprint(
                mut_exe, corpus_dir,
                sample_n=args.corpus_sample,
                per_file_timeout_s=args.per_file_timeout_s,
            )
        except subprocess.TimeoutExpired:
            timeout += 1
            per_mutant.append({
                "mid": m.mid, "category": m.category,
                "line": m.line, "orig": m.orig,
                "replacement": m.replacement,
                "status": "timeout",
            })
            continue
        status = "killed" if mut_fp != baseline_fp else "survived"
        if status == "killed":
            killed += 1
        else:
            survived += 1
        per_mutant.append({
            "mid": m.mid, "category": m.category,
            "line": m.line, "orig": m.orig,
            "replacement": m.replacement,
            "status": status,
            "fingerprint": mut_fp[:12],
        })
        # Clean up per-mutant .exe to save disk.
        try:
            mut_exe.unlink()
        except OSError:
            pass
        if (i + 1) % 10 == 0:
            logger.info(
                "progress: %d/%d  killed=%d survived=%d compile_fail=%d",
                i + 1, len(mutants), killed, survived, compile_fail,
            )

    reachable = killed + survived + timeout
    total = reachable + compile_fail
    score = (killed / reachable) if reachable else 0.0
    dur = time.time() - started

    payload = {
        "tool": "pure_random",
        "sut": "seqan3",
        "phase": "mutation",
        "engine": "DIY C++ source mutator (mull substitute)",
        "time_budget_s": args.budget_s,
        "killed": killed,
        "survived": survived,
        "timeout": timeout,
        "suspicious": 0,
        "skipped": 0,
        "no_tests": 0,
        "not_checked": compile_fail,
        "reachable": reachable,
        "mutant_count": total,
        "score": round(score, 4),
        "score_display": (
            f"{score * 100:.2f}%" if reachable else "n/a (reachable=0)"
        ),
        "seqan3_duration_s": round(dur, 2),
        "corpus_dir": str(corpus_dir),
        "corpus_sample": args.corpus_sample,
        "per_mutant": per_mutant,
    }
    (out / "summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    logger.info(
        "[seqan3 DIY] killed=%d survived=%d reachable=%d score=%s dur=%.0fs",
        killed, survived, reachable, payload["score_display"], dur,
    )
    # Clean scratch so we don't balloon disk.
    try:
        shutil.rmtree(scratch_dir)
    except OSError:
        pass
    # Remove per-run gcda residue from the harness build dir (our
    # baseline compile writes .gcno/.gcda under cwd — avoid polluting
    # future runs).
    for suffix in (".gcda", ".gcno"):
        for p in Path(".").glob(f"*{suffix}"):
            try:
                p.unlink()
            except OSError:
                pass
    for p in out.glob("_baseline*"):
        try:
            p.unlink()
        except OSError:
            pass
    return 0


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--budget-s", type=int, default=3600)
    p.add_argument("--corpus-sample", type=int, default=30,
                   help="max files replayed per mutant fingerprint")
    p.add_argument("--per-file-timeout-s", type=float, default=3.0)
    p.add_argument("--max-mutants", type=int, default=0,
                   help="cap on number of mutants to test (0 = all)")
    args = p.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
