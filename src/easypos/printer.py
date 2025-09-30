
from easypos.models.ticket import TicketModel
from escpos.printer import Usb
from PIL import Image
import traceback
import os
vendor_id = 1046   # 0x0416
product_id = 20497  # 0x5001


printer = Usb(vendor_id, product_id)


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
class EasyPrinter():

    def __init__(self, printer_connection_type, ticket_width=203):
        
        self.ticket_width = ticket_width

        if printer_connection_type == "usb":
            vendor_id, product_id = get_usb_printer_info()
            self.printer = Usb(vendor_id, product_id)
        elif printer_connection_type == "fake":
            self.printer = FakePrinter()
        else:
            raise ValueError(f"Invalid printer connection type: {printer_connection_type}")


    def print_title(self, title):
        self.printer.set(**PRINTER_STYLE_TITLE)
        self.printer.text(title)
    
    def print_icon(self, icon_path):
        icon = Image.open(os.path.join("images", icon_path)).convert("1")  # 1-bit B/W for ESC/POS
        max_width = 203
        w_percent = (max_width / float(icon.size[0]))
        h_size = int((float(icon.size[1]) * float(w_percent)))
        icon = icon.resize((max_width, h_size))
        
        self.printer.image(icon, center=True)
    

    def print_info(self, description, value):
        self.printer.set(**PRINTER_STYLE_INFO)
        self.printer.text(description)
        self.printer.text(value)

    def print_ticket(self, ticket: TicketModel):
        
        try:
            self.print_title(ticket.name)
            self.printer.textln()

            self.print_icon(ticket.icon)
            self.printer.textln()

            self.print_info(ticket.description, f"#{ticket.id}")

            self.printer.cut()

        except Exception as e:
            print(f"[ERROR] Error printing ticket: {e}")
            traceback.print_exc()
        

    def open_cashdrawer(self):
        self.printer.cashdraw()



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

