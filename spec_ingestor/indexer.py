"""
Step 4: Vector Database Integration

Generates embeddings and stores them in a local ChromaDB instance with full
metadata for filtered retrieval.

By default uses ChromaDB's built-in local embedding model (all-MiniLM-L6-v2
via onnxruntime) — no API key required. Optionally supports OpenAI
text-embedding-3-small when OPENAI_API_KEY is set and use_openai=True.
"""

import logging
import os
from typing import Optional

import chromadb
from chromadb.config import Settings

from .config import (
    CHROMA_COLLECTION,
    CHROMA_DIR,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,
)
from .parser import Chunk

logger = logging.getLogger(__name__)

_BATCH_SIZE = 128


class SpecIndex:
    """Manages the ChromaDB vector store for spec chunks."""

    def __init__(self, persist_dir: Optional[str] = None, use_openai: bool = False):
        path = persist_dir or str(CHROMA_DIR)
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(
            path=path,
            settings=Settings(anonymized_telemetry=False),
        )
        self._use_openai = use_openai and bool(os.environ.get("OPENAI_API_KEY"))

        if self._use_openai:
            from openai import OpenAI
            self._openai = OpenAI()
            logger.info("Using OpenAI %s for embeddings", EMBEDDING_MODEL)
        else:
            self._openai = None
            logger.info("Using ChromaDB default local embeddings (all-MiniLM-L6-v2)")

        # When using local embeddings, ChromaDB handles embedding automatically
        # via its default embedding function — no explicit embeddings needed.
        self._collection = self._client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "ChromaDB collection '%s' ready (%d existing documents)",
            CHROMA_COLLECTION,
            self._collection.count(),
        )

    # ------------------------------------------------------------------
    # Embedding helpers (only used in OpenAI mode)
    # ------------------------------------------------------------------

    def _embed_texts_openai(self, texts: list[str]) -> list[list[float]]:
        """Call OpenAI embeddings API in batches."""
        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), _BATCH_SIZE):
            batch = texts[i : i + _BATCH_SIZE]
            resp = self._openai.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch,
                dimensions=EMBEDDING_DIMENSIONS,
            )
            all_embeddings.extend([d.embedding for d in resp.data])
        return all_embeddings

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def index_chunks(self, chunks: list[Chunk]) -> int:
        """
        Upsert chunks into ChromaDB. Generates embeddings locally or via
        OpenAI depending on configuration.

        Returns the number of chunks indexed.
        """
        if not chunks:
            logger.warning("No chunks to index")
            return 0

        ids = [c.chunk_id for c in chunks]
        texts = [c.text for c in chunks]
        metadatas = [
            {
                "format": c.format,
                "spec_version": c.spec_version,
                "commit_sha": c.commit_sha,
                "section_id": c.section_id,
                "rule_severity": c.rule_severity,
                "chunk_type": c.chunk_type,
                "has_tables": len(c.tables) > 0,
            }
            for c in chunks
        ]

        logger.info("Generating embeddings for %d chunks ...", len(chunks))

        batch = 500
        if self._use_openai:
            embeddings = self._embed_texts_openai(texts)
            for i in range(0, len(ids), batch):
                self._collection.upsert(
                    ids=ids[i : i + batch],
                    embeddings=embeddings[i : i + batch],
                    documents=texts[i : i + batch],
                    metadatas=metadatas[i : i + batch],
                )
        else:
            # Let ChromaDB compute embeddings locally via its default function
            for i in range(0, len(ids), batch):
                self._collection.upsert(
                    ids=ids[i : i + batch],
                    documents=texts[i : i + batch],
                    metadatas=metadatas[i : i + batch],
                )

        total = self._collection.count()
        logger.info("Index now contains %d documents", total)
        return len(chunks)

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def query(
        self,
        question: str,
        n_results: int = 5,
        where: Optional[dict] = None,
    ) -> dict:
        """
        Semantic search over the indexed spec chunks.

        Args:
            question: Natural language query.
            n_results: Number of results to return.
            where: Optional ChromaDB metadata filter, e.g.
                   {"format": "VCF", "rule_severity": "CRITICAL"}

        Returns:
            ChromaDB query result dict with ids, documents, metadatas, distances.
        """
        kwargs: dict = {
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
        }

        if self._use_openai:
            q_embedding = self._embed_texts_openai([question])[0]
            kwargs["query_embeddings"] = [q_embedding]
        else:
            # Let ChromaDB embed the query locally
            kwargs["query_texts"] = [question]

        if where:
            if len(where) > 1:
                kwargs["where"] = {"$and": [{k: v} for k, v in where.items()]}
            else:
                kwargs["where"] = where

        return self._collection.query(**kwargs)

    def collection_stats(self) -> dict:
        """Return basic statistics about the indexed collection."""
        return {
            "collection": CHROMA_COLLECTION,
            "total_documents": self._collection.count(),
            "persist_dir": str(CHROMA_DIR),
        }
