import json
import requests
import pymongo
from .PollingHandler import PollingHandler
from .SmartqqLoginPipeline import SmartqqLoginPipeline
from .ContactDatabaseManager import ContactDatabaseManager
from .GroupDatabaseManager import GroupDatabaseManager
from .SmartqqMessageHandler import SmartqqMessageHandler
from .FaultyLoginDataException import FaultyLoginDataException
from .Logger import logger


class SmartqqClient:
    def handler_wrapper(self, orig_handler):
        #
        # def result_handler(message):
        #     orig_handler(message)
        #     return self.stopped
        # return result_handler
        # return lambda message: (orig_handler(message) or self.stopped)
        return lambda message: ((orig_handler(message, self.env) if self.passing_env else orig_handler(message)),
                                self.stopped)[1]

    def print_response_and_check(self, x):
        response_json = x.json()
        if "errmsg" in response_json:
            return self.stopped
        message = response_json["result"][0]["value"]
        print(self.contact_manager.get_contact_info(message["from_uin"]))
        print(message["content"][-1])
        return self.stopped

    def default_friend_message_handler(self, message):
        content = message["value"]
        logger.info(self.contact_manager.get_contact_info(content["from_uin"]))
        logger.info(content["content"][-1])
        return self.stopped

    def default_group_message_handler(self, message):
        logger.info("this is a group message")
        return self.stopped

    def __init__(self, login_data=None, barcode_handler=None,
                 friend_message_handler=None, group_message_handler=None, passing_env=False):
        self.session = requests.Session()
        self.login_pipeline = SmartqqLoginPipeline(self.session, barcode_handler)
        self.friend_message_handler = (
            self.handler_wrapper(friend_message_handler) if friend_message_handler is not None
            else self.default_friend_message_handler
        )
        self.group_message_handler = (
            self.handler_wrapper(group_message_handler) if group_message_handler is not None
            else self.default_group_message_handler
        )
        self.message_handler = SmartqqMessageHandler.print_all_handler(
            friend_message_handler=self.friend_message_handler,
            group_message_handler=self.group_message_handler
        )
        self.passing_env = passing_env
        self.env = {}
        self.stopped = False
        self.contact_manager = None
        self.group_manager = None
        self.login_data = login_data

    def login(self):
        self.login_data, dispose = self.login_pipeline.run()

    def run(self):
        if self.login_data is None:
            self.login()
        contact_db = pymongo.MongoClient()["python-smartqq-client"]
        self.contact_manager = ContactDatabaseManager(contact_db, self.login_data, self.session)
        # self.contact_manager.get_data()
        self.group_manager = GroupDatabaseManager(contact_db, self.login_data, self.session)
        # self.group_manager.get_data()
        self.env["contact_manager"] = self.contact_manager
        self.env["group_manager"] = self.group_manager

        def message_grabber():
            self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
            data_r = {
                "ptwebqq": self.login_data["ptwebqq"],
                "clientid": self.login_data["clientid"],
                "psessionid": self.login_data["psessionid"],
                "key": ""
            }
            return self.session.post(
                "http://d1.web2.qq.com/channel/poll2",
                data={"r": json.dumps(data_r)}
            )

        logger.info("Starting polling")
        polling = PollingHandler(message_grabber, self.message_handler,
                                 pass_through_exceptions=[FaultyLoginDataException])
        polling.run()
