import requests
from .BarcodeExpiredException import BarcodeExpiredException
from .LoginStepHandler import LoginStepHandler


class LoginPipeline:
    def __init__(self, session: requests.Session, exception_handler) -> None:
        self.pipeline = []
        self.session = session
        self.exception_handler = exception_handler

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
                # self.session.cookies.clear()
                # self.session.headers.clear()
                # print("Barcode expired, please try again.")
                restart = self.exception_handler(ex) if self.exception_handler is not None else True

        return accumulated, response
