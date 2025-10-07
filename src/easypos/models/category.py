from dataclasses import dataclass
from typing import Optional, List
from easypos.database.connection import DBConnection

from datetime import datetime


@dataclass
class CategoryModel:
    """Represents a product category in the POS system."""
    id: Optional[int] = None
    slug: str = ""
    label: str = ""
    icon: str = ""


class CategoryService:
    """Handles CRUD operations for categories."""

    @classmethod
    def add_category(cls, category: CategoryModel) -> CategoryModel:
        """Insert a new category into the database."""
        with DBConnection() as db:
            db.execute(
                "INSERT INTO categories (slug, label, icon) VALUES (?, ?, ?)",
                (category.slug, category.label, category.icon),
            )
            category.id = db.cursor.lastrowid
        return category

    @classmethod
    def get_all(cls) -> List[CategoryModel]:
        """Fetch all categories."""
        with DBConnection() as db:
            db.execute("SELECT id, slug, label, icon FROM categories")
            rows = db.fetchall()
            return [
                CategoryModel(id=row[0], slug=row[1], label=row[2], icon=row[3])
                for row in rows
            ]

    @classmethod
    def get_by_id(cls, category_id: int) -> CategoryModel:
        """Fetch a single category by ID."""
        with DBConnection() as db:
            db.execute("SELECT id, slug, label, icon FROM categories WHERE id = ?", (category_id,))
            row = db.fetchone()
            if row:
                return CategoryModel(id=row[0], slug=row[1], label=row[2], icon=row[3])
            raise ValueError(f"Category with ID {category_id} not found")

    @classmethod
    def update_category(cls, category: CategoryModel) -> None:
        """Update an existing category."""
        if category.id is None:
            raise ValueError("Category must have an ID to update.")
        with DBConnection() as db:
            db.execute(
                "UPDATE categories SET slug = ?, label = ?, icon = ? WHERE id = ?",
                (category.slug, category.label, category.icon, category.id),
            )

    @classmethod
    def delete_category(cls, category_id: int) -> None:
        """Delete a category by ID."""
        with DBConnection() as db:
            db.execute("DELETE FROM categories WHERE id = ?", (category_id,))