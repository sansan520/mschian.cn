# coding : utf-8
from flask import render_template
from . import vi
import requests
import json
from flask import jsonify,request,g,current_app,redirect,url_for
from website.model import HouseOwner
from website.config import Conf


@vi.route("/ho_register")
def house_owner_register():
    return render_template("homestay.html")


@vi.route("/do_ho_register", methods=["POST"])
def do_ho_register():
    # 接收JS POST 过来的参数,并进行验证
    ho_name = request.get_json.get("ho_name")
    if not ho_name:
        return jsonify({"code": 0, "message": "用户姓名不能为空"})
    ho_mobile = request.get_json().get("ho_mobile")
    ho_tel = request.get_json().get("ho_tel")
    ho_email = request.get_json().get("ho_email")
    ho_nicard = request.get_json().get("ho_nicard")

    #获取参数后,将这些数据,通过接口传给service api==> http://localhost:8080/接口名称
    data =json.dumps({"ho_name": ho_name,
            "ho_mobile" :ho_mobile,
            "ho_tel" : ho_tel,
            "ho_email" : ho_email,
            "ho_nicard" : ho_nicard,
            })
    api = Conf.API_ADDRESS
    # service api 返回的 response
    response = requests.post(url=api+"/api/v1.0/ho_register",
                                 data=data,
                                 headers={"content-type": "application/json"})
    #json格式化并返回JS
    response_data = json.loads(response.content)

    #return jsonify(response_data)
    if response_data["code"] == 0:
        return jsonify(response_data)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"注册成功","go_url":"/index"})

@vi.route("user_register")
def user_register():
    return render_template("visitor.html")

@vi.route("/do_user_register",methods = ["POST"])
def do_user_register():
    user_account = request.json.get("user_account")
    if not user_account:
        return jsonify({"code":0,"message":"用户名不能为空"})
    user_password = request.json.get("user_password")
    if not user_password:
        return jsonify({"code": 0, "message": "密码不能为空"})
    user_mobile = request.json.get("user_mobile")
    if not user_account:
        return jsonify({"code": 0, "message": "手机号不能为空"})
    user_headimg = request.json.get("user_headimg")
    user_type = request.json.get("user_type")

    data=json.dumps({
        "user_account":user_account,
        "user_password":user_password,
        "user_mobile":user_mobile,
        "user_headimg":user_headimg,
        "user_type":user_type
    })
    api = Conf.API_ADDRESS
    response = requests.post(url=api+"/api/v1.0/user_register",
                            data = data,
                            headers = {"contentType":"application/json"})
    response_data = json.loads(response.content)
    #code =1 注册成功
    if response_data['code'] == 1:
        return jsonify({"code":1,"message":"注册成功","go_url":"/index"})
    #code = 0 注册失败
    if response_data['code'] == 0:
        return jsonify(response_data)
    return jsonify(response_data)
