
from easypos.models.ticket import TicketModel
from easypos.printer.fake_printer import FakePrinter
from escpos.printer import Usb
from PIL import Image
import traceback
import os
import time

import logging
logger = logging.getLogger(__name__)

def get_usb_printer_info():
    return vendor_id, product_id

PRINTER_STYLE_TITLE = {
    "align": "center",
    "bold": True,
    "custom_size": True,
    "width": 2,
    "height": 2
}

PRINTER_STYLE_INFO = {
    "align": "center",
    "bold": False,
    "custom_size": True,
    "width": 1,
    "height": 1
}

# Custom exception for clarity
class PrinterConnectionError(Exception):
    pass


class EasyPrinter:
    def __init__(self, printer_connection_type, connection_args={}, ticket_width=203):
        self.ticket_width = ticket_width
        self.is_busy = False

        try:
            logger.info(f"Connecting to printer (type={printer_connection_type})")
            if printer_connection_type == "usb":
                self.printer = Usb(**connection_args)
            elif printer_connection_type == "fake":
                self.printer = FakePrinter(connection_args, ticket_width=self.ticket_width)
            else:
                raise ValueError(f"Invalid printer connection type: {printer_connection_type}")

            is_online = self._check_connection()

            if not is_online:
                raise PrinterConnectionError(
                    f"Could not connect to printer (type={printer_connection_type})"
                )

               
        except Exception as e:
            # Log the traceback for debugging
            #traceback.print_exc()
            # Raise a clear, custom error to stop execution
            raise PrinterConnectionError(
                f"Could not connect to printer (type={printer_connection_type}): {e}"
            ) from e
        
    def _check_connection(self):
        try:
            self.printer._raw(b'\x1b@')  # ESC @ = Initialize printer
            return True
        except Exception as e:
            return False

    def _print_title(self, title):
        self.printer.set(**PRINTER_STYLE_TITLE)
        self.printer.text(title)

    def _print_icon(self, icon_path):
        icon = Image.open(os.path.join("images", icon_path)).convert("1")
        max_width = self.ticket_width
        w_percent = (max_width / float(icon.size[0]))
        h_size = int((float(icon.size[1]) * float(w_percent)))
        icon = icon.resize((max_width, h_size))
        self.printer.image(icon, center=True)

    def _print_info(self, description):
        self.printer.set(**PRINTER_STYLE_INFO)
        self.printer.text(description)

    def print_ticket(self, ticket: TicketModel):
        self.is_busy = True
        logger.info(f"Printing ticket {ticket}")
        try:
            self._print_title(ticket.name)
            self.printer.textln()
            self._print_icon(ticket.icon)
            self.printer.textln()
            self._print_info(ticket.description)
            self.printer.cut()
        except Exception as e:
            traceback.print_exc()
            raise PrinterConnectionError(f"Error printing ticket: {e}") from e
        finally:
            self.is_busy = False

    def close(self):
        self.printer.close()

    def open_cashdrawer(self, pin=2):
        try:
            self.printer.cashdraw(pin)
        except Exception as e:
            traceback.print_exc()
            raise PrinterConnectionError(f"Could not open cash drawer: {e}") from e


