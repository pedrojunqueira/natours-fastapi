from functools import lru_cache
import os
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

    class Config:
        env_file = p / ".env"

@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
