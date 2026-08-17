from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Keep the runtime SQLite file in the shared careportal_backend database folder.
DEFAULT_SQLITE_DB_PATH = Path(__file__).resolve().parents[2] / "careportal_backend" / "src" / "database" / "careportal.db"


class Settings(BaseSettings):
    # Basic app info used by FastAPI docs.
    app_name: str = "CarePortal API"
    app_version: str = "0.1.0"
    debug: bool = True

    # JWT settings for login tokens.
    jwt_secret_key: str = "dev-secret-change-before-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 1440

    # Database connection string used by SQLAlchemy.
    database_url: str = f"sqlite:///{DEFAULT_SQLITE_DB_PATH.as_posix()}"

    # Load values from .env file using CAREPORTAL_ prefix.
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CAREPORTAL_")


# Create one shared settings object for the whole app.
settings = Settings()
