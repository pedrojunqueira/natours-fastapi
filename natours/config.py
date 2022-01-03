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
    USER_IMAGE_PATH: str
    CORS_ORIGINS: list = ['http://0.0.0.0:8084',
                          'http://0.0.0.0:8084',
                          'http://localhost:8084',
                          'http://front-end:8084',
                          'http://0.0.0.0:8085',
                          'http://localhost:8085',
                          'http://front-end:8085',
                          'http://127.0.0.1:8085',
                          "front-end:80",
                          "http://front-end:80",
                          "http://194.195.124.103:8084",
                          "*"]
    class Config:
        env_file = p / ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
