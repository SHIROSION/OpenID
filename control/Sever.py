import hashlib
import time

from common import Connect

"""
@module  : server.py
@author  : Rinne
@contact : yejunbin123@qq.com
@time    : 2019/08/04
"""


class CampSever:
    def __init__(self):
        pass

    @staticmethod
    def login_control(login_info):
        get_info = None

        if login_info["email"] is not None:
            get_info = Connect.DataBaseControl.get_user_information_by_email(login_info["email"])

        elif login_info["username"] is not None:
            get_info = Connect.DataBaseControl.get_user_information_by_email(login_info["username"])

        elif login_info["phone"] is not None:
            get_info = Connect.DataBaseControl.get_user_information_by_email(login_info["phone"])

        get_time = time.strftime("%Y-%m-%d %H:%M:%S")
        login_return_info = {
            "timestamp": get_time,
            "request_id": login_info["request_id"],
            "code": "200",
            "sub_code": 0
        }

        if get_info is not None:

            login_success_info = {
                                        "uid": get_info["uid"], "username": get_info["username"],
                                        "phone": get_info["phone"], "email": get_info["email"],
                                        "login_success": 0, "token": login_info["token"],
                                        "request_id": login_info["request_id"], "appid": login_info["appid"],
                                        "clientId": login_info["clientId"], "timestamp": get_time,
                                        "login_channel": login_info["login_channel"], "user_ip": login_info["user_ip"],
                                        "remote_ip": login_info["remote_ip"]
                }

            if CampSever.sha256_key(login_info["username"], login_info["password"]) == get_info["pwd"]:
                login_success_info["login_success"] = 0

                Connect.DataBaseControl.login_operating_information_update(**login_success_info)

                login_return_info["code"] = "200"
                login_return_info["sub_code"] = 0
                return login_return_info
            else:
                login_return_info["code"] = "200"
                login_return_info["sub_code"] = 1
                return login_return_info
        else:
            login_return_info["code"] = "500"
            login_return_info["sub_code"] = -1
            return login_return_info

    @staticmethod
    def sign_in_control(self):
        pass

    def update_control(self):
        pass

    def get_user_list_control(self):
        pass

    def delete_user_control(self):
        pass

    @staticmethod
    def sha256_key(username, pwd):
        __hash = hashlib.sha256()
        __hash.update(username + "RengeRinkaStrangerLtWk" + pwd.ebcide("utf8"))

        return __hash.hexdigest()