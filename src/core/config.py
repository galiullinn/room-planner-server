from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = "Room Planner API"
    app_debug: bool = False
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:3000"]

    db_user: str
    db_pass: SecretStr
    db_host: str
    db_port: int
    db_name: str
    db_echo: bool = False

    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    s3_endpoint_url: str
    s3_access_key: SecretStr
    s3_secret_key: SecretStr
    s3_bucket_name: str
    s3_region: str = "us-east-1"

    @property
    def db_url(self) -> str:
        """Строка подключения к базе данных."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
