# coding = utf8
from flask import Flask, render_template, json, request, jsonify
import requests
from . import vi


@vi.route('/')
@vi.route('/index')
def index():
    return render_template("index.html", account="")


