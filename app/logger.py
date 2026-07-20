import logging
import sys

def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid duplication
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
    return logger

log = setup_logging()
