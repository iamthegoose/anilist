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
    data_file: Path = Field(default=Path("data/media_library.json"), alias="DATA_FILE")
    fallback_image_url: str = Field(
        default="https://placehold.co/800x1200/png?text=Media",
        alias="FALLBACK_IMAGE_URL",
    )
    webhook_base_url: str = Field(default="", alias="WEBHOOK_BASE_URL")
    webhook_path: str = Field(default="/telegram/webhook", alias="WEBHOOK_PATH")
    webhook_secret: SecretStr = Field(default=SecretStr(""), alias="WEBHOOK_SECRET")
    web_server_host: str = Field(default="0.0.0.0", alias="WEB_SERVER_HOST")
    web_server_port: int = Field(default=8080, alias="WEB_SERVER_PORT")

    @property
    def token(self) -> str:
        return self.telegram_bot_token.get_secret_value().strip()

    def validate_ready(self) -> None:
        if not self.token:
            msg = "TELEGRAM_BOT_TOKEN is empty. Copy .env.example to .env and fill the token."
            raise RuntimeError(msg)
        if not self.webhook_base_url.strip():
            msg = "WEBHOOK_BASE_URL is empty. Set your public HTTPS base URL in .env."
            raise RuntimeError(msg)
        if not self.webhook_path.startswith("/"):
            msg = "WEBHOOK_PATH must start with '/'."
            raise RuntimeError(msg)

    @property
    def webhook_url(self) -> str:
        return self.webhook_base_url.rstrip("/") + self.webhook_path

    @property
    def secret_token(self) -> str | None:
        value = self.webhook_secret.get_secret_value().strip()
        return value or None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
