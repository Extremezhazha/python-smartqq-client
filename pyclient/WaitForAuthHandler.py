import random
from requests import Response
from requests import Session
from .BarcodeExpiredException import BarcodeExpiredException
from .LoginStepHandler import LoginStepHandler
from .PollingHandler import PollingHandler


class WaitForAuthHandler(LoginStepHandler):
    def __init__(self, session: Session, barcode_handler=None):
        super().__init__(session)
        self.barcode_handler = barcode_handler

    @staticmethod
    def bkn_hash(key, init_str=5381):
        hash_str = init_str
        for i in key:
            hash_str += (hash_str << 5) + ord(i)
        hash_str = int(hash_str & 2147483647)
        return hash_str

    def next_step(self, accumulated, last_response: Response) -> ({}, Response):
        if self.barcode_handler is not None:
            self.barcode_handler(accumulated["login_barcode"])
        self.session.headers.update({"Referer": "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16"
                                                "&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1 "
                                                "&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert "
                                                "&strong_login=1&login_state=10&t=20131024001"})
        self.session.cookies.update({
            'RK': 'OfeLBai4FB',
            'pgv_pvi': '911366144',
            'pgv_info': 'ssid pgv_pvid=1051433466',
            'ptcz': ('ad3bf14f9da2738e09e498bfeb93dd9da7'
                     '540dea2b7a71acfb97ed4d3da4e277')
        })
        url = ('https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=' +
               str(WaitForAuthHandler.bkn_hash(self.session.cookies['qrsig'], init_str=0)) +
               '&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106' +
               '&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26' +
               'webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&' +
               'from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-' +
               repr(random.random() * 900000 + 1000000) +
               '&mibao_css=m_webqq&t=undefined&g=1&js_type=0' +
               '&js_ver=10141&login_sig=&pt_randsalt=0')

        def response_handler(response: Response):
            login_state = response.content.decode("utf-8")
            if "已失效" in login_state:
                print("barcode fail")
                raise BarcodeExpiredException
            if "成功" in login_state:
                login_data = login_state.split(",")
                nonlocal accumulated
                accumulated["login_success_url"] = login_data[2][1:-1]
                accumulated["user_name"] = login_data[-1][2:-5]
                return True
            return False

        response = PollingHandler(
            lambda: self.session.get(url),
            response_handler,
            delay=3,
            pass_through_exceptions=(BarcodeExpiredException,),
            exception_handler=lambda ex: print(ex)
        ).run()
        return accumulated, response
