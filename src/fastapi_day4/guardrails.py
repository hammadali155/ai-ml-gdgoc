from __future__ import annotations

from statistics import mean

from fastapi_day4.settings import get_settings


def is_query_too_vague(question: str) -> bool:
    stripped = question.strip().lower()

    vague_queries = {
        "tell me",
        "explain",
        "what is this",
        "help",
        "answer this",
        "maloomat do",
    }

    if stripped in vague_queries:
        return True

    if len(stripped.split()) <= 1:
        return True

    return False


def compute_confidence(results: list[dict]) -> dict:
    if not results:
        return {
            "top_score": 0.0,
            "avg_score": 0.0,
            "result_count": 0,
        }

    scores = [item["score"] for item in results]
    return {
        "top_score": max(scores),
        "avg_score": mean(scores),
        "result_count": len(results),
    }


def choose_rag_action(question: str, results: list[dict]) -> dict:
    settings = get_settings()
    confidence = compute_confidence(results)

    if settings.enable_clarify_behavior and is_query_too_vague(question):
        return {
            "action": "clarify",
            "reason": "Question is too vague or underspecified.",
            "confidence": confidence,
        }

    if settings.enable_refuse_behavior:
        if confidence["result_count"] < settings.min_results_for_answer:
            return {
                "action": "refuse",
                "reason": "Not enough supporting results were retrieved.",
                "confidence": confidence,
            }

        if confidence["top_score"] < settings.min_top_score_for_answer:
            return {
                "action": "refuse",
                "reason": "Top retrieval score is too weak.",
                "confidence": confidence,
            }

        if confidence["avg_score"] < settings.min_avg_score_for_answer:
            return {
                "action": "refuse",
                "reason": "Average retrieval confidence is too weak.",
                "confidence": confidence,
            }

    return {
        "action": "answer",
        "reason": "Retrieved context is sufficient for answer generation.",
        "confidence": confidence,
    }
