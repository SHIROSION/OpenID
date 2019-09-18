import ast
import hashlib
import time

from datetime import datetime
from common import Connect

"""
@module  : server.py
@author  : Rinne
@contact : yejunbin123@qq.com
@time    : 2019/08/04
"""


class CampServer:
    def __init__(self):
        pass

    @staticmethod
    def login_control(login_info):

        login_return_info = {
            "timestamp": CampServer.time_now_str(),
            "request_id": login_info["request_id"],
            "data": {},
            "code": 200,
            "sub_code": 0
        }

        try:
            get_info = None

            if "email" in login_info:
                get_info = Connect.DataBaseControl.get_user_information_by_email(login_info["email"])

            elif "username" in login_info:
                get_info = Connect.DataBaseControl.get_user_information_by_username(login_info["username"])

            elif "phone" in login_info:
                get_info = Connect.DataBaseControl.get_user_information_by_phone(login_info["phone"])

            if get_info is not None and get_info["state"] == 0:

                login_success_info = {
                    "uid": get_info["uid"],
                    "username": get_info["username"],
                    "phone": get_info["phone"],
                    "email": get_info["email"],
                    "login_success": 0,
                    "request_id": login_info["request_id"],
                    "appid": login_info["appid"],
                    "timestamp": login_info["timestamp"],
                    "login_channel": login_info["login_channel"],
                    "user_ip": login_info["user_ip"],
                    "remote_ip": login_info["remote_ip"]
                }
                if "token" in login_info:
                    login_success_info["token"] = login_info["token"]
                if "clientId" in login_info:
                    login_success_info["clientId"] = login_info["clientId"]

                if CampServer.sha256_key(login_info["username"], login_info["pwd"]) == get_info["pwd"]:
                    login_success_info["login_success"] = 0

                    Connect.DataBaseControl.login_operating_information_update(**login_success_info)

                    del get_info["pwd"]
                    login_return_info["data"] = get_info
                    login_return_info["code"] = 200
                    login_return_info["sub_code"] = 0
                    return login_return_info
                else:
                    login_return_info["code"] = 200
                    login_return_info["sub_code"] = 1

                    Connect.DataBaseControl.login_operating_information_update(**login_success_info)

                    return login_return_info
            else:
                login_return_info["code"] = 200
                login_return_info["sub_code"] = 1

                return login_return_info

        except Exception as ex:
            print(ex)
            login_return_info["code"] = 500
            login_return_info["sub_code"] = -1
            return login_return_info

    @staticmethod
    def sign_in_control(sign_in_info):

        login_return_info = {
            "timestamp": CampServer.time_now_str(),
            "request_id": sign_in_info["request_id"],
            "code": 200,
            "sub_code": 0
        }
        try:
            info = {
                "username": sign_in_info["username"],
                "pwd": CampServer.sha256_key(sign_in_info["username"], sign_in_info["pwd"]),
                "appid": sign_in_info["appid"],
                "clientId": sign_in_info["clientId"],
                "timestamp": sign_in_info["timestamp"],
                "login_channel": sign_in_info["login_channel"],
            }

            check_account = False
            if "email" in sign_in_info:
                info["email"] = sign_in_info["email"]
                check_account = True
            if check_account is False:
                raise Exception('lack email')

            if "phone" in sign_in_info:
                info["phone"] = sign_in_info["phone"]

            try:
                Connect.DataBaseControl.sign_in_information(**info)
                login_return_info["code"] = 200
                login_return_info["sub_code"] = 0
                return login_return_info
            except Exception as ex:
                print(ex)
                login_return_info["code"] = 200
                login_return_info["sub_code"] = 1
                return login_return_info
        except Exception as ex:
            print(ex)
            login_return_info["code"] = 500
            login_return_info["sub_code"] = -1
            return login_return_info
        
    @staticmethod
    def update_control(update_info):

        update_return_info = {
            "timestamp": CampServer.time_now_str(),
            "request_id": update_info["request_id"],
            "code": 200,
            "sub_code": 0
        }

        try:
            old_info = Connect.DataBaseControl.get_user_information_by_username(update_info["username"])
            need_update_info = {}

            for x in update_info.keys():
                if x in ["token", "timestamp", "request_id"]:
                    continue
                elif x == "pwd":
                    new_pwd = CampServer.sha256_key(update_info["username"], update_info["pwd"])
                    if new_pwd == old_info["pwd"]:
                        continue
                    else:
                        need_update_info[x] = new_pwd
                elif x == "extra_payload":
                    new_data = CampServer.payload_update(old_info["extra_payload"], update_info["extra_payload"])
                    if new_data is not None:
                        need_update_info["extra_payload"] = new_data
                    else:
                        continue
                elif x == "user_payload":
                    new_data = CampServer.payload_update(old_info["user_payload"], update_info["user_payload"])
                    if new_data is not None:
                        need_update_info["user_payload"] = new_data
                    else:
                        continue
                else:
                    need_update_info[x] = update_info[x]

            Connect.DataBaseControl.update_information_by_username(update_info["username"], need_update_info)
            update_return_info["code"] = 200
            update_return_info["sub_code"] = 0
            return update_return_info

        except Exception as ex:
            print(ex)
            update_return_info["code"] = 500
            update_return_info["sub_code"] = -1
            return update_return_info

    @staticmethod
    def get_user_list_control(list_info):

        user_list_return_info = {
            "timestamp": CampServer.time_now_str(),
            "request_id": list_info["request_id"],
            "code": 200,
            "sub_code": 0,
            "data": None
        }

        try:
            if "usernames" in list_info:
                user_list_return_info["data"] = Connect.DataBaseControl.get_user_many(
                    u_key='username',
                    user_list=list_info["usernames"]
                    )
            elif "emails" in list_info:
                user_list_return_info["data"] = Connect.DataBaseControl.get_user_many(
                    u_key='email',
                    user_list=list_info["emails"]
                )
            elif "phones" in list_info:
                user_list_return_info["data"] = Connect.DataBaseControl.get_user_many(
                    u_key='phone',
                    user_list=list_info["phones"]
                )

            user_list_return_info["code"] = 200
            user_list_return_info["sub_code"] = 0
            return user_list_return_info
        except Exception as ex:
            print(ex)
            user_list_return_info["code"] = 500
            user_list_return_info["sub_code"] = -1
            return user_list_return_info

    @staticmethod
    def delete_user_control(delete_info):

        delete_return_info = {
            "timestamp": CampServer.time_now_str(),
            "request_id": delete_info["request_id"],
            "code": 200,
            "sub_code": 0
        }

        try:
            Connect.DataBaseControl.delete_information(delete_info["username"])
            delete_return_info["code"] = 200
            delete_return_info["sub_code"] = 0
            return delete_return_info

        except Exception as ex:
            print(ex)
            delete_return_info["code"] = 500
            delete_return_info["sub_code"] = -1

    @staticmethod
    def sha256_key(username, pwd):
        __hash = hashlib.sha256()
        __hash.update((username + "RengeRinkaStrangerLtWk" + pwd).encode("utf8"))
        __new_hash = __hash.hexdigest()
        return __new_hash

    @staticmethod
    def payload_update(old_payload, new_payload):
        new_date_flag = False
        if old_payload is not None and new_payload is not None:
            old_payload = ast.literal_eval(old_payload)
            new_payload = ast.literal_eval(new_payload)
            for x in new_payload.keys():
                if x in old_payload.keys():
                    if new_payload[x] == old_payload[x]:
                        continue
                    else:
                        new_date_flag = True
                        old_payload[x] = new_payload[x]
                else:
                    new_date_flag = True
                    old_payload[x] = new_payload[x]
        else:
            return new_payload

        if new_date_flag:
            return str(old_payload)
        else:
            return None

    @staticmethod
    def time_now_str():
        return time.time()

    @staticmethod
    def time_now_format(date, date_format):
        return datetime.strptime(date, date_format)


if __name__ == "__main__":
    a = "{'gender': 'male', 'age': 28, 'name': 'john'}"
    b = ast.literal_eval(a)
    print(b)
