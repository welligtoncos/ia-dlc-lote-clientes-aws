from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    celery_broker_url: str
    storage_path: str
    cache_url: str = "redis://localhost:6379/1"
    log_level: str = "INFO"


def carregar_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
