from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IntegriNews API"
    database_url: str = Field(default="sqlite:///./integri_news.db", alias="INTEGRINEWS_DB_URL")
    model_path: Path = Field(
        default=Path(__file__).resolve().parents[1] / "model_assets" / "fakenewsdetector.h5",
        alias="INTEGRINEWS_MODEL_PATH",
    )
    tokenizer_path: Path = Field(
        default=Path(__file__).resolve().parents[1] / "model_assets" / "tokenizer.pickle",
        alias="INTEGRINEWS_TOKENIZER_PATH",
    )
    allowed_origins_raw: str = Field(
        default="http://localhost:5173",
        alias="INTEGRINEWS_ALLOWED_ORIGINS",
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
