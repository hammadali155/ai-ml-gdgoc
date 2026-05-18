from __future__ import annotations

from sqlalchemy.orm import Session

from fastapi_day4.models import RagLog


def create_rag_log(
    db: Session,
    *,
    question: str,
    normalized_query: str,
    action: str,
    reason: str,
    answer: str,
    top_score: float,
    avg_score: float,
    result_count: int,
) -> RagLog:
    log = RagLog(
        question=question,
        normalized_query=normalized_query,
        action=action,
        reason=reason,
        answer=answer,
        top_score=top_score,
        avg_score=avg_score,
        result_count=result_count,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
