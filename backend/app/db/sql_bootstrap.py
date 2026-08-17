from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine


SQL_SCRIPTS_DIR = Path(__file__).resolve().parents[3] / "careportal_backend" / "src" / "database"
INIT_SQL_PATH = SQL_SCRIPTS_DIR / "init.sql"
SEED_SQL_PATH = SQL_SCRIPTS_DIR / "insert_sample_data.sql"


def _executescript_sqlite(engine: Engine, script_text: str) -> None:
    raw_connection = engine.raw_connection()
    try:
        cursor = raw_connection.cursor()
        try:
            cursor.executescript(script_text)
        finally:
            cursor.close()
        raw_connection.commit()
    finally:
        raw_connection.close()


def bootstrap_database_from_scripts(engine: Engine) -> None:
    init_sql = INIT_SQL_PATH.read_text(encoding="utf-8")
    _executescript_sqlite(engine, init_sql)

    with engine.connect() as connection:
        user_count = connection.execute(text("SELECT COUNT(1) FROM users")).scalar_one()

    if user_count == 0:
        seed_sql = SEED_SQL_PATH.read_text(encoding="utf-8")
        _executescript_sqlite(engine, seed_sql)
