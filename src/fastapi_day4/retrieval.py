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


def merge_results(result_sets: list[list[dict]], final_limit: int) -> list[dict]:
    best_by_chunk_id: dict[str, dict] = {}

    for result_set in result_sets:
        for item in result_set:
            chunk_id = item["chunk_id"]
            if chunk_id not in best_by_chunk_id:
                best_by_chunk_id[chunk_id] = item
            else:
                if item["score"] > best_by_chunk_id[chunk_id]["score"]:
                    best_by_chunk_id[chunk_id] = item

    merged = list(best_by_chunk_id.values())
    merged.sort(key=lambda x: x["score"], reverse=True)
    return merged[:final_limit]


def dual_query_search(query: str, limit: int) -> dict:
    settings = get_settings()
    original_query = query.strip()

    from fastapi_day4.normalization import normalize_roman_urdu

    normalized_query = normalize_roman_urdu(query)

    original_results = search_chunks(original_query, limit)
    normalized_results = search_chunks(normalized_query, limit)

    merged_results = merge_results(
        [original_results, normalized_results],
        final_limit=settings.merged_search_limit,
    )

    return {
        "original_query": original_query,
        "normalized_query": normalized_query,
        "results": merged_results,
    }
