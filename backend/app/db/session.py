from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


def _prepare_sqlite_path(database_url: str) -> None:
    sqlite_prefix = "sqlite:///"
    if not database_url.startswith(sqlite_prefix):
        return

    raw_target = database_url[len(sqlite_prefix) :].split("?", 1)[0]
    if raw_target in ("", ":memory:"):
        return

    Path(raw_target).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


_prepare_sqlite_path(settings.database_url)


# SQLite requires this flag to allow DB access from multiple FastAPI threads.
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

# Engine manages connections to the configured database backend.
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)

# Session factory used per-request by dependency injection.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
