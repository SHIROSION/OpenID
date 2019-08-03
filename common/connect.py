import pymysql

"""
@module  : connect.py
@author  : Rinne
@contact : yejunbin123@qq.com
@time    : 2019/08/03
"""

class DataBaseControl:
    def __init__(self):
        self.connect = pymysql.connect(
        )