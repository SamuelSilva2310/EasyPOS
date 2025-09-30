from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from easypos.database import DBConnection

@dataclass
class SaleModel():
    id: Optional[int] = None
    item_id: str = ""  # Item name (matching your schema)
    quantity: int = 0
    total_price: float = 0.0
    fully_printed: bool = False
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    """Represents a completed sale transaction."""
    def __post_init__(self):
        """Validate data after initialization."""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.total_price < 0:
            raise ValueError("Total cannot be negative")
        if not self.item_id:
            raise ValueError("Item Id cannot be empty")
    

class SaleService:

    @classmethod
    def set_printed(cls,sale_id):
        with DBConnection() as db:
            db.execute("UPDATE sales SET fully_printed = 1 WHERE id = ?", (sale_id,))
            return True

    @classmethod
    def add_sale(cls, sale):
        with DBConnection() as db:
            db.execute("INSERT INTO sales (item_id, quantity, total_price) VALUES (?, ?, ?)"
            , (sale.item_id, sale.quantity, sale.total_price)
            )
            
        
        return cls.get_sale_by_id(db.cursor.lastrowid)
    @classmethod
    def delete_sale(cls, sale_id):
        with DBConnection() as db:
            db.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
            return True

    @classmethod
    def get_sales(cls) -> list[SaleModel]:
        with DBConnection() as db:
            db.execute("SELECT * FROM sales")
            return [SaleModel(id=row[0], item_id=row[1], quantity=row[2], total_price=row[3]) for row in db.fetchall()]

    @classmethod
    def get_sale_by_id(cls, sale_id: int) -> SaleModel:
        with DBConnection() as db:
            db.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
            row = db.fetchone()
            if row:
                return SaleModel(id=row[0], item_id=row[1], quantity=row[2], total_price=row[3])
            else:
                raise ValueError(f"Sale with ID {sale_id} not found")