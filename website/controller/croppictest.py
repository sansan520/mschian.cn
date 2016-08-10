
import os
from flask import Flask, request, render_template, jsonify,make_response,json
from werkzeug.utils import secure_filename
import os
import sys
import time,datetime
from PIL import Image,ImageDraw,ImageFont, ImageEnhance
from . import vi
from website.tools import json_mkdir

# http://www.cnblogs.com/kissdodog/archive/2012/12/21/2827867.html
# os.path.getsize(filePath) 获取文件大小bytes单位 /1024/1024 = > M

app = Flask(__name__)

#绝对路径获取
HS_LOCATION = '/static/upload/hs/'   #房源图片路径
ABSPATH = os.path.abspath(sys.argv[0])
ABSPATH = os.path.dirname(ABSPATH)+"/"

UPLOAD_FOLDER = ABSPATH + '/static/upload/bhImg/'  # 裁剪前的图片 big_head_img  服务器定时删除
CROPPIC_FOLDER = ABSPATH + '/static/upload/shImg/'  # 裁剪后的小图片 small head img
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'JPEG'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CROPPIC_FOLDER'] = CROPPIC_FOLDER
app.config['HS_FOLDER'] = ABSPATH + HS_LOCATION

@vi.route('/uploadPic', methods=['POST'])
def upload_pic_new():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files[]")
        response = make_response()
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                file_prename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
                filename = file_prename + "." + file.filename.rsplit('.', 1)[1]
                filepath = os.path.join(app.config['HS_FOLDER'], filename)
                minetype = file.content_type
                r = json_mkdir(app.config['HS_FOLDER'])
                try:
                    file.save(filepath)
                    response.data = json.dumps({"files": [{"name": HS_LOCATION + filename, "minetype": minetype}]})
                    return response
                except IOError:
                    response.data = '{"code":"0","file_names":"图片存取错误!"}'
                    return response
            response.data = '{"code":"0","file_names":"图片格式不正确!!"}'
            return response
    response.data = '{"code":"0","file_names":"必须POST提交!!"}'
    return response

@vi.route('/croptest')
def croptest():
    return render_template('croptest.html')

@vi.route('/crop_uploadPic', methods=['POST'])
def upload_pic():
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            file_prename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = file_prename + "_" + random_str(8) + "." + file.filename.rsplit('.', 1)[1]
            upload_folder = app.config['UPLOAD_FOLDER']
            r = json_mkdir(upload_folder)
            filepath = os.path.join(upload_folder, filename)
            try:
                file.save(filepath)
                img = Image.open(filepath)
                #img.thumbnail(800*600)
                width, height = img.size
                return jsonify({"status": 'success', "url": '/static/upload/bhImg/' + filename, "width": width,
                                "height": height})
            except IOError:
                return jsonify({"status": 'error', "message": '图片存取错误!'})


@vi.route("/crop_cutPic", methods=['POST'])
def crop_pic():

    """
    imgUrl 		// your image path (the one we recieved after successfull upload)
    imgInitW  	// your image original width (the one we recieved after upload)
    imgInitH 	// your image original height (the one we recieved after upload)

    imgW 		// your new scaled image width
    imgH 		// your new scaled image height

    imgX1 		// top left corner of the cropped image in relation to scaled image
    imgY1 		// top left corner of the cropped image in relation to scaled image

    cropW 		// cropped image width
    cropH 		// cropped image height
    """
    # original size 原图信息--地址/大小
    imgUrl = request.form['imgUrl']
    imgInitW = request.form['imgInitW']  # 800
    imgInitH = request.form['imgInitH']   # 1036
    # resized sizes  调整后大小
    imgW = request.form['imgW']  # 318
    imgH = request.form['imgH']    # 412
    # offsets 偏移量
    imgY1 = request.form['imgY1']  # 0
    imgX1 = request.form['imgX1']  # 59
    # crop box  裁剪框
    cropW = request.form['cropW']  # 178
    cropH = request.form['cropH']  # 148
    # rotation angle 旋转角度
    angle = request.form['rotation']  # 0


    #  进行裁剪
    filename = os.path.basename(imgUrl)
    try:
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        crop_w = int(cropW) + int(imgX1)
        crop_h = int(cropH) + int(imgY1)
        box = (int(imgX1), int(imgY1), crop_w, crop_h)
        newImg = img.crop(box)
        file_prename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename =  "small_"+ file_prename + ".jpg"
        r = json_mkdir(app.config['CROPPIC_FOLDER'])
        filepath = os.path.join(app.config['CROPPIC_FOLDER'] + filename)
        os.remove(ABSPATH + imgUrl)
        try:
            newImg.save(filepath, 'JPEG')
            time.sleep(0.5)
            return jsonify({"status": 'success', "url": '/static/upload/shImg/' + filename})
        except IOError:
            return jsonify({"status": 'error', "message": '图片裁剪错误!'})
    except IOError:
        return jsonify({"status": 'error', "message": '图片裁剪错误!'})


def cut_imgage():

    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], '1.jpg'))

    width, height = img.size  # 700 * 525 (宽 * 高)
    # img.crop(左,上,右,下)
    # box = (width-200, height-100, width, height)  # 1_1.jpg
    # box =(0, 0, 100, 100)   #1_2.jpg
    box = (100, 100, 200, 500) # (100,100) =>左上 (200,500)=> 右下点
    newImg = img.crop(box)

    # region = region.transpose(Image.ROTATE_180)  # 旋转
    # img.paste(region, box)    # 复制到原图
    newImg.save(os.path.join(app.config['UPLOAD_FOLDER']+'1_2.jpg'), 'JPEG')

    return render_template('index123.html')
    # jsonify({"status": 'success', "url": "static/upload/" + '1_11.jpg'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


from random import Random
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

@vi.route('/upload_delete_image', methods=['POST'])
def upload_delete_image():
    del_image = request.json.get("del_image")
    data = json.dumps({"image": del_image})
    response = requests.post(url=api + "/api/v1.0/save_delete_image",data=data, headers={"content-type": "application/json"})
    response_data = json.loads(response.content)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
