from easypos.printer.easy_printer import EasyPrinter, PrinterConnectionError
import threading
import logging

logger = logging.getLogger(__name__)


class PrinterManager:
    _instance = None

    def __init__(self):
        self.printer = None
        self.connected = False
        self.connection_type = None
        self.lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PrinterManager()
        return cls._instance

    def connect(self, connection_type="usb", connection_args={}):
        """
        Connects to the printer. If already connected, safely closes the previous connection
        and reconnects using the new type.
        """
        with self.lock:
            # Close existing printer safely
            if self.printer is not None:
                try:
                    if hasattr(self.printer, "close"):
                        self.printer.close()
                except Exception as e:
                    # Log but ignore errors during closing
                    print(f"Warning: error closing previous printer: {e}")
                finally:
                    self.printer = None
                    self.connected = False

            # Try to create a new printer connection
            try:
                self.printer = EasyPrinter(connection_type, connection_args)
                self.connected = True
                self.connection_type = connection_type
                logger.info("Connected to printer")
            except PrinterConnectionError as e:
                self.connected = False
                self.printer = None
                logger.error(f"Error connecting to printer: {e}")
                

    def print_ticket(self, ticket):
        if not self.connected:
            raise PrinterConnectionError("Printer not connected")
        with self.lock:
            self.printer.print_ticket(ticket)

    def open_cashdrawer(self, pin=2):
        if not self.connected:
            raise PrinterConnectionError("Printer not connected")
        with self.lock:
            self.printer.open_cashdrawer(pin)

    def status(self):
        return {
            "connected": self.connected,
            "connection_type": self.connection_type,
        }