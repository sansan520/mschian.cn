# coding = utf8

#  更多房源,分页显示

from flask import Flask, render_template, json, request, jsonify, session
import requests
from . import vi
from flask_paginate import Pagination
from website.config import Conf


@vi.route('/re_more_page')
def res_more_page():

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
            # entities = response_data['message']

            pagination = Pagination(page=page, total=total, pages=pages)
            return render_template("index_more.html", pagination=pagination)

    except Exception as e:
        return render_template("index_more.html")
    return render_template("index_more.html")