import logging
from config import LOG_LEVEL, LOG_FILE

def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('synageion')