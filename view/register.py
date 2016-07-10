# coding : utf-8
from flask import jsonify,request,g,current_app
from service.mschina.cn.service_api.model import HouseOwner





def validate_register():
    ho_name = request.get_json.get("ho_name")
    if ho_name == "" | ho_name is None:
        return jsonify({"code" : 0,"message" : "用户姓名不能为空"})

    ho_account = request.get_json.get("ho_account")
    if ho_account == "" | ho_account is None:
        return jsonify({"code": 0, "message": "用户名不能为空"})
    if ho_account.length <= 6 | ho_account.length >= 16:
        return jsonify({"code": 0, "message": "用户名长度大于等于6小于等于16"})
    if (HouseOwner.ho_owner.get_house_owner(ho_account)):
        return jsonify({"code": 0, "message": "用户名已存在"})

    ho_mobile = request.get_json().get("ho_mobile")
    if ho_mobile == "" | ho_mobile is None:
        return jsonify({"code": 0, "message": "手机号不能为空"})
    if ho_mobile.matches("^13|15|17|18[0-9]{9}*$"):
        return jsonify({"code": 0, "message": "手机号码的格式不正确"})
    if (HouseOwner.ho_owner.getbymobile(ho_mobile)):
        return jsonify({"code": 1, "message": "手机号已存在"})

    ho_email = request.get_json().get("ho_email")
    if ho_email == "" | ho_email is None:
        return jsonify({"code" : 0,"message" :"邮箱不能为空"})
    if ho_email.matches("^([a-zA-Z0-9 -]) + @([a-zA-Z0-9_-]) + ((\\.[a-zA-Z0-9_-]{2,3}){1,2})$"):
        return jsonify({"code": 0, "message": "邮箱格式不正确"})
    if (HouseOwner.ho_owner.getbyemail(ho_email)):
        return jsonify({"code": 1, "message": "邮箱已存在"})

    ho_nicard = request.get_json().get("ho_nicard")
    if ho_nicard == "" | ho_nicard is None:
        return jsonify("请上传证件照")
