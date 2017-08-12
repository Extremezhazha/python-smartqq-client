from SmartqqLoginPipeline import SmartqqLoginPipeline
from PollingHandler import PollingHandler
from lib.requests import requests
import json


class SmartqqClient:
    def print_response_and_check(self, x):
        print(x.json())
        return self.stopped

    def __init__(self, barcode_handler=None, message_handler=print_response_and_check):
        self.session = requests.Session()
        self.login_pipeline = SmartqqLoginPipeline(self.session, barcode_handler)
        self.message_handler = message_handler
        self.stopped = False

    def run(self):
        accumulated, dispose = self.login_pipeline.run()
        del dispose

        def message_grabber():
            nonlocal accumulated
            self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
            data_r = {
                "ptwebqq": accumulated["ptwebqq"],
                "clientid": 53999199,
                "psessionid": accumulated["psessionid"],
                "key": ""
            }
            return self.session.post(
                "http://d1.web2.qq.com/channel/poll2",
                data={"r": json.dumps(data_r)}
            )

        polling = PollingHandler(message_grabber, self.message_handler)
        polling.run()
