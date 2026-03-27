from __future__ import annotations

import json
import os
from pathlib import Path

from qdrant_client import models
from sentence_transformers import SentenceTransformer

from fastapi_day4.ingestion import build_chunk_records
from fastapi_day4.vector_store import get_qdrant_client, recreate_collection

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "week2_day13_chunks"
DATA_FILE = Path("data/raw/day13_documents.json")
HF_CACHE_DIR = Path(".cache/huggingface")


def load_documents() -> list[dict]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def get_model() -> SentenceTransformer:
    os.environ.setdefault("HF_HOME", str(HF_CACHE_DIR.resolve()))
    return SentenceTransformer(MODEL_NAME)


def main() -> None:
    documents = load_documents()
    chunk_records = build_chunk_records(documents)
    if not chunk_records:
        raise RuntimeError("No chunk records were created.")

    model = get_model()
    vectors = model.encode(
        [record["text"] for record in chunk_records],
        normalize_embeddings=True,
    ).tolist()

    vector_size = len(vectors[0])
    client = get_qdrant_client()
    recreate_collection(client, COLLECTION_NAME, vector_size)

    points = []
    for idx, (record, vector) in enumerate(
        zip(chunk_records, vectors, strict=True), start=1
    ):
        points.append(
            models.PointStruct(
                id=idx,
                vector=vector,
                payload=record,
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created:   {len(chunk_records)}")
    print(f"Collection ready: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()
