import threading
import time
from easypos.printer.printer_manager import PrinterManager
from easypos.models.ticket import TicketService

import logging
logger = logging.getLogger(__name__)

def start_consumer(queue):
    
    logger.info("Starting printer consumer...")
    printer = PrinterManager.get_instance()
    while True:
        ticket = queue.get()  # blocks until an item is available
        try:
            logger.info(f"Processing ticket {ticket.id}")
            printer.print_ticket(ticket)
            TicketService.set_printed(ticket.id)
            logger.info(f"Ticket {ticket.id} printed successfully")
        except Exception as e:
            logger.error(f"Failed to print ticket {ticket.id}: {e}")
            # Retry after a short delay
            time.sleep(2)
            queue.put(ticket)
        finally:
            queue.task_done()  # mark ticket as processed
