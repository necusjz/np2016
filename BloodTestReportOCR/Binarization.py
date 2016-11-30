# -*- coding: UTF-8 -*-

from PIL import ImageEnhance
import cv2.cv
from PIL import Image, ImageDraw
import os
# 输入文件
# 创建文件夹
try:
    os.system('mkdir temp bin_pics')
except:
    pass

# ------ 图像去噪 (像素暴力遍历，速度较慢)-------
# 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
# 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 < N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败

def getPixel(image, x, y, G, N):
    L = image.getpixel((x, y))
    if L > G:
        L = True
    else:
        L = False
    nearDots = 0
    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1
    if nearDots < N:
        return image.getpixel((x, y - 1))
    else:
        return None

def clearNoise(image, G, N, Z):
    draw = ImageDraw.Draw(image)
    for i in xrange(0, Z):
        for x in xrange(1, image.size[0] - 1):
            for y in xrange(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)




# 二值化
def Binarization(file_name, save_name):
    # 读取文件
    img = Image.open(file_name)
    # ------ 图像预处理（亮度、对比度、锐度） -------
    # 亮度不变
    imgenhancer_Brightness = ImageEnhance.Brightness(img)
    img_enhance_Brightness = imgenhancer_Brightness.enhance(1.0)
    # 对比度增加
    imgenhancer_Contrast = ImageEnhance.Contrast(img_enhance_Brightness)
    img_enhance_Contrast = imgenhancer_Contrast.enhance(1.6)
    # 锐度降低
    imgenhancer_Sharpness = ImageEnhance.Sharpness(img_enhance_Contrast)
    img_enhance_Sharpness = imgenhancer_Sharpness.enhance(0.5)
    # 保存临时图片
    img_enhance_Sharpness.save("temp/preDeal.jpg")
    # ------ 自适应高斯边缘提取 -------
    imgFile = 'temp/preDeal.jpg'
    # 读取图片
    img = cv2.imread(imgFile)
    # 转为灰度图
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 自适应高斯提取边缘
    imgAdapt = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # 保存临时图片
    cv2.imwrite('temp/Gaussian.jpg', imgAdapt)
    # 去燥
    image = Image.open('temp/Gaussian.jpg')
    # 去噪,G = 50,N = 3,Z = 1
    clearNoise(image, 50, 3, 1)
    # 去噪,G = 50,N = 2,Z = 2
    clearNoise(image, 50, 2, 1)
    # 保存临时图片
    image.save('temp/noise.jpg')
    # -------- 形态学操作 ----------
    img = cv2.imread('temp/noise.jpg')
    # 腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    eroded = cv2.erode(img, kernel)
    # 膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    dilated = cv2.dilate(eroded, kernel)
    # 再次膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(dilated, kernel)
    # 保存图像
    cv2.imwrite(save_name, dilated);
    print save_name + ' done'

