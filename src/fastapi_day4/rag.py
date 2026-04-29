from __future__ import annotations

from fastapi_day4.guardrails import choose_rag_action
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
    """Full RAG pipeline: retrieve -> build prompt -> generate answer."""
    retrieval_payload = dual_query_search(question, limit)
    results = retrieval_payload["results"]
    normalized_query = retrieval_payload["normalized_query"]

    decision = choose_rag_action(question, results)

    if decision["action"] == "clarify":
        return {
            "question": question,
            "normalized_query": normalized_query,
            "action": "clarify",
            "reason": decision["reason"],
            "answer": "Please clarify your question with more specific details.",
            "sources": results,
            "confidence": decision["confidence"],
        }

    if decision["action"] == "refuse":
        return {
            "question": question,
            "normalized_query": normalized_query,
            "action": "refuse",
            "reason": decision["reason"],
            "answer": "I do not have enough reliable context to answer that safely.",
            "sources": results,
            "confidence": decision["confidence"],
        }

    prompt = build_rag_prompt(question, results)
    answer = generate_answer_from_prompt(prompt)

    return {
        "question": question,
        "normalized_query": normalized_query,
        "action": "answer",
        "reason": decision["reason"],
        "answer": answer,
        "sources": results,
        "confidence": decision["confidence"],
    }
