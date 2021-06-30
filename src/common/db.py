from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
from common.config import secret_meta_data
from common.init_helper import get_docdb_certificate


DOCUMENT_DB_HOSTNAME = secret_meta_data.get("docDBHost")
DOCUMENT_DB_USERNAME = secret_meta_data.get("docDBUsername")
DOCUMENT_DB_PASSWORD = secret_meta_data.get("docDBPassword")
DATABASE_NAME = secret_meta_data.get("docDBDBName")
DOCUMENT_DB_PORT = str(secret_meta_data.get("docDBPort"))

# Downloads PEM file
db_cert = get_docdb_certificate(
    secret_meta_data.get("docDBCertBucket"), secret_meta_data.get("docDBCertS3Key")
)

# Make DocDB connections
uri = f"mongodb://{DOCUMENT_DB_USERNAME}:{DOCUMENT_DB_PASSWORD}"
uri += f"@{DOCUMENT_DB_HOSTNAME}:{DOCUMENT_DB_PORT}"

try:
    logging.info("Attempting to establish connection with DocDB")
    client = MongoClient(
        uri,
        ssl=True,
        tlsCAFile=db_cert,
        socketTimeoutMS=5000,
        replicaSet="rs0",
        readPreference="secondaryPreferred",
        minPoolSize=0,
        maxPoolSize=100,
        maxIdleTimeMS=300000,
    )
    mongo = client[DATABASE_NAME]
    logging.info("DocDB connection established: {}".format(client.server_info()))
except ServerSelectionTimeoutError as err:
    logging.error("Failed to connect to server {} with the error: {}".format(uri, err))
