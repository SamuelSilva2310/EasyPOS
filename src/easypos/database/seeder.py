# easypos/database/seeder.py
import json
from pathlib import Path
from easypos.database.connection import DBConnection

import logging
logger = logging.getLogger(__name__)

ITEMS_PATH = Path("db/items.json")

def seed_items():
    if not ITEMS_PATH.exists():
        logger.info("No items.json found, skipping seeding.")
        return

    with open(ITEMS_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    with DBConnection() as db:
        for item in items:
            # check if item exists by name
            db.execute("SELECT id FROM items WHERE name = ?", (item["name"],))
            row = db.fetchone()
            if row is None:
                logger.info(f"Seeding item: {item['name']}")
                db.execute(
                    "INSERT INTO items (name, price, icon, category) VALUES (?, ?, ?, ?)",
                    (item["name"], item["price"], item["icon"], item["category"]),
                )
            else:
                # optional: update price/stock if needed
                pass