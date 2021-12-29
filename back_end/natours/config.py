import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

p = Path(os.path.dirname(__file__)).resolve()


class Settings(BaseSettings):
    app_name: str = "Natours API"
    PORT: str
    FASTAPI_ENV: str
    USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE: str
    DATABASE_LOCAL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool
    MAIL_SSL: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool
    RESET_PASSWORD_REDIRECT: str

    class Config:
        env_file = p / ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()