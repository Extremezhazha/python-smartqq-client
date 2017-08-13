from requests import Response
from .LoginStepHandler import LoginStepHandler


class GetVfwebqqHandler(LoginStepHandler):
    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        self.session.headers.update({"Referer": "http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"})
        response = self.session.get("http://s.web2.qq.com/api/getvfwebqq?ptwebqq=" + accumulated["ptwebqq"] +
                                    "&clientid=53999199&psessionid=&t=0.1")
        accumulated["vfwebqq"] = response.json()["result"]["vfwebqq"]
        return accumulated, response
