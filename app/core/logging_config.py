import logging
import colorlog
from logging.handlers import RotatingFileHandler
from .config import settings

# Add custom log level for success
SUCCESS_LEVEL = 25  # Between INFO (20) and WARNING (30)
logging.addLevelName(SUCCESS_LEVEL, 'SUCCESS')

# Add success method to logger
def success(self, message, *args, **kwargs):
    self.log(SUCCESS_LEVEL, message, *args, **kwargs)

logging.Logger.success = success

def setup_logging():
    # Create a color formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'SUCCESS':  'bold_green',  # Success will be bold green
            'WARNING': 'yellow',
            'ERROR':   'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    # Create a file formatter (without colors)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Set up the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler without colors
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Set specific log levels for third-party libraries
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING) 