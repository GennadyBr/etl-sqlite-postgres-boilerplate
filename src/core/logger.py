"""Logger"""

import logging.config

import yaml

from src.core.colored_formatter import replace_formatter_4_all_loggers
from src.core.config import log_settings

with open(log_settings.log_config_filename, 'r') as file:
    logger_config = yaml.safe_load(file)
    logger_config['handlers']['file_rotation_handler'][
        'filename'
    ] = log_settings.log_rotation_filename
    logging.config.dictConfig(logger_config)

logger = logging.getLogger()

# Replace root_formatter with colored_formatter
replace_formatter_4_all_loggers()
