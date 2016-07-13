#!/usr/bin/python
# coding = utf8

from flask import render_template, make_response
from . import vi


# @vi.route("/error/<int:error_code>")
# def error(error_code):
#     if error_code == 500:
#         error_msg = "服务器异常"
#         return render_template("error.html", error_code=error_code, error_msg=error_msg)
#     if error_code == 404:
#         error_msg = "找不到URL路径"
#         return render_template("error.html", error_code=error_code, error_msg=error_msg)
#     return render_template("error.html", '')
#
#
# @vi.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404

@vi.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

# @vi.errorhandler(500)
# def internal_server_error(error):
#     return render_template("error.html"), 500