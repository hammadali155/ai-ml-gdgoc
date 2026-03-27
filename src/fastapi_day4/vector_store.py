from __future__ import annotations

import os

from qdrant_client import QdrantClient, models

QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def recreate_collection(
    client: QdrantClient, collection_name: str, vector_size: int
) -> None:
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )
