import io
from requests import Response
from .LoginStepHandler import LoginStepHandler


class GetBarcodeStepHandler(LoginStepHandler):
    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        response = self.session.get("https://ssl.ptlogin2.qq.com/ptqrshow""?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.1")
        accumulated["login_barcode"] = io.BytesIO(response.content)
        return accumulated, response
