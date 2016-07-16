import os
from flask import render_template,request,jsonify,url_for,g
from werkzeug import secure_file
from Pillow import Image
from . import vi
@vi.route("/upload_file")
def upload_file():
    return render_template("")

ALLOWED_EXTENSTIONES = set({"JPG","JPEG","PNG"})
def allow_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSTIONES

@vi.route("/do_upload_file")
def upload_file():
    current_user = g.current_user
    upload_file = request.files.getList("file[]")
    filenames = []
    size(80,80)
    im = Image.open(upload_file)
    im.thumbniall(size)
    for file in upload_file:
        if file in allow_file(file.filename):
            filename = secure_file(file.filename)
            im.save(os.path.join("http://127.0.0.1:8080/static/"),"avaster",filename)
            current_user.new_avaster_file = url_for("main.static",filename = "%s %s" % ('avaster',filename))
            current_user.is_avaster_file = False
        return jsonify({"code":1,"message":"修改成功"})