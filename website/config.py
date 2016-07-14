#   发布环境
class ProductionConfig(object):
    DEBUG = False

    SERVICE_HOST = 'mschina.cn'
    SERVICE_PORT = 8000
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT/json/wang'

    REDIS_HOST = 'localhost'
    REDIS_PORT = 80

#   开发环境
class DevelopmentConfig(object):
    DEBUG = True

    SERVICE_HOST = 'mschina.cn'
    SERVICE_PORT = 8000
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT/json/wang'
    # flask-session
    SESSION_TYPE = 'redis'
    SESSION_COOKIE_NAME = 'mysession'
    SESSION_COOKIE_DOMAIN = SERVICE_HOST
    PERMANENT_SESSION_LIFETIME = 60*10  # session保存10分钟

    API_ADDRESS = "http://127.0.0.1:8080"
    MYSQL_INFO = "mysql+pymysql://root:123@127.0.0.1:3306/mschina?charset=utf8"

Conf = DevelopmentConfig