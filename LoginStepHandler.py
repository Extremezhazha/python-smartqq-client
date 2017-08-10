from lib.requests.requests import Response
from lib.requests.requests import Session


class LoginStepHandler:
    def __init__(self, session: Session):
        self.session = session

    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        raise NotImplementedError("")
