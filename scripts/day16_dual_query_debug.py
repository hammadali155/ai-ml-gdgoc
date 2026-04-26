from __future__ import annotations

from fastapi_day4.retrieval import dual_query_search


def main() -> None:
    queries = [
        "qdrant kia karta he",
        "docker compose kia krta he",
        "mujhe retrieval ka jawab do",
    ]

    for query in queries:
        result = dual_query_search(query, limit=3)
        print("=" * 70)
        print(f"Original Query:   {result['original_query']}")
        print(f"Normalized Query: {result['normalized_query']}")
        print("-" * 70)
        for idx, item in enumerate(result["results"], start=1):
            print(
                {
                    "rank": idx,
                    "score": item["score"],
                    "chunk_id": item["chunk_id"],
                    "title": item["title"],
                    "text": item["text"],
                }
            )


if __name__ == "__main__":
    main()
