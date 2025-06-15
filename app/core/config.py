import os
import json
from dotenv import load_dotenv
from typing import List, Optional, ClassVar, Type
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Base configuration class."""

    # General configuration
    APP_NAME: str = Field(default="MyShortsApp")
    DEBUG: bool = Field(default=True)
    ENVIRONMENT: str = Field(default="development")
    API_PREFIX: str = Field(default="/api")

    # Database configuration
    DB_HOST: str = Field(default="localhost")
    DB_PORT: str = Field(default="5432")
    DB_NAME: str = Field(default="name_db")
    DB_USER: str = Field(default="user")
    DB_PASSWORD: str = Field(default="password")

    # Secret key for JWT or session management
    SECRET_KEY: str = Field(default="secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    ALGORITHM: str = Field(default="HS256")

    # Auth settings
    USE_COOKIE_AUTH: bool = Field(default=False)

    # CORS - use validator-style fallback
    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # Optional API configurations
    API_BASE_URL: Optional[str] = Field(default="https://api.example.com")

    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentConfig(Settings):
    DEBUG: bool = True
    ENVIRONMENT: str = "development"


class ProductionConfig(Settings):
    DEBUG: bool = False
    ENVIRONMENT: str = "production"


class TestingConfig(Settings):
    TESTING: ClassVar[bool] = True
    DEBUG: bool = False
    ENVIRONMENT: str = "testing"


# Configuration map
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config() -> Type[Settings]:
    env = os.getenv("ENVIRONMENT", "development")
    return config_map.get(env, DevelopmentConfig)


settings = get_config()()
