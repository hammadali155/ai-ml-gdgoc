from __future__ import annotations

from sqlalchemy import select

from fastapi_day4.db import SessionLocal
from fastapi_day4.models import AgentLog


def main() -> None:
    with SessionLocal() as session:
        stmt = select(AgentLog).order_by(AgentLog.created_at.desc()).limit(10)
        rows = session.execute(stmt).scalars().all()

        for row in rows:
            print("=" * 80)
            print(f"id: {row.id}")
            print(f"question: {row.question}")
            print(f"normalized_query: {row.normalized_query}")
            print(f"plan: {row.plan}")
            print(f"action: {row.action}")
            print(f"reason: {row.reason}")
            print(f"created_at: {row.created_at}")
            print(f"answer: {row.answer[:200]}")


if __name__ == "__main__":
    main()
