# coding:utf-8
from flask import Blueprint


vi = Blueprint('vi', __name__)

from . import index
from . import about_user
from . import error
from . import register

