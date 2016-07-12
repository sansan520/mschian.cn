#!/usr/bin/python
# coding = utf8

from flask import render_template
from . import vi


@vi.route("/error/<int:error_code>")
def error(error_code):
    if error_code == 500:
        error_msg = "服务器异常"
        return render_template("error.html", error_code=error_code, error_msg=error_msg)
    if error_code == 404:
        error_msg = "找不到URL路径"
        return render_template("error.html", error_code=error_code, error_msg=error_msg)
    return render_template("error.html", '')