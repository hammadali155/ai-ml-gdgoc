from fastapi_day4.normalization import normalize_roman_urdu


def test_normalize_roman_urdu_changes_common_forms() -> None:
    assert normalize_roman_urdu("qdrant kia karta he") == "qdrant kya karta hai"


def test_normalize_roman_urdu_keeps_clean_text_stable() -> None:
    assert normalize_roman_urdu("what does qdrant do") == "what does qdrant do"
