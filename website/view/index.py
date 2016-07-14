# coding = utf8
from flask import Flask, render_template, json, request, jsonify, session
import requests
from . import vi
from website.model import HouseOwner
from website.config import Conf

@vi.route('/')
@vi.route('/index')
def index():
    api_address = Conf.API_ADDRESS
    current_user = session.get('current_user', '') # json
    if current_user == '':
        username = ''
    else:
        username = current_user['ho_account']
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

    # return render_template("index.html", username=username, hot4index=hot4index, special=special, goden=goden)
    return render_template("index.html", **locals()) # **locals() 将本地参数全部传到index.html,并可以直接使用


