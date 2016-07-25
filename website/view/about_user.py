# coding : utf8

import hashlib
import requests
from flask import render_template, jsonify, request, json, current_app, make_response

from website import tools
from website.config import Conf
from website.model import HouseOwner
from . import vi
import website.tools

# http://www.361way.com/python-hashlib-md5-sha/4249.html  => hashlib
# http://www.cnblogs.com/agmcs/p/4445428.html
#
# http://www.programcreek.com/python/example/51515/flask.Response

@vi.route("/login")
def login():
    return render_template("login.html")

@vi.route("/do_login", methods=['POST'])
def do_login():
    user_account = request.json.get("user_account")
    if not user_account:
        return jsonify({'code': 0, 'message': "账号不能为空"})

    user_password = request.json.get("user_password")
    if not user_password:
        return jsonify({'code': 0, 'message': '密码不能为空'})

    # response = make_response()
    # response.set_cookie('username', value=user_account, max_age=300)
    # response.set_cookie('password', value=user_password, max_age=300)
    # response.data = '{"code":"1","message":"scuess"}'  # response.data 返回json字符串
    # return response

    user_password_hash = hashlib.md5(user_password.encode('utf-8')).hexdigest()
    #  md5(123) = 202cb962ac59075b964b07152d234b70
    data = json.dumps({"user_account": user_account, "user_password": user_password_hash})
    api_url = Conf.API_ADDRESS
    response_data = requests.post(url=api_url+"/api/v1.0/user_login", data=data, headers={"content-type": "application/json"})
    result_data = json.loads(response_data.content)
    # code == 1登录成功
    if response_data['code'] == 1:
        # current_user = result_data['current_user']
        response = make_response()
        response.set_cookie('username', value=user_account, max_age=60*60*24*7)
        response.set_cookie('password', value=user_password_hash, max_age=60*60*24*7)  # cookie存储的是密码md5之后的hash
        response.data = '{"code":"1","message":"success"}'  # response.data 返回json字符串
        return response

    #code ==0 登录失败
    if response_data['code'] == 0:
        return jsonify({'code': 0, 'message': '登录失败'})
    return jsonify(result_data)

# json.dumps : dict转成str
# json.loads:str转成dict


# @vi.route("/register")
# def register():
#     return render_template("register.html")

@vi.route("/do_logout",methods=["POST"])
def do_logout():
    # 从redis中删除缓存
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    hash_account = tools.get_hash_account(username, password)
    if hash_account:
        result = current_app.session_redis.hdel('user:%s' % hash_account, 'current_user')
        return jsonify({'code': 1, 'message': '成功退出!', 'gourl': 'index'})
    return jsonify({'code': 1, 'message': '退出异常!', 'gourl': 'index'})

