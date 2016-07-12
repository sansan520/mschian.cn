# coding : utf8

import flask_login
import requests
from flask import render_template, jsonify, request, json, redirect, url_for
from website.config import Conf
from website.model import HouseOwner
from . import vi


# http://www.cnblogs.com/agmcs/p/4445428.html


@vi.route("/login")
def login():
    return render_template("login.html")

@vi.route("/do_login", methods=['POST'])
def do_login():

    u_name = request.json.get("ho_account")
    if not u_name:
        return jsonify({'code': 0, 'message': "账号不能为空"})
    u_password = request.json.get("ho_password")
    if not u_password:
        return jsonify({'code': 0, 'message': '密码不能为空'})
    data = json.dumps({"ho_account": u_name, "ho_password": u_password})
    # api_url = Conf.API_ADDRESS
    response = requests.post(url="http://localhost:8080/api/v1.0/ho_login", data=data, headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code == 1登录成功
    if response_data['code'] == 1:
        user = HouseOwner()
        user.ho_id = 1
        user.ho_account = response_data['acount']

        return redirect(url_for('vi.index'))
    #code ==0 登录失败
    if response_data['code'] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

# json.dumps : dict转成str
# json.loads:str转成dict


@vi.route("/register")
def register():
    return render_template("register.html")

@vi.route("/do_logout")
def do_logout():
    # remove the username from the session if it's there
    flask_login.logout_user()
    # session.pop('username', None)
    return redirect(('index'))

