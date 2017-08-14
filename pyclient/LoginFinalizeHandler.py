from requests import Response
from .LoginStepHandler import LoginStepHandler


class LoginFinalizeHandler(LoginStepHandler):
    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        del accumulated["login_barcode"]
        del accumulated["login_success_url"]
        self.session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        self.session.headers.update({"Origin": "http://d1.web2.qq.com"})
        url = (
            "http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq=" +
            accumulated["vfwebqq"] +
            "&clientid=" +
            str(accumulated["clientid"]) +
            "&psessionid=" +
            accumulated["psessionid"] +
            "&t=0.1"
        )
        return accumulated, self.session.get(url)
