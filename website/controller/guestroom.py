import requests
from flask import Flask,request,current_app,jsonify,render_template,json
from website import tools
from website.config import Conf
from . import vi


api = Conf.API_ADDRESS
@vi.route('insert_guestroom')
def insert_guestroom():
    return render_template("/guestroom.html")

#添加客户
@vi.route("/do_insert_guestroom",methods=['POST'])
def insert_guestroom():

    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if username and password:
        user_hash_account = tools.get_hash_hashlib(username,password)
        current_user = current_app.session_redis.hget('user%' % user_hash_account,'current_user')
        #判断用户是否登录，用户登录，从缓存中得到房源id
        if current_user:
            current_user = current_user.decode()
            hs_id = current_user['username']
        else:
            return jsonify({"code":0,"message":"您还未登录,请先登录"})
    gr_name = request.json.get('gr_name')
    gr_price = request.json.get('gr_price')
    gr_describe = request.json.get('gr_describe')
    data = json.dumps({
        'hs_id':hs_id,
        'gr_name':gr_name,
        'gr_price':gr_price,
        'gr_describe':gr_describe
    })
    response = requests.post(url=api+'/api/v1.0/gr_insert',data=data,
                  headers = {"ContentType":"application/json"})
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"statue":1,"message":"添加成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

#编辑客户
@vi.route("/do_update_guestroom",methods=['POST'])
def update_guestroom():
    username = requests.cookies.get("username")
    password = requests.cookies.get("password")
    user_hash_hashlib = tools.get_hash_account(username,password)
    current_user = current_app.session_redis.hget("user%" % user_hash_hashlib,"current_user")
    if current_user:
        current_user = current_user.decode()
        hs__id = current_user["username"]
    else:
        return jsonify({"code":0,"message":"您还未登录,请先登录"})
    gr_id = request.json.get("gr_id")
    gr_name = request.json.get("gr_name")
    gr_price = request.json.get("gr_price")
    gr_describe = request.json.get("gr_describe")
    data = json.dumps({
        "gr_id":gr_id,
        "hs_id":hs__id,
        "gr_name":gr_name,
        "gr_price":gr_price,
        "gr_describe":gr_describe
    })
    response = requests.post(url=api+"/api/v1.0/gr_update/<int:gr_id>",
                  data=data,
                  headers={"ContentType":"application/json"})
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"添加成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

#删除客户
@vi.route("/do_delete_guestroom",methods=['POST'])
def delete_guestroom():
    username = requests.cookies.get("username")
    password = requests.cookies.get("password")
    user_hash_hashlib = tools.get_hash_account(username, password)
    current_user = current_app.session_redis.hget("user%" % user_hash_hashlib, "current_user")
    if current_user:
        current_user = current_user.decode()
        gr__id = current_user["username"]
    else:
        return jsonify({"code": 0, "message": "您还未登录,请先登录"})
    data = json.dumps({"gr_id":gr__id})
    response = requests.post(url=api+"/api/v1.0/gr_delete/"+gr__id,
                  data=data,
                  headers={"contenttype":"application/json"})
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"删除成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

@vi.route("/do_search_guestroom")
def search_guestroom_all():
    response = requests.get(url=api+"/api/v1.0/get_all_guest_room",headers={"contenttype":"application/json"})
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"查询成功"})
    if response_data["code"] == 0:
        return jsonify({"code":0,"message":"查询失败"})
    return jsonify({"code":0,"message":"参数错误"})





