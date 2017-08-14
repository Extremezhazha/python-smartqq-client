import json
import requests
import pymongo
from .PollingHandler import PollingHandler
from .SmartqqLoginPipeline import SmartqqLoginPipeline
from .ContactDatabaseManager import ContactDatabaseManager


class SmartqqClient:
    def print_response_and_check(self, x):
        response_json = x.json()
        if "errmsg" in response_json:
            return self.stopped
        message = response_json["result"][0]["value"]
        print(self.contact_manager.get_contact(message["from_uin"]))
        print(message["content"][-1])
        return self.stopped

    def __init__(self, barcode_handler=None, message_handler=None):
        self.session = requests.Session()
        self.login_pipeline = SmartqqLoginPipeline(self.session, barcode_handler)
        self.message_handler = message_handler if message_handler is not None else self.print_response_and_check
        self.stopped = False
        self.contact_manager = None

    def run(self):
        accumulated, dispose = self.login_pipeline.run()
        del dispose
        contact_db = pymongo.MongoClient()["python-smartqq-client"]
        self.contact_manager = ContactDatabaseManager(contact_db, accumulated, self.session)
        self.contact_manager.get_data()

        def message_grabber():
            nonlocal accumulated
            self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
            data_r = {
                "ptwebqq": accumulated["ptwebqq"],
                "clientid": accumulated["clientid"],
                "psessionid": accumulated["psessionid"],
                "key": ""
            }
            return self.session.post(
                "http://d1.web2.qq.com/channel/poll2",
                data={"r": json.dumps(data_r)}
            )

        print("polling")
        polling = PollingHandler(message_grabber, self.message_handler)
        polling.run()
