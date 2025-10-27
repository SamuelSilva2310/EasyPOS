
from easypos.settings import APP_SETTINGS
import logging
from easypos.logger import setup_logging
setup_logging()
logger = logging.getLogger("easypos")

import threading
import argparse
from queue import Queue

from easypos.database.bootstrap import init_db
from easypos.app import EasyPOSApp
from easypos.printer.consumer import start_consumer
from easypos.printer.printer_manager import PrinterManager
import sys


def main(args):

    logger.info("Starting EasyPOS...")
    logger.info(f"RUNTIME_DIRECTORY: {APP_SETTINGS.RUNTIME_DIRECTORY}")


    # Load app settings
    printer_connection_type = APP_SETTINGS.get("printer_connection_type")
    printer_connection_args = APP_SETTINGS.get("printer_connection_args", {}).get(printer_connection_type)


    # Initialize database
    init_db()

    # Initialize printer
    printer = PrinterManager.get_instance()
    printer.connect(printer_connection_type, printer_connection_args)
    logger.info(f"Printer connected: {printer.status()}")

    # Shared queue
    ticket_queue = Queue()

    # Start consumer thread first
    consumer_thread = threading.Thread(
        target=start_consumer,
        args=(ticket_queue,),
        daemon=True
    )
    consumer_thread.start()
    # Start the app (UI or CLI)
    app = EasyPOSApp(ticket_queue)
    app.run()   # This may block, which is okay because consumer is already running


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--printer-connection-type", type=str, default="fake")
    args = parser.parse_args()

    main(args)