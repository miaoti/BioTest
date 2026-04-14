"""
Main orchestrator for the Spec Ingestor and RAG Index Builder pipeline.

Usage:
    python -m spec_ingestor.main                  # Full pipeline (ingest + parse + index)
    python -m spec_ingestor.main --step ingest     # Only fetch from GitHub
    python -m spec_ingestor.main --step parse      # Only parse (requires prior ingest)
    python -m spec_ingestor.main --step index      # Only index (requires prior parse)
    python -m spec_ingestor.main --query "What are valid CIGAR operations?"
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from .config import RAW_DIR, PARSED_DIR
from .ingestor import run_ingestion
from .parser import parse_and_chunk_all, Chunk
from .indexer import SpecIndex

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def step_ingest() -> tuple[str, dict[str, str]]:
    """Run the ingestion step: fetch specs from GitHub."""
    logger.info("=== Step 1: Ingestion ===")
    sha, files = run_ingestion()
    logger.info("Fetched %d files at commit %s", len(files), sha[:10])
    return sha, files


def step_parse(sha: str | None = None, files: dict[str, str] | None = None) -> list[Chunk]:
    """Run the parse + chunk step. Loads from disk if args not provided."""
    logger.info("=== Step 2-3: Parsing & Chunking ===")

    if sha is None or files is None:
        manifest_path = RAW_DIR / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(
                "No manifest.json found. Run the ingest step first."
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        sha = manifest["commit_sha"]
        files = {}
        for fname in manifest["files"]:
            fpath = RAW_DIR / fname
            if fpath.exists():
                files[fname] = fpath.read_text(encoding="utf-8")

    chunks = parse_and_chunk_all(files, sha)
    logger.info("Produced %d chunks", len(chunks))
    return chunks


def step_index(chunks: list[Chunk] | None = None) -> SpecIndex:
    """Run the indexing step. Loads chunks from disk if not provided."""
    logger.info("=== Step 4: Indexing ===")

    if chunks is None:
        chunks = []
        for json_file in PARSED_DIR.glob("*_chunks.json"):
            raw = json.loads(json_file.read_text(encoding="utf-8"))
            for item in raw:
                chunks.append(Chunk(**item))

    if not chunks:
        raise ValueError("No chunks found. Run the parse step first.")

    index = SpecIndex()
    count = index.index_chunks(chunks)
    logger.info("Indexed %d chunks", count)
    return index


def run_query(question: str, where: dict | None = None) -> None:
    """Run a semantic query against the existing index."""
    index = SpecIndex()
    results = index.query(question, n_results=5, where=where)

    print(f"\n{'='*60}")
    print(f"Query: {question}")
    if where:
        print(f"Filter: {where}")
    print(f"{'='*60}\n")

    for i, (doc, meta, dist) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0])
    ):
        print(f"--- Result {i+1} (distance: {dist:.4f}) ---")
        print(f"  Section: {meta['section_id']}")
        print(f"  Format: {meta['format']} {meta['spec_version']}")
        print(f"  Severity: {meta['rule_severity']}")
        print(f"  Text: {doc[:300]}...")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Spec Ingestor and RAG Index Builder"
    )
    parser.add_argument(
        "--step",
        choices=["ingest", "parse", "index", "all"],
        default="all",
        help="Which pipeline step to run (default: all)",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Run a semantic query against the index instead of building it",
    )
    parser.add_argument(
        "--filter-format",
        type=str,
        help="Filter query results by format (VCF or SAM)",
    )
    parser.add_argument(
        "--filter-severity",
        type=str,
        help="Filter query results by rule_severity (CRITICAL, ADVISORY, INFORMATIONAL)",
    )
    args = parser.parse_args()

    if args.query:
        where = {}
        if args.filter_format:
            where["format"] = args.filter_format
        if args.filter_severity:
            where["rule_severity"] = args.filter_severity
        run_query(args.query, where or None)
        return

    sha, files, chunks = None, None, None

    if args.step in ("ingest", "all"):
        sha, files = step_ingest()

    if args.step in ("parse", "all"):
        chunks = step_parse(sha, files)

    if args.step in ("index", "all"):
        index = step_index(chunks)
        stats = index.collection_stats()
        logger.info("Final index stats: %s", stats)

    logger.info("Pipeline complete.")


if __name__ == "__main__":
    main()
