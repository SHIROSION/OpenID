import pymysql
from control.log import log
from common.Riko import Riko, DictModel, ObjectModel, INSERT

"""
@module  : connect.py
@author  : Rinne
@contact : yejunbin123@qq.com
@time    : 2019/08/03
"""


class user_information(DictModel):
    pk = ["uid"]
    fields = ["username", "pwd", "appid", "clientId", "timestamp", "login_channel", "extra_payload", "user_payload"]


class login_information(DictModel):
    pk = ["id"]
    fields = ["uid", "username", "login_success", "token", "request_id", "appid", "clientId", "timestamp",
              "login_channel", "user_ip", "remote_ip", "extra_payload", "user_payload"]


class DataBaseControl:

    @staticmethod
    def get_user_information_by_uid(uid):
        """

        :rtype: object
        """
        return user_information.get_one(uid=uid)

    @staticmethod
    def get_user_information_by_username(username):
        """

        :param username:
        :return:
        """
        return user_information.get_one(username=username)

    @staticmethod
    def login_operating_information_update(**kwargs):
        """

        :rtype: object
        """
        login_information.new(**kwargs).insert()

    @staticmethod
    def sign_in_information(**kwargs):
        """

        :rtype: object
        """
        user_information.new(**kwargs).insert()

    @staticmethod
    def update_information(uid, info_dict):
        new_info = user_information.get_one(uid=uid)
        for k, v in info_dict.items():
            new_info[k] = v
        new_info.update()


if __name__ == "__main__":
    Riko.db_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "123456",
        "db": "camptalk",
        "charset": "utf8",
        "autocommit": True,
        'cursorclass': pymysql.cursors.DictCursor
    }
    test_dict = {"uid": 1, "username": "RK", "login_success": 0, "token": "123", "request_id": "45", "appid": "56",
                 "clientId": "67", "timestamp": "78", "login_channel": "89", "user_ip": "a", "remote_ip": "b",
                 "extra_payload": "q"}

    test_update_dict = {"timestamp": "1111", "login_channel": "qweeq"}

    print(DataBaseControl.get_user_information_by_uid(1000))
    print(DataBaseControl.get_user_information_by_username("莲华"))
    DataBaseControl.login_operating_information_update(**test_dict)
    log.info("test")
    print(login_information.get_many())
    print()
    DataBaseControl.update_information(1000, test_update_dict)
