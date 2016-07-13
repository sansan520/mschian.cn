# coding = utf8
from flask import Flask, render_template, json, request, jsonify, session
import requests
from . import vi
from website.model import HouseOwner

@vi.route('/')
@vi.route('/index')
def index():
    current_user = session.get('current_user', '') # json
    if current_user == '':
        username = ''
    else:
        username = current_user['ho_account']
    # 从接口获取热门房源:/api/v1.0/get_hot_source4index
    # headers = {"content-type": "application/json"}
    response = requests.get(url="http://localhost:8080/api/v1.0/get_hot_source4index")
    response_data = json.loads(response.content)
    if response_data['code'] == 1:
        hot4index = response_data['message']  #list
    # hot4index = [{'ho_id': 1, 'ty_id': 1, 'hs_province': '河南', 'hs_city': '濮阳', 'hs_id': 1, 'hs_images': 'http://img1.zzkcdn.com/rr177bea245c40fcf79732ce1b1fe4c1/2000x1500.jpg-homepic800x600.jpg', 'hs_address': '莽劳而无功枯', 'hs_country': '濮阳', 'hs_hitvalume': '0'}, {'ho_id': 1, 'ty_id': 1, 'hs_province': '浙江', 'hs_city': '杭州', 'hs_id': 2, 'hs_images': 'http://img1.zzkcdn.com/rr177bea245c40fcf79732ce1b1fe4c1/2000x1500.jpg-homepic800x600.jpg', 'hs_address': 'xxxxx', 'hs_country': '存在', 'hs_hitvalume': '0'}, {'ho_id': 1, 'ty_id': 4, 'hs_province': '浙江', 'hs_city': '杭州', 'hs_id': 3, 'hs_images': 'http://img1.zzkcdn.com/rr177bea245c40fcf79732ce1b1fe4c1/2000x1500.jpg-homepic800x600.jpg', 'hs_address': 'xxxxx', 'hs_country': '存在', 'hs_hitvalume': '0'}]
    return render_template("index.html", username=username, hot4index=hot4index)


