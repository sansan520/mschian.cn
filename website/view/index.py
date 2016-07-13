# coding = utf8
from flask import Flask, render_template, json, request, jsonify, session
import requests
from . import vi
from website.model import HouseOwner

@vi.route('/')
@vi.route('/index')
def index():
    current_user = session.get('current_user', '') # json
    if current_user == '':
        username = ''
    else:
        username = current_user['ho_account']
    return render_template("index.html", username=username)


