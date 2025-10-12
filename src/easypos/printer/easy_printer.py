
from easypos.models.ticket import TicketModel
from easypos.printer.fake_printer import FakePrinter
from escpos.printer import Usb, Network
from easypos.printer.styles import TicketStyles
from easypos.utils import utils
from easypos.settings import APP_SETTINGS
from PIL import Image
import traceback
import os
import time

import logging
logger = logging.getLogger(__name__)



# Custom exception for clarity
class PrinterConnectionError(Exception):
    pass


class EasyPrinter:
    def __init__(self, printer_connection_type, connection_args={}):
        
        self.is_busy = False

        try:
            logger.info(f"Connecting to printer (type={printer_connection_type})")
            if printer_connection_type == "usb":
                self.printer = Usb(**connection_args)
            elif printer_connection_type == "fake":
                self.printer = FakePrinter(connection_args)
            elif printer_connection_type == "network":
                self.printer = Network(**connection_args)
            else:
                raise ValueError(f"Invalid printer connection type: {printer_connection_type}")

            #is_online = self._check_connection()

            # if not is_online:
            #     raise PrinterConnectionError(
            #         f"Could not connect to printer (type={printer_connection_type})"
            #     )

               
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
        self.printer.set(**TicketStyles.STYLE_HEADER_TITLE)
        self.printer.text(title)

    def _print_info(self, description):
        self.printer.set(**TicketStyles.STYLE_INFO)
        self.printer.text(description)

    def _print_logo(self, image_path):
        path = os.path.join(APP_SETTINGS.get("images_directory"), image_path)

        image = utils.load_image(path, TicketStyles.ICON_IMAGE_WIDTH, TicketStyles.LOGO_SCALE_FACTOR)
        image.crop(image.getbbox())
        image = utils.prepare_escpos_image(image)
        self.printer.image(image, center=True)

    def _print_icon(self, icon_path):
        path = os.path.join(APP_SETTINGS.get("images_directory"), 'products', icon_path)
        image = utils.load_image(path, TicketStyles.ICON_IMAGE_WIDTH, TicketStyles.ICON_IMAGE_SCALE_FACTOR)
        logger.info(f"Image size: {image.size}")
        image = utils.prepare_escpos_image(image)
        self.printer.image(image, center=True)
        

    def _print_spacer(self, lines=1):
        for _ in range(lines):
            self.printer.textln()
    

    def print_ticket(self, ticket: TicketModel):
        self.is_busy = True
        logger.info(f"Printing ticket {ticket}")
        try:
            self._print_logo("logo.png")
            self._print_title(ticket.name)
            self._print_spacer(2)
            self._print_icon(ticket.icon)
            self._print_spacer(4)
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


