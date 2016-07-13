# coding : utf-8
from flask import render_template
from . import vi
import requests
import json
from flask import jsonify, request, session
from website.model import HouseOwner

@vi.route("/test")
def test():
    current_user = session.get('current_user', 'not set')  # json
    # tmp = HouseOwner.json_to_houseowner(current_user)
    return render_template('test.html', current_user=current_user['ho_account'])