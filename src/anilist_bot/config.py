from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    telegram_bot_token: SecretStr = Field(default=SecretStr(""), alias="TELEGRAM_BOT_TOKEN")
    app_env: str = Field(default="local", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    data_file: Path = Field(default=Path("data/anime_list.json"), alias="DATA_FILE")
    fallback_image_url: str = Field(
        default="https://placehold.co/800x1200/png?text=Anime",
        alias="FALLBACK_IMAGE_URL",
    )

    @property
    def token(self) -> str:
        return self.telegram_bot_token.get_secret_value().strip()

    def validate_ready(self) -> None:
        if not self.token:
            msg = "TELEGRAM_BOT_TOKEN is empty. Copy .env.example to .env and fill the token."
            raise RuntimeError(msg)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
