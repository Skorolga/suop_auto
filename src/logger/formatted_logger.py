import logging
from src.logger.custom_formatter import CustomFormatter


class FormattedLogger:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._ch = logging.StreamHandler()
        self._ch.setLevel(logging.DEBUG)
        self._ch.setFormatter(CustomFormatter())
        self._logger.addHandler(self._ch)

    def log(self, level, msg, need_to_print=True):
        if need_to_print:
            self._logger.log(level, msg)

    def debug(self, msg, need_to_print=True):
        self.log(logging.DEBUG, msg, need_to_print)

    def info(self, msg, need_to_print=True):
        self.log(logging.INFO, msg, need_to_print)

    def warning(self, msg, need_to_print=True):
        self.log(logging.WARNING, msg, need_to_print)

    def error(self, msg, need_to_print=True):
        self.log(logging.ERROR, msg, need_to_print)

    def critical(self, msg, need_to_print=True):
        self.log(logging.CRITICAL, msg, need_to_print)


logger = FormattedLogger()
