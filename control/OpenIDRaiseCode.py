#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@module  : OpenIDRaiseCode.py
@author  : Rinne
@contact : minami.rinne.me@gmail.com
@time    : 2019/11/20 午前 11:33
"""
from enum import IntEnum


class OpenIDRaiseCode(IntEnum):
    not_existed = 1001
    has_existed = 1002
    insert_fail = 1003
    del_fail = 1004
    lack_param = 1005
    update_fail = 1006
    database_error = 1007
    timeout = 1008
    frequent = 1009
    server_error = 1010
    auth_fail = 1011
    verify_code_incorrect = 1012
    password_incorrect = 1013
    user_has_existed = 1014
