# coding : utf8

import hashlib
from functools import wraps
from flask import request,current_app,redirect,url_for

def get_hash_account(username,password):
    if username and password:
        m = hashlib.md5()
        m.update(username.encode("utf8"))
        m.update(password.encode("utf8"))
        user_hash_account = m.hexdigest()
        return user_hash_account
    return ""


# 用来创建文件夹
def json_mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # print path + ' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print path + ' 目录已存在'
        return False

#  装饰器,验证是否登录的,如果没有登录则跳转到login页面
def check_user_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        user_hash_account = get_hash_account(username, password)
        current_user = current_app.session_redis.hget('user:%s' % user_hash_account, 'current_user')
        if not current_user:
            return redirect(url_for('vi.login'))
        return func(*args, **kwargs)
    # print(wrapper.__name__)
    return wrapper