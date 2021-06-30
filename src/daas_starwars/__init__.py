import logging
from flask import Blueprint
from flask_restful import Api
import os

logger = logging.getLogger('starwars_daas.starwars')
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))

starwars_bp = Blueprint('starwars', __name__, url_prefix="/api")
starwars_api = Api(starwars_bp)
