from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Keep the runtime SQLite file in the shared careportal_backend database folder.
REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SQLITE_DB_PATH = REPO_ROOT / "careportal_backend" / "src" / "database" / "careportal.db"


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

    @field_validator("database_url", mode="after")
    @classmethod
    def normalize_sqlite_database_url(cls, value: str) -> str:
        """Resolve relative SQLite paths from backend root instead of process cwd."""
        sqlite_prefix = "sqlite:///"
        if not value.startswith(sqlite_prefix):
            return value

        raw_target = value[len(sqlite_prefix) :]
        raw_path, separator, raw_query = raw_target.partition("?")

        if raw_path in ("", ":memory:") or raw_path.startswith("/"):
            return value

        normalized_path = (BACKEND_ROOT / raw_path).resolve().as_posix()
        return f"{sqlite_prefix}{normalized_path}{separator}{raw_query}" if separator else f"{sqlite_prefix}{normalized_path}"

    # Load values from .env file using CAREPORTAL_ prefix.
    model_config = SettingsConfigDict(env_file=BACKEND_ROOT / ".env", env_prefix="CAREPORTAL_")


# Create one shared settings object for the whole app.
settings = Settings()
