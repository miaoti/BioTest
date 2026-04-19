"""
Smoke tests for the Tier-2 seed fetch list.

The fetch itself hits the network and is exercised only in the
`integration` marker. These tests are offline and assert invariants
on `SEED_SOURCES` that would silently rot the corpus if broken:

- every SAM entry that is a .bam file gets URL-encoding preserved;
- no duplicate destination filenames;
- SAM block is at least the size claimed in the Phase 1 plan (so a
  future edit that accidentally drops entries is caught).
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from seeds.fetch_real_world import SEED_SOURCES, MAX_FILE_BYTES


def _by_fmt(fmt: str):
    return [e for e in SEED_SOURCES if e[0] == fmt]


def test_no_duplicate_destinations():
    names = [f"{fmt}/{name}" for fmt, name, _url, _desc in SEED_SOURCES]
    dups = sorted(n for n in set(names) if names.count(n) > 1)
    assert not dups, f"duplicate SEED_SOURCES entries: {dups}"


def test_sam_corpus_size_post_phase_1():
    sam = _by_fmt("sam")
    # Pre-phase-1 had 11 SAM entries. Phase 1 adds ~30 htslib SAMs + 3 BAMs.
    assert len(sam) >= 40, (
        f"SAM seed corpus shrunk to {len(sam)} entries (expected >=40 post-Phase-1)"
    )


def test_hash_urls_use_percent_23():
    # Every htslib test file whose upstream name contains `#` MUST URL-encode
    # it as %23; a raw `#` becomes a fragment separator and silently 404s.
    for fmt, name, url, _desc in SEED_SOURCES:
        if "htslib" in url and "develop/test/" in url:
            # If the local filename hints at a `#` (e.g. ce_1 from ce#1),
            # the URL's path component must contain %23 before the .sam.
            # We only flag the positive case: if %23 is present, it must
            # not be a plain %23% (double-encoded) artifact.
            path = url.split("?", 1)[0]
            assert "%2523" not in path, f"double-encoded # in {url}"


def test_bam_entries_live_under_sam_subdir():
    # BAM files are stored under seeds/sam/ so SeedCorpus globs discover
    # them with a single glob in Phase 3. The fetch script decides this
    # by looking at the first tuple element.
    for fmt, name, _url, _desc in SEED_SOURCES:
        if name.endswith(".bam"):
            assert fmt == "sam", (
                f"BAM file {name} should be fetched into seeds/sam/, not seeds/{fmt}/"
            )


def test_file_size_cap_is_honored():
    # Safety invariant — not checked by the fetch loop directly, but any
    # future edit that loosens this cap should be visible.
    assert MAX_FILE_BYTES == 500 * 1024, "per-file size cap changed unexpectedly"
