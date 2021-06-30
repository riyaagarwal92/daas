import json
from pymongo.errors import NetworkTimeout
from common.helpers import get_projection, get_limit, get_offset, timer, build_mongo_query
from common.db import mongo
from common import config
from daas_starwars import logger


class PymongoError(Exception):
    """Thrown when a database error occurs"""

    pass

# GraphQL Star Wars Characters Mongo Query
@timer
def getCharacters(args, info):
    """Retrieve records from the Star Wars Characters Collection using pyMongo."""
    
    limit = get_limit(info, args)
    offset = get_offset(args)
    projection = get_projection(info)
    projection.update(config.CHARACTER_PROJECTION)
    query = build_mongo_query(args)  
    collection = json.loads(config.secret_meta_data.get("collections")).get("character_col")
    try:
        return (
            mongo[collection]
            .find(query, projection)
            .skip(offset)
            .limit(limit)
        )
    except NetworkTimeout as err:
        logger.error("Database operation timed out with the error: {}".format(err))
        raise PymongoError("Database operation timed out with the error: {}".format(err))  

