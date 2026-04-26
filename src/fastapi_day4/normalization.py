from __future__ import annotations

import re

ROMAN_URDU_REPLACEMENTS = {
    "kia": "kya",
    "kya": "kya",
    "kr": "kar",
    "krta": "karta",
    "krti": "karti",
    "krna": "karna",
    "he": "hai",
    "hy": "hai",
    "hn": "hain",
    "mje": "mujhe",
    "muje": "mujhe",
    "mjhe": "mujhe",
    "qdrnt": "qdrant",
    "retrival": "retrieval",
    "maloomat": "malumat",
    "javab": "jawab",
    "btado": "bata do",
    "btao": "batao",
}


def basic_cleanup(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_roman_urdu(text: str) -> str:
    cleaned = basic_cleanup(text)
    words = cleaned.split()

    normalized_words = []
    for word in words:
        normalized_words.append(ROMAN_URDU_REPLACEMENTS.get(word, word))

    normalized = " ".join(normalized_words)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized
