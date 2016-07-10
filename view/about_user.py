#!/usr/bin/python
# coding = utf8

from flask import render_template
from . import vi


@vi.route("/login")
def login():
    return render_template("login.html")


@vi.route("/register")
def register():
    return render_template("register.html")

