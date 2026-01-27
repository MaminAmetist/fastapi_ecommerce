from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Fastapi ecommerce"
    environment: Literal["development", "testing", "production"] = "development"
    database_url: str = Field(..., validation_alias="DATABASE_URL")
    secret_key: str = "super_insecure_default_key"
    yookassa_shop_id: str = Field(..., validation_alias="YOOKASSA_SHOP_ID")
    yookassa_secret_key: str = Field(..., validation_alias="YOOKASSA_SECRET_KEY")
    yookassa_return_url: str = "http://localhost:8000/"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
