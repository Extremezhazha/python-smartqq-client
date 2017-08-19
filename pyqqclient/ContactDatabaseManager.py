from pymongo import database
from .DatabaseManager import DatabaseManager
from requests import Session
from . import SmartqqHash
from .UnknownUserException import UnknownUserException
import json


class ContactDatabaseManager(DatabaseManager):
    def __init__(self, mongo_database: database.Database, login_data: {},
                 session: Session, contact_collection_string="contact",
                 category_collection_string="category", identify_string="global"):
        super().__init__(mongo_database, login_data)
        self.contact_collection = self.mongo_database[contact_collection_string]
        self.category_collection = self.mongo_database[category_collection_string]
        self.session = session
        self.identify_string = identify_string
        self.data_r = {
            "vfwebqq": login_data["vfwebqq"],
            "hash": SmartqqHash.smartqq_hash(login_data["uin"], login_data["ptwebqq"])
        }

    def clear(self):
        self.contact_collection.delete_many({"identify_string": self.identify_string})
        self.category_collection.delete_many({"identify_string": self.identify_string})

    def get_data(self):
        self.clear()
        self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        self.session.headers.update({"Origin": "http://d1.web2.qq.com"})
        result = self.session.post(
            "http://s.web2.qq.com/api/get_user_friends2",
            data={"r": json.dumps(self.data_r)}
        ).json()["result"]
        friends = result["friends"]
        marknames = result["marknames"]
        info = result["info"]
        self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        for contact in friends:
            self.contact_collection.insert_one({
                "uin": contact["uin"],
                "identify_string": self.identify_string,
                "category_id": contact["categories"]
            })
        for contact in marknames:
            self.contact_collection.update_one({"uin": contact["uin"], "identify_string": self.identify_string},
                                               {"$set": {"marked_name": contact["markname"]}})
        for contact in info:
            self.contact_collection.update_one({"uin": contact["uin"], "identify_string": self.identify_string},
                                               {"$set": {"name": contact["nick"]}})
        categories = result["categories"]
        root_added = False
        for category in categories:
            if category["index"] == 0:
                root_added = True
            self.category_collection.insert_one({
                "identify_string": self.identify_string,
                "index": category["index"],
                "sort": category["sort"],
                "name": category["name"]
            })
        if not root_added:
            self.category_collection.insert_one({
                "identify_string": self.identify_string,
                "index": 0,
                "sort": 0,
                "name": "My Friends"
            })

    def get_contact_info(self, uin, retrying=False):
        contact = self.contact_collection.find_one({"uin": uin, "identify_string": self.identify_string})
        if contact is None:
            if retrying:
                raise UnknownUserException
            self.get_data()
            return self.get_contact_info(uin, retrying=True)
        category = self.category_collection.find_one({
            "index": contact["category_id"], "identify_string": self.identify_string
        })
        if category is None:
            if retrying:
                raise UnknownUserException
            self.get_data()
            return self.get_contact_info(uin, retrying=True)
        contact["category_name"] = category["name"]
        return contact
