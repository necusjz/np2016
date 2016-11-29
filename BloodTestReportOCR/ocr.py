# -*- coding: UTF-8 -*-
import csv
import codecs
try:
	from PIL import Image
except ImportError:
	from PIL import Image
import pytesseract
#import Binarization
import imgproc
import cv2

digtitsresult = []
chiresult = []
#识别
def ocr(image,flag = True):
	if flag:
		text = pytesseract.image_to_string(Image.fromarray(image),config = '-psm 7 digits')
	else:
		text = pytesseract.image_to_string(Image.fromarray(image),lang = 'chi_sim',config = ' -psm 7 Bloodtest')
	return text
#读取图片
def read(url):
	image = cv2.imread(url)
	return image

#识别数字
for i in range(22):
	image = read('temp_pics/data'+str(i)+'.jpg')
	image = imgproc.digitsimg(image)
	digtitstr = ocr(image)
	digtitstr = digtitstr.replace(" ",'')
	digtitstr = digtitstr.replace("-",'')
	digtitstr = digtitstr.strip(".")
	print digtitstr
	digtitsresult.append(digtitstr)
with open('digitdata.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile,dialect='excel')
	spamwriter.writerow(digtitsresult)

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