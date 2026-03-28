from __future__ import annotations

from pydantic import BaseModel, Field


class RagRequest(BaseModel):
    question: str = Field(min_length=1, description="The user question.")
    limit: int = Field(default=3, ge=1, le=10)


class RagSourceItem(BaseModel):
    score: float
    doc_id: str
    chunk_id: str
    title: str
    language: str
    source: str
    chunk_index: int
    text: str


class RagResponse(BaseModel):
    question: str
    answer: str
    sources: list[RagSourceItem]
