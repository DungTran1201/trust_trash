from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Trust Trash API"
    app_env: str = "local"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    database_url: str | None = None
    opensearch_url: str | None = None
    redis_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
