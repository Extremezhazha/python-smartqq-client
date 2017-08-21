import json
import requests
import pymongo
from .PollingHandler import PollingHandler
from .SmartqqLoginPipeline import SmartqqLoginPipeline
from .ContactDatabaseManager import ContactDatabaseManager
from .GroupDatabaseManager import GroupDatabaseManager
from .SmartqqMessageHandler import SmartqqMessageHandler
from .Logger import logger


class SmartqqClient:
    def handler_wrapper(self, orig_handler):
        return lambda message: ((orig_handler(message, self.env) if self.passing_env else orig_handler(message)),
                                self.stopped)[1]

    @staticmethod
    def get_group_name(group_info):
        return group_info["name"]

    @staticmethod
    def get_user_name(user_info):
        if "marked_name" in user_info:
            result = user_info["marked_name"] + "(" + user_info["name"] + ")"
        else:
            result = user_info["name"]
        return result

    @staticmethod
    def get_message_content(message):
        content = message["content"]
        if len(content) < 2:
            return "Unsupported message"
        else:
            result = "".join(
                map(
                    lambda x: x if x.__class__ == str else json.dumps(x),
                    content[1:]
                )
            )
            return result

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
        logger.info(
            SmartqqClient.get_user_name(self.contact_manager.get_contact_info(content["from_uin"])) +
            " sent a message: " +
            SmartqqClient.get_message_content(content)
        )
        return self.stopped

    def friend_message_echo_handler(self, message):
        self.default_friend_message_handler(message)
        content = message["value"]
        self.send_message(content["from_uin"], SmartqqClient.get_message_content(content))
        return self.stopped

    def default_group_message_handler(self, message):
        content = message["value"]
        logger.info(
            SmartqqClient.get_user_name(
                self.group_manager.get_member_info(content["from_uin"], content["send_uin"])
            ) + " from group " +
            SmartqqClient.get_group_name(
                self.group_manager.get_group_info(content["from_uin"])
            ) + " sent a message: " +
            SmartqqClient.get_message_content(content)
        )
        return self.stopped

    def __init__(self, login_data=None, barcode_handler=None,
                 friend_message_handler=None, group_message_handler=None, passing_env=False,
                 login_done_handler=None, login_exception_handler=None,
                 db_identify_string=None):
        self.session = requests.Session()
        self.login_pipeline = SmartqqLoginPipeline(
            self.session, barcode_handler, exception_handler=login_exception_handler
        )
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
        self.db_identify_string = db_identify_string
        self.login_done_handler = login_done_handler

    def login(self):
        self.login_data, dispose = self.login_pipeline.run()

    def run(self):
        if self.login_data is None:
            self.login()
        contact_db = pymongo.MongoClient()["python-smartqq-client"]
        self.contact_manager = ContactDatabaseManager(contact_db, self.login_data, self.session,
                                                      identify_string=self.db_identify_string)
        # self.contact_manager.get_data()
        self.group_manager = GroupDatabaseManager(contact_db, self.login_data, self.session,
                                                  identify_string=self.db_identify_string)
        # self.group_manager.get_data()
        self.env["contact_manager"] = self.contact_manager
        self.env["group_manager"] = self.group_manager
        if self.login_done_handler is not None:
            self.login_done_handler()

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

        logger.info("Starting polling for messages")
        polling = PollingHandler(
            message_grabber, self.message_handler,
            pass_through_exceptions={},
            exception_handler=lambda ex: (
                logger.error("raised {exception_class} ({exception_docstring}): {exception_message}"
                             .format(exception_class=ex.__class__,
                                     exception_docstring=ex.__doc__,
                                     exception_message=str(ex)
                                     ))
                , False)[1]
        )
        polling.run()

    def get_sending_data_r(self, to_name, to_id, message):
        data_content = [
            message,
            [
                "font",
                {
                    "name": "宋体",
                    "size": 10,
                    "style": [
                        0,
                        0,
                        0
                    ],
                    "color": "000000"
                }
            ]
        ]
        data_r = {
            to_name: to_id,
            "content": json.dumps(data_content),
            "face": 522,
            "clientid": self.login_data["clientid"],
            "msg_id": 65890001,
            "psessionid": self.login_data["psessionid"]
        }
        return data_r

    def send_message(self, uin, message):
        data_r = self.get_sending_data_r("to", uin, message)
        self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        self.session.headers.update({"Origin": "http://d1.web2.qq.com"})
        return self.session.post("http://d1.web2.qq.com/channel/send_buddy_msg2", data={"r": json.dumps(data_r)}).json()

    def send_group_message(self, gid, message):
        data_r = self.get_sending_data_r("group_uin", gid, message)
        self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        self.session.headers.update({"Origin": "http://d1.web2.qq.com"})
        return self.session.post("http://d1.web2.qq.com/channel/send_qun_msg2", data={"r": json.dumps(data_r)}).content

    def db_clear_all(self):
        self.group_manager.clear_all()
        self.contact_manager.clear()
