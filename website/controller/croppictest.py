import requests
import os
from flask import Flask, request, render_template, jsonify,make_response,json
from werkzeug.utils import secure_filename
import sys
import time,datetime
from PIL import Image,ImageDraw,ImageFont, ImageEnhance
from . import vi
from website.tools import json_mkdir,get_hash_file_name
from website.config import Conf


# http://www.cnblogs.com/kissdodog/archive/2012/12/21/2827867.html
# os.path.getsize(filePath) 获取文件大小bytes单位 /1024/1024 = > M

app = Flask(__name__)

#绝对路径获取
HS_LOCATION = '/static/upload/hs/'   #房源图片路径
ABSPATH = os.path.abspath(sys.argv[0])
ABSPATH = os.path.dirname(ABSPATH)+"/"

UPLOAD_FOLDER = ABSPATH + '/static/upload/bhImg/'  # 裁剪前的图片 big_head_img  服务器定时删除
CROPPIC_FOLDER = ABSPATH + '/static/upload/shImg/'  # 裁剪后的小图片 small head img
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'JPEG','jpeg'])

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
                ext_name = file.filename.rsplit('.',1)[1]
                img = resizeImg(file)
                prename = get_hash_file_name(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                filename = prename + "." + ext_name
                filepath = os.path.join(app.config['HS_FOLDER'], filename)
                minetype = file.content_type
                r = json_mkdir(app.config['HS_FOLDER'])
                try:
                    img.save(filepath,qua=85)
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
    return render_template('/test/croptest.html')

@vi.route('/crop_uploadPic', methods=['POST'])
def upload_pic():
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            ext_name = file.filename.rsplist('.', 1)[1]
            # file_prename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            # filename = file_prename + "_" + random_str(8) + "." + file.filename.rsplit('.', 1)[1]
            prename = get_hash_file_name(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
            filename = prename + "." + ext_name
            upload_folder = app.config['UPLOAD_FOLDER']
            r = json_mkdir(upload_folder)
            filepath = os.path.join(upload_folder, filename)
            try:
                file.save(filepath)
                img = Image.open(filepath)
                #img.thumbnail(800*600)
                width, height = img.size
                return jsonify({"status": 'success', "url": UPLOAD_FOLDER + filename, "width": width,
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

#  保存删除图片地址函数接口
@vi.route('/upload_delete_image', methods=['POST'])
def upload_delete_image():
    del_image = request.json.get("del_image")
    data = json.dumps({"image": del_image})
    response = requests.post(url=Conf.API_ADDRESS + "/api/v1.0/save_delete_image",data=data, headers={"content-type": "application/json"})
    response_data = json.loads(response.content)

    return jsonify(response_data)

#  直接删除图片函数接口
@vi.route("/del_by_imgUrl",methods=["post"])
def del_by_imgUrl():
    imgUrl = request.json.get("del_image")
    try:
        file_path = ABSPATH + imgUrl
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"code": 1, "message": '已成功删除图片!'})
    except IOError:
        return jsonify({"code": 0, "message": '删除图片出错!'})
    return None

def resizeImg(imgUrl):
    im = Image.open(imgUrl)
    dst_w = 800
    dst_h = 600

    ori_w,ori_h = im.size

    if(ori_h > ori_w and ori_w >= 800):
        im = cut_pic(im,dst_w,dst_h)
        ori_w, ori_h = im.size

    widthRatio = heightRatio =None
    ratio = 1
    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h
        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio
        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio
        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
        im.resize((newWidth, newHeight), Image.ANTIALIAS)  #.save(app.config['UPLOAD_FOLDER']+'test1.jpg', qua=85)
        return im
    else:

        im.resize((ori_w,ori_h),Image.ANTIALIAS)  #.save(app.config['UPLOAD_FOLDER']+'test2.jpg',qua=85)
        return im



def cut_pic(Image,dst_w,dst_h):
    # dst_w = 800,dst_h = 600
    try:
        ori_w, ori_h = Image.size
        if(ori_h>ori_w):
            y = (ori_h-dst_h)/2
            box = (0, int(y), dst_w, dst_h+y)
        newImg = Image.crop(box)
        try:
            return newImg
        except IOError:
            return None
    except IOError:None


if __name__ == '__main__':
    app.run(debug=True)
