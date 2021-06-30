""" Domain Level Config """
from graphene import Int
from common import secrets


# Flask Settings
DEBUG = False
TESTING = False
DEFAULT_LIMIT = 50
DEFAULT_OFFSET = 0

# AWS Configuration Settings
SECRET_NAME = "Starwars-DaaS-ConfigServer"
REGION = "us-east-1"

# Domain Specific Parameters
DOMAIN = "Star Wars"
VERSION = "1.0"

# Projection should include all requests fields, foreign key fields in source & target tables + any RDM fields
CHARACTER_PROJECTION = {
    "_id": 0,
    "name": 1,
    "age": 1,
    "height": 1,
}

# GENERIC GraphQL CONFIG. DO NOT CHANGE PLEASE
DATA_LOADER = {}
INFO = "info"
KEY_NAME = "key_name"
DEFAULT_QUERY_ARGS = {
    "__limit": Int(
        description="Limit the number of documents to be fetched from datastore. Default is {}".format(
            DEFAULT_LIMIT
        )
    ),
    "__offset": Int(
        description="Offest to the number of records to be fetched from datastore. Default is {}".format(
            DEFAULT_OFFSET
        )
    ),
}

DEFAULT_FILTER = {"validity": {"$ne": False}}

secret_meta_data = secrets.get_secret()
