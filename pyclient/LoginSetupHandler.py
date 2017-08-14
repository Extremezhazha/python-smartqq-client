from .LoginStepHandler import LoginStepHandler
from requests import Response


class LoginSetupHandler(LoginStepHandler):
    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        accumulated["clientid"] = 53999199
        return accumulated, last_response
