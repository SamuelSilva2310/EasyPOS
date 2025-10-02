import sqlite3
from pathlib import Path
from easypos.config.db_config import DB_CONFIG
from easypos.database.connection import DBConnection

import logging
logger = logging.getLogger(__name__)

DB_PATH = Path("data/easypos_database.db")
MIGRATIONS_PATH = Path("db/migrations")



def ensure_migrations_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)



def get_applied_migrations(conn):
    query = "SELECT filename FROM schema_migrations"
    conn.execute(query, params=())
    return {row[0] for row in conn.fetchall()}


def apply_migration(conn, filename, sql):
    logger.info(f"Applying migration: {filename}")
    conn.execute_script(sql)
    conn.execute("INSERT INTO schema_migrations (filename) VALUES (?)", (filename,))


def migrate():

    logger.info("Applying migrations...")

    with DBConnection() as db:
        ensure_migrations_table(db)
        applied = get_applied_migrations(db)

        # Ensure migration folder exists
        MIGRATIONS_PATH.mkdir(parents=True, exist_ok=True)

        # Sort migration files by name (001, 002, ...)
        for migration_file in sorted(MIGRATIONS_PATH.glob("*.sql")):
            if migration_file.name not in applied:
                with open(migration_file, "r", encoding="utf-8") as f:
                    sql = f.read()
                apply_migration(db, migration_file.name, sql)

