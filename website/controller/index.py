# coding = utf8
from flask import Flask, render_template, json, request, jsonify, current_app
import requests
from . import vi
from website.model import HouseOwner
from website.config import Conf
from website import tools
import hashlib
#import website.tools

@vi.route('/')
@vi.route('/index')
def index():
    api_address = Conf.API_ADDRESS

    # 从cookie获取值
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if username and password:
        user_hash_account = tools.get_hash_account(username, password)  # 2dd99d263ecc5ebf25b91d2532b46080
        # # 从session_redis中获取数据,查看用户是否已经登录
        # hmget一次取多个值,hget一个值 ,hkeys返回list,HGETALL返回dict
        current_user = current_app.session_redis.hget('user:%s' % user_hash_account, 'current_user')
        if current_user:
            current_user = current_user.decode()
            login_user = username  # current_user[b'user_account'].decode()

    # 从接口获取热门目的地房源:/api/v1.0/get_hot_source4index
    try:
        response = requests.get(url=api_address + "/api/v1.0/get_hot_source4index")
        response_data = json.loads(response.content)
        if response_data['code'] == 1:
            hot4index = response_data['message']  #list
    except Exception as e:
        hot4index = None
    # 从接口获取特色房源
    try:
        response = requests.get(url=api_address + "/api/v1.0/get_special_resources4index")
        response_data = json.loads(response.content)
        if response_data['code'] == 1:
            special = response_data['message']  # list

    except Exception as e:
        special = None
    # 从接口获取金牌房源
    try:
        response = requests.get(url=api_address + "/api/v1.0/get_goden_resources4index")
        response_data = json.loads(response.content)
        if response_data['code'] == 1:
            goden = response_data['message']  # list
    except Exception as e:
        goden = None

    #return render_template("index.html", username=username, hot4index=hot4index, special=special, goden=goden)
    return render_template("/index.html", **locals()) # **locals() 将本地参数全部传到index.html,并可以直接使用


