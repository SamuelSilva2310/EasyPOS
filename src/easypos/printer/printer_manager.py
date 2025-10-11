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
        self.connection_args = {}
        self.lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PrinterManager()
        return cls._instance

    def connect(self, connection_type="usb", connection_args=None):
        """Safely connect or reconnect to the printer."""
        if connection_args is None:
            connection_args = {}

        logger.info(f"Connecting to printer using {connection_type}...")

        with self.lock:
            # Always remember the requested connection info
            self.connection_type = connection_type
            self.connection_args = connection_args

            # Close any previous connection safely
            if self.printer:
                try:
                    # Some fake printers have close() without 'self'
                    close_fn = getattr(self.printer, "close", None)
                    if callable(close_fn):
                        try:
                            close_fn()
                        except TypeError:
                            close_fn(self.printer)
                except Exception as e:
                    logger.warning(f"Error closing previous printer: {e}")
                finally:
                    self.printer = None
                    self.connected = False

            # Try to connect
            try:
                printer = EasyPrinter(connection_type, connection_args)
                # Verify connection
                if hasattr(printer, "_check_connection"):
                    is_connected = printer._check_connection()
                else:
                    is_connected = True  # Assume connected if not checkable

                if not is_connected:
                    logger.warning("Printer _check_connection() returned False.")
                    self.connected = False
                    self.printer = None
                    return False

                self.printer = printer
                self.connected = True
                logger.info("Printer connected successfully.")
                return True

            except Exception as e:
                self.printer = None
                self.connected = False
                logger.error(f"Failed to connect to printer: {e}")
                return False

    def check_connection(self):
        """Check if the printer is still connected."""
        with self.lock:
            if not self.printer:
                self.connected = False
                return False

            try:
                is_connected = self.printer._check_connection()
                self.connected = bool(is_connected)
                if not self.connected:
                    logger.warning("Printer appears to be disconnected.")
                return self.connected
            except Exception as e:
                logger.warning(f"Printer check_connection() failed: {e}")
                self.connected = False
                self.printer = None
                return False

    def status(self):
        """Return real printer connection status without altering previous type."""
        self.check_connection()
        return {
            "connected": self.connected,
            "connection_type": self.connection_type,
        }
    
    def print_ticket(self, ticket):
        with self.lock:
            if not self.printer:
                raise PrinterConnectionError("Printer not connected.")
            return self.printer.print_ticket(ticket)
        
    def open_cashdrawer(self, pin=2):
        with self.lock:
            if not self.printer:
                raise PrinterConnectionError("Printer not connected.")
            return self.printer.open_cashdrawer(pin)