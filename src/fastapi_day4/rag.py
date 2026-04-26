from __future__ import annotations

from fastapi_day4.llm_client import generate_answer_from_prompt
from fastapi_day4.retrieval import dual_query_search


def build_context_block(results: list[dict]) -> str:
    """Format retrieved chunks into a numbered context block."""
    parts: list[str] = []
    for idx, item in enumerate(results, start=1):
        parts.append(
            f"[Source {idx}]\n"
            f"doc_id: {item['doc_id']}\n"
            f"chunk_id: {item['chunk_id']}\n"
            f"title: {item['title']}\n"
            f"text: {item['text']}\n"
        )
    return "\n".join(parts)


def build_rag_prompt(question: str, results: list[dict]) -> str:
    """Build a grounded RAG prompt from the question and retrieved context."""
    context = build_context_block(results)
    return f"""Answer the question using only the context below.

Question:
{question}

Context:
{context}

Rules:
- Use only the provided context.
- Do not invent facts.
- If the answer is not supported by the context, say that clearly.
- Mention supporting sources using the source numbers.""".strip()


def answer_with_rag(question: str, limit: int) -> dict:
    """Full RAG pipeline: retrieve → build prompt → generate answer."""
    retrieval_payload = dual_query_search(question, limit)
    results = retrieval_payload["results"]

    prompt = build_rag_prompt(question, results)
    answer = generate_answer_from_prompt(prompt)

    return {
        "question": question,
        "normalized_query": retrieval_payload["normalized_query"],
        "answer": answer,
        "sources": results,
    }
