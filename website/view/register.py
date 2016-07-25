# coding : utf-8
import requests
import hashlib
from flask import render_template,jsonify, request, json,jsonify,g,current_app,redirect,url_for,make_response,session
from . import vi
from website.model import HouseOwner,UserBase
from website.config import Conf


@vi.route("/register")
def register():
    return render_template("register.html")

@vi.route("/ho_register")
def house_owner_register():
    return render_template("register02.html")

@vi.route("/ho_next_register")
def ho_next_register():
    return render_template("register03.html")

#房东注册
@vi.route("/do_ho_register", methods=["POST"])
def do_ho_register():
    api = Conf.API_ADDRESS
    # 接收JS POST 过来的参数,并进行验证
    user_account = request.cookies.get('username')
    resp = requests.get(url=api+"/api/v1.0/get_by_account/"+user_account)
    resp_data = json.loads(resp.content.decode())
    if(resp_data['code'] ==1):
        result = resp_data['message']
        user_id = result[0]['user_id']
    ho_name = request.json.get("ho_name")
    if not ho_name:
        return jsonify({"code": 0, "message": "姓名不能为空"})

    ho_email = request.get_json().get("ho_email")
    if not ho_email:
        return jsonify({"code": 0, "message": "邮箱不能为空"})

    ho_nicard = request.get_json().get("ho_nicard")
    if not ho_nicard:
        return jsonify({"code": 0, "message": "证件照不能为空"})

    ho_tel = request.get_json().get("ho_tel")
    data = json.dumps({"user_id": user_id,
                       "ho_name": ho_name,
                       "ho_email": ho_email,
                       "ho_tel": ho_tel,
                       "ho_nicard": ho_nicard
                       })

    # 获取参数后,将这些数据,通过接口传给service api==> http://localhost:8080/接口名称
    response = requests.post(url=api + "/api/v1.0/ho_register",
                             data=data,
                             headers={"content-type": "application/json"})
    # service api 返回的 response
    #json格式化并返回JS
    response_data = json.loads(response.content)

    # code = 1房东注册成功
    if response_data['code'] == 1:
        return jsonify({"code": 1, "message": "注册成功", "go_url": "/index"})

    # code = 0房东注册失败
    if response_data['code'] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

#游客注册
@vi.route("/user_register")
def user_register():
    return render_template("register01.html")

@vi.route("/check_user_account",methods=["POST"])
def check_user_account():
    user_account = request.json.get("user_account")
    response = requests.get(url=Conf.API_ADDRESS + "/api/v1.0/get_by_account/"+user_account)
    response_data = json.loads(response.content.decode())
    code = response_data['code']
    if code==0:
        return jsonify({"code": 0, "message": "该账号可以使用"})
    if code==1:
        return jsonify({"code": 1, "message": "该用户已经存在"})

@vi.route("/check_user_mobile",methods=["POST"])
def check_user_mobile():
    user_mobile = request.json.get("user_mobile")
    response = requests.get(url=Conf.API_ADDRESS + "/api/v1.0/get_by_mobile/" + user_mobile)
    response_data = json.loads(response.content.decode())
    code = response_data['code']
    if code==0:
        return jsonify({"code": 0, "message": "该手机可以使用"})
    if code==1:
        return jsonify({"code": 1, "message": "该用户已经存在"})

@vi.route("/do_user_register",methods = ["POST"])
def do_user_register():
    user_account = request.json.get("user_account")
    if not user_account:
        return jsonify({"code":0,"message":"用户名不能为空"})
    user_password = request.json.get("user_password")
    if not user_password:
        return jsonify({"code": 0, "message": "密码不能为空"})

    user_password_hash = hashlib.md5(user_password.encode('utf-8')).hexdigest()
    user_mobile = request.json.get("user_mobile")
    if not user_mobile:
        return jsonify({"code": 0, "message": "手机号不能为空"})
    user_headimg = request.json.get("user_headimg")
    user_type = request.json.get("user_type")

    data=json.dumps({
        "user_account":user_account,
        "user_password":user_password_hash,
        "user_mobile":user_mobile,
        "user_headimg":user_headimg,
        "user_type":user_type
    })
    # data = json.dumps({"user_account": user_account, "user_password": user_password_hash})
    response_data = requests.post(url=Conf.API_ADDRESS+"/api/v1.0/user_register", data = data, headers={"content-type": "application/json"})
    result_data = json.loads(response_data.content)
    #code =1 注册成功
    if result_data['code'] == 1:
        #user_id = response_data['user_id']
        #user_type==1用户类型为游客
        if user_type == 1:
            response = make_response()
            response.set_cookie("username",value = user_account,max_age=60*60*24*7)
            response.set_cookie("userpassword",value = user_password_hash,max_age=60*60*24*7)
            response.data = '{"code":"1","message":"注册成功","user_type":1}'
            return response

        if user_type == 0:
            response = make_response()
            response.set_cookie("username", value=user_account, max_age=60*60*24*7)
            response.set_cookie("userpassword", value=user_password_hash, max_age=60*60*24*7)
            response.data = '{"code":"1","message": "注册成功","user_type":0}'
            return response
    #code = 0 注册失败
    if response_data['code'] == 0:
        return jsonify(result_data)
    return jsonify(result_data)
