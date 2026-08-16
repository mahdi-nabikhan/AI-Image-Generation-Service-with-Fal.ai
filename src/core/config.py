from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env file.

    Attributes:
        SQLALCHEMY_DATABASE_URL: SQLAlchemy database connection URL.
    """
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sqlite.db"

    FAL_KEY: str
    WEBHOOK_URL: str 
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env"
    )



setting = Settings()
os.environ["FAL_KEY"] = setting.FAL_KEY