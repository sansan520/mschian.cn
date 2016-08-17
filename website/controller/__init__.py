# coding:utf-8
from flask import Blueprint

vi = Blueprint('vi', __name__)

from . import error
from . import index
from . import about_user
from . import register
from . import res_more
from . import croppictest
from . import houseresources
from . import guestroom
from . import help_center

# from . import test

