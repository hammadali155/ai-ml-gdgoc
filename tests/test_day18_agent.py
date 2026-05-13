from fastapi_day4.agent import build_agent_plan


def test_build_agent_plan_returns_steps() -> None:
    plan = build_agent_plan("What does Qdrant do?")
    assert isinstance(plan, list)
    assert len(plan) >= 4


def test_build_agent_plan_contains_retrieve_step() -> None:
    plan = build_agent_plan("What does Qdrant do?")
    assert any("Retrieve" in step or "retrieve" in step for step in plan)
