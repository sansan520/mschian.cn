from flask import Flask,request,current_app,redirect,url_for,jsonify
from functools import wraps
from website import tools

def checkuser(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        user_hash_account = tools.get_hash_account(username,password)
        current_user = current_app.session_redis.hget("user%" % user_hash_account,"current_user")
        if current_user:
            current_user = current_user.decode()
            return current_user
        return decorated_function
    return redirect(url_for('/login'))
