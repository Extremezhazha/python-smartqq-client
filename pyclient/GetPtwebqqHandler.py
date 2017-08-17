from requests import Response
from .LoginStepHandler import LoginStepHandler
from .Logger import logger


class GetPtwebqqHandler(LoginStepHandler):
    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        self.session.headers.update({"Referer": "http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"})
        response = self.session.get(accumulated["login_success_url"])
        accumulated["ptwebqq"] = self.session.cookies.get("ptwebqq")
        logger.info("Ptwebqq step finished")
        return accumulated, response
