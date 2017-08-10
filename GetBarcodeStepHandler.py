from lib.requests.requests import Response
from LoginStepHandler import LoginStepHandler
import io
import shutil


class GetBarcodeStepHandler(LoginStepHandler):
    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        response = self.session.get("https://ssl.ptlogin2.qq.com/ptqrshow""?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.1")
        accumulated["login_barcode"] = io.BytesIO(response.content)
        return accumulated, response
