import json
from requests import Response
from .LoginStepHandler import LoginStepHandler


class GetPsessionidHandler(LoginStepHandler):
    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        data_r = {
            "ptwebqq": accumulated["ptwebqq"],
            "clientid": 53999199,
            "psessionid": "",
            "status": "online"
        }
        response = self.session.post("http://d1.web2.qq.com/channel/login2",
                                     data={"r": json.dumps(data_r)})
        response_data = response.json()
        accumulated["uin"] = response_data["result"]["uin"]
        accumulated["psessionid"] = response_data["result"]["psessionid"]
        return accumulated, response
