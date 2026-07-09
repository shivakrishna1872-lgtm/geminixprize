from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


RuntimeEnvironment = Literal["development", "test", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ANTIGRAVITY_", extra="ignore")

    environment: RuntimeEnvironment = "development"
    version: str = "0.1.0"
    cors_allowed_origins: tuple[str, ...] = ("http://127.0.0.1:3000",)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
