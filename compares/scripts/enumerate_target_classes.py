"""Enumerate the fully-qualified Java class names that match
`biotest_config.yaml: coverage.target_filters[<FMT>][<sut>]` — i.e. the
same scope the fairness recipe (compares/scripts/measure_coverage.py)
uses to grade coverage. PIT's `--targetClasses` is then populated with
exactly this list so mutation testing hits only the code BioTest /
Jazzer actually exercises, not the whole htsjdk surface.

For htsjdk this matters: the raw `htsjdk.jar` ships BAM codecs, CRAM,
legacy BCF writers, JEXL filter expressions, tabix indexers etc. —
none of which are touched by the VCF-text or SAM-text parse paths. If
PIT mutates them they contribute to the denominator without any test
ever killing them; the mutation score craters from "real signal" to
"dominant dead weight." The fairness recipe already scopes coverage
to just the parse path — we reuse the exact same filter here.

Implementation:
  1. Load filter rules from
     `biotest_config.yaml: coverage.target_filters[<FMT>][<sut>]`.
  2. Walk the classfiles directory (same one the sampler uses for
     JaCoCo `--classfiles`) and convert each `foo/bar/Baz.class` into
     `foo.bar.Baz`.
  3. Group by JaCoCo-style package ("foo/bar") and apply the rule's
     include / exclude sourcefile-prefix filters via
     `test_engine.feedback.coverage_collector.filter_file_matches` —
     same code the JaCoCoCollector uses for line coverage.
  4. Emit the list either as a plain newline-separated dump or as a
     PIT-CLI comma-separated string.

The match uses the CLASS-name prefix rule `filter_file_matches` uses
on sourcefile names. Sourcefile name "VCFCodec.java" matches if
"VCFCodec" starts with any include pattern. Inner classes like
`VCFCodec$Listener.class` appear as separate files but share the same
sourcefile-name prefix `VCFCodec` so they are captured automatically.

Usage:

    # VCF target class list, one per line:
    py -3.12 compares/scripts/enumerate_target_classes.py \
        --sut htsjdk --format VCF \
        --classes-dir compares/harnesses/jazzer/build/htsjdk-classes

    # PIT-CLI comma form, newline-free — feed to --targetClasses:
    py -3.12 compares/scripts/enumerate_target_classes.py \
        --sut htsjdk --format SAM \
        --classes-dir compares/harnesses/jazzer/build/htsjdk-classes \
        --format-out pit
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from test_engine.feedback.coverage_collector import (  # noqa: E402
    parse_filter_rules,
    filter_file_matches,
)


def enumerate_classes(
    classes_dir: Path,
    filter_rules: list[str],
) -> list[str]:
    """Walk `classes_dir` (dir holding foo/bar/Baz.class files) and
    return the fully-qualified class names whose sourcefile-basename
    matches any rule's (package, includes, excludes) triple.

    A rule like
    `htsjdk/variant/variantcontext::-JEXL,-Jexl,-*JEXL*,-*Jexl*` only
    matches classes directly in package `htsjdk.variant.variantcontext`
    (sub-packages `filter/`, `writer/` are handled by their own rules).
    This mirrors `JaCoCoCollector._ensure_xml`'s per-package semantics.
    """
    rules = parse_filter_rules(filter_rules)
    # Pre-group class files by JaCoCo-style package name.
    by_pkg: dict[str, list[Path]] = {}
    for cls_path in classes_dir.rglob("*.class"):
        rel = cls_path.relative_to(classes_dir)
        if rel.parent == Path("."):
            pkg = ""  # default package — no rule should match this
        else:
            pkg = rel.parent.as_posix()
        by_pkg.setdefault(pkg, []).append(cls_path)

    out: set[str] = set()
    for pkg, includes, excludes in rules:
        files = by_pkg.get(pkg, [])
        for cp in files:
            cls_basename = cp.name  # "VCFCodec.class" or "VCFCodec$1.class"
            # JaCoCo's filter rule keys on the *sourcefile* name, which
            # looks like "VCFCodec.java" — convert by mapping .class
            # (and any "$…" inner-class marker) back to the outer
            # sourcefile name the rule author would have typed.
            sourcefile = cls_basename.split("$", 1)[0]  # strip inner-class tail
            if sourcefile.endswith(".class"):
                sourcefile = sourcefile[: -len(".class")] + ".java"
            if not filter_file_matches(sourcefile, includes, excludes):
                continue
            stem = cls_basename[: -len(".class")]
            fqn = (pkg.replace("/", ".") + "." + stem) if pkg else stem
            out.add(fqn)
    return sorted(out)


def _cli() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sut", required=True,
                    help="SUT key in biotest_config.yaml (e.g. htsjdk)")
    ap.add_argument("--format", dest="format_", required=True,
                    choices=["VCF", "SAM", "vcf", "sam"])
    ap.add_argument("--classes-dir", type=Path, required=True,
                    help="Directory with foo/bar/Baz.class tree (same dir "
                         "coverage_sampler passes to JaCoCo --classfiles).")
    ap.add_argument("--config", default=str(_REPO_ROOT / "biotest_config.yaml"))
    ap.add_argument("--format-out", choices=["lines", "pit"], default="lines",
                    help="`lines` = one FQN per line (default). "
                         "`pit` = comma-joined single line for PIT's "
                         "--targetClasses flag.")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    per_fmt = (cfg.get("coverage") or {}).get("target_filters", {}).get(args.format_.upper(), {})
    if not isinstance(per_fmt, dict):
        print(f"no coverage.target_filters.{args.format_.upper()} entry in {args.config}",
              file=sys.stderr)
        return 2
    filter_rules = per_fmt.get(args.sut)
    if not isinstance(filter_rules, list):
        print(f"no coverage.target_filters.{args.format_.upper()}.{args.sut} entry",
              file=sys.stderr)
        return 2

    classes = enumerate_classes(Path(args.classes_dir), filter_rules)
    if args.format_out == "pit":
        print(",".join(classes))
    else:
        for c in classes:
            print(c)
    print(f"[enumerate] {args.format_.upper()}/{args.sut}: {len(classes)} classes",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
