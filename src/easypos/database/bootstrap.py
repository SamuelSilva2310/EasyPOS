from easypos.database.connection import DB_PATH
import sqlite3
from easypos.database.migrate import migrate
from easypos.database.seeder import import_data
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def init_db():
    """Ensure database exists and run migrations."""
    logger.info("Initializing database...")
    

    # Ensure the folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create DB file if not exists
    if not DB_PATH.exists():
        logger.info("Database not found, creating new database...")
        sqlite3.connect(DB_PATH).close()

    # Apply migrations
    migrate()

    logger.info("Database initialized successfully.")
    # Seed data
    import_data()