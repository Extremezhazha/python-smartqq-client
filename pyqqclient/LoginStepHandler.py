from requests import Response
from requests import Session


class LoginStepHandler:
    def __init__(self, session: Session):
        self.session = session

    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        raise NotImplementedError("")
