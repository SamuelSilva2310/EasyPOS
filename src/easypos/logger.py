import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s",
        handlers=[
            RotatingFileHandler("easypos.log", maxBytes=5_000_000, backupCount=3),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("PIL").setLevel(logging.WARNING)  # silence noisy libs
    logging.debug("Logging initialized")