from __future__ import annotations

import json
from pathlib import Path

from fastapi_day4.ingestion import build_chunk_records

DATA_FILE = Path("data/raw/day13_documents.json")
OUTPUT_FILE = Path("data/processed/day13_chunks.json")


def main() -> None:
    documents = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    chunk_records = build_chunk_records(documents)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(chunk_records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Documents: {len(documents)}")
    print(f"Chunks:    {len(chunk_records)}")
    print(f"Saved to:  {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
