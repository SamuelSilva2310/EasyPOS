#### FakePrinter ###

from PIL import Image

class FakePrinter:
    def __init__(self, printer_connection_args=None, ticket_width=40):
        self.ticket_width = ticket_width  # characters
        self.logs = []  # keep text output for debugging/tests
        self.align = "left"
        self.bold = False
        self.width = 1
        self.height = 1

    def _raw(self, data):
        print(data.decode("utf-8"), end="")

    def _line(self, char="─"):
        return char * self.ticket_width

    def set(self, align="left", bold=False, width=1, height=1, **kwargs):
        self.align = align
        self.bold = bold
        self.width = width
        self.height = height

    def _format_text(self, txt):
        if self.bold:
            txt = txt.upper()
        if self.align == "center":
            txt = txt.center(self.ticket_width)
        elif self.align == "right":
            txt = txt.rjust(self.ticket_width)
        else:
            txt = txt.ljust(self.ticket_width)
        return txt

    def text(self, txt):
        formatted = self._format_text(txt)
        print(formatted, end="")
        self.logs.append(formatted)

    def textln(self, txt=""):
        formatted = self._format_text(txt)
        print(formatted)
        self.logs.append(formatted)

    def image(self, img: Image.Image, center=False):
        # ASCII placeholder for image
        placeholder = "[#### IMAGE ####]"
        if center:
            placeholder = placeholder.center(self.ticket_width)
        print(placeholder)
        self.logs.append(placeholder)

    def cut(self):
        border = self._line("=")
        print(border)
        print("----- END OF TICKET -----".center(self.ticket_width))
        print(border)

    def cashdraw(self, pin=2):
        msg = f"[CASH DRAWER OPEN PIN {pin}]".center(self.ticket_width)
        print(msg)
        self.logs.append(msg)

    def close():
        pass