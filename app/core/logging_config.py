import logging
from logging.handlers import RotatingFileHandler
from .config import settings

def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'app.log',
                maxBytes=1024*1024,  # 1MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    ) 