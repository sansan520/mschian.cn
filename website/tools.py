# coding : utf8

import hashlib

def get_hash_account(username,password):
    if username and password:
        m = hashlib.md5()
        m.update(username.encode("utf8"))
        m.update(password.encode("utf8"))
        user_hash_account = m.hexdigest()
        return user_hash_account
    return ""
