from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "GenAI RAG API"
    app_version: str = "0.1.0"
    environment: str = "development"


def get_settings() -> Settings:
    return Settings()