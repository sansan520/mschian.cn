# coding : utf8

from flask import render_template, jsonify, request, json, current_app, make_response
from . import vi

@vi.route("/about_us")
def about_us():
    return render_template("/help_center/about_us.html")


@vi.route("/contact_us")
def contact_us():
    return render_template("/help_center/contact_us.html")