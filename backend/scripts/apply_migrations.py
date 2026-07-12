from __future__ import annotations

from pathlib import Path

import psycopg
from dotenv import dotenv_values


ROOT_DIR = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = ROOT_DIR / "supabase" / "migrations"


def load_database_url() -> str:
    root_env = dotenv_values(ROOT_DIR / ".env")
    backend_env = dotenv_values(ROOT_DIR / "backend" / ".env")
    database_url = backend_env.get("DIRECT_URL") or root_env.get("DIRECT_URL")
    database_url = database_url or backend_env.get("DATABASE_URL") or root_env.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DIRECT_URL or DATABASE_URL must be configured to apply migrations")

    return database_url


def ensure_migrations_table(connection: psycopg.Connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            create table if not exists schema_migrations (
              version text primary key,
              applied_at timestamptz not null default now()
            )
            """
        )


def applied_versions(connection: psycopg.Connection) -> set[str]:
    with connection.cursor() as cursor:
        cursor.execute("select version from schema_migrations")
        return {row[0] for row in cursor.fetchall()}


def apply_migration(connection: psycopg.Connection, migration_path: Path) -> None:
    version = migration_path.stem
    sql = migration_path.read_text(encoding="utf-8")

    with connection.cursor() as cursor:
        cursor.execute(sql)
        cursor.execute(
            "insert into schema_migrations (version) values (%s)",
            (version,),
        )


def main() -> None:
    migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not migrations:
        raise RuntimeError(f"No migrations found in {MIGRATIONS_DIR}")

    database_url = load_database_url()

    with psycopg.connect(database_url, autocommit=False) as connection:
        ensure_migrations_table(connection)
        applied = applied_versions(connection)

        pending = [migration for migration in migrations if migration.stem not in applied]
        if not pending:
            print("No pending migrations.")
            return

        for migration in pending:
            apply_migration(connection, migration)
            print(f"Applied migration: {migration.name}")

        connection.commit()


if __name__ == "__main__":
    main()
