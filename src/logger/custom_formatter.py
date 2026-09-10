import logging


class CustomFormatter(logging.Formatter):
    grey = '\x1b[0;20m'
    yellow = '\x1b[33;20m'
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    green = '\x1b[1;32m'
    reset = '\x1b[0m'
    format = '%(asctime)s - %(levelname)s - %(message)s'

    FORMATS = {
        logging.DEBUG: green + format + reset + '\r',
        logging.INFO: grey + format + reset + '\r',
        logging.WARNING: yellow + format + reset + '\r',
        logging.ERROR: red + format + reset + '\r',
        logging.CRITICAL: bold_red + format + reset + '\r'
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
