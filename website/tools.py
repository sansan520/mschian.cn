# coding : utf8

import hashlib

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
