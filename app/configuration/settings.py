from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / '.env',
        env_file_encoding='utf-8'
    )

    DNED_ORGANIZATION: str
    SECRET_KEY: str
    JOBS_DB_HOST: str
    JOBS_DB_PORT: str
    JOBS_DB_USER: str
    JOBS_DB_PASSWORD: str
    JOBS_DB_NAME: str


# Instantiate the settings
settings = Settings()
