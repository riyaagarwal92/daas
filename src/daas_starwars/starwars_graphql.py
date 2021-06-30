import os
import logging
from datetime import datetime
from functools import wraps
from flask_restful import Resource, reqparse, abort
from flask import request
from graphene import Schema
from common.config import secret_meta_data
from logging_config import logger
from common.helpers import format_logs
from flask_graphql import GraphQLView
from daas_starwars.schema import StarwarsDomainQuery
from daas_starwars import starwars_bp, starwars_api


class StarwarsGraphQL(Resource):
    def get(self):
        res = self.execute_graphql_query()
        return res

    def post(self):
        res = self.execute_graphql_query()
        return res

    def execute_graphql_query(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "query", type=str, required=True, help="Provide a valid graphql query."
        )
        parser.add_argument("variables", type=dict, help="Variables for graphql query.")
        parser.add_argument(
            "apiKey", type=str, help="Api Key secret used to call Star Wars DaaS."
        )
        args = parser.parse_args(strict=True)
        graphql_query = args.pop('query')
        schema = Schema(query=StarwarsDomainQuery)
        execution_result = schema.execute(graphql_query, **args)
        if execution_result.invalid:
            status_code = 400
        elif execution_result.errors and all(value == None for value in execution_result.data.values()):
            status_code = 500
        else:
            status_code = 200
        return execution_result.to_dict(), status_code


starwars_api.add_resource(StarwarsGraphQL, "/starwars")
starwars_bp.add_url_rule(
    "/starwars/graphiql",
    view_func=
        GraphQLView.as_view(
            "graphql", schema=Schema(query=StarwarsDomainQuery), graphiql=True
        )
)
