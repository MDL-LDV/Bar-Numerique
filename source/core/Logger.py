import logging
from typing import Literal

LoggingLevel = Literal[
    50, # logging.CRITICAL
    40, # logging.ERROR,
    30, # logging.WARNING
    20, # logging.INFO,
    10, # logging.DEBUG,
    0 #logging.NOTSET
]

class BarLogger:
    def __init__(self, name, level: LoggingLevel = logging.INFO, log_file='application.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        

        # Create handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Create formatters and add them to handlers
        formatter = logging.Formatter('[%(asctime)s] |%(name)s| - %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

