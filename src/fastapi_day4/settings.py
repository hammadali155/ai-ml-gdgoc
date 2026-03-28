from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration object.
    Values are loaded from:
    1) environment variables
    2) .env file (for local development)
    Strong typing + validation prevents silent misconfiguration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="FastAPI App", validation_alias="APP_NAME")
    environment: str = Field(default="dev", validation_alias="ENVIRONMENT")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    host: str = Field(default="127.0.0.1", validation_alias="HOST")
    port: int = Field(default=8000, validation_alias="PORT")

    api_key: str = Field(..., validation_alias="API_KEY")
    database_url: str = Field(..., validation_alias="DATABASE_URL")
    qdrant_url: str = Field(..., validation_alias="QDRANT_URL")

    # --- Day 15: RAG settings ---
    qdrant_collection_name: str = Field(
        default="week2_day13_chunks", validation_alias="QDRANT_COLLECTION_NAME"
    )
    default_search_limit: int = Field(default=3)
    embedding_model_name: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    groq_api_key: str = Field(..., validation_alias="GROQ_API_KEY")
    groq_model_name: str = Field(
        default="llama-3.1-8b-instant", validation_alias="GROQ_MODEL"
    )

    # Comma-separated list in .env -> parsed into list[str] using custom logic
    allowed_origins_raw: str = Field(default="", validation_alias="ALLOWED_ORIGINS")

    @property
    def allowed_origins(self) -> List[str]:
        raw = self.allowed_origins_raw.strip()
        if not raw:
            return []
        return [x.strip() for x in raw.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    # Cached so Settings is created once.
    return Settings()
