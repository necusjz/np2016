# -*- coding: UTF-8 -*-
import ocr

path = 'origin_pics/bloodtestreport2.jpg'

json_data = ocr.ocr(path)
print json_data