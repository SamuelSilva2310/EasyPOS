from dataclasses import dataclass
from easypos.database.connection import DBConnection
from typing import Optional


@dataclass
class ItemModel():
    """Represents a sellable item in the POS system."""
    id: Optional[int] = None
    name: str = ""
    price: float = 0.0
    icon: str = ""
    description: str = ""
    
    def __post_init__(self):
        """Validate data after initialization."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.name.strip():
            raise ValueError("Item name cannot be empty")


class ItemService:
    @classmethod
    def add_item(cls, item: ItemModel):
        with DBConnection() as db:
            db.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
            item.id = db.cursor.lastrowid

        return item
    @classmethod
    def get_items(cls) -> list[ItemModel]:
        with DBConnection() as db:
            db.execute("SELECT * FROM items")
            return [ItemModel(id=row[0], name=row[1], price=row[2], icon=row[3], description=row[4]) for row in db.fetchall()]
        
    @classmethod    
    def get_item_by_id(cls, item_id: int) -> ItemModel:
        with DBConnection() as db:
            db.execute("SELECT * FROM items WHERE id = ?", (item_id,))
            row = db.fetchone()
            if row:
                return ItemModel(id=row[0], name=row[1], price=row[2], icon=row[3], description=row[4])
            else:
                raise ValueError(f"Item with ID {item_id} not found")