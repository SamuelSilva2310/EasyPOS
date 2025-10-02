from dataclasses import dataclass
from easypos.database.connection import DBConnection
from datetime import datetime
from typing import Optional

@dataclass
class TicketModel:
    item_id: int
    sale_id: int
    id: Optional[int] = None
    printed: bool = False

    name: str = ""
    icon: str = ""
    description: str = ""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TicketService:
    @classmethod
    def add_ticket(cls, ticket):
        with DBConnection() as db:
            db.execute("INSERT INTO tickets (sale_id, item_id, name, description, icon) VALUES (?, ?, ?, ?, ?)"
            , (ticket.sale_id, ticket.item_id, ticket.name, ticket.description, ticket.icon)
            )
            
        return cls.get_ticket_by_id(db.cursor.lastrowid)

    @classmethod
    def get_ticket_by_id(cls, ticket_id: int) -> TicketModel:
        with DBConnection() as db:
            db.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
            row = db.fetchone()
            if row:
                return TicketModel(id=row[0], item_id=row[1], sale_id=row[2], name=row[3], description=row[4], icon=row[5], printed=row[6])
            else:
                raise ValueError(f"Ticket with ID {ticket_id} not found")

    @classmethod
    def get_tickets(cls) -> list[TicketModel]:
        with DBConnection() as db:
            db.execute("SELECT * FROM tickets")
            return [TicketModel(id=row[0], item_id=row[1], sale_id=row[2], name=row[3], description=row[4], icon=row[5], printed=row[6]) for row in db.fetchall()]
    @classmethod
    def set_printed(cls, ticket_id):
        with DBConnection() as db:
            db.execute("UPDATE tickets SET printed = 1 WHERE id = ?", (ticket_id,))
            return True