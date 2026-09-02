from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GenAI RAG API"
    app_version: str = "0.1.0"
    environment: str = "development"

    model_version: str = "rag-model-v1"
    prompt_version: str = "prompt-v1"

    database_url: str = "sqlite+aiosqlite:///./genai.db"

    model_config = SettingsConfigDict(
        env_prefix="GENAI_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()