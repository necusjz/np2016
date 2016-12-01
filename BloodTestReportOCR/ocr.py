# -*- coding: UTF-8 -*-
import csv
import codecs

try:
    from PIL import Image
except ImportError:
    from PIL import Image
import pytesseract
# import Binarization
import imgproc
import cv2
import autocut
import classifier
import json

digtitsresult = []
chiresult = []
num = 22

# input a image,output a json
def ocr(path ):
    ret = autocut.autocut(path, num, autocut.default)
    if ret != 0:
        return null

    # 识别
    def image_to_string(image, flag=True):
        if flag:
            text = pytesseract.image_to_string(Image.fromarray(image), config='-psm 7 digits')
        else:
            text = pytesseract.image_to_string(Image.fromarray(image), lang='chi_sim', config=' -psm 7 Bloodtest')
        return text

    # 读取图片
    def read(url):
        image = cv2.imread(url)
        return image
    # load json example
    with open('bloodtestdata.json') as json_file:
        data = json.load(json_file)

    # 识别检测项目编号及数字
    for i in range(num):
        item = read('temp_pics/p' + str(i) + '.jpg')
        item_num = classifier.getItemNum(item)
        image = read('temp_pics/data' + str(i) + '.jpg')
        image = imgproc.digitsimg(image)
        digtitstr = image_to_string(image)
        digtitstr = digtitstr.replace(" ", '')
        digtitstr = digtitstr.replace("-", '')
        digtitstr = digtitstr.strip(".")
        data['bloodtest'][item_num]['value'] = digtitstr
    json_data = json.dumps(data,ensure_ascii=False,indent=4)
    return json_data

# unit test
if __name__ == '__main__':
    import ocr

    path = 'origin_pics/bloodtestreport2.jpg'

    json_data = ocr.ocr(path)
    print json_data
