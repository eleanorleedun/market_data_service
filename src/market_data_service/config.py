from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "market-data-service"
    environment: str = "development"

    market_symbol: str = "AAPL"
    stale_after_seconds: float = 10.0

    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_prefix="MD_",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
