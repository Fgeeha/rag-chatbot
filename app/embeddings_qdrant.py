"""
Embeddings & Vector Store — Qdrant backend
"""

from __future__ import annotations
import os
from typing import List
from uuid import uuid4

from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient, models

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION = "docs"

_embedder = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={"device": "cpu"},
)
_DIM = _embedder._client.get_sentence_embedding_dimension()

_HOST = os.getenv("QDRANT_HOST", "localhost")
_PORT = int(os.getenv("QDRANT_PORT", 6333))
_client = QdrantClient(host=_HOST, port=_PORT)

if COLLECTION not in {c.name for c in _client.get_collections().collections}:
    _client.create_collection(
        collection_name=COLLECTION,
        vectors_config=models.VectorParams(
            size=_DIM,
            distance=models.Distance.COSINE,
        ),
    )


class VectorStore:
    def similarity_search_by_vector(
        self, vector: List[float], k: int = 5
    ) -> List[str]:
        if not vector:
            return []
        res = _client.search(COLLECTION, query_vector=vector, limit=k)
        return [p.payload.get("text", "") for p in res]

    def add_vectors(self, vectors: List[List[float]], docs: List[str]) -> None:
        if not vectors:
            return
        points = [
            models.PointStruct(id=str(uuid4()), vector=v, payload={"text": t})
            for v, t in zip(vectors, docs)
        ]
        _client.upsert(COLLECTION, points=points)


_vs = VectorStore()


def load_vector_store() -> VectorStore:
    return _vs


def embed_text(text: str) -> List[float]:
    return _embedder.embed_query(text)


def save_vectors(chunks: list[str]) -> None:
    if not chunks:
        return
    vecs = _embedder.embed_documents(chunks)
    _vs.add_vectors(vecs, chunks)
