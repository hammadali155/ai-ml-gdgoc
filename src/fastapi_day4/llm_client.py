from __future__ import annotations

from groq import Groq

from fastapi_day4.settings import get_settings


def get_groq_client() -> Groq:
    settings = get_settings()
    return Groq(api_key=settings.groq_api_key)


def generate_answer_from_prompt(prompt: str) -> str:
    """Send a grounded prompt to Groq and return the model's answer."""
    settings = get_settings()
    client = get_groq_client()
    response = client.chat.completions.create(
        model=settings.groq_model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded assistant. "
                    "Answer only from the provided context. "
                    "If the context is insufficient, say so clearly."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
