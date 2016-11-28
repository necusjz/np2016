# -*- coding: UTF-8 -*-
import os
import pytesseract
from PIL import Image

input_path='temp_pics'
output_path='temp_nums'

if not(os.path.exists(output_path)):
    os.makedirs(output_path)

# 遍历input_path下所有后缀为jpg的图片
for i in os.listdir(input_path):
    if os.path.splitext(i)[1] == '.jpg':
        image = Image.open(input_path+'/'+i)
        num = pytesseract.image_to_string(image,None,False,'-psm 7 digits') #-psm 7 digits表示识别一行数字
        if(num!=''):
            print i+'\t'+num
            output = open(output_path+'/'+os.path.splitext(i)[0]+'.txt', 'w')
            output.write(num)
            output.close()
