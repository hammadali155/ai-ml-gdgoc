from __future__ import annotations

from typing import Any


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 20) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    step = chunk_size - overlap
    if step <= 0:
        raise ValueError("chunk_size must be greater than overlap")
    for start in range(0, len(words), step):
        end = start + chunk_size
        chunk_words = words[start:end]
        if not chunk_words:
            continue
        chunks.append(" ".join(chunk_words))
        if end >= len(words):
            break
    return chunks


def build_chunk_records(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for index, chunk in enumerate(chunks, start=1):
            records.append(
                {
                    "chunk_id": f"{doc['doc_id']}-chunk-{index:03d}",
                    "doc_id": doc["doc_id"],
                    "title": doc["title"],
                    "language": doc["language"],
                    "source": doc["source"],
                    "chunk_index": index,
                    "text": chunk,
                }
            )
    return records
