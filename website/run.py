# coding:utf-8
from flask import Flask
from website.config import Conf
from website.view import vi as vi_blueprint
import redis
from flask_session import Session

sess = Session()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Conf)

    app.config['ALLOW_FOLDER'] = True
    app.secret_key = app.config['SECRET_KEY']

    app.debug = app.config['DEBUG']

    rd = redis.Redis(host='127.0.0.1', port=6379, db=0)
    SESSION_REDIS = rd
    sess.init_app(app)

    # 蓝图
    app.register_blueprint(vi_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.debug, host=Conf.SERVICE_HOST, port=Conf.SERVICE_PORT)