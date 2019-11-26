#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@module  : EmailServer.py
@author  : Rinne
@contact : minami.rinne.me@gmail.com
@time    : 2019/11/21 午前 02:59
"""
import json
import smtplib
from email.mime.text import MIMEText


class EmailServer:
    def __init__(self):
        with open("control/RGMailAccount.json", "r", encoding="UTF-8") as file:
            self.__config = json.loads(file.read())

    def new_user_mail(self, user_email, code):
        self.__send_email(
            self.__config.get("bindVerifyCodeMailFormat").format(code),
            user_email,
            self.__config.get("newUserMailTitle")
        )

    def bind_user_mail(self, user_info):
        pass

    def new_password_mail(self, user_info):
        pass

    def __send_email(self, text, receiver, title):
        __user = self.__config.get("user")
        __pwd = self.__config.get("pwd")
        __mail_host = self.__config.get("mailHost")
        __main_port = self.__config.get("sendMailPort")

        message = MIMEText(text, "plain", "utf-8")
        message["From"] = __user
        message["To"] = receiver
        message["Subject"] = title

        send_email_server = smtplib.SMTP_SSL(__mail_host, __main_port)
        send_email_server.login(__user, __pwd)
        send_email_server.sendmail(__user, receiver, message.as_string())
