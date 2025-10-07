# easypos/database/seeder.py
import json
from pathlib import Path
from easypos.database.connection import DBConnection

import logging
logger = logging.getLogger(__name__)

DATA_PATH = Path("db/data.json")


def seed_categories():
    if not DATA_PATH.exists():
        logger.info(f"No {DATA_PATH} found, skipping seeding.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    with DBConnection() as db:
        for category in data["categories"]:
            # check if category exists by name
            db.execute("SELECT id FROM categories WHERE slug = ?", (category["slug"],))
            row = db.fetchone()
            if row is None:
                logger.info(f"Seeding category: {category['slug']}")
                db.execute(
                    "INSERT INTO categories (slug, label, icon) VALUES (?, ?, ?)",
                    (category["slug"], category["label"], category["icon"]),
                )
            else:
                # optional: update price/stock if needed
                pass

def seed_items():
    if not DATA_PATH.exists():
        logger.info(f"No {DATA_PATH} found, skipping seeding.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    with DBConnection() as db:
        for item in data["items"]:
            # check if item exists by name
            db.execute("SELECT id FROM items WHERE name = ?", (item["name"],))
            row = db.fetchone()
            if row is None:
                logger.info(f"Seeding item: {item['name']}")
                db.execute(
                    "INSERT INTO items (name, price, icon, category_id) VALUES (?, ?, ?, ?)",
                    (item["name"], item["price"], item["icon"], item["category_id"]),
                )
            else:
                # optional: update price/stock if needed
                pass