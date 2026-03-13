"""
Module that config app from .env
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения или файла .env.
    """
    telegram_token: str = ... # type: ignore
    api_chat_url: str = ... # type: ignore
    embed_url: str = ... # type: ignore
    mongo_url: str = ... # type: ignore
    mongo_db_name: str = ... # type: ignore
    proxy_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

config: Settings = Settings()
