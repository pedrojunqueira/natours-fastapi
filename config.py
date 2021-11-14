from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Natours API"
    PORT: str
    FASTAPI_ENV: str
    USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE: str
    DATABASE_LOCAL: str

    class Config:
        env_file = ".env"
