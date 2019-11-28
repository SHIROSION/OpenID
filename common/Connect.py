#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@module  : Connect.py
@author  : Rinne
@contact : minami.rinne.me@gmail.com
@time    : 2019/08/03
"""
import json
import logging

import pymysql
from common.Riko import Riko, DictModel, ObjectModel, INSERT


class user_information(DictModel):
    pk = ["uid"]
    fields = ["phone", "email", "username", "pwd", "appid", "clientId", "timestamp", "login_channel", "extra_payload",
              "user_payload", "state"]


class login_information(DictModel):
    pk = ["id"]
    fields = ["uid", "username", "phone", "email", "login_success", "token", "request_id", "appid", "clientId",
              "timestamp", "login_channel", "user_ip", "remote_ip", "extra_payload", "user_payload"]


class verification_code(DictModel):
    pk = ["index"]
    fields = ["username", "email", "code", "timestamp", "type"]


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
    def check_username_and_email(username, email):
        get_info = user_information.select() \
            .where_raw("username = %(input_username)s OR email = %(input_email)s") \
            .get({"input_username": username, "input_email": email})
        return get_info

    @staticmethod
    def delete_information(username):
        user_information.update_query().set(state=-1).where_in("username", username).go()

    @staticmethod
    def get_verification_code(email):
        get_info = verification_code.get_many(email=email)
        return get_info

    @staticmethod
    def insert_verification_code(**kwargs):
        verification_code.new(**kwargs).insert()

    @staticmethod
    def delete_expired_verification_code(now_times):
        verification_code.delete_query() \
            .where_raw("%(current_ts)s - timestamp > 120") \
            .go({'current_ts': now_times})

    @staticmethod
    def get_new_one_verification_code(email):
        return verification_code.select() \
            .where(email=email) \
            .order_by("timestamp DESC") \
            .limit(1) \
            .only()


# if __name__ == "__main__":
#     with open("camptalk_db.json", "r") as file:
#         config = json.loads(file.read())
#     config["cursorclass"] = pymysql.cursors.DictCursor
#     Riko.db_config = config
#     log = logging.getLogger(__name__)
#     formatter = logging.Formatter(
#         '%(asctime)s %(name)s %(filename)s file line:%(lineno)d %(levelname)s: %(message)s')
#     logging.basicConfig(filename='example.log',
#                         level=logging.DEBUG,
#                         format='%(asctime)s %(name)s %(filename)s line:%(lineno)d %(levelname)s: %(message)s')
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.DEBUG)
#     console_handler.setFormatter(formatter)
#     log.addHandler(console_handler)
#     print(DataBaseControl.get_new_one_verification_code("yejunbin123@qq.com"))

