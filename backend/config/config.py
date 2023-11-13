from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_USERNAME: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_DATABASE: Optional[str] = None

    SECRET_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file="./backend/.env")


config = Settings()