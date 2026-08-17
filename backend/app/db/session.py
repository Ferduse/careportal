from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


# SQLite requires this flag to allow DB access from multiple FastAPI threads.
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

# Engine manages connections to the configured database backend.
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)

# Session factory used per-request by dependency injection.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
