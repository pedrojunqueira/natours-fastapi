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
    CORS_ORIGINS: list = [
        "http://0.0.0.0:8084",
        "http://0.0.0.0:8084",
        "http://localhost:8084",
        "http://front-end:8084",
        "http://0.0.0.0:8085",
        "http://localhost:8085",
        "http://127.0.0.1:8085",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://194.195.124.103:8084",
        "http://194.195.124.103:80",
        "*",
    ]
    AZURE_TENANT_ID: str
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_SUBSCRIPTION_ID: str
    AZURE_STORAGE_ACCOUNT: str
    AZURE_VAULT_ACCOUNT: str
    AZURE_STORAGE_KEY_NAME: str
    AZURE_BLOG_USER_IMAGE_PATH: str
    AZURE_APP_BLOB_NAME: str
    GMAIL_USERNAME: str
    GMAIL_PASSWORD: str
    GMAIL_FROM: str
    GMAIL_PORT: int
    GMAIL_SERVER: str
    GMAIL_TLS: str
    GMAIL_SSL: str

    class Config:
        env_file = p / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
