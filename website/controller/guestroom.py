import requests
from flask import Flask,request,current_app,jsonify,render_template,json
from website import tools
from website.config import Conf
from . import vi


api = Conf.API_ADDRESS

@vi.route("/manage_center/room_default/<int:hs_id>")
@tools.check_user_wrapper
def room_default(hs_id):
    # 获取房源信息
    current_user = tools.get_current_user()
    username = request.cookies.get("username")
    response = requests.get(api + "/api/v1.0/get_houseresources_by_hs_id/" + str(hs_id))
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        entity = response_data["message"]
    # 获取该房源下的所有客房列表
    response_room = requests.get(api + "/api/v1.0/get_guestroom_by_hsId/" + str(hs_id))
    response_room_data = json.loads(response_room.content)
    if response_room_data["code"] == 1:
        roomlist = response_room_data["message"]
    return render_template("/hcenter/room_default.html",username=username,user_id=current_user['user_id'],entity = entity,roomlist=roomlist)

@vi.route("/room_detail/<int:hs_id>/<int:gr_id>")
@tools.check_user_wrapper
def room_detail(hs_id,gr_id):
    #current_user = tools.get_current_user()
    username = request.cookies.get("username")
    response = requests.get(api+"/api/v1.0/get_houseresources_by_hs_id/"+str(hs_id))
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        entity = response_data["message"]
    #根据gr_id获取客房
    response_room = requests.get(url=api + "/api/v1.0/get_guestroom_by_gr_id/" + str(gr_id))
    response_room_data = json.loads(response_room.content)
    if response_room_data['code'] == 1:
        room = response_room_data['message']
    return render_template("/hcenter/room_details.html", username=username, hs_id=entity['hs_id'],gr_id=room['gr_id'],entity=entity,room=room)


@vi.route('/manage_center/room_add/<int:hs_id>')#  hs_id 房源的主键ID
@tools.check_user_wrapper
def room_add(hs_id):
    # 获取房源信息
    username = request.cookies.get("username")
    response = requests.get(api + "/api/v1.0/get_houseresources_by_hs_id/" + str(hs_id))
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        entity = response_data["message"]
    response_room = requests.get(api + "/api/v1.0/get_guestroom_by_hsId/" + str(hs_id))
    response_room_data = json.loads(response_room.content)
    if response_room_data["code"] == 1:
        roomlist = response_room_data["message"]
        rooms_name = []
        for m in roomlist:
            rooms_name.append(m['gr_name'])
    return render_template("/hcenter/room_add.html",username=username,house_name = entity['hs_name'],house_id = entity['hs_id'],rooms_name=rooms_name)

#添加客户
@vi.route("/manage_center/do_insert_guestroom",methods=['POST'])
#@tools.check_user_wrapper
def do_insert_guestroom():
    hs_id = request.json.get('hs_id')
    gr_name = request.json.get('gr_name')
    gr_price = request.json.get('gr_price')
    gr_desc = request.json.get('gr_desc')
    gr_images = request.json.get('gr_images')
    gr_status = request.json.get('gr_status')
    # 详细信息
    gr_room_type = request.get_json().get("gr_room_type")
    gr_room_area = request.get_json().get("gr_room_area")
    gr_bed_type = request.get_json().get("gr_bed_type")
    gr_bed_count = request.get_json().get("gr_bed_count")
    gr_settings = request.get_json().get("gr_settings")

    data = json.dumps({
        'hs_id':hs_id,
        'gr_name':gr_name,
        'gr_price':gr_price,
        'gr_desc':gr_desc,
        'gr_images':gr_images,
        'gr_status':gr_status,
        'gr_room_type': gr_room_type,
        'gr_room_area': gr_room_area,
        'gr_bed_type': gr_bed_type,
        'gr_bed_count': gr_bed_count,
        'gr_settings': gr_settings,
    })
    response = requests.post(url=api+'/api/v1.0/gr_insert',
                             data=data,
                             headers = {"content-type":"application/json"}
                             )
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({'code': 1,"message":"添加成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

@vi.route('/manage_center/room_edit/<int:hs_id>/<int:gr_id>')
#@tools.check_user_wrapper
def room_edit(hs_id,gr_id):  # hs_id 房源ID; gr_id 客房主键ID
    #current_user = tools.get_current_user()
    username = request.cookies.get("username")
    response = requests.get(url=api+"/api/v1.0/get_houseresource_by_hs_id/"+str(hs_id))
    response_data=json.loads(response.content)
    if response_data['code'] == 1:
        entity = response_data['message']
    response_room = requests.get(url=api + "/api/v1.0/get_guestroom_by_gr_id/" + str(gr_id))
    response_room_data = json.loads(response_room.content)
    if response_room_data['code'] == 1:
        room = response_data['message']
    return render_template("/hcenter/room_edit.html",username=username,hs_id = entity['hs_id'],gr_id=room['gr_id'],entity=entity,room=room)


@vi.route("/manage_center/get_all_rooms_by_hs_id")
def get_all_rooms_by_hs_id():
    hs_id = request.json.get("hs_id")
    response = requests.get(url=api + "/api/v1.0/get_guestroom_by_hsId/" + str(hs_id))
    response_data = json.loads(response.content)
    if response_data['code'] == 1:
        room_list = response_data['message']
        return jsonify({'code': 1, 'message': room_list})
    return jsonify({'code': 0, 'message': '查询失败'})

#编辑客户
@vi.route("/manage_center/do_update_guestroom",methods=['POST'])
@tools.check_user_wrapper
def do_update_guestroom():
    gr_id = request.json.get("gr_id")
    hs_id = request.json.get("hs_id")
    gr_name = request.json.get("gr_name")
    gr_price = request.json.get("gr_price")
    gr_desc = request.json.get("gr_desc")
    gr_images = request.json.get('gr_image')
    gr_status = request.json.get('gr_status')

    data = json.dumps({
        "gr_id":gr_id,
        "hs_id":hs_id,
        "gr_name":gr_name,
        "gr_price":gr_price,
        "gr_desc":gr_desc,
        "gr_images":gr_images,
        "gr_status":gr_status
    })
    response = requests.put(url=api+"/api/v1.0/gr_update/"+gr_id,
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
@vi.route("/manage_center/do_delete_guestroom",methods=['POST'])
@tools.check_user_wrapper
def do_delete_guestroom():
    gr_id = request.json.get("gr_id")
    response = requests.delete(url=api+"/api/v1.0/gr_delete/"+gr_id,
                  headers={"content-type":"application/json"})
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"删除成功"})
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

@vi.route("/manage_center/do_search_guestroom")
def do_search_guestroom():
    response = requests.get(url=api+"/api/v1.0/get_all_guest_room")
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"查询成功"})
    if response_data["code"] == 0:
        return jsonify({"code":0,"message":"查询失败"})
    return jsonify({"code":0,"message":"参数错误"})





