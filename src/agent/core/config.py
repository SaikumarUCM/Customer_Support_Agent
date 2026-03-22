from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ───────────────────────────────────────────────────────────────────
    app_env: Literal["development", "staging", "production"] = "development"
    log_level: str = "INFO"

    # ── LLM ───────────────────────────────────────────────────────────────────
    openai_api_key: str
    model_name: str = "gpt-4o-mini"
    model_temperature: float = 0.2

    # ── LangSmith ─────────────────────────────────────────────────────────────
    langchain_api_key: str = ""
    langchain_tracing_v2: bool = False
    langchain_project: str = "customer-support-agent"
    langchain_endpoint: str = "https://api.smith.langchain.com"

    # ── API Security ──────────────────────────────────────────────────────────
    api_key: str = "changeme-secret-key"

    # ── Postgres checkpointer (optional) ─────────────────────────────────────
    postgres_dsn: str = ""

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def tracing_enabled(self) -> bool:
        return self.langchain_tracing_v2 and bool(self.langchain_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
