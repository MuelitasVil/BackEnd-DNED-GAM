from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env',
        env_file_encoding='utf-8'
    )

    DNED_ORGANIZATION: str
    JOBS_DB_HOST: str
    JOBS_DB_PORT: str
    JOBS_DB_USER: str
    JOBS_DB_PASSWORD: str
    JOBS_DB_NAME: str


# Instantiate the settings
settings = Settings()
