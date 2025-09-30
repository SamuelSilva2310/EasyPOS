from easypos.models.sale import SaleModel, SaleService
from easypos.models.item import ItemService
from easypos.models.ticket import TicketModel, TicketService
from easypos.printer import EasyPrinter

import traceback


class SaleController():

    def __init__(self):

        self.printer = EasyPrinter("fake")

    def make_sale(self, item_id, quantity):
        
        item = ItemService.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")

        item_price = item.price
        total_price = item_price * quantity 
        sale = SaleModel(item_id=item_id, quantity=quantity, total_price=total_price)

        print(f"[INFO] Adding sale to database {sale}")
        sale = SaleService.add_sale(sale)

        self.print_tickets(item, sale)


    def print_tickets(self, item, sale):

        status = True
        for i in range(sale.quantity):

            try:
                print(f"[INFO] Printing ticket #{i}")
                ticket = TicketModel(sale_id=sale.id, name=item.name, icon=item.icon, description=item.description, item_id=item.id)
                ticket_id = TicketService.add_ticket(ticket)

                self.printer.print_ticket(ticket)
                TicketService.set_printed(ticket.id)

            except Exception as e:
                print(f"Error printing ticket: {e}")
                traceback.print_exc()
                status = False
        
        if status:
            self.printer.open_cashdrawer()
            SaleService.set_printed(sale.id)
            print("[INFO] Sale printed successfully")
        
        return status

    def get_sales(self):
        return self.sales