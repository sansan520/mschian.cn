#   发布环境
class ProductionConfig(object):
    DEBUG = False

    REDIS_HOST = 'localhost'
    REDIS_PORT = 80

#   开发环境
class DevelopmentConfig(object):
    DEBUG = True

    SERVICE_HOST = '127.0.0.1'
    SERVICE_PORT = 8000

Conf = DevelopmentConfig