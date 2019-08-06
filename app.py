import logging
import pymysql

from flask import Flask, request
from control.Sever import CampSever
from common.Riko import Riko

"""
@module  : app.py
@author  : Rinne
@contact : yejunbin123@qq.com
@time    : 2019/08/03
"""

app = Flask(__name__)


@app.route("/")
def index():
    return "test"


@app.route("/api/sauth", methods=["POST"])
def log_in():
    if request.method == "POST":
        return CampSever.login_control(request.json)


@app.route("/api/user", methods=["POST"])
def sign_in():
    pass


@app.route("/api/user", methods=["PUT"])
def update_user():
    pass


@app.route("/api/user", methods=["GET"])
def get_user_list():
    pass


@app.route("/api/user", methods=["PUT"])
def delete_user():
    pass


if __name__ == "__main__":

    Riko.db_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "123456",
        "db": "camptalk",
        "charset": "utf8",
        "autocommit": True,
        "cursorclass": pymysql.cursors.DictCursor
    }

    log = logging.getLogger(__name__)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(filename)s file line:%(lineno)d %(levelname)s: %(message)s')
    logging.basicConfig(filename='example.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(filename)s line:%(lineno)d %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)

    app.run(debug=True)
