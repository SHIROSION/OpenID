import pymysql
from common.Riko import Riko, DictModel, ObjectModel, INSERT

"""
@module  : Connect.py
@author  : Rinne
@contact : minami.rinne.me@gmail.com
@time    : 2019/08/03
"""


class user_information(DictModel):
    pk = ["uid"]
    fields = ["phone", "email", "username", "pwd", "appid", "clientId", "timestamp", "login_channel", "extra_payload",
              "user_payload", "state"]


class login_information(DictModel):
    pk = ["id"]
    fields = ["uid", "username", "phone", "email", "login_success", "token", "request_id", "appid", "clientId",
              "timestamp", "login_channel", "user_ip", "remote_ip", "extra_payload", "user_payload"]


class DataBaseControl:

    @staticmethod
    def get_user_information_by_email(email):
        return user_information.get_one(email=email)

    @staticmethod
    def get_user_information_by_phone(phone):
        return user_information.get_one(phone=phone)

    @staticmethod
    def get_user_information_by_username(username):
        return user_information.get_one(username=username)

    @staticmethod
    def get_user_many(u_key, user_list):
        users = user_information.select().where_in(u_key, user_list).get()
        for user in users:
            del user["pwd"]
        return users

    @staticmethod
    def login_operating_information_update(**kwargs):
        login_information.new(**kwargs).insert()

    @staticmethod
    def sign_in_information(**kwargs):
        user_information.new(**kwargs).insert()

    @staticmethod
    def update_information_by_email(email, info_dict):
        new_info = user_information.get_one(email=email)
        for k, v in info_dict.items():
            new_info[k] = v
        new_info.update()

    @staticmethod
    def update_information_by_phone(phone, info_dict):
        new_info = user_information.get_one(phone=phone)
        for k, v in info_dict.items():
            new_info[k] = v
        new_info.update()

    @staticmethod
    def update_information_by_username(username, info_dict):
        new_info = user_information.get_one(username=username)
        for k, v in info_dict.items():
            new_info[k] = v
        new_info.update()

    @staticmethod
    def delete_information(info_dict):
        user_information.update_query().set(state=-1).where_in("username", info_dict).go()
