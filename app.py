from flask import Flask

"""
@module  : app.py
@author  : Rinne
@contact : yejunbin123@qq.com
@time    : 2019/08/03
"""

app = Flask(__name__)


@app.route("/api/sauth", methods=["POST"])
def log_in_control():
    pass

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
