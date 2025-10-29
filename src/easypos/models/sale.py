from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from easypos.database.connection import DBConnection
import logging

logger = logging.getLogger(__name__)


@dataclass
class SaleModel():
    id: Optional[int] = None
    total_price: float = 0.0
    fully_printed: bool = False

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    """Represents a completed sale transaction."""

    def __post_init__(self):
        """Validate data after initialization."""
        if self.total_price < 0:
            raise ValueError("Total cannot be negative")


@dataclass
class SaleItemModel():
    sale_id: int
    item_id: int
    quantity: int
    item_price: float
    total_price: float

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SaleService:

    @classmethod
    def set_printed(cls, sale_id):
        with DBConnection() as db:
            db.execute(
                "UPDATE sales SET fully_printed = 1 WHERE id = ?", (sale_id,))
            return True

    @classmethod
    def make_sale(cls, sale):
    
        with DBConnection() as db:
            db.execute("INSERT INTO sales (total_price) VALUES (?)", (sale.total_price,)
                       )

        return cls.get_sale_by_id(db.cursor.lastrowid)

    @classmethod
    def add_item_to_sale(cls, sale_item: SaleItemModel):
        with DBConnection() as db:
            db.execute("INSERT INTO sales_items (sale_id, item_id, quantity, item_price, total_price) VALUES (?, ?, ?, ?, ?)",
                       (sale_item.sale_id, sale_item.item_id,
                        sale_item.quantity, sale_item.item_price, sale_item.total_price)
                       )
            return True

    @classmethod
    def delete_sale(cls, sale_id):
        with DBConnection() as db:
            db.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
            return True

    @classmethod
    def get_sales(cls) -> list[SaleModel]:
        with DBConnection() as db:
            db.execute("SELECT * FROM sales")
            return [SaleModel(**row) for row in db.fetchall()]

    @classmethod
    def get_sale_by_id(cls, sale_id: int) -> SaleModel:
        with DBConnection() as db:
            db.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
            row = db.fetchone()
            if row:
                return SaleModel(**row)
            else:
                raise ValueError(f"Sale with ID {sale_id} not found")
