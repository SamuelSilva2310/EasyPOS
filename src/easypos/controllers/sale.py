from easypos.models.sale import SaleModel, SaleService
from easypos.models.item import ItemService
from easypos.models.ticket import TicketModel, TicketService
from easypos.printer.easy_printer import EasyPrinter

import traceback
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SaleController():

    def __init__(self, ticket_queue, printer_connection_type):
        self.ticket_queue = ticket_queue
        self.printer = EasyPrinter(printer_connection_type)
        logger.info("Initialized SaleController")

    def make_sale(self, item_id, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be positive")
    
        
        item = ItemService.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")


        item_price = item.price
        total_price = item_price * quantity 
        sale = SaleModel(item_id=item_id, quantity=quantity, total_price=total_price)

        logger.info(f"New sale: {sale}")
    
        sale = SaleService.add_sale(sale)
        self.print_tickets(item, sale)


    def print_tickets(self, item, sale):

        logger.info(f"Printing tickets for sale {sale.id}")
        status = True
        for i in range(1, sale.quantity+1):

            try:
                logger.info(f"Printing ticket #{i}/{sale.quantity}")
                
                current_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                description = f"#{sale.id}\n{current_date}"
                ticket = TicketModel(sale_id=sale.id, name=item.name, icon=item.icon, description=description, item_id=item.id)
                ticket_id = TicketService.add_ticket(ticket)

                self.ticket_queue.put(ticket)
                logger.info(f"Ticket {ticket_id} added to queue")

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