import logging
import pymysql

from flask import Flask, request, json
from control.Server import CampServer
from common.Riko import Riko

"""
@module  : app.py
@author  : Rinne
@contact : yejunbin123@qq.com
@time    : 2019/08/03
"""

app = Flask(__name__)

with open("camptalk_db.json", "r") as file:
    config = json.loads(file.read())
config["cursorclass"] = pymysql.cursors.DictCursor
Riko.db_config = config


@app.route("/")
def index():
    return "test"


@app.route("/api/sauth", methods=["POST"])
def log_in():
    if request.method == "POST":
        return json.dumps(CampServer.login_control(request.json))


@app.route("/api/user", methods=["POST"])
def sign_in():
    if request.method == "POST":
        return json.dumps(CampServer.sign_in_control(request.json))


@app.route("/api/user", methods=["PUT"])
def update_user():
    if request.method == "PUT":
        return json.dumps(CampServer.update_control(request.json))


@app.route("/api/user", methods=["GET"])
def get_user_list():
    if request.method == "GET":
        return json.dumps(CampServer.get_user_list_control(request.json))


@app.route("/api/user", methods=["DELETE"])
def delete_user():
    if request.method == "DELETE":
        return json.dumps(CampServer.delete_user_control(request.json))


if __name__ == "__main__":
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
