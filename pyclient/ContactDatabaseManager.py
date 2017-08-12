import pymongo


class ContactDatabaseManager:
    def __init__(self, mongodb_host="127.0.0.1", mongodb_port=27017):
        self.mongo_client = pymongo.MongoClient(mongodb_host, mongodb_port)
        pass
