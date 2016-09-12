import requests
from flask import render_template,request,jsonify,json
from website import tools
from website.config import Conf
from . import vi



@vi.route("/manage_center/do_add_reserve",methods=['POST'])
@tools.check_user_wrapper
def do_add_reserve():
    # current_user = tools.get_current_user()
    # user_id = current_user['user_id']
    gr_id = request.json.get("gr_id")
    user_id = request.json.get("user_id")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    status = request.json.get("status")
    data = json.dumps({
        'gr_id':gr_id,
        'user_id':user_id,
        'start_time':start_time,
        'end_time':end_time,
        'status':status
    })
    response = requests.post(Conf.API_ADDRESS+"/api/v1.0/insert_reserve",
        data = data,
        headers={"content-type":"application/json"})
    response_data = json.loads(response.content)
    if response_data['code'] == 1:
        return jsonify({'code':1,'message':'预订成功'})
    if response_data['code'] == 0:
        return response_data['message']
    return response_data['message']

@vi.route("/manage_center/do_del_reserve/<int:id>",method=['POST'])
@tools.check_user_wrapper
def do_del_reserve():
    id = request.json.get("id")
    response = requests.delete(Conf.API_ADDRESS+"/api/v1.0/del_reserve/"+str(id),
                            headers = {"content-type":"application/json"}
                            )
    response_data = json.loads(response.content)
    if response_data['code'] == 1:
        return jsonify({"code":1,"message":"reverse success"})
    if response_data['code'] == 0:
        return response_data['message']
    return response_data['message']