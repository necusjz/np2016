# -*- coding: UTF-8 -*-
import csv
try:
	import Image
except ImportError:
	from PIL import Image
import pytesseract
result=[]
for i in range(22):
	image=Image.open('temp_pics/data'+str(i)+'.jpg')
	result.append(pytesseract.image_to_string(image))
	#result.append(pytesseract.image_to_string((image),config='-psm 7'))
with open('data.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile,dialect='excel')
	spamwriter.writerow(result)