import logging 
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# constants for log configuration
LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5*1024*1024 # 5 MB
BACKUP_COUNT = 3           # Number of backup file logs to keep

# construct log path
log_dir_path = os.path.join(os.getcwd(),LOG_DIR)
os.makedirs(log_dir_path,exist_ok=True)
log_file_path = os.path.join(log_dir_path,LOG_FILE)

def configure_logger():
    """
    Configure logging with a rotating file handler and a console handler
    """
    # create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # define formatter
    formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file_path,maxBytes=MAX_LOG_SIZE,backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Avoid duplicate handlers if configure_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


# configure the logger
configure_logger()



