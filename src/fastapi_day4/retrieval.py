from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from fastapi_day4.settings import get_settings
from fastapi_day4.vector_store import get_qdrant_client


@lru_cache(maxsize=1)
def _get_embedding_model() -> SentenceTransformer:
    settings = get_settings()
    return SentenceTransformer(settings.embedding_model_name)


def search_chunks(query: str, limit: int | None = None) -> list[dict]:
    """Embed *query* and return the top-k matching chunks from Qdrant."""
    settings = get_settings()
    if limit is None:
        limit = settings.default_search_limit

    model = _get_embedding_model()
    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    client = get_qdrant_client()
    results = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True,
    )

    chunks: list[dict] = []
    for point in results.points:
        payload = point.payload or {}
        chunks.append(
            {
                "score": round(point.score, 4),
                "doc_id": payload.get("doc_id", ""),
                "chunk_id": payload.get("chunk_id", ""),
                "title": payload.get("title", ""),
                "language": payload.get("language", ""),
                "source": payload.get("source", ""),
                "chunk_index": payload.get("chunk_index", 0),
                "text": payload.get("text", ""),
            }
        )
    return chunks
