# coding:utf-8
from flask import Flask
from website import lm

from website.config import Conf
from website.view import vi as vi_blueprint


def create_app():

    app = Flask(__name__)
    app.config.from_object(Conf)

    app.config['ALLOW_FOLDER'] = True
    app.secret_key = app.config['SECRET_KEY']

    app.debug = app.config['DEBUG']

    # flask_login
    # LM = flask_login.LoginManager()
    # lm.session_protection = 'strong'
    # lm.init_app(app)
    # loginManager.login_view = "login"
    # 蓝图
    app.register_blueprint(vi_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.debug, host=Conf.SERVICE_HOST, port=Conf.SERVICE_PORT)