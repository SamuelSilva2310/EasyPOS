import sqlite3
import os
from pathlib import Path
from easypos.config.db_config import DB_CONFIG
from easypos.settings import APP_SETTINGS

# Database and schema paths
DB_PATH = Path(APP_SETTINGS.DB_PATH)
SCHEMA_PATH = Path("db/schema.sql")






class DBConnection:
    """SQLite database connection with context manager support."""

    def __init__(self):
        self._ensure_db_folder_exists()
        self._conn = sqlite3.connect(DB_PATH)
        self._conn.row_factory = sqlite3.Row  # Enable dict-like access
        self._cursor = self._conn.cursor()

    def _ensure_db_folder_exists(self):
        """Ensure the folder for the database exists."""
        if DB_PATH.parent and not DB_PATH.parent.exists():
            os.makedirs(DB_PATH.parent)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def execute_script(self, sql):
        self.cursor.executescript(sql)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()