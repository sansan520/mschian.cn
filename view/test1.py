# coding = utf8
from flask import Flask,render_template,json,request,jsonify
import requests
from . import vi


@vi.route('/')
def hello_world():
    return render_template("index.html")

@vi.route('/index')
def index():
    return "index"


# #http://wjapi.wjw.cn/api/RegistLogon?Mobile=15957124901  = > post
# @app.route("/login", methods=['POST'])
# def get_data():
#     # data = json.loads(request.form.get('data'))
#     # account = data['account']
#     # password = data['password']
#     # wjapi返回类型：{"status": 1,"message": "sample string 2"}
#     response = requests.post(url="http://wjapi.wjw.cn/api/RegistLogon?Mobile=15957124901",
#                              data="",
#                              headers={"content-type": "application/json"})
#     response_data = json.loads(response.content)
#     return jsonify(response_data)

