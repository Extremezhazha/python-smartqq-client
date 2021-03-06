from pymongo import database
from .FaultyLoginDataException import FaultyLoginDataException


class DatabaseManager:
    @staticmethod
    def check_login_data_exist(data: {str: str}):
        return (
            "uin" in data and
            "psessionid" in data and
            "vfwebqq" in data and
            "ptwebqq" in data and
            "clientid" in data
        )

    def __init__(self, mongo_database: database.Database, login_data: {}, retrieve_handler=None):
        if not DatabaseManager.check_login_data_exist(login_data):
            raise FaultyLoginDataException
        else:
            self.login_data = login_data
        self.mongo_database = mongo_database
        self.retrieve_handler = retrieve_handler


def delkey(source, *keys):
    result = dict(source)
    for key in keys:
        result.pop(key, None)
    return result
