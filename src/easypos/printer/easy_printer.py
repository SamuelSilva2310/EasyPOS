
from easypos.models.ticket import TicketModel
from escpos.printer import Usb
from PIL import Image
import traceback
import os
import time

vendor_id = 1046   # 0x0416
product_id = 20497  # 0x5001


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
    def __init__(self, printer_connection_type, ticket_width=203):
        self.ticket_width = ticket_width
        self.is_busy = False

        try:
            if printer_connection_type == "usb":
                vendor_id, product_id = get_usb_printer_info()
                self.printer = Usb(vendor_id, product_id)
            elif printer_connection_type == "fake":
                self.printer = FakePrinter(ticket_width=self.ticket_width)
            else:
                raise ValueError(f"Invalid printer connection type: {printer_connection_type}")

            # is_online = self.printer.paper_status()
            # print(f"Printer is online: {is_online}")
            # if not is_online:
            #     raise PrinterConnectionError(
            #         f"Printer is not online (type={printer_connection_type})"
            #     )
        except Exception as e:
            # Log the traceback for debugging
            #traceback.print_exc()
            # Raise a clear, custom error to stop execution
            raise PrinterConnectionError(
                f"Could not connect to printer (type={printer_connection_type}): {e}"
            ) from e

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
        try:
            #self._print_title(ticket.name)
            #self.printer.textln()
            #self._print_icon(ticket.icon)
            #self.printer.textln()
            self._print_info(ticket.description)
            self.printer.cut()
        except Exception as e:
            traceback.print_exc()
            raise PrinterConnectionError(f"Error printing ticket: {e}") from e
        finally:
            self.is_busy = False

    def open_cashdrawer(self, pin=2):
        try:
            self.printer.cashdraw(pin)
        except Exception as e:
            traceback.print_exc()
            raise PrinterConnectionError(f"Could not open cash drawer: {e}") from e


#### FakePrinter ###

from PIL import Image

class FakePrinter:
    def __init__(self, ticket_width=40):
        self.ticket_width = ticket_width  # characters
        self.logs = []  # optional, store output for tests

    def set(self, align="left", bold=False, width=1, height=1, **kwargs):
        self.align = align
        self.bold = bold
        self.width = width
        self.height = height
        # Simulate style info in console
        print(f"[SET] align={align}, bold={bold}, width={width}, height={height}")

    def _format_text(self, txt):
        # Apply bold simulation
        if self.bold:
            txt = txt.upper()
        # Center or left align
        if self.align == "center":
            txt = txt.center(self.ticket_width)
        return txt

    def text(self, txt):
        # Print text without newline
        formatted = self._format_text(txt)
        print(formatted, end="")
        self.logs.append(formatted)

    def textln(self, txt=""):
        # Print text with newline
        formatted = self._format_text(txt)
        print(formatted)
        self.logs.append(formatted)

    def image(self, img: Image.Image, center=False):
        # Simulate image with a placeholder box
        width, height = img.size
        lines = ["#" * min(width, self.ticket_width) for _ in range(min(height, 5))]
        if center:
            lines = [line.center(self.ticket_width) for line in lines]
        for line in lines:
            print(line)
            self.logs.append(line)

    def cut(self):
        print("-" * self.ticket_width)
        print("--- END OF TICKET ---".center(self.ticket_width))
        print("-" * self.ticket_width)

    def cashdraw(self, pin=2):
        print(f"[CASH DRAWER OPEN PIN {pin}]".center(self.ticket_width))

