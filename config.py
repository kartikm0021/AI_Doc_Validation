from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "FastAPI PostgreSQL App"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A simple FastAPI application with PostgreSQL integration"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 