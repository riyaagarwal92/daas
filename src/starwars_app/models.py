import os
from flask import jsonify
from flask_restful import Resource, abort
from common import config
from common.db import mongo


class AboutAPI(Resource):
    def get(self):
        md_info = config.secret_meta_data

        info = {
            "title": "Star Wars DaaS API",
            "description": "Data as a Service App for Star Wars",
            "version": config.VERSION,
            "Star Wars Data Domain": config.DOMAIN
        }
        return jsonify(info)


# Flask restful Readiness check resource
class ReadyCheck(Resource):
    def get(self):
        collection_data = mongo.collection_names(include_system_collections=False)
        if collection_data:
            return jsonify("Ready")
        else:
            return abort(503)
