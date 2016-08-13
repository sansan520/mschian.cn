import requests
from flask import Flask,request,current_app,jsonify,render_template,json
from website import tools
from website.config import Conf
from . import vi


api = Conf.API_ADDRESS

@vi.route("/room_default/<int:hs_id>")
def room_default(hs_id):
    # 获取房源信息
    response = requests.get(api + "/api/v1.0/get_houseresources_by_hs_id/" + str(hs_id))
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        entity = response_data["message"]
    # 获取该房源下的所有客房列表
    response_room = requests.get(api + "/api/v1.0/get_guestroom_by_hsId/" + str(hs_id))
    response_room_data = json.loads(response_room.content)
    if response_room_data["code"] == 1:
        roomlist = response_room_data["message"]
    return render_template("/hcenter/room_default.html",entity = entity,roomlist=roomlist)


@vi.route('/room_add/<int:hs_id>')   #  hs_id 房源的主键ID
def room_add(hs_id):
    # 获取房源信息
    response = requests.get(api + "/api/v1.0/get_houseresources_by_hs_id/" + str(hs_id))
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        entity = response_data["message"]
    return render_template("/hcenter/room_add.html",house_name = entity['hs_name'],house_id = entity['hs_id'])

#添加客户
@vi.route("/do_insert_guestroom",methods=['POST'])
@tools.check_user_wrapper
def do_insert_guestroom():

    # username = request.cookies.get('username')
    # password = request.cookies.get('password')
    # if username and password:
    #     user_hash_account = tools.get_hash_hashlib(username,password)
    #     current_user = current_app.session_redis.hget('user%' % user_hash_account,'current_user')
    #     #判断用户是否登录，用户登录，从缓存中得到房源id
    #     if current_user:
    #         current_user = eval(current_user)
    #         hs_id = current_user['username']
    #     else:
    #         return jsonify({"code":0,"message":"您还未登录,请先登录"})
    hs_id = request.json.get('hs_id')
    gr_name = request.json.get('gr_name')
    gr_price = request.json.get('gr_price')
    gr_desc = request.json.get('gr_desc')
    gr_images = request.json.get('gr_images')
    #gr_status = request.json.get('gr_status')
    data = json.dumps({
        'hs_id':hs_id,
        'gr_name':gr_name,
        'gr_price':gr_price,
        'gr_desc':gr_desc,
        'gr_images':gr_images
        #'gr_status':gr_status
    })
    response = requests.post(url=api+'/api/v1.0/gr_insert',
                             data=data,
                             headers = {"content-type":"application/json"}
                             )
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"statue":1,"message":"添加成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

@vi.route('/room_edit/<int:gr_id>')
def room_edit(gr_id):  # gr_id 客房主键ID
    response = request.get(url=api + "/api 1.0/get_guestroom_by_gr_id/" + gr_id)
    response_data = json.loads(response.content)
    if response_data['code'] == 1:
       entity=response_data['message']
    return render_template("/hcenter/room_edit.html",house_id = entity['hs_id'],room_name = entity['gr_name'],room_id = entity['gr_id'])


#编辑客户
@vi.route("/do_update_guestroom",methods=['POST'])
@tools.check_user_wrapper
def do_update_guestroom():
    # username = requests.cookies.get("username")
    # password = requests.cookies.get("password")
    # user_hash_hashlib = tools.get_hash_account(username,password)
    # current_user = current_app.session_redis.hget("user%" % user_hash_hashlib,"current_user")
    # if current_user:
    #     current_user = current_user.decode()
    #     hs__id = current_user["username"]
    # else:
    #     return jsonify({"code":0,"message":"您还未登录,请先登录"})
    gr_id = request.json.get("gr_id")
    hs_id = request.json.get("hs_id")
    gr_name = request.json.get("gr_name")
    gr_price = request.json.get("gr_price")
    gr_desc = request.json.get("gr_desc")
    gr_images = request.json.get('gr_image')
    #gr_status = request.json.get('gr_status')

    data = json.dumps({
        "gr_id":gr_id,
        "hs_id":hs_id,
        "gr_name":gr_name,
        "gr_price":gr_price,
        "gr_desc":gr_desc,
        "gr_images":gr_images
        #"gr_status":gr_status
    })
    response = requests.post(url=api+"/api/v1.0/gr_update/"+gr_id,
                             data=data,
                             headers={"content-type":"application/json"}
                             )
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"添加成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

#删除客户
@vi.route("/do_delete_guestroom",methods=['POST'])
@tools.check_user_wrapper
def do_delete_guestroom():
    # username = request.cookies.get("username")
    # password = request.cookies.get("password")
    # user_hash_hashlib = tools.get_hash_account(username, password)
    # current_user = current_app.session_redis.hget("user%" % user_hash_hashlib, "current_user")
    # if current_user:
    #     current_user = current_user.decode()
    #     gr__id = current_user["username"]
    # else:
    #     return jsonify({"code": 0, "message": "您还未登录,请先登录"})
    gr_id = request.json.get("gr_id")
    response = requests.post(url=api+"/api/v1.0/gr_delete/"+gr_id,
                  headers={"contenttype":"application/json"})
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"删除成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

@vi.route("/do_search_guestroom")
def do_search_guestroom():
    response = requests.get(url=api+"/api/v1.0/get_all_guest_room",headers={"ContentType":"application/json"})
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"查询成功"})
    if response_data["code"] == 0:
        return jsonify({"code":0,"message":"查询失败"})
    return jsonify({"code":0,"message":"参数错误"})





