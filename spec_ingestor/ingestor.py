"""
Step 1: Automated Spec Ingestion

Fetches LaTeX source files from the samtools/hts-specs GitHub repository
via the GitHub API. Records the exact commit SHA for reproducibility.
Resolves \\input{...} references to pull dependent files.
"""

import json
import logging
import re
import base64
from pathlib import Path

import requests

from .config import (
    GITHUB_API_BASE,
    GITHUB_BRANCH,
    RAW_DIR,
    TARGET_TEX_FILES,
    SPEC_META,
)

logger = logging.getLogger(__name__)


def _github_headers() -> dict:
    """Return headers for GitHub API requests (supports optional token)."""
    import os

    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_head_sha() -> str:
    """Fetch the current HEAD commit SHA of the master branch."""
    url = f"{GITHUB_API_BASE}/git/ref/heads/{GITHUB_BRANCH}"
    resp = requests.get(url, headers=_github_headers(), timeout=30)
    resp.raise_for_status()
    sha = resp.json()["object"]["sha"]
    logger.info("HEAD commit SHA: %s", sha)
    return sha


def fetch_file_content(path: str, commit_sha: str) -> str:
    """Fetch a single file's content from the repo at a specific commit."""
    url = f"{GITHUB_API_BASE}/contents/{path}?ref={commit_sha}"
    resp = requests.get(url, headers=_github_headers(), timeout=60)
    resp.raise_for_status()
    data = resp.json()

    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")

    # For large files, fall back to the raw download URL
    raw_url = data.get("download_url")
    if raw_url:
        raw_resp = requests.get(raw_url, timeout=120)
        raw_resp.raise_for_status()
        return raw_resp.text

    raise RuntimeError(f"Could not decode content for {path}")


def _extract_input_refs(tex_content: str) -> list[str]:
    """Find all \\input{filename} references in a TeX file."""
    # Matches \input{somefile} — the referenced file may or may not have .tex extension
    return re.findall(r"\\input\{([^}]+)\}", tex_content)


def fetch_spec_files(commit_sha: str) -> dict[str, str]:
    """
    Download target .tex files and any files they \\input{...}.

    Returns a dict mapping filename -> content for every file fetched.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fetched: dict[str, str] = {}
    to_fetch = list(TARGET_TEX_FILES)
    seen: set[str] = set()

    while to_fetch:
        filename = to_fetch.pop(0)
        if filename in seen:
            continue
        seen.add(filename)

        # Ensure .tex extension for input references
        tex_name = filename if filename.endswith(".tex") else f"{filename}.tex"
        logger.info("Fetching %s ...", tex_name)

        try:
            content = fetch_file_content(tex_name, commit_sha)
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                # For primary targets, try PDF fallback; for \input refs, skip
                is_primary = tex_name in TARGET_TEX_FILES
                if is_primary:
                    logger.warning(
                        "%s not found as .tex — attempting PDF fallback", tex_name
                    )
                    pdf_name = tex_name.replace(".tex", ".pdf")
                    try:
                        content = fetch_file_content(pdf_name, commit_sha)
                        fetched[pdf_name] = content
                        (RAW_DIR / pdf_name).write_bytes(
                            content.encode("utf-8", errors="replace")
                        )
                        continue
                    except requests.HTTPError:
                        logger.error("PDF fallback also failed for %s", pdf_name)
                        raise
                else:
                    logger.info(
                        "Skipping \\input ref %s (not found — likely build-generated)",
                        tex_name,
                    )
                    continue
            else:
                raise

        fetched[tex_name] = content
        (RAW_DIR / tex_name).write_text(content, encoding="utf-8")

        # Resolve \input{} dependencies
        for ref in _extract_input_refs(content):
            ref_file = ref if ref.endswith(".tex") else f"{ref}.tex"
            if ref_file not in seen:
                logger.info("  -> found \\input{%s}, queuing", ref)
                to_fetch.append(ref_file)

    return fetched


def run_ingestion() -> tuple[str, dict[str, str]]:
    """
    Top-level ingestion entry point.

    Returns:
        (commit_sha, files_dict) where files_dict maps filename -> content.
    """
    sha = get_head_sha()
    files = fetch_spec_files(sha)

    # Persist manifest for reproducibility
    manifest = {"commit_sha": sha, "files": list(files.keys())}
    manifest_path = RAW_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info(
        "Ingestion complete: %d files fetched at commit %s", len(files), sha[:10]
    )
    return sha, files
