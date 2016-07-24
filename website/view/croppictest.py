
import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import sys
import time,datetime
from PIL import Image,ImageDraw,ImageFont, ImageEnhance
from . import vi

# http://www.cnblogs.com/kissdodog/archive/2012/12/21/2827867.html
# os.path.getsize(filePath) 获取文件大小bytes单位 /1024/1024 = > M

app = Flask(__name__)

#绝对路径获取
ABSPATH = os.path.abspath(sys.argv[0])

ABSPATH = os.path.dirname(ABSPATH)+"/"

UPLOAD_FOLDER = ABSPATH + 'static/upload/'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'JPEG'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            filepath = os.path.join(upload_folder, filename)
            try:
                file.save(filepath)
                img = Image.open(filepath)
                width, height = img.size
                return jsonify({"status": 'success', "url": 'static/upload/' + filename, "width": width,
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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'] + filename)
        os.remove(ABSPATH + imgUrl)
        try:
            newImg.save(filepath, 'JPEG')
            time.sleep(0.5)
            return jsonify({"status": 'success', "url": 'static/upload/' + filename})
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

if __name__ == '__main__':
    app.run(debug=True)
