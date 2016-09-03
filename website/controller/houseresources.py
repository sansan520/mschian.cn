import requests
from flask import render_template,request,jsonify,json,redirect,url_for,current_app
from website.model import HouseOwner,HouseResources,HouseType
from website.config import Conf
from website import tools

from .import vi


@vi.route("/manage_center/house_default")
@tools.check_user_wrapper
def house_default():
    # 获取user_id,根据user_id获取当前用户对应的所有房源列表,以及默认第一个房源信息
    current_user = tools.get_current_user()
    username = request.cookies.get("username")

    return render_template('/hcenter/house_default.html',user_id=current_user['user_id'],username=username)

@vi.route("/manage_center/house_details/<int:hs_id>")
@tools.check_user_wrapper
def house_details(hs_id):
    current_user = tools.get_current_user()
    username = request.cookies.get("username")
    if hs_id > 0:
        response = requests.get(Conf.API_ADDRESS + "/api/v1.0/get_houseresources_by_hs_id/" + str(hs_id))
        response_data = json.loads(response.content)
        if response_data["code"] == 1:
            house_entity = response_data["message"]
            return render_template('/hcenter/house_details.html', username=username, entity=house_entity,
                                   user_id=current_user['user_id'])
    return render_template('/hcenter/house_details.html')


@vi.route("/manage_center/get_resource_by_user_id", methods=['POST'])
def get_resource_by_user_id():
    user_id = request.json.get("user_id")
    # user_id ="1"
    response = requests.get(Conf.API_ADDRESS + "/api/v1.0/get_resource_by_user_id/" + user_id)
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        house_list = response_data["message"]
        return jsonify({'code': 1, 'message': house_list})
    return jsonify({'code': 0, 'message': '查询失败'})



@vi.route("/manage_center/house_edit/<int:hs_id>")
def house_edit(hs_id):
    current_user = tools.get_current_user()
    username = request.cookies.get("username")
    if hs_id > 0:
        response = requests.get(Conf.API_ADDRESS + "/api/v1.0/get_houseresources_by_hs_id/" + str(hs_id))
        response_data = json.loads(response.content)
        if response_data["code"] == 1:
            house_entity = response_data["message"]
            return render_template('/hcenter/house_edit.html',username=username,entity=house_entity,user_id=current_user['user_id'])
    return render_template('/hcenter/house_edit.html')

@vi.route("/manage_center/house_add")
@tools.check_user_wrapper
def house_add():
    current_user = tools.get_current_user()
    username = request.cookies.get("username")
    return render_template("/hcenter/house_add.html",username=username,user_id=current_user['user_id'])


@vi.route("/manage_center/do_hs_insert",methods=['POST'])
#将JS Post过来的参数转化成Json格式
@tools.check_user_wrapper
def do_hs_insert():
    api = Conf.API_ADDRESS
    current_user = tools.get_current_user()
    user_id = current_user['user_id']

    hs_name = request.json.get("hs_name")
    hs_intro = request.json.get("hs_intro")
    hs_province = request.json.get("hs_province")
    hs_city = request.json.get("hs_city")
    hs_country = request.json.get("hs_country")
    hs_address = request.json.get("hs_address")
    # hs_hitvalume = request.json.get("hs_hitvalume") # 点击量由后台统计
    hs_images = request.json.get("hs_images")
    hs_status = request.json.get("hs_status")

    data = json.dumps({
        "user_id":user_id,
        "hs_name":hs_name,
        "hs_intro":hs_intro,
        "hs_province":hs_province,
        "hs_city":hs_city,
        "hs_country":hs_country,
        "hs_address":hs_address,
        #"hs_hitvalume":0,  # 统计数初始化为0
        "hs_images":hs_images,  # 多张图片以|分隔,最多3张
        "hs_status":hs_status
    })
    #data = json.dumps({})
    #访问service api
    response = requests.post(api+"/api/v1.0/hs_insert",
                  data = data,
                  headers = {"content-type":"application/json"}
                  )
    response_data = json.loads(response.content)
    #  code = 0 添加失败
    if response_data["code"] == 0:
        return jsonify({'code':0,'message':'添加失败'})
    # code = 1 添加成功
    if response_data["code"] == 1:
        return jsonify({'code': 1, 'message': '添加成功'})

#  加载用户添加的房源
@vi.route("/manage_center/do_loadhs")
def do_loadhs():
    # username = request.cookies.get("username")
    # password = request.cookies.get("password")
    # user_hash_account = tools.get_hash_account(username,password)
    # current_user = current_app.session_redis.hget("user %s " % user_hash_account,"current_user")
    # if current_user:
    #     current_user = eval(current_user)
    current_user = tools.get_current_user()
    user_id = current_user['user_id']
    api = Conf.API_ADDRESS
    response = requests.get(api+"/api/v1.0/get_resource_by_user_id/"+user_id)
    response_data = json.loads(response.content)
    #code = 0查询失败
    if response_data["code"] == 0:
        return jsonify(response_data)
    #code = 1 查询成功
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"success"})


#编辑房源
@vi.route("/manage_center/do_ediths",methods=['POST'])
@tools.check_user_wrapper
def do_ediths():
    api = Conf.API_ADDRESS
    current_user = tools.get_current_user()
    user_id = current_user['user_id']
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "房源不存在"})
    hs_name = request.json.get("hs_name")
    hs_intro = request.json.get("hs_intro")
    hs_province = request.json.get("hs_province")
    hs_city = request.json.get("hs_city")
    hs_country = request.json.get("hs_country")
    hs_address = request.json.get("hs_address")
    hs_images = request.json.get("hs_images")
    hs_status = request.json.get("hs_status")

    data = json.dumps({
                       "user_id": user_id,
                       "hs_name": hs_name,
                       "hs_intro": hs_intro,
                       "hs_province": hs_province,
                       "hs_city": hs_city,
                       "hs_country": hs_country,
                       "hs_address": hs_address,
                       "hs_images": hs_images,
                       "hs_status": hs_status
                       })
    response = requests.put(api+"/api/v1.0/hs_edit/"+hs_id,
                            data=data,
                            headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0编辑失败
    if response_data["code"] == 0:
        return jsonify(response_data)

    # code = 1 编辑成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "message": "success"})



#删除房源
@vi.route("/manage_center/do_delete_hs",methods=['POST'])
def do_delete_hs():
    api = Conf.API_ADDRESS
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "房源不存在"})
    #data = json.dumps({"hs_id": hs_id})
    response = requests.delete(api+"/api/v1.0/hs_delete/"+str(hs_id),
                            headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0删除失败
    if response_data["code"] == 0:
        return jsonify(response_data)

    # code = 1 删除成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "message": "删除成功"})


#根据点击量的提升更新房源类型
@vi.route("/manage_center/do_update_type",methods=['POST'])
def do_update_type():
    api = Conf.API_ADDRESS
    ty_id = request.json.get("ty_id")
    if not ty_id:
        return jsonify({"code": 0, "message": "房源类型不存在"})
    hitvalue = request.json.get("hs_hitvalume")
    if not hitvalue:
        return jsonify({"code":0,"message":"点击量达不到升级标准"})
    data = json.dumps({"ty_id":ty_id,
                       "hs_hitvalume":hitvalue})
    response = requests.put(api+"/api/v1.0/update_ty_id",
                 data = data,
                 headers = {"content-type":"application/json"}
                 )
    response_data = json.loads(response.content)
    #更新成功 code = 1
    if response_data['code'] == 1:
        return jsonify({"code":1,"message":"更新成功"})
    #code = 0 更新失败
    if response_data["code"] == 0:
        return jsonify(response_data)



