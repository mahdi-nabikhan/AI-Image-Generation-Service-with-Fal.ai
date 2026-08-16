from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env file.

    Attributes:
        SQLALCHEMY_DATABASE_URL: SQLAlchemy database connection URL.
    """
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./app.db"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env"
    )



setting = Settings()