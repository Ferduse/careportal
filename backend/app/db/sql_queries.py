from functools import lru_cache
from pathlib import Path


QUERIES_SQL_PATH = Path(__file__).resolve().parents[3] / "careportal_backend" / "src" / "database" / "queries.sql"


def _parse_named_queries(text: str) -> dict[str, str]:
    queries: dict[str, str] = {}
    current_name: str | None = None
    buffer: list[str] = []

    for line in text.splitlines():
        if line.strip().startswith("-- name:"):
            if current_name is not None:
                queries[current_name] = "\n".join(buffer).strip()
            current_name = line.split(":", 1)[1].strip()
            buffer = []
            continue

        if current_name is not None:
            buffer.append(line)

    if current_name is not None:
        queries[current_name] = "\n".join(buffer).strip()

    return queries


@lru_cache(maxsize=1)
def _load_queries() -> dict[str, str]:
    content = QUERIES_SQL_PATH.read_text(encoding="utf-8")
    queries = _parse_named_queries(content)
    if not queries:
        raise ValueError(f"No named queries found in {QUERIES_SQL_PATH}")
    return queries


def get_sql_query(name: str) -> str:
    queries = _load_queries()
    if name not in queries:
        raise KeyError(f"Named query '{name}' was not found in {QUERIES_SQL_PATH}")
    return queries[name]
