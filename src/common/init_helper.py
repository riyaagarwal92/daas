import os
import json
import datetime
import yaml
import boto3
from common import logger
from common import config
from botocore.exceptions import ClientError

dir = os.path.dirname(__file__)
path_parent = os.path.dirname(dir)
DOCDB_CERT_LOCATION = os.path.join(path_parent, "resources/rds-combined-ca-bundle.pem")


def get_docdb_certificate(bucket_name, file_name):
    """Download certificate for TLS DocDB connection."""
    if not os.path.isfile(DOCDB_CERT_LOCATION):
        logger.info("Getting the docdb cert from s3")
        s3 = boto3.resource("s3")
        s3.meta.client.download_file(bucket_name, file_name, DOCDB_CERT_LOCATION)
        logger.info("Downloaded the docDB cert from s3")
    return DOCDB_CERT_LOCATION

