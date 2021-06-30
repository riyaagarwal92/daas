"""Star Wars access API."""

from flask import Flask
from flask_restful import Api
import logging
from common import config
from daas_starwars.starwars_graphql import StarWarsGraphQL
from daas_starwars import starwars_bp
from daas_starwars.schema import StarwarsDomainQuery
from graphene import Schema
from starwars_app.models import AboutAPI, ReadyCheck
from flask_log_request_id import RequestID

logger = logging.getLogger('starwars_daas')

def create_app():
    app = Flask(__name__)
    RequestID(app)
    app.config["DOMAIN"] = config.DOMAIN
    app.config["VERSION"] = config.VERSION

    api = Api(app, catch_all_404s=True)
    api.add_resource(AboutAPI, "/", "/about")
    api.add_resource(ReadyCheck, "/ready")

    app.register_blueprint(starwars_bp)

    return app
