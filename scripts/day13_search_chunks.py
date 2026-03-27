from __future__ import annotations

from sentence_transformers import SentenceTransformer

from fastapi_day4.vector_store import get_qdrant_client

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "week2_day13_chunks"


def get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def main() -> None:
    client = get_qdrant_client()
    model = get_model()

    query = "How does Qdrant help with semantic search?"
    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
        with_payload=True,
    )

    print(f"Query: {query}")
    print("-" * 60)
    for rank, point in enumerate(results.points, start=1):
        payload = point.payload or {}
        print(f"Rank {rank}")
        print(f"Score:    {point.score}")
        print(f"Doc ID:  {payload.get('doc_id')}")
        print(f"Chunk ID:{payload.get('chunk_id')}")
        print(f"Title:   {payload.get('title')}")
        print(f"Text:    {payload.get('text')}")
        print("-" * 60)


if __name__ == "__main__":
    main()
