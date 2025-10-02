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



def main(args):

    logger.info("Starting EasyPOS...")

    # Initialize database
    init_db()

    # Shared queue
    ticket_queue = Queue()

    # Start consumer thread first
    consumer_thread = threading.Thread(
        target=start_consumer,
        args=(args.printer_connection_type, ticket_queue),
        daemon=True
    )
    consumer_thread.start()

    # Start the app (UI or CLI)
    app = EasyPOSApp(ticket_queue, args.printer_connection_type)
    app.run()   # This may block, which is okay because consumer is already running


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--printer-connection-type", type=str, default="fake")
    args = parser.parse_args()

    main(args)