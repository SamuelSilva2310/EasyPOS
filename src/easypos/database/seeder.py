# easypos/database/seeder.py
import json
from pathlib import Path
from easypos.database.connection import DBConnection
import logging

logger = logging.getLogger(__name__)

DATA_PATH = Path("db/data.json")


def import_data(filepath=DATA_PATH):
    """
    Import and sync data from a JSON file into the database.
    If filepath != DATA_PATH, compares the two and updates DATA_PATH if content differs.
    """
    filepath = Path(filepath)

    # --- Step 1: Validate ---
    if not filepath.exists():
        logger.error(f"Data file not found: {filepath}")
        return

    if not _is_valid_json(filepath):
        logger.error(f"Invalid JSON structure in {filepath}")
        return

    # --- Step 2: Detect differences with the original data file ---
    if filepath != DATA_PATH:
        if not DATA_PATH.exists():
            logger.info(f"No original data file found at {DATA_PATH}, creating one.")
            _copy_file(filepath, DATA_PATH)
        else:
            if not _files_match(filepath, DATA_PATH):
                logger.info("Changes detected — updating original data file...")
                _copy_file(filepath, DATA_PATH)
            else:
                logger.info("No changes detected between files.")

    # --- Step 3: Seed database ---
    logger.info("Seeding database...")
    seed_categories(DATA_PATH)
    seed_items(DATA_PATH)
    logger.info("Seeding complete.")


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def _is_valid_json(filepath: Path) -> bool:
    """Check if a file contains valid JSON with required keys."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return False
        if not all(k in data for k in ("categories", "items")):
            return False
        if not isinstance(data["categories"], list) or not isinstance(data["items"], list):
            return False
        return True
    except Exception as e:
        logger.error(f"JSON validation failed: {e}")
        return False


def _files_match(file1: Path, file2: Path) -> bool:
    """Compare two JSON files by content (ignores formatting/whitespace)."""
    try:
        with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        return data1 == data2
    except Exception as e:
        logger.warning(f"Error comparing files: {e}")
        return False


def _copy_file(src: Path, dst: Path):
    """Safely overwrite destination file with source content."""
    try:
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Copied {src} → {dst}")
    except Exception as e:
        logger.error(f"Failed to copy {src} to {dst}: {e}")


# -------------------------------------------------------------------
# Seeding Logic
# -------------------------------------------------------------------
def seed_categories(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    with DBConnection() as db:
        for category in data.get("categories", []):
            slug = category["slug"]
            db.execute("SELECT id, label, icon FROM categories WHERE slug = ?", (slug,))
            row = db.fetchone()

            if row is None:
                logger.info(f"Adding new category: {slug}")
                db.execute(
                    "INSERT INTO categories (slug, label, icon) VALUES (?, ?, ?)",
                    (slug, category["label"], category["icon"]),
                )
            else:
                _, current_label, current_icon = row
                if current_label != category["label"] or current_icon != category["icon"]:
                    logger.info(f"Updating category: {slug}")
                    db.execute(
                        "UPDATE categories SET label = ?, icon = ? WHERE slug = ?",
                        (category["label"], category["icon"], slug),
                    )


def seed_items(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    with DBConnection() as db:
        for item in data.get("items", []):
            name = item["name"]
            db.execute(
                "SELECT id, price, icon, category_id FROM items WHERE name = ?",
                (name,),
            )
            row = db.fetchone()

            if row is None:
                logger.info(f"Adding new item: {name}")
                db.execute(
                    "INSERT INTO items (name, price, icon, category_id) VALUES (?, ?, ?, ?)",
                    (name, item["price"], item["icon"], item["category_id"]),
                )
            else:
                _, current_price, current_icon, current_category = row
                if (
                    float(current_price) != float(item["price"])
                    or current_icon != item["icon"]
                    or current_category != item["category_id"]
                ):
                    logger.info(f"Updating item: {name}")
                    db.execute(
                        """
                        UPDATE items 
                        SET price = ?, icon = ?, category_id = ?
                        WHERE name = ?
                        """,
                        (item["price"], item["icon"], item["category_id"], name),
                    )