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

        get_time = time.strftime("%Y-%m-%d %H:%M:%S")

        login_return_info = {
            "timestamp": get_time,
            "request_id": login_info["request_id"],
            "code": "200",
            "sub_code": 0
        }

        try:
            get_info = None

            if login_info["email"] is not None:
                get_info = Connect.DataBaseControl.get_user_information_by_email(login_info["email"])

            elif login_info["username"] is not None:
                get_info = Connect.DataBaseControl.get_user_information_by_email(login_info["username"])

            elif login_info["phone"] is not None:
                get_info = Connect.DataBaseControl.get_user_information_by_email(login_info["phone"])

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

                    Connect.DataBaseControl.login_operating_information_update(**login_success_info)

                    return login_return_info

        except Exception as ex:
            print(ex)
            login_return_info["code"] = "500"
            login_return_info["sub_code"] = -1
            return login_return_info

    @staticmethod
    def sign_in_control(sign_in_info):
        get_time = time.strftime("%Y-%m-%d %H:%M:%S")

        login_return_info = {
            "timestamp": get_time,
            "request_id": sign_in_info["request_id"],
            "code": "200",
            "sub_code": 0
        }
        try:
            info = {
                "email": sign_in_info["email"],
                "phone": sign_in_info["phone"],
                "username": sign_in_info["username"],
                "pwd": CampSever.sha256_key(sign_in_info["username"], sign_in_info["pwd"]),
                "appid": sign_in_info["appid"],
                "clientId": sign_in_info["clientId"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "login_channel": sign_in_info["login_channel"]
            }

            try:
                print(type(info))
                Connect.DataBaseControl.sign_in_information(**info)
                login_return_info["code"] = "200"
                login_return_info["sub_code"] = 0
                return login_return_info
            except Exception as ex:
                print(ex)
                login_return_info["code"] = "200"
                login_return_info["sub_code"] = 1
                return login_return_info
        except Exception as ex:
            print(ex)
            login_return_info["code"] = "500"
            login_return_info["sub_code"] = -1
            return login_return_info

    def update_control(self):
        pass

    def get_user_list_control(self):
        pass

    def delete_user_control(self):
        pass

    @staticmethod
    def sha256_key(username, pwd):
        __hash = hashlib.sha256()
        __hash.update((username + "RengeRinkaStrangerLtWk" + pwd).encode("utf8"))
        __new_hash = __hash.hexdigest()
        return __new_hash
