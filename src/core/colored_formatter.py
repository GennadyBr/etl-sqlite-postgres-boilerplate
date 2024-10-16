import logging
from logging.handlers import RotatingFileHandler


class ColoredFormatter(logging.Formatter):
    """Custom Color Formatter Class"""

    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',  # Magenta
    }
    RESET = '\033[0m'

    def format(self, record: logging.LogRecord) -> str:
        """Add color to log levels"""
        log_level = record.levelname
        if log_level in self.COLORS:
            record.colorlevel = (
                f'{self.COLORS[log_level]}{log_level}{self.RESET}'
            )
        else:
            record.colorlevel = log_level
        return super().format(record)


colored_format = (
    '%(asctime)s - %(colorlevel)s - %(name)s '
    '- %(module)s:(%(funcName)s):%(lineno)d - %(message)s'
)
colored_formatter = ColoredFormatter(fmt=colored_format)


def replace_formatter(logger: logging.Logger) -> None:
    """Replace root_formatter with colored_formatter"""
    for handler in logger.handlers:
        # no need color in log file
        if not isinstance(handler, RotatingFileHandler):
            handler.setFormatter(colored_formatter)


def replace_formatter_4_all_loggers() -> None:
    """Replace root_formatter with colored_formatter"""
    for logger in logging.root.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            replace_formatter(logger)
