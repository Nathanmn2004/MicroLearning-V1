from __future__ import annotations

from pathlib import Path

import psycopg
from dotenv import dotenv_values


ROOT_DIR = Path(__file__).resolve().parents[2]

EXPECTED_TABLES = {
    "schema_migrations",
    "subscribers",
    "books",
    "lessons",
    "lesson_quotes",
    "subscriptions",
    "payment_events",
    "deliveries",
    "delivery_parts",
}

REMOVED_TABLES = {
    "profiles",
    "book_pages",
    "book_chunks",
    "chunk_analyses",
    "chapter_analyses",
    "book_analyses",
}


def load_database_url() -> str:
    root_env = dotenv_values(ROOT_DIR / ".env")
    backend_env = dotenv_values(ROOT_DIR / "backend" / ".env")
    database_url = backend_env.get("DIRECT_URL") or root_env.get("DIRECT_URL")
    database_url = database_url or backend_env.get("DATABASE_URL") or root_env.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DIRECT_URL or DATABASE_URL must be configured")

    return database_url


def main() -> None:
    with psycopg.connect(load_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select table_name
                from information_schema.tables
                where table_schema = 'public'
                """
            )
            actual_tables = {row[0] for row in cursor.fetchall()}

    missing_tables = sorted(EXPECTED_TABLES - actual_tables)
    if missing_tables:
        raise RuntimeError(f"Missing tables: {', '.join(missing_tables)}")

    unexpected_tables = sorted(REMOVED_TABLES & actual_tables)
    if unexpected_tables:
        raise RuntimeError(f"Old tables still present: {', '.join(unexpected_tables)}")

    print(f"Schema verified: {len(EXPECTED_TABLES)} tables found.")


if __name__ == "__main__":
    main()
