from easypos.models.sale import SaleModel, SaleService, SaleItemModel
from easypos.models.item import ItemService
from easypos.models.ticket import TicketModel, TicketService
from easypos.printer.printer_manager import PrinterManager

import traceback
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SaleController():

    def __init__(self, ticket_queue):
        self.ticket_queue = ticket_queue
        self.printer = PrinterManager.get_instance()
        logger.info("Initialized SaleController")

    def make_sale(self, cart_items):

        if not cart_items:
            raise ValueError("No items in to sell")

        self.printer.open_cashdrawer(5)
        
        total = 0
        for item_id, data in cart_items.items():
            item = data["item"]
            quantity = data["quantity"]

            item_price = item.price
            total_price = item_price * quantity 
            total += total_price

        sale = SaleModel(total_price=total)
        logger.info(f"Creating sale: {sale}")
        sale = SaleService.make_sale(sale)
            
        # Process each item
        for item_id, data in cart_items.items():
            item = data["item"]
            quantity = data["quantity"]

            self._process_item(sale, data)


        self.print_tickets(cart_items, sale)

    def _process_item(self, sale, data):
        item = data["item"]
        quantity = data["quantity"]
        sale_item = SaleItemModel(sale_id=sale.id, item_id=item.id, quantity=quantity, item_price=item.price, total_price=item.price * quantity)
        SaleService.add_item_to_sale(sale_item)
        

    def print_tickets(self, cart_items, sale):

        logger.info(f"Printing tickets for sale {sale.id}")
        status = True
        for item_id, data in cart_items.items():
            item = data["item"]
            quantity = data["quantity"]
            logger.info(f"Creating {quantity} tickets for item {item.name}")
            for i in range(1, quantity+1):
                try:
                    logger.info(f"Creating ticket {i}/{quantity}")
                    current_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    #description = f"#{sale.id}\n{current_date}"
                    description = f"{current_date}"
                    ticket = TicketModel(sale_id=sale.id, name=item.name, icon=item.icon, description=description, item_id=item.id)
                    ticket = TicketService.add_ticket(ticket)

                    self.ticket_queue.put(ticket)
                    logger.info(f"Ticket {ticket.id} added to queue")

                except Exception as e:
                    logger.error(f"Failed to print ticket: {e}")
                    traceback.print_exc()
                    status = False
                
        if status:
            SaleService.set_printed(sale.id)
            logger.info(f"Sale {sale.id} printed successfully")
        
        return status

    def get_sales(self):
        return self.sales
    
    def open_cashdrawer(self, pin=2):
        self.printer.open_cashdrawer(pin)