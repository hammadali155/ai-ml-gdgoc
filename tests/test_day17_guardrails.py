from fastapi_day4.guardrails import choose_rag_action, is_query_too_vague


def test_is_query_too_vague_for_single_word() -> None:
    assert is_query_too_vague("help") is True


def test_choose_rag_action_returns_refuse_for_empty_results() -> None:
    decision = choose_rag_action("what is this", [])
    assert decision["action"] in {"clarify", "refuse"}


def test_choose_rag_action_returns_answer_for_strong_results() -> None:
    results = [
        {"score": 0.90, "chunk_id": "c1"},
        {"score": 0.82, "chunk_id": "c2"},
        {"score": 0.80, "chunk_id": "c3"},
    ]
    decision = choose_rag_action("What does Qdrant do?", results)
    assert decision["action"] == "answer"
