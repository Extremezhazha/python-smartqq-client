from LoginStepHandler import LoginStepHandler
from lib.requests import requests


class LoginPipeline:
    def __init__(self, session: requests.Session) -> None:
        self.pipeline = []
        self.session = session

    def add_step(self, next_step: LoginStepHandler) -> None:
        self.pipeline.append(next_step)

    def run(self) -> ({}, requests.Response):
        accumulated, response = {}, requests.Response()
        restart = True
        while restart:
            restart = False
            try:
                for step in self.pipeline:
                    accumulated, response = step.next_step(accumulated, response)
            except Exception as ex:
                self.session.cookies.clear()
                self.session.headers.clear()
                print(ex)
                restart = True
        return accumulated, response
