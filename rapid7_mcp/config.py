from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="R7_",
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    console_url: str = "https://localhost:3780"
    username: str = "admin"
    password: str = "password"
    verify_ssl: bool = False

    # No R7_ prefix — override via validation_alias
    demo_mode: bool = Field(default=False, validation_alias="DEMO_MODE")


@lru_cache
def get_settings() -> Settings:
    return Settings()
