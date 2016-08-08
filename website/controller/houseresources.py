import requests
from flask import render_template,request,jsonify,json,redirect,url_for,current_app
from website.model import HouseOwner,HouseResources,HouseType
from website.config import Conf
from website import tools

from .import vi


@vi.route("/house_default")
@tools.check_user_wrapper
def house_default():
    # 获取user_id,根据user_id获取当前用户对应的所有房源列表,以及默认第一个房源信息
    # current_user = tools.get_current_user()
    # if current_user is not None:
        # user_id = current_user['user_id']
    #user_id ="1"
    #response = requests.get(Conf.API_ADDRESS + "/api/v1.0/get_resource_by_user_id/" + user_id)
    #response_data = json.loads(response.content)
    #if response_data["code"] == 1:
        # <class 'list'>:
        # [{'hs_city': '杭州市', 'user_id': 1, 'hs_status': 1, 'hs_images': 'static/upload/hs/20160806201620685193.jpg|static/upload/hs/20160806201623776844.jpg', 'hs_country': '下城区', 'hs_id': 32, 'ty_id': 1, 'hs_address': '西溪湿地18号', 'hs_hitvalume': '0', 'hs_province': '浙江省', 'hs_name': '房源123'},
        # {'hs_city': '杭州市', 'user_id': 1, 'hs_status': 1, 'hs_images': 'static/upload/hs/20160806201620685193.jpg|static/upload/hs/20160806201623776844.jpg', 'hs_country': '下城区', 'hs_id': 33, 'ty_id': 1, 'hs_address': '西溪湿地18号', 'hs_hitvalume': '0', 'hs_province': '浙江省', 'hs_name': '房源123'},
        # {'hs_city': '杭州市', 'user_id': 1, 'hs_status': 1, 'hs_images': 'static/upload/hs/20160806201620685193.jpg|static/upload/hs/20160806201623776844.jpg', 'hs_country': '下城区', 'hs_id': 34, 'ty_id': 1, 'hs_address': '西溪湿地18号', 'hs_hitvalume': '0', 'hs_province': '浙江省', 'hs_name': '房源123'},
        # {'hs_city': '杭州市', 'user_id': 1, 'hs_status': 1, 'hs_images': 'static/upload/hs/20160806201620685193.jpg|static/upload/hs/20160806201623776844.jpg', 'hs_country': '下城区', 'hs_id': 35, 'ty_id': 1, 'hs_address': '西溪湿地18号', 'hs_hitvalume': '0', 'hs_province': '浙江省', 'hs_name': '房源123'}]
        #house_list = response_data["message"]
        # namelist = []  #
        # for item in house_list:  # item - > dict
        #     # tmp = item['hs_name']
        #     namelist.append(item['hs_name'])
        #, house_list = house_list
    return render_template('house_default.html')


@vi.route("/get_resource_by_user_id", methods=['POST'])
def get_resource_by_user_id():
    user_id = request.json.get("user_id")
    # user_id ="1"
    response = requests.get(Conf.API_ADDRESS + "/api/v1.0/get_resource_by_user_id/" + user_id)
    response_data = json.loads(response.content)
    if response_data["code"] == 1:
        house_list = response_data["message"]
        return jsonify({'code': 1, 'message': house_list})
    return jsonify({'code': 0, 'message': '查询失败'})



@vi.route("/house_edit/<int:hs_id>")
def house_edit(hs_id):
    # if hs_id > 0:
    #     response = requests.get(Conf.API_ADDRESS + "/api/v1.0/get_houseresources_by_hs_id/" + str(hs_id))
    #     response_data = json.loads(response.content)
    #     if response_data["code"] == 1:
    #         house_entity = response_data["message"]
    #         return render_template('house_edit.html',entity=house_entity)
    return render_template('house_edit.html')

@vi.route("/house_add")
@tools.check_user_wrapper
def house_add():
    return render_template("house_add.html")


@vi.route("/do_hs_insert",methods=['POST'])
#将JS Post过来的参数转化成Json格式
@tools.check_user_wrapper
def do_hs_insert():
    api = Conf.API_ADDRESS
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username and password:
        user_hash_account = tools.get_hash_account(username, password)
        current_user = current_app.session_redis.hget('user:%s' % user_hash_account, 'current_user')
        # print(type(current_user))
    # #判断用户是否登录:用户登录
    if current_user:
        # redis返回的类型为bytes的字符串,如下格式:
        # b"{'user_account': 'sansan', 'user_mobile': '15957124901', 'user_id': 1, 'user_type': 0, 'user_headimg': None}"
        # 这里使用eval()将bytes字符串转为dict
        # {'user_type': 0, 'user_account': 'sansan', 'user_id': 1, 'user_mobile': '15957124901', 'user_headimg': None}
        current_user= eval(current_user)

        # tmp = json.loads(tmp) 和 decode() 都会生成str,格式如: #'{\\'user_account\\': \\'sansan\\', \\'user_mobile\\': \\'15957124901\\', \\'user_id\\': 1, \\'user_type\\': 0, \\'user_headimg\\': None}'
        # current_user = current_user.decode()
        # print(type(current_user))
        user_id = current_user['user_id']
    else:
        return jsonify({"code": 0, "message": "您还未登陆,请先登陆"})
        # return redirect(url_for("/login"))

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
@vi.route("/do_loadhs")
def do_loadhs():
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    user_hash_account = tools.get_hash_account(username,password)
    current_user = current_app.session_redis.hget("user % " % user_hash_account,"current_user")
    if current_user:
        current_user = eval(current_user)
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
@vi.route("/do_ediths",methods=['POST'])
@tools.check_user_wrapper
def do_ediths():
    api = Conf.API_ADDRESS
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username and password:
        user_hash_account = tools.get_hash_account(username, password)
        current_user = current_app.session_redis.hget("user % " % user_hash_account, 'current_user')
    # 判断用户是否登录:用户登录
    if current_user:
        current_user = eval(current_user)
        user_id = current_user['user_id']
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "房源不存在"})
    ty_id = request.json.get("ty_id")
    hs_intro = request.json.get("hs_intro")
    hs_province = request.json.get("hs_province")
    hs_city = request.json.get("hs_city")
    hs_country = request.json.get("hs_country")
    hs_address = request.json.get("hs_address")
    hs_hitvalume = request.json.get("hs_hitvalume")
    hs_images = request.json.get("hs_images")
    hs_status = request.json.get("hs_status")

    data = json.dumps({
                       "user_id":user_id,
                       "ty_id": ty_id,
                       "hs_intro": hs_intro,
                       "hs_province": hs_province,
                       "hs_city": hs_city,
                       "hs_country": hs_country,
                       "hs_address": hs_address,
                       "hs_images": hs_images,
                       "hs_hitvalume": hs_hitvalume,
                       "hs_status":hs_status
                       })
    response = requests.post(api+"/api/v1.0/hs_edit/"+hs_id,
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
@vi.route("/do_delete_hs",methods=['POST'])
def do_delete_hs():
    api = Conf.API_ADDRESS
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "房源不存在"})
    #data = json.dumps({"hs_id": hs_id})
    response = requests.post(api+"/api/v1.0/hs_delete/"+hs_id,
                            headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0删除失败
    if response_data["code"] == 0:
        return jsonify(response_data)

    # code = 1 删除成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "message": "删除成功"})


#根据点击量的提升更新房源类型
@vi.route("/do_update_type",methods=['POST'])
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
    response = requests.post(api+"/api/v1.0/update_ty_id",
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



