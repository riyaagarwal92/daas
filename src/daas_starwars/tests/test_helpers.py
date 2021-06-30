import mock
import unittest
import datetime
from common import helpers


@mock.patch('common.config.DEFAULT_FILTER', {"validity": {"$ne": False}})                
class Test(unittest.TestCase):
    # No argument passed
    def test_build_mongo_query_no_args(self):
        response = helpers.build_mongo_query({})
        self.assertEqual({'validity': {'$ne': False}}, response)

    # Date field passed - dob
    def test_build_mongo_query_datetype1_args(self):
        response = helpers.build_mongo_query({'dob': datetime.date(1900, 1, 1)})
        self.assertEqual({'dob': datetime.datetime(1900, 1, 1, 0, 0), 'validity': {'$ne': False}}, response)

    # String field passed - name
    def test_build_mongo_query_name_args(self):
        response = helpers.build_mongo_query({'name': 'Luke Skywalker'})
        self.assertEqual({'name': 'Luke Skywalker', 'validity': {'$ne': False}}, response)
