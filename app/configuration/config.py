# app/configuration/config.py
from pydantic import BaseSettings


class Config(BaseSettings):
    DNED_ORGANIZATION: str  # Aquí estamos cargando la URL de la organización

    class Config:
        env_file = ".env"


config = Config()
