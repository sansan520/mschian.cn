# coding:utf-8
from flask import Flask
from config import Conf
from view import vi as vi_blueprint

def create_app():

    app = Flask(__name__)
    app.config.from_object(Conf)

    app.config['ALLOW_FOLDER'] = True
    app.secret_key = app.config['SECRET_KEY']

    app.debug = app.config['DEBUG']

    # from service_api.v1_0 import api as api_1_0_blueprint
    app.register_blueprint(vi_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.debug, host=Conf.SERVICE_HOST, port=Conf.SERVICE_PORT)