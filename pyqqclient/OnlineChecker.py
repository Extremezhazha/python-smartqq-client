from requests import Session


class OnlineChecker:
    @staticmethod
    def check_online(login_data: dict, session: Session):
        session.headers.update({"Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"})
        session.headers.update({"Origin": "http://d1.web2.qq.com"})
        url = (
            "http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq=" +
            login_data["vfwebqq"] +
            "&clientid=" +
            str(login_data["clientid"]) +
            "&psessionid=" +
            login_data["psessionid"] +
            "&t=0.1"
        )
        return session.get(url)