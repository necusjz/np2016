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

digtitsresult = []
chiresult = []


def ocr(path, num):
    ret = autocut.autocut(path, num, autocut.default)
    if ret != 0:
        return -1

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

    # 识别数字
    for i in range(22):
        item = read('temp_pics/p' + str(i) + '.jpg')
        item_num = classifier.getItemNum(item)
        image = read('temp_pics/data' + str(i) + '.jpg')
        image = imgproc.digitsimg(image)
        digtitstr = image_to_string(image)
        digtitstr = digtitstr.replace(" ", '')
        digtitstr = digtitstr.replace("-", '')
        digtitstr = digtitstr.strip(".")
        print item_num, digtitstr
        digtitsresult.append(item_num)
        digtitsresult.append(digtitstr)
    with open('data.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(digtitsresult)
    '''
    #识别中文
    for x in range(22):
        image = read('temp_pics/p'+str(x)+'.jpg')
        image = imgproc.chineseimg(image)
        chistr = ocr(image,False)
        chistr = chistr.replace(" ",'')
        chistr = chistr.replace(".",'')
        print chistr.decode('utf-8')

        chiresult.append(chistr)
    with open('chidata.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        spamwriter = csv.writer(csvfile,dialect='excel')
        spamwriter.writerow(chiresult)
    '''
    return 0
# unit test
if __name__ == '__main__':
    import ocr

    path = 'origin_pics/bloodtestreport2.jpg'
    num = 22

    ocr.ocr(path, num)
