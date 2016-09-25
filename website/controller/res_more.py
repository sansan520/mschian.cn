# coding = utf8

#  更多房源,分页显示

from flask import Flask, render_template, json, request, jsonify, session,current_app
import requests
from . import vi
from flask_paginate import Pagination
from website.config import Conf
from website import tools


@vi.route('/re_more_page')
def res_more_page():

    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username and password:
        user_hash_account = tools.get_hash_account(username,password)
        current_user = current_app.session_redis.hget('user:%s' %user_hash_account,'current_user')
        if current_user:
            current_user = current_user.decode()
            login_user = username

    page = request.args.get('page')
    if page == None:
        page = '1'
    api_address = Conf.API_ADDRESS  # PAI地址

    try:
        response = requests.get(url=api_address + "/api/v1.0/get_res_page/"+page)
        response_data = json.loads(response.content)
        if response_data['code'] == 1:
            page = response_data['page']
            pages = response_data['pages']
            total = response_data['total']
            entities = response_data['message']

            pagination = Pagination(page=page, total=total, pages=pages)
            return render_template("index_more.html", **locals())

    except Exception as e:
        return render_template("index_more.html")
    return render_template("index_more.html")