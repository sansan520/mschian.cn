# www.mschina.cn 中国名宿网

目录结构:
service_api:服务的接口
website:    web端(前端php/python)
说明文档:     计划以及产品说明word文档


一) service_api(服务的接口)
统一URL格式:service.mschina.cn:8080/api/v1.0/ <==> 本地:localhost:8080/api/v1.0 <==> 127.0.0.1/api/v1.0

服务端的数据存储介质:mysql
服务器的缓存以及token存储介质:redis

model.py  mysql数据库表结构,配置完环境,执行该文件即可(注意安装sqlalchemy库)
client.py 测试文件
config.py 接口配置文件

v1_0: 版本一主要接口文件目录:
      要创建接口文件(如test.py),写完相关代码,然后,在该目录下的__init__.py内导入即可(from service_api.v1_0 import test)
      然后注意的是test.py接口上的路由@api开头即可

run.py    本地接口主要入口文件,执行该文件后进行测试.



 2. 登录API
    url:localhost:8080/api/v1.o/ho_login
    参数:
    ho_account : 账号
    ho_password: 密码
    返回值: json格式如下:
    {'code': 1, 'message': '成功登录', 'acount': ho_account, 'token': token}
    Airbnb的房东账号密码809493896@qq.com   wanghuaisang1234




