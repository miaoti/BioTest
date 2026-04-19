"""
Smoke tests for the htslib-corpus subset of seeds/fetch_real_world.py.

We do NOT hit the network here; the tests check that:
  1. The SEED_SOURCES list registers the htslib entries under the agreed
     naming + URL-encoding convention.
  2. If htslib seeds are already present on disk (landed by a previous
     fetch), they parse through the framework's normalizers — the same
     gate Phase C will apply.

CI without network stays green; a locally-populated corpus catches
normalizer regressions against upstream htslib test files.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SEEDS_DIR = Path(__file__).resolve().parent.parent / "seeds"


def _load_seed_sources():
    """Load the SEED_SOURCES tuple from seeds/fetch_real_world.py."""
    script = SEEDS_DIR / "fetch_real_world.py"
    spec = importlib.util.spec_from_file_location("fetch_real_world", script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SEED_SOURCES


def _htslib_entries():
    return [
        (subdir, name, url, desc)
        for (subdir, name, url, desc) in _load_seed_sources()
        if name.startswith("real_world_htslib_")
    ]


class TestHtslibSourceRegistration:
    def test_htslib_block_is_registered(self):
        entries = _htslib_entries()
        # At least the VCF + SAM block we added should be present.
        assert len(entries) >= 10, (
            f"Expected at least 10 htslib sources, got {len(entries)}"
        )

    def test_naming_convention(self):
        for subdir, name, url, desc in _htslib_entries():
            assert name.startswith("real_world_htslib_"), name
            assert name.endswith(f".{subdir}"), (name, subdir)

    def test_raw_github_host(self):
        for _, name, url, _ in _htslib_entries():
            assert url.startswith(
                "https://raw.githubusercontent.com/samtools/htslib/"
            ), (name, url)

    def test_hash_is_url_encoded(self):
        """Any htslib test filename containing `#` must be %23 in the URL.

        htslib uses `#` as a test-variant separator (e.g. `c1#clip.sam`).
        `requests.get` silently strips `#` as a fragment separator, so the
        raw URL MUST pre-encode it as `%23` or we get 404s that look like
        network flakes.
        """
        for _, name, url, _ in _htslib_entries():
            # If the filename portion of the raw URL contains a literal '#',
            # the request would 404 — fail the test loudly.
            path_part = url.split("?", 1)[0]
            assert "#" not in path_part, (
                f"{name}: url {url} contains bare '#'; must be %23"
            )


class TestHtslibSeedsParse:
    """If the htslib seeds are on disk (landed by a previous fetch),
    they must parse through the framework's normalizers. Otherwise
    skip — preserves CI-no-network."""

    @pytest.mark.parametrize(
        "subdir,name,_url,_desc",
        _htslib_entries(),
        ids=[n for _, n, _, _ in _htslib_entries()],
    )
    def test_seed_parses_if_present(self, subdir, name, _url, _desc):
        path = SEEDS_DIR / subdir / name
        if not path.exists():
            pytest.skip(f"{name} not fetched yet; run seeds/fetch_real_world.py")

        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)

        if subdir == "vcf":
            from test_engine.canonical.vcf_normalizer import normalize_vcf_text
            normalize_vcf_text(lines)
        elif subdir == "sam":
            from test_engine.canonical.sam_normalizer import normalize_sam_text
            normalize_sam_text(lines)
        else:
            pytest.fail(f"Unknown subdir {subdir}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
