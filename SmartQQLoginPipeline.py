from LoginPipeline import LoginPipeline
from GetBarcodeStepHandler import GetBarcodeStepHandler
from WaitForAuthHandler import WaitForAuthHandler


class SmartQQLoginPipeline(LoginPipeline):
    def __init__(self, session):
        super().__init__(session)
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        self.add_step(GetBarcodeStepHandler(session))
        self.add_step(WaitForAuthHandler(session))
