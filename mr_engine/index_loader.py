"""
In-memory SpecIndex loader for Phase B.

Workaround for chromadb 1.5.7 HNSW persistence bug on Windows/Python 3.14:
instead of reopening a persisted ChromaDB, we load an ephemeral (in-memory)
instance and re-index from the Phase A parsed JSON chunks on startup.

This takes ~30-45 seconds but guarantees a working index every time.
"""

from __future__ import annotations

import json
import logging
import time

import chromadb
from chromadb.config import Settings

from spec_ingestor.config import PARSED_DIR, CHROMA_COLLECTION
from spec_ingestor.parser import Chunk

logger = logging.getLogger(__name__)

# Module-level singleton
_ephemeral_index: "EphemeralSpecIndex | None" = None


class EphemeralSpecIndex:
    """In-memory ChromaDB index loaded from parsed JSON chunks."""

    def __init__(self):
        t0 = time.time()
        logger.info("Loading ephemeral SpecIndex from parsed JSON...")

        self._client = chromadb.EphemeralClient(
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

        # Load chunks from Phase A parsed output
        chunks = self._load_chunks()
        if not chunks:
            raise RuntimeError(
                f"No parsed chunks found in {PARSED_DIR}. "
                "Run Phase A first: python -m spec_ingestor"
            )

        # Index in batches
        BATCH = 100
        for i in range(0, len(chunks), BATCH):
            batch = chunks[i:i + BATCH]
            self._collection.add(
                ids=[c.chunk_id for c in batch],
                documents=[c.text for c in batch],
                metadatas=[{
                    "format": c.format,
                    "spec_version": c.spec_version,
                    "commit_sha": c.commit_sha,
                    "section_id": c.section_id,
                    "rule_severity": c.rule_severity,
                    "chunk_type": c.chunk_type,
                    "has_tables": len(c.tables) > 0,
                } for c in batch],
            )

        elapsed = time.time() - t0
        logger.info(
            "Ephemeral index ready: %d documents in %.1fs",
            self._collection.count(), elapsed,
        )

    @staticmethod
    def _load_chunks() -> list[Chunk]:
        chunks: list[Chunk] = []
        for fname in ["VCFv4.5_chunks.json", "SAMv1_chunks.json"]:
            path = PARSED_DIR / fname
            if not path.exists():
                continue
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for item in raw:
                chunks.append(Chunk(**item))
        return chunks

    def query(self, question: str, n_results: int = 5, where=None) -> dict:
        """Same interface as SpecIndex.query()."""
        kwargs: dict = {
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
            "query_texts": [question],
        }
        if where:
            if len(where) > 1:
                kwargs["where"] = {"$and": [{k: v} for k, v in where.items()]}
            else:
                kwargs["where"] = where
        return self._collection.query(**kwargs)

    def collection_stats(self) -> dict:
        return {
            "collection": CHROMA_COLLECTION,
            "total_documents": self._collection.count(),
            "type": "ephemeral",
        }


def get_ephemeral_index() -> EphemeralSpecIndex:
    """Get or create the singleton ephemeral index."""
    global _ephemeral_index
    if _ephemeral_index is None:
        _ephemeral_index = EphemeralSpecIndex()
    return _ephemeral_index
