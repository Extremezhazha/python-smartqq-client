from .DatabaseManager import DatabaseManager
from pymongo import database
from requests import Session
from . import SmartqqHash
from .UnknownUserException import UnknownUserException
import json


class GroupDatabaseManager(DatabaseManager):
    def __init__(self, mongo_database: database.Database, login_data: {}, session: Session,
                 group_collection_string="groups", group_member_collection_string="group_member",
                 identify_string="global"):
        super().__init__(mongo_database, login_data)
        self.session = session
        self.group_collection = self.mongo_database[group_collection_string]
        self.group_member_collection = self.mongo_database[group_member_collection_string]
        self.data_r = {
            "vfwebqq": login_data["vfwebqq"],
            "hash": SmartqqHash.smartqq_hash(login_data["uin"], login_data["ptwebqq"])
        }
        self.identify_string = identify_string

    def clear(self):
        self.group_collection.delete_many({"identify_string": self.identify_string})

    def mem_clear(self, gid: str):
        self.group_member_collection.delete_many({"identify_string": self.identify_string, "gid": gid})

    def mem_clear_all(self):
        self.group_member_collection.delete_many({"identify_string": self.identify_string})

    def clear_all(self):
        self.clear()
        self.mem_clear_all()

    def get_data(self):
        self.clear()
        self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        self.session.headers.update({"Origin": "http://d1.web2.qq.com"})
        result = self.session.post(
            "http://s.web2.qq.com/api/get_group_name_list_mask2",
            data={"r": json.dumps(self.data_r)}
        ).json()["result"]
        gnamelist = result["gnamelist"]
        for group in gnamelist:
            self.group_collection.insert_one({"code": group["code"], "gid": group["gid"],
                                              "identify_string": self.identify_string,
                                              "name": group["name"]})

    def get_group_member_data(self, gcode: str, gid: str):
        self.mem_clear(gid)
        self.session.headers.update({"Referer": "http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"})
        result = self.session.get("http://s.web2.qq.com/api/get_group_info_ext2?gcode=" +
                                  str(gcode) +
                                  "&vfwebqq=" +
                                  self.login_data["vfwebqq"] +
                                  "&t=0.1").json()["result"]
        minfo = result["minfo"]
        for member in minfo:
            self.group_member_collection.insert_one({
                "name": member["nick"],
                "gid": gid,
                "uin": member["uin"],
                "identify_string": self.identify_string
            })
        if "cards" in result:
            cards = result["cards"]
            for card in cards:
                self.group_member_collection.update_one({
                    "gid": gid,
                    "uin": card["muin"],
                    "identify_string": self.identify_string
                }, {"$set": {"marked_name": card["card"]}}
                )

    def get_group_info(self, gid, retrying=False):
        group = self.group_collection.find_one({"gid": gid, "identify_string": self.identify_string})
        if group is None:
            if retrying:
                raise UnknownUserException
            self.get_data()
            return self.get_group_info(gid, retrying=True)
        return group

    def get_member_info(self, gid, uin, retrying=False):
        member = self.group_member_collection.find_one({"gid": gid, "uin": uin,
                                                        "identify_string": self.identify_string})
        if member is None:
            if retrying:
                raise UnknownUserException
            group = self.get_group_info(gid)
            self.get_group_member_data(group["code"], group["gid"])
            return self.get_member_info(gid, uin, retrying=True)
        return member
