import pymongo
from pymongo import database


class ContactDatabaseManager:
    def __init__(self, mongo_database: database.Database, collection_string="contact"):
        self.mongo_collection = mongo_database[collection_string]

    def clear(self):
        self.mongo_collection.drop()

    def update(self):
        pass
