# -*- coding:utf-8 -*-
from skimage import io, data, color, img_as_float ,img_as_ubyte, transform, exposure, filters
import numpy as np
import math

# 读取图片
img = io.imread('d:/OCR/bloodtestreport3.jpg')
# img = io.imread('d:/OCR/picture.jpg', as_grey=True)

# 图片编码类型
print(img.dtype.name)

# 确定阈值
thresh = filters.threshold_isodata(img)
print(thresh)

# 分割图像
# img = (img >= thresh)*1.0

# 编码转换
# img = img_as_float(img)
# print(img.dtype.name)
# img = img_as_ubyte(img)
# print(img.dtype.name)

# 裁剪图片
# roi = img[80:180, 100:200, :]
# roi = img[80:180, 100:200]

# 保存图片
# io.imshow(roi)
# io.imsave('d:/img.jpg', roi)

# 旋转
# img = transform.rotate(img, -1)

# 判断对比度
if exposure.is_low_contrast(img):
    # 修改强度
    image = np.array([50, 100, 150], dtype=np.uint8)
    image = image * 1.0
    mat = exposure.rescale_intensity(image)
    print(mat)

# 1.计算图像的RGB像素均值– M
# 2.对图像的每个像素点Remove平均值-M
# 3.对去掉平均值以后的像素点 P乘以对比度系数
# 4.对步骤上处理以后的像素P加上 M乘以亮度系统
# 5.对像素点RGB值完成重新赋值

img = np.array(img)
mean = np.mean(img)
img = img - mean
img = img*1.5 + mean*0.7 #修对比度和亮度
# img = img/255.0
# print(img)

# 亮暗调节
# img = exposure.adjust_gamma(img, 1 - math.pow(thresh/255.0 * 1.0, 4))

# 对数调整
img = exposure.adjust_log(img, 1 + math.pow(thresh/255.0 * 1.0, 4))

# 二值化
img_gray = color.rgb2gray(img)
rows, cols = img_gray.shape
for i in range(rows):
    for j in range(cols):
        if img_gray[i, j] <= thresh/255.0:
            img_gray[i, j] = 0
        else:
            img_gray[i, j] = 1

io.imsave('d:/img1.jpg', img)
io.imsave('d:/img2.jpg', img_gray)
