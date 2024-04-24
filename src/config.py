import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ALGORITHM: str = os.getenv("ALGORITHM")
    SERVICE_HOST: str = os.getenv("SERVICE_HOST")
    SERVICE_PORT: int = os.getenv("SERVICE_PORT")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
