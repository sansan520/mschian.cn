import requests
from flask import render_template,request,jsonify,json,redirect,url_for,current_app
from website.model import HouseOwner,HouseResources,HouseType
from website.config import Conf
from website import tools
from .import vi

@vi.route("/houseresources")
def add_houseresource():
    return render_template("/houseresources.html")

@vi.route("/do_hs_insert")
#将JS Post过来的参数转化成Json格式
def add_houseresources():
    api = Conf.APIADRESS
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username and password:
        user_hash_account = tools.get_hash_account(username, password)
        current_user = current_app.session_redis.hget("user % " % user_hash_account, 'current_user')
    #判断用户是否登录:用户登录
    if current_user:
        current_user = current_user.decode()
        ho_id = current_user['username']

        # #从缓存里查询房东
        # ho_name = request.cookies.get("username")
        # resp = requests.get(api+"/api/v1.0/get_hs/"+ho_name)
        # resp_data = json.loads(resp.content.decode())
        # if resp_data["code"] == 1:
        #     result = resp_data["message"]
        #     ho_id = result[0]['ho_id']
    ty_id = request.json.get("ty_id")
    hs_intro = request.json.get("hs_intro")
    hs_province = request.json.get("hs_province")
    hs_city = request.json.get("hs_city")
    hs_country = request.json.get("hs_country")
    hs_address = request.json.get("hs_address")
    hs_hitvalume = request.json.get("hs_hitvalume")
    hs_images = request.json.get("hs_images")
    data = {
        "ho_id":ho_id,
        "ty_id":ty_id,
        "hs_intro":hs_intro,
        "hs_province":hs_province,
        "hs_city":hs_city,
        "hs_country":hs_country,
        "hs_address":hs_address,
        "hs_hitvalume":hs_hitvalume,
        "hs_image":hs_images
    }
    #data = json.dumps({})
    #访问service api
    response = requests.post(api+"/api/v1.0/hs_insert",
                  data = data,
                  headers = {"content-type":"application/json"}
                  )
    response_data = json.loads(response.content)
    #code = 0 添加失败
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)
    #code = 1 添加成功
    if request_data["code"] == 1:
        return jsonify({"code":1,"message":"添加成功"})
#加载用户添加的房源
@vi.route("/do_loadhs")
def loadhs():
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code":0,"message":"房源不存在"})
    api = Conf.API_ADDRESS
    response = requests.get(api+"/api/v1.0/get_by_hs_id/<int:hs_id>"+hs_id)
    response_data = json.loads(response.content)
#code = 0查询失败
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)
#code = 1 查询成功
    if response_data["code"] == 1:
        return jsonify({"code":1,"message":"success"})


#编辑房源
def ediths():
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "房源不存在"})
    user = session['current_user']
    ho_id = user.ho_id
    ty_id = request.json.get("ty_id")
    hs_intro = request.json.get("hs_intro")
    hs_province = request.json.get("hs_province")
    hs_city = request.json.get("hs_city")
    hs_country = request.json.get("hs_country")
    hs_address = request.json.get("hs_address")
    hs_hitvalume = request.json.get("hs_hitvalume")
    hs_images = request.json.get("hs_images")

    data = json.dumps({"hs_id": hs_id,
                       "ho_id":ho_id,
                       "ty_id": ty_id,
                       "hs_intro": hs_intro,
                       "hs_province": hs_province,
                       "hs_city": hs_city,
                       "hs_country": hs_country,
                       "hs_address": hs_address,
                       "hs_images": hs_images,
                       "hs_hitvalume": hs_hitvalume
                       })
    response = requests.get("http://127.0.0.1:8080/api/v1.0/hs_edit/<int:hs_id>",
                            data=data,
                            headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0编辑失败
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

    # code = 1 编辑成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "go_url": "/index"})



#删除房源
@vi.route("/do_delete_hs")
def deletehs():
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "房源不存在"})
    data = json.dumps({"hs_id": hs_id})
    response = requests.get("http://127.0.0.1:8080/api/v1.0/hs_delete/<int:hs_id>",
                            data=data,
                            headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0删除失败
    if response_data["code"] == 0:
        return jsonify(response_data)
    return jsonify(response_data)

    # code = 1 删除成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "go_url": "/index"})
#根据点击量的提升更新房源类型
@vi.route("/do_update_type")
def update_type():
    ty_id = request.json.get("ty_id")
    if not ty_id:
        return jsonify({"code": 0, "message": "房源类型不存在"})
    hitvalue = request.json.get("hs_hitvalume")
    if not hitvalue:
        return jsonify({"code":0,"message":"点击量达不到升级标准"})
    data = json.dumps({"ty_id":ty_id})
    response = requests.post("http:127.0.0.1:8080/api/v1.0/update_ty_id",
                 data = data,
                 headers = {"content-type":"application/json"}
                 )
    response_data = json.loads(response.content)
    #更新成功 code = 1
    if response_data['code'] == 1:
        return render_template("/houseresources.html")
    #code = 0 更新失败
    if response_data["code"] == 0:
        return jsonify(response_data)



