"""This module is used to configure custom logger for Star Wars App."""

import os
import logging
from flask_log_request_id import RequestIDLogFilter

# Create handlers
handler = logging.StreamHandler()

# Create formatters and add it to handlers
formatter = logging.Formatter(
    "%(asctime)s %(process)d:%(thread)d;TRACE;%(levelname)s;request_id=%(request_id)s;%(message)s"
)
handler.setFormatter(formatter)
# Add request id contextual filter
handler.addFilter(RequestIDLogFilter())

# Create a custom logger
logger = logging.getLogger("daas_starwars")
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)
logger.propagate = False
