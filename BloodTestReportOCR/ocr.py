# -*- coding: UTF-8 -*-
import csv
try:
	from PIL import Image
except ImportError:
	from PIL import Image
import pytesseract
import Binarization

result = []

# 二值化
for i in range(22):
	Binarization.Binarization('temp_pics/data'+str(i)+'.jpg', 'bin_pics/bin_data'+str(i)+'.jpg')

# 识别
for i in range(22):
	image=Image.open('bin_pics/bin_data'+str(i)+'.jpg')
	# 仅识别数字
	tempstr = pytesseract.image_to_string(image,  config='-psm 7 digits')
	# 去除空格，去除负号
	tempstr = tempstr.replace(" ",'')
	tempstr = tempstr.replace("-",' ')
	tempstr = tempstr.lstrip()
	tempstr = tempstr.rstrip()
	tempstr = tempstr.replace(" ", '.')
	print tempstr
	result.append(tempstr)
	#result.append(pytesseract.image_to_string((image),config='-psm 7'))
with open('data.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile,dialect='excel')
	spamwriter.writerow(result)