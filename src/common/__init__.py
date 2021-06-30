import logging
import os
logger = logging.getLogger('daas.common')
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
